import cgi
import webapp2
import time, datetime
from google.appengine.ext import ndb
from google.appengine.ext.webapp import template
from google.appengine.api import users
from google.appengine.api import images
from webapp2_extras import sessions, auth, json
from BaseHandler import SessionHandler, login_required
from models import User, Profile, Request, Endorsement

class RegisterHandler(SessionHandler):
  def get(self):
    self.response.out.write(template.render('views/register.html',{}))
  def post(self):
    """Registers the user and updates datastore"""
    username = cgi.escape(self.request.get('username')).strip().lower()
    email = cgi.escape(self.request.get('email')).strip().lower()
    password = cgi.escape(self.request.get('password'))
    unique_properties = ['email_address']

    # Creation of User
    user_data = User.create_user(username, unique_properties, username=username,
                                email_address=email, password_raw=password, verified=False)
    time.sleep(1)
    try:
      u = self.auth.get_user_by_password(username, password, remember=True,
      save_session=True)
      self.redirect('/foodie/{}'.format(self.user_model.username))
    except( auth.InvalidAuthIdError, auth.InvalidPasswordError):
      error = "Invalid Email/Password"
      self.response.out.write(template.render('views/login.html', {'error':error}))

class UsernameHandler(SessionHandler):
  ''' Used to ensure no two users can have the same username '''
  def get(self):
    username = cgi.escape(self.request.get('username'))
    user_query = User.query(User.username == username)
    taken = user_query.get()
    if taken == None:
      self.response.out.write('Username is available')
    else:
      self.response.out.write('Username is taken')

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
      self.response.out.write(template.render('views/login.html', {'error':error}))

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
    self.response.out.write(template.render('views/profile-foodie.html',
                             {'owner':profile_owner, 'profile':profile, 'endorsements':endorsements, 'viewer': viewer}))

class RequestsHandler(SessionHandler):
  ''' Sends request or views current requests from other users '''
  @login_required
  def get(self):
    user = self.user_model
    my_requests = Request.query(Request.sender == user.key).order(-Request.creation_time)
    all_requests = Request.query().order(-Request.creation_time)
    date = datetime.datetime.now() - datetime.timedelta(hours=7)
    hours = str(date.hour)
    if date.minute < 10:
      minutes = "0"+str(date.minute)
    else:
      minutes = str(date.minute)
    current_time = hours+":"+minutes
    available_requests = []
    dead_requests = []
    for request in all_requests:
      print "Request time: ", request.start_time, "Current Time: ", current_time
      if request.start_time >= current_time:
        available_requests.append(request)
      else:
        dead_requests.append(request)
    self.response.out.write(template.render('views/requests.html',
                            {'user': user, 'my_requests': my_requests, "all_requests": available_requests, "dead_requests": dead_requests}))
    





class CreateRequestHandler(SessionHandler):
  @login_required
  def post(self):
    user = self.user_model
    location = cgi.escape(self.request.get("location"))
    date = cgi.escape(self.request.get("date"))
    time = cgi.escape(self.request.get("time"))

    # Create request
    request = Request()
    request.sender = user.key
    request.sender_name = user.username
    request.location = location
    request.date = date
    request.start_time = time
    request.creation_time = datetime.datetime.now() - datetime.timedelta(hours=7) #PST
    request.put()
    self.redirect('/')

class ApproveRequestHandler(SessionHandler):
  ''' Processes current requests and removes from database '''
  def post(self):
    sender = User.query(User.KeyProperty == cgi.escape(self.request.get('sender'))).get()
    receiver = User.query(User.KeyProperty == cgi.escape(self.request.get('receiver'))).get()
    # Get request
    request = Request.query(Request.sender == sender.key, Request.receiver == receiver.key).get()
    if request != None:
        # Remove notification
        request.key.delete()
    self.redirect('/requests')

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
                             ('/confirm', ApproveRequestHandler),
                             ('/request', CreateRequestHandler),
                             ('/logout', LogoutHandler),
                              ], debug=False, config=config)
