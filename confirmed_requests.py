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
    #completed_requests = Request.query(Request.start_time >= current_time,
    #  Request.start_time < max_time).fetch()
    completed_requests = Request.query(Request.start_time >= current_time).fetch()
    completed_requests = [x for x in completed_requests if x.recipient != None and x.status == "accepted"]
    for request in completed_requests:
      send_sms(request)

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
          request.status = "complete"
          request.put()
          #Process payment here
      else:
        print "YOU ARE NOT THERE!"
    else:
      print "Requestor approved"

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
  sender_body = "Please confirm " + acceptor.first_name + "(" + acceptor.telephone + ") showed up. " + sender_short_url
  acceptor_body = "Please confirm " + sender.first_name + "(" + sender.telephone + ") showed up. " + acceptor_short_url
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
