$(document).ready(function(){
  $('#register_tab').click(function() {
    window.location.href = '/register';
  });
  $('#login_tab').click(function() {
    window.location.href = '/';
  });
  $('#settings_tab').click(function() {
    window.location.href = '#';
  });

  $(function () {
    $('#username').focus();
    $('#username').keyup(function () {
      if($(this).val().length != 0){
        checkUsername($(this).val().toLowerCase());
      }
      else{
        $("#available").hide();
      }
    });
    $('#confirm_password').keyup(function () {
      if($(this).val() != $('#password').val()){
        $('#passwords_match').show();
        $('#signup_button').hide();
      }
      else{
        $('#passwords_match').hide();
        $('#signup_button').show();
      }
    });
    $('#email').keyup(function() {
      var email = $('#email').val();
      if(email){
        if(validateEmail(email)){
          $('#signup_button').show();
          $('#email_available').hide();
        }
        else{
          $('#signup_button').hide();
          $('#email_available').text('Email not available');
          $('#email_available').show();
        }
      }
      else{
        $('#signup_button').hide();
      }
    });
  });


  function checkUsername(username) {
    $.ajax({
      url: "/checkusername",
      cache: false,
      data:{'username' : username},
      success: function(result){
        $("#available").text(result);
        if(result == 'Username is available'){
          $("#available").show();
          $("#signup_button").show();
        }
        else {
          $("#available").show();
          $("#signup_button").hide();
        }
    }});
  }

  function validateEmail(email) {
    var re = /^([\w-]+(?:\.[\w-]+)*)@((?:[\w-]+\.)*\w[\w-]{0,66})\.([a-z]{2,6}(?:\.[a-z]{2})?)$/i;
    return re.test(email);
  }
});

