import json
import smtplib
import time
from collections import defaultdict
from threading import Thread
from email.mime.text import MIMEText
from datetime import date, datetime
from dateutil.relativedelta import relativedelta


class Mark:
    def __init__(self,
                 mark: int,
                 date: str = date.today().strftime('%d.%m.%Y')):
        if not isinstance(mark, int):
            raise TypeError
        if mark < 1 or mark > 12:
            raise ValueError
        self.mark: int = mark
        self.date: str = date

    def __str__(self):
        return f"{str(self.mark)}"


class Student:
    counter: int = 0

    def __init__(self, name: str, info: str = "", marks: list[Mark] | None = None):
        Student.counter += 1
        self.id = Student.counter
        self.name: str = name
        self.info: str = info
        self.marks: list[Mark] = marks if marks is not None else []

    def __str__(self):
        return (
            f"Student {self.id}: {self.name}\n"
            f"Marks: {', '.join(str(mark) for mark in self.marks)}\n"
            f"Info: {self.info}\n"
        )

    def add_mark(self, mark: int, date: str) -> None:
        if mark < 1 or mark > 12:
            print('Incorrect mark entered, must be integer from 1 to 12')
            return None
        return self.marks.append(Mark(mark, date))


class Repository:
    def __init__(self):
        self.students: dict[int, Student] = {}

    def __iter__(self):
        return iter(self.students.values())

    def __len__(self):
        return len(self.students)

    def __str__(self):
        return "\n".join(str(student) for student in self.students.values())

    def get_storage(self) -> dict[int, Student]:
        with open('students1000.json') as file:
            students_data = json.load(file)
        for student_data in students_data:
            student = Student(student_data['name'], student_data['info'])
            for mark in student_data['marks']:
                student.add_mark(mark['mark'], mark['date'])
            self.add_student(student)
        return self.students

    def update_storage(self) -> None:
        with open('students1000.json', 'w') as file:
            json.dump(
                [student.__dict__ for student in self.students.values()],
                file, indent=4, default=lambda o: o.__dict__)

    def get_student(self, student_id: int) -> Student | None:
        return self.students.get(student_id, None)

    def add_student(self, student: Student) -> Student:
        if student.id in self.students:
            print(f"Student with id {student.id} already exists.")
        else:
            self.students[student.id] = student
            self.update_storage()
        return student

    def update_student(self, id_: int, student: Student) -> None:
        self.students[id_] = student
        self.update_storage()
        print(f"Student {student.name} is updated")

    def delete_student(self, id_: int):
        name = self.students[id_].name
        del self.students[id_]
        self.update_storage()
        print(f"Student {name} is deleted")

    def add_mark(self, id_: int, mark: Mark) -> None:
        self.students[id_].marks.append(mark)
        self.update_storage()
        print(f"Student {self.students[id_].name} is updated")


class ReportService:
    def __init__(self, repo: Repository):
        self.repo = repo
        self.previous_month = date.today() - relativedelta(months=1)

    def generate_monthly_report(self) -> str:
        reporting_data = [f"Report for the last month ({self.previous_month.strftime('%B %Y')}):"]
        total_students = len(self.repo.students)
        if total_students == 0:
            report = "No students in the journal."
            reporting_data.append(report)
            return "\n".join(reporting_data)

        monthly_marks = []
        for student in self.repo.students.values():
            for mark in student.marks:
                if mark.date[3:5] == str(date.today().month - 1).zfill(2):
                    monthly_marks.append(mark)
                else:
                    continue

        total_marks = len(monthly_marks)
        average_mark = sum(mark.mark for mark in monthly_marks) / len(monthly_marks)

        reporting_data.append(f"Total students: {total_students}")
        reporting_data.append(f"Total marks: {total_marks}")
        reporting_data.append(f"Average mark: {average_mark:.2f}")

        dayly_marks = defaultdict(list)
        for mark in monthly_marks:
            dayly_marks[mark.date].append(mark.mark)
        for day, marks in sorted(dayly_marks.items()):
            average_mark = sum(marks) / len(marks) if marks else 0
            reporting_data.append(f"{day}: average mark = {average_mark:.2f}")

        return "\n".join(reporting_data)

    def create_report_message(self, body: str) -> MIMEText:
        message = MIMEText(body)
        message["Subject"] = f"Report ({self.previous_month.strftime('%B %Y')})"
        message["From"] = "sender@email.com"
        message["To"] = "recipient@email.com"
        return message


# ─────────────────────────────────────────────────────────
# OPERATIONAL (APPLICATION) LAYER
# ─────────────────────────────────────────────────────────
def ask_student_payload() -> Student | None:
    name = input("Enter student's name: ")
    while not name:
        name = input("Student name is required. Please, enter the name again: ")

    row_marks = input("Enter student's marks separated by ','.\nIf the student has no marks, press Enter: ")
    if row_marks:
        row_marks = row_marks.replace(" ", "").split(",")
        if all([item.isdigit() for item in row_marks]):
            marks = [Mark(int(item)) for item in row_marks]
        else:
            print("Incorrect input of student marks")
            return None
    else:
        marks = []

    info = input("Enter some information about student or press Enter: ")

    return Student(name, info, marks)


def student_management_command_handle(command: str):
    if command == "show":
        if not repo_students:
            print("There are no students in the journal\n")
            return
        print("\nStudents in the journal:\n")
        print(repo_students)

    elif command == "add":
        student_for_addition = ask_student_payload()
        if student_for_addition is None:
            print("Error on adding student.")
        else:
            repo_students.add_student(student_for_addition)
            print(f"Student: {student_for_addition.name} is added")

    elif command == "search":
        student_id: str = input("\nEnter student's ID: ")
        if not student_id:
            print("Student's ID is required to search")
            return
        if not student_id.isdigit():
            print("Student's ID must be a number")
            return
        student: Student | None = repo_students.get_student(int(student_id))
        if student is None:
            print("Error searching student. Non-existent ID entered.")
        else:
            print(student)

    elif command == "delete":
        student_id: str = input("\nEnter student's ID: ")
        if not student_id:
            print("Student's id is required to delete")
            return
        if not student_id.isdigit():
            print("Student's ID must be a number")
            return
        id_ = int(student_id)
        if repo_students.get_student(id_):
            repo_students.delete_student(id_)
        else:
            print("Error on deleting student")

    elif command == "update":
        student_id: str = input("\nEnter student's ID: ")
        if not student_id:
            print("Student's ID is required to update student information.")
            return
        if not student_id.isdigit():
            print("Student's ID must be a number")
            return
        id_ = int(student_id)
        student = repo_students.get_student(id_)
        if student:
            print(student)
            print(
                f"What information about student you want to update?\n"
                f"If NAME pres `N`, if INFO press `I`, if NAME and INFO press `A`.\n"
            )
            user_input: str = input("Enter: ").upper()

            if user_input == "N":
                student.name = input("Enter new student's name: ")
                repo_students.update_student(id_, student)
            elif user_input == "I":
                student.info = input("Enter new student's info: ")
                repo_students.update_student(id_, student)
            elif user_input == "A":
                student.name = input("Enter new student's name: ")
                student.info = input("Enter new student's info: ")
                repo_students.update_student(id_, student)
            else:
                print("Error of choice")
        else:
            print("Error on updating student")

    elif command == "add mark":
        student_id: str = input("\nEnter student's ID: ")
        if not student_id:
            print("Student's id is required to update student marks.")
            return
        if not student_id.isdigit():
            print("Student's ID must be a number")
            return
        id_ = int(student_id)
        student = repo_students.get_student(id_)
        if student:
            print(student)
            try:
                mark: Mark = Mark(int(input("Enter new mark: ")))
            except ValueError or TypeError:
                print("Mark must be an integer from 1 to 12")
                return
            else:
                repo_students.add_mark(id_, mark)
                print(f"Mark {mark} is added to student {student.name}")
        else:
            print("Error on adding mark. Student not found.")


# ─────────────────────────────────────────────────────────
# PRESENTATION LEVEL
# ─────────────────────────────────────────────────────────
def handle_user_input():
    OPERATIONAL_COMMANDS = ("quit", "help")
    STUDENT_MANAGEMENT_COMMANDS = ("show", "add", "search", "delete", "update", "add mark")
    AVAILABLE_COMMANDS = (*OPERATIONAL_COMMANDS, *STUDENT_MANAGEMENT_COMMANDS)

    HELP_MESSAGE = (
        "\nHello in the `Digital Journal Applicationl`! Use the menu to interact with the application.\n"
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


def send_email(repo: Repository):
    report_service = ReportService(repo)
    sent_month = None

    while True:
        now = datetime.now()
        if now.day == 1 and now.month != sent_month:
            report = report_service.generate_monthly_report()
            message = report_service.create_report_message(report)
            server = smtplib.SMTP(host="localhost", port=1025)
            server.send_message(
                msg=message,
                from_addr="sender@email.com",
                to_addrs=["recipient@email.com"]
            )
            server.quit()
            print(f"Monthly report sent on {now.strftime('%Y-%m-%d %H:%M:%S')}")
            sent_month = now.month
            time.sleep(60 * 60 * 12)
        else:
            time.sleep(60 * 60)

        # Uncomment the following lines to send a report every 2 minutes
        # now = datetime.now()
        # if now.minute % 2 == 0:
        #     report = report_service.generate_monthly_report()
        #     message = report_service.create_report_message(report)
        #     server = smtplib.SMTP(host="localhost", port=1025)
        #     server.send_message(
        #         msg=message,
        #         from_addr="sender@email.com",
        #         to_addrs=["recipient@email.com"]
        #     )
        #     server.quit()
        #     print(f"\n\tMonthly report sent on {now.strftime('%Y-%m-%d %H:%M:%S')}")
        #     time.sleep(60)
        # else:
        #     time.sleep(30)


# ─────────────────────────────────────────────────────────
# ENTRYPOINT
# ─────────────────────────────────────────────────────────
if __name__ == '__main__':
    repo_students = Repository()
    repo_students.get_storage()
    thread1 = Thread(target=handle_user_input)
    thread2 = Thread(target=send_email, args=(repo_students,), daemon=True)
    thread1.start()
    thread2.start()
