__author__ = 'chrisnavy'
from google.appengine.ext import ndb
import webapp2_extras.appengine.auth.models as auth_models

#Payment Models

class payment(ndb.Model):
    '''
    1. ID
    2. Receiver
    3. Status
    4. Amount
    5. createdAt
    '''
