$(function(){
    KindEditor.ready(function(K){
        window.editor = K.create("#content", {
            width: '90%',
            height: '500px',
        });
    });
});