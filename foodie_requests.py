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

from urllib2 import urlopen
import json

api_key = 'AIzaSyBAO3qaYH4LGQky8vAA07gCVex1LBhUdbE'

class RequestsHandler(SessionHandler):
  ''' Views current requests from other users '''
  @login_required
  def get(self):
    user = self.user_model
    current_date = datetime.datetime.now() - datetime.timedelta(hours=7)
    available_requests = Request.query(Request.start_time > current_date).order(Request.start_time)
    dead_requests = Request.query(Request.start_time <= current_date, Request.sender == user.key).order(Request.start_time)
    
    my_requests = []
    empty_requests = []
    accepted_requests = []
    for request in available_requests:
      if request.sender == user.key:
        # User generated requests
        my_requests.append(request)
      else:
        # Accepted requests
        if request.recipient == user.key:
          accepted_requests.append(request)
        elif request.recipient is None:
          empty_requests.append(request)
          print "Added to empty"
      
    self.response.out.write(template.render('views/requests.html',
                            {'user': user, 'my_requests': my_requests,
                            'empty_requests': empty_requests, 'accepted_requests':accepted_requests,
                            'dead_requests':dead_requests}))


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

class ApproveRequestHandler(SessionHandler):
  ''' Processes current requests and removes from database '''
  def post(self):
    approver = User.query(User.username == cgi.escape(self.request.get('approver'))).get()
    request_key = self.request.get('request')
    
    # Get request
    request = ndb.Key(urlsafe=request_key).get()
    if request != None:
        # TODO Remove request

        # Check if already appended
        if approver.username not in request.recipient_name:
          request.recipient = approver.key
          request.recipient_name.append(approver.username)
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
      city = j['results'][0]['address_components'][3]['long_name']
      state = j['results'][0]['address_components'][5]['long_name']
      zip_code = j['results'][0]['address_components'][7]['long_name']
      current_location= city+ ", "+ state + " " + zip_code
      self.response.out.write(current_location)
    else:
      self.response.out.write("Couldn't find location")



