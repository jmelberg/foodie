from google.appengine.ext import ndb
import webapp2_extras.appengine.auth.models as auth_models

''' Foodie and Expert User Models '''
class User(auth_models.User):
  username = ndb.StringProperty()
  email_address = ndb.StringProperty()

''' Profile entity hold information specific to user on profile '''
class Profile(ndb.Model):
  owner = ndb.KeyProperty(kind= "User")
  about_me = ndb.StringProperty()

''' Handles the basic connection between foodie and expert'''
class Notification(ndb.Model):
  recepient = ndb.KeyProperty(kind="User")
  sender = ndb.KeyProperty(kind="User")
  description = ndb.StringProperty()
  time = ndb.DateTimeProperty(auto_now_add=True)
  priority = ndb.IntegerProperty(default = 0)
