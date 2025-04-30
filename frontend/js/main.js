$(document).ready(function() {
  // Smooth scrolling per i link di navigazione
  $('a.page-scroll').click(function(e) {
    e.preventDefault();
    var target = $(this).attr('href');
    var offset = $(target).offset().top;
    $('html, body').animate({ scrollTop: offset - 40 }, 900);
  });
  $(window).scroll(function() {
    if ($(this).scrollTop() > 100) {
      $('#site-nav').addClass('scrolled');
    } else {
      $('#site-nav').removeClass('scrolled');
    }
  });

  // Inizializzazione della lightbox 
  if ($.fn.nivoLightbox) {
    $('.gallery-item a').nivoLightbox({ effect: 'fade' });
  }
});
