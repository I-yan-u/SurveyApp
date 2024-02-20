// import { token } from './auth.js'
// let token = localStorage.getItem('token');
// token = JSON.parse(token);

$(document).ready(() => {
  $('#invalid_tag').slideUp(500);

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


  $('.acPass').on('focusin', () => {
    $('#show_hide1').animate({opacity: '1'}, 300);
  });
  $('.acPass').on('focusout', () => {
    $('#show_hide1').animate({opacity: '0'}, 300);
  });

  $('.confirmPass').on('focusin', () => {
    $('#show_hide2').animate({opacity: '1'}, 300);
  });
  $('.confirmPass').on('focusout', () => {
    $('#show_hide2').animate({opacity: '0'}, 300);
  });

  $('#inPass').on('focusin', () => {
    $('#show_hideL').animate({opacity: '1'}, 300);
  });
  $('#inPass').on('focusout', () => {
    $('#show_hideL').animate({opacity: '0'}, 300);
  });

// Login
  $('#show_hideL').on('click', () => {
    $('#inPass').attr('type', 'text');
    $('#show_hideL').animate({opacity: '0'}, 300).css({display: 'none'});
    $('#hide_showL').css({display: 'block'}).animate({opacity: '1'}, 300);
  });

  $('#hide_showL').on('click', () => {
    $('#inPass').attr('type', 'password');
    $('#hide_showL').animate({opacity: '0'}, 300).css({display: 'none'});
    $('#show_hideL').css({display: 'block'}).animate({opacity: '1'}, 300);
  });

  // Actual password
  $('#show_hide1').on('click', () => {
    $('.acPass').attr('type', 'text');
    $('#show_hide1').animate({opacity: '0'}, 300).css({display: 'none'});
    $('#hide_show1').css({display: 'block'}).animate({opacity: '1'}, 300);
  });

  $('#hide_show1').on('click', () => {
    $('.acPass').attr('type', 'password');
    $('#hide_show1').animate({opacity: '0'}, 300).css({display: 'none'});
    $('#show_hide1').css({display: 'block'}).animate({opacity: '1'}, 300);
  });

  // Confirm password
  $('#show_hide2').on('click', () => {
    $('.confirmPass').attr('type', 'text');
    $('#show_hide2').animate({opacity: '0'}, 300).css({display: 'none'});
    $('#hide_show2').css({display: 'block'}).animate({opacity: '1'}, 300);
  });

  $('#hide_show2').on('click', () => {
    $('.confirmPass').attr('type', 'password');
    $('#hide_show2').animate({opacity: '0'}, 300).css({display: 'none'});
    $('#show_hide2').css({display: 'block'}).animate({opacity: '1'}, 300);
  });
});