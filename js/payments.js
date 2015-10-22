/*
USE PAYME API TO CREATE PAYMENT LINKS TO FOODIE AND POST TO PYTHON BACK END!
*/
$(document).ready(function(){

$("#createpayment").click(function(){
  var foodie = document.getElementById('foodiepay').value;
  var expert = document.getElementById('expertpay').value;
  var amount = document.getElementById('priceamount').value;

  $.ajax({
    type: "POST",
    url: '/createpayment',
      data: {'foodie':foodie, 'expert':expert, 'amount':amount}
  });


});

WePay.iframe_checkout("payhere", "https://stage.wepay.com/api/checkout/12345");

});
