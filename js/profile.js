$(document).ready(function() {
  var tab = getUrlParameter('q');

  if(tab == 'table/all') {
    $('#table-all').show();
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
  }
  else if(tab == 'timeline/accepted') {
    $('#timeline-accepted').show();
  }
  else if(tab == 'timeline/completed') {
    $('#timeline-completed').show();
  }

  var owner = $('#username').attr('value');
  var cancel_type = "";

  // Cancel pending request
  $("[id^='pending_cancel']").click(function(){
      cancel_type = "pending";
      $('#cancel_request').openModal();
      cancel_request = $(this).val();
  });

  // Cancel accepted request
  $("[id^='accepted_cancel']").click(function(){
      cancel_type = "accepted"
      $('#cancel_request').openModal();
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
      if(cancel_type == "accepted") {
        window.location.href = '/foodie/'+owner+'?q=table/accepted';
      }
      if(cancel_type == "pending") {
        window.location.href = '/foodie/'+owner+'?q=table/pending';
      }
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


  // For sorted results
  if(tab == 'time'){
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