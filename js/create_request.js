$(document).ready(function(){
  $(function () {
    $('#time').focus();
    $('#time').keyup(function () {
      if($(this).val().length != 0) {
        var date = $('#date').val();
        var time = $(this).val();
        checkTime(time, date);
      }
      else{
        $('#available').hide();
      }
    });

    $('#cancel_request').click(function(){
      $('#requests').closeModal();
    });

    $('#send_request').click(function() {
      var date = $('#date').val();
      var time = $('#time').val();
      var location = $('#location').val();
      $.ajax({
        type: "POST",
        url: '/request',
        data: {'date':date, 'time':time, 'location':location,}
      });
      setTimeout(function(){ // Refresh after 1 second
      window.location.href = '/requests';
    }, 100);
    });

    function checkTime(time, date) {
      $.ajax({
        url: "/checktime",
        cache: false,
        data:{'date':date, 'time':time},
        success: function(result){
          $("#available").text(result);
          if(result == 'Available'){
            $("#available").show();
            $("#send_request").show();
          }
          else {
            $("#available").show();
            $("#send_request").hide();
          }
        }});
    }
  });
});
