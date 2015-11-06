// Call functions from other js
$.getScript("../js/create_request.js");

$(document).ready(function() {
  var tab = getUrlParameter('q');
  var bidder;
  var request = $('#request').val();
  var cancel_request;
  $('ul.tabs').tabs();

  // pending Confirm application modal
  $("[id^='pending_confirm_modal']").click(function() {
    $('#respond').openModal();
    bidder = $(this).val();
    console.log(request);
  });
 
  // Hide requests
  $("[id^='hide']").click(function(){
      $(this).parents().eq(1).hide();
  });

  // Hide pending requests
  $("[id^='pending_hide']").click(function(){
      $(this).parents().eq(1).hide();
  });

  // Cancel pending request
  $("[id^='pending_cancel']").click(function(){
      $('#cancel_request').openModal();
      cancel_request = $(this).val();
  });

  // Confirm cancel pending request
  $("[id^='confirm_cancel_request']").click(function(){
      $.ajax({
        type: "POST",
        url: "/cancel",
        data: {'request' : cancel_request},
      });
    setTimeout(function(){ // Refresh after 1 second
      window.location.href = '/requests';
    }, 200); 
  });

  // Accept confirm application
  $("#select_bid_button").click(function() {
    $.ajax({
      type: "POST",
      url: "/choose/"+request,
      data: {'bidder': bidder},
    });
    setTimeout(function(){ // Refresh after 1 second
      window.location.href = '/requests';
    }, 200);
  });
  // Close pending confirm application modal
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
    setTimeout(function(){ // Refresh after 1 second
      window.location.href = '/requests';
    }, 200);
  });

  // For sorted results
  if(tab == 'mine'){
    $('ul.tabs').tabs('select_tab', 'mine');
  }
  else if(tab=='all'){
    $('ul.tabs').tabs('select_tab', 'all');
  }
  else if(tab == 'location'){
    $('#location_requests').show();
    $('#all').hide();
  }
  else if(tab == 'price'){
    $('#price_requests').show();
    $('#all').hide();  
  }
  else if(tab == 'hangouts'){
    $('#hangouts_requests').show();
    $('#all').hide();
    $('#hangouts_sort').hide();
  }
  else if(tab == 'lessons'){
    $('#lessons_requests').show();
    $('#all').hide();
    $('#lessons_sort').hide();
  }
  else {
    $('ul.tabs').tabs('select_tab', 'all');
  }

  if($('#pending').click(function(){ 
      $('#price_requests').hide();
      $('#location_requests').hide();
    }));
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

function changeElements(){
  $('#location_requests').hide();
  $('#price_requests').hide();
}