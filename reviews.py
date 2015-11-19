import cgi
import webapp2
import time, datetime
import requests
from google.appengine.ext import ndb
from google.appengine.ext.webapp import template
from google.appengine.api import users
from google.appengine.api import images
from webapp2_extras import sessions, auth, json
from basehandler import SessionHandler, login_required
from account_creation import RegisterHandler, UsernameHandler
from foodie_requests import *
from confirmed_requests import *
from wepay import *
from models import User, Profile, Request, Endorsement, Rating, PendingReview
from ratings import CreateRating, DeletePending

class CommentHandler(SessionHandler):
  ''' Leave a comment for another user '''
  def post(self):
    user = self.user_model
    rating = cgi.escape(self.request.get('rating'))
    comment = cgi.escape(self.request.get('comment'))
    # Person getting endorsement
    recipient = cgi.escape(self.request.get('recipient'))
    recipient_user = User.query(User.username == recipient).get()
    recipient_key = recipient_user.key

    if comment != None:
      endorsement = Endorsement()
      endorsement.recipient = recipient_key
      endorsement.sender = user.first_name + " " + user.last_name
      endorsement.creation_time = datetime.datetime.now() - datetime.timedelta(hours=8) #PST
      endorsement.rating = rating
      endorsement.text = comment
      endorsement.put()
      # modify rating
      if rating == "positive":
        recipient_user.positive = recipient_user.positive + 1
      elif rating == "neutral":
        recipient_user.neutral = recipient_user.neutral + 1
      else:
        recipient_user.negative = recipient_user.negative + 1
      recipient_user.percent_positive = (recipient_user.positive / (recipient_user.positive + recipient_user.negative)) * 100
      recipient_user.put()

    self.redirect('/foodie/{}'.format(recipient))
class RatingsHandler(SessionHandler):
  def get(self):
    user = self.user_model
    pending = PendingReview()
    review = pending.query(PendingReview.sender == user.key)
    self.response.out.write(template.render('views/ratings.html', {'rating': review}))
  def post(self):
    user = self.user_model
    rating = Rating()
    pendingkey = cgi.escape(self.request.get("pendingkey"))
    ratingtype = cgi.escape(self.request.get("ratingtype"))
    experience = cgi.escape(self.request.get("experience"))
    enthusiasm = cgi.escape(self.request.get("enthusiasm"))
    friendliness = cgi.escape(self.request.get("friendliness"))
    experiencecomment = cgi.escape(self.request.get("experiencecomments"))
    enthusiasmcomment = cgi.escape(self.request.get("enthusiasmcomments"))
    friendlinesscomment = cgi.escape(self.request.get("friendlinesscomments"))
    recipient = cgi.escape(self.request.get("recipient"))
    experience = int(experience)
    enthusiasm = int(enthusiasm)
    friendliness = int(friendliness)
    rating.person = recipient
    rating.ratingtype = ratingtype
    rating.experience = experience
    rating.enthusiasm = enthusiasm
    rating.friendliness = friendliness
    rating.experienceComments = experiencecomment
    rating.enthusiasmComments = enthusiasmcomment
    rating.friendlinessComments = friendlinesscomment
    rating.put()
    DeletePending(pendingkey)

class PendingRatingHandler(SessionHandler):
  def get(self):
    user = self.user_model
    review = PendingReview().query(PendingReview.sender == user)
    self.response.out.write(template.render('views/pendingratings.html', {'review': review}))

class CreatePendingRatingHandler(SessionHandler):
  def get(self):
    user = self.user_model
    CreateRating("foodie", user.key, user.key)
    CreateRating("expert", user.key, user.key)
