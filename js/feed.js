"use strict"
var FeedCarousel = (function () {
  var owl = $(".owl-slides");
 
  owl.owlCarousel({
      items : 5, // items above 1000px browser width
      itemsDesktop : [1000,5], //5 items between 1000px and 901px
      itemsDesktopSmall : [900,3], // betweem 900px and 601px
      itemsTablet: [600,2], //2 items between 600 and 0
      itemsMobile : false, // itemsMobile disabled - inherit from itemsTablet option
      lazyLoad : true,
      // navigation : true,
      autoPlay: true,
  });
<<<<<<< HEAD
 
  // Custom Navigation Events
  $(".next").click(function(){
    owl.trigger('owl.next');
  })
  $(".prev").click(function(){
    owl.trigger('owl.prev');
  })
  $(".play").click(function(){
    owl.trigger('owl.play',1000); //owl.play event accept autoPlay speed as second parameter
  })
  $(".stop").click(function(){
    owl.trigger('owl.stop');
  })
})();
=======

$( "[id^=slider]" ).owlCarousel({
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
>>>>>>> 649b3382630c6bac99db4f3ac0b5ab03ab63bc9d
