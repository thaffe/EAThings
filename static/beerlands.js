var heightStep = 100/15.0;
var widthStep = 100/30.0;
var timePrStep = 150;
var object,catcher;

$(function(){
    catcher = $("#catcher");
    object = $("#object");
   resetObject(30-4,4);

    i = 0;
    function play(){
        if(i < window.gameState.length){
            i++;
            playState(i, play)
        }
    }

    play();

//   catcher.animate({left:stepSize+"%"},300);
});


function resetObject(startIndex,size){
    object.css({bottom:(heightStep*14)+"%",left:(startIndex*widthStep)+"%",width:(widthStep*size)+"%"});
}

function playState(index, callback){
    var s = window.gameState[index];
    animate(s.c,s.o,callback);
}

function animate(catchSteps,objectSteps, callback){
    for(var i = 0; i < catchSteps.length; i++){
        catcher.animate({left:(catchSteps[i]*widthStep)+"%"}, timePrStep, i == catchSteps.length -1 ? callback : null);
        object.animate({bottom:(heightStep*(14-i))+"%",left:(objectSteps[i]*widthStep)+"%"},timePrStep)
    }
}
