$(function(){
    $('.glyphicon-wrench').click(function(){
        var _this = $(this);
        if(_this.hasClass("disabled")){
        } else {
            _this.addClass("disabled");
            var _parentTd = _this.parent('td');
            var _val = _parentTd.find("label").html() || '';
            var _inputHtml = '<input type="text" value = "'+_val+'" id="permissions"/>'
            _parentTd.find("label").html(_inputHtml);
        }
    });
    $(".hovertable").on('keyup','#permissions',function(event){
        var _this = $(this);
        var _parentTd = _this.parents('td');
        var user_id = _parentTd.find("span").attr("data-userid");
        var _permissions = _this.val();
        if(event.keyCode == 13) {
            $.ajax({
                type:"POST",
                url:"/app/modify_user_permissions/",
                dataType:"json",
                data:{"user_id":user_id,"permissions":_permissions},
                success:function(data){
                    _parentTd.find("label").html(_permissions);
                    $('.glyphicon-wrench').removeClass("disabled");
                },
                error:function(data){
                    console.log('error');
                }
            });
        }

    });
});