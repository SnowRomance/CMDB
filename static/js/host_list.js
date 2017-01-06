$(function(){
    $(".btn").on('click', function(){
        $.ajax({
            type:"POST",
            url:"/app/sync_host/",
            dataType:"json",
            success:function(data){
                $(".table-default").html()
                _add_html = "<tr><th>集群名称</th><th>主机组</th><th>主机名称</th><th>公网IP</th><th>私网IP</th><th>操作</th></tr>"

                for (var key in data) {
                    _add_html = _add_html + "<tr><td>"+data[key]['idc_name']+"</td>"
                    +"<td>"+data[key]['group_name']+"</td><td><span class=\"glyphicon glyphicon-wrench\" data-hostid=\""+data[key]['id']+"\"></span>&nbsp;<label>"+data[key]['hostname']+"</label></td>"
                    +"<td><span class=\"glyphicon glyphicon-wrench\" data-hostid=\""+data[key]['id']+"\"></span>&nbsp;<label>"+data[key]['ip']+"</label></td>"
                    +"<td><span class=\"glyphicon glyphicon-wrench\" data-hostid=\""+data[key]['id']+"\"></span>&nbsp;<label>"+data[key]['inner_ip']+"</label></td>"
                    +"<td><span class=\"glyphicon glyphicon-remove\"></span></td></tr>"
                }
                $(".table-default").html(_add_html)
            },
            error:function(data){
                console.log('error');
            }
        });
    });

    // nickname_modify
    $('.nickname').click(function(){
        var _this = $(this);
        if(_this.hasClass("disabled")){
        } else {
            _this.addClass("disabled");
            var _parentTd = _this.parent('td');
            var _val = _parentTd.find("label").html() || '';
            var _inputHtml = '<input type="text" value = "'+_val+'" id="nickname"/>'
            _parentTd.find("label").html(_inputHtml);
        }
    });
    $(".table-default").on('keyup','#nickname',function(event){
        var _this = $(this);
        var _parentTd = _this.parents('td');
        var host_id = _parentTd.find("span").attr("data-hostid");
        var _nickname = _this.val();
        if(event.keyCode == 13) {
            $.ajax({
                type:"POST",
                url:"/app/modify_host_nickname/",
                dataType:"json",
                data:{"host_id":host_id,"nickname":_nickname},
                success:function(data){
                    _parentTd.find("label").html(_remark);
                    $('.nickname').removeClass("disabled");
                },
                error:function(data){
                    console.log('error');
                }
            });
        }
    });

    // ip_modify
    $('.ip').click(function(){
        var _this = $(this);
        if(_this.hasClass("disabled")){
        } else {
            _this.addClass("disabled");
            var _parentTd = _this.parent('td');
            var _val = _parentTd.find("label").html() || '';
            var _inputHtml = '<input type="text" value = "'+_val+'" id="ip"/>'
            _parentTd.find("label").html(_inputHtml);
        }
    });
    $(".table-default").on('keyup','#ip',function(event){
        var _this = $(this);
        var _parentTd = _this.parents('td');
        var host_id = _parentTd.find("span").attr("data-hostid");
        var _ip = _this.val();
        if(event.keyCode == 13) {
            $.ajax({
                type:"POST",
                url:"/app/modify_host_ip/",
                dataType:"json",
                data:{"host_id":host_id,"ip":_ip},
                success:function(data){
                    _parentTd.find("label").html(_remark);
                    $('.ip').removeClass("disabled");
                },
                error:function(data){
                    console.log('error');
                }
            });
        }
    });

    // inner_ip_modify
    $('.inner_ip').click(function(){
        var _this = $(this);
        if(_this.hasClass("disabled")){
        } else {
            _this.addClass("disabled");
            var _parentTd = _this.parent('td');
            var _val = _parentTd.find("label").html() || '';
            var _inputHtml = '<input type="text" value = "'+_val+'" id="inner_ip"/>'
            _parentTd.find("label").html(_inputHtml);
        }
    });
    $(".table-default").on('keyup','#inner_ip',function(event){
        var _this = $(this);
        var _parentTd = _this.parents('td');
        var host_id = _parentTd.find("span").attr("data-hostid");
        var _inner_ip = _this.val();
        if(event.keyCode == 13) {
            $.ajax({
                type:"POST",
                url:"/app/modify_host_inner_ip/",
                dataType:"json",
                data:{"host_id":host_id,"inner_ip":_inner_ip},
                success:function(data){
                    _parentTd.find("label").html(_remark);
                    $('.inner_ip').removeClass("disabled");
                },
                error:function(data){
                    console.log('error');
                }
            });
        }
    });
});