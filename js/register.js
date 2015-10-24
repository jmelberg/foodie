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
    var valid_username = 'false';
    var valid_password = 'false';
    var valid_email = 'false';
    var valid_first_name = 'false';
    var valid_last_name ='false';
    $('#username').focus();
    $('#username').keyup(function () {
      checkUsername($(this).val().toLowerCase());
      if($(this).val().length != 0){
        setTimeout(function() {
          if($('#available').text().length == 21) {
            valid_username = 'true';
          }
          else {
            valid_username = 'false';
          }
        }, 300);
      }
      else{
        valid_username = 'false';
        $("#available").show();
      }
    });
    $('#password').keyup(function () {
      valid_password = matchingPasswords($(this).val(), $('#confirm_password').val());
    });
    $('#confirm_password').keyup(function () {
      valid_password = matchingPasswords($('#password').val(), $(this).val());
    });
    $('#email').keyup(function() {
      if($('#email').val()){
        if(validateEmail($('#email').val())){
          valid_email = 'true';
          $('#email_available').hide();
        }
        else{
          valid_email = 'false';
          $('#email_available').text('Email not available');
          $('#email_available').show();
        }
      }
    });
    $('#first_name').keyup(function() {
      if($('#first_name').val().length != 0) {
        valid_first_name = 'true';
      }
      else {
        valid_first_name = 'false';
      }
    });
    $('#last_name').keyup(function() {
      if($('#last_name').val().length != 0) {
        valid_last_name = 'true';
      }
      else {
        valid_last_name = 'false';
      }
    });
    $(window).keyup(function() {
      setTimeout(function() {
        showSignUp(valid_username,valid_password,valid_email,valid_first_name,valid_last_name);
      }, 200);
    });
  });

  function checkUsername(username) {
    $.ajax({
      url: "/checkusername",
      cache: false,
      data:{'username' : username},
      success: function(result){
        $("#available").text(result);
        $("#available").show();
    }});
  }

  function matchingPasswords(password, confirm_password) {
    if(password.length > 5 && confirm_password.length > 5) {
      if(password != confirm_password){
        $('#passwords_match').show();
        $('#passwords_match').text('The passwords do not match');
        return 'false';
      }
      else{
        $('#passwords_match').hide();
        return 'true';
      } 
    }
    else {
      $('#passwords_match').show();
      $('#passwords_match').text('The password needs to be 6 characters or higher');
    }
  }

  function validateEmail(email) {
    var re = /^([\w-]+(?:\.[\w-]+)*)@((?:[\w-]+\.)*\w[\w-]{0,66})\.([a-z]{2,6}(?:\.[a-z]{2})?)$/i;
    return re.test(email);
  }

  function showSignUp(username, email, password, first_name, last_name) {
    if(username === 'true'
      && email === 'true'
      && password === 'true'
      && first_name === 'true'
      && last_name === 'true') {
      $("#signup_button").show();
    }
    else {
      $("#signup_button").hide();
    }
  }
});