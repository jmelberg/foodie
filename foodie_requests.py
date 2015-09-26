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
  ''' Create request from html modal '''
  @login_required
  def post(self):
    user = self.user_model
    location = cgi.escape(self.request.get("location"))
    date = cgi.escape(self.request.get("date"))
    time = cgi.escape(self.request.get("time"))
    min_price = int(cgi.escape(self.request.get("min_price")))
    max_price = int(cgi.escape(self.request.get("max_price")))

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
    request.put()
    print "Added request to queue"
    #Increment open requests
    user.open_requests += 1
    user.put()

    self.redirect('/')

class EditRequestHandler(SessionHandler):
  ''' Edit current request '''
  def post(self):
    user = self.user_model
    location = cgi.escape(self.request.get("edit_location"))
    date = cgi.escape(self.request.get("edit_date"))
    time = cgi.escape(self.request.get("edit_time"))
    min_price = int(cgi.escape(self.request.get("edit_min_price")))
    max_price = int(cgi.escape(self.request.get("edit_max_price")))

    previous_request_key = cgi.escape(self.request.get("request"))
    previous_request = ndb.Key(urlsafe=previous_request_key).get()
    if previous_request:
      previous_request.delete()
    
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
    request.put()
    print "Added request to queue"

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
          # Decrement open requests
          approver.open_requests -= 1
          approver.put()
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
    active_request = cgi.escape(self.request.get("active_request"))
    print "======="
    print active_request
    # Convert date and time to datetime
    format_date = str(date+ " " +time+":00.0")
    start_time = datetime.datetime.strptime(format_date, "%Y-%m-%d %H:%M:%S.%f")

    # Check for current request within time limit
    ongoing_request = Request.query(Request.sender == user.key).fetch()
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
  if len(ongoing_request) > 0:
    for request in ongoing_request:
      print "Reserved: " , request.start_time
      if request.start_time > alloted_date or request.start_time < start_time:
        if start_time > current_time:
          create = True
        else:
          print "Request time already passed"
          break
      else:
        create = False
        break
  else:
    create = True
  return create

class ReturnRequestHandler(SessionHandler):
  ''' Returns request object specifics '''
  def get(self):
    user = self.user_model
    print "In Return"
    key = cgi.escape(self.request.get("key"))
    request = ndb.Key(urlsafe=key).get()
    date = request.start_time.strftime("%B %d, %Y")
    time = request.start_time.strftime("%H:%M:%S")
    min_price = request.min_price
    max_price = request.max_price
    if request:
      results = {"location": request.location, "date": date, "time_slot": time,
      'min_price':min_price, 'max_price':max_price,}
      self.response.out.write(json.dumps(results), )
    else:
      self.response.out.write("None")
