$(function(){
    $(".btn").on('click', function(){
        $.ajax({
            type:"POST",
            url:"/app/sync_host/",
            dataType:"json",
            success:function(data){
                $(".hovertable").html()
                _add_html = "<tr><th>集群名称</th><th>主机组</th><th>主机名称</th><th>公网IP</th><th>私网IP</th><th>操作</th></tr>"

                for (var key in data) {
                    _add_html = _add_html + "<tr onmouseover=\"this.style.backgroundColor='#ffff66';\" onmouseout=\"this.style.backgroundColor='#d4e3e5';\"><td>"+data[key]['idc_name']+"</td>"
                    +"<td>"+data[key]['group_name']+"</td><td><span class=\"glyphicon glyphicon-wrench\" data-hostid=\""+data[key]['id']+"\"></span>&nbsp;<label>"+data[key]['hostname']+"</label></td>"
                    +"<td><span class=\"glyphicon glyphicon-wrench\" data-hostid=\""+data[key]['id']+"\"></span>&nbsp;<label>"+data[key]['ip']+"</label></td>"
                    +"<td><span class=\"glyphicon glyphicon-wrench\" data-hostid=\""+data[key]['id']+"\"></span>&nbsp;<label>"+data[key]['inner_ip']+"</label></td>"
                    +"<td><span class=\"glyphicon glyphicon-remove\"></span></td></tr>"
                }
                $(".hovertable").html(_add_html)
            },
            error:function(data){
                console.log('error');
            }
        });
    });
});