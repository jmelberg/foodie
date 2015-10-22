import payments
from wepay import *

#Python Class for Full Refund
class fullRefund:
	def post(self, checkoutID, reason):
		processRefund = fullRefund = wepay.call('/checkout/refund', {
			'checkout_id': checkoutID,
			'refund_reason': reason
		})

#Full Refund

fullRefund = wepay.call('/checkout/refund', {
	'checkout_id': checkout_id,
	'refund_reason': 'Dinner Dash!'
})
print json.dumps(fullRefund)

#Python Class for Partial Refund
class partialRefund:
	def post(self, checkoutID, reason , partialRefundAmount)
		self.processRefund = wepay.call('/checkout/refund', {
			'checkout_id': checkout_id,
			'refund_reason': reason,
			'amount': partialRefundAmount
		})

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
