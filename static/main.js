$(function(){
   $("#parentStrategy").change(function(){
    id = this.value+"-parent-opts";
    show("#"+id,"[id$=parent-opts]");
   });

   $("#puzzle").change(function(){
       id = this.value+"-puzzle-opts";
       show("#"+id,"[id$=puzzle-opts]");
   });

   $("#puzzle").trigger('change');
   $("#parentStrategy").trigger('change');

   $(".popup .container").click(function(e){
        e.stopPropagation();
   });

   $("html").click(closePopup);

   $(".chart-toggle").click(function(e){
        showPopup(e,"chartHolder");
        setTimeout(function(){
            $(window).resize();
        },500);
   });

   $(".showpopup").click(showPopup);
});

function showPopup(e, target){
    closePopup();
    $("#"+(target ? target : $(this).attr("data-target"))).addClass("show");
    e.stopPropagation();
}


function closePopup(){
    $(".popup.show").removeClass("show");
}

function show(id, hide){
console.log(id)
    $(hide+"[id!="+id+"]").addClass("hide");
    $(id).removeClass("hide");
}