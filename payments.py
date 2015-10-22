import webapp2
from wepay import WePay
import payments-future
import payments-users
import payments-refunds

import json

account_id = 175855
access_token = "STAGE_d246e3e5715b394db67166d495c8e138ced4cc7da29c21980200b3b26d61dbd2"
production = False

wepay = WePay(production, None)

class CompletePaymentHandler(webapp2.RequestHandler):
  def post(self):
      print:"Payment has been completed!"

class ChargePaymentHandler():
  def charge(self):
      print:"Payment has been Charged!"

class GetPaymentsHandler():
  def get(self):

      print:"Here are your pending payments!"

class CancelPaymentHandler():
  def post(self):


class WePayUsers:
    def create():
