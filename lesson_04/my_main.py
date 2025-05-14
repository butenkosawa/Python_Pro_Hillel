import csv
from pathlib import Path

# ─────────────────────────────────────────────────────────
# STORAGE SIMULATION
# ─────────────────────────────────────────────────────────
STORAGE_FILE_NAME = Path(__file__).parent.parent / "storage/students.csv"

# ─────────────────────────────────────────────────────────
# INFRASTRUCTURE
# ─────────────────────────────────────────────────────────
class Repository:

    def __init__(self):
        self.file = open(STORAGE_FILE_NAME, "r")
        self.students = self.get_storage()

        # close after reading
        self.file.close()

    def get_storage(self):
        reader = csv.DictReader(self.file)
        students: dict = {}
        for student in reader:
            id_ = int(student.pop('id'))
            if student["marks"]:
                student["marks"] = [int(item) for item in student["marks"].split(',')]
            else:
                student["marks"] = []
            students[id_] = student
        return students

    def update_storage(self):
        storage_ = []
        for k, v in self.students.items():
            student_ = {"id": k}
            v["marks"] = ",".join(list(map(lambda x: str(x), v["marks"])))
            student_.update(v)
            storage_.append(student_)

        self.file = open(STORAGE_FILE_NAME, "w", newline="")
        writer = csv.DictWriter(self.file, fieldnames=["id", "name", "marks", "info"])
        writer.writeheader()
        for student in storage_:
            writer.writerow(student)
        self.file.close()

    def add_student(self, student: dict):
        next_id = max(self.students.keys(), default=0) + 1
        self.students[next_id] = student
        self.update_storage()
        return student

    def update_student(self, id_: int, student: dict):
        self.students[id_] = student
        self.update_storage()
        print(f"Student {student['name']} is updated")

    def delete_student(self, id_: int):
        name = self.students[id_]["name"]
        del self.students[id_]
        self.update_storage()
        print(f"Student {name} is deleted")

    def add_mark(self, id_: int, mark: int):
        self.students[id_]["marks"].append(mark)
        self.update_storage()
        print(f"Student {self.students[id_]['name']} is updated")

    def get_student(self, id_: int) -> dict | None:
        return self.students.get(id_)


repo = Repository()


def inject_repository(func):
    def inner(*args, **kwargs):
        return func(*args, repo=repo, **kwargs)

    return inner


# ─────────────────────────────────────────────────────────
# DOMAIN (students, users, notification)
# ─────────────────────────────────────────────────────────
class StudentService:

    @inject_repository
    def show_students(self, repo: Repository):
        print("=========================")
        for id_, student in repo.students.items():
            print(f"{id_}. Student {student['name']}")
        print("=========================\n")

    @staticmethod
    def show_student(student: dict) -> None:
        print(
            "=========================\n"
            f"Student {student['name']}\n"
            f"Marks: {student['marks']}\n"
            f"Info: {student['info']}\n"
            "========================="
        )


# ─────────────────────────────────────────────────────────
# OPERATIONAL (APPLICATION) LAYER
# ─────────────────────────────────────────────────────────
def ask_student_payload() -> dict | None:
    name = input("Enter student's name: ")
    while not name:
        name = input("Student name is required. Please, enter the name again: ")

    row_marks = input("Enter student's marks separated by ','.\nIf the student has no marks, press Enter: ")
    if row_marks:
        row_marks = row_marks.replace(" ", "").split(",")
        if all([item.isdigit() for item in row_marks]):
            marks = [int(item) for item in row_marks]
        else:
            print("Incorrect input of student marks")
            return None
    else:
        marks = []

    details = input("Enter some detail information about student or press Enter: ")

    return {
        "name": name,
        "marks": marks,
        "info": details
    }


def student_management_command_handle(command: str):
    students_service = StudentService()
    if command == "show":
        students_service.show_students()

    elif command == "add":
        data = ask_student_payload()
        if data:
            student: dict | None = repo.add_student(data)
            if student is None:
                print("Error adding student")
            else:
                print(f"Student: {student['name']} is added")
        else:
            print("The student's data is NOT correct. Please try again")

    elif command == "search":
        student_id: str = input("\nEnter student's ID: ")
        if not student_id:
            print("Student's ID is required to search")
            return

        student: dict | None = repo.get_student(int(student_id))
        if student is None:
            print("Error searching student. Non-existent ID entered.")
        else:
            students_service.show_student(student)

    elif command == "delete":
        student_id: str = input("\nEnter student's ID: ")
        if not student_id:
            print("Student's id is required to delete")
            return

        id_ = int(student_id)
        if repo.get_student(id_):
            repo.delete_student(id_)
        else:
            print("Error on deleting student")

    elif command == "update":
        student_id: str = input("\nEnter student's ID: ")
        if not student_id:
            print("Student's ID is required to update student information.")
            return

        id_ = int(student_id)
        student = repo.get_student(id_)
        if student:
            students_service.show_student(student)
            print(
                f"What information about student you want to update?\n"
                f"If NAME pres `N`, if INFO press `I`, if NAME and INFO press `A`.\n"
            )

            user_input: str = input("Enter: ").upper()

            if user_input == "N":
                student["name"] = input("Enter new student's name: ")
                repo.update_student(id_, student)
            elif user_input == "I":
                student["info"] = input("Enter new student's info: ")
                repo.update_student(id_, student)
            elif user_input == "A":
                student["name"] = input("Enter new student's name: ")
                student["info"] = input("Enter new student's info: ")
                repo.update_student(id_, student)
            else:
                print("Error of choice")
        else:
            print("Error on updating student")

    elif command == "add mark":
        student_id: str = input("\nEnter student's ID: ")
        if not student_id:
            print("Student's id is required to update student marks.")
            return

        id_ = int(student_id)
        student = repo.get_student(id_)
        if student:
            students_service.show_student(student)
            mark: int = int(input("Enter new mark: "))
            if 0 < mark <= 12:
                repo.add_mark(id_, mark)
            else:
                print("Incorrect mark entered, must be from 1 to 12")
        else:
            print("Error on updating student marks")


# ─────────────────────────────────────────────────────────
# PRESENTATION LEVEL
# ─────────────────────────────────────────────────────────
def handle_user_input():
    OPERATIONAL_COMMANDS = ("quit", "help")
    STUDENT_MANAGEMENT_COMMANDS = ("show", "add", "search", "delete", "update", "add mark")
    AVAILABLE_COMMANDS = (*OPERATIONAL_COMMANDS, *STUDENT_MANAGEMENT_COMMANDS)

    HELP_MESSAGE = (
        "Hello in the Journal! User the menu to interact with the application.\n"
        f"Available commands: {AVAILABLE_COMMANDS}"
    )

    print(HELP_MESSAGE)

    while True:
        command = input("\n Select command: ")

        if command == "quit":
            print("\nThanks for using the Journal application")
            break
        elif command == "help":
            print(HELP_MESSAGE)
        else:
            student_management_command_handle(command)


# ─────────────────────────────────────────────────────────
# ENTRYPOINT
# ─────────────────────────────────────────────────────────
if __name__ == "__main__":
    handle_user_input()
