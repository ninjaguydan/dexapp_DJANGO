const menuBtn = document.querySelector('.menu-btn');
// ..hamburger to "x" animation
let menuOpen = false;
menuBtn.addEventListener('click', () => {
    menuBtn.classList.toggle('open');
});

// ..hamburger Function
function openMenu() {
    let nav = document.querySelector('.mobile-nav-slider');
    if (nav.style.display === "block") {
        nav.style.display = "none";
    } else {
        nav.style.display = "block";
    }
}
//textarea counter
$('.column').on('keyup', 'form', function(){
    let limit = 255;
    let input = $(this).find('textarea').val();
    limit -= input.length;
    $(this).find('small.counter').html(limit + '/255');
    if ( limit < 100 ) {
        $(this).find('small.counter').addClass('warning')
    } else {
        $(this).find('small.counter').removeClass('warning')
    }
})
// disable buttons if form inputs contain only white space 
$('.column').on('keyup', 'form', function(){
    let str = $(this).find('textarea').val().replace(/\s/g, '').length;
    if (!str || str > 255) {
        $(this).find('button').prop("disabled", true)
    } else {
        $(this).find('button').prop("disabled", false)
    }
})
//------------------------------ Navigation Functions ------------------------------//
//check if a user is logged in and reduce width if true
const loggedIn = $('forjs').attr('logged-in');
if (loggedIn == "True") {
    $('.main-nav').css("width", "325px");
} 
if (loggedIn == "False") {
    $('#menu-btn').hide()
}

//display main nav dropdown menu
$('.main-nav span').click(function(){
    console.log("what?");
    $('.dropdown-menu').toggle();
    $('.main-nav span').toggleClass('active');
})

//Close dropdown menu when clicking anywhere outside of it
function closeDropdown() {
    $('.dropdown-menu').hide();
    $('.main-nav span').removeClass('active');
}
$(document.body).click(function(e){
    closeDropdown();
})
$('.main-nav span').click(function(e) {
    e.stopPropagation();
})

//------------------------------ Search Icon Function ------------------------------ //
$('.search-icon').click(function(){
    $('.search-form').toggleClass("hidden");
})

//------------------------------ Reply Form Functions ------------------------------//
// display review reply form
$(document).on('click', '.reply', function(){
    let review_id = $(this).attr('review_id');
    $(".comment_" + review_id).toggle();
})
// display post reply form
$(document).on('click', '.reply', function(){
    let post_id = $(this).attr('post_id');
    $(".comment_" + post_id).toggle();
})

//------------------------------ Profile Modal Functions ------------------------------//
//display "edit Profile" modal
$('#edit-profile').click(function(){
    $('.modal-bg').css("display", "block");
})
//close "Edit Profile" modal
$('#close').click(function(){
    $('.modal-bg').css("display", "none");
    $('.new-team').css("display", "none");
    $('#create-team').css("display", "flex");
})
// select profile image
$('.img-container img').click(function(){
    $('.img-container img').css("outline", "none");
    $(this).css("outline", "5px solid #86b7fe");
    let image = $(this).attr('id');
    $('#img').val(image);
})
//select profile color
$('.img-container span').click(function(){
    $('.img-container span').css("outline", "none");
    $(this).css("outline", "5px solid #86b7fe");
    let color = $(this).attr('color');
    $('#color').val(color);
})
//validate update fields
$('.modal-bg').on('keyup', '.form-group', function(){
    let fieldInput = $(this).find('input').val()
    if ( fieldInput.length < 2 ) {
        $(this).children('.error').show();
    } else {
        $(this).children('.error').hide();
    }
})

//------------------------------ Profile Functions ------------------------------//
//profile tabs
$( function() {
    $( "#tabs" ).tabs();
})
//Switch active tabs
$('.tab-nav li a').click(function(){
    $('.tab-nav li a').removeClass('active');
    $(this).addClass('active');
})
//post AJAX
$('.column').on('submit', '#post-form', function(e){
    e.preventDefault()
    let userid = $(this).attr('userid')
    $.ajax({
        url: "/profile/" + userid + "/create_post",
        method: "POST",
        data: $(this).serialize(),
        success: function(response){
            $('#post-form small.counter').html('255/255');
            $('#post-form button').prop("disabled", true);
            $('.post-list').html(response);
            $('#post-form textarea').val(null);
        }
    })
})
//like post AJAX
$('.column').on('submit', '.like-post-form', function(e){
    e.preventDefault()
    let post_id = $(this).attr('post_id')
    $.ajax({
        url: "/profile/like_post",
        method: "POST",
        data: $(this).serialize(),
        success: function(response){
            $('.p' + post_id).html(response)
        }
    })
})
//post comment AJAX
$('.column').on('submit','.post_comment_form', function(e){
    e.preventDefault()
    let post_id = $(this).attr('post_id')
    $.ajax({
        url: "/profile/"+ post_id +"/comment_post",
        method: "POST",
        data: $(this).serialize(),
        success: function(response){
            $('.comment.comment_' + post_id).html(response)
            $('.post_comment_form textarea').val(null)
        }
    })
})
//like post comment AJAX
$('.column').on('submit', '.like-post-comment-form', function(e){
    e.preventDefault()
    let comment_id = $(this).attr('comment_id');
    $.ajax({
        url: "/profile/like_post_comment",
        method: "POST",
        data: $(this).serialize(),
        success: function(response){
            $('.c' + comment_id).html(response)
        }
    })
})
//like team AJAX
$('.column').on('submit','.like-team-form', function(e){
    e.preventDefault()
    let team_id = $(this).attr('team_id')
    $.ajax({
        url: "/like_team",
        method: "POST",
        data: $(this).serialize(),
        success: function(response){
            $('.t'+ team_id).html(response)
        }
    })
})
//------------------------------ Pokemon Functions ------------------------------//
// display "Add to Team" modal
$('#add-to-team').click(function(){
    $('.modal-bg').css("display", "block")
})
// display 'Create Team' form
$('#create-team').click(function(){
    $('#create-team').css("display", "none");
    $('.new-team').css("display", "block");
})
//popup notification AJAX
$('.edit-profile-modal').on('submit', '#add-to-team', function(e){
    e.preventDefault();
    let pkmn_id = $('tojs').attr('pkmn_id');
    $.ajax({
        url: pkmn_id + "/add_to_team",
        method: "POST",
        data: $(this).serialize(),
        success: function(response){
            $('.popup-container').append(response)
            $('.modal-bg').css("display", "none");
        }
    })
    setTimeout(function(){
        $('.popup-container').fadeOut()
    }, 5000);
})
//review AJAX
$('.column.posts').on('submit', '#review-form', function(e){
    e.preventDefault();
    let pkmn_id = $('tojs').attr('pkmn_id');
    $.ajax({
        url: pkmn_id + "/create_review",
        method: "POST",
        data: $(this).serialize(),
        success: function(response){
            $('.review-list').html(response)
            $('#review-form textarea').val(null)
            $('#review-form small.counter').html('255/255');
            $('#review-form button').prop("disabled", true);
            allRatings()
        }
    })
})
//like review AJAX
$('.column').on('submit', '#like_form', function(e){
    let review_id = $(this).attr('review_id')
    e.preventDefault();
    $.ajax({
        url: "/like_review",
        method: "POST",
        data: $(this).serialize(),
        success: function(response){
            $('.r'+review_id).children('.card-item-icons.r').html(response)
        }
    })
})
//review comment AJAX
$('.column').on('submit', '.comment_form', function(e){
    e.preventDefault();
    let review_id = $(this).attr('review_id')
    $.ajax({
        url: "/" + review_id + "/comment_review",
        method: "POST",
        data: $(this).serialize(),
        success: function(response){
            $('.comment.comment_'+ review_id).html(response)
            $('.comment-form textarea').val(null)
        }
    })
})
//like review comment AJAX
$('.column').on('submit', '.like_form', function(e){
    e.preventDefault()
    let comment_id = $(this).attr('comment_id');
    $.ajax({
        url: "/like_review_comment",
        method: "POST",
        data: $(this).serialize(),
        success: function(response){
            $('.c'+comment_id).children('.card-item-icons.c').html(response)
        }
    })
})

//Display Star Rating
function displayRating(num){
    var result = "";
    for (var i = 1; i < 11; i++) {
        if (i <= num) {
            result = result + "&#x2605"
        } else {
            result = result  + "&#x2606";
        }
    }
    return result
}
function allRatings() {
    $('.n1').html(displayRating(1));
    $('.n2').html(displayRating(2));
    $('.n3').html(displayRating(3));
    $('.n4').html(displayRating(4));
    $('.n5').html(displayRating(5));
    $('.n6').html(displayRating(6));
    $('.n7').html(displayRating(7));
    $('.n8').html(displayRating(8));
    $('.n9').html(displayRating(9));
    $('.n10').html(displayRating(10));
}
allRatings()

//------------------------------ Team Functions ------------------------------//
//toggle Team stats
$('#toggle-stats').click(function(){
    $('.list-group-item.striped').toggle()
})
//Toggle Team Weakness
$('#toggle-weakness').click(function(){
    $('.chart-container').toggle()
})
//Toggle Team Updates
$('.update-toggle p').click(function(){
    $('.update').toggle()
})
//team comment AJAX
$('.column').on('submit', '.team_comment_form', function(e){
    e.preventDefault()
    let team_id = $(this).attr('team_id')
    $.ajax({
        url: "/" + team_id + "/comment_team",
        method: "POST",
        data: $(this).serialize(),
        success: function(response){
            $('.comment_'+ team_id).html(response)
            $('.team_comment_form textarea').val(null)
            $('.team_comment_form small.counter').html('255/255');
            $('.team_comment_form button').prop("disabled", true);
        }
    })
})
//like team comment AJAX
$('.column').on('submit','.like_team_comment_form', function(e){
    e.preventDefault()
    let comment_id = $(this).attr('comment_id')
    $.ajax({
        url: "/like_team_comment",
        method: "POST",
        data: $(this).serialize(),
        success: function(response){
            $('.c'+comment_id).html(response)
        }
    })
})

//------------------------------ Team Modal Functions ------------------------------//
//display "Edit Team" modal
$('.edit-team').click(function(){
    $('.modal-bg').css("display", "block")
})