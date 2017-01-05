$(function(){
    $('.dark-matter .button').click(function(){
        var _this = $(this);
        _parentTd = _this.parents("div");
        _salt_api = _parentTd.find("select").eq(0).find("option:selected").attr("data-saltip")
        _salt_name = _parentTd.find("select").eq(0).find("option:selected").val()
        _group_name = _parentTd.find("select").eq(1).find("option:selected").val()
        _yum_command = "touch /tmp/cmdb.txt;echo 'idc="+ _salt_name +"' >> /tmp/cmdb.txt;echo 'group="+ _group_name +"' >> /tmp/cmdb.txt;yum install epel-release -y;yum install salt-minion -y;sed -i 's/#master: salt/master: "+ _salt_api +"/g' /etc/salt/minion;service salt-minion start;"

        $(".hd_text").find("span B").eq(1).html(_salt_api)
        $(".hd_text").find("span B").eq(2).html(_group_name)
        $(".hd_text .text").html(_yum_command)

        _parentTd.find("select#group").val();
        _parentTd.find(".hd_text").show();
    });

//    $("body").on("click", function(){
//        if $(".hd_text").hasClass("display: block") {
//            $(".hd_text").css("display", "none")
//        }
//    });
});