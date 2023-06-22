from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, \
    QPushButton, QTableWidget, QTableWidgetItem
import sys


class Student:
    def __init__(self, student_id, name, gender, year_level, course_code):
        self.student_id = student_id
        self.name = name
        self.gender = gender
        self.year_level = year_level
        self.course_code = course_code


class Course:
    def __init__(self, course_code, course_name):
        self.course_code = course_code
        self.course_name = course_name


class StudentInformationSystem:
    def __init__(self):
        self.students = []
        self.courses = []
        self.student_filename = 'students.txt'
        self.course_filename = 'courses.txt'
        self.load_data()

    def load_data(self):
        try:
            with open(self.student_filename, 'r') as file:
                for line in file:
                    student_id, name, gender, year_level, course_code = line.strip().split(',')
                    student = Student(student_id, name, gender, year_level, course_code)
                    self.students.append(student)
        except FileNotFoundError:
            print("No student data found. Starting with an empty database.")

        try:
            with open(self.course_filename, 'r') as file:
                for line in file:
                    course_code, course_name = line.strip().split(',')
                    course = Course(course_code, course_name)
                    self.courses.append(course)
        except FileNotFoundError:
            print("No course data found. Starting with an empty database.")

    def save_data(self):
        with open(self.student_filename, 'w') as file:
            for student in self.students:
                file.write(f"{student.student_id},{student.name},{student.gender},{student.year_level},"
                           f"{student.course_code}\n")

        with open(self.course_filename, 'w') as file:
            for course in self.courses:
                file.write(f"{course.course_code},{course.course_name}\n")

    def add_student(self, student_id, name, gender, year_level, course_code):
        new_student = Student(student_id, name, gender, year_level, course_code)
        self.students.append(new_student)
        print(f"Student {name} has been added.")
        self.save_data()

    def delete_student(self, student_id):
        deleted = False
        for student in self.students:
            if student.student_id == student_id:
                self.students.remove(student)
                print(f"Student with ID {student_id} has been deleted.")
                deleted = True
                break
        if not deleted:
            print(f"Student with ID {student_id} was not found.")
        self.save_data()

    def edit_student(self, student_id, name=None, gender=None, year_level=None, course_code=None):
        for student in self.students:
            if student.student_id == student_id:
                if name:
                    student.name = name
                if gender:
                    student.gender = gender
                if year_level:
                    student.year_level = year_level
                if course_code:
                    student.course_code = course_code
                print(f"Student with ID {student_id} has been edited.")
                self.save_data()
                return
        print(f"Student with ID {student_id} was not found.")

    def search_student(self, student_id):
        for student in self.students:
            if student.student_id == student_id:
                print(f"Student ID: {student.student_id}")
                print(f"Name: {student.name}")
                print(f"Gender: {student.gender}")
                print(f"Year Level: {student.year_level}")
                print(f"Course Code: {student.course_code}")
                return
        print(f"Student with ID {student_id} was not found.")

    def list_students(self):
        print("List of Students:")
        for student in self.students:
            print(f"Student ID: {student.student_id}")
            print(f"Name: {student.name}")
            print(f"Gender: {student.gender}")
            print(f"Year Level: {student.year_level}")
            print(f"Course Code: {student.course_code}")
            print("------")

    def add_course(self, course_code, course_name):
        new_course = Course(course_code, course_name)
        self.courses.append(new_course)
        print(f"Course {course_name} has been added.")
        self.save_data()

    def delete_course(self, course_code):
        deleted = False
        deleted_students = []
        for student in self.students:
            if student.course_code == course_code:
                deleted_students.append(student)
        if deleted_students:
            for student in deleted_students:
                self.students.remove(student)
            print(f"All students enrolled in Course Code {course_code} have been deleted.")
            deleted = True

        for course in self.courses:
            if course.course_code == course_code:
                self.courses.remove(course)
                print(f"Course with Code {course_code} has been deleted.")
                deleted = True
                break

        if not deleted:
            print(f"Course with Code {course_code} was not found.")
        self.save_data()

    def edit_course(self, course_code, course_name):
        for course in self.courses:
            if course.course_code == course_code:
                course.course_name = course_name
                print(f"Course with Code {course_code} has been edited.")
                self.save_data()
                return
        print(f"Course with Code {course_code} was not found.")

    def search_course(self, course_code):
        for course in self.courses:
            if course.course_code == course_code:
                print(f"Course Code: {course.course_code}")
                print(f"Course Name: {course.course_name}")
                return
        print(f"Course with Code {course_code} was not found.")

    def list_courses(self):
        print("List of Courses:")
        for course in self.courses:
            print(f"Course Code: {course.course_code}")
            print(f"Course Name: {course.course_name}")
            print("------")


class MainWindow(QMainWindow):
    def __init__(self, sis):
        super().__init__()
        self.sis = sis
        self.setWindowTitle("Student Information System")
        self.setGeometry(100, 100, 500, 400)
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self.central_widget)

        # Search Section
        search_layout = QHBoxLayout()
        layout.addLayout(search_layout)

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search Student or Course")
        search_layout.addWidget(self.search_input)

        search_button = QPushButton("Search")
        search_button.clicked.connect(self.search)
        search_layout.addWidget(search_button)

        # Student Section
        student_label = QLabel("\n Student Information [Fill all information to add and edit student. Fill Student ID to delete.]")
        layout.addWidget(student_label)

        student_form_layout = QHBoxLayout()
        layout.addLayout(student_form_layout)

        self.student_id_input = QLineEdit()
        self.student_id_input.setPlaceholderText("Student ID")
        student_form_layout.addWidget(self.student_id_input)

        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Name")
        student_form_layout.addWidget(self.name_input)

        self.gender_input = QLineEdit()
        self.gender_input.setPlaceholderText("Gender")
        student_form_layout.addWidget(self.gender_input)

        self.year_level_input = QLineEdit()
        self.year_level_input.setPlaceholderText("Year Level")
        student_form_layout.addWidget(self.year_level_input)

        self.course_code_input = QLineEdit()
        self.course_code_input.setPlaceholderText("Course Code")
        student_form_layout.addWidget(self.course_code_input)

        student_button_layout = QHBoxLayout()
        layout.addLayout(student_button_layout)

        add_student_button = QPushButton("Add Student")
        add_student_button.clicked.connect(self.add_student)
        student_button_layout.addWidget(add_student_button)

        delete_student_button = QPushButton("Delete Student")
        delete_student_button.clicked.connect(self.delete_student)
        student_button_layout.addWidget(delete_student_button)

        edit_student_button = QPushButton("Edit Student")
        edit_student_button.clicked.connect(self.edit_student)
        student_button_layout.addWidget(edit_student_button)

        # Course Section
        course_label = QLabel("\n Course Information [Fill all information to add and edit course. Fill Course Code to delete.]")
        layout.addWidget(course_label)

        course_form_layout = QHBoxLayout()
        layout.addLayout(course_form_layout)

        self.course_code_input2 = QLineEdit()
        self.course_code_input2.setPlaceholderText("Course Code")
        course_form_layout.addWidget(self.course_code_input2)

        self.course_name_input = QLineEdit()
        self.course_name_input.setPlaceholderText("Course Name")
        course_form_layout.addWidget(self.course_name_input)

        course_button_layout = QHBoxLayout()
        layout.addLayout(course_button_layout)

        add_course_button = QPushButton("Add Course")
        add_course_button.clicked.connect(self.add_course)
        course_button_layout.addWidget(add_course_button)

        delete_course_button = QPushButton("Delete Course")
        delete_course_button.clicked.connect(self.delete_course)
        course_button_layout.addWidget(delete_course_button)

        edit_course_button = QPushButton("Edit Course")
        edit_course_button.clicked.connect(self.edit_course)
        course_button_layout.addWidget(edit_course_button)

        # Student List Section
        student_list_label = QLabel("\n Student List")
        layout.addWidget(student_list_label)

        self.student_table = QTableWidget()
        self.student_table.setColumnCount(5)
        self.student_table.setHorizontalHeaderLabels(["Student ID", "Name", "Gender", "Year Level", "Course Code"])
        layout.addWidget(self.student_table)

        # Course List Section
        course_list_label = QLabel("\n Course List")
        layout.addWidget(course_list_label)

        self.course_table = QTableWidget()
        self.course_table.setColumnCount(2)
        self.course_table.setHorizontalHeaderLabels(["Course Code", "Course Name"])
        layout.addWidget(self.course_table)

        self.refresh_tables()

    def refresh_tables(self):
        self.student_table.setRowCount(len(self.sis.students))
        for row, student in enumerate(self.sis.students):
            self.student_table.setItem(row, 0, QTableWidgetItem(student.student_id))
            self.student_table.setItem(row, 1, QTableWidgetItem(student.name))
            self.student_table.setItem(row, 2, QTableWidgetItem(student.gender))
            self.student_table.setItem(row, 3, QTableWidgetItem(student.year_level))
            self.student_table.setItem(row, 4, QTableWidgetItem(student.course_code))

        self.course_table.setRowCount(len(self.sis.courses))
        for row, course in enumerate(self.sis.courses):
            self.course_table.setItem(row, 0, QTableWidgetItem(course.course_code))
            self.course_table.setItem(row, 1, QTableWidgetItem(course.course_name))

    def search(self):
        search_text = self.search_input.text()
        if search_text:
            # Search for student
            self.student_table.clearSelection()
            for row in range(self.student_table.rowCount()):
                for col in range(self.student_table.columnCount()):
                    item = self.student_table.item(row, col)
                    if item and search_text.lower() in item.text().lower():
                        item.setSelected(True)

            # Search for course
            self.course_table.clearSelection()
            for row in range(self.course_table.rowCount()):
                for col in range(self.course_table.columnCount()):
                    item = self.course_table.item(row, col)
                    if item and search_text.lower() in item.text().lower():
                        item.setSelected(True)

    def add_student(self):
        student_id = self.student_id_input.text()
        name = self.name_input.text()
        gender = self.gender_input.text()
        year_level = self.year_level_input.text()
        course_code = self.course_code_input.text()

        if student_id and name and gender and year_level and course_code:
            self.sis.add_student(student_id, name, gender, year_level, course_code)
            self.refresh_tables()
            self.clear_input_fields()
        else:
            print("Please fill in all student information.")

    def delete_student(self):
        student_id = self.student_id_input.text()
        if student_id:
            self.sis.delete_student(student_id)
            self.refresh_tables()
            self.clear_input_fields()
        else:
            print("Please enter a student ID.")

    def edit_student(self):
        student_id = self.student_id_input.text()
        name = self.name_input.text()
        gender = self.gender_input.text()
        year_level = self.year_level_input.text()
        course_code = self.course_code_input.text()

        if student_id:
            self.sis.edit_student(student_id, name, gender, year_level, course_code)
            self.refresh_tables()
            self.clear_input_fields()
        else:
            print("Please enter a student ID.")

    def add_course(self):
        course_code = self.course_code_input2.text()
        course_name = self.course_name_input.text()

        if course_code and course_name:
            self.sis.add_course(course_code, course_name)
            self.refresh_tables()
            self.clear_input_fields()
        else:
            print("Please fill in both course code and course name.")

    def delete_course(self):
        course_code = self.course_code_input2.text()
        if course_code:
            self.sis.delete_course(course_code)
            self.refresh_tables()
            self.clear_input_fields()
        else:
            print("Please enter a course code.")

    def edit_course(self):
        course_code = self.course_code_input2.text()
        course_name = self.course_name_input.text()

        if course_code:
            self.sis.edit_course(course_code, course_name)
            self.refresh_tables()
            self.clear_input_fields()
        else:
            print("Please enter a course code.")

    def clear_input_fields(self):
        self.student_id_input.clear()
        self.name_input.clear()
        self.gender_input.clear()
        self.year_level_input.clear()
        self.course_code_input.clear()
        self.course_code_input2.clear()
        self.course_name_input.clear()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    sis = StudentInformationSystem()
    window = MainWindow(sis)
    window.show()
    sys.exit(app.exec_())
