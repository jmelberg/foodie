import requests
import json

class CreatePaymentExample:
    def __init__(self):
        test = requests.get('http://107.170.240.130:3000/createpayment')
        print test.json()

class CreatePayment:
    def __init__(self, price, accountID, short_desc):
        create = requests.post('http://107.170.240.130:3000/createpayment', data={"price":price, "accountID":accountID, "short_desc":short_desc})
        print create.json()

class ChargePayment:
    def __init__(self, future_id, price, accountID, desc):
        charge = requests.post('http://107.170.240.130:3000/chargepayment', data={"future_id":future_id, "price":price, "account_id":accountID, "desc":desc})
        print charge.json()
