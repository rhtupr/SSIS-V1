import sqlite3

conn = sqlite3.connect("course.db")
cursor = conn.cursor()

# Create tables
def create_tables():
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS courses (
            course_code TEXT PRIMARY KEY,
            course_name TEXT
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS students (
            student_id INTEGER PRIMARY KEY,
            name TEXT,
            gender TEXT,
            year_level TEXT,
            course_code TEXT,
            FOREIGN KEY (course_code) REFERENCES courses (course_code)
        )
    """)
    conn.commit()

# Add course
def add_course(course_code, course_name):
    cursor.execute("INSERT INTO courses (course_code, course_name) VALUES (?, ?)", (course_code, course_name))
    conn.commit()

# Get courses
def get_courses():
    cursor.execute("SELECT course_code, course_name FROM courses")
    return cursor.fetchall()

# Add student
def add_student(student_id, name, gender, year_level, course_code):
    cursor.execute("INSERT INTO students (student_id, name, gender, year_level, course_code) VALUES (?, ?, ?, ?, ?)",
                   (student_id, name, gender, year_level, course_code))
    conn.commit()


# Get students
def get_students():
    cursor.execute("SELECT student_id, name, gender, year_level, course_code FROM students")
    return cursor.fetchall()

# Delete student
def delete_student(student_id):
    cursor.execute("DELETE FROM students WHERE student_id = ?", (student_id,))
    conn.commit()

# Update student
def update_student(student_id, name, gender, year_level, course_code):
    cursor.execute("UPDATE students SET name = ?, gender = ?, year_level = ?, course_code = ? WHERE student_id = ?",
                   (name, gender, year_level, course_code, student_id))
    conn.commit()

# Search students
def search_students(keyword):
    cursor.execute("SELECT student_id, name, gender, year_level, course_code FROM students WHERE name LIKE ?",
                   ('%' + keyword + '%',))
    return cursor.fetchall()
