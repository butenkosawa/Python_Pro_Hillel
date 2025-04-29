"""
1. Application - Python
2. User - Teacher in the school
3. Interface - TUI (Terminal User Interface)


struct Student:
    name: str
    marks: list[int]

struct Teacher: no structure since authentication process
"""

storage = [
    {
        "name": "John Doe",
        "marks": [4, 12, 8, 9, 9, 10, 11]
    },
    {
        "name": "Marry Black",
        "marks": [9, 12, 8, 4, 1, 9, 7]
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


def represent_student():
    for student in storage:
        info = (
            "==========================\n"
            f"Student: {student['name']}\n"
            f"Marks: {student['marks']}"
        )

        print(info)


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


def handle_command(command: str):
    if command == "show":
        represent_student()
    elif command == "add":
        data = ask_student_payload()
        if data:
            student: dict = add_student(data)
            print(f"Student {student['name']} is added")
        else:
            print("The student's data is NOT correct. Please try again.")


if __name__ == '__main__':
    handle_command("show")
    handle_command("add")
    handle_command("show")
