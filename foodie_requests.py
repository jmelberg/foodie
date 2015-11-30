import cgi
import webapp2
import time, datetime
import json
import logging
from google.appengine.ext import ndb
from google.appengine.ext.webapp import template
from google.appengine.api import users
from google.appengine.api import images
from google.appengine.api import urlfetch
from webapp2_extras import sessions, auth
from basehandler import SessionHandler, login_required
from models import User, Profile, Request, Endorsement, Location, Bidder
from yelp_api import query_api
from urllib2 import urlopen
import urllib
import json

from twilio.rest import TwilioRestClient


api_key = 'AIzaSyBAO3qaYH4LGQky8vAA07gCVex1LBhUdbE'

class RequestsHandler(SessionHandler):
  ''' Views current requests from other users '''
  @login_required
  def get(self):
    user = self.user_model
    request_sort = cgi.escape(self.request.get('requests'))
    current_date = datetime.datetime.now() - datetime.timedelta(hours=8)
    # Return only those two hours or more in future
    alloted_time = current_date + datetime.timedelta(minutes=20)
    sorted_requests = []
    available_requests = Request.query(Request.start_time >= alloted_time).order(Request.start_time)
    print "alloted", alloted_time
    print "current", current_date
    if request_sort == 'price' or request_sort == 'location' or request_sort == 'hangouts' or request_sort == 'lessons':
      sorted_requests = sortRequests(request_sort, alloted_time)

    dead_requests = Request.query(Request.start_time <= alloted_time, Request.sender == user.key).order(Request.start_time)
    empty_requests = []
    pending_requests = []
    approved_requests = []

    # Get User requests
    my_requests = Request.query(Request.start_time >= alloted_time - datetime.timedelta(minutes=30),
                                Request.sender == user.key).order(Request.start_time).fetch()

    for request in my_requests:
      if len(request.bidders) > 0:
        if request.recipient != None:
          approved_requests.append(request)
        else:
          pending_requests.append(request)

    for request in available_requests:
      # Get all requests you didn't send
      if request.sender != user.key:
        # Request not accepted yet
        if request.recipient == None:
          # Check for bidders
          for bid in request.bidders:
            bid = bid.get()
            if bid.name == user.username:
              # Bid by user
              pending_requests.append(request)
          empty_requests.append(request)
        else:
          # Request has recipient
          if request.recipient == user.key:
            # You are recipient
            approved_requests.append(request)
        
    # Get sorted requests
    l_requests = Request.query().order(Request.location).fetch()
    location_requests = [r for r in l_requests if r.start_time >= alloted_time ]
    location_requests = [r for r in location_requests if r.recipient == None]

    p_requests = Request.query().order(Request.price).fetch()
    price_requests = [r for r in p_requests if r.start_time >= alloted_time]
    price_requests = [r for r in price_requests if r.recipient == None]

    h_requests = Request.query(Request.interest == 'fun').order(Request.start_time).fetch()
    hangouts_requests = [r for r in h_requests if r.start_time >= alloted_time]
    hangouts_requests = [r for r in h_requests if r.recipient == None]

    fl_requests = Request.query(Request.interest == 'food lesson').order(Request.start_time).fetch()
    foodlesson_requests = [r for r in fl_requests if r.start_time >= alloted_time]
    foodlesson_requests = [r for r in fl_requests if r.recipient == None]

    #user.last_check = datetime.datetime.now() - datetime.timedelta(hours=8)
    #print "Updated check time to: " , user.last_check
    user.put()

    for request in approved_requests:
      print "Approved:"
      print "Request:", request.key.urlsafe()
      print "Sender:", request.sender.urlsafe()
      print "Recipient:", request.recipient.urlsafe()
    
    self.response.out.write(template.render('views/requests.html',
                            {'user': user, 'sorted_requests': sorted_requests, 'my_requests': my_requests,
                            'price_requests': price_requests, 'location_requests': location_requests, 'hangouts_requests': hangouts_requests,
                            'foodlesson_requests': foodlesson_requests, 'empty_requests': empty_requests,
                            'accepted_requests':approved_requests, 'pending_requests': pending_requests}))


def get_notifications(user):
  #Get Requests for Notifications
  accepted_requests = []
  new_requests = []
  current_time = datetime.datetime.now() - datetime.timedelta(hours=8)
  # Check for last login/update
  check_time = user.last_check
  print "Last Check: " , check_time
  if check_time is None:
    # Pull all results from previous week
    check_time = datetime.datetime.now() - datetime.timedelta(days=7, hours=8)
    print "Updated time: ", check_time

  # New requests
  available_requests = Request.query(Request.sender != user.key).fetch()
  available_requests = [r for r in available_requests if r.creation_time >= check_time]
  available_requests = [r for r in available_requests if r.start_time >= current_time]
  available_requests = [r for r in available_requests if r.recipient == None]

  # Approved requests
  approved_requests = Request.query(Request.recipient == user.key).fetch()
  approved_requests = [r for r in approved_requests if r.accept_time != None]
  approved_requests = [r for r in approved_requests if r.start_time >= current_time]
  approved_requests = [r for r in approved_requests if r.accept_time >= check_time]


  # Pending requests
  pend_requests = Request.query(Request.sender == user.key).fetch()
  pend_requests = [r for r in pend_requests if r.start_time >= current_time]
  pend_requests = [r for r in pend_requests if len(r.bidders) > 0]
  new_bidders = 0
  if len(pend_requests) > 0:
    for r in pend_requests:
      for bid in r.bidders:
        bid = bid.get()
        if bid.bid_time != None:
          if bid.bid_time > check_time:
            print "Bid Time: " , bid.bid_time
            new_bidders += 1
  else:
    pend_requests = [r for r in pend_requests if r.creation_time >= check_time]
    print "No bidders: ", pend_requests

  user.pending_requests = new_bidders
  user.available_requests = len(available_requests)
  print len(available_requests)
  user.approved_requests = len(approved_requests)
  print len(approved_requests)
  user.put()
  print "user updated"

class CreateRequestHandler(SessionHandler):
  ''' Create request '''
  @login_required
  def get(self):
    user = self.user_model
    self.response.out.write(template.render('views/create_request.html', {'user': user}))

  def post(self):
    user = self.user_model
    location = cgi.escape(self.request.get("location")).strip().lower()
    date = cgi.escape(self.request.get("date"))
    r_time = cgi.escape(self.request.get("time"))
    price = int(cgi.escape(self.request.get("price")))
    food_type = cgi.escape(self.request.get("food_type")).strip().lower()
    interest = cgi.escape(self.request.get("interest")).strip().lower()

    # Convert date and time to datetime
    format_date = str(date+ " " +r_time+":00.0")
    start_time = datetime.datetime.strptime(format_date, "%Y-%m-%d %H:%M:%S.%f")
    
    # Create request
    request = Request()
    request.sender = user.key
    request.sender_name = user.username
    request.location = location
    request.start_time = start_time
    request.creation_time = datetime.datetime.now() - datetime.timedelta(hours=8) #PST
    request.price = abs(price)
    request.food_type = food_type
    request.interest = interest
    request.status = "waiting for a bid"
    request.put()
    print "Added request to queue"
    time.sleep(1)
    self.redirect('/')

class EditRequestHandler(SessionHandler):
  ''' Edit current request '''
  @login_required
  def get(self, request_id):
    user = self.user_model
    request = ndb.Key(urlsafe=request_id).get()
    edit_date = request.start_time.strftime("%Y-%m-%d")
    edit_time = request.start_time.strftime("%H:%M:%S")
    price = request.price
    food_type = request.food_type
    interest = request.interest

    self.response.out.write(template.render('views/edit_request.html', {'user': self.user_model, 'request': request, 'edit_time': edit_time, 'edit_date': edit_date}))

  def post(self, request_id):
    print "in post"
    user = self.user_model
    location = cgi.escape(self.request.get("location"))
    date = cgi.escape(self.request.get("date"))
    time = cgi.escape(self.request.get("time"))
    price = int(cgi.escape(self.request.get("price")))
    food_type = cgi.escape(self.request.get("food_type"))
    interest = cgi.escape(self.request.get("interest"))

    previous_request = ndb.Key(urlsafe=request_id).get()
    print location, "date: ", date, "time: ", time, price, food_type, interest
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
      previous_request.price = abs(price)
      previous_request.put()
      print "Added request to queue"
    else:
      print "Could not add"

    self.redirect('/foodie/{}'.format(user.username) + "?q=timeline/all")

class ChooseRequestHandler(SessionHandler):
  @login_required
  def get(self, request_id):
    user = self.user_model
    request = ndb.Key(urlsafe = request_id).get()
    bidders = []
    locations = []
    for bid in request.bidders:
      bid = bid.get()
      bidders.append(bid)
      locations.append(bid.location.get())
    choices = zip(bidders, locations)
    self.response.out.write(template.render('views/choose_request.html', {'user': self.user_model,'request':request,'bids': choices}))

  def post(self, request_id):
    request = ndb.Key(urlsafe = request_id).get()
    bidder = ndb.Key(urlsafe = cgi.escape(self.request.get('bidder'))).get()
    request.recipient = bidder.sender
    request.recipient_name = bidder.name
    request.accept_time = datetime.datetime.now() - datetime.timedelta(hours=8)
    # Get location data
    location = bidder.location.get()
    request.latitude = location.latitude
    request.longitude = location.longitude
    request.status = "accepted"
    request.put()

class JoinRequestHandler(SessionHandler):
  ''' Processes current requests and removes from database '''
  @login_required
  def get(self, request_id):
    user = self.user_model
    request = ndb.Key(urlsafe=request_id).get()
    if request.location is None or request.food_type is None:
      self.redirect('/feed')
    response = query_api(request.food_type, request.location)
    results = []
    for business in response:
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
      if business['location']['display_address']:
        location_string =""
        for a in business['location']['display_address']:
          location_string +=a + " " 
        location['location'] = location_string
      if business['location']['coordinate']:
        coordinates = ""
        for a in business['location']['coordinate']:
          coordinates += str(business['location']['coordinate'][a]) + " "
        location["coordinates"] = coordinates
      results.append(location)
    self.response.out.write(template.render('views/confirm_request.html', {'user': self.user_model,'results':results, 'request': request}))
  
  def post(self, request_id):
    location = self.request.get('location')
    # Get request
    request = ndb.Key(urlsafe=request_id).get()
    location = location.split('^')

    # Check if location has been previously used
    existing_location = Location.query(Location.name == location[0], Location.address == location[1]).get()
    if existing_location is None:
      # Add new location
      categories = location[3].split(',')
      coordinates = location[4].split(' ')
      new_location = Location()
      new_location.name = location[0]
      new_location.address = location[1]
      new_location.image_url = location[2]
      for c in categories:
        new_location.categories.append(c)
      new_location.longitude = float(coordinates[0])
      new_location.latitude = float(coordinates[1])
      new_location.put()
      
    else:
      new_location = existing_location

    if request != None:
      # Check if already appended
      add = True
      if len(request.bidders) > 0:
        for bid in request.bidders:
          bid = bid.get()
          if bid.name == self.user_model.username:
            print "Already bid"
            add = False
      if add is True:
          print "Haven't bid"
          bidder = Bidder()
          bidder.sender = self.user_model.key
          bidder.location = new_location.key
          bidder.name = self.user_model.username
          bidder.bid_time = datetime.datetime.now() - datetime.timedelta(hours=8)
          bidder.price = request.price
          bidder.put()
          request.bidders.append(bidder.key)
          request.status = "pending"
          request.put()
    else:
      print "Already connected"

    self.redirect('/feed')

class DeleteRequestHandler(SessionHandler):
  ''' Removes request entirely '''
  @login_required
  def post(self):
    user = self.user_model
    request_key = self.request.get('request')
    # Get request
    request = ndb.Key(urlsafe=request_key).get()
    if request.sender == user.key:
      request.key.delete()
    else:
      print "Not permitted to delete"

class CancelRequestHandler(SessionHandler):
  @login_required
  def post(self):
    user = self.user_model
    request_key = self.request.get('request')
    request = ndb.Key(urlsafe = request_key).get()
    cancel_bid = ""
    # See if pending or completed
    if request.recipient != None:
      request.recipient = None
      request.recipient_name = None
      request.status = "pending"

    for bid in request.bidders:
      bid = bid.get()
      if bid.sender == user.key:
        cancel_bid = bid
        print "Removing from request"

    if cancel_bid != "":
      request.bidders.remove(cancel_bid.key)

    # Change state of request
    if len(request.bidders) > 0:
      request.status = "pending"
    else:
      request.status = "waiting for bid"

    request.put()


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
    alloted_date = start_time + datetime.timedelta(minutes=20) #Max limit

    create = timeCheck(ongoing_request, alloted_date, start_time)
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
  current_time = datetime.datetime.now() - datetime.timedelta(hours=8)
  min_time = start_time - datetime.timedelta(minutes=20) #Min limit
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

