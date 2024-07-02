document.addEventListener("DOMContentLoaded", function () {
    // Get all modals
    var modals = document.querySelectorAll(".modalBackground");

    // Get all buttons that open the modal
    var btns = document.querySelectorAll(".sign-up-button");

    // Add click event listeners to buttons
    btns.forEach(function (btn) {
        btn.onclick = function () {
            var modalId = btn.getAttribute("data-modal");
            var modal = document.getElementById(modalId);
            if (modal) {
                modal.style.display = "block";
            }
        };
    });

    // Add click event listeners to close buttons and modals
    modals.forEach(function (modal) {
        var closeBtn = modal.querySelector(".closeModalButton");
        closeBtn.onclick = function () {
            modal.style.display = "none";
        };
        window.onclick = function (event) {
            if (event.target == modal) {
                modal.style.display = "none";
            }
        };
    });

    window.onclick = function (event) {
        if (event.target == modal) {
            modal.style.display = "none";
        }
    };
    modals.forEach(function (modal) {
        window.onclick = function (event) {
            if (event.target == modal) {
                
            }
        }
    })
});