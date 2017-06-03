/**
 * Created by shangmingyang on 5/20/17.
 */
$(document).ready(function(){
   $("#buy").click(buy);
    $("#pre_page").click(prepage);
    $("#next_page").click(nextpage);
    

});

function buy(){
    if($('#buy').text() == 'Buy'){
        $.ajax({
            url: '/buy/book/'+$("#book_id").text(),
            type: 'POST',
            dataType: 'text',
            data: "",
            success: function (data) {
                data = $.parseJSON(data);
                if (data.result == -1) {
                    alert(data.error);
                } else if (data.result == 1) {
                    alert(data.msg);
                    $("#buy").text('Buyed');
                }
            },
            error: function (request) {
                alert(request.error);
            }
        });

    }
}

function prepage(){
    var currUrl = new Url(location.href);
    var p = currUrl.query.page;
    var next_page = 1;
    if(p == undefined){
        next_page = 1;
    }else{
        next_page = parseInt(p) - 1;
    }
    if(next_page<=0){
        next_page=1;
    }
    gotoPage(next_page);
}
function nextpage(){
    var currUrl = new Url(location.href);
    var p = currUrl.query.page;
    var next_page = 2;
    if(p == undefined){
        next_page = 2;
    }else{
        next_page = parseInt(p) + 1;
    }
    gotoPage(next_page);
}
function gotoPage(page){
    var currUrl = new Url(location.href);
    currUrl.query.page = page.toString();
    window.location.href = currUrl.toString();
}