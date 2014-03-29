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

   $(".popup").click(function(e){
        e.stopPropagation();
   });

   $("html").click(function(){
        $(".popup.show").removeClass("show");
   });

   $(".chart-toggle").click(function(e){
        $("#chartHolder").addClass('show');
        setTimeout(function(){
            $(window).resize();
        },500);

        e.stopPropagation();
   });
   $(".settings-toggle").click(function(e){
        $("#settings").addClass("show");
        e.stopPropagation();
   });
});



function show(id, hide){
console.log(id)
    $(hide+"[id!="+id+"]").addClass("hide");
    $(id).removeClass("hide");
}