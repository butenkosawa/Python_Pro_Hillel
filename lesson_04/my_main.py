import csv
from pathlib import Path


# ─────────────────────────────────────────────────────────
# STORAGE SIMULATION
# ─────────────────────────────────────────────────────────
storage: dict[int, dict] = {
    1: {
        "name": "Alice Johnson",
        "marks": [7, 8, 9, 10, 6, 7, 8],
        "info": "Alice Johnson is 18 y.o. Interests: math",
    },
    2: {
        "name": "Michael Smith",
        "marks": [6, 5, 7, 8, 7, 9, 10],
        "info": "Michael Smith is 19 y.o. Interests: science",
    },
    3: {
        "name": "Emily Davis",
        "marks": [9, 8, 8, 7, 6, 7, 7],
        "info": "Emily Davis is 17 y.o. Interests: literature",
    },
    4: {
        "name": "James Wilson",
        "marks": [5, 6, 7, 8, 9, 10, 11],
        "info": "James Wilson is 20 y.o. Interests: sports",
    },
    5: {
        "name": "Olivia Martinez",
        "marks": [10, 9, 8, 7, 6, 5, 4],
        "info": "Olivia Martinez is 18 y.o. Interests: art",
    },
    6: {
        "name": "Emily Davis",
        "marks": [4, 5, 6, 7, 8, 9, 10],
        "info": "Daniel Brown is 19 y.o. Interests: music",
    },
    7: {
        "name": "Sophia Taylor",
        "marks": [11, 10, 9, 8, 7, 6, 5],
        "info": "Sophia Taylor is 20 y.o. Interests: physics",
    },
    8: {
        "name": "William Anderson",
        "marks": [7, 7, 7, 7, 7, 7, 7],
        "info": "William Anderson is 18 y.o. Interests: chemistry",
    },
    9: {
        "name": "Isabella Thomas",
        "marks": [8, 8, 8, 8, 8, 8, 8],
        "info": "Isabella Thomas is 19 y.o. Interests: biology",
    },
    10: {
        "name": "Benjamin Jackson",
        "marks": [9, 9, 9, 9, 9, 9, 9],
        "info": "Benjamin Jackson is 20 y.o. Interests: history",
    },
}

STORAGE_FILE_NAME = Path(__file__).parent.parent / "storage/students.csv"


# ─────────────────────────────────────────────────────────
# INFRASTRUCTURE
# ─────────────────────────────────────────────────────────
class Repository:
    """
    RAM: John, Marry, Mark
    SSD: John, Marry
    """
    def __init__(self):
        self.file = open(STORAGE_FILE_NAME, "r")
        self.students = self.get_storage()

        # close after reading
        self.file.close()

    def get_storage(self):
        self.file.seek(0)
        reader = csv.DictReader(self.file)
        return list(reader)

    def add_student(self, student: dict):
        self.students.append(student)
        writer = csv.DictWriter(self.file, fieldnames=["id", "name", "marks", "info"])
        writer.writerow(student)


    def update_storage(self, students: list[dict]):
        file = open(STORAGE_FILE_NAME, "w")
        writer = csv.DictWriter(file, fieldnames=["id", "name", "marks", "info"])
        writer.writeheader()
        for student in students:
            writer.writerow(student)

        file.close()

    # def __del__(self):
    #     self.file.seek(0)
    #     writer = csv.DictWriter(self.file, fieldnames=["id", "name", "marks", "info"])
    #     for student in self.students:
    #         writer.writerow(student)
    #     self.file.close()

repo = Repository()

def inject_repository(func):
    def inner(*args, **kwargs):
        return func(*args, repo=repo, **kwargs)
    return inner

# ─────────────────────────────────────────────────────────
# DOMAIN (students, users, notification)
# ─────────────────────────────────────────────────────────
class StudentService:
    def __init__(self):
        self.repository = Repository()

    @inject_repository
    def add_student(self, student: dict) -> dict | None:
        next_id = max(storage.keys()) + 1
        storage[next_id] = student
        return student

    @inject_repository
    def show_students(self, repo: Repository):
        print("=========================")
        for student in repo.students:
            print(f"{student['id']}. Student {student['name']}")
        print("=========================\n")


    def show_student(self, student: dict) -> None:
        print(
            "=========================\n"
            f"Student {student['name']}\n"
            f"Marks: {student['marks']}\n"
            f"Info: {student['info']}\n"
            "========================="
        )


    def update_student(self, id_: int, name: str = None, info: str = None) -> dict | None:
        student: dict | None = storage.get(id_)
        if student is None:
            return None

        if name:
            student["name"] = name

        if info:
            current_info = student["info"]

            if current_info.lower().strip() in info.lower().strip():
                student["info"] = info
            elif info.lower() in current_info.lower():
                student["info"] = info
            else:
                student["info"] = f"{current_info}. {info}"

        return student


    def add_mark(self, id_: int, raw_input: str) -> dict | None:
        if raw_input == "":
            return None

        raw_input = raw_input.replace(" ", "").split(",")

        if all([item.isdigit() for item in raw_input]):
            marks = [int(item) for item in raw_input]
            student: dict | None = storage.get(id_)

            if student is None:
                return None

            student["marks"] += marks
            return student

        else:
            print("Incorrect input of student marks")
            return None

# ─────────────────────────────────────────────────────────
# OPERATIONAL (APPLICATION) LAYER
# ─────────────────────────────────────────────────────────
def ask_student_payload() -> dict:
    name = input("Enter student's name: ")
    while not name:
        name = input("Student name is required. Please, enter the name again: ")

    row_marks = input("Enter student's marks separated by ','.\nIf the student has no marks, press Enter: ")
    details = input("Enter some detail information about student or press Enter: ")
    marks = [int(item) for item in row_marks.replace(" ", "").split(",")] if row_marks else []

    return {"name": name, "marks": marks, "info": details}


def ask_student_update():
    student_id: str = input("\nEnter student's ID: ")
    if not student_id:
        print("Student ID must be specified for update")
        return

    id_ = int(student_id)
    student: dict | None = storage.get(id_)
    if student is None:
        print(f"Student {student_id} not found")
        return

    show_student(student)

    return id_


def student_management_command_handle(command: str):
    students_service = StudentService()
    if command == "show":
        students_service.show_students()

    # elif command == "add":
    #     data = ask_student_payload()
    #     repo = Repository()
    #     repo.add_student(data)
    #     repo.students
    #
    #     if data:
    #         student: dict | None = add_student(data)
    #         if student is None:
    #             print("Error adding student")
    #         else:
    #             print(f"Student: {student['name']} is added")
    #     else:
    #         print("The student's data is NOT correct. Please try again")
    #
    # elif command == "search":
    #     student_id: str = input("\nEnter student's ID: ")
    #     if not student_id:
    #         print("Student's ID is required to search")
    #         return
    #
    #     students = get_storage()
    #
    #     student: dict | None = storage.get(int(student_id))
    #     if student is None:
    #         print("Error adding student")
    #     else:
    #         show_student(student_id, student)
    #
    # elif command == "delete":
    #     student_id: str = input("\nEnter student's ID: ")
    #     if not student_id:
    #         print("Student's id is required to delete")
    #         return
    #
    #     id_ = int(student_id)
    #     if storage.get(id_):
    #         del storage[id_]
    #
    # elif command == "update":
    #     id_ = ask_student_update()
    #     if id_:
    #         print(
    #             f"What information about student you want to update?\n"
    #             f"If NAME pres `N`, if INFO press `I`, if NAME and INFO press `A`.\n"
    #         )
    #
    #         user_input: str = input("Enter: ").upper()
    #
    #         if user_input == "N":
    #             new_name: str = input("Enter new student's name: ")
    #             updated_student: dict | None = update_student(id_=id_, name=new_name)
    #             print(f"Student {updated_student['name']} is updated")
    #         elif user_input == "I":
    #             new_info: str = input("Enter new student's info: ")
    #             updated_student: dict | None = update_student(id_=id_, info=new_info)
    #             print(f"Student {updated_student['name']} is updated")
    #         elif user_input == "A":
    #             new_name: str = input("Enter new student's name: ")
    #             new_info: str = input("Enter new student's info: ")
    #             updated_student: dict | None = update_student(id_=id_, name=new_name, info=new_info)
    #             print(f"Student {updated_student['name']} is updated")
    #         else:
    #             print("Error of choice")
    #     else:
    #         print("Error on updating student")
    #
    # elif command == "marks":
    #     id_ = ask_student_update()
    #     if id_:
    #         print(
    #             f"To add student grades, enter them separated by `,`"
    #         )
    #
    #         user_input: str = input("Enter: ")
    #         updated_student: dict | None = add_mark(id_=id_, raw_input=user_input)
    #         if updated_student:
    #             print(f"Student {updated_student['name']} is updated")
    #     else:
    #         print("Error on updating student marks")

# ─────────────────────────────────────────────────────────
# PRESENTATION LEVEL
# ─────────────────────────────────────────────────────────
def handle_user_input():
    OPERATIONAL_COMMANDS = ("quit", "help")
    STUDENT_MANAGEMENT_COMMANDS = ("show", "add", "search", "delete", "update", "marks")
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
