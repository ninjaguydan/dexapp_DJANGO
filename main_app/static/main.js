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

// display reply form
$('.list-group-item').click(function(){
    $(this).find('.comment').css("display", "block");
})

