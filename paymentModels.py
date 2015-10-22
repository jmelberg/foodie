import cgi
import urllib2

from google.appengine.ext import ndb
import webapp2_extras.appengine.auth.models as auth_models

#Payment Models

class PaymentAccount(ndb.Model)
    '''
    1. WePay Account Token
    2. FoodieAccountID
    '''
    wepaytoken = ndb.StringProperty()

class Payment(ndb.Model):

    '''
    1. ID
    2. Receiver
    3. Status
    4. Amount
    5. createdAt
    '''

    paymentkey = ndb.KeyProperty()
    paymentid = ndb.StringProperty()
    foodie = ndb.StringProperty()
    expert = ndb.StringProperty()
    foodiePaymentApproved = ndb.BooleanProperty(default=False)
    expertPaymentApproved = ndb.BooleanProperty(default=False)
    foodiePaymentLink = ndb.StringProperty()
    expertPaymentLink = ndb.StringProperty()
    amount = ndb.FloatProperty()
