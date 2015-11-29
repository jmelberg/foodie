$(document).ready(function(){
  $.getScript("../js/create_request.js");
    var current_request = $('#confirm_request').val();
    var location;

    // Confirm requests modal
  $("[id^='confirm_modal']").click(function() {
    $('#respond').openModal();
    location = $(this).val();
    var attributes = location.split(',');
    $('.modal-content #location').val(attributes[0]);
    $('.modal-content #address').val(attributes[1]);
    $('.modal-content #city').val(attributes[2]);
  });

  // Accept confirm request
  $("#accept_button").click(function() {
    $.ajax({
      type: "POST",
      url: "/confirm/"+confirm_request.value,
      data: {'location': location},
    });
    setTimeout(function(){ // Refresh after 1 second
      window.location.href = '/requests';
    }, 200);
  });

  // Close confirm request modal
  $('#close_modal').click(function(){
    $('#respond').closeModal();
    window.location.href = '/requests';
  });
});