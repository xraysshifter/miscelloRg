$(document).ready(function(){
    wimg = $(".img_container").width();
    console.log(wimg);
    $(".img_container").css("height",wimg);
    
    $(window).resize(function(){
       wimg = $(".img_container").width();
       console.log(wimg);
       $(".img_container").css("height",wimg);
    })


    $('#gal .img_container img').click(function(){
    //        $(" #gal .img_container").removeClass("fullImg");
            $(this).parent().toggleClass("fullImg");
    });

})



