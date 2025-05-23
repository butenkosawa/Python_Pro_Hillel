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
        "id": 1,
        "name": "John Doe",
        "marks": [4, 12, 8, 9, 9, 10, 11],
        "info": "John is 19 y.o. Interest: boxing",
    },
    {
        "id": 2,
        "name": "Marry Black",
        "marks": [9, 12, 8, 4, 1, 9, 7],
        "info": "John is 19 y.o. Interest: music"
    },
    {
        "id": 3,
        "name": "Alice Smith",
        "marks": [2, 11, 8, 10, 3, 4, 12],
        "info": "Alice is 18 y.o. Interest: reading"
    },
    {
        "id": 4,
        "name": "Bob Johnson",
        "marks": [5, 7, 12, 6, 8, 10, 9],
        "info": "Bob is 20 y.o. Interest: swimming"
    },
    {
        "id": 5,
        "name": "Charlie Davis",
        "marks": [9, 4, 6, 11, 12, 5, 8],
        "info": "Charlie is 17 y.o. Interest: coding"
    },
    {
        "id": 6,
        "name": "Diana Evans",
        "marks": [7, 6, 12, 9, 1, 2, 10],
        "info": "Diana is 21 y.o. Interest: football"
    },
    {
        "id": 7,
        "name": "Ethan Foster",
        "marks": [10, 8, 6, 5, 7, 3, 9],
        "info": "Ethan is 19 y.o. Interest: chess"
    },
    {
        "id": 8,
        "name": "Bob Johnson",
        "marks": [3, 5, 9, 11, 12, 7, 4],
        "info": "Fiona is 20 y.o. Interest: music"
    },
    {
        "id": 9,
        "name": "George Harris",
        "marks": [6, 10, 8, 9, 2, 11, 1],
        "info": "George is 18 y.o. Interest: hiking"
    },
    {
        "id": 10,
        "name": "Hannah Irving",
        "marks": [11, 2, 4, 6, 7, 8, 12],
        "info": "Hannah is 17 y.o. Interest: photography"
    },
    {
        "id": 11,
        "name": "Ian Jackson",
        "marks": [8, 12, 7, 9, 10, 4, 3],
        "info": "Ian is 21 y.o. Interest: gaming"
    },
    {
        "id": 12,
        "name": "Julia King",
        "marks": [1, 6, 8, 12, 5, 11, 9],
        "info": "Julia is 20 y.o. Interest: basketball"
    }
]


# CRUD
def add_student(student: dict):
    new_id = max([student["id"] for student in storage], default=0) + 1
    student["id"] = new_id
    storage.append(student)
    return student


def show_students():
    print("==========================\n")
    for student in storage:
        print(f"{student['id']}. Student: {student['name']}\n")
    print("==========================")


def search_student(student_id: int) -> None:
    for student in storage:
        if student["id"] == student_id:
            print(
                "==========================\n"
                f"{student['id']}. Student: {student['name']}\n"
                f"Marks: {student['marks']}\n"
                f"Info: {student['info']}\n"
                "=========================="
            )
            return

    print(f"Student with ID {student_id} NOT found.")


def ask_student_payload():
    name = input("Enter student's name: ")
    while not name:
        name = input("Student name is required. Please, enter the name again: ")

    row_marks = input("Enter student's marks separated by ','.\nIf the student has no marks, press Enter: ")
    details = input("Enter some detail information about student or press Enter: ")
    marks = [int(item) for item in row_marks.replace(" ", "").split(",")] if row_marks else []

    return {"name": name, "marks": marks, "info": details}


def student_management_command_handle(command: str):
    if command == "show":
        show_students()
    elif command == "add":
        data = ask_student_payload()
        student: dict = add_student(data)
        print(f"\nStudent {student['name']} added with ID {student['id']}")
    elif command == "search":
        student_id: str = input("\nEnter student's ID: ")
        if student_id:
            search_student(student_id=int(student_id))
        else:
            print("Student's ID is required to search.")


def main():
    OPERATIONAL_COMMANDS = ("quit", "help")
    STUDENT_MANAGMENT_COMMANDS = ("show", "add", "search")
    AVAILADLE_COMMANDS = (*OPERATIONAL_COMMANDS, *STUDENT_MANAGMENT_COMMANDS)
    HELP_MESSAGE = (
        "Hello in the Jornal! Use the menu to interact with the application.\n"
        f"Available commands: {AVAILADLE_COMMANDS}"
    )

    print(HELP_MESSAGE)

    while True:
        command = input("\n Select command: ")

        if command == "quit":
            print("\nThanks for using Jornal application.")
            break
        elif command == "help":
            print(HELP_MESSAGE)
        else:
            student_management_command_handle(command)


if __name__ == '__main__':
    main()
