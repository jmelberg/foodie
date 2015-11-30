/*
USE PAYME API TO CREATE PAYMENT LINKS TO FOODIE AND POST TO PYTHON BACK END!
*/
$(document).ready(function(){

  $('#addpayment').openModal();

  WePay.set_endpoint("production"); // change to "production" when live

  // Shortcuts
  var d = document;
      d.id = d.getElementById,
      valueById = function(id) {
          return d.id(id).value;
      };

  // For those not using DOM libraries
  var addEvent = function(e,v,f) {
      if (!!window.attachEvent) { e.attachEvent('on' + v, f); }
      else { e.addEventListener(v, f, false); }
  };

  // Attach the event to the DOM
  addEvent(d.id('cc-submit'), 'click', function() {
      var userName = [valueById('name')].join(' ');
          response = WePay.credit_card.create({
          "client_id":        3044,
          "user_name":        valueById('name'),
          "email":            valueById('email'),
          "cc_number":        valueById('cc-number'),
          "cvv":              valueById('cc-cvv'),
          "expiration_month": valueById('cc-month'),
          "expiration_year":  valueById('cc-year'),
          "address": {
              "zip": valueById('zip')
          }
      }, function(data) {
          if (data.error) {
              console.log(data);
              // handle error response
          } else {
              // call your own app's API to save the token inside the data;
              // show a success page
              $.ajax({
                type: "POST",
                url: '/authorizepayment',
                data: {'credit_card_id': JSON.stringify(data.credit_card_id)},
                success: function(){
                  setTimeout(function(){
                    window.location.href = '/feed';
                  }, 200);
                }
              });
          }
      });
  });

});
