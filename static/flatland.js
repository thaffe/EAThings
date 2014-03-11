var bot,map,tiles;
var blockWidth = 100.0/8,blockHeight = 100.0/8 * 1.69;
var activeMap = window.maps[0];
var playback = 1;
var counter = {
    food:0,poison:0,time:0
}
$(function(){
     map = $("#map");
     map.css({maxWidth:activeMap.length*100});
     $(window).resize(function(){
            map.height(map.width());
            updateBot();
     });

     $("#maps a").click(function(){
        activeMap = window.maps[$("#maps a").index(this)];
        updateMap();
     });

     $(".controller button").click(function(){
        $(this).siblings().removeClass("active");
        actions[$(this).attr("data-type")](true);
     });

     $("#playback").change(function(){
            playback = parseInt(this.value);
     });

    bot = $("<div class='tile bot'><div>").css({width:blockWidth+"%",height:blockHeight+"%"});

    tiles = createMap(map, window.maps.length, window.maps.length);
    map.append(bot);
    updateMap();
    $(window).resize();
});

function move(dir){
    window.botPos[0] += dir[0];
    window.botPos[1] += dir[1]

    tiles[window.botPos[0]][window.botPos[1]].children().fadeOut(300,function(){
        counter[$(this).hasClass('food') ? 'food' : 'poison']+=1;
        updateStats();
        $(this).remove();
    });
    updateBot();
}

function updateStats(){
    console.log(counter);
    $("#food-counter").text(counter.food);
    $("#poison-counter").text(counter.poison);
    $("#time-counter").text(counter.time);
}

function updateMap(){
    for(var i = 0; i < activeMap.length; i++){
        for(var j = 0; j < activeMap[0].length; j++){
            if(activeMap[i][j]){
                tiles[i][j].html('<div class="'+map_class[activeMap[i][j]]+'"></div>')
            }
        }
    }
}

function updateBot(){
    bot.css(tiles[window.botPos[0]][window.botPos[1]].position());
}

function createMap(mapholder){
    var m = [];
    for(var i = 0; i < activeMap.length; i++){
        row = [];
        for(var j = 0; j < activeMap[0].length; j++){
            div = $("<div class='tile grass' style='width:"+blockWidth+"%;height:"+blockHeight+"%'></div>");
            row.push(div);
            mapholder.append(div);
        }
        m.push(row);
    }
    return m;
}

var actions = {
    playInterval: null,
    play:function(){
        if(!actions.clear()){
           $("#play").attr("class", "fa fa-pause").parent().addClass("active");
           actions.forward();
           actions.playInterval = setInterval(actions.forward, 500/playback);
        }
    },

    forward:function(click){
        if(click) actions.clear();
        counter.time++;
        updateStats();
        move([1,0]);
        if(this.counter >= 50){
            actions.clear();
        }
    },

    back:function(click){
        if(click) actions.clear();
        counter.time--;
        updateStats();
        move([-1,0]);
    },

    begin:function(){
        counter.time=0;
        updateStats();
        actions.clear();
    },

    end:function(){
        counter.time=50;
        updateStats();
        actions.clear();
    },

    clear:function(){
         if(actions.playInterval){
            $("#play").attr("class", "fa fa-play").parent().removeClass("active");
            clearInterval(actions.playInterval);
            actions.playInterval = null;
            return true;
        }
        return false;
    }
}

var map_class = {
    'f':'tile object food',
    'p':'tile object poison'
}