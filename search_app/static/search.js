$('.column').on('click', 'li', (function(){
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