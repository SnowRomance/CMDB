$(function(){
    $("#all").on("click", function(){
        $("table tr td").find("input").attr("checked","checked")
    });
    $("#all_not").on("click", function(){
        $("table tr td").find("input").removeAttr("checked")
    });

    //request_user 删选
    $("#request_user").on("change", function(){
        var _user = $(this).val()
        $.ajax({
            type:"POST",
            url:"/approval/get_approval_accept_page_by_username/",
            data: {"username": _user},
            dataType:"json",
            success:function(data){
                $(".table-default").html()
                _add_html = "<tr><th>用户名</th><th>主机名称</th><th>申请天数</th><th>状态</th><th>开始时间</th><th>操作</th></tr>"

                for (var key in data) {
                    _add_html = _add_html + "<tr><td>"+data[key]['username']+"</td>"
                    +"<td>"+data[key]['hostname']+"</td><td>"+data[key]['lease_time']+"</td>"
                    +"<td>"+data[key]['status']+"</td>"
                    +"<td>"+data[key]['create_time']+"</td>"
                    +"<td><input type=\"checkbox\" data-host_requestid=\""+data[key]['id']+"\" class=\"checkbox\"/></td>"
                    +"</tr>"
                }
                $(".table-default").html(_add_html)
            },
            error:function(data){
                console.log('error');
            }
        });
    });

    $("#accept").on("click", function(){
        var request_user = $("#request_user").val()
        var requestid_list = ""
        $(".checkbox:checked").each(function(){
            requestid_list += $(this).attr("data-host_requestid") +","
        })
        location.href="/approval/approval_accept?request_status=1" +"&request_user=" + request_user + "&requestid_list=" + requestid_list
    });

    $("#deny").on("click", function(){
        var request_user = $("#request_user").val()
        var requestid_list = []
        $(".checkbox:checked").each(function(){
            requestid_list += $(this).attr("data-host_requestid") +","
        })
        location.href="/approval/approval_accept?request_status=2" +"&request_user=" + request_user + "&requestid_list=" + requestid_list
    });
});
