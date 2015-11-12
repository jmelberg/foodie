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


class SMSHandler(SessionHandler):
  def get(self):
    current_time = datetime.datetime.now() - datetime.timedelta(hours=8)
    max_time = current_time - datetime.timedelta(minutes=30)
    # Get all requests in accepted state
    completed_requests = Request.query(Request.start_time >= current_time, Request.start_time < max_time).fetch()
    completed_requests = [x for x in completed_requests if x.recipient != None and x.status == "accepted"]
    for request in completed_requests:
      send_sms(request)

class SMSFireHandler(SessionHandler):
  # Option to fire after 10 minutes has passed
  def get(self):
    current_time = datetime.datetime.now() - datetime.timedelta(hours=8)
    max_time = current_time + datetime.timedelta(minutes=10)
    # Get all requests in accepted state
    completed_requests = Request.query(Request.start_time >= max_time, Request.start_time < current_time).fetch()
    completed_requests = [x for x in completed_requests if x.recipient != None and x.status == "foodie"]
    for request in completed_requests:
      send_fire_notification(request)

class FireHandler(SessionHandler):
  # Fires food expert
  def get(self, request_id, employee_id):
    request = ndb.Key(urlsafe=request_id).get()
    receiver = ndb.Key(urlsafe=employee_id).get()
    if request.status == "foodie":
      request.status = "fired"
      send_fire(request)
      self.response.out.write(template.render('views/fired.html', {}))
    else:
      self.response.out.write(template.render('views/showed.html', {}))


class VerifyHandler(SessionHandler):
  def get(self, request_id, message_id):
    request = ndb.Key(urlsafe=request_id).get()
    receiver = ndb.Key(urlsafe=message_id).get()
    print "Receiver of message: ", receiver.username
    if request.status == "complete":
      self.response.out.write(template.render('views/thanks.html', {}))
    else:
      self.response.out.write(template.render('views/verify_state.html', {'receiver': receiver, 'request': request}))


class CompletedRequestHandler(SessionHandler):
  def get(self):
    latitude = cgi.escape(self.request.get("latitude"))
    longitude = cgi.escape(self.request.get("longitude"))
    message_id = cgi.escape(self.request.get("message"))
    request_id = cgi.escape(self.request.get("request"))
    user_key = ndb.Key(urlsafe=message_id).get()
    request = ndb.Key(urlsafe=request_id).get()
    print "Request:", request.longitude, request.latitude
    print "Actual:", longitude, latitude

    if request.recipient == user_key:
      if latitude <= (request.latitude - 0.01) or latitude >= (request.latitude + 0.01):
        if longitude <= (request.longitude - 0.01) or longitude >= (request.longitude + 0.01):
          print "Expert approved!"
          if request.status == "foodie":
            #Foodie checked in already
            request.status = "complete"
          elif request.status == "approved":
            #Expert is first to check in
            request.status = "expert"
          else:
            # Request has expired
            print "Request is no longer valid"
          request.put()
          #Process payment here
      else:
        print "YOU ARE NOT THERE!"
    else:
      if latitude <= (request.latitude - 0.01) or latitude >= (request.latitude + 0.01):
        if longitude <= (request.longitude - 0.01) or longitude >= (request.longitude + 0.01):
          print "Requestor approved"
          if request.status == "expert":
            request.status = "complete"
          elif request.status =="approved":
            request.status = "foodie"
          else:
            # Request has experied / fired
            print "Request is no longer valid"
          request.put()
      else:
        print "YOU ARE NOT THERE! Nice try!"

class ThanksHandler(SessionHandler):
  def get(self):
    self.response.out.write(template.render('views/thanks.html', {}))    


def shorten_url(url):
  post_url = 'https://www.googleapis.com/urlshortener/v1/url?key='+api_key
  postdata = json.dumps({'longUrl':url})
  result = urlfetch.fetch(url=post_url, payload=postdata,
    method=urlfetch.POST,
    headers={'Content-Type':'application/json'})
  return json.loads(result.content)['id']

def send_sms(request):
  AUTH_TOKEN = '3d55c9d85ab388eacc42e8cfb1ad06e4'
  ACCOUNT_SID = 'AC8d1e55b2a96dde764f3b6df1313bc3d1'
  twilio_number = '+16503992009'

  sender = User.query(User.username == request.sender_name).get()
  acceptor = User.query(User.username == request.recipient_name).get()
  print "Sender: ", sender.username
  print "Acceptor:", acceptor.username
  key = request.key.urlsafe()
  sender_key = sender.key.urlsafe()
  acceptor_key = acceptor.key.urlsafe()

  sender_short_url = shorten_url("http://localhost:8080/verify/" + key + "/" + sender_key)
  acceptor_short_url = shorten_url("http://localhost:8080/verify/" + key +"/" + acceptor_key)
  print sender_short_url
  print acceptor_short_url
  client = TwilioRestClient(ACCOUNT_SID, AUTH_TOKEN)
  #Send to creator
  print("Sending message to ", sender.telephone)
  print("Sending message to ", acceptor.telephone)
  sender_body = "Please contact " + acceptor.first_name + "(" + acceptor.telephone + ") if needed. " + "Check in: " + sender_short_url
  acceptor_body = "Please contact " + sender.first_name + "(" + sender.telephone + ") if needed. " + "Check in: " + acceptor_short_url
  #Send to poster
  client.messages.create(
    to = (sender.telephone),
    from_ = twilio_number,
    body = sender_body
  )
  #Send to acceptor
  client.messages.create(
    to = (acceptor.telephone),
    from_ = twilio_number,
    body = acceptor_body
  )

def send_fire_notifiation(request):
  AUTH_TOKEN = '3d55c9d85ab388eacc42e8cfb1ad06e4'
  ACCOUNT_SID = 'AC8d1e55b2a96dde764f3b6df1313bc3d1'
  twilio_number = '+16503992009'

  sender = User.query(User.username == request.sender_name).get()
  acceptor = User.query(User.username == request.recipient_name).get()
  print "Sender: ", sender.username
  print "Acceptor:", acceptor.username
  key = request.key.urlsafe()
  sender_key = sender.key.urlsafe()
  acceptor_key = acceptor.key.urlsafe()

  sender_short_url = shorten_url("http://localhost:8080/fire/" + key + "/" + acceptor_key)
  print sender_short_url
  client = TwilioRestClient(ACCOUNT_SID, AUTH_TOKEN)
  #Send to creator
  print("Sending option to fire message to ", sender.telephone)
  sender_body = acceptor.first_name + "(" + acceptor.telephone + ") hasn't checked in. Fire " + acceptor.first_name + "? "  + sender_short_url
  #Send to poster
  client.messages.create(
    to = sender.telephone,
    from_ = twilio_number,
    body = sender_body
  )

def send_fire(request):
  AUTH_TOKEN = '3d55c9d85ab388eacc42e8cfb1ad06e4'
  ACCOUNT_SID = 'AC8d1e55b2a96dde764f3b6df1313bc3d1'
  twilio_number = '+16503992009'

  sender = User.query(User.username == request.sender_name).get()
  acceptor = User.query(User.username == request.recipient_name).get()
  print "Acceptor:", acceptor.username
  key = request.key.urlsafe()
  sender_key = sender.key.urlsafe()
  acceptor_key = acceptor.key.urlsafe()

  client = TwilioRestClient(ACCOUNT_SID, AUTH_TOKEN)
  #Send to expert
  print("Sending option to fire message to ", acceptor.telephone)
  acceptor_body = sender.first_name +" fired you. Please make it to your event next time."
  client.messages.create(
    to = acceptor.telephone,
    from_ = twilio_number,
    body = accepter_body
  )

