import cgi
import webapp2
import time
from google.appengine.ext import ndb
from google.appengine.ext.webapp import template
from google.appengine.api import users
from google.appengine.api import images
from webapp2_extras import sessions, auth, json
from BaseHandler import SessionHandler, login_required
from models import User, Profile, Notification

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
    print username
    print password
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
    user = self.user_model
    if user:
      profile_owner = User.query(User.username == profile_id).get()
      profile = Profile.query(Profile.owner == profile_owner.key).get()
      # If profile isn't created, instantiate
      if not profile:
        new_profile = Profile()
        new_profile.owner = profile_owner.key
        new_profile.about_me = "I love to eat food"
        new_profile.put()
      self.response.out.write(template.render('views/profile.html', {'user':user, 'profile':profile}))
    else:
      self.redirect('/')

class NotificationHandler(SessionHandler):
  ''' Sends request or views current requests from other users '''
  @login_required
  def get(self):
    user = self.user_model
    requests = Notification.query(Notification.receipient == user.key).order(-Notification.time)
    self.response.out.write(template.render('#notification view here',
                            {'user': user, 'requests': requests}))

  def post(self):
    sender = self.user_model
    receiver = User.query(User.username == self.request.get('# notification receiver')).get()
    desc = cgi.escape(self.request.get('#notification description'))
    # Check for standing request
    incoming = Notification.query(Notification.sender == receiver.key,
                                  Notification.recipient == sender.key).get()
    outgoing = Notification.query(Notification.recipient == sender.key,
                                  Notification.sender == receiver.key).get()
    # No current request made
    if incoming is None and outgoing is None:
      request = Notification()
      request.sender = sender.key
      request.recipient = receiver.key
      request.description = desc
      request.time = datetime.datetime.now() - datetime.timedelta(hours=7) #PST
      request.put()
    self.redirect('/')

class ApproveRequestHandler(SessionHandler):
  ''' Processes current requests and removes from database '''
  def post(self):
    sender = User.query(User.KeyProperty == cgi.escape(self.request.get('sender'))).get()
    receiver = User.query(User.KeyProperty == cgi.escape(self.request.get('receiver'))).get()
    # Get notification request
    request = Notification.query(Notification.sender == sender.key).get()
    if request != None:
        # Remove notification
        request.key.delete()
    self.redirect('# List of current notifications')

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
                             ('/notifications', NotificationHandler),
                             ('/confirm', ApproveRequestHandler),
                             ('/logout', LogoutHandler),
                              ], debug=False, config=config)
