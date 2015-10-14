import cgi
import webapp2
import time, datetime
import json
from google.appengine.ext import ndb
from google.appengine.ext.webapp import template
from google.appengine.api import users
from google.appengine.api import images
from webapp2_extras import sessions, auth
from basehandler import SessionHandler, login_required
from models import User, Profile, Request, Endorsement
from yelp_api import query_api

from urllib2 import urlopen
import json

api_key = 'AIzaSyBAO3qaYH4LGQky8vAA07gCVex1LBhUdbE'

class RequestsHandler(SessionHandler):
  ''' Views current requests from other users '''
  @login_required
  def get(self):
    user = self.user_model
    request_sort = cgi.escape(self.request.get('requests'))
    current_date = datetime.datetime.now() - datetime.timedelta(hours=7)
    # Return only those two hours or more in future
    alloted_time = current_date + datetime.timedelta(hours=2)
    sorted_requests = []
    available_requests = Request.query(Request.start_time >= alloted_time).order(Request.start_time)
    if request_sort == 'price' or request_sort == 'location':
      sorted_requests = sortRequests(request_sort, alloted_time)

    dead_requests = Request.query(Request.start_time <= alloted_time, Request.sender == user.key).order(Request.start_time)
    my_requests = []
    empty_requests = []
    pending_requests = []
    approved_request = []

    for request in available_requests:
      if request.sender == user.key:
        # User generated requests
        my_requests.append(request)
        # Accepted Personal Request
        if request.recipient != None:
          approved_request.append(request)
      else:
        # Accepted requests
        if request.recipient == user.key:
          pending_requests.append(request)
        else:
          empty_requests.append(request)
          print "Time: ", request.start_time, ' Alloted: ', alloted_time

    user.available_requests = len(empty_requests)
    user.my_requests = len(my_requests)
    user.pending_requests = len(pending_requests)
    user.approved_request = len(approved_request)
    user.put()

    self.response.out.write(template.render('views/requests.html',
                            {'user': user, 'sorted_requests': sorted_requests, 'my_requests': my_requests,
                            'empty_requests': empty_requests, 'pending_requests':pending_requests,
                            'dead_requests':dead_requests, }))

def sortRequests(request_sort, alloted_time):
  ''' Sort requests by location or price '''
  if request_sort == "location":
    print "Sort by location"
    sorted_requests = Request.query().order(Request.location).fetch()
    for request in sorted_requests:
      if request.start_time < alloted_time:
        sorted_requests.remove(request)
  if request_sort == "price":
    print "Sort by price"
    sorted_requests = Request.query().order(Request.min_price).fetch()
    for request in sorted_requests:
      if request.start_time < alloted_time:
        sorted_requests.remove(request)
  return sorted_requests

class CreateRequestHandler(SessionHandler):
  ''' Create request '''
  @login_required
  def get(self):
    user = self.user_model
    self.response.out.write(template.render('views/create_request.html', {'user': user}))

  def post(self):
    user = self.user_model
    location = cgi.escape(self.request.get("location"))
    date = cgi.escape(self.request.get("date"))
    time = cgi.escape(self.request.get("time"))
    min_price = int(cgi.escape(self.request.get("min_price")))
    max_price = int(cgi.escape(self.request.get("max_price")))
    food_type = cgi.escape(self.request.get("food_type"))
    interest = cgi.escape(self.request.get("interest"))

    # Convert date and time to datetime
    format_date = str(date+ " " +time+":00.0")
    start_time = datetime.datetime.strptime(format_date, "%Y-%m-%d %H:%M:%S.%f")
    
    # Create request
    request = Request()
    request.sender = user.key
    request.sender_name = user.username
    request.location = location
    request.start_time = start_time
    request.creation_time = datetime.datetime.now() - datetime.timedelta(hours=7) #PST
    request.min_price = min_price
    request.max_price = max_price
    request.food_type = food_type
    request.interest = interest
    request.put()
    print "Added request to queue"

    self.redirect('/')

class EditRequestHandler(SessionHandler):
  ''' Edit current request '''
  def get(self, request_id):
    user = self.user_model
    request = ndb.Key(urlsafe=request_id).get()
    edit_date = request.start_time.strftime("%Y-%m-%d")
    edit_time = request.start_time.strftime("%H:%M:%S")
    min_price = request.min_price
    max_price = request.max_price
    food_type = request.food_type
    interest = request.interest
    self.response.out.write(template.render('views/edit_request.html', {'request': request, 'edit_time': edit_time, 'edit_date': edit_date}))

  def post(self, request_id):
    print "in post"
    user = self.user_model
    location = cgi.escape(self.request.get("location"))
    date = cgi.escape(self.request.get("date"))
    time = cgi.escape(self.request.get("time"))
    min_price = int(cgi.escape(self.request.get("min_price")))
    max_price = int(cgi.escape(self.request.get("max_price")))
    food_type = cgi.escape(self.request.get("food_type"))
    interest = cgi.escape(self.request.get("interest"))

    previous_request = ndb.Key(urlsafe=request_id).get()
    print location, "date: ", date, "time: ", time, min_price, max_price, food_type, interest
    # Convert date and time to datetime
    if previous_request.start_time.strftime("%H:%M:%S") == time:
      format_date = str(date+ " " + time+ ".0")
    else:
      format_date = str(date+ " " +time+":00.0")
    start_time = datetime.datetime.strptime(format_date, "%Y-%m-%d %H:%M:%S.%f")
    
    if previous_request:
      previous_request.location = location
      previous_request.start_time = start_time
      previous_request.food_type = food_type
      previous_request.interest = interest
      previous_request.min_price = min_price
      previous_request.max_price = max_price
      previous_request.put()
      print "Added request to queue"
    else:
      print "Could not add"

    self.redirect('/')

class JoinRequestHandler(SessionHandler):
  ''' Processes current requests and removes from database '''
  def get(self, request_id):
    request = ndb.Key(urlsafe=request_id).get()
    response = query_api(request.food_type, request.location)
    results = []
    for business in response:
      print business
      location = {}
      if business['name']:
        location['name'] = business['name']
      if business['rating']:
        location['rating'] = business['rating']
      if business['url']:
        location['url'] = business['url']
      if business['image_url']:
        location['image_url'] = business['image_url']
      food_type = []
      for a in business['categories']:
        food_type.append(a[0])
      location['categories'] = food_type
      location['location'] = business['location']['display_address'][0]
      results.append(location)
    print results
    self.response.out.write(template.render('views/confirm_request.html', {'results':results, 'request': request}))
  
  def post(self, request_id):
    location = self.request.get('location')
    print request_id
    print location
    # Get request
    request = ndb.Key(urlsafe=request_id).get()
    if request != None:
        # Check if already appended
        if self.user_model.username not in request.recipient_name:
          request.recipient = self.user_model.key
          request.recipient_name.append(self.user_model.username)
          request.description = location
          request.put()
        else:
          print "Already connected"
    self.redirect('/requests')

class DeleteRequestHandler(SessionHandler):
  ''' Removes request entirely '''
  def post(self):
    user = self.user_model
    request_key = self.request.get('request')
    # Get request
    request = ndb.Key(urlsafe=request_key).get()
    if request.sender == user.key:
      request.key.delete()
      user.open_requests -= 1
      user.put()

    else:
      print "Not permitted to delete"

class CheckTimeConflict(SessionHandler):
  ''' jQuery async function to check time permittance '''
  def get(self):
    user = self.user_model
    date = cgi.escape(self.request.get("date"))
    time = cgi.escape(self.request.get("time"))
    active_request = cgi.escape(self.request.get("edit_request"))
    if active_request:
      edit_request = ndb.Key(urlsafe=active_request).get()

    # Check for lack of values
    if len(date) < 1:
      if active_request:
        date = edit_request.start_time.strftime("%Y-%m-%d")
      else:
        self.response.out.write('Please choose date')

    # Convert date and time to datetime
    format_date = str(date+ " " +time+":00.0")
    start_time = datetime.datetime.strptime(format_date, "%Y-%m-%d %H:%M:%S.%f")

    # Check for current request within time limit
    ongoing_request = Request.query(Request.sender == user.key).fetch()

    # Remove current request if applicable
    if active_request:
      ongoing_request.remove(edit_request)
    alloted_date = start_time + datetime.timedelta(hours=2) #Max limit

    create = timeCheck(ongoing_request, alloted_date, start_time)
    print create
    if create is True:
      self.response.out.write('Available')
    else:
      self.response.out.write('Time Already Passed/Reserved')

def timeCheck(ongoing_request, alloted_date, start_time):
  ''' INPUT: list of requst objects, timeframe in datetime format 
      Returns: True or False if time slot is available
  '''
  create = False
  print "Requested: ", start_time
  print "MAX: ", alloted_date
  current_time = datetime.datetime.now() - datetime.timedelta(hours=7)
  min_time = start_time - datetime.timedelta(hours=2) #Min limit
  # Check to see if time has already passed
  if start_time > current_time:
    # Check for current requests
    if len(ongoing_request) > 0:
      for request in ongoing_request:
        print "Reserved: " , request.start_time
        # Create if time is outside of alloted period
        if request.start_time > alloted_date or request.start_time < min_time:
          create = True
        else:
          create = False
          break
    else:
      create = True
  else:
    print "Request time already passed"
  return create

class GetLocationHandler(SessionHandler):
  def get(self):
    lat = cgi.escape(self.request.get('latitude'))
    lon = cgi.escape(self.request.get('longitude'))
    url = "https://maps.googleapis.com/maps/api/geocode/json?latlng="+ lat + "," + lon + "&key=" + api_key
    v = urlopen(url).read()
    j = json.loads(v)
    if j:
      print j['results'][0]['address_components']
      city = j['results'][0]['address_components'][3]['long_name']
      state = j['results'][0]['address_components'][5]['long_name']
      zip_code = j['results'][0]['address_components'][6]['long_name']
      current_location= city+ ", "+ state + " " + zip_code
      self.response.out.write(current_location)
    else:
      self.response.out.write("Couldn't find location")
