"""
User -> login
User -> password
"""


user = {
    "name": "John",
    "login": "john",
    "password": "1234"
}


authenticated = False

login = input("enter login: ")
password = input("enter password: ")

if login == user["login"] and password == user["password"]:
    authenticated = True


if not authenticated:
    login = input("enter login: ")
    password = input("enter password: ")

    if login == user["login"] and password == user["password"]:
        authenticated = True

if not authenticated:
    login = input("enter login: ")
    password = input("enter password: ")

    if login == user["login"] and password == user["password"]:
        authenticated = True

if not authenticated:
    login = input("enter login: ")
    password = input("enter password: ")

    if login == user["login"] and password == user["password"]:
        authenticated = True

if not authenticated:
    login = input("enter login: ")
    password = input("enter password: ")

    if login == user["login"] and password == user["password"]:
        authenticated = True

