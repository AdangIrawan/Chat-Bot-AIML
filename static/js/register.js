
document.getElementById('registerForm').addEventListener('submit', function (event) {
    var password = document.getElementById('password').value;
    var confirmPassword = document.getElementById('confirmPassword').value;
    var errorMessage = document.getElementById('errorMessage');

    // Clear previous error message
    errorMessage.textContent = '';

    setTimeout(function () {
        errorMessage.textContent = ''; // Clear error message
    }, 2000);

    if (password !== confirmPassword) {
        errorMessage.textContent = 'Password do not match';
        event.preventDefault(); // Prevent form submission
        setTimeout(function () {
            errorMessage.textContent = ''; // Clear error message after 2 seconds
        }, 2000);
    }
});

// Set timeout to clear error message after 2 seconds
setTimeout(function () {
    var errorMessage = document.getElementById('errorMessage');
    errorMessage.textContent = ''; // Clear error message
}, 2000);