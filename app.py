from flask import Flask, render_template, request, jsonify
import sqlite3
from flask import g

app = Flask(__name__)

DATABASE = 'students.db'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def init_db():
    with app.app_context():
        db = get_db()
        cursor = db.cursor()
        cursor.execute('DROP TABLE IF EXISTS students')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS students (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id TEXT NOT NULL UNIQUE,
                name TEXT NOT NULL,
                gender TEXT NOT NULL,
                level INTEGER NOT NULL,
                course TEXT NOT NULL
            )
        ''')
        db.commit()

# Initialize the database
init_db()

# Route for home page
@app.route('/')
def index():
    return render_template('index.html')

# Route for fetching student data
@app.route('/students', methods=['GET'])
def get_students():
    cursor = get_db().cursor()
    cursor.execute('SELECT * FROM students')
    students = cursor.fetchall()
    # Convert to list of dictionaries
    students_list = [{'id': row[0], 'student_id': row[1], 'name': row[2], 'gender': row[3], 'level': row[4], 'course': row[5]} for row in students]
    return jsonify(students_list)

# Route for adding a new student record
@app.route('/students', methods=['POST'])
def add_student():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'Invalid input'}), 400
        
        required_fields = ['student_id', 'name', 'gender', 'level', 'course']
        if not all(field in data for field in required_fields):
            return jsonify({'error': 'Missing fields in input'}), 400
        
        cursor = get_db().cursor()
        cursor.execute('''
            INSERT INTO students (student_id, name, gender, level, course) VALUES (?, ?, ?, ?, ?)
        ''', (data['student_id'], data['name'], data['gender'], data['level'], data['course']))
        get_db().commit()
        return jsonify({'message': 'Student added successfully'}), 201
    except sqlite3.IntegrityError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Route for updating a student record
@app.route('/students/<student_id>', methods=['PUT'])
def update_student(student_id):
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'Invalid input'}), 400
        
        cursor = get_db().cursor()
        cursor.execute('''
            UPDATE students SET name=?, gender=?, level=?, course=? WHERE student_id=?
        ''', (data['name'], data['gender'], data['level'], data['course'], student_id))
        get_db().commit()
        return jsonify({'message': 'Student updated successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Route for deleting a student record
@app.route('/students/<student_id>', methods=['DELETE'])
def delete_student(student_id):
    try:
        cursor = get_db().cursor()
        cursor.execute('DELETE FROM students WHERE student_id=?', (student_id,))
        get_db().commit()
        return jsonify({'message': 'Student deleted successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
