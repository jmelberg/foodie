"use strict"
var RequestSuggestionGrid = (function($,FM){
	var wrappers;
	var itemSelector;
	var textSelector;
	var foodTypeInputId;
	var maxCategorySearch = 12;
	var suggestionList = Array(
		"thai food",
		"japanese food",
		"chinese food",
		"italian food",
		"vietnamese food",
		"ice cream",
		"hawaiian food",
		"korean food",
		"sea food",
		"sushi",
		"shake shack burgers",
		"in-n-out burgers",
		"desserts"
	);

	function displaySuggestionImages(categories) {
		grabUrlFromCategory(categories,function(index) {

			return function(data){
				var randomIndex = Math.floor( Math.random() * data.length );
				var url = "url(" + data[randomIndex].url + ")";
				wrappers[index].getElementsByClassName(itemSelector)[0].style.backgroundImage = url;
				wrappers[index].getElementsByClassName(textSelector)[0].innerHTML = categories[index];
			}
		});
	}

	function grabUrlFromCategory(categories,cb) {
		var shuffledArr = shuffle(categories);
		var resultObj = [];
		for(var i = 0; i<maxCategorySearch; i++) {
			FM.searchKey( shuffledArr[i],"n",cb(i) );
		}
	}


	function shuffle(array) {
	  var currentIndex = array.length, temporaryValue, randomIndex ;

	  // While there remain elements to shuffle...
	  while (0 !== currentIndex) {

	    // Pick a remaining element...
	    randomIndex = Math.floor(Math.random() * currentIndex);
	    currentIndex -= 1;

	    // And swap it with the current element.
	    temporaryValue = array[currentIndex];
	    array[currentIndex] = array[randomIndex];
	    array[randomIndex] = temporaryValue;
	  }

	  return array;
	}

	function attachHoverEvent() {
		wrappers.hover(function(e){
			$(this).children('.'+textSelector).fadeIn();
			var itemEle = $(this).children('.'+itemSelector)[0];

			itemEle.style.MozTransform = 'scale(1.2,1.2)';
			itemEle.style.webkitTransform = 'scale(1.2,1.2)';
		    itemEle.style.msTransform = 'scale(1.2,1.2)';
		    itemEle.style.transform = 'scale(1.2,1.2)';
		    itemEle.style.opacity = '.7';
		    itemEle.style.zIndex = '-10';

			e.stopPropagation();
		}, function(e) {
			$(this).children('.'+textSelector).hide();
			var itemEle = $(this).children('.'+itemSelector)[0];

			itemEle.style.MozTransform = 'scale(1,1)';
			itemEle.style.webkitTransform = 'scale(1,1)';
		    itemEle.style.msTransform = 'scale(1,1)';
		    itemEle.style.transform = 'scale(1,1)';
		    itemEle.style.opacity = '1';
		    itemEle.style.zIndex = '0';

			e.stopPropagation();
		})
		.on('click',function() {
			var foodType = $(this).children('.'+textSelector).html();

			$("#"+foodTypeInputId).val(foodType);
		});
	}

	return {
		init: function(classes) {
			wrappers = $("."+classes.wrapperSelector);
			itemSelector = classes.itemSelector;
			textSelector = classes.textSelector;
			foodTypeInputId = classes.foodTypeInputId;

			attachHoverEvent();
			displaySuggestionImages(suggestionList);
		}

	}


})(jQuery,FlickrMe);

