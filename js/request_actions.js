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
