import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton,
    QComboBox, QTableWidget, QTableWidgetItem, QMessageBox, QDialog, QFormLayout
)
from PyQt5.QtCore import Qt
import database


class StudentInfoSystem(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Student Information System")
        self.resize(600, 600)
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.setup_ui()

    def setup_ui(self):
        # Title Label
        title_label = QLabel("Student Information System", self)
        title_label.setAlignment(Qt.AlignCenter)

        # Search Layout
        search_layout = QHBoxLayout()
        search_label = QLabel("Search:", self)
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Enter student name to search")  # Add placeholder text
        search_button = QPushButton("Search")
        search_button.clicked.connect(self.search_students)
        search_layout.addWidget(search_label)
        search_layout.addWidget(self.search_input)
        search_layout.addWidget(search_button)

        # Main Layout
        main_layout = QVBoxLayout(self.central_widget)
        main_layout.addWidget(title_label)
        main_layout.addLayout(search_layout)

        # Students Table
        self.students_table = QTableWidget()
        self.students_table.setColumnCount(5)
        self.students_table.setHorizontalHeaderLabels(
            ["Student ID", "Name", "Gender", "Year Level", "Course Code"]
        )
        self.students_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.students_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.students_table.setSelectionMode(QTableWidget.SingleSelection)
        main_layout.addWidget(self.students_table)

        # List Layout
        list_layout = QHBoxLayout()
        list_button = QPushButton("Students List")
        list_button.clicked.connect(self.list_students)
        list_layout.addWidget(list_button)
        main_layout.addLayout(list_layout)

        # CRUD Layout
        crud_layout = QHBoxLayout()
        add_student_button = QPushButton("Add Student")
        add_student_button.clicked.connect(self.add_student_window)
        add_course_button = QPushButton("Add Course")
        add_course_button.clicked.connect(self.add_course_window)
        delete_button = QPushButton("Delete")
        delete_button.clicked.connect(self.delete_student)
        edit_button = QPushButton("Edit")
        edit_button.clicked.connect(self.edit_student_window)  # Connect to the edit_student_window function
        crud_layout.addWidget(add_student_button)
        crud_layout.addWidget(add_course_button)
        crud_layout.addWidget(delete_button)
        crud_layout.addWidget(edit_button)
        main_layout.addLayout(crud_layout)

    def search_students(self):
        search_text = self.search_input.text()
        if search_text:
            students = database.search_students(search_text)
            self.populate_students_table(students)
        else:
            QMessageBox.warning(self, "Error", "Please enter a search query.")

    def list_students(self):
        students = database.get_students()
        self.populate_students_table(students)

    def populate_students_table(self, students):
        self.students_table.clearContents()
        self.students_table.setRowCount(len(students))
        for row_number, data in enumerate(students):
            for column_number, data in enumerate(data):
                item = QTableWidgetItem(str(data))
                item.setTextAlignment(Qt.AlignCenter)
                self.students_table.setItem(row_number, column_number, item)

    def delete_student(self):
        selected_row = self.students_table.currentRow()
        if selected_row >= 0:
            student_id = self.students_table.item(selected_row, 0).text()
            reply = QMessageBox.question(
                self, "Confirmation", f"Are you sure you want to delete student ID {student_id}?",
                QMessageBox.Yes | QMessageBox.No
            )
            if reply == QMessageBox.Yes:
                database.delete_student(student_id)
                self.list_students()
        else:
            QMessageBox.warning(self, "Error", "Please select a student to delete.")

    def edit_student_window(self):  # Add the function to open the edit student window
        selected_row = self.students_table.currentRow()
        if selected_row >= 0:
            student_id = self.students_table.item(selected_row, 0).text()
            name = self.students_table.item(selected_row, 1).text()
            gender = self.students_table.item(selected_row, 2).text()
            year_level = self.students_table.item(selected_row, 3).text()
            course_code = self.students_table.item(selected_row, 4).text().split(" - ")[0]
            dialog = EditStudentWindow(self, student_id, name, gender, year_level, course_code)  # Create an instance of the edit student window
            dialog.exec_()
        else:
            QMessageBox.warning(self, "Error", "Please select a student to edit.")

    def add_student_window(self):
        dialog = AddStudentWindow(self)
        dialog.exec_()

    def add_course_window(self):
        dialog = AddCourseWindow(self)
        dialog.exec_()

    def closeEvent(self, event):
        reply = QMessageBox.question(
            self, "Confirmation", "Are you sure you want to exit the application?",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()


class AddStudentWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Add Student")

        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)

        form_layout = QFormLayout()
        self.student_id_input = QLineEdit()
        self.student_id_input.setPlaceholderText("eg. 2021-0510")  # Add placeholder text
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("First Name M.I. Last Name")  # Add placeholder text
        self.gender_combo = QComboBox()
        self.gender_combo.addItem("")
        self.gender_combo.addItems(["Male", "Female"])
        self.year_level_combo = QComboBox()
        self.year_level_combo.addItem("")
        self.year_level_combo.addItems(["1st Year", "2nd Year", "3rd Year", "4th Year", "5th Year"])
        self.course_code_combo = QComboBox()
        self.load_course_codes()

        form_layout.addRow("Student ID:", self.student_id_input)
        form_layout.addRow("Name:", self.name_input)
        form_layout.addRow("Gender:", self.gender_combo)
        form_layout.addRow("Year Level:", self.year_level_combo)
        form_layout.addRow("Course Code:", self.course_code_combo)

        button_layout = QHBoxLayout()
        add_button = QPushButton("Add")
        add_button.clicked.connect(self.add_student)
        cancel_button = QPushButton("Cancel")
        cancel_button.clicked.connect(self.close)
        button_layout.addWidget(add_button)
        button_layout.addWidget(cancel_button)

        layout.addLayout(form_layout)
        layout.addLayout(button_layout)

    def load_course_codes(self):
        courses = database.get_courses()
        self.course_code_combo.clear()
        for code, name in courses:
            self.course_code_combo.addItem(f"{code} - {name}")

    def add_student(self):
        student_id = self.student_id_input.text()
        name = self.name_input.text()
        gender = self.gender_combo.currentText()
        year_level = self.year_level_combo.currentText()
        course_code = self.course_code_combo.currentText().split(" - ")[0]
        if student_id and name and gender and year_level and course_code:
            database.add_student(student_id, name, gender, year_level, course_code)
            QMessageBox.information(self, "Success", "Student added successfully!")
            self.close()
        else:
            QMessageBox.warning(self, "Error", "Please fill in all the student details.")


class EditStudentWindow(QDialog):  # Add the edit student window class
    def __init__(self, parent=None, student_id="", name="", gender="", year_level="", course_code=""):
        super().__init__(parent)
        self.setWindowTitle("Edit Student")

        self.student_id = student_id

        self.setup_ui(name, gender, year_level, course_code)

    def setup_ui(self, name, gender, year_level, course_code):
        layout = QVBoxLayout(self)

        form_layout = QFormLayout()
        self.name_input = QLineEdit(name)
        self.gender_combo = QComboBox()
        self.gender_combo.addItems(["Male", "Female"])
        self.gender_combo.setCurrentText(gender)
        self.year_level_combo = QComboBox()
        self.year_level_combo.addItems(["1st Year", "2nd Year", "3rd Year", "4th Year", "5th Year"])
        self.year_level_combo.setCurrentText(year_level)
        self.course_code_combo = QComboBox()
        self.load_course_codes()
        self.course_code_combo.setCurrentText(course_code)

        form_layout.addRow("Name:", self.name_input)
        form_layout.addRow("Gender:", self.gender_combo)
        form_layout.addRow("Year Level:", self.year_level_combo)
        form_layout.addRow("Course Code:", self.course_code_combo)

        button_layout = QHBoxLayout()
        save_button = QPushButton("Save")
        save_button.clicked.connect(self.save_student)
        cancel_button = QPushButton("Cancel")
        cancel_button.clicked.connect(self.close)
        button_layout.addWidget(save_button)
        button_layout.addWidget(cancel_button)

        layout.addLayout(form_layout)
        layout.addLayout(button_layout)

    def load_course_codes(self):
        courses = database.get_courses()
        self.course_code_combo.clear()
        for code, name in courses:
            self.course_code_combo.addItem(f"{code} - {name}")

    def save_student(self):
        name = self.name_input.text()
        gender = self.gender_combo.currentText()
        year_level = self.year_level_combo.currentText()
        course_code = self.course_code_combo.currentText().split(" - ")[0]
        if name and gender and year_level and course_code:
            database.update_student(self.student_id, name, gender, year_level, course_code)
            QMessageBox.information(self, "Success", "Student updated successfully!")
            self.close()
        else:
            QMessageBox.warning(self, "Error", "Please fill in all the student details.")


class AddCourseWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Add Course")

        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)

        form_layout = QFormLayout()
        self.course_code_input = QLineEdit()
        self.course_code_input.setPlaceholderText("Course Code")  # Add placeholder text
        self.course_name_input = QLineEdit()
        self.course_name_input.setPlaceholderText("Course Name")  # Add placeholder text

        form_layout.addRow("Course Code:", self.course_code_input)
        form_layout.addRow("Course Name:", self.course_name_input)

        button_layout = QHBoxLayout()
        add_button = QPushButton("Add")
        add_button.clicked.connect(self.add_course)
        cancel_button = QPushButton("Cancel")
        cancel_button.clicked.connect(self.close)
        button_layout.addWidget(add_button)
        button_layout.addWidget(cancel_button)

        layout.addLayout(form_layout)
        layout.addLayout(button_layout)

    def add_course(self):
        course_code = self.course_code_input.text()
        course_name = self.course_name_input.text()
        if course_code and course_name:
            database.add_course(course_code, course_name)
            QMessageBox.information(self, "Success", "Course added successfully!")
            self.close()
        else:
            QMessageBox.warning(self, "Error", "Please fill in the course details.")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = StudentInfoSystem()
    window.show()
    sys.exit(app.exec_())
