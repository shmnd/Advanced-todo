document.addEventListener("DOMContentLoaded", function () {
    var signupForm = document.getElementById("_sign_up_form");

    if (signupForm) {
        signupForm.addEventListener("submit", function (event) {
            event.preventDefault(); // Prevent default form submission

            var email = document.getElementById("signup-email").value.trim();
            var username = document.getElementById("signup-username").value.trim();
            var password = document.getElementById("signup-password").value.trim();
            var confirmPassword = document.getElementById("confirm-password").value.trim();

            // Validate form fields
            if (!validateEmail(email)) {
                showMessage("Please enter a valid email address.", "error");
                return;
            }
            if (username.length < 3) {
                showMessage("Username must be at least 3 characters long.", "error");
                return;
            }
            if (password.length < 6) {
                showMessage("Password must be at least 6 characters long.", "error");
                return;
            }
            if (password !== confirmPassword) {
                showMessage("Passwords do not match.", "error");
                return;
            }

            // Simulate form submission (AJAX)
            submitSignupForm(email, username, password);
        });
    }

    // Function to validate email
    function validateEmail(email) {
        var re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return re.test(email);
    }

    // Function to show messages (error/success)
    function showMessage(message, type) {
        var messageBox = document.createElement("div");
        messageBox.className = "alert alert-" + (type === "error" ? "danger" : "success");
        messageBox.innerHTML = message;
        var formContainer = document.querySelector(".w-lg-500px");
        formContainer.prepend(messageBox);
        setTimeout(function () {
            messageBox.remove();
        }, 3000);
    }

    // Function to submit signup form (AJAX)
    function submitSignupForm(email, username, password) {
        var submitButton = document.getElementById("_sign_up_submit");
        submitButton.disabled = true;
        submitButton.innerHTML = 'Please wait... <span class="spinner-border spinner-border-sm align-middle ms-2"></span>';

        fetch(api_config.authentication_url, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": getCSRFToken(),
            },
            body: JSON.stringify({
                email: email,
                username: username,
                password: password
            }),
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                showMessage("Signup successful! Redirecting...", "success");
                setTimeout(() => {
                    window.location.href = "/login/"; // Redirect to login
                }, 2000);
            } else {
                showMessage(data.error || "An error occurred. Please try again.", "error");
            }
        })
        .catch(error => {
            showMessage("Network error. Please try again later.", "error");
        })
        .finally(() => {
            submitButton.disabled = false;
            submitButton.innerHTML = "Sign Up";
        });
    }

    // Function to get CSRF token from cookies
    function getCSRFToken() {
        let cookieValue = null;
        if (document.cookie && document.cookie !== "") {
            document.cookie.split(";").forEach(function (cookie) {
                let trimmedCookie = cookie.trim();
                if (trimmedCookie.startsWith("csrftoken=")) {
                    cookieValue = trimmedCookie.substring("csrftoken=".length);
                }
            });
        }
        return cookieValue;
    }
});
