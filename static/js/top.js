$(function(){
    $("#user").hover(function(){
        $("#user span").css("display", "block");
    });
    $("#user").mouseleave(function(){
        $("#user span").css("display", "none");
    });
});