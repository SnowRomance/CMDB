$(function(){
    $('.glyphicon-wrench').click(function(){
        var _this = $(this);
        if(_this.hasClass("disabled")){
        } else {
            _this.addClass("disabled");
            var _parentTd = _this.parent('td');
            var _val = _parentTd.find("label").html() || '';
            var _inputHtml = '<input type="text" value = "'+_val+'" id="remark"/>'
            _parentTd.find("label").html(_inputHtml);
        }
    });
    $(".hovertable").on('keyup','#remark',function(event){
        var _this = $(this);
        var _parentTd = _this.parents('td');
        var group_id = _parentTd.find("span").attr("data-groupid");
        var _remark = _this.val();
        if(event.keyCode == 13) {
            $.ajax({
                type:"POST",
                url:"/app/modify_group_remark/",
                dataType:"json",
                data:{"group_id":group_id,"remark":_remark},
                success:function(data){
                    _parentTd.find("label").html(_remark);
                    $('.glyphicon-wrench').removeClass("disabled");
                },
                error:function(data){
                    console.log('error');
                }
            });
        }

    });
});