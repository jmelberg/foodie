import cgi
import webapp2
import time, datetime
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
from models import User, Profile, Request, Endorsement

client_id = 175855
client_secret = 'dfb950e7ea'
redirect_url = 'http://localhost:8080/'
wepay = WePay(False, None)


class LoginHandler(SessionHandler):
  def get(self):
    if self.user_model != None:
      self.redirect('/foodie/{}'.format(self.user_model.username))
    else:
      self.response.out.write(template.render('views/login.html', {}))
  def post(self):
    username = cgi.escape(self.request.get('email')).strip().lower()
    password = cgi.escape(self.request.get('password'))
    try:
      if '@' in username:
        user_login = User.query(User.email_address == username).get()
        if user_login != None:
          username = user_login.username
      u = self.auth.get_user_by_password(username, password, remember=True,
      save_session=True)
      get_notifications(self.user_model)
      self.redirect('/feed')
    except( auth.InvalidAuthIdError, auth.InvalidPasswordError):
      error = "Invalid Email/Password"
      print error
      self.response.out.write(template.render('views/login.html', {'error': error}))

class ProfileHandler(SessionHandler):
  """handler to display a profile page"""
  @login_required
  def get(self, profile_id):
    viewer = self.user_model
    # Get profile info
    profile_owner = User.query(User.username == profile_id).get()
    profile = Profile.query(Profile.owner == profile_owner.key).get()
    if not profile:
      # If profile isn't created, instantiate
      new_profile = Profile()
      new_profile.owner = profile_owner.key
      new_profile.about_me = "I love to eat food"
      new_profile.put()

    current_date = datetime.datetime.now() - datetime.timedelta(hours=8)
    get_notifications(self.user_model)
    # Get comments
    comments = Endorsement.query(Endorsement.recipient == profile_owner.key).order(Endorsement.creation_time).fetch()

    # Get profile history
    history =  Request.query(Request.start_time <= current_date, Request.sender == profile_owner.key).order(Request.start_time)

    self.response.out.write(template.render('views/profile.html',
                             {'owner':profile_owner, 'profile':profile, 'endorsements': comments,
                            'history': history, 'user': viewer}))

class FeedHandler(SessionHandler):
  """handler to display a feed page"""
  def get(self):
    user = self.user_model
    self.response.out.write(template.render('views/feed.html', {'user': self.user_model}))

class Image(SessionHandler):
  """Serves the image associated with an avatar"""
  def get(self):
    """receives user by urlsafe key"""
    user_key = ndb.Key(urlsafe=self.request.get('user_id'))
    height = cgi.escape(self.request.get('height'))
    width = cgi.escape(self.request.get('width'))
    user = user_key.get()
    self.response.headers['content-type'] = 'image/png'
    if len(height) > 0 and len(width) > 0:
      height = int(height)
      width = int(width)
      self.response.out.write(images.resize(user.avatar,height,width))
    else:
      self.response.out.write(user.avatar)


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

class SearchHandler(SessionHandler):
  ''' Search for users by the following criteria:
        Username
        First Name 
        Last Name
        First & Last Name
        Food Type
        Location given City, State
  '''
  def get(self):
    user = self.user_model
    search = self.request.get('search').lower().strip()
    print "Search Term: ", search
    
    #Seach for people
    results = []
    profiles = []
    
    # Search for requests
    available_requests = []
    available_users = []

    completed_requests = []
    completed_users = []
    current_time = datetime.datetime.now() - datetime.timedelta(hours=8)
    
    # Check for type
    food_type_requests = Request.query(Request.food_type == search).fetch()
    food_type = [x for x in food_type_requests if x.start_time > current_time]
    if food_type:
      print "Type Match: "
      for match in food_type:
        sender = User.query(User.username == match.sender_name).get()
        if match.recipient != None:
          print 'STATUS: COMPLETED REQUESTS'
          print match.sender_name, "requested:", match.food_type,"for:", match.start_time, "in:", match.location
          completed_requests.append(match)
          completed_users.append(sender)
        else:
          print 'STATUS: AVAILABLE REQUESTS'
          print match.sender_name, "requested:", match.food_type,"for:", match.start_time, "in:", match.location
          available_requests.append(match)
          available_users.append(sender)

    # Location Search
    location_requests = Request.query(Request.location == search).fetch()
    locations = [x for x in location_requests if x.start_time > current_time]
    if locations:
      print "Location Match: "
      for match in locations:
        sender = User.query(User.username == match.sender_name).get()
        if match.recipient != None:
          print 'STATUS: COMPLETED REQUESTS'
          print match.sender_name, "requested:", match.food_type,"for:", match.start_time, "in:", match.location
          completed_requests.append(match)
          completed_users.append(sender)
        else:
          print 'STATUS: AVAILABLE REQUESTS'
          print match.sender_name, "requested:", match.food_type,"for:", match.start_time, "in:", match.location
          available_requests.append(match)
          available_users.append(sender)

    if ' ' in search:
      search_list = search.split(' ')
      # Full name
      print "Full name search..."
      full_name = User.query(User.l_first_name == search_list[0], User.l_last_name == search_list[1]).fetch()
      for user in full_name:
        profile = Profile.query(Profile.owner == user.key).get()
        results.append(user)
        profiles.append(profile)
    else:
      print "First, last, or username search..."
      search_names = User.query(ndb.OR(User.l_first_name == search, User.l_last_name == search, User.username == search)).fetch()
      for user in search_names:
        profile = Profile.query(Profile.owner == user.key).get()
        results.append(user)
        profiles.append(profile)

    results = zip(results, profiles)
    available = zip(available_users, available_requests)
    completed = zip(completed_users, completed_requests)
    self.response.out.write(template.render('views/search.html',
      {'user':user, 'search_results':results, 'available_requests':available, 'completed_requests':completed}))


class LogoutHandler(SessionHandler):
  """ Terminate current session """
  @login_required
  def get(self):
    print "Log out successful..."
    self.auth.unset_session()
    self.redirect('/')

class GetWePayUserTokenHandler(SessionHandler):
  def get(self):
    self.response.out.write(template.render('views/payments.html', {'user': self.user_model}))

  def post(self):
    user = self.user_model
    code = cgi.escape(self.request.get("acct_json"))
    r = wepay.get_token(redirect_url, client_id, client_secret, code[1:-1])
    acct_token = r["access_token"]
    acct_id = r["user_id"]
    user.wepay_id = str(acct_id)
    user.put()
    
        

config = {}
config['webapp2_extras.sessions'] = {
    'secret_key': 'zomg-this-key-is-so-secret',
}
config['webapp2_extras.auth'] = {
    'user_model': User,
}

app = webapp2.WSGIApplication([
                             ('/', LoginHandler),
                             ('/register', RegisterHandler),
                             ('/checkusername', UsernameHandler),
                             ('/foodie/(\w+)', ProfileHandler),
                             ('/feed', FeedHandler),
                             ('/requests', RequestsHandler),
                             ('/editrequest/(.+)', EditRequestHandler),
                             ('/checktime', CheckTimeConflict),
                             ('/confirm/(.+)', JoinRequestHandler),
                             ('/choose/(.+)', ChooseRequestHandler),
                             ('/comment', CommentHandler),
                             ('/delete', DeleteRequestHandler),
                             ('/cancel', CancelRequestHandler),
                             ('/query', SearchHandler),
                             ('/request', CreateRequestHandler),
                             ('/getlocation', GetLocationHandler),
                             ('/img', Image),
                             ('/notify', SMSHandler),
                             ('/notify_fire', SMSFireHandler),
                             ('/thanks', ThanksHandler),
                             ('/verify/(.+)/(.+)', VerifyHandler),
                             ('/fire/(.w)/(.+)', FireHandler),
                             ('/complete', CompletedRequestHandler), 
                             ('/logout', LogoutHandler),
                             #payment stuff here!
                             #('/createpayment', CreatePaymentHandler),
                             #('/getpayments', GetPaymentHandler),
                             #('/approvepayment', PaymentApprovedHandler),
                             #('/completepayment', CompletePaymentHandler),
                             #('/chargepayment', ChargePaymentHandler),
                             ('/getwepaytoken', GetWePayUserTokenHandler),
                             #('/setwepaytoken/', SetWePayUserTokenHandler),
                              ], debug=False, config=config)
