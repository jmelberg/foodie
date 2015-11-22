import cgi
import webapp2
import time, datetime
from google.appengine.ext import ndb
from google.appengine.ext.webapp import template
from google.appengine.api import users
from google.appengine.api import images
from webapp2_extras import sessions, auth, json
from basehandler import SessionHandler, login_required
from account_creation import RegisterHandler, UsernameHandler
from foodie_requests import *
from confirmed_requests import *
from wepay import *
from ratings import CreateRating, DeletePending
from payments import CreatePaymentExample, CreatePayment, ChargePayment, AddCreditCard, AuthorizeCreditCard, Charge
from models import User, Profile, Request, Endorsement, Bidder

client_id = 175855
client_secret = 'dfb950e7ea'
redirect_url = 'http://localhost:8080/'
wepay = WePay(False, None)


class LoginHandler(SessionHandler):
  def get(self):
    if self.user_model != None:
      self.redirect('/feed'.format(self.user_model.username))
    else:
      self.response.out.write(template.render('views/login.html', {}))
  def post(self):
    username = cgi.escape(self.request.get('login_email')).strip().lower()
    password = cgi.escape(self.request.get('login_password'))
    try:
      if '@' in username:
        user_login = User.query(User.email_address == username).get()
        if user_login != None:
          username = user_login.username
      u = self.auth.get_user_by_password(username, password, remember=True,
      save_session=True)
      get_notifications(self.user_model)
      self.redirect('/feed')
    except( auth.InvalidAuthIdError, auth.InvalidPasswordError):
      error = "Invalid Email/Password"
      print error
      self.response.out.write(template.render('views/login.html', {'error': error}))

class FeedHandler(SessionHandler):
  def get(self):
    get_notifications(self.user_model)
    self.response.out.write(template.render('views/feed.html',{'user': self.user_model}))

class ProfileHandler(SessionHandler):
  """handler to display a profile page"""
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

    current_date = datetime.datetime.now() - datetime.timedelta(hours=8)
    #get_notifications(self.user_model)

    # Get comments that have match to request
    comments = Endorsement.query(Endorsement.recipient == profile_owner.key).fetch()
    comments = [x for x in comments if x.request != None]


    # Get profile history
    history =  Request.query(Request.start_time <= current_date, Request.sender == profile_owner.key).order(Request.start_time)

    # Get Request regarding the user
    reqs = []
    my_reqs = []
    pending_reqs = []
    accepted_reqs = []
    alloted_time = current_date + datetime.timedelta(hours=2)

    my_reqs = Request.query().order(Request.start_time).fetch()

    for request in my_reqs:
      if len(request.bidders) > 0:
        if request.recipient != None:
          accepted_reqs.append(request)
          my_reqs.remove(request)
        else:
          pending_reqs.append(request)
          my_reqs.remove(request)

    for request in my_reqs:
      if request.sender != viewer.key:
        if request.recipient == None:
          for bid in request.bidders:
            bid = bid.get()
            if bid.name == viewer.username:
              pending_reqs.append(request)
              my_reqs.remove(request)
        else:
          if request.recipient == viewer.key:
            accepted_reqs.append(request)
            my_reqs.remove(request)

    for request in my_reqs:
      if request.sender != viewer.key:
        my_reqs.remove(request)

    result = my_reqs + pending_reqs + accepted_reqs



    self.response.out.write(template.render('views/profile.html',
                             {'owner':profile_owner, 'profile':profile, 'endorsements': comments,
                            'history': history, 'user': viewer, 'result': result}))

class Image(SessionHandler):
  """Serves the image associated with an avatar"""
  def get(self):
    """receives user by urlsafe key"""
    user_key = ndb.Key(urlsafe=self.request.get('user_id'))
    height = cgi.escape(self.request.get('height'))
    width = cgi.escape(self.request.get('width'))
    user = user_key.get()
    self.response.headers['content-type'] = 'image/png'
    if len(height) > 0 and len(width) > 0:
      height = int(height)
      width = int(width)
      self.response.out.write(images.resize(user.avatar,height,width))
    else:
      self.response.out.write(user.avatar)


class CommentHandler(SessionHandler):
  ''' Leave a comment for another user '''
  def post(self):
    user = self.user_model
    rating = cgi.escape(self.request.get('rating'))
    comment = cgi.escape(self.request.get('comment'))
    # Person getting endorsement
    recipient = cgi.escape(self.request.get('recipient'))
    recipient_user = User.query(User.username == recipient).get()
    recipient_key = recipient_user.key

    if comment != None:
      endorsement = Endorsement()
      endorsement.recipient = recipient_key
      endorsement.sender = user.first_name + " " + user.last_name
      endorsement.creation_time = datetime.datetime.now() - datetime.timedelta(hours=8) #PST
      endorsement.rating = rating
      endorsement.text = comment
      endorsement.put()
      # modify rating
      if rating == "positive":
        recipient_user.positive = recipient_user.positive + 1
      elif rating == "neutral":
        recipient_user.neutral = recipient_user.neutral + 1
      else:
        recipient_user.negative = recipient_user.negative + 1
      recipient_user.percent_positive = (recipient_user.positive / (recipient_user.positive + recipient_user.negative)) * 100
      recipient_user.put()

    self.redirect('/foodie/{}'.format(recipient))

class SearchHandler(SessionHandler):
  ''' Search for users by the following criteria:
        Username
        First Name
        Last Name
        First & Last Name
        Food Type
        Location given City, State
  '''
  def get(self):
    user = self.user_model
    search = self.request.get('search').lower().strip()
    print "Search Term: ", search

    #Seach for people
    results = []
    profiles = []

    # Search for requests
    available_requests = []
    available_users = []

    completed_requests = []
    completed_users = []
    current_time = datetime.datetime.now() - datetime.timedelta(hours=8)

    # Check for type
    food_type_requests = Request.query(Request.food_type == search).fetch()
    food_type = [x for x in food_type_requests if x.start_time > current_time]
    if food_type:
      print "Type Match: "
      for match in food_type:
        sender = User.query(User.username == match.sender_name).get()
        if match.recipient != None:
          print 'STATUS: COMPLETED REQUESTS'
          print match.sender_name, "requested:", match.food_type,"for:", match.start_time, "in:", match.location
          completed_requests.append(match)
          completed_users.append(sender)
        else:
          print 'STATUS: AVAILABLE REQUESTS'
          print match.sender_name, "requested:", match.food_type,"for:", match.start_time, "in:", match.location
          available_requests.append(match)
          available_users.append(sender)

    # Location Search
    location_requests = Request.query(Request.location == search).fetch()
    locations = [x for x in location_requests if x.start_time > current_time]
    if locations:
      print "Location Match: "
      for match in locations:
        sender = User.query(User.username == match.sender_name).get()
        if match.recipient != None:
          print 'STATUS: COMPLETED REQUESTS'
          print match.sender_name, "requested:", match.food_type,"for:", match.start_time, "in:", match.location
          completed_requests.append(match)
          completed_users.append(sender)
        else:
          print 'STATUS: AVAILABLE REQUESTS'
          print match.sender_name, "requested:", match.food_type,"for:", match.start_time, "in:", match.location
          available_requests.append(match)
          available_users.append(sender)

    if ' ' in search:
      search_list = search.split(' ')
      # Full name
      print "Full name search..."
      full_name = User.query(User.l_first_name == search_list[0], User.l_last_name == search_list[1]).fetch()
      for user in full_name:
        profile = Profile.query(Profile.owner == user.key).get()
        results.append(user)
        profiles.append(profile)
    else:
      print "First, last, or username search..."
      search_names = User.query(ndb.OR(User.l_first_name == search, User.l_last_name == search, User.username == search)).fetch()
      for user in search_names:
        profile = Profile.query(Profile.owner == user.key).get()
        results.append(user)
        profiles.append(profile)

    results = zip(results, profiles)
    available = zip(available_users, available_requests)
    completed = zip(completed_users, completed_requests)
    self.response.out.write(template.render('views/search.html',
      {'user':user, 'search_results':results, 'available_requests':available, 'completed_requests':completed}))

class LogoutHandler(SessionHandler):
  """ Terminate current session """
  @login_required
  def get(self):
    print "Log out successful..."
    self.auth.unset_session()
    self.redirect('/')

class GetWePayUserTokenHandler(SessionHandler):
  def get(self):
    self.response.out.write(template.render('views/payments.html', {'user': self.user_model}))
  def post(self):
    user = self.user_model
    code = cgi.escape(self.request.get("acct_json"))
    r = wepay.get_token(redirect_url, client_id, client_secret, code[1:-1])
    acct_token = r["access_token"]
    acct_id = r["user_id"]
    user.wepay_id = str(acct_id)
    user.put()

class RatingsHandler(SessionHandler):
    def get(self):
        user = self.user_model
        pending = PendingReview()
        review = pending.query(PendingReview.sender == user.key)
        self.response.out.write(template.render('views/ratings.html', {'rating': review}))
    def post(self):
        user = self.user_model
        rating = Rating()
        pendingkey = cgi.escape(self.request.get("pendingkey"))
        ratingtype = cgi.escape(self.request.get("ratingtype"))
        experience = cgi.escape(self.request.get("experience"))
        enthusiasm = cgi.escape(self.request.get("enthusiasm"))
        friendliness = cgi.escape(self.request.get("friendliness"))
        experiencecomment = cgi.escape(self.request.get("experiencecomments"))
        enthusiasmcomment = cgi.escape(self.request.get("enthusiasmcomments"))
        friendlinesscomment = cgi.escape(self.request.get("friendlinesscomments"))
        recipient = cgi.escape(self.request.get("recipient"))
        experience = int(experience)
        enthusiasm = int(enthusiasm)
        friendliness = int(friendliness)
        rating.person = recipient
        rating.ratingtype = ratingtype
        rating.experience = experience
        rating.enthusiasm = enthusiasm
        rating.friendliness = friendliness
        rating.experienceComments = experiencecomment
        rating.enthusiasmComments = enthusiasmcomment
        rating.friendlinessComments = friendlinesscomment
        rating.put()
        DeletePending(pendingkey)

class PendingRatingHandler(SessionHandler):
    def get(self):
        user = self.user_model
        review = PendingReview().query(PendingReview.sender == user)
        self.response.out.write(template.render('views/pendingratings.html', {'review': review}))

class CreatePendingRatingHandler(SessionHandler):
    def get(self):
        user = self.user_model
        CreateRating("foodie", user.key, user.key)
        CreateRating("expert", user.key, user.key)

class PaymentsViewHandler(SessionHandler):
    def get(self):
        payment = "Yo"
        self.response.out.write(template.render('views/payments.html', {'payments': payment}))

class AuthorizedPaymentHandler(SessionHandler):
    def get(self, request_id, preapproval_id):
        print request_id + ' ' + preapproval_id
        #THIS CODE IS TO CONFIRM THAT PAYMENT IS AUTHORIZED!!!!

        #SOME BOOLEAN IN REQUESTS MODEL THAT PAYMENT IS PROCESSED SET FROM FALSE TO TRUE

        #PREAPPROVAL ID IS ALSO SET INTO THE PREAPPROVAL ID

        self.redirect('/')

class TestPaymentHandler(SessionHandler):
    def get(self):
        user = self.user_model
        pay = CreatePayment("butthole", user.key, user.key, user.key, "69.69", "1526170804", "Hello")

class CreditCardHandler(SessionHandler):
    def get(self):
        self.response.out.write(template.render('views/creditcard.html', {'wutwut': 'inthebutt'}))


class PostCardHandler(SessionHandler):
    def post(self, name, creditcard, expmonth, expyear, cvv, zipcode):
        name = cgi.escape(self.request.get("pendingkey"))
        creditcard = cgi.escape(self.request.get("ratingtype"))
        expmonth = cgi.escape(self.request.get("expmonth"))
        expyear = cgi.escape(self.request.get("expyear"))
        cvv = cgi.escape(self.request.get("cvv"))
        zipcode = cgi.escape(self.request.get("zipcode"))
        add = AddCreditCard(name, creditcard, expmonth, expyear, cvv, zipcode)
        print add
        authorize = AuthorizeCreditCard()
        Charge()

class TestChargeHandler(SessionHandler):
    def get(self):
        #This is to add a credit card, look at the class for parameters...
        add  = AddCreditCard("Chris Navy", "chikorita415@gmail.com", "4242424242424242", "09", "20", "3050 El Camino Real" ,"Santa Clara" ,"CA","193", "95051")
        pay = add.json()
        #This is the credit card id that you use to charge your payments, send this into the Database, in the User Model.
        print pay["credit_card_id"]
        #You need to call the authorize class to be able to use the credit card id.
        authorize = AuthorizeCreditCard(pay["credit_card_id"])
        #This creates the charge. Look at class for Parameters
        Charge("1526170804", pay["credit_card_id"], "7.45", "Test Payment for Foodie")

class ChargeHandler(SessionHandler):
    def get(self):
        Charge("1526170804", "3943601348", "8.41", "Test Payment for Foodie")
        print "Change Created!"

class AuthorizePaymentsHandler(SessionHandler):
    def post(self):
        user = self.user_model
        credit = cgi.escape(self.request.get("credit_card_id"))
        authorize = AuthorizeCreditCard(credit)
        user.credit_id = credit
        user.put()

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
                             ('/feed', FeedHandler),
                             ('/requests', RequestsHandler),
                             ('/editrequest/(.+)', EditRequestHandler),
                             ('/checktime', CheckTimeConflict),
                             ('/confirm/(.+)', JoinRequestHandler),
                             ('/choose/(.+)', ChooseRequestHandler),
                             ('/comment', CommentHandler),
                             ('/delete', DeleteRequestHandler),
                             ('/cancel', CancelRequestHandler),
                             ('/query', SearchHandler),
                             ('/request', CreateRequestHandler),
                             ('/getlocation', GetLocationHandler),
                             ('/img', Image),
                             ('/notify', SMSHandler),
                             ('/notify_fire', SMSFireHandler),
                             ('/thanks', ThanksHandler),
                             ('/verify/(.+)/(.+)', VerifyHandler),
                             ('/fire/(.w)/(.+)', FireHandler),
                             ('/complete', CompletedRequestHandler),
                             ('/creditcard', CreditCardHandler),
                             ('/samplecharge', TestChargeHandler),
                             ('/chargethis', ChargeHandler),
                             ('/postcard', PostCardHandler),
                             ('/paymentauthorized/(.+)/(.+)', AuthorizedPaymentHandler),
                             ('/authorizepayment', AuthorizePaymentsHandler),
                             ('/logout', LogoutHandler),
                             #payment stuff here!
                             #('/createpayment', CreatePaymentHandler),
                             #('/getpayments', GetPaymentHandler),
                             #('/approvepayment', PaymentApprovedHandler),
                             #('/completepayment', CompletePaymentHandler),
                             #('/chargepayment', ChargePaymentHandler),
                             ('/getwepaytoken', GetWePayUserTokenHandler),
                             #('/setwepaytoken/', SetWePayUserTokenHandler),
                              ], debug=False, config=config)
