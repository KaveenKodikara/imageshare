function register() {
    const username = document.getElementById("username").value;
    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;
    const confirmPassword = document.getElementById("confirmPassword").value;

    if (password !== confirmPassword) {
        alert("Passwords do not match");
        return;
    }

    const user = { username, email, password };
    localStorage.setItem("user", JSON.stringify(user));
    alert("Registration successful");
}

function login() {
    const storedUser = JSON.parse(localStorage.getItem("user"));
    if (!storedUser) {
        alert("User not found. Please register.");
        return;
    }

    const loginUsername = document.getElementById("loginUsername").value;
    const loginPassword = document.getElementById("loginPassword").value;

    if (loginUsername === storedUser.username && loginPassword === storedUser.password) {
        alert("Login successful");
        redirectToHome();
    } else {
        alert("Invalid username or password");
    }
}
function redirectToHome() {
    window.location.href = "home.html";
}