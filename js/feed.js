$(document).ready(function(){
var owlLength;
var owlCurrent;

/*
$('').(function(){
  $.ajax({
    type: "POST",
    url: '/authorizepayment',
      data: {'credit_card_id': JSON.stringify(data.credit_card_id)}
  });
});
*/

  $('.collapsible').collapsible({
    accordion : true // A setting that changes the collapsible behavior to expandable instead of the default accordion style
  });

  $("#slider").owlCarousel({
pagination: false,
afterAction: afterAction,
autoPlay: 2000
  });

  $("#slider1").owlCarousel({
pagination: false,
afterAction: afterAction,
autoPlay: 2000
  });

  $("#slider2").owlCarousel({
pagination: false,
afterAction: afterAction,
autoPlay: 2000
  });


function afterAction(){
owlLength = this.owl.owlItems.length;
}

/*

for(var i = 0; i < owlLength; i++){
if(i != owlCurrent){
var $this = $(this);
var current = '#' + i;
var checkThis = $(current)
var slider = $("#slider");
if(checkThis.hasClass('hidden')){
  alert(owlCurrent);
  checkThis.removeAttr('style').removeClass('hidden');
} else{
  checkThis.css('display','none').addClass('hidden');
}
}
}

*/
  $('.one').on('click', function(event){
  var $this = $(this);
  var checkThis = $('#one')
  var slider = $("#slider");
  if(checkThis.hasClass('hidden')){
    checkThis.removeAttr('style').removeClass('hidden');
  } else{
    checkThis.css('display','none').addClass('hidden');
  }
});

$('.two').on('click', function(event){
var $this = $(this);
var checkThis = $('#two')
var slider = $("#slider");
if(checkThis.hasClass('hidden')){
  checkThis.removeAttr('style').removeClass('hidden');
} else{
  checkThis.css('display','none').addClass('hidden');
}
});

$('.three').on('click', function(event){
var $this = $(this);
var checkThis = $('#three')
var slider = $("#slider");
if(checkThis.hasClass('hidden')){
  checkThis.removeAttr('style').removeClass('hidden');
} else{
  checkThis.css('display','none').addClass('hidden');
}
});

$('.four').on('click', function(event){
var $this = $(this);
var checkThis = $('#four')
var slider = $("#slider");
if(checkThis.hasClass('hidden')){
  checkThis.removeAttr('style').removeClass('hidden');
} else{
  checkThis.css('display','none').addClass('hidden');
}
});

$('.five').on('click', function(event){
var $this = $(this);
var checkThis = $('#five')
var slider = $("#slider");
if(checkThis.hasClass('hidden')){
  checkThis.removeAttr('style').removeClass('hidden');
} else{
  checkThis.css('display','none').addClass('hidden');
}
});

$('.six').on('click', function(event){
var $this = $(this);
var checkThis = $('#six')
var slider = $("#slider");
if(checkThis.hasClass('hidden')){
  checkThis.removeAttr('style').removeClass('hidden');
} else{
  checkThis.css('display','none').addClass('hidden');
}
});



});
