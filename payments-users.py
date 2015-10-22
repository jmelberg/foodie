import cgi
import urllib
from google.appengine.ext import ndb
import payments

#Get the Account's Permanent Token
#class createToken(code)

class GetWePayUserTokenHandler():
  def get(self):
      redirect_uri = self.
      code = self.
      getToken = wepay.get_token(redirect_uri, client_id, client_secret, code)
      #You Get a Token Here
      #Pass it into the Set User Token Class!
      print:"User Token has been set!"

class SetWePayUserTokenHandler():
  def post(self):
      accessToken =
      #Creating the Merchant Account here!
      createaccount = WePay(production, accessToken)


#Store Token on Server!
