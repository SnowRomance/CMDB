$(function(){
    $("#all").on("click", function(){
        $("table tr td").find("input").attr("checked","checked")
    });
    $("#all_not").on("click", function(){
        $("table tr td").find("input").removeAttr("checked")
    });

    $("#accept").on("click", function(){
        var requestid_list = []
        var request_nick_name_list = []
        var request_host_name_list = []
        var username = $("#user_list").val()
        console.log(username)
        $(".checkbox:checked").each(function(){
            requestid_list.push($(this).attr("data-host_requestid"))
            request_host_name_list.push($(this).parents("tr").find("td").eq(1).html())
            request_nick_name_list.push($(this).parents("tr").find("td").eq(2).html())
        })
        $.ajax({
            type:"POST",
            url:"/app/approval_accept/",
            data: {"username": username, "requestid_list": requestid_list, "request_host_name_list": request_host_name_list,
            "request_nick_name_list": request_nick_name_list},
            dataType:"json",
            success:function(data){
                console.log(data);
            },
            error:function(data){
                console.log('error');
            }
        });
//        location.href="/app/approval_accept?requestid_list=" + requestid_list +"&request_host_name_list=" +
//        request_host_name_list + "&request_nick_name_list=" + request_nick_name_list + "&username=" + username
    });

    $("#user_list").on("change", function(){
        username = $(this).val()
        $.ajax({
            type:"POST",
            url:"/app/get_host_request_by_username/",
            data: {"username": username},
            dataType:"json",
            success:function(data){
                console.log(data);
            },
            error:function(data){
                console.log('error');
            }
        });
    });
});