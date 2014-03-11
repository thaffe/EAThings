var heightStep = 100/15.0;
var widthStep = 100/30.0;
var timePrStep = 150;
var object,catcher;

$(function(){
    catcher = $("#catcher");
    object = $("#object");
   resetObject(30-4,4);
   var c = [],o=[];
    for(var i = 0; i < 15; i++){
        c.push(i);
        o.push(30-4-i);
    }

    animate(c,o);

//   catcher.animate({left:stepSize+"%"},300);
});


function resetObject(startIndex,size){
    object.css({bottom:(heightStep*14)+"%",left:(startIndex*widthStep)+"%",width:(widthStep*size)+"%"});
}

function animate(catchSteps,objectSteps){
    for(var i = 0; i < catchSteps.length; i++){
        catcher.animate({left:(catchSteps[i]*widthStep)+"%"},timePrStep);
        object.animate({bottom:(heightStep*(14-i))+"%",left:(objectSteps[i]*widthStep)+"%"},timePrStep)
    }
}
