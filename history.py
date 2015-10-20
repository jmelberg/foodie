import cgi
import webapp2
import time, datetime
import json
import copy
from google.appengine.ext import ndb
from google.appengine.ext.webapp import template
from google.appengine.api import users
from google.appengine.api import images
from webapp2_extras import sessions, auth
from basehandler import SessionHandler, login_required
from models import User, Profile, Request, Endorsement

class HistoryHandler(SessionHandler):
  ''' Views current requests from other users '''
  @login_required
  def get(self):
    user = self.user_model
    current_date = datetime.datetime.now() - datetime.timedelta(hours=7)
    requested = Request.query(Request.start_time <= current_date, Request.sender == user.key).order(Request.start_time)

    provided = []  
    self.response.out.write(template.render('views/history.html',
                            {'user' : user, 'requested' : requested, 'provided' : provided}))