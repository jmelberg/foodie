var filled_location = false;
var filled_time = false;
$(document).ready(function(){
  // Variables
  var submit_button = $('#send_request');
  var confirmed_price = false;
  var filled_food_type = false;
  var confirmed_aggreement = false;
  var status = false;

  $(function () {

    // Check for empty fields
    // Location
    $('#location').on("keypress change",function(e) {
      var location = $(this).val();
      if(location.length > 0){
        filled_location = true;
        status = finalAgreement(filled_time, filled_food_type, filled_location, confirmed_price, confirmed_aggreement);
      }
      else{
        filled_location = false;
        if(submit_button.attr('class') === 'btn-flat disabled' && location.length != 0) {
          submit_button.removeClass('disabled');
        }
        else {
          submit_button.addClass('disabled');
        }
      }
    });

    $('#food_type').on("keypress change",function(){
      var food_type = $(this).val();
      if(food_type.length > 0){
        filled_food_type = true;
        status = finalAgreement(filled_time, filled_food_type, filled_location, confirmed_price, confirmed_aggreement);
      }
      else{
        filled_food_type = false;
        if(submit_button.attr('class') === 'btn-flat disabled' && food_type.length != 0) {
          submit_button.removeClass('disabled');
        }
        else {
          submit_button.addClass('disabled');
        }
      }
    })

    $('#time').on("change keypress",function () {
      var date = $('#date');
      var time = $('#time');
      if($(this).val().length != 0) {
        checkTime(time.val(), date.val(), confirmed_aggreement);
      }
      else{
      }
    });

    $('#price').on("change keypress", function() {
      var price = $(this).val();
      if(price > 0 && price.length > 0){
        confirmed_price = true;
        status = finalAgreement(filled_time, filled_food_type, filled_location, confirmed_price, confirmed_aggreement);
      }
      else{
        confirmed_price = false;
        if(submit_button.attr('class') === 'btn-flat disabled' && price <= 0 && price.length != 0) {
          submit_button.removeClass('disabled');
        }
        else {
          submit_button.addClass('disabled');
        }
      }
      if(price.substring(0, 1) == "-") {
        confirmed_price = false;
        status = finalAgreement(filled_time, filled_food_type, filled_location, confirmed_price, confirmed_aggreement);
      }      
    });

    $('#agreement').click(function(){
      confirmed_aggreement = !confirmed_aggreement;
      
      status = finalAgreement(filled_time, filled_food_type, filled_location, confirmed_price, confirmed_aggreement);
    });

    $('#send_request').click(function() {
      if ($('#agreement:checked').length>0 && status === true){
        console.log("sending request");
        var date = $('#date').val();
        var time = $('#time').val();
        var location = $('#location').val();
        var food_type = $('#food_type').val();
        var price = $('#price').val();
        var interest = $('input[type="radio"]:checked').val();
        var owner = $('#username').attr('value');
        
        $.ajax({
          type: "POST",
          url: '/request',
          data: {'date':date, 'time':time, 'location':location, 'price': price,
          'food_type': food_type, 'interest': interest},
          success: function(){
            setTimeout(function(){ // Refresh after 1 second
            window.location.href = '/foodie/'+owner+'?q=table/all';
            }, 100);
          }
        });
      }
    });
  });
});

function checkLocation(location) {
  if(location.length > 0) {
    filled_location = true;
  }
}

function finalAgreement(time, food_type, location, confirmed_price, confirmed_aggreement) {
  if(time === true && location === true && food_type === true && confirmed_price === true && confirmed_aggreement === true) {
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
        filled_time = true;
      }
      else {
        $("#slot_available").show();
        if($("#send_request").attr('class') === 'btn-flat') {
          $("#send_request").addClass('disabled');
        }
        filled_time = false;
      }
    }
  });
}