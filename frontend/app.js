// Example function to register a user
async function registerUser(username, password) {
    const response = await fetch('http://localhost:5000/auth/register', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ username, password })
    });
    const data = await response.json();
    console.log(data);
}

// Example function to login a user
async function loginUser(username, password) {
    const response = await fetch('http://localhost:5000/auth/login', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ username, password })
    });
    const data = await response.json();
    console.log(data);
}

// Example function to get students
async function getStudents(token) {
    const response = await fetch('http://localhost:5000/students', {
        method: 'GET',
        headers: {
            'Authorization': `Bearer ${token}`
        }
    });
    const data = await response.json();
    console.log(data);
}

// Example function to mark attendance
async function markAttendance(student_id, subject, token) {
    const response = await fetch('http://localhost:5000/attendance', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({ student_id, subject })
    });
    const data = await response.json();
    console.log(data);
}