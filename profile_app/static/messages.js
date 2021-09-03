//Hide Message List
$('.column').on('click', '.back', function(){
    $('.messages').hide();
})

//Display Message-List
$('.column').on('click', '.card', function(){
    $('.messages').show();
})

//display thread
$('.card').click(function(){
    let thread_id = $(this).attr('thread_id');
    $.ajax({
        url: "/profile/messages/" + thread_id,
        method: "GET",
        data: $(this).serialize(),
        success: function(response){
            $('.messages').html(response)
        }
    })
})

//send message from thread
$('.column').on('submit', '.msg-form', function(e){
    e.preventDefault();
    let profile_id = $(this).attr('profile_id');
    $.ajax({
        url: "/profile/" + profile_id + "/send_message",
        method: "POST",
        data: $(this).serialize(),
        success: function(response){
            $('.msg-container').html(response);
            $('.msg-form textarea').val(null)
        }
    })
})