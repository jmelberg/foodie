"use strict"
var FoodTypeDisplays = (function($,FM) {
	var imgEle;

	function displayImage(foodType) {
		FM.searchKey(foodType,'n',function(data){
			// var index = Math.floor( Math.random() * data.length );
			var index = 1;

			//prefetch image
			var newImage = new Image();
			newImage.src = data[index].url;
			newImage.onload = function() {
				imgEle.src = this.src;
			};
		});
	}

	return {
		init: function(classes,foodType) {
			imgEle = document.getElementsByClassName(classes.imgId)[0];

			displayImage(foodType);
		}
	}
})(jQuery,FlickrMe);

