import enum


class Role(enum.StrEnum):
    STUDENT = enum.auto()
    TEACHER = enum.auto()


class User:
    def __init__(self, name: str, email: str, role: Role) -> None:
        self.name = name
        self.email = email
        self.role = role

    def send_notification(self, notification):
        print(f'Sending message from {self.name} ({self.role})')
        print(notification)
        print('-' * 40)


class Notification:
    def __init__(self, subject: str, message: str, attachment: str = "") -> None:
        self.subject = subject
        self.message = message
        self.attachment = attachment  # Optional extra info

    def __str__(self):
        output = f'Subject: {self.subject}\nMessage: {self.message}'
        if self.attachment:
            output += f'\nAttachment: {self.attachment}'
        return output


class StudentNotification(Notification):
    def __str__(self):
        return super().__str__() + f'\nNote: Sent via Student Portal'


class TeacherNotification(Notification):
    def __str__(self):
        return super().__str__() + f"\nNote: Teacher's Desk Notification"


def main():
    student = User('Mark Black', 'mark@mail.com', Role.STUDENT)
    teacher = User('Marry White', 'marry_tch@post.school.com', Role.TEACHER)

    student_notification = StudentNotification(
        subject='Home work',
        message='Some comments to home work',
        attachment='task1.txt'
    )
    teacher_notification = TeacherNotification(
        subject='Home work lesson 1',
        message='Deadline for HW: 12/12/2025'
    )

    student.send_notification(student_notification)
    teacher.send_notification(teacher_notification)


if __name__ == "__main__":
    main()
