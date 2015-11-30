$(document).ready(function() {
  var tab = getUrlParameter('q');

  if(tab == 'table/waiting') {
    $('#table-waiting').show();
    $('#timelineViewBtn').show();
    $('#tableViewBtn').hide();
    $('#tableDDBtn').show();
    $('#timelineDDBtn').hide();
  } 
  else if(tab == 'table/pending') {
    $('#table-pending').show();
    $('#timelineViewBtn').show();
    $('#tableViewBtn').hide();
    $('#tableDDBtn').show();
    $('#timelineDDBtn').hide();
  }
  else if(tab == 'table/accepted') {
    $('#table-accepted').show();
    $('#timelineViewBtn').show();
    $('#tableViewBtn').hide();
    $('#tableDDBtn').show();
    $('#timelineDDBtn').hide();
  }
  else if(tab == 'table/completed') {
    $('#table-completed').show();
    $('#timelineViewBtn').show();
    $('#tableViewBtn').hide();
    $('#tableDDBtn').show();
    $('#timelineDDBtn').hide();
  }
  else if(tab == 'timeline/all') {
    $('#timeline-all').show();
    $('#sexy-sort-btn').hide();
  }
  else if(tab == 'timeline/accepted') {
    $('#timeline-accepted').show();
    $('#sexy-sort-btn').hide();
  }
  else if(tab == 'timeline/completed') {
    $('#timeline-completed').show();
    $('#sexy-sort-btn').hide();
  }

  var owner = $('#username').attr('value');
  var cancel_type = "";

  $('#hangouts_sort').click(function() {
    window.location.href = '/foodie/'+owner+'?q='+tab+'/hangouts';
  });
  $('#lesson_sort').click(function() {
    window.location.href = '/foodie/'+owner+'?q='+tab+'/lesson';
  });
  $('#price_sort').click(function() {
    window.location.href = '/foodie/'+owner+'?q='+tab+'/price';
  });
  $('#time_sort').click(function() {
    window.location.href = '/foodie/'+owner+'?q='+tab;
  });
  $('#lcoation_sort').click(function() {
    window.location.href = '/foodie/'+owner+'?q='+tab+'/location';
  });

  // Cancel pending request
  $("[id^='pending_cancel']").click(function(){
      cancel_type = "pending";
      $("[id^='cancel_request_p']").openModal();
      cancel_request = $(this).val();
  });

  $("[id^='cancel_pending']").click(function(){
      cancel_type = "pending";
      $("[id^='cancel_pending_request']").openModal();
      cancel_request = $(this).val();
  });

  // Cancel accepted request
  $("[id^='accepted_cancel']").click(function(){
      cancel_type = "accepted"
      $("[id^='cancel_request_a']").openModal();
      cancel_request = $(this).val();
  });

  $("[id^='cancel_accepted']").click(function(){
      cancel_type = "accepted";
      $("[id^='cancel_accepted_request']").openModal();
      cancel_request = $(this).val();
  });
  
   // Confirm cancel request
  $("[id^='confirm_cancel_request']").click(function(){
      $.ajax({
        type: "POST",
        url: "/cancel",
        data: {'request' : cancel_request},
      });
    setTimeout(function(){ // Refresh after 1 second
      window.location.href = '/foodie/'+owner+'?q='+tab;
    }, 200); 
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
      window.location.href = '/foodie/'+owner+'?q='+tab;
    }, 200);
  });
  $("[id^='pending_confirm_modal']").click(function() {
    $('#respond').openModal();
    bidder = $(this).val();
  });
  // Accept confirm application
  $("#select_bid_button").click(function() {
    console.log(request.value);
    $.ajax({
      type: "POST",
      url: "/choose/"+request.value,
      data: {'bidder': bidder},
    });
    setTimeout(function(){ // Refresh after 1 second
      window.location.href = '/foodie/'+owner+'?q=table/pending';
    }, 200);
  });
  // Close pending confirm application modal
  $('#close_modal').click(function(){
    $('#respond').closeModal();
  });
})

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