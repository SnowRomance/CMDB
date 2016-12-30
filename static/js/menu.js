$(function () {
    $(".menu > li").on('click', function () {
        $(this).find('ul').toggle("slow").end()
            .siblings('li').find('ul').slideUp();
    });
});