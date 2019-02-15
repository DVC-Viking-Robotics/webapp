var cross = document.getElementById("cross");
var menu = document.getElementById("menu");
var ham = document.getElementById("ham");

function showMenu() {
    menu.style.visibility = "visible";
    ham.style.visibility = "hidden";
    cross.style.visibility = "visible";
}

function hideMenu() {
    menu.style.visibility = "hidden";
    ham.style.visibility = "visible";
    cross.style.visibility = "hidden";
}

window.onload = function () {
    ham.onclick = showMenu;
    cross.onclick = hideMenu;
    menu.style.visibility = "hidden";
    cross.style.visibility = "hidden";
}

