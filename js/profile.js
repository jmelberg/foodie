$(document).ready(function() {
  var tab = getUrlParameter('q');

  if(tab == 'table/all') {
    $('#timeline-dropdown').hide();
    $('#table-dropdown').show();
    $('#table').show();
    $('#timeline-all').hide();
    $('#tableViewBtn').hide();
    $('#timelineViewBtn').show();
  } 
  else if(tab == 'table/pending') {
    $('#timeline-dropdown').hide();
    $('#table-dropdown').show();

  }
  else if(tab == 'table/accepted') {
    $('#timeline-dropdown').hide();
    $('#table-dropdown').show();

  }
  else if(tab == 'table/completed') {
    $('#timeline-dropdown').hide();
    $('#table-dropdown').show();
  }
  else if(tab == 'timeline/pending') {
    $('#timeline-all').hide();
    $('#timeline-pending').show();
  }
  else if(tab == 'timeline/accepted') {

  }
  else if(tab == 'timeline/completed') {

  }
  


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