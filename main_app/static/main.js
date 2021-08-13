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
//---------- Navigation Functions ----------//
//check if a user is logged in and reduce width if true
let loggedIn = $('forjs').attr('logged-in');
if (loggedIn == "True") {
    $('.main-nav').css("width", "300px");
}

//display main nav dropdown menu
$('.main-nav span').click(function(){
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

//---------- Search Icon Function ---------- //
$('.search-icon').click(function(){
    $('.search-form').toggleClass("hidden");
})

//---------- Reply Form Functions ----------//
// display team reply form
$(document).on('click', '.reply', function(){
    let team_id = $(this).attr('team_id');
    $(".comment_" + team_id).toggle();
})
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

//---------- Profile Modal Functions ----------//
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

//---------- Profile Functions ----------//
//profile tabs
$( function() {
    $( "#tabs" ).tabs();
})
//Switch active tabs
$('.tab-nav li a').click(function(){
    $('.tab-nav li a').removeClass('active');
    $(this).addClass('active');
})

//---------- Pokemon Functions ----------//
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
            allRatings()
        }
    })
})
//like review AJAX
$('.card').on('submit', '#like_form', function(e){
    let review_id = $(this).attr('review_id')
    e.preventDefault();
    console.log(review_id)
    $.ajax({
        url: "/like_review",
        method: "POST",
        data: $(this).serialize(),
        success: function(response){
            console.log(response)
            $('.r'+review_id).children('.card-item-icons.r').html(response)
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

//---------- Team Functions ----------//
//toggle Team stats
$('#toggle-stats').click(function(){
    $('.list-group-item.striped').toggle()
})
//Toggle Team Weakness
$('#toggle-weakness').click(function(){
    $('.chart-container').toggle()
})

//---------- Team Modal Functions ----------//
//display "Edit Team" modal
$('.edit-team').click(function(){
    $('.modal-bg').css("display", "block")
})