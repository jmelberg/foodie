from google.appengine.ext import ndb
import webapp2_extras.appengine.auth.models as auth_models

''' Foodie and Expert User Models '''
class User(auth_models.User):
  username = ndb.StringProperty()
  email_address = ndb.StringProperty()
  # Foodie/Expert
  account_type = ndb.StringProperty()

''' Profile entity hold information specific to user on profile '''
class Profile(ndb.Model):
  owner = ndb.KeyProperty(kind= "User")
  about_me = ndb.StringProperty()

''' Handles the basic connection between foodie and expert'''
class Request(ndb.Model):
  recipient = ndb.KeyProperty(kind="User")
  sender = ndb.KeyProperty(kind="User")
  sender_name = ndb.StringProperty()
  recipient_name = ndb.StringProperty(repeated=True)
  location = ndb.StringProperty()
  description = ndb.StringProperty()
  creation_time = ndb.DateTimeProperty(auto_now_add=True)
  start_time = ndb.DateTimeProperty()
  priority = ndb.IntegerProperty(default = 0)

class Endorsement(ndb.Model):
  recipient = ndb.KeyProperty(kind="User")
  sender = ndb.KeyProperty(kind="User")
  text = ndb.StringProperty()
  
