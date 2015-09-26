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
});