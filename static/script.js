document.addEventListener('DOMContentLoaded', function() {
    loadStudents();
});

async function loadStudents() {
    try {
        const response = await fetch('/students');
        const students = await response.json();
        
        const tbody = document.getElementById('studentTable').getElementsByTagName('tbody')[0];
        tbody.innerHTML = '';

        students.forEach(student => {
            const row = document.createElement('tr');

            row.innerHTML = `
                <td>${student.id || ''}</td>
                <td>${student.student_id || ''}</td>
                <td>${student.name || ''}</td>
                <td>${student.gender || ''}</td>
                <td>${student.level || ''}</td>
                <td>${student.course || ''}</td>
                <td class="actions">
                    <button class="edit" onclick="editStudent('${student.student_id}', '${student.name}', '${student.gender}', ${student.level}, '${student.course}')">Edit</button>
                    <button class="delete" onclick="deleteStudent('${student.student_id}')">Delete</button>
                </td>
            `;

            tbody.appendChild(row);
        });
    } catch (error) {
        console.error('Error loading students:', error);
    }
}

async function submitForm(event) {
    event.preventDefault();
    
    const studentId = document.getElementById('student_id').value;
    const name = document.getElementById('name').value;
    const gender = document.getElementById('gender').value;
    const level = document.getElementById('level').value;
    const course = document.getElementById('course').value;

    const method = document.querySelector('button[type="submit"]').textContent === 'Add Student' ? 'POST' : 'PUT';
    const url = method === 'POST' ? '/students' : `/students/${studentId}`;
    
    const response = await fetch(url, {
        method: method,
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            student_id: studentId,
            name: name,
            gender: gender,
            level: parseInt(level),
            course: course
        })
    });

    const result = await response.json();
    alert(result.message || result.error);
    clearForm();
    loadStudents();
}

async function editStudent(studentId, name, gender, level, course) {
    document.getElementById('student_id').value = studentId;
    document.getElementById('name').value = name;
    document.getElementById('gender').value = gender;
    document.getElementById('level').value = level;
    document.getElementById('course').value = course;

    const submitButton = document.querySelector('#studentForm button[type="submit"]');
    submitButton.textContent = 'Update Student';
    submitButton.onclick = function(event) {
        submitForm(event);
    };
}

async function deleteStudent(studentId) {
    if (confirm(`Are you sure you want to delete student with ID ${studentId}?`)) {
        const response = await fetch(`/students/${studentId}`, {
            method: 'DELETE'
        });

        const result = await response.json();
        alert(result.message || result.error);
        loadStudents();
    }
}

function clearForm() {
    document.getElementById('studentForm').reset();
    document.querySelector('#studentForm button[type="submit"]').textContent = 'Add Student';
}
