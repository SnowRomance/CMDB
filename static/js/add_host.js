$(function(){
    $('.dark-matter .button').click(function(){
        var _this = $(this);
        _parentTd = _this.parents("div");
        alert(_parentTd.find("select#idc").attr("data-saltip"));

        _parentTd.find("select#group").val();
        _parentTd.find(".hd_text").show();
    });
});