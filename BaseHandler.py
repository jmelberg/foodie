import webapp2
from google.appengine.ext import ndb
from google.appengine.ext.webapp import template
from google.appengine.api import users
import webapp2_extras.appengine.auth.models as auth_models
from webapp2_extras import sessions, auth

''' Handles the user's session upon loggin in/out '''
class SessionHandler(webapp2.RequestHandler):
  @webapp2.cached_property
  def session_store(self):
    return sessions.get_store(request=self.request)

  @webapp2.cached_property
  def session(self):
    return self.session_store.get_session(backend="datastore")

  def dispatch(self):        
    try:
      super(SessionHandler, self).dispatch()
    finally:
      # Save the session after each request        
      self.session_store.save_sessions(self.response)

  @webapp2.cached_property
  def auth(self):
    return auth.get_auth(request=self.request)
    
  @webapp2.cached_property
  def user(self):
    user = self.auth.get_user_by_session()
    return user
    
  @webapp2.cached_property
  def user_model(self):
    user_model, timestamp = self.auth.store.user_model.get_by_auth_token(
      self.user['user_id'], self.user['token']) if self.user else (None, None)
    return user_model

  @webapp2.cached_property
  def user_info(self):
    return self.auth.get_user_by_session()

def login_required(handler):
  "Requires that a user be logged in to access the given resource"
  def check_login(self, *args, **kwargs):     
    if not self.user:
      return self.redirect('/')
    else:
      return handler(self, *args, **kwargs)
  return check_login

