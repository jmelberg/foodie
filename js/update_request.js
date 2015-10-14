// Set active tab
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
    success: function(response){
      $('body').html(response);
      $('#mine').hide();
      $('#pending').hide();
      $('#accepted').hide();
      $('ul.tabs').tabs('select_tab', 'all');
    }
  });
}