$(document).ready(function(){
  // the "href" attribute of .modal-trigger must specify the modal ID that wants to be triggered
  var exp, fir, enth;
  var type = "foodie";

  $('.modal-trigger').leanModal();


  $("#submitreview").click(function(){
    //var ratingtype = document.getElementById('ratingtype').value;
    //var experience = document.getElementById('experience').value;
    //var enthusiasm = document.getElementById('enthusiasm').value;
    //var friendliness = document.getElementById('friendliness').value;
    var experiencecomment = document.getElementById('experiencecomment').value;
    var enthusiasmcomment = document.getElementById('enthusiasmcomment').value;
    var friendlinesscomment = document.getElementById('friendlinesscomment').value;
    var keyz = document.getElementById('pendingkey').value;
    var recipient = document.getElementById('recipient').value;

    $.ajax({
      type: "POST",
      url: '/ratings',
        data: {
        'pendingkey':keyz,
        'ratingtype':type,
        'experience':5,
        'enthusiasm':5,
        'friendliness':5,
        'experiencecomments':experiencecomment,
        'enthusiasmcomments':enthusiasmcomment,
        'friendlinesscomments':friendlinesscomment}
    });


  });

/* HOVER OVER STUFF NOT WORKING ATM.



$("#exp1").hover(function(){
  var check = $("#exp1").hasClass("clicked");
  if(check = false){
    $("#exp1").addClass("wineglassactive");
  }
    }, function(){
      if(check = false){
    $("#exp1").removeClass("wineglassactive");
  }
});

$("#exp2").hover(function(){
  if(check = false){
  $("#exp1").addClass("wineglassactive");
  $("#exp2").addClass("wineglassactive");
}
  }, function(){
    if(check = false){
    $("#exp1").removeClass("wineglassactive");
    $("#exp2").removeClass("wineglassactive");
  }

});

$("#exp3").hover(function(){
  var check = $("#exp1").hasClass("clicked");
  if(check = false){
  $("#exp1").addClass("wineglassactive");
  $("#exp2").addClass("wineglassactive");
  $("#exp3").addClass("wineglassactive");
}
  }, function(){
    if(check = false){
    $("#exp1").removeClass("wineglassactive");
    $("#exp2").removeClass("wineglassactive");
    $("#exp3").removeClass("wineglassactive");
  }
});

$("#exp4").hover(function(){
  var check = $("#exp1").hasClass("clicked");

  if(check = false){
  $("#exp1").addClass("wineglassactive");
  $("#exp2").addClass("wineglassactive");
  $("#exp3").addClass("wineglassactive");
  $("#exp4").addClass("wineglassactive");
}
  }, function(){
    if(check = false){
    $("#exp1").removeClass("wineglassactive");
    $("#exp2").removeClass("wineglassactive");
    $("#exp3").removeClass("wineglassactive");
    $("#exp4").removeClass("wineglassactive");
  }
});

$("#exp5").hover(function(){
  var check = $("#exp1").hasClass("clicked");

  if(check = false){
  $("#exp1").addClass("wineglassactive");
  $("#exp2").addClass("wineglassactive");
  $("#exp3").addClass("wineglassactive");
  $("#exp4").addClass("wineglassactive");
  $("#exp5").addClass("wineglassactive");
}
  }, function(){
    if(check = false){
    $("#exp1").removeClass("wineglassactive");
    $("#exp2").removeClass("wineglassactive");
    $("#exp3").removeClass("wineglassactive");
    $("#exp4").removeClass("wineglassactive");
    $("#exp5").removeClass("wineglassactive");
  }
});

*/

/* CLICK ON STUFF */

$("#exp1").click(function(){
    $("#exp1").addClass("wineglassactive");
    $("#exp1").addClass("clicked");
    $("#exp2").addClass("clicked");
    $("#exp3").addClass("clicked");
    $("#exp4").addClass("clicked");
    $("#exp5").addClass("clicked");
    $("#exp2").removeClass("wineglassactive");
    $("#exp3").removeClass("wineglassactive");
    $("#exp4").removeClass("wineglassactive");
    $("#exp5").removeClass("wineglassactive");
    exp = 1;
    });

$("#exp2").click(function(){
  $("#exp1").addClass("wineglassactive");
  $("#exp2").addClass("wineglassactive");
  $("#exp1").addClass("clicked");
  $("#exp2").addClass("clicked");
  $("#exp3").addClass("clicked");
  $("#exp4").addClass("clicked");
  $("#exp5").addClass("clicked");
  $("#exp3").removeClass("wineglassactive");
  $("#exp4").removeClass("wineglassactive");
  $("#exp5").removeClass("wineglassactive");
  exp = 2;
  });

$("#exp3").click(function(){
  $("#exp1").addClass("wineglassactive");
  $("#exp2").addClass("wineglassactive");
  $("#exp3").addClass("wineglassactive");
  $("#exp1").addClass("clicked");
  $("#exp2").addClass("clicked");
  $("#exp3").addClass("clicked");
  $("#exp4").addClass("clicked");
  $("#exp5").addClass("clicked");
  $("#exp4").removeClass("wineglassactive");
  $("#exp5").removeClass("wineglassactive");
  exp = 3;
  });

$("#exp4").click(function(){
  $("#exp1").addClass("wineglassactive");
  $("#exp2").addClass("wineglassactive");
  $("#exp3").addClass("wineglassactive");
  $("#exp4").addClass("wineglassactive");
  $("#exp1").addClass("clicked");
  $("#exp2").addClass("clicked");
  $("#exp3").addClass("clicked");
  $("#exp4").addClass("clicked");
  $("#exp5").addClass("clicked");
  $("#exp5").removeClass("wineglassactive");
  exp = 4;
  });

$("#exp5").click(function(){
  $("#exp1").addClass("wineglassactive");
  $("#exp2").addClass("wineglassactive");
  $("#exp3").addClass("wineglassactive");
  $("#exp4").addClass("wineglassactive");
  $("#exp5").addClass("wineglassactive");
  $("#exp1").addClass("clicked");
  $("#exp2").addClass("clicked");
  $("#exp3").addClass("clicked");
  $("#exp4").addClass("clicked");
  $("#exp5").addClass("clicked");
  exp = 5;
  });

  $("#fir1").click(function(){
      $("#fir1").addClass("wineglassactive");
      $("#fir1").addClass("clicked");
      $("#fir2").addClass("clicked");
      $("#fir3").addClass("clicked");
      $("#fir4").addClass("clicked");
      $("#fir5").addClass("clicked");
      $("#fir2").removeClass("wineglassactive");
      $("#fir3").removeClass("wineglassactive");
      $("#fir4").removeClass("wineglassactive");
      $("#fir5").removeClass("wineglassactive");
      fir = 1;
      });

  $("#fir2").click(function(){
    $("#fir1").addClass("wineglassactive");
    $("#fir2").addClass("wineglassactive");
    $("#fir1").addClass("clicked");
    $("#fir2").addClass("clicked");
    $("#fir3").addClass("clicked");
    $("#fir4").addClass("clicked");
    $("#fir5").addClass("clicked");
    $("#fir3").removeClass("wineglassactive");
    $("#fir4").removeClass("wineglassactive");
    $("#fir5").removeClass("wineglassactive");
    fir = 2;
    });

  $("#fir3").click(function(){
    $("#fir1").addClass("wineglassactive");
    $("#fir2").addClass("wineglassactive");
    $("#fir3").addClass("wineglassactive");
    $("#fir1").addClass("clicked");
    $("#fir2").addClass("clicked");
    $("#fir3").addClass("clicked");
    $("#fir4").addClass("clicked");
    $("#fir5").addClass("clicked");
    $("#fir4").removeClass("wineglassactive");
    $("#fir5").removeClass("wineglassactive");
    fir = 3;
    });

  $("#fir4").click(function(){
    $("#fir1").addClass("wineglassactive");
    $("#fir2").addClass("wineglassactive");
    $("#fir3").addClass("wineglassactive");
    $("#fir4").addClass("wineglassactive");
    $("#fir1").addClass("clicked");
    $("#fir2").addClass("clicked");
    $("#fir3").addClass("clicked");
    $("#fir4").addClass("clicked");
    $("#fir5").addClass("clicked");
    $("#fir5").removeClass("wineglassactive");
    fir = 4;
    });

  $("#fir5").click(function(){
    $("#fir1").addClass("wineglassactive");
    $("#fir2").addClass("wineglassactive");
    $("#fir3").addClass("wineglassactive");
    $("#fir4").addClass("wineglassactive");
    $("#fir5").addClass("wineglassactive");
    $("#fir1").addClass("clicked");
    $("#fir2").addClass("clicked");
    $("#fir3").addClass("clicked");
    $("#fir4").addClass("clicked");
    $("#fir5").addClass("clicked");
    fir = 5;
    });

    $("#enth1").click(function(){
        $("#enth1").addClass("wineglassactive");
        $("#enth1").addClass("clicked");
        $("#enth2").addClass("clicked");
        $("#enth3").addClass("clicked");
        $("#enth4").addClass("clicked");
        $("#enth5").addClass("clicked");
        $("#enth2").removeClass("wineglassactive");
        $("#enth3").removeClass("wineglassactive");
        $("#enth4").removeClass("wineglassactive");
        $("#enth5").removeClass("wineglassactive");
        enth = 1;
        });

    $("#enth2").click(function(){
      $("#enth1").addClass("wineglassactive");
      $("#enth2").addClass("wineglassactive");
      $("#enth1").addClass("clicked");
      $("#enth2").addClass("clicked");
      $("#enth3").addClass("clicked");
      $("#enth4").addClass("clicked");
      $("#enth5").addClass("clicked");
      $("#enth3").removeClass("wineglassactive");
      $("#enth4").removeClass("wineglassactive");
      $("#enth5").removeClass("wineglassactive");
      enth = 2;
      });

    $("#enth3").click(function(){
      $("#enth1").addClass("wineglassactive");
      $("#enth2").addClass("wineglassactive");
      $("#enth3").addClass("wineglassactive");
      $("#enth1").addClass("clicked");
      $("#enth2").addClass("clicked");
      $("#enth3").addClass("clicked");
      $("#enth4").addClass("clicked");
      $("#enth5").addClass("clicked");
      $("#enth4").removeClass("wineglassactive");
      $("#enth5").removeClass("wineglassactive");
      enth = 3;
      });

    $("#enth4").click(function(){
      $("#enth1").addClass("wineglassactive");
      $("#enth2").addClass("wineglassactive");
      $("#enth3").addClass("wineglassactive");
      $("#enth4").addClass("wineglassactive");
      $("#enth1").addClass("clicked");
      $("#enth2").addClass("clicked");
      $("#enth3").addClass("clicked");
      $("#enth4").addClass("clicked");
      $("#enth5").addClass("clicked");
      $("#enth5").removeClass("wineglassactive");
      enth = 4;
      });

    $("#enth5").click(function(){
      $("#enth1").addClass("wineglassactive");
      $("#enth2").addClass("wineglassactive");
      $("#enth3").addClass("wineglassactive");
      $("#enth4").addClass("wineglassactive");
      $("#enth5").addClass("wineglassactive");
      $("#enth1").addClass("clicked");
      $("#enth2").addClass("clicked");
      $("#enth3").addClass("clicked");
      $("#enth4").addClass("clicked");
      $("#enth5").addClass("clicked");
      enth = 5;
      });

});
