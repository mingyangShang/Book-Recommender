/**
 * Created by shangmingyang on 5/21/17.
 */
$(document).ready(function(){
   $("#signup_link").click(switchToSignup);
   $("#signin_link").click(switchToSignin);
});

function switchToSignup(){
    $("#signup_link").addClass('active');
    $("#signin_link").removeClass('active');
    $("#signup_div").css('display', 'block');
    $('#signin_div').css('display' ,'none');
    $('.index-tab-navs .navs-slider .navs-slider-bar').css('left', '0')
}

function switchToSignin(){
    $("#signin_link").addClass('active');
    $("#signup_link").removeClass('active');
    $("#signin_div").css('display', 'block');
    $('#signup_div').css('display', 'none');
    $('.index-tab-navs .navs-slider .navs-slider-bar').css('left', '4em')
}