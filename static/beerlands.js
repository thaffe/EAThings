var heightStep = 100/15.0;
var widthStep = 100/30.0;
var timePrStep = 150;
var object,catcher,objectholder;
var playback = 1;
var currentIndex = 0;


function initGame(states){
    currentIndex = 0;
    window.gameState = states;
    catcher = $("#catcher");
    object = $("#object");
    objectholder = $("#objectholder");

    $(".controller button").click(function(){
        $(this).siblings().removeClass("active");
        actions[$(this).attr("data-type")]();
     });

    updateStats();
    $("#playback").change(function(){
        playback = parseInt(this.value);
     });
    $("#play").parent().click();

    var s = 0,m = 0, f = 0;
    for(var i = 0; i < window.gameState.length; i++){
        var res = window.gameState[i].res;
        if(res == 0) m++;
        else if(res < 0) f++;
        else if(res > 0) s++;
    }
    $("#fail-total").text(f);
    $("#success-total").text(s);
    $("#miss-total").text(m);
}

function playState(index, callback){
    var s = window.gameState[index];
    updateStats();
    animate(s, function(){
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

function animate(r, callback){
    actions.stop();
    var time = timePrStep/playback;
    object.children(r.size >= 5 ? ".big" : ".small").show().siblings().hide();
    catcher.css(getLeft(r.c[0]));
    object.css({bottom:(heightStep*15)+"%"});
    objectholder.css({left:(r.o[0]*widthStep)+"%",width:(widthStep*r.size)+"%"});

    for(var i = 1; i < r.c.length; i++){
        var move = r.c[i-1] - r.c[i];
        if(move > 4){
            index = move > 0 ? -1 : r.c.length;
            catcher.animate(getLeft(index),0);
        }

        move = r.o[i-1] - r.o[i];
        if(move > 4){
            index = move > 0 ? -1 : r.c.length;
            objectholder.animate(getLeft(index),0);
            console.log("wrap object");
        }
        catcher.animate(getLeft(r.c[i]) ,time,"linear");
        objectholder.animate(getLeft(r.o[i]), time,"linear");
    }
    object.animate({bottom:"0%"},time * r.c.length, "linear",callback);

}

function getLeft(index){
    return {left:(index * widthStep)+"%"};
}


var actions = {
    play:function(forcePlay){
        var $p =  $("#play");
        if(forcePlay !== true && $p.hasClass("fa-pause")){
            $p.attr("class","fa fa-play");
            actions.stop();
            console.log("stop");
        }else{
            $p.attr("class","fa fa-pause");
            this.step();
        }
        updateStats();
    },

    step : function(){
        playState(currentIndex, actions.step);
        currentIndex++;
    },

    forward:function(){
        if(currentIndex >= 40) return;
        actions.play(true);
    },

    back:function(){
        if(currentIndex <= 0) return;
        currentIndex-=2;
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
       catcher.finish();
       object.finish();
       objectholder.finish();
    }
}