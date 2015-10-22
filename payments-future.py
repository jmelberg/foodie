import payments
'''
1. Create Payments
2. Charge Payment Full Amount
3. Charge Payment Partial Amount
'''
class FuturePayments:
    def create(account, ):

    def charge():

    def chargePartial():





#Python Class for Processing Preapproved Payments
class createFuturePayment:
    def create(account_id, price, description):
        createpayment = wepay.call('/preapproval/create', {
        'account_id': account_id,
        'period': 'once',
        'amount': price,
        'mode': 'regular',
        'short_description': description,
        'redirect_uri': redirect_uri
})

class chargePayment:


    def chargePartial

    def chargeFull

class chargePaymentFull:
    def charge(self):
        chargepayment =

class chargePaymentPartial:
    def charge(self):
        chargePartial = wepay.call('/checkout/create', {
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


class ApprovedPaymentHandler():
  def post(self):
      print:"Payment has been approved!"

# display the response
print json.dumps(response)

'''
1. Retrieve Preapproval ID, store it in database somewhere along with amount.
2. When Payment is to be charged, Retrieve Preapproval ID and charge Future Payment
'''

#Get Preapproved Payment ID



#Charge the Future Payment
