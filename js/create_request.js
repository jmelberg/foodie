$(document).ready(function(){
  // Variables
  var slider = document.getElementById('range-input');
  var min_price = document.getElementById('min_price');
  var max_price = document.getElementById('max_price');
  var submit_button = document.getElementById('send_request');


  $(function () {
    $('#time').focus();
    $('#time').keyup(function () {
      if($(this).val().length != 0) {
        var date = $('#date').val();
        var time = $(this).val();
        checkTime(time, date);
      }
      else{
        $('#slot_available').hide();
      }
    });

    // Check for empty fields
    // Location
    $('#location').keyup(function() {
      var location = $(this).val();
      if(location.length > 0){
      submit_button.style.visibility = "visible";
      }
      else{
        submit_button.style.visibility = "hidden";
      }
    });
    // // Food Type
    // $('select').change(function(){
    //   var selected_type = $("#food_type option:selected").text();
    //   if(selected_type != "Choose your option"){
    //     submit_button.style.visibility = "visible";
    //   }
    //   else{
    //     submit_button.style.visibility = "hidden";
    //   }
    // });

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

    $('#agreement').click(function(){
      $('#send_request').removeClass('disabled');
    });

    $('#cancel_request').click(function(){
      $('#requests').closeModal();
    });

    $('#send_request').click(function() {
      if ($('#agreement:checked').length>0){
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

function checkTime(time, date) {
  var selected_edit_request;
  if (document.getElementById('edit_modal') != null){
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
        $("#submit_edit").show();
      }
      else {
        $("#edit_slot_available").show();
        $("#submit_edit").hide();
      }
      $("#slot_available").text(result);
      if(result == 'Available'){
        $("#slot_available").show();
        $("#send_request").show();
      }
      else {
        $("#slot_available").show();
        $("#send_request").hide();
      }

      $("#slot_available").text(result);
      if(result == 'Available'){
        $("#slot_available").show();
        $("#send_request").show();
      }
      else {
        $("#slot_available").show();
        $("#send_request").hide();
      } 
    }
  });
}
