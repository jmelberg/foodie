$(document).ready(function(){
  // Variables
  var slider = document.getElementById('range-input');
  var min_price = document.getElementById('min_price');
  var max_price = document.getElementById('max_price');

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

    $('#cancel_request').click(function(){
      $('#requests').closeModal();
    });

    $('#send_request').click(function() {
      var date = $('#date').val();
      var time = $('#time').val();
      var location = $('#location').val();
      var m_price = $('#min_price').val();
      var mx_price = $('#max_price').val();
      $.ajax({
        type: "POST",
        url: '/request',
        data: {'date':date, 'time':time, 'location':location,
        'max_price': mx_price, 'min_price':m_price}
      });
      setTimeout(function(){ // Refresh after 1 second
      window.location.href = '/requests';
    }, 100);
    });
  });
});
function checkTime(time, date) {
  $.ajax({
    url: "/checktime",
    cache: false,
    data:{'date':date, 'time':time},
    success: function(result){
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
