//Hide Message List
$('.back').click(function(){
    $('.messages').hide();
})

//Display Message-List
$('.column').on('click', '.card', function(){
    $('.messages').show();
})