$(function(){
    $(".email-list ul li").on("click", function(){
        var _this = $(this);
        var _from_user = _this.find(".from_user").html();
        var _to_user = _this.find(".to_user").html();
        var _title = _this.find(".title").html();
        var _content = _this.find(".content").html();
        var _create_time = _this.find(".create_time").html();

        $(".email_title").html(_title);
        $(".email_head").show();
        $(".email_head .from_user").html(_from_user);
        $(".email_head .to_user").html(_to_user);
        $(".email_head .create_time").html(_create_time);
        $(".email_content").html(_content);
        $(".email_from_user").html(_from_user);
    });
});