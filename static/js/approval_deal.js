$(function(){
    $("#all").on("click", function(){
        $("table tr td").find("input").attr("checked","checked")
    });
    $("#all_not").on("click", function(){
        $("table tr td").find("input").removeAttr("checked")
    });

    $("#accept").on("click", function(){
        var requestid_list = []
        $(".checkbox:checked").each(function(){
            requestid_list.push($(this).attr("data-host_requestid"))
        })
        location.href="/app/approval_accept?requestid_list=" + requestid_list
    });
});