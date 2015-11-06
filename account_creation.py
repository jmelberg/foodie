import cgi
import webapp2
import time, datetime
from google.appengine.ext import ndb
from google.appengine.ext.webapp import template
from google.appengine.api import users
from google.appengine.api import images
from webapp2_extras import sessions, auth, json
from basehandler import SessionHandler, login_required
from models import User, Profile, Request, Endorsement

class RegisterHandler(SessionHandler):
  def get(self):
    self.response.out.write(template.render('views/register.html',{}))
  def post(self):
    """Registers the user and updates datastore"""
    username = cgi.escape(self.request.get('username')).strip().lower()
    email = cgi.escape(self.request.get('email')).strip().lower()
    password = cgi.escape(self.request.get('password'))
    first_name = cgi.escape(self.request.get('first_name')).strip()
    last_name = cgi.escape(self.request.get('last_name')).strip()
    l_first_name = first_name.lower()
    l_last_name = last_name.lower()
    avatar= self.request.get('img')
    avatar = images.resize(avatar,400,400) 
    
    unique_properties = ['email_address']

    # Creation of User
    user_data = User.create_user(username, unique_properties, username=username,
                                email_address=email, password_raw=password, first_name = first_name,
                                last_name=last_name, l_first_name = l_first_name, l_last_name = l_last_name,
                                avatar = avatar, verified=False)
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
    if len(username) < 4:
    	self.response.out.write('Username must be between 4 to 16 characters')
    elif len(username) > 16:
    	self.response.out.write('Username must be between 4 to 16 characters')
    else:
    	if taken == None:
    		self.response.out.write('Username is available')
    	else:
    		self.response.out.write('Username is taken')