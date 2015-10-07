import cgi
import requests, json
import paypalrestsdk
from requests_oauth2 import OAuth2

config = paypalrestsdk.configure({
    'mode': 'sandbox',
    'client_id': 'AQkquBDf1zctJOWGKWUEtKXm6qVhueUEMvXO_-MCI4DQQ4-LWvkDLIN2fGsd',
    'client_secret': 'EL1tVxAjhT7cJimnz5-Nsx9k2reTKSVfErNQF-CmrwJgxRtylkGTKlU4RvrX'
})


client_secret = "EL1tVxAjhT7cJimnz5-Nsx9k2reTKSVfErNQF-CmrwJgxRtylkGTKlU4RvrX"

paypal_url = 'https://api.sandbox.paypal.com'


''' CREATE PAYPAL TOKEN WITHOUT USING SDK '''

api = paypalrestsdk.set_config(
  mode="sandbox", # sandbox or live
  client_id = "AQkquBDf1zctJOWGKWUEtKXm6qVhueUEMvXO_-MCI4DQQ4-LWvkDLIN2fGsd",
  client_secret='EL1tVxAjhT7cJimnz5-Nsx9k2reTKSVfErNQF-CmrwJgxRtylkGTKlU4RvrX')
print api.get_access_token()

price = input('Enter the price transaction in $')

payment = paypalrestsdk.Payment({
  "intent": "sale",
  "payer": {
    "payment_method": "paypal" },
  "redirect_urls": {
    "return_url": "https://devtools-paypal.com/guide/pay_paypal/python?success=true",
    "cancel_url": "https://devtools-paypal.com/guide/pay_paypal/python?cancel=true" },

  "transactions": [ {
    "amount": {
      "total": price,
      "currency": "USD" },
    "description": "creating a payment" } ] } )

if payment.create():
  print("Payment[%s] created successfully" % (payment.id))
  for link in payment.links:
        if link.method == "REDIRECT":
            redirect_url = str(link.href)
            print("Redirect for approval: %s" % (redirect_url))
else:
  print(payment.error)
