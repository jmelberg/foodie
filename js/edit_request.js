$(document).ready(function(){
  // Call functions from other js
  $.getScript("../js/create_request.js");

  
  var interest_box = document.getElementById('get_my_interest').value
  if (interest_box == "fun"){
    document.getElementById('edit_interest_fun').checked = true;
  }
  else{
    document.getElementById('edit_interest_food_lesson').checked = true;
  }

  // Edit Functions //
  $('#edit_food_type').keyup(function() {
    if($('#edit_food_type').val().length === 0) {
      $('#submit_edit').addClass('disabled');
    }
    else {
      $('#submit_edit').removeClass('disabled');
    }
  })

  $('#edit_location').keyup(function() {
    if($('#edit_location').val().length === 0) {
      $('#submit_edit').addClass('disabled');
    }
    else {
      $('#submit_edit').removeClass('disabled');
    }
  })
  
  $('#edit_time').focus();
  $('#edit_time').keyup(function () {
    if($(this).val().length != 0) {
      var date = $('#edit_date').val();
      var time = $(this).val();
      checkTime(time, date, false);
    }
    else{
      $('#edit_slot_available').hide();
    }
  });

  $('#submit_edit').click(function() {
    if($('#edit_food_type').val().length > 0 && $('#edit_location').val().length > 0 && $('#edit_slot_available').text() === 'Available') {
      var date = $('#edit_date').val();
      var time = $('#edit_time').val();
      var location = $('#edit_location').val();
      var e_price = $('#edit_price').val();
      var food_type = $('#edit_food_type').val();
      var interest = $('input[type="radio"]:checked').val();
      var request = $('#edit_request').val();
      $.ajax({
        type: "POST",
        url: '/editrequest/'+ request,
          data: {'date':date, 'time':time, 'location':location,
            'price': e_price,'food_type': food_type, 'interest': interest}
      });
      setTimeout(function(){ // Refresh after 1 second
        window.location.href = '/feed';
      }, 200);
    }
  });
});