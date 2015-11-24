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
        payment.foodie = foodie
        payment.expert = expert
        payment.amount = price
        payment.put()

class ChargePayment:
    def __init__(self, future_id, price, accountID, desc):
        charge = requests.post('http://107.170.240.130:3000/chargepayment', data={"future_id":future_id, "price":price, "account_id":accountID, "desc":desc})
        print charge.json()

def AddCreditCard(name, email, creditcard, expmonth, expyear, address, city, state, cvv, zipcode):
    add = requests.post('http://107.170.240.130:3000/addcreditcard', data={"user_name": name, "email":email, "cc_number":creditcard, "cvv":cvv, "expiration_month":expmonth, "expiration_year":expyear, "address1":address, "city":city, "state":state, "country":"US", "zip":zipcode})
    return add

def AuthorizeCreditCard(credit_card_id):
    authorize = requests.post('http://107.170.240.130:3000/authorizecredit', data={"credit_id":credit_card_id})
    return authorize

def Charge(account_id, credit_card_id, amount, desc):
    charge = requests.post('http://107.170.240.130:3000/charge', data={"credit_card_id": credit_card_id, "account_id": account_id, "amount": amount, "desc": desc})
