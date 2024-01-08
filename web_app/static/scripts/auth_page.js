$(document).ready(() => {

// Script file to handle login and signup pages
// login page
const invalid_tag_len = $('#invalid_tag').text().length
if(invalid_tag_len === 0) {
  console.log(invalid_tag_len);
} else {
  $('#login_email').css({'animation': 'shake-pos 0.5s ease', 'border-color': '#f32727'});
  $('#inPass').css({'animation': 'shake-pos 0.5s ease', 'border-color': '#f32727'});
  $('.confirmPass').css({'animation': 'shake-pos 0.5s ease', 'border-color': '#f32727'});
  $('.acPass').css({'animation': 'shake-pos 0.5s ease', 'border-color': '#f32727'});
}

  $('#login_email').on('focus', () => {
    $('#invalid_tag').slideUp(500);
    $('#login_email').css({'border-color': '#05396b'});
    $('#inPass').css({'border-color': '#fff'});
  });


  $('#inPass').on('focus', () => {    
    $('#invalid_tag').slideUp(500);
    $('#login_email').css({'border-color': '#fff'});
    $('#inPass').css({'border-color': '#05396b'});
  });

  $('.signup_body input').on('focus', () => {
    $('#invalid_tag').slideUp(500);
    $('.acPass').css({'border-color': '#fff'});
    $('.confirmPass').css({'border-color': '#fff'});
  });
});