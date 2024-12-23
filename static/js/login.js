  // Function to open the popup (login or signup)
  function openPopup(type) {
    if (type === 'login') {
        document.getElementById("login-popup").style.display = "block";
        document.getElementById("signup-popup").style.display = "none"; // Close signup if open
    } else if (type === 'signup') {
        document.getElementById("signup-popup").style.display = "block";
        document.getElementById("login-popup").style.display = "none"; // Close login if open
    }
}

// Function to close the popup (login or signup)
function closePopup(type) {
    if (type === 'login') {
        document.getElementById("login-popup").style.display = "none";
    } else if (type === 'signup') {
        document.getElementById("signup-popup").style.display = "none";
    }
}

// Close the popup when clicking outside of it
window.onclick = function(event) {
    const loginPopup = document.getElementById("login-popup");
    const signupPopup = document.getElementById("signup-popup");

    if (event.target === loginPopup) {
        loginPopup.style.display = "none";
    } else if (event.target === signupPopup) {
        signupPopup.style.display = "none";
    }
}