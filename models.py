from google.appengine.ext import ndb
import webapp2_extras.appengine.auth.models as auth_models

''' Foodie and Expert User Models '''
class User(auth_models.User):
  username = ndb.StringProperty()
  email_address = ndb.StringProperty()
  first_name = ndb.StringProperty()
  last_name = ndb.StringProperty()
  l_first_name = ndb.StringProperty()
  l_last_name = ndb.StringProperty()
  zip_code = ndb.IntegerProperty(default = 0)
  wepay_id = ndb.StringProperty()
  avatar = ndb.BlobProperty()
  telephone = ndb.StringProperty()
  credit_id = ndb.StringProperty()

  # Notifications
  available_requests = ndb.IntegerProperty(default=0)
  my_requests = ndb.IntegerProperty(default = 0)
  accepted_requests = ndb.IntegerProperty(default = 0)
  pending_requests = ndb.IntegerProperty(default = 0)
  approved_requests = ndb.IntegerProperty(default = 0)
  last_check = ndb.DateTimeProperty()

  #ratings
  positive = ndb.FloatProperty(default = 0)
  neutral = ndb.FloatProperty(default = 0)
  negative = ndb.FloatProperty(default = 0)
  percent_positive = ndb.FloatProperty(default = 0)


''' Profile entity hold information specific to user on profile '''
class Profile(ndb.Model):
  owner = ndb.KeyProperty(kind = "User")
  about_me = ndb.StringProperty()


''' Handles the basic connection between foodie and expert'''
class Request(ndb.Model):
  recipient = ndb.KeyProperty(kind="User")
  sender = ndb.KeyProperty(kind="User")
  sender_name = ndb.StringProperty()
  recipient_name = ndb.StringProperty()
  location = ndb.StringProperty()
  creation_time = ndb.DateTimeProperty(auto_now_add=True)
  start_time = ndb.DateTimeProperty()
  accept_time = ndb.DateTimeProperty()
  price = ndb.IntegerProperty(default=0)
  food_type = ndb.StringProperty()
  interest = ndb.StringProperty()
  bidders = ndb.KeyProperty(kind="Bidder", repeated=True)
  bidder_names = ndb.StringProperty(repeated=True)
  status= ndb.StringProperty()
  longitude = ndb.FloatProperty()
  latitude = ndb.FloatProperty()

class Bidder(ndb.Model):
  sender = ndb.KeyProperty(kind="User")
  location = ndb.KeyProperty(kind="Location")
  name = ndb.StringProperty()
  price = ndb.IntegerProperty(default = 0)
  bid_time = ndb.DateTimeProperty()

class Location(ndb.Model):
  name = ndb.StringProperty()
  address = ndb.StringProperty()
  image_url = ndb.StringProperty()
  rating = ndb.StringProperty()
  categories = ndb.StringProperty(repeated = True)
  longitude = ndb.FloatProperty()
  latitude = ndb.FloatProperty()

class Endorsement(ndb.Model):
  recipient = ndb.KeyProperty(kind="User")
  sender = ndb.KeyProperty(kind="User")
  sender_name = ndb.StringProperty()
  creation_time = ndb.DateTimeProperty(auto_now_add=True)
  rating = ndb.StringProperty()
  text = ndb.StringProperty()
  request = ndb.KeyProperty(kind="Request")

''' Handles transations between users '''
class Transaction(ndb.Model):
  sender = ndb.KeyProperty(kind = "User")
  receiver = ndb.KeyProperty(kind = "User")
  amount = ndb.FloatProperty(default = 0)
  description = ndb.StringProperty()

class Rating(ndb.Model):
    person = ndb.StringProperty()
    ratingtype = ndb.StringProperty()
    experience = ndb.IntegerProperty()
    enthusiasm = ndb.IntegerProperty()
    friendliness = ndb.IntegerProperty()
    experienceComments = ndb.StringProperty()
    enthusiasmComments = ndb.StringProperty()
    friendlinessComments = ndb.StringProperty()

class PendingReview(ndb.Model):
    ratingtype = ndb.StringProperty()
    sender = ndb.KeyProperty(kind="User")
    recipient = ndb.KeyProperty(kind="User")
    date = ndb.DateTimeProperty(auto_now_add=True)
