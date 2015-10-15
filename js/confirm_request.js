$(document).ready(function(){
    var current_request = $('#confirm_request').val();
    var location;
    // Confirm requests modal
  $("[id^='confirm_modal']").click(function() {
    $('#respond').openModal();
    location = $(this).val();   
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
    }, 100);
  });

  // Close confirm request modal
  $('#close_modal').click(function(){
    $('#respond').closeModal();
    window.location.href = '/requests';
  });
});