# StudentID:	p2008493
# Name:	        Ng Jun Han
# Class:		DISM/FT/1B/05   
# Assessment:	CA1 
# 
# Script name:	server.py
# 
# Purpose:	The purpose of the script is for the user to retrieve the quiz settings, question pool, and user data without needing
#           to have the files downloaded onto the user's computer. With the script managing all the request that is coming from the 
#           client user.
#
# Usage syntax:	Run with play button / command line, eg. py read-cmd-line 1 2 3
# 
# Input file:   C:\PSEC_project\courses.json
#               C:\PSEC_project\quiz_settings.json
#               C:\PSEC_project\users.json
#               C:\PSEC_project\quiz_results.csv
# 
# Output file:  C:\PSEC_project\users.json
#               C:\PSEC_project\quiz_results.csv
# 
# Python ver:	Python 3
#
# Reference:	This program is adapted from the following:
#                   a) Socket Programming with Multi-Threading in Python
#                   https://www.tutorialspoint.com/socket-programming-with-multi-threading-in-python
# 
#                   
# Library/
# package/	
# Module /      sys, socket, traceback, threading, json, csv
#
# Known issues:	N/A

import sys
import socket
import traceback
import threading
import json
import csv

HOST = "127.0.0.1"
PORT = 8181

_USERNAME_AND_PASSWORD = "./server/users.json"   # Stored as a list
_QUIZ_SETTING = "./server/quiz_settings.json"    # Stored as a dict
_QUESTION_POOL = "./server/question_pool.json"    # Stored as a list
_QUIZ_RESULTS = "./server/quiz_results.csv"      # Stored as a csv

def main():
    start_server(HOST, PORT)

# Reads and empties value into "dictionary" variable
# "option" parameter used to define what format it should print in
def read_file(file: str, option):
    if option == "csv":
        csv_file_content = []
        with open(file, 'r') as csvfile:
            # Uses DictReader for easy storing of the value
            for line in csv.DictReader(csvfile):
                csv_file_content.append(dict(line))
        
        return csv_file_content
    elif option == "json":
        # Loading of JSON file into the program
        with open(file,"r") as f:
            file_content = json.load(f)
        return file_content

def start_server(host, port):
    print("[STARTING] Server is starting...")
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    try:
        server.bind((host, port))
    except:
        print("Bind failed. Error : " + str(sys.exc_info()))
        sys.exit()
    server.listen(6) # listening up to 6 different clients
    print("[LISTENING] Socket now listening")
    # infinite loop- do not reset for every requests
    while True:
        connection, address = server.accept()   # Server would wait here until a new connection is received
        ip, port = str(address[0]), str(address[1])
        print(f"[NEW CONNECTION] Connected with {ip}:{port}")
        try:
            # Server attempts to start a thread with target function "clientThread()"
            thread = threading.Thread(target=clientThread, args=(connection, ip, port))
            thread.start()
        except:
            print("Thread did not start.")
            traceback.print_exc()

# Handler for client machine
def clientThread(connection, ip, port, max_buffer_size = 5120):
    is_active = True
    while is_active:
        client_input = receive_input(connection, max_buffer_size)
        if client_input == "quit":
            # Closes the connection of current thread
            connection.close()
            print(f"[CLOSED] Connection with {ip}:{port} closed")
            is_active = False
        else:
            # Send the message after dumping it and encoding it.
            connection.sendall(json.dumps(client_input).encode("utf8"))  
            print(f"[PROCESS] {ip}:{port}, Packet type: '{client_input['type']}'")

def receive_input(connection, max_buffer_size):
    client_input = connection.recv(max_buffer_size)
    decoded_input = client_input.decode("utf8")
    result = process_input(decoded_input)
    return result

def process_input(client_request):
    client_request = json.loads(client_request)
    match client_request['type']:
        case "quit":
            response = "quit"
        case "add_user":
            pass
        case "user_login":
            server_response = check_credentials(client_request)
            if server_response == True:
                response = {
                    "type": "Login Success"
                    }
            else:
                response = {
                    "type": "Login Failed"
                }
        case "reset_password":
            response = {
                "type": "Reset Password"
            }
        case "quiz_settings":
            pass
        case "question_pool":
            pass
    return response

# Checks the userID and password against the files
def check_credentials(client_request):
    server_user_files = read_file(_USERNAME_AND_PASSWORD, "json")
    for element in server_user_files:
        if check_userID(element, client_request) and check_password(element, client_request):
            print(f"[PROCESS] {element['userID']} Login Successful")
            return True
    return False

def check_userID(server_files, client_request):
    if server_files['userID'] == client_request['userID']:
        return True
    return False

def check_password(server_files, client_request):
    if server_files['password_SHA256'] == client_request['password']:
        return True
    return False

if __name__ == "__main__":
    main()
