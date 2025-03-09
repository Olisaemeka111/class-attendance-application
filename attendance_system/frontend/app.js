document.getElementById('login-form').addEventListener('submit', function(event) {
    event.preventDefault();
    // Add your login logic here
    document.getElementById('login').style.display = 'none';
    document.getElementById('dashboard').style.display = 'block';
});