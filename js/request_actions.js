// Call functions from other js
$.getScript("../js/create_request.js");

var tab = getUrlParameter('q')
var current_request;
$(document).ready(function() {
  var user = document.getElementById('user').getAttribute('value');

  // Hide requests
  $("[id^='hide']").click(function(){
    $(this).parents().eq(1).hide();
  });

  // Confirm requests modal
  $("[id^='confirm_modal']").click(function() {
    var request = $(this).val();
    current_request = request;
    $('#respond').openModal();
  });

  // Accept confirm request
  $("#accept_button").click(function() {
    $.ajax({
      type: "POST",
      url: "/confirm",
      data: {'request' : current_request, 'approver': user},
    });
    setTimeout(function(){ // Refresh after 1 second
      window.location.href = '/requests';
    }, 100);
  });

  // Close confirm request modal
  $('#close_modal').click(function(){
    $('#respond').closeModal();
  });

  //Delete Selected
  $("[id^='delete']").click(function(){
    // Delete function
    var request = $(this).val();
    $.ajax({
      type: "POST",
      url: "/delete",
      data: {'request' : request},
    });
    top.location.href = '/requests';
  });


  // Edit Functions //
  $('#edit_time').focus();
  $('#edit_time').keyup(function () {
    if($(this).val().length != 0) {
      var date = $('#edit_date').val();
      var time = $(this).val();
      checkTime(time, date);
    }
    else{
      $('#slot_available').hide();
    }
  });

  //Edit Selected
  $("[id^='edit_request']").click(function(){
    // Edit function
    var request = $(this).val();
    var active_request = request;
    returnRequest(request);    
    document.getElementById('edit_modal').value=request;
    $('#edit_modal').openModal();
  });

  // Close edit modal
  $('#close_edit').click(function(){
    $('#edit_modal').closeModal();
  });

  // Submit Edit
  $('#submit_edit').click(function() {
      var date = $('#date').val();
      var time = $('#time').val();
      var location = $('#location').val();
      var m_price = $('#min_price').val();
      var mx_price = $('#max_price').val();
      var food_type = $('#food_type').val();
      var interest = $('input[type="radio"]:checked').val();
      $.ajax({
        type: "POST",
        url: '/editrequest',
        data: {'edit_date':date, 'edit_time':time, 'edit_location':location,
        'edit_max_price': mx_price, 'edit_min_price':m_price, 'edit_food_type': food_type, 'edit_interest': interest}
      });
      setTimeout(function(){ // Refresh after 1 second
      window.location.href = '/requests';
    }, 100);
    });


  // Set active tab
  if(tab == 'mine'){
    $('ul.tabs').tabs('select_tab', 'mine');
  }
  else {
    $('ul.tabs').tabs('select_tab', 'all');
  }                
});

// Returns string from appended url
function getUrlParameter(sParam)
{
    var sPageURL = window.location.search.substring(1);
    var sURLVariables = sPageURL.split('&');
    for (var i = 0; i < sURLVariables.length; i++) 
    {
        var sParameterName = sURLVariables[i].split('=');
        if (sParameterName[0] == sParam) 
        {
            return sParameterName[1];
        }
    }
}

// Returns request attributes given key
function returnRequest(key){
  $.ajax({
    url: "/returnrequest",
    cache: false,
    data:{'key':key},
    success: function(response){
      var json = jQuery.parseJSON(response);
      $('#edit_location').attr("placeholder", json.location);
      $('#edit_date').attr("placeholder", json.date);
      $('#prev_time').attr("placeholder", json.time_slot);
      $('#edit_min_price').value = json.min_price;
      $('#edit_max_price').value = json.max_price;

      // Create slider
      var slider = document.getElementById('edit_slider');
      noUiSlider.create(slider, {
        start: [json.min_price, json.max_price],
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
    }
  });
};
