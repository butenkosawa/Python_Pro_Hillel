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
    raise NotImplementedError


def represent_student():
    raise NotImplementedError


def ask_student_payload():
    raise NotImplementedError


def handle_command():
    raise NotImplementedError


handle_command("show")
handle_command("add")
handle_command("show")
