$(document).ready(function(){
  // Call functions from other js
  $.getScript("../js/create_request.js");

  // Edit Functions //
  var valid_time = false;
  $('#edit_time').focus();
  $('#edit_time').keyup(function () {
    if($(this).val().length != 0) {
      var date = $('#edit_date').val();
      var time = $(this).val();
      checkTime(time, date, false);
      if($('#edit_slot_available').val() === 'Available') {
        valid_time = true;
      }
      else
      {
        valid_time = false;
      }
    }
    else{
      $('#edit_slot_available').hide();
    }
  });

  var slider = document.getElementById('edit_slider');
  var min_price = $('#edit_min_price').val();
  var max_price = $('#edit_max_price').val();
  var interest = $('#edit_interest').val();

  // Create slider
  var slider = document.getElementById('edit_slider');
  noUiSlider.create(slider, {
    start: [min_price, max_price],
    connect: true,
    step: 1,
    range: {
      'min': 0,
      'max': 100
    },
    format: wNumb({
      decimals: 0
    })
  });

  slider.noUiSlider.on('update', function( values, handle ) {
    var value = values[handle];
    if ( handle ) {
      $('#edit_max_price').val(value);
    } else {
      $('edit_min_price').val(value);
    }
  });

  $('#submit_edit').click(function() {
    if(valid_time === true) {
      var date = $('#edit_date').val();
      var time = $('#edit_time').val();
      var location = $('#edit_location').val();
      var m_price = $('#edit_min_price').val();
      var mx_price = $('#edit_max_price').val();
      var food_type = $('#edit_food_type').val();
      var interest = $('input[type="radio"]:checked').val();
      var request = $('#edit_request').val();
      $.ajax({
        type: "POST",
        url: '/editrequest/'+ request,
          data: {'date':date, 'time':time, 'location':location,
            'max_price': mx_price, 'min_price':m_price, 'food_type': food_type, 'interest': interest}
      });
      setTimeout(function(){ // Refresh after 1 second
        window.location.href = '/requests';
      }, 100);      
    }
  });
});