$(document).ready(function() {  
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

  //Selected
  $("[id^='select']").click(function(){
    var request = $(this).val();
    var user = document.getElementById('user').getAttribute('value');
    $.ajax({
      type: "POST",
      url: "/confirm",
      data: {'request' : request, 'approver': user},
    });
    top.location.href = '/requests';
  });                
});