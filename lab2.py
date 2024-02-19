import enum

# Define the SAVE variable or provide a valid file path
SAVE = "University.txt"

# Define the Level enum for logging
class Level(enum.Enum):
    ERROR = 1
    WARNING = 2
    INFO = 3
    DEBUG = 4

class StudyField(enum.Enum):
    MECHANICAL_ENGINEERING = 0
    SOFTWARE_ENGINEERING = 1
    FOOD_TECHNOLOGY = 2
    URBANISM_ARCHITECTURE = 3
    VETERINARY_MEDICINE = 4

class Student:
    def __init__(self, first, last, email, enrollment, dob, grad=False):
        self.first_name = first
        self.last_name = last
        self.email = email
        self.enrollment_date = enrollment
        self.date_of_birth = dob
        self.is_graduated = grad

    def print_info(self):
        print(f"\n{self.first_name}|{self.last_name}|{self.email}|{self.enrollment_date}|{self.date_of_birth}")


class Faculty:
    def __init__(self, name, abbreviation, field):
        self.name = name
        self.abbreviation = abbreviation
        self.students = []
        self.study_field = field

    def add_student(self, student):
        self.students.append(student)

    def display_students(self):
        print(f"Students enrolled in {self.name} faculty:")
        for student in self.students:
            student.print_info()

    def display_graduates(self):
        print(f"Graduates from {self.name} faculty:")
        for student in self.students:
            if student.is_graduated:
                student.print_info()

    def check_student(self, email):
        for student in self.students:
            if student.email == email:
                return True
        return False

    def graduate_student(self, email):
        for student in self.students:
            if student.email == email:
                student.is_graduated = True
                print(f"{student.first_name} {student.last_name} graduated from {self.name} faculty.")
                return
        print(f"Student with email '{email}' not found in {self.name} faculty.")


class University:
    def __init__(self):
        self.faculties = []

    def create_faculty(self, name, abbreviation, field):
        self.faculties.append(Faculty(name, abbreviation, field))

    def find_faculty_by_student_email(self, email):
        for faculty in self.faculties:
            if faculty.check_student(email):
                return faculty
        return None

    def display_faculties(self):
        print("University Faculties:")
        for faculty in self.faculties:
            print(f"- {faculty.abbreviation} Faculty: {faculty.name}")

    def display_faculties_by_field(self, field):
        print(f"Faculties in {field.name} field:")
        for faculty in self.faculties:
            if faculty.study_field == field:
                print(f"- {faculty.abbreviation} Faculty: {faculty.name}")

    def display_students_in_faculty(self, abbreviation):
        for faculty in self.faculties:
            if faculty.abbreviation == abbreviation:
                faculty.display_students()
                return
        print(f"Faculty with abbreviation '{abbreviation}' not found!")

    def display_graduates_in_faculty(self, abbreviation):
        for faculty in self.faculties:
            if faculty.abbreviation == abbreviation:
                faculty.display_graduates()
                return
        print(f"Faculty with abbreviation '{abbreviation}' not found!")


class FileManager:
    @staticmethod
    def save_university_data(filename, university):
        with open(filename, "w") as outfile:
            for faculty in university.faculties:
                outfile.write(f"{faculty.name} {faculty.abbreviation} {faculty.study_field.value}\n")
                for student in faculty.students:
                    outfile.write(f"{student.first_name} {student.last_name} {student.email} "
                                  f"{student.enrollment_date} {student.date_of_birth} {student.is_graduated}\n")
                outfile.write("\n")

    @staticmethod
    def load_university_data(filename, university):
        with open(filename, "r") as infile:
            lines = infile.readlines()
            i = 0
            while i < len(lines):
                name, abbreviation, field = lines[i].split()
                university.create_faculty(name, abbreviation, StudyField(int(field)))
                i += 1
                while i < len(lines) and lines[i].strip():
                    first, last, email, enroll, birth, grad = lines[i].split()
                    university.faculties[-1].add_student(
                        Student(first, last, email, enroll, birth, bool(int(grad)))
                    )
                    i += 1
                i += 1

class Log:
    def __init__(self, level):
        self.log_level = level

    def create_log_file(self):
        try:
            with open("log.txt", "w") as create_file:
                print("Log file created successfully!")
        except IOError:
            print("Error: Unable to create log file!")

    def log_message(self, level, message):
        if self.log_level.value >= level.value:  # Compare integer values of enum members
            try:
                with open("log.txt", "a") as logfile:
                    level_string = {Level.ERROR: "ERROR", Level.WARNING: "WARNING",
                                    Level.INFO: "INFO", Level.DEBUG: "DEBUG"}[level]
                    logfile.write(f"[{level_string}] {message}\n")
            except IOError:
                print("Error: Unable to open log file for writing!")
                self.create_log_file()

    def m_error(self, message):
        self.log_message(Level.ERROR, message)

    def m_warn(self, message):
        self.log_message(Level.WARNING, message)

    def m_info(self, message):
        self.log_message(Level.INFO, message)

    def m_debug(self, message):
        self.log_message(Level.DEBUG, message)

if __name__ == "__main__":
    tum = University()
    log = Log(Level.DEBUG)
    log.m_debug("Trying to load the university.txt file")
    FileManager.load_university_data(SAVE, tum)
    choice = None

    while choice != 0:
        print("TUM Board Menu:")
        print("1. Faculty Operations")
        print("2. General Operations")
        print("0. Exit")
        choice = int(input("Enter your choice: "))

        if choice == 1:  # Faculty Choice
            print("Faculty Operations:")
            print("1. Create and assign a student to a faculty")
            print("2. Graduate a student from a faculty")
            print("3. Display current enrolled students")
            print("4. Display graduates")
            print("5. Check if a student belongs to a faculty")
            print("0. Return to the Board Menu")
            faculty_choice = int(input("Enter your choice: "))

            if faculty_choice == 1:  # Create and assign a student to a faculty
                first = input("Enter student first name: ")
                last = input("Enter student last name: ")
                email = input("Enter student email: ")
                enrollment = input("Enter student enrollment date: ")
                dob = input("Enter student date of birth: ")

                student = Student(first, last, email, enrollment, dob)

                abbreviation = input("Enter the abbreviation of the faculty: ")
                faculty_found = False
                for f in tum.faculties:
                    if f.abbreviation == abbreviation:
                        f.add_student(student)
                        print(f"Student added to {f.name} faculty.")
                        log.m_info(f"Student added to {f.name} faculty.")
                        faculty_found = True
                        FileManager.save_university_data(SAVE, tum)
                        log.m_info("Saved the operation in the file.")
                        break

                if not faculty_found:
                    print(f"Faculty with abbreviation '{abbreviation}' not found!")
                    log.m_error(f"Faculty with abbreviation '{abbreviation}' not found when adding a student.")

            elif faculty_choice == 2:  # Graduate a student from a faculty
                email = input("Enter student email to graduate: ")
                log.m_info("Attempting to graduate student with email: " + email)
                faculty = tum.find_faculty_by_student_email(email)
                if faculty is not None:
                    faculty.graduate_student(email)
                    FileManager.save_university_data(SAVE, tum)
                    log.m_info("Saved data in the file.")
                else:
                    print(f"Student with email '{email}' not found in any faculty.")
                    log.m_warn(f"Attempted to graduate student with email '{email}', but student not found.")

            elif faculty_choice == 3:  # Display current enrolled students
                abbreviation = input("Enter faculty abbreviation to display current enrolled students: ")
                tum.display_students_in_faculty(abbreviation)

            elif faculty_choice == 4:  # Display graduates
                abbreviation = input("Enter faculty abbreviation to display graduates: ")
                tum.display_graduates_in_faculty(abbreviation)

            elif faculty_choice == 5:  # Check if a student belongs to a faculty
                email = input("Enter student email to check: ")
                log.m_info(f"Checking if student with email '{email}' belongs to any faculty.")
                faculty = tum.find_faculty_by_student_email(email)
                if faculty is not None:
                    print(f"Student with email '{email}' belongs to {faculty.name} faculty.")
                    log.m_info(f"Student with email '{email}' belongs to {faculty.name} faculty.")
                else:
                    print(f"Student with email '{email}' not found in any faculty.")
                    log.m_warn(f"Student with email '{email}' not found in any faculty.")

        elif choice == 2:  # General Choice
            print("General Operations:")
            print("1. Create a new faculty")
            print("2. Search what faculty a student belongs to")
            print("3. Display University faculties")
            print("4. Display faculties belonging to a field")
            print("0. Return to the Board Menu")
            general_choice = int(input("Enter your choice: "))

            if general_choice == 1:  # Create a new faculty
                name = input("Enter faculty name: ")
                abbreviation = input("Enter faculty abbreviation: ")
                field = int(input("Enter field (0-4): "))
                tum.create_faculty(name, abbreviation, StudyField(field))
                print("Faculty created successfully!")
                log.m_info(f"Faculty created successfully: {abbreviation}")
                FileManager.save_university_data(SAVE, tum)
                log.m_info("Saved data in the file.")

            elif general_choice == 2:  # Search what faculty a student belongs to
                email = input("Enter student email to search: ")
                log.m_info("Searching faculty for student with email: " + email)
                faculty = tum.find_faculty_by_student_email(email)
                if faculty is not None:
                    print(f"Student with email '{email}' belongs to {faculty.name} faculty.")
                    log.m_info(f"Student with email '{email}' belongs to {faculty.name} faculty.")
                else:
                    print(f"Student with email '{email}' not found in any faculty.")
                    log.m_warn(f"Student with email '{email}' not found in any faculty.")

            elif general_choice == 3:  # Display University faculties
                tum.display_faculties()

            elif general_choice == 4:  # Display faculties belonging to a field
                field = int(input("Enter the field (0-4): "))
                tum.display_faculties_by_field(StudyField(field))

        elif choice == 0:  # Exiting the Program
            print("Exiting...")
            FileManager.save_university_data(SAVE, tum)
            log.m_info("Exiting the program.")

        else:
            print("Invalid choice!")
            log.m_warn("Invalid choice entered in main menu.")

