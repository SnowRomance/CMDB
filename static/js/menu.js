$(function () {
    $(".menu > li").on('click', function () {
        $(this).find('ul').slideDown().end()
            .siblings('li').find('ul').slideUp();
    });
});