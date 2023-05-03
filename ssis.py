class Student:
    # Define the __init__ method, which is called when a new instance is created
    def __init__(self, name, age, courses):
        # Set the name, age, and courses attributes of the new instance
        self.name = name
        self.age = age
        self.courses = courses

    # Define the __repr__ method, which returns a string representation of the object
    def __repr__(self):
        # Return a formatted string that includes the name, age, and courses attributes of the instance
        return f"Student(name='{self.name}', age={self.age}, courses={self.courses})"

class StudentInformationSystem:
    # This is the constructor for the class, which initializes an empty list of students.
    def __init__(self):
        self.students = []

    # This method adds a new student to the list of students.
    def add_student(self, name, age, courses):
        # Create a new Student object with the provided name, age, and courses.
        student = Student(name, age, courses)
        # Add the new student to the list of students.
        self.students.append(student)
        # Print a message indicating that the student has been added to the system.
        print(f"{name} has been added to the system.")

    # This method removes a student from the list of students by name.
    def delete_student(self, name):
        # Iterate through the list of students.
        for student in self.students:
            # If the student's name matches the provided name, remove the student from the list of students.
            if student.name == name:
                self.students.remove(student)
                # Print a message indicating that the student has been removed from the system.
                print(f"{name} has been removed from the system.")
                # Exit the loop since we found the student we wanted to remove.
                break
        # If no match is found, print a message indicating that the student is not in the system.
        else:
            print(f"{name} is not in the system.")

    # This method updates a student's information by name.
    def edit_student(self, name, age=None, courses=None):
        # Iterate through the list of students.
        for student in self.students:
            # If the student's name matches the provided name, update the student's information as needed.
            if student.name == name:
                if age is not None:
                    student.age = age
                if courses is not None:
                    student.courses = courses
                # Print a message indicating that the student's information has been updated.
                print(f"{name}'s information has been updated.")
                # Exit the loop since we found the student we wanted to update.
                break
        # If no match is found, print a message indicating that the student is not in the system.
        else:
            print(f"{name} is not in the system.")

    # This method lists all students in the system.
    def list_students(self):
        # Iterate through the list of students and print each student's information.
        for student in self.students:
            print(student)

    # This method searches for a student by name in the system.
    def search_student(self, name):
        # Iterate through the list of students.
        for student in self.students:
            # If the student's name matches the provided name, print the student's information.
            if student.name == name:
                print(student)
                # Exit the loop since we found the student we were searching for.
                break
        # If no match is found, print a message indicating that the student is not in the system.
        else:
            print(f"{name} is not in the system.")


import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QTextEdit, QPushButton, QMessageBox

class StudentInformationSystemGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(100, 100, 400, 300)
        self.setWindowTitle('Student Information System')

        self.name_label = QLabel('Name:', self)
        self.name_label.move(20, 20)
        self.name_textbox = QLineEdit(self)
        self.name_textbox.move(80, 20)

        self.age_label = QLabel('Age:', self)
        self.age_label.move(20, 50)
        self.age_textbox = QLineEdit(self)
        self.age_textbox.move(80, 50)

        self.courses_label = QLabel('Courses:', self)
        self.courses_label.move(20, 80)
        self.courses_textbox = QTextEdit(self)
        self.courses_textbox.setGeometry(80, 80, 300, 100)

        self.add_button = QPushButton('Add', self)
        self.add_button.move(20, 200)
        self.add_button.clicked.connect(self.add_student)

        self.delete_button = QPushButton('Delete', self)
        self.delete_button.move(80, 200)
        self.delete_button.clicked.connect(self.delete_student)

        self.edit_button = QPushButton('Edit', self)
        self.edit_button.move(140, 200)
        self.edit_button.clicked.connect(self.edit_student)

        self.list_button = QPushButton('List', self)
        self.list_button.move(200, 200)
        self.list_button.clicked.connect(self.list_students)

        self.search_button = QPushButton('Search', self)
        self.search_button.move(260, 200)
        self.search_button.clicked.connect(self.search_student)

        self.result_textbox = QTextEdit(self)
        self.result_textbox.setGeometry(20, 240, 360, 50)

        self.show()

    def add_student(self):
        name = self.name_textbox.text()
        age = self.age_textbox.text()
        courses = self.courses_textbox.toPlainText()

        if name and age and courses:
            with open('students.txt', 'a') as f:
                f.write(f"{name},{age},{courses}\n")
            self.result_textbox.setText(f"Added student: {name} ({age}) {courses}")
            self.clear_fields()
        else:
            QMessageBox.warning(self, "Warning", "Please fill in all fields!")

    def delete_student(self):
        name = self.name_textbox.text()

        if name:
            students = []
            with open('students.txt', 'r') as f:
                for line in f:
                    student_name, _, _ = line.strip().split(',')
                    if student_name != name:
                        students.append(line)

            with open('students.txt', 'w') as f:
                f.writelines(students)

            self.result_textbox.setText(f"Deleted student: {name}")
            self.clear_fields()
        else:
            QMessageBox.warning(self, "Warning", "Please enter a name to delete!")

    def edit_student(self):
        name = self.name_textbox.text()
        age = self.age_textbox.text()
        courses = self.courses_textbox.toPlainText()

        if name and age and courses:
            students = []
            with open('students.txt', 'r') as f:
                for line in f:
                    student_name, _, _ = line.strip().split
                    if student_name == name:
                        students.append(f"{name},{age},{courses}\n")
                    else:
                        students.append(line)

            with open('students.txt', 'w') as f:
                f.writelines(students)

            self.result_textbox.setText(f"Edited student: {name} ({age}) {courses}")
            self.clear_fields()
        else:
            QMessageBox.warning(self, "Warning", "Please fill in all fields!")

    def list_students(self):
        students = []
        with open('students.txt', 'r') as f:
            for line in f:
                students.append(line)

        if students:
            self.result_textbox.setText("List of students:\n" + "".join(students))
        else:
            self.result_textbox.setText("No students found!")

    def search_student(self):
        name = self.name_textbox.text()

        if name:
            students = []
            with open('students.txt', 'r') as f:
                for line in f:
                    student_name, _, _ = line.strip().split(',')
                    if student_name == name:
                        students.append(line)

            if students:
                self.result_textbox.setText("Search result:\n" + "".join(students))
            else:
                self.result_textbox.setText(f"No student found with name: {name}")
            self.clear_fields()
        else:
            QMessageBox.warning(self, "Warning", "Please enter a name to search!")

    def clear_fields(self):
        self.name_textbox.clear()
        self.age_textbox.clear()
        self.courses_textbox.clear()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = StudentInformationSystemGUI()
    sys.exit(app.exec_())
