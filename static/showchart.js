
var chartData;
var options;

window.onbeforeunload = function(){
    var page = window.location.href.split("/");
    if(page[page.length-1].length > 3)
        return "Sure you want to reload settings and run will be reset";
}
function initChart(sds, means, bests, similarities){
    $chart = $("#chart");

    if(!$chart.length) return;

    labels = [];
    steps = Math.ceil(bests.length / 10.0)
    console.log(steps);

    var highest = 0;
    for(var i = 0; i <= bests.length; i++){
        if(bests[i] > highest) highest = bests[i];
        if(means[i] > highest) highest = means[i];
        if(sds[i] > highest) highest = sds[i];
    }

    var stepsize = highest/15.0;

    for (var i = 1; i <= bests.length; i++) {
        labels.push(i % steps == 0 ? i : "");
    }
    chartData = {
        labels: labels,
        datasets: [
            {
                fillColor: "rgba(217, 83, 79,0.2)",
                strokeColor: "rgba(217, 83, 79,1)",
                pointColor: "rgba(151,187,205,1)",
                pointStrokeColor: "#fff",
                data: bests
            },
            {
                fillColor: "rgba(92, 184, 92,0.2)",
                strokeColor: "rgba(92, 184, 92,1)",
                pointColor: "rgba(151,187,205,1)",
                pointStrokeColor: "#fff",
                data: means
            },
            {
                fillColor: "rgba(66, 139, 202,0.2)",
                strokeColor: "rgba(66, 139, 202,1)",
                pointColor: "rgba(220,220,220,1)",
                pointStrokeColor: "#fff",
                data: sds
            },
//            {
//                fillColor: "rgba(0, 83, 79,0.2)",
//                strokeColor: "rgba(0, 83, 79,1)",
//                pointColor: "rgba(151,187,205,1)",
//                pointStrokeColor: "#fff",
//                data: similarities
//            }
        ]
    };
    options = {
      pointDot: false,
      scaleOverride: true,
      scaleSteps: 15,
      scaleStepWidth: Math.ceil(stepsize)
    };
    var ctx = $chart.get(0).getContext("2d");

    drawChart();
    //var chart = new Chart(ctx).Line(data,options);
    options.animation = false;

    $(window).resize(function () {
        console.log("drawChart")
        drawChart();
    });

}

function drawChart() {
    var ctx = $("#chart");
    var width = Math.min(ctx.parent().width(), 800);

    ctx.attr({"width": width, "height": width / 1.3});
    new Chart(ctx.get(0).getContext("2d")).Line(chartData, options);
}
