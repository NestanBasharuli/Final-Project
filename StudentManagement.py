import json
import sys


# Creating Student class which initialize every student in student list/
class Student:
    def __init__(self, name, roll_number, grade):
        self.name = name
        self.roll_number = roll_number
        self.grade = grade

    def __str__(self):
        return f"Name: {self.name}, Roll Number: {self.roll_number}, Grade: {self.grade}"


class StudentManager:
    # JSON file which contains students information
    student_list = "Student_List.json"

    def add_student(self):
        try:
            # Get new student information from user input
            student_name = str(input("Please Input Student Name: "))
            student_roll_number = int(input("Please Input Student Roll Number: "))
            student_grade = str(input("Please Input Student Grade: "))
            print()

            # Creating a new Student object to add in json
            new_student = Student(student_name, student_roll_number, student_grade)

            # Check if the student with the given roll number already exists
            check_if_student_exists = self.search_student_roll_number(
                student_roll_number)

            if not check_if_student_exists:
                # If the student does not exist, add to the list
                self.add_in_list(new_student)
            else:
                print("Student Already Exists With This Roll Number")
                return

        except TypeError:
            print("Oops Something Went Wrong, Please Input Correct Information")
        else:
            print("Student Added Successfully In List")

    def search_student_roll_number(self, roll_number=None):
        # Search for a student by roll number
        if roll_number is None:
            roll_number = int(
                input("Please Input Student Roll Number For Searching: "))
        print()

        # Read student data from JSON file
        json_data = self.read_json_file()

        # Use filter to find students with the specified roll number
        result = list(filter(lambda student: student.roll_number == roll_number, json_data))
        if result:
            for student in result:
                print(student)
                return student
        else:
            print("This Student Is Not In The List")
            return False

    # Show all students information
    def show_student_list(self):
        # Read information from json file
        json_data = self.read_json_file()

        if len(json_data) != 0:
            for student in json_data:
                print(student)
        else:
            print("Student List Is Empty")

    def add_in_list(self, student: Student):
        try:
            # Add a student to the list in the JSON file
            student_list = self.read_json_file()

            if not isinstance(student_list, list):
                student_list = [student_list]
            student_list.append(student)
            self.write_json_file(student_list)

        except FileNotFoundError:
            # If the file doesn't exist, create a new list with the student
            student = [student]
            self.write_json_file(student)

        except json.JSONDecodeError:
            print("Oops, there is wrong info in json file")


    # Change the grade of a student
    def change_student_grade(self):
        
        search_student = self.search_student_roll_number()
        new_grade = str(input("Please Input Student's New Grade: "))

        if isinstance(search_student, Student):
            # Modify the grade of the found student
            data_from_json = self.read_json_file()
            for student in data_from_json:
                if student.roll_number == search_student.roll_number:
                    data_from_json.remove(student)

            search_student.grade = new_grade

            data_from_json.append(search_student)
            self.write_json_file(data_from_json)

    def read_json_file(self):
        try:
            # Read data from the json file
            with open(self.student_list, "r") as json_file:
                data = json.load(
                    json_file, object_hook=self.custom_student_deserialization)
                return data
        except FileNotFoundError:
            return []

    def write_json_file(self, info):
        # Write data to the JSON file
        with open(self.student_list, "w") as json_file:
            json.dump(info, json_file, indent=4,
                      default=self.custom_student_serialization)

    @staticmethod
    def custom_student_serialization(obj):
        # Serialize a Student object to JSON
        if isinstance(obj, Student):
            return {
                "Name": obj.name,
                "Roll Number": obj.roll_number,
                "Grade": obj.grade
            }
        return obj

    @staticmethod
    def custom_student_deserialization(json_data):
        # Deserialize JSON data to a Student object
        return Student(json_data["Name"], json_data["Roll Number"], json_data["Grade"])


while True:
    student_manager = StudentManager()

    menu = """
        1. Add Student
        2. Show All Student
        3. Search By Roll Number
        4. Update Student's Grade
        5. Shut Down
    """

    print(menu)

    try:
        menu_choice = int(
            input("Please Input Number Which Is Shown In Menu: "))
        print()

        if menu_choice == 1:
            student_manager.add_student()
        elif menu_choice == 2:
            student_manager.show_student_list()
        elif menu_choice == 3:
            student_manager.search_student_roll_number()
        elif menu_choice == 4:
            student_manager.change_student_grade()
        elif menu_choice == 5:
            print("Good Bye See You Later")
            sys.exit()
        else:
            print("This Number Is Not In Menu, Please Input Correct Number")
    except Exception:
        print("Input Must Be Number Which Is Shown In The Menu")
