var logoImage1 = document.getElementsByClassName("logo-icon-footer");
if (logoImage1) {
    logoImage1.addEventListener("click", function () {
        var anchor = document.querySelector("[data-scroll-to='navbar']");
        if (anchor) {
            anchor.scrollIntoView({ block: "start", behavior: "smooth" });
        }
    });
}
