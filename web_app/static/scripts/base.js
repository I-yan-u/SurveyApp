$(document).ready(() => {

  let path = window.location.pathname;
  let page = path.split('/').pop();
  console.log("Document Title: " + page);

  if (page === 'login' || page === 'signup') {
    $('html').css('backgroundColor', '#5cdb95')
    $('.header').slideUp();
    $('.footer').fadeOut();
  }

  // nav dropdown
  $('.header #show').click(() => {
    $('.header').animate({'height': '220px'}, 1000);
    $('.header .nav').animate({opacity: '1'}, 1000);
    $('.header #show').css({ display: 'none' }).fadeOut('fast');
    $('.header #close').css({ display: 'block' }).fadeIn('slow');
    $('.header .nav').css({ display: 'flex' }).slideDown('slow');
  });

  $('.header #close').click(() => {
    $('.header #close').css({ display: 'none' }).fadeOut('fast');
    $('.header #show').css({display: 'block'}).fadeIn('slow');
    $('.header .nav').animate({opacity: '0'}, 1000);
    // $('.header .nav').css({ display: 'none' }).slideUp('slow');
    $('.header').animate({'height': '50px'}, 1000);
  });
  

  $('#search_survey_btn').click(() => {
    $('.response_search button').hide(100).show(1000);
    $('.response_search input').hide(100).show(1000);
    $('.response_search h2').animate({'opacity': '0'}, 500).text('Response');
    $('.response_search h2').animate({'opacity': '1'}, 500);
    $('.response_search').animate({'height': '60px'}, 1000);
    $('.response_search button').css({
      position: 'absolute', 
      right: '10px'}).animate({marginTop: '10px', width: '5vw'}, 500);
    $('.response_search input').css({position: 'absolute', right: '7vw'});

  })
});


// const placeActive = (children) => {
//   children.each(function() {
//       $(this).click(() => {
//           // Remove 'active' class from all children
//           children.removeClass('active');
          
//           // Add 'active' class to the clicked element
//           $(this).addClass('active');
//       });
//   });
// };