function close_sidebar() {
    document.getElementById("overlay").style.display = "none";
    document.getElementById("sidebar").style.display = "none";
}

function dropdown_click(name) {
    var x = document.getElementById(name);
    if (x.className.indexOf("w3-show") == -1) {
        x.className += " w3-show";
        x.previousElementSibling.className += " w3-blue";
    } else {
        x.className = x.className.replace(" w3-show", "");
        x.previousElementSibling.className = x.previousElementSibling.className.replace(" w3-blue", "");
    }
}

function open_sidebar() {
    document.getElementById("overlay").style.display = "block";
    document.getElementById("sidebar").style.display = "block";
}
