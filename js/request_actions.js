// Call functions from other js
$.getScript("../js/create_request.js");
var current_request;

// Hide requests
$("[id^='hide']").click(function(){
    $(this).parents().eq(1).hide();
});

$(document).ready(function() {
  var user = document.getElementById('user').getAttribute('value');
  var tab = getUrlParameter('q')
  $('ul.tabs').tabs()

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