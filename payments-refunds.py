__author__ = 'chrisnavy'
from payments import *

#Full Refund

fullRefund = wepay.call('/checkout/refund', {
	'checkout_id': checkout_id,
	'refund_reason': 'Dinner Dash!'
})
print json.dumps(fullRefund)



#Partial Refund
partialRefund = wepay.call('/checkout/refund', {
	'checkout_id': checkout_id,
	'refund_reason': 'Product was defective.',
	'amount': partialRefundAmount
})
print json.dumps(partialRefund)

#Calculate Partial Refund

'''
1. Get Transaction amount from somewhere lol.
2. Use it with w.e. Penalty rate and calculate.
'''

