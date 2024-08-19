const forms = document.querySelector(".forms"),
pwShowHide = document.querySelectorAll(".eye-icon"),
links = document.querySelectorAll(".link");

pwShowHide.forEach(eyeIcon => {
    eyeIcon.addEventListener("click", () => {
        let pwFields = eyeIcon.parentElement.parentElement.querySelectorAll(".password");

        pwFields.forEach(password => {
            if(password.type === "password"){
                password.type = "text";
                eyeIcon.classList.replace("bx-hide", "bx-show");
                return;
            }
            password.type = "password";
            eyeIcon.classList.replace("bx-show", "bx-hide");
        })

    })
})

links.forEach(link => {
    link.addEventListener("click", e => {
        e.preventDefault(); //preventing form submit
        forms.classList.toggle("show-signup");
    })
})

document.addEventListener('DOMContentLoaded', function() {
    const loginPopup = document.getElementById('login-popup');
    const loginLink = document.getElementById('login-link');
    const closeBtn = document.getElementById('close-btn');

    // Open the popup
    loginLink.addEventListener('click', function(event) {
        event.preventDefault();
        loginPopup.style.display = 'flex';
    });

    // Close the popup
    closeBtn.addEventListener('click', function() {
        loginPopup.style.display = 'none';
    });

    // Optional: Close the popup if user clicks outside of the popup content
    window.addEventListener('click', function(event) {
        if (event.target === loginPopup) {
            loginPopup.style.display = 'none';
        }
    });
});
