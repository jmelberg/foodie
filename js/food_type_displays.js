"use strict"
var FoodTypeDisplays = (function(FM) {

	/*
	* Display image 
	*/
	function displayImage(obj,foodType) {
		var imgEle = document.getElementById(obj.imgId);
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

	/*
	* Display background image
	* Get the URL of images
	* @param size key word
	    s	small square 75x75
		q	large square 150x150
		t	thumbnail, 100 on longest side
		m	small, 240 on longest side
		n	small, 320 on longest side
		-	medium, 500 on longest side
		z	medium 640, 640 on longest side
		c	medium 800, 800 on longest side†
		b	large, 1024 on longest side*
		h	large 1600, 1600 on longest side†
		k	large 2048, 2048 on longest side†
		
		Example: FlickrMe.search("hello world",'n');
		More Info: https://www.flickr.com/services/api/misc.urls.html
	* @return {title:sometime,url:someurl}	
	*/
	function displayBackground(obj,foodType,size) {
		var sizeCode = size || 'q' ;
		var backgroundEle = document.getElementById(obj.backgroundId);
		FM.searchKey(foodType,sizeCode,function(data){
			var index = Math.floor( Math.random() * data.length );
			// var index = 1;

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

