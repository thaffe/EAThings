var progText;
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
     $("form").submit(function(e){
        e.preventDefault();
        var params = $(this).serialize();
        progText.text("Starting up");
        showPopup(null, "progress");
        $("html").unbind('click',closePopup);
        $.getJSON("/start?"+params,function(data){
            setTimeout(trackProgress,200);
        });
        return false;
    });

    showPopup(null, "settings");

});


function trackProgress(){
    $.getJSON("/progress",function(data){
        if(data.complete){
            $("html").click(closePopup);
            closePopup();
            initGame(data.game);
            initChart(data.sds,data.means,data.bests, data.similarity);

        }else{
            progText.text(data.m);
            setTimeout(trackProgress, 200);
        }
    })
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