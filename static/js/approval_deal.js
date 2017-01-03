$(function(){
    $("#all").on("click", function(){
        $("table tr td").find("input").attr("checked","checked")
    });
    $("#all_not").on("click", function(){
        $("table tr td").find("input").removeAttr("checked")
    });

    $("#accept").on("click", function(){
        var request_user = $("#request_user").val()
        var requestid_list = ""
        $(".checkbox:checked").each(function(){
            requestid_list += $(this).attr("data-host_requestid") +","
        })
        location.href="/app/approval_accept?request_status=1" +"&request_user=" + request_user + "&requestid_list=" + requestid_list
    });

    $("#deny").on("click", function(){
        var request_user = $("#request_user").val()
        var requestid_list = []
        $(".checkbox:checked").each(function(){
            requestid_list += $(this).attr("data-host_requestid") +","
        })
        location.href="/app/approval_accept?request_status=2" +"&request_user=" + request_user + "&requestid_list=" + requestid_list
    });
});
