//filter search results by all, people, or pokemon
$('.column').on('click', '.filters li', (function(){
    let query = $('query').attr('query');
    let filter = $(this).attr('name');
    if (filter == "people") {
        $.ajax({
            url: "/search/" + query + "/people",
            method: "GET",
            data: $(this).serialize(),
            success: function(response){
                console.log(response)
                $('.column').html(response)
            }
        })
        // $('.pokemon').hide()
        // $('.people').show()
    } 
    else if ( filter == "pokemon" ) {
        $('.pokemon').show()
        $('.people').hide()
    } else {
        $('.people').show()
        $('.pokemon').show()
    }
})
)
//switch active filter style
$('.filters li').click(function(){
    $('.filters li').removeClass('current');
    $(this).addClass('current');
})