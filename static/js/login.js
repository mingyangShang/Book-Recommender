/**
 * Created by shangmingyang on 5/21/17.
 */
$(document).ready(function(){
   $("#signup_link").click(switchToSignup);
   $("#signin_link").click(switchToSignin);
   $("#signup_div .sign-button.submit").click(signup);
   $("#signin_div .sign-button.submit").click(signin);
});

function switchToSignup(){
    $("#signup_link").addClass('active');
    $("#signin_link").removeClass('active');
    $("#signup_div").css('display', 'block');
    $('#signin_div').css('display' ,'none');
    $('.index-tab-navs .navs-slider .navs-slider-bar').css('left', '0');
}

function switchToSignin(){
    $("#signin_link").addClass('active');
    $("#signup_link").removeClass('active');
    $("#signin_div").css('display', 'block');
    $('#signup_div').css('display', 'none');
    $('.index-tab-navs .navs-slider .navs-slider-bar').css('left', '4em');
}

function signup() {
    $('#signup-form').submit(function (e) {
        e.preventDefault();
        $.ajax({
            url: '/register/',
            type: 'POST',
            dataType: 'text',
            data: $("#signup-form").serialize(),
            success: function (data) {
                data = $.parseJSON(data);
                if (data.result == -1) {
                    alert(data.error);
                } else if (data.result == 1) {
                    alert(data.msg);
                    //to login
                    switchToSignin();
                    $('#signin-form input[name="account"]').val(data.content.username);
                    $('#signin-form input[name="password"]').val('');
                }
            },
            error: function (request) {
                alert('error');
                alert(request.error);
            }
        });
    });
}

function signin() {
    $("#signin-form").submit(function (e){
        e.preventDefault();
        $.ajax({
            url: '/register/',
            type: 'POST',
            dataType: 'text',
            data: $("#signin-form").serialize(),
            success: function (data) {
                data = $.parseJSON(data);
                if (data.result == -1) {
                    alert(data.error);
                } else if (data.result == 1) {
                    alert(data.msg);
                    $.cookie('logined', true, {expires: 7, path: '/'});
                    $.cookie('user', data.content.username, {expires: 7, path: '/'});
                    window.location.replace('/');
                }
            },
            error: function (request) {
                alert(request.error);
            }
        });
    });
}