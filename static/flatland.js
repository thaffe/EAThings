var bot,map,tiles;
var blockWidth = 100.0/8,blockHeight = 100.0/8 * 1.69;
var activeMap, currentPos, currentMapIndex, lookDir;
var playback = 1;
var moveHist;
var counter;
var currentGame;
function initGame(game){
    counter = {
          food:0,poison:0,time:0
      }

    currentGame = game;
     map.css({maxWidth:currentGame.maps[0].length*100});
    $("#maps").html("");
    for(var i = 0; i < game.mapRes.length; i++){
        var a = '<a class="list-group-item" id="map-$loop.index0"><h4 class="list-group-item-heading">Map ';
        a+= (i+1)+'</h4><p class="list-group-item-text">Best result food:';
        a+= game.mapRes[i][0]+'poison:'+game.mapRes[i][1]+'</p></a>';
        $("#maps").append(a);
    }
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

    setMap(0);
    $(window).resize();

}

$(function(){
    currentPos = {dir:[1,0],pos:[0,0]};
    bot = $("<div class='tile bot'><div>").css({width:blockWidth+"%",height:blockHeight+"%"});
    map = $("#map");
    tiles = createMap(map, 8, 8);
    map.append(bot);

    $(window).resize(function(){
            map.height(map.width());
            updateBot();
     });
    $(window).resize();
})

function setMap(index){
    $("#maps a:eq("+index+")").addClass("active").siblings().removeClass("active");
    counter.time = 0;
    activeMap = currentGame.maps[index].slice(0);
    moveHist = getHistSteps(index);
    currentPos = moveHist[0];
    currentMapIndex = index;

    updateMap();
    updateBot();
}

function getHistSteps(index){
    var max = 7;
    var h = currentGame.hists[index];
    var l = currentGame.botDir[index].slice(0);
    var p = currentGame.botPos[index].slice(0);
    var res = [{pos:p.slice(0),dir:"dir"+l[0]+""+l[1]}];
    console.log("StartLook:"+l, "StartPos:"+p, "Histlength:"+h.length);
    for(var i = 0; i < h.length; i++){
        var dir = h[i];
        switch(dir){
            case 'r':
            if(l[0]){
                l[1] = -l[0];
                l[0] = 0;
            }else{
                l[0] = l[1];
                l[1] = 0;
            }
            break;
            case 'l':
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

        if(p[0] > max) p[0] = 0;
        if(p[1] > max) p[1] = 0;
        if(p[0] < 0) p[0] = max;
        if(p[1] < 0) p[1] = max;

        console.log("Move:"+dir,"From:"+t, "To:"+p, "Look:"+l)
        res.push({
            pos:p.slice(0),
            dir:"dir"+l[0]+""+l[1]
        });
    }
    return res;
}

function step(forward){
    if(forward && counter.time < moveHist.length - 1) counter.time++;
    else if(!forward && counter.time) counter.time--;

    if(!forward)fadeTile(currentPos.pos,forward);

    currentPos = moveHist[counter.time];

    if(forward) fadeTile(currentPos.pos,forward);
    updateBot();
}

function fadeTile(pos, fadeOut){
    tiles[pos[0]][pos[1]].children()[fadeOut ? "fadeOut" : "fadeIn"](300, updateStats);
}

function updateStats(){
    console.log("Food:"+$(".food:hidden").length, "Poison:"+$(".poison:hidden").length)
    $("#food-counter").text($(".food:hidden").length);
    $("#poison-counter").text($(".poison:hidden").length);
    $("#time-counter").text(counter.time);
    var done = counter.time - 1 >= 0 ? currentGame.hists[currentMapIndex][counter.time - 1] : "First";
    var next = currentGame.hists[currentMapIndex][counter.time];
    $("#movedone").text("Move:"+done+" Next:"+next);
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
    bot.css(tiles[currentPos.pos[0]][currentPos.pos[1]].position());
}

function createMap(mapholder){
    var m = [];
    for(var i = 0; i < 8; i++){
        row = [];
        for(var j = 0; j < 8; j++){
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
        $(".poison,.food").fadeIn();
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