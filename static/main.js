var progText;
var testCurrent = false;
$(function(){

    progText = $("#progressText");

   $("#parentStrategy").change(function(){
    id = this.value+"-parent-opts";
    show("#"+id,"[id$=parent-opts]");
   });

   $("#puzzle").change(function(){
       id = this.value+"-puzzle-opts";
       show("#"+id,"[id$=puzzle-opts]");
   });

   $("#parentStrategy").trigger('change');

   $(".popup .container").click(function(e){
        e.stopPropagation();
   });
    $("#test-current").click(function(){
        testCurrent = true;
    })


   $(".chart-toggle").click(function(e){
        showPopup(e,"chartHolder");
        setTimeout(function(){
            $(window).resize();
        },500);
   });

    $(".showpopup").click(showPopup);

    $(".restart-btn").click(function(){
        $("form").submit();
    });

    $("html").click(closePopup);
     $("form").submit(function(e){
        e.preventDefault();
        var params = $(this).serialize();
        progText.text("Starting up");
        showPopup(null, "progress");
        $.getJSON("/start?"+params,function(data){
            setTimeout(trackProgress,200);
        });
        return false;
    });

    showPopup(null, "settings");

});


function initNeural(net){
    var canvas = $(canvas).get(0)
    var ctx = canvas.getContext("2d");
    var particleSystem
}

function trackProgress(){
    p = {}
    if(testCurrent){
        testCurrent = false;
        p['requestupdate'] = true;
    }
    $.getJSON("/progress",p,function(data){
        if(data.game){
            initGame(data.game);
            initChart(data.sds,data.means,data.bests, data.similarity);
            initNet(data.net);
            $("#fitness").text(data.fitness);
        }
        if(data.complete){
            closePopup();
            $("#progress")
        }else{
            progText.text(data.m);
            setTimeout(trackProgress, 500);
        }
    });
}

function showPopup(e, target){
    closePopup();
    $("#"+(target ? target : $(this).attr("data-target"))).addClass("show");
    if(e)
        e.stopPropagation();
}


function closePopup(){
    $(".popup.show").removeClass("show");
}

function show(id, hide){
console.log(id)
    $(hide+"[id!="+id+"]").addClass("hide");
    $(id).removeClass("hide");
}