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

// function leaveReply() {
//     let form = document.querySelector('.comment');
//     if (form.style.display === "block") {
//         form.style.display = "none";
//     } else {
//         form.style.display = "block"
//     }
// }