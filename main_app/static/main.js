const menuBtn = document.querySelector('.menu-btn');
// ..hamburger to "x" animation
let menuOpen = false;
menuBtn.addEventListener('click', () => {
    menuBtn.classList.toggle('open');
});

// ..hamburger Function
function openMenu() {
    let nav = document.querySelector('.mobile-nav');
    if (nav.style.display === "block") {
        nav.style.display = "none";
    } else {
        nav.style.display = "block";
    }
}
//---------- Navigation Functions ----------//
//display main nav dropdown menu
$('.main-nav span').click(function(){
    $('.dropdown-menu').toggle();
    $('.main-nav span').toggleClass('active');
})
//Close dropdown menu when clicking anywhere outside of it


//---------- Reply Form Functions ----------//
// display team reply form
$('.reply').click(function(){
    let team_id = $(this).attr('team_id');
    $(".comment_" + team_id).toggle();
})
// display review reply form
$('.reply').click(function(){
    let review_id = $(this).attr('review_id');
    $(".comment_" + review_id).toggle();
})
// display post reply form
$('.reply').click(function(){
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