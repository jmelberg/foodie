var filled_location = false;

$(document).ready(function(){
  // Variables
  var slider = document.getElementById('range-input');
  var min_price = document.getElementById('min_price');
  var max_price = document.getElementById('max_price');
  var submit_button = $('#send_request');
  var filled_food_type = false;
  var filled_time = false;
  var confirmed_aggreement = false;
  var status = false;

  $(function () {
    // Check for empty fields
    // Location
    $('#location').keyup(function() {
      var location = $(this).val();
      if(location.length > 0){
        filled_location = true;
      status = finalAgreement(filled_time, filled_food_type, filled_location, confirmed_aggreement);
        /*submit_button.style.visibility = "visible";*/
      }
      else{
        filled_location = false;
        if(submit_button.attr('class') === 'btn-flat disabled' && location.length != 0) {
          submit_button.removeClass('disabled');
        }
        else {
          submit_button.addClass('disabled');
        }
        /*submit_button.style.visibility = "hidden";*/
      }
    });

    $('#food_type').keyup(function() {
      var food_type = $(this).val();
      if(food_type.length > 0){
        filled_food_type = true;
      status = finalAgreement(filled_time, filled_food_type, filled_location, confirmed_aggreement);
        /*submit_button.style.visibility = "visible";*/
      }
      else{
        filled_food_type = false;
        if(submit_button.attr('class') === 'btn-flat disabled' && food_type.length != 0) {
          submit_button.removeClass('disabled');
        }
        else {
          submit_button.addClass('disabled');
        }
        /*submit_button.style.visibility = "hidden";*/
      }
    });

    $('#time').keyup(function () {
      var date = $('#date');
      var time = $('#time');
      if($(this).val().length != 0) {
        checkTime(time.val(), date.val(), confirmed_aggreement);
        setTimeout(function() {
          if($("#slot_available").text() == 'Available') {
            filled_time = true;
          }
          else {
            filled_time = false;
          }
        }, 350);
      }
      else{
      }
    });

    $('#agreement').click(function(){
      confirmed_aggreement = !confirmed_aggreement;
      console.log(filled_time);
      status = finalAgreement(filled_time, filled_food_type, filled_location, confirmed_aggreement);
    });

    noUiSlider.create(slider, {
      start: [20, 80],
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
        max_price.value = value;
      } else {
        min_price.value = value;
      }
    });

    $('#send_request').click(function() {
      if ($('#agreement:checked').length>0 && status === true){
        var date = $('#date').val();
        var time = $('#time').val();
        var location = $('#location').val();
        var m_price = $('#min_price').val();
        var mx_price = $('#max_price').val();
        var food_type = $('#food_type').val();
        var interest = $('input[type="radio"]:checked').val();
      
        $.ajax({
          type: "POST",
          url: '/request',
          data: {'date':date, 'time':time, 'location':location,
          'max_price': mx_price, 'min_price':m_price, 'food_type': food_type, 'interest': interest}
        });
        setTimeout(function(){ // Refresh after 1 second
        window.location.href = '/requests';
        }, 100);
      }
    });
  });
});

function checkLocation(location) {
  if(location.length > 0) {
    filled_location = true;
  }
}

function finalAgreement(time, food_type, location, confirmed_aggreement) {
  if(time === true && location === true && food_type === true && confirmed_aggreement === true) {
    $('#send_request').removeClass('disabled');
    return true;
  }
  else {
    $('#send_request').addClass('disabled');
    return false;
  }
}

function checkTime(time, date, confirmed_aggreement) {
  var selected_edit_request;
  if (document.getElementById('edit_request') != null){
    selected_edit_request = document.getElementById('edit_request').value;
  }
  $.ajax({
    url: "/checktime",
    cache: false,
    data:{'date':date, 'time':time, 'edit_request': selected_edit_request},
    success: function(result){
      $('#edit_slot_available').text(result);
      if(result == 'Available'){
        $("#edit_slot_available").show();
        /*$("#submit_edit").show();*/
        $('#submit_edit').removeClass('disabled');
      }
      else {
        $("#edit_slot_available").show();
        if($("#submit_edit").attr('class') === 'btn-flat') {
          $("#submit_edit").addClass('disabled');
        }
      }
      $("#slot_available").text(result);
      if(result == 'Available'){
        $("#slot_available").show();
        /*$("#send_request").show();*/
        if(confirmed_aggreement === true) {
          $("#send_request").removeClass('disabled');          
        }
      }
      else {
        $("#slot_available").show();
        if($("#send_request").attr('class') === 'btn-flat') {
          $("#send_request").addClass('disabled');
        }
      }
/*
      $("#slot_available").text(result);
      if(result == 'Available'){
        $("#slot_available").show();
        $("#send_request").show();
      }
      else {
        $("#slot_available").show();
        $("#send_request").hide();
      } */
    }
  });
}