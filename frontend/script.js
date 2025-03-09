const API_URL = "http://127.0.0.1:5000";

// Fetch students and populate dropdown
async function loadStudents() {
    try {
        let response = await fetch(`${API_URL}/students`);
        if (!response.ok) throw new Error("Failed to fetch students");
        let students = await response.json();
        let dropdown = document.getElementById("students");
        dropdown.innerHTML = ""; // Clear existing options

        students.forEach(student => {
            let option = document.createElement("option");
            option.value = student.student_id;
            option.textContent = `${student.name} (${student.class})`;
            dropdown.appendChild(option);
        });
    } catch (error) {
        console.error("Error loading students:", error);
        alert("Error loading students. Please try again later.");
    }
}

// Mark Attendance
async function markAttendance(status) {
    let student_id = document.getElementById("students").value;
    let subject = document.getElementById("subject").value;

    if (!student_id || !subject) {
        alert("Please select a student and enter subject!");
        return;
    }

    try {
        let response = await fetch(`${API_URL}/attendance`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ student_id, subject, status })
        });

        if (!response.ok) throw new Error("Failed to mark attendance");
        let result = await response.json();
        alert(result.message);
        fetchAttendance(student_id);
    } catch (error) {
        console.error("Error marking attendance:", error);
        alert("Error marking attendance. Please try again later.");
    }
}

// Fetch attendance records
async function fetchAttendance(student_id) {
    try {
        let response = await fetch(`${API_URL}/attendance/${student_id}`);
        if (!response.ok) throw new Error("Failed to fetch attendance records");
        let records = await response.json();

        let list = document.getElementById("attendance-list");
        list.innerHTML = "";

        records.forEach(record => {
            let li = document.createElement("li");
            li.textContent = `${record.date} - ${record.subject} - ${record.status}`;
            list.appendChild(li);
        });
    } catch (error) {
        console.error("Error fetching attendance records:", error);
        alert("Error fetching attendance records. Please try again later.");
    }
}

// Load students on page load
window.onload = loadStudents;
