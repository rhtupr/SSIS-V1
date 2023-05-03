class Student:
    def __init__(self, name, age, courses):      # called when a new instance is created
        self.name = name           # set the name, age, and courses attributes of the new instance
        self.age = age
        self.courses = courses

    def __repr__(self):     # returns a string representation of the object
        return f"Student(name='{self.name}', age={self.age}, courses={self.courses})"   # return a formatted string that includes the name, age, and courses attributes of the instance

class StudentInformationSystem:     # constructor for the class, initializes an empty list of students
    def __init__(self):
        self.students = []

    def add_student(self, name, age, courses):  # adds a new student to the list of students.
        student = Student(name, age, courses)      # create a new Student object with the provided name, age, and courses
        self.students.append(student)              # add the new student to the list
        print(f"{name} has been added to the system.")

    def delete_student(self, name):     # removes a student from the list of students by name
        for student in self.students:        # iterate through the list of students
            if student.name == name:              # if the student's name matches the provided name, the student will be remove from the list
                self.students.remove(student)
                print(f"{name} has been removed from the system.")
                break
        else:
            print(f"{name} is not in the system.")

    def edit_student(self, name, age=None, courses=None):     # updates a student's information by name
        for student in self.students:           # iterate through the list of students
            if student.name == name:                # if the student's name matches the provided name, the student's information is updated
                if age is not None:
                    student.age = age
                if courses is not None:
                    student.courses = courses
                print(f"{name}'s information has been updated.")
                break
        else:
            print(f"{name} is not in the system.")

    def list_students(self):     # lists all students in the system
        for student in self.students:     # iterate through the list of students and print each student's information
            print(student)

    def search_student(self, name):     # searches for a student by name in the system
        for student in self.students:      # iterate through the list of students
            if student.name == name:         # iterate through the list of students
                print(student)
                break
        else:
            print(f"{name} is not in the system.")

import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QTextEdit, QPushButton, QMessageBox

class StudentInformationSystemGUI(QWidget): # defines a class that inherits from the QWidget class in PyQt5
    def __init__(self):
        super().__init__()   # calls the __init__ method of the QWidget class
        self.initUI()       # Calls the initUI method defined in this class

    def initUI(self):
        self.setGeometry(100, 100, 350, 500) # sets the size and position of the window
        self.setWindowTitle('Simple Student Information System')
        self.setStyleSheet('background-color: #333333; color: white;')

        self.name_label = QLabel('Name:', self)     # creates a label for the student's name and sets its position and style
        self.name_label.move(20, 20)
        self.name_label.setStyleSheet('font-size: 10pt')
        self.name_textbox = QLineEdit(self)         # creates a text box for the student's name and sets its position, style, and size
        self.name_textbox.move(80, 20)
        self.name_textbox.setStyleSheet('background-color: #616161; color: white; font-size: 12px; border: 1px #616161;')
        self.name_textbox.setGeometry(80, 20, 250, 25)

        self.age_label = QLabel('Age:', self)
        self.age_label.move(20, 50)
        self.age_label.setStyleSheet('font-size: 10pt')
        self.age_textbox = QLineEdit(self)
        self.age_textbox.move(80, 50)
        self.age_textbox.setStyleSheet('background-color: #616161; color: white; font-size: 12px; border: 1px #616161;')
        self.age_textbox.setGeometry(80, 50, 250, 25)

        self.courses_label = QLabel('Courses:', self)
        self.courses_label.move(20, 80)
        self.courses_label.setStyleSheet('font-size: 10pt')
        self.courses_textbox = QLineEdit(self)
        self.courses_textbox.move(80, 80)
        self.courses_textbox.setStyleSheet('background-color: #616161; color: white; font-size: 12px; border: 1px #616161;')
        self.courses_textbox.setGeometry(80, 80, 250, 25)

        self.add_button = QPushButton('Add', self) # creates a button with the label 'Add', sets it as a child widget of this class
        self.add_button.move(20, 130)
        self.add_button.clicked.connect(self.add_student) # connects the button's 'clicked' signal to the 'add_student' method of this class
        self.add_button.setStyleSheet('font-size: 9pt;')

        self.delete_button = QPushButton('Delete', self)
        self.delete_button.move(80, 130)
        self.delete_button.clicked.connect(self.delete_student)
        self.delete_button.setStyleSheet('font-size: 9pt;')

        self.edit_button = QPushButton('Edit', self)
        self.edit_button.move(140, 130)
        self.edit_button.clicked.connect(self.edit_student)
        self.edit_button.setStyleSheet('font-size: 9pt;')

        self.list_button = QPushButton('List', self)
        self.list_button.move(200, 130)
        self.list_button.clicked.connect(self.list_students)
        self.list_button.setStyleSheet('font-size: 9pt;')

        self.search_button = QPushButton('Search', self)
        self.search_button.move(260, 130)
        self.search_button.clicked.connect(self.search_student)
        self.search_button.setStyleSheet('font-size: 9pt;')

        self.result_textbox = QTextEdit(self)
        self.result_textbox.setGeometry(20, 180, 315, 300)
        self.result_textbox.setStyleSheet('background-color: #292828; color: white; font-size: 12px; border: 1px #292828;')

        self.show()

    def add_student(self):
        name = self.name_textbox.text() # gets the name, age and course of the student from the text box
        age = self.age_textbox.text()
        courses = self.courses_textbox.text()

        if name and age and courses: # checks if all fields are filled out
            with open('students.txt', 'a') as f: # opens a file called 'students.txt' in append mode
                f.write(f"{name},{age},{courses}\n") # writes the new student information to the file
            self.result_textbox.setText(f"Added student: {name} ({age}) {courses}") # sets the result text box to show the added student's information
            self.clear_fields() # clears the input fields
        else:
            QMessageBox.warning(self, "Warning", "Please fill in all fields!")

    def delete_student(self):
        name = self.name_textbox.text()

        if name: # checks if a name was entered
            students = []
            with open('students.txt', 'r') as f:    # opens the file 'students.txt' in read mode
                for line in f:  # iterates over each line in the file
                    student_name, _, _ = line.strip().split(',')    # splits the line into name, age, and courses and assigns them to variables
                    if student_name != name:    # if the name of the student in the file does not match the entered name, add the line to a list
                        students.append(line)

            with open('students.txt', 'w') as f:
                f.writelines(students)  # writes the remaining students, those that were not deleted back to the file

            self.result_textbox.setText(f"Deleted student: {name}")
            self.clear_fields()
        else:
            QMessageBox.warning(self, "Warning", "Please enter a name to delete!")

    def edit_student(self):
        name = self.name_textbox.text()
        age = self.age_textbox.text()
        courses = self.courses_textbox.text()

        if name and age and courses:
            students = []
            with open('students.txt', 'r') as f:
                for line in f:
                    student_name, _, _ = line.strip().split(',')
                    if student_name == name:
                        students.append(f"{name},{age},{courses}\n")
                    else:
                        students.append(line)

            with open('students.txt', 'w') as f:
                f.writelines(students)

            print(f"Edited student: {name} ({age}) {courses}")
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
            self.result_textbox.setText("List of students:\n\n" + "".join(students))
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

if __name__ == '__main__': # checks if the script is being run directly as the main module
    app = QApplication(sys.argv) # creates an instance of QApplication, is necessary to create a GUI application in PyQt
    ex = StudentInformationSystemGUI() #  creates an instance of the StudentInformationSystemGUI class
    sys.exit(app.exec_())
