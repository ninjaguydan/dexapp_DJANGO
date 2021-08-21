//filter search results by all, people, or pokemon
$('.column').on('click', '.filters li', (function(){
    let query = $('query').attr('query');
    let filter = $(this).attr('name')
    $.ajax({
        url: "/search/" + query + "/" + filter,
        method: "GET",
        data: $(this).serialize(),
        success: function(response) {
            console.log(response)
            $('.results').html(response)
        }
    })
})
)
//switch active filter style
$('.filters li').click(function(){
    $('.filters li').removeClass('current');
    $(this).addClass('current');
})