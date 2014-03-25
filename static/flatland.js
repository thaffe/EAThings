var bot,map,tiles;
var blockWidth = 100.0/8,blockHeight = 100.0/8 * 1.69;
var activeMap, currentPos, currentMapIndex, lookDir;
var playback = 1;
var moveHist;
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
    moveHist = getHistSteps(index);
    currentPos = moveHist[0];
    currentMapIndex = index;

    updateMap();
    updateBot();
}

function getHistSteps(index){
    var h = window.hists[index];
    var l = window.botDir[index].slice(0);
    var p = window.botPos[index].slice(0);
    var res = [{pos:p.slice(0),dir:"dir"+l[0]+""+l[1]}];
    console.log("StartLook:"+l, "StartPos:"+p);
    for(var i = 0; i < h.length; i++){
        var dir = h[i];
        switch(dir){
            case 'l':
            if(l[0]){
                l[1] = -l[0];
                l[0] = 0;
            }else{
                l[0] = l[1];
                l[1] = 0;
            }
            break;
            case 'r':
            if(l[0]){
                l[1] = l[0];
                l[0] = 0;
            }else{
                l[0] = -l[1];
                l[1] = 0;
            }
        }
        t = p.slice(0);
        if(dir != 'n'){
            p[0] += l[0];
            p[1] += l[1];
        }
        console.log("Move:"+dir,"From:"+t, "To:"+p, "Look:"+l)
        res.push({
            pos:p.slice(0),
            dir:"dir"+l[0]+""+l[1]
        });
    }
    return res;
}

function step(forward){
    var index = forward && counter.time < moveHist.length - 1? ++counter.time :
        counter.time > 0 ? --counter.time : 0;
    currentPos = moveHist[index];

    tiles[currentPos.pos[0]][currentPos.pos[1]].children()[forward ? "fadeOut" : "fadeIn"](300,updateStats);
    updateBot();
}

function updateStats(){
    console.log("Food:"+$(".food:hidden").length, "Poison:"+$(".poison:hidden").length)
    $("#food-counter").text($(".food:hidden").length);
    $("#poison-counter").text($(".poison:hidden").length);
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
    bot.attr("class","bot "+currentPos.dir);
    bot.css(tiles[currentPos.pos[1]][currentPos.pos[0]].position());
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
        step(true);
        updateStats();
        if(this.counter >= 50){
            actions.clear();
        }
    },

    back:function(click){
        if(click) actions.clear();
        updateStats();
        step(false);
    },

    begin:function(){
        counter.time = -1;
        step(true);
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