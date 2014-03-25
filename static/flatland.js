var bot,map,tiles;
var blockWidth = 100.0/8,blockHeight = 100.0/8 * 1.69;
var activeMap, currentPos, currentMapIndex, lookDir;
var playback = 1;
var counter = {
    food:0,poison:0,time:0
}
$(function(){
     map = $("#map");
     map.css({maxWidth:window.maps[0].length*100});
     $(window).resize(function(){
            map.height(map.width());
            updateBot();
     });

     $("#maps a").click(function(){
        var index = $("#maps a").index(this);
        setMap(index);
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
    setMap(0);
    $(window).resize();

});

function setMap(index){
    counter.time = 0;
    activeMap = window.maps[index].slice(0);
    currentPos = window.botPos[index].slice(0);
    lookDir = window.botDir[index].slice(0);
    currentMapIndex = index;
    updateMap();
    updateBot();
}

function move(){
    var dir = window.hists[currentMapIndex][counter.time];
    console.log("Move in:"+dir)
    if(dir == 'n') return;

    switch(dir){
        case 'l':
        if(lookDir[0]){
            lookDir[1] = lookDir[0];
            lookDir[0] = 0;
        }else{
            lookDir[0] = -lookDir[1];
            lookDir[1] = 0;
        }
        break;
        case 'r':
        if(lookDir[0]){
            lookDir[1] = -lookDir[0];
            lookDir[0] = 0;
        }else{
            lookDir[0] = lookDir[1];
            lookDir[1] = 0;
        }
    }
    currentPos[0] += lookDir[0];
    currentPos[1] += lookDir[1]

    tiles[currentPos[0]][currentPos[1]].children().fadeOut(300,function(){
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
    for(var i = 0; i < window.maps[0].length; i++){
        for(var j = 0; j < window.maps[0][0].length; j++){
            if(activeMap[i][j]){
                tiles[i][j].html('<div class="'+map_class[activeMap[i][j]]+'"></div>')
            }
        }
    }
}

function updateBot(){
    bot.css(tiles[currentPos[0]][currentPos[1]].position());
}

function createMap(mapholder){
    var m = [];
    for(var i = 0; i < window.maps[0].length; i++){
        row = [];
        for(var j = 0; j < window.maps[0][0].length; j++){
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
        move();
        updateStats();
        counter.time++;
        if(this.counter >= 50){
            actions.clear();
        }
    },

    back:function(click){
        if(click) actions.clear();
        counter.time--;
        updateStats();
        move();
    },

    begin:function(){
        setMap(currentIndex);
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