$(function(){
    $(".btn").on('click', function(){
        $.ajax({
            type:"POST",
            url:"/app/sync_host/",
            dataType:"json",
            success:function(data){
                console.log('success');
            },
            error:function(data){
                console.log('error');
            }
        });
    });
});