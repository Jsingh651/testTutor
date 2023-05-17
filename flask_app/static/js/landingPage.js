function openMenu() {
    const screenWidth = window.innerWidth;
    if (screenWidth <= 800) {
        document.getElementById("menu").style.left = "0";
    } else {
        document.getElementById("menu").style.left = "0";
        document.getElementById("main").style.marginLeft = "240px";
    }
    document.querySelector(".section__one").classList.add("menu-opened");
    localStorage.setItem("menuOpen", "true");
    document.querySelector(".header__btn_menu").innerHTML = '<i class="fa-solid fa-xmark"></i>';
}

function closeMenu() {
    const screenWidth = window.innerWidth;
    if (screenWidth <= 800) {
        document.getElementById("menu").style.left = "-240px";
    } else {
        document.getElementById("menu").style.left = "-240px";
        document.getElementById("main").style.marginLeft = "0";
    }
    document.querySelector(".section__one").classList.remove("menu-opened");
    localStorage.setItem("menuOpen", "false");
    document.querySelector(".header__btn_menu").innerHTML = '<i class="fas fa-bars"></i>';
}

function setMenuState() {
    const menuOpen = localStorage.getItem("menuOpen");
    if (menuOpen === "true") {
        openMenu();
    } else {
        closeMenu();
    }
}

// Set the menu state on page load
setMenuState();

// Toggle the menu state when the header button is clicked
document.querySelector(".header__btn_menu").addEventListener("click", function () {
    const menuOpen = localStorage.getItem("menuOpen");
    if (menuOpen === "true") {
        closeMenu();
    } else {
        openMenu();
    }
});

// Close the menu when the close button is clicked
document.querySelector(".btn__menu--close").addEventListener("click", closeMenu);

// Close the menu when the user clicks outside the menu
document.addEventListener("click", function (event) {
    const menu = document.getElementById("menu");
    const menuButton = document.querySelector(".header__btn_menu");
    if (event.target !== menu && event.target !== menuButton && !menu.contains(event.target)) {
        closeMenu();
    }
});



document.querySelectorAll('details').forEach(function (details) {
    details.addEventListener('toggle', function () {
        var icon = details.querySelector('summary i');
        if (icon) {
            icon.classList.toggle('fa-rotate-180');
        }
    });
});
var details = document.getElementsByTagName('details');

// loop through each details element
for(var i=0; i<details.length; i++) {
    // set the open attribute to true
    details[i].setAttribute('open', 'true');
}

