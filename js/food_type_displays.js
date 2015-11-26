"use strict"
var FoodTypeDisplays = (function(FM) {

	/*
	* Display image 
	*/
	function displayImage(obj,foodType) {
		var imgEle = document.getElementById(obj.imgId);
		FM.searchKey(foodType" food",'n',function(data){
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

	/*
	* Display background image
	*/
	function displayBackground(obj,foodType) {
		var backgroundEle = document.getElementById(obj.backgroundId);
		FM.searchKey(foodType+" food",'q',function(data){
			// var index = Math.floor( Math.random() * data.length );
			var index = 1;

			//prefetch image
			var newImage = new Image();
			newImage.src = data[index].url;
			newImage.onload = function() {
				backgroundEle.style.backgroundImage = "url("+this.src+")";
			};
		});
	}

	return {
		displayImg: displayImage,
		displayBackground: displayBackground
	}
})(FlickrMe);

