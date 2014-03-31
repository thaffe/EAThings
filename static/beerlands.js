var heightStep = 100/15.0;
var widthStep = 100/30.0;
var timePrStep = 150;
var object,catcher;
var playback = 1;
var currentIndex = 0;

$(function(){
    catcher = $("#catcher");
    object = $("#object");

    $(".controller button").click(function(){
        $(this).siblings().removeClass("active");
        actions[$(this).attr("data-type")](true);
     });

    updateStats();
    $("#playback").change(function(){
        playback = parseInt(this.value);
     });
    $("#play").parent().click();
});


function resetObject(startIndex,size){
    object.css({bottom:(heightStep*14)+"%",left:(startIndex*widthStep)+"%",width:(widthStep*size)+"%"});
}

function playState(index, callback){
    var s = window.gameState[index];
    resetObject(s.o[0],s.size);
    animate(s.c,s.o, function(){
        updateStats();
        callback();
    });
}

function updateStats(){
    var s = 0, m = 0, f = 0;

    for(var i = 0; i < currentIndex; i++){

        var res = window.gameState[i].res;
        if(res == 0) m++;
        else if(res < 0) f++;
        else if(res > 0) s++;
    }

    $("#success").text(s);
    $("#miss").text(m);
    $("#fail").text(f);
    $("#stats").html(h3("Round", currentIndex+1));
}

function h3(l,v){
    return "<h3>"+l+": "+v+"</h3>";
}

function animate(catchSteps,objectSteps, callback){
    for(var i = 0; i < catchSteps.length; i++){
        catcher.animate({left:(catchSteps[i]*widthStep)+"%"}, timePrStep/playback, i == catchSteps.length -1 ? callback : null);
        object.animate({bottom:(heightStep*(14-i))+"%",left:(objectSteps[i]*widthStep)+"%"},timePrStep/playback)
    }
}


var actions = {
    play:function(forcePlay){
        actions.stop();
        var $p =  $("#play");
        if(!forcePlay && $p.hasClass("fa fa-pause active")){
            $p.attr("class","fa fa-play");
        }else{
            $p.attr("class","fa fa-pause");
            this.step();
        }
    },

    step : function(){
        playState(currentIndex++, actions.step);
    },

    forward:function(){
        if(currentIndex >= 15) return;
        currentIndex++;
        actions.play(true);
    },

    back:function(){
        if(currentIndex <= 0) return;
        currentIndex--;
        if(actions.timeout) clearTimeout(actions.timeout);

        timeout = setTimeout(function(){
            actions.play(true);
        }, 700);
    },
    timeout : null,
    begin:function(){
        currentIndex = 0;
        actions.play(true);
    },

    end:function(){

    },

    stop : function(){
       catcher.stop(true);
       object.stop(true);
    }
}