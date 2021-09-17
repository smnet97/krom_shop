var $item = $('.carousel-item');
var $wHeight = $(window).height();
$item.eq(0).addClass('active');
$item.height($wHeight);



$(window).on('resize', function (){
  $wHeight = $(window).height();
  $item.height($wHeight);
});

$('.carousel').carousel({
  interval: 6000,
  pause: "false"
});



  $('.likes').on( 'click', function() {
    $(this).children('.like').toggleClass('d-none')
  });

  $('.carts').on( 'click', function() {
    $(this).children('.aaa .cartt').addClass('d-none')
    $(this).children('.aaa .carttt').removeClass('d-none')
  });






