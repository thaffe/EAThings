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

   $(".settings-toggle").click(function(){
        $("#settings").toggle(300);
   })
});



function show(id, hide){
console.log(id)
    $(hide+"[id!="+id+"]").addClass("hide");
    $(id).removeClass("hide");
}