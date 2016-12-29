$(function(){
    $(".idc").on("change", function(){
        idc_name = $(".idc").val()
        $.ajax({
            type:"POST",
            url:"/app/change_idc/",
            data: {"idc_name": idc_name},
            dataType:"json",
            success:function(data){
                $(".group").html()
                _add_html = ""
                for (var key in data["group_list_dict"]) {
                    _add_html = _add_html + "<option>" +data["group_list_dict"][key]["group_name"]+ "</option>"
                }
                $(".group").html(_add_html)

                $(".host").html()
                _add_html = ""
                for (var key in data["host_list_dict"]) {
                    _add_html = _add_html + "<option data-hostname=\""+ data["host_list_dict"][key]["hostname"] +"\">" +data["host_list_dict"][key]["nick_name"]+ "</option>"
                }
                $(".host").html(_add_html)
            },
            error:function(data){
                console.log('error');
            }
        });
    });
    $(".group").on("change", function(){
        group_name = $(".group").val()
        $.ajax({
            type:"POST",
            url:"/app/change_group/",
            data: {"group_name": group_name},
            dataType:"json",
            success:function(data){
                $(".host").html()
                _add_html = ""
                for (var key in data) {
                    _add_html = _add_html + "<option data-hostname=\""+ data[key]["id"] +"\">" +data[key]["nick_name"]+ "</option>"
                }
                $(".host").html(_add_html)
            },
            error:function(data){
                console.log('error');
            }
        });
    });

    // 删选
    $('.hostlist_box_left,.hostlist_box_right').on('click', 'span', function(){
        _this = $(this)
        if(_this.attr("data-select") == undefined){
            _this.css("background-color", "#00FFFF")
            _this.attr("data-select", "selected")
        }else {
            _this.css("background-color", "white")
            _this.removeAttr("data-select")
        }
    });
    $('#add').on('click', function(){
        $('.nick-name').each(function(){
            if($(this).attr("data-select") != undefined){
                var _span = $(this).clone();
                $('.hostlist_box_right').append(_span).find("span").css("background-color", "white").removeAttr("data-select");
                $(this).remove();
            }
        });
    });
    $('#remove').on('click', function(){
         $('.nick-name').each(function(){
            if($(this).attr("data-select") != undefined){
                var _span = $(this).clone();
                $('.hostlist_box_left').append(_span).find("span").css("background-color", "white").removeAttr("data-select");
                $(this).remove();
            }
        });
    });

    // hostlist_box_right request
    $(".btn").on("click", function(){
        var hostname_list = ""
        $(".hostlist_box_right span").each(function(){
            hostname_list = hostname_list + $(this).attr("data-hostname") + ","
        });
//        $.ajax({
//            type:"POST",
//            url:"/app/approval_request/",
//            data: {"hostname_list": hostname_list},
//            dataType:"json",
//            success:function(data){
//                console.log('success');
//            },
//            error:function(data){
//                console.log('error');
//            }
//        });
        console.log(hostname_list)
        location.href = "/app/approval_request/?hostname_list=" + hostname_list
    });
});