__author__ = 'chrisnavy'
from payments import *

#Store Payment Amount and
price = input('Enter how much the charge should be: ')


# create the future payment
response = wepay.call('/preapproval/create', {
    'account_id': account_id,
    'period': 'once',
    'amount': price,
    'mode': 'regular',
    'short_description': 'Your Payment for a Foodie Adventure!',
    'redirect_uri': 'http://example.com/success/'
})

# display the response
print json.dumps(response)

'''
1. Retrieve Preapproval ID, store it in database somewhere along with amount.
2. When Payment is to be charged, Retrieve Preapproval ID and charge Future Payment
'''

#Get Preapproved Payment ID



#Charge the Future Payment

response = wepay.call('/checkout/create', {
    'account_id': account_id,
    'amount': adjustedPrice,
    'currency': 'USD',
    'short_description': 'Payment for test project',
    'type': 'goods',
    'payment_method': {
            'type': 'preapproval',
            'preapproval': {
                'id': preapproval_id
            }
    }
})