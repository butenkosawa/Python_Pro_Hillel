"""
1. Application - Python
2. User - Teacher in the school
3. Interface - TUI (Terminal User Interface)


struct Student:
    name: str
    marks: list[int]

struct Teacher: no structure since authentication process
"""

storage: list[dict] = [
    {
        "name": "John Doe",
        "marks": [4, 12, 8, 9, 9, 10, 11],
        "info": "John is 19 y.o. Interest: boxing",
    },
    {
        "name": "Marry Black",
        "marks": [9, 12, 8, 4, 1, 9, 7],
        "info": "John is 19 y.o. Interest: music"
    },
    {
        "name": "Alice Smith",
        "marks": [2, 11, 8, 10, 3, 4, 12],
        "info": "Alice is 18 y.o. Interest: reading"
    },
    {
        "name": "Bob Johnson",
        "marks": [5, 7, 12, 6, 8, 10, 9],
        "info": "Bob is 20 y.o. Interest: swimming"
    },
    {
        "name": "Charlie Davis",
        "marks": [9, 4, 6, 11, 12, 5, 8],
        "info": "Charlie is 17 y.o. Interest: coding"
    },
    {
        "name": "Diana Evans",
        "marks": [7, 6, 12, 9, 1, 2, 10],
        "info": "Diana is 21 y.o. Interest: football"
    },
    {
        "name": "Ethan Foster",
        "marks": [10, 8, 6, 5, 7, 3, 9],
        "info": "Ethan is 19 y.o. Interest: chess"
    },
    {
        "name": "Fiona Green",
        "marks": [3, 5, 9, 11, 12, 7, 4],
        "info": "Fiona is 20 y.o. Interest: music"
    },
    {
        "name": "George Harris",
        "marks": [6, 10, 8, 9, 2, 11, 1],
        "info": "George is 18 y.o. Interest: hiking"
    },
    {
        "name": "Hannah Irving",
        "marks": [11, 2, 4, 6, 7, 8, 12],
        "info": "Hannah is 17 y.o. Interest: photography"
    },
    {
        "name": "Ian Jackson",
        "marks": [8, 12, 7, 9, 10, 4, 3],
        "info": "Ian is 21 y.o. Interest: gaming"
    },
    {
        "name": "Julia King",
        "marks": [1, 6, 8, 12, 5, 11, 9],
        "info": "Julia is 20 y.o. Interest: basketball"
    }
]


# CRUD
def add_student(student: dict):
    if len(student) != 2:
        return None

    if not student.get("name") or not student.get("marks"):
        return None
    else:
        storage.append(student)
        return student


def show_students():
    print("==========================\n")
    for index, student in enumerate(storage, 1):
        print(f"{index}. Student: {student['name']}\n")
    print("==========================\n")


def search_student(student_name: str) -> None:

    for student in storage:
        info = (
            "==========================\n"
            f"Student: {student['name']}\n"
            f"Marks: {student['marks']}\n"
            f"Info: {student['info']}\n"
            "==========================\n"
        )

        if student["name"] == student_name:
            print(info)
            return

    print(f"Student {student_name} NOT found.")


def ask_student_payload():
    ask_prompt = (
        "Enter student's payload data using text template: "
        "John Doe;1,2,3,4,5\n"
        "where 'John Doe' is a full name and [1,2,3,4,5] are marks.\n"
        "The data must be separated by ';'\n"
    )

    def parse(data) -> dict | None:
        name, row_marks = data.split(';')
        return {
            "name": name,
            "marks": [int(item) for item in row_marks.replace(" ", "").split(",")]
        }

    user_data: str = input(ask_prompt)
    return parse(user_data)


def student_management_command_handle(command: str):
    if command == "show":
        show_students()
    elif command == "add":
        data = ask_student_payload()
        if data:
            student: dict = add_student(data)
            print(f"Student {student['name']} is added")
        else:
            print("The student's data is NOT correct. Please try again.")
    elif command == "search":
        name = input("\nEnter student's name: ")
        if name:
            search_student(student_name=name)
        else:
            print("Student's name is required to search.")


def handle_user_input():
    OPERATIONAL_COMMANDS = ("quit", "help")
    STUDENT_MANAGMENT_COMMANDS = ("show", "add", "search")
    AVAILADLE_COMMANDS = (*OPERATIONAL_COMMANDS, *STUDENT_MANAGMENT_COMMANDS)
    HELP_MESSAGE = (
        "Hello in the Jornal! Use the menu to interact with the application.\n"
        f"Available commands: {AVAILADLE_COMMANDS}"
    )

    print(HELP_MESSAGE)

    while True:
        command = input("Select command: ")

        if command == "quit":
            print("\nThanks for using Jornal application.")
            break
        elif command == "help":
            print(HELP_MESSAGE)
        else:
            student_management_command_handle(command)


if __name__ == '__main__':
    handle_user_input()
    # handle_command("show")
    # handle_command("add")
    # handle_command("show")
