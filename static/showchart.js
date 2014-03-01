$(function(){
    console.log(fitnessGoal)
    labels = [];
    steps = Math.ceil(bests.length/10)
    for(var i = 1; i <= bests.length; i++){
        labels.push(i%steps == 0 ? i : "");
    }
    var data = {
        labels :labels,
    	datasets : [
    		{
                fillColor : "rgba(217, 83, 79,0.2)",
                strokeColor : "rgba(217, 83, 79,1)",
                pointColor : "rgba(151,187,205,1)",
                pointStrokeColor : "#fff",
                data :bests
            },
    		{
    			fillColor : "rgba(92, 184, 92,0.2)",
    			strokeColor : "rgba(92, 184, 92,1)",
    			pointColor : "rgba(151,187,205,1)",
    			pointStrokeColor : "#fff",
    			data :means
    		},
    		{
    			fillColor : "rgba(66, 139, 202,0.2)",
    			strokeColor : "rgba(66, 139, 202,1)",
    			pointColor : "rgba(220,220,220,1)",
    			pointStrokeColor : "#fff",
    			data :sds
    		},
    	]
    };
    var options = {
      pointDot:false,
      scaleOverride:true,
      scaleSteps:Math.ceil(fitnessGoal/2),
      scaleStepWidth:2
    };
    var ctx = $("#chart").get(0).getContext("2d");

    drawChart();
     //var chart = new Chart(ctx).Line(data,options);
    options.animation = false;

    $(window).resize(function(){
        drawChart();
    });

    function drawChart(){
         var ctx = $("#chart");
         var width = Math.min(ctx.parent().width(),800);

         ctx.attr({"width":width, "height":width/1.3});
        new Chart(ctx.get(0).getContext("2d")).Line(data,options);
    }
});