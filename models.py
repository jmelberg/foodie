from google.appengine.ext import ndb
import webapp2_extras.appengine.auth.models as auth_models

''' Foodie and Expert User Models '''
class User(auth_models.User):
  username = ndb.StringProperty()
  email_address = ndb.StringProperty()
  first_name = ndb.StringProperty()
  last_name = ndb.StringProperty()
  zip_code = ndb.IntegerProperty(default = 0)
  credit_card = ndb.IntegerProperty(default = 0)
  security_code = ndb.IntegerProperty(default = 0)
  expiration_date = ndb.DateTimeProperty()
  # Foodie/Expert
  account_type = ndb.StringProperty()

''' Profile entity hold information specific to user on profile '''
class Profile(ndb.Model):
  owner = ndb.KeyProperty(kind= "User")
  about_me = ndb.StringProperty()

''' Handles the basic connection between foodie and expert'''
class Notification(ndb.Model):
  recipient = ndb.KeyProperty(kind="User")
  sender = ndb.KeyProperty(kind="User")
  description = ndb.StringProperty()
  time = ndb.DateTimeProperty(auto_now_add=True)
  priority = ndb.IntegerProperty(default = 0)

class Endorsement(ndb.Model):
  recipient = ndb.KeyProperty(kind="User")
  sender = ndb.KeyProperty(kind="User")
  text = ndb.StringProperty()

''' Handles transations between users '''
class Transaction(ndb.Model):
  sender = ndb.KeyProperty(kind = "User")
  receiver = ndb.KeyProperty(kind = "User")
  amount = ndb.FloatProperty(default = 0)
  description = ndb.StringProperty()
