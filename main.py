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
from models import User, Profile, Request, Endorsement

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
      self.redirect('/foodie/{}'.format(self.user_model.username))
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
    endorsements = Endorsement.query(Endorsement.recipient == profile_owner.key).fetch()
    
    #Get Requests for Notifications
    accepted_requests = []
    new_requests = []

    current_date = datetime.datetime.now() - datetime.timedelta(hours=7)
    
    available_requests = Request.query(Request.sender == profile_owner.key).fetch()
    if available_requests:
      for request in available_requests:
        if request.start_time > current_date and request.recipient != None:
          accepted_requests.append(request)

      viewer.accepted_requests = len(accepted_requests)
    
    # Get new requests
    active_requests = Request.query(Request.start_time > current_date, Request.recipient == None).fetch()
    if active_requests:
      for request in active_requests:
        if request.sender != viewer.key:
          new_requests.append(request)
      viewer.new_requests = len(new_requests)
    viewer.put()

    self.response.out.write(template.render('views/profile.html',
                             {'owner':profile_owner, 'profile':profile, 'endorsements':endorsements, 'user': viewer}))
    
class LogoutHandler(SessionHandler):
  """ Terminate current session """
  @login_required
  def get(self):
    print "Log out successful..."
    self.auth.unset_session()
    self.redirect('/')

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
                             ('/requests', RequestsHandler),
                             ('/editrequest/(.+)', EditRequestHandler),
                             ('/checktime', CheckTimeConflict),
                             ('/confirm/(.+)', ApproveRequestHandler),
                             ('/delete', DeleteRequestHandler),
                             ('/request', CreateRequestHandler),
                             ('/getlocation', GetLocationHandler),
                             ('/logout', LogoutHandler),
                              ], debug=False, config=config)
