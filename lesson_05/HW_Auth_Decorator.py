"""
About the code:

`users` list includes multiple users (define them by yourself)
`command()` is only a single function that mimics the business logic
`auth()` is a decorator that requires user authorization to perform tasks


NOTES
"""

class User:
    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password

users = [
    User("Mark", "1234"),
    User("Harry", "qwer"),
    User("Marry", "1q2w")
]

def auth(func):
    authorized_user = {"user": None}

    def wrapper(*args, **kwargs):
        if not authorized_user["user"]:
            while True:
                username = input("Username: ")
                password = input("Password: ")
                for user in users:
                    if user.username == username and user.password == password:
                        authorized_user["user"] = user
                        print(f"Welcome, {user.username}!")
                        break
                if authorized_user["user"]:
                    break
                else:
                    print("Invalid credentials. Try again.\n")

        return func(*args, **kwargs)

    return wrapper


@auth
def command(payload):
    print(f"Executing command by authorized user.\nPayload: {payload}")

while user_input := input("Enter anything: "):
    command(user_input)