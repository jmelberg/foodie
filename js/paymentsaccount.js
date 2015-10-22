
$(document).ready(function(){


  WePay.set_endpoint("stage"); // stage or production

  WePay.OAuth2.button_init(document.getElementById('start_oauth2'), {
      "client_id":"175855",
       "scope":["manage_accounts","collect_payments","view_user","send_money","preapprove_payments"],
      "user_name":"",
      "user_email":"",
      "redirect_uri":"http://food-enthusiast.appspot.com/",
      "top":100, // control the positioning of the popup with the top and left params
      "left":100,
      "state":"robot", // this is an optional parameter that lets you persist some state value through the flow
      "callback":function(data) {
      /** This callback gets fired after the user clicks "grant access" in the popup and the popup closes. The data object will include the code which you can pass to your server to make the /oauth2/token call **/
      if (data.code.length !== 0) {
        $.ajax({
          type: "POST",
          url: '/getwepaytoken/',
            data: data
        });
      } else {
        // an error has occurred and will be in data.error
      }
    }
  });

});
