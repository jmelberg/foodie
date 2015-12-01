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
      autoPlayHoverPause:true
  }); 
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
  $(".owl-left-arrow-wrapper").click(function(event) {
    console.log('hello');
    owl.trigger('owl.next');
  });
  $(".food-item-wrapper").hover(function(event) {
    $(this).children(".food-item-picture").children(".reply-icon").fadeIn();
    $(this).children(".food-item-picture").children(".food-selector").children(".owl-item-text").css('visibility','hidden');
    owl.trigger('owl.stop');
    $(this).children(".food-item-picture").css('color', 'blue');
  }, 
  function(e) {
    $(this).children(".food-item-picture").children(".reply-icon").fadeOut();
    $(this).children(".food-item-picture").children(".food-selector").children(".owl-item-text").css('visibility','visible');
    owl.trigger('owl.play',2500);
    e.stopPropagation();
  });
})();
