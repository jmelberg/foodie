// Call functions from other js
$.getScript("../js/create_request.js");

$(document).ready(function() {
  var user = document.getElementById('user').getAttribute('value');
  var tab = getUrlParameter('q');
  $('ul.tabs').tabs();

  var current_request;
  if(tab == 'mine'){
  alert("here");
  $('ul.tabs').tabs('select_tab', 'mine');
  }
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

  if(tab == 'mine'){
    $('ul.tabs').tabs('select_tab', 'mine');
  }
  else if(tab=='all'){
    $('ul.tabs'.tabs('select_tab', 'all'));
  }
  else if(tab == 'location' || tab == 'price'){
    updateRequests(tab);
    
  }
  else {
    $('ul.tabs').tabs('select_tab', 'all');
  }

  function updateRequests(requests){
  $.ajax({
    url:"/requests",
    cache:false,
    data: {'requests': tab},
    async: true,
    success: function(response){
      $('body').html(response);
      $('#mine').hide();
      $('#pending').hide();
      $('#accepted').hide();
    }
  });
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