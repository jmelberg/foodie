import requests
import json
from models import PaymentLinks, PaymentModel

class CreatePaymentExample:
    def __init__(self):
        test = requests.get('http://107.170.240.130:3000/createpayment')
        print test

class CreatePayment:
    def __init__(self, foodie, expert, welink, price, accountID, short_desc):
        create = requests.post('http://107.170.240.130:3000/createpayment', data={"welink": welink, "price":price, "accountID":accountID, "short_desc":short_desc})
        link = create.json()
        print link["preapproval_uri"]
        payment = PaymentModel()
        payment.confirm = False
        payment.link = link["preapproval_uri"]
        payment.foodie = self.user_model
        payment.expert = self.user_model
        payment.amount = price
        payment.put()

class ChargePayment:
    def __init__(self, future_id, price, accountID, desc):
        charge = requests.post('http://107.170.240.130:3000/chargepayment', data={"future_id":future_id, "price":price, "account_id":accountID, "desc":desc})
        print charge.json()
