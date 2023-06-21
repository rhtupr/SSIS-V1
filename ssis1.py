import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QMainWindow, QLabel, QLineEdit, QPushButton,
    QTextEdit, QMessageBox, QTableWidget, QTableWidgetItem,
    QVBoxLayout, QHBoxLayout, QDialog, QComboBox, QFormLayout, QDialogButtonBox
)
from PyQt5.QtCore import Qt
import csv

class Student:
    def __init__(self, student_id, name, gender, year_level, course_code, course):
        self.student_id = student_id
        self.name = name
        self.gender = gender
        self.year_level = year_level
        self.course_code = course_code
        self.course = course

    def __str__(self):
        return f"ID {self.student_id}      {self.name}\t{self.gender}\tLevel {self.year_level}\t{self.course_code}\t{self.course}"

class Course:
    def __init__(self, course_code, course):
        self.course_code = course_code
        self.course = course

    def __repr__(self):
        return f"Course(course_code='{self.course_code}', course='{self.course}')"

class StudentInformationSystem:
    def __init__(self):
        self.students = []
        self.courses = []

    def load_students_from_file(self):
        try:
            with open('students.csv', 'r') as f:
                reader = csv.reader(f)
                next(reader)  # skip the header row
                for row in reader:
                    if len(row) >= 5:
                        student_id, name, gender, year_level, course_code, *course = row
                        student = Student(student_id, name, gender, year_level, course_code, ''.join(course))
                        self.students.append(student)
                    else:
                        print(f"Ignoring row: {row} (insufficient values)")
        except FileNotFoundError:
            print("Students file not found.")

    def load_courses_from_file(self):
        try:
            with open('courses.csv', 'r') as f:
                reader = csv.reader(f)
                next(reader)  # skip the header row
                for row in reader:
                    if len(row) >= 2:
                        course_code, course = row[:2]
                        course = Course(course_code, course)
                        self.courses.append(course)
                    else:
                        print(f"Ignoring row: {row} (insufficient values)")
        except FileNotFoundError:
            print("Courses file not found.")

    def run(self):
        # Main program logic
        pass

    def add_student(self, student_id, name, gender, year_level, course_code, course):
        student = Student(student_id, name, gender, year_level, course_code, course)
        self.students.append(student)
        self.save_students_to_file()
        print(f"Added student: {student}")

        # Add the course to self.courses if it doesn't already exist
        if not self.get_course_by_code(course_code):
            self.add_course(course_code, course)

    def add_course(self, course_code, course):
        course = Course(course_code, course)
        self.courses.append(course)
        self.save_courses_to_file()
        print(f"Added course: {course}")

    def get_course_by_code(self, course_code):
        for course in self.courses:
            if course.course_code == course_code:
                return course
        return None

    def delete_student(self, student_id):
        student = self.search_student(student_id)
        if student:
            self.students.remove(student)
            print(f"Deleted student: {student}")

            # Remove the course if no other students are enrolled
            course_code = student.course_code
            self.remove_course_if_unused(course_code)

            self.save_students_to_file()
        else:
            print(f"Student with ID {student_id} not found.")

    def remove_course_if_unused(self, course_code):
        for student in self.students:
            if student.course_code == course_code:
                return  # Course still has enrolled students

        course = self.get_course_by_code(course_code)
        if course:
            self.courses.remove(course)
            self.save_courses_to_file()
            print(f"Deleted unused course: {course}")

    def search_student(self, student_id):
        for student in self.students:
            if student.student_id == student_id:
                return student
        return None

    def save_students_to_file(self):
        with open('students.csv', 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(["student_id", "name", "gender", "year_level", "course_code", "course"])
            for student in self.students:
                writer.writerow([student.student_id, student.name, student.gender, student.year_level, student.course_code, student.course])
        print("Saved students to file.")

    def save_courses_to_file(self):
        with open('courses.csv', 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(["course_code", "course"])
            for course in self.courses:
                writer.writerow([course.course_code, course.course])
        print("Saved courses to file.")

class StudentInfoSystemGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Student Information System")
        self.resize(600, 600)
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.sis = StudentInformationSystem()
        self.sis.load_students_from_file()
        self.sis.load_courses_from_file()

        self.setup_ui()

    def setup_ui(self):
        # Title Label
        title_label = QLabel("Student Information System", self)
        title_label.setAlignment(Qt.AlignCenter)

        # Search Layout
        search_layout = QHBoxLayout()
        search_label = QLabel("Search:", self)
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Enter student name to search")
        search_button = QPushButton("Search")
        search_button.clicked.connect(self.search_students)
        search_layout.addWidget(search_label)
        search_layout.addWidget(self.search_input)
        search_layout.addWidget(search_button)

        # Student Table
        self.student_table = QTableWidget()
        self.student_table.setColumnCount(6)
        self.student_table.setHorizontalHeaderLabels(["ID", "Name", "Gender", "Level", "Course Code", "Course"])
        self.student_table.setEditTriggers(QTableWidget.NoEditTriggers)  # Make table read-only
        self.student_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.student_table.setSelectionMode(QTableWidget.SingleSelection)

        # Buttons Layout
        buttons_layout = QHBoxLayout()
        add_button = QPushButton("Add Student")
        add_button.clicked.connect(self.show_add_student_dialog)
        delete_button = QPushButton("Delete Student")
        delete_button.clicked.connect(self.delete_student)
        edit_button = QPushButton("Edit Student")
        edit_button.clicked.connect(self.edit_student)
        list_button = QPushButton("List of Students")
        list_button.clicked.connect(self.list_students)
        buttons_layout.addWidget(add_button)
        buttons_layout.addWidget(delete_button)
        buttons_layout.addWidget(edit_button)
        buttons_layout.addWidget(list_button)

        # Main Layout
        main_layout = QVBoxLayout(self.central_widget)
        main_layout.addWidget(title_label)
        main_layout.addLayout(search_layout)
        main_layout.addWidget(self.student_table)
        main_layout.addLayout(buttons_layout)

        # Populate student table
        self.populate_student_table()

    def populate_student_table(self):
        self.student_table.setRowCount(0)  # Clear existing rows

        for student in self.sis.students:
            row_position = self.student_table.rowCount()
            self.student_table.insertRow(row_position)

            self.student_table.setItem(row_position, 0, QTableWidgetItem(student.student_id))
            self.student_table.setItem(row_position, 1, QTableWidgetItem(student.name))
            self.student_table.setItem(row_position, 2, QTableWidgetItem(student.gender))
            self.student_table.setItem(row_position, 3, QTableWidgetItem(student.year_level))
            self.student_table.setItem(row_position, 4, QTableWidgetItem(student.course_code))
            self.student_table.setItem(row_position, 5, QTableWidgetItem(student.course))

    def show_add_student_dialog(self):
        dialog = AddStudentDialog(self)
        if dialog.exec_():
            student_id = dialog.student_id_input.text()
            name = dialog.name_input.text()
            gender = dialog.gender_input.currentText()
            year_level = dialog.year_level_input.text()
            course_code = dialog.course_code_input.text()
            course = dialog.course_input.text()

            if not student_id or not name or not year_level or not course_code or not course:
                QMessageBox.warning(self, "Error", "Please fill all the fields.")
                return

            if self.sis.search_student(student_id):
                QMessageBox.warning(self, "Error", "A student with the same ID already exists.")
                return

            self.sis.add_student(student_id, name, gender, year_level, course_code, course)
            self.populate_student_table()

    def delete_student(self):
        selected_row = self.student_table.currentRow()
        if selected_row >= 0:
            student_id = self.student_table.item(selected_row, 0).text()
            self.sis.delete_student(student_id)
            self.populate_student_table()

    def edit_student(self):
        selected_row = self.student_table.currentRow()
        if selected_row >= 0:
            student_id = self.student_table.item(selected_row, 0).text()
            student = self.sis.search_student(student_id)
            if student:
                dialog = EditStudentDialog(self, student)
                if dialog.exec_():
                    name = dialog.name_input.text()
                    gender = dialog.gender_input.currentText()
                    year_level = dialog.year_level_input.text()
                    course_code = dialog.course_code_input.text()
                    course = dialog.course_input.text()

                    if not name or not year_level or not course_code or not course:
                        QMessageBox.warning(self, "Error", "Please fill all the fields.")
                        return

                    student.name = name
                    student.gender = gender
                    student.year_level = year_level
                    student.course_code = course_code
                    student.course = course

                    self.sis.save_students_to_file()
                    self.populate_student_table()
                    QMessageBox.information(self, "Success", "Student information updated.")
            else:
                QMessageBox.warning(self, "Error", "Student not found.")

    def search_students(self):
        search_text = self.search_input.text().lower()
        if search_text:
            results = []
            for student in self.sis.students:
                if search_text in student.name.lower():
                    results.append(student)

            self.student_table.setRowCount(0)  # Clear existing rows
            for student in results:
                row_position = self.student_table.rowCount()
                self.student_table.insertRow(row_position)

                self.student_table.setItem(row_position, 0, QTableWidgetItem(student.student_id))
                self.student_table.setItem(row_position, 1, QTableWidgetItem(student.name))
                self.student_table.setItem(row_position, 2, QTableWidgetItem(student.gender))
                self.student_table.setItem(row_position, 3, QTableWidgetItem(student.year_level))
                self.student_table.setItem(row_position, 4, QTableWidgetItem(student.course_code))
                self.student_table.setItem(row_position, 5, QTableWidgetItem(student.course))
        else:
            self.populate_student_table()

    def list_students(self):
        students = [str(student) for student in self.sis.students]
        QMessageBox.information(self, "List of Students", "\n".join(students))


class AddStudentDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Add Student")

        self.student_id_input = QLineEdit()
        self.name_input = QLineEdit()
        self.gender_input = QComboBox()
        self.gender_input.addItems(["Male", "Female"])
        self.year_level_input = QComboBox()
        self.year_level_input.addItems(["1", "2", "3", "4"])
        self.course_code_input = QComboBox()
        self.course_code_input.addItems(["BSIS", "BSIT", "BSCA", "BSCS"])
        self.course_input = QComboBox()
        self.course_input.addItems(["BS in Information System", "BS in Information Technology", "BS in Computer Application", "BS in Computer Science"])


        form_layout = QFormLayout()
        form_layout.addRow("Student ID:", self.student_id_input)
        form_layout.addRow("Name:", self.name_input)
        form_layout.addRow("Gender:", self.gender_input)
        form_layout.addRow("Year Level:", self.year_level_input)
        form_layout.addRow("Course Code:", self.course_code_input)
        form_layout.addRow("Course:", self.course_input)

        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)

        layout = QVBoxLayout(self)
        layout.addLayout(form_layout)
        layout.addWidget(buttons)

class EditStudentDialog(QDialog):
    def __init__(self, parent=None, student=None):
        super().__init__(parent)
        self.setWindowTitle("Edit Student")
        self.student = student

        self.student_id_input = QLineEdit(student.student_id)
        self.name_input = QLineEdit(student.name)
        self.gender_input = QComboBox()
        self.gender_input.addItems(["Male", "Female"])
        self.gender_input.setCurrentText(student.gender)
        self.year_level_input = QLineEdit(student.year_level)
        self.course_code_input = QLineEdit(student.course_code)
        self.course_input = QLineEdit(student.course)

        form_layout = QFormLayout()
        form_layout.addRow("Student ID:", self.student_id_input)
        form_layout.addRow("Name:", self.name_input)
        form_layout.addRow("Gender:", self.gender_input)
        form_layout.addRow("Year Level:", self.year_level_input)
        form_layout.addRow("Course Code:", self.course_code_input)
        form_layout.addRow("Course:", self.course_input)

        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(self.accept_changes)
        buttons.rejected.connect(self.reject)

        main_layout = QVBoxLayout(self)
        main_layout.addLayout(form_layout)
        main_layout.addWidget(buttons)

    def accept_changes(self):
        self.student.student_id = self.student_id_input.text()
        self.student.name = self.name_input.text()
        self.student.gender = self.gender_input.currentText()
        self.student.year_level = self.year_level_input.text()
        self.student.course_code = self.course_code_input.text()
        self.student.course = self.course_input.text()

        self.accept()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = StudentInfoSystemGUI()
    window.show()
    sys.exit(app.exec_())
