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


});