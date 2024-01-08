$(document).ready(() => {
  let top = $('.top');
  $('#view-more').click(() => {
    $('html, body').animate({
      scrollTop: $(".thank_you_content").offset().top
    }, 1000);
    $("#create-survey").focus();
  });

});