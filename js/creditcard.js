/*
USE PAYME API TO CREATE PAYMENT LINKS TO FOODIE AND POST TO PYTHON BACK END!
*/
$(document).ready(function(){

  <form>
  <input id="name" placeholder="Name" />
  <input id="creditcard" placeholder="credit card" />
  <input id="expmonth" placeholder="expiration month" />
  <input id="expyear" placeholder="expiration year" />
  <input id="cvv" placeholder="cvv" />
  <input id="zipcode" placeholder="zipcode" />
  <button>Post Credit Card info</button>
  </form>

$("#postcard").click(function(){
  var name = document.getElementById('name').value;
  var creditcard = document.getElementById('creditcard').value;
  var expmonth = document.getElementById('expmonth').value;
  var expyear = document.getElementById('expyear').value;
  var cvv = document.getElementById('cvv').value;
  var zipcode = document.getElementById('zipcode').value;

  $.ajax({
    type: "POST",
    url: '/postcard',
      data: {'name':name, 'credit':creditcard, 'expmonth':expmonth, 'expyear':expyear, 'cvv':cvv, 'zipcode':zipcode}
  });


});

});
