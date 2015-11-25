$(document).ready(function() {
  var tab = getUrlParameter('q');

  if(tab == 'table/all') {
    $('#table').show();
    $('#timeline').hide();
    $('#tableViewBtn').hide();
    $('#timelineViewBtn').show();
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

function findViewType(sParam)
{
    var sPageURL = window.location.search.substring(1);
    var sURLVariables = sPageURL.split('&');
    for (var i = 0; i < sURLVariables.length; i++) 
    {
        var sParameterName = sURLVariables[i].split('/');
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