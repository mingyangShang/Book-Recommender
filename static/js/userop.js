/**
 * Created by shangmingyang on 5/20/17.
 */
$(document).ready(function(){
   $("#buy").click(buy)
});

function buy(){
    // if($('#buy').text() == 'Buy'){
    //     $("#buy").click(function(){
    //         alert('Buy succeed!')
    //         $("#buy").text('Buyed');
    //     })
    // }else{
    //     $("#buy").
    // }
    if($('#buy').text() == 'Buy'){
        alert('Buy succeed!')
        $("#buy").text('Buyed')
    }
}