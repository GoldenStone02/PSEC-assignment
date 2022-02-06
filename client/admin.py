# StudentID:	p2008493
# Name:	        Ng Jun Han
# Class:		DISM/FT/1B/05   
# Assessment:	CA1 
# 
# Script name:	admin.py
# 
# Purpose:	The purpose of the script is to allow an administrator to edit and change the settings within 
#           the files without having to manual search through every file to find the correct setting
#           or text to change. The administrator can also get the data about student performance within the quiz
#           and other statistical data for analysis.
#
# Usage syntax:	Run with play button / command line, eg. py read-cmd-line 1 2 3
# 
# Input file:   C:\PSEC_project\question_pool.json
#               C:\PSEC_project\quiz_settings.json
#               C:\PSEC_project\quiz_results.csv
# 
# Output file:  C:\PSEC_project\question_pool.json
#               C:\PSEC_project\quiz_settings.json
#               C:\PSEC_project\quiz_results.csv
# 
# Python ver:	Python 3
#
# Reference:	This program is adapted from the following:
#               a) GeeksforGeeks - Use of regex to filter out text
#               https://www.geeksforgeeks.org/check-if-a-string-contains-uppercase-lowercase-special-characters-and-numeric-values/
# 
#               b) hashlib - Python Documentation
#               https://docs.python.org/3/library/hashlib.html 
# 
#               c) w3schools - Python Dictionary values() method
#               https://www.w3schools.com/python/ref_dictionary_values.asp
#  
# Library/
# package/	
# Module /      sys, socket, traceback, os, re, csv, hashlib, json, getpass
#
# Known issues:	N/A
#

import sys, socket, traceback
import os
import re
import csv
import hashlib
import getpass
import json

# ==================================================================
#   Initialize Variables
# ==================================================================

dictionary = {}

# Used for the dynamic spacing for the UI
EMPTY = ""

PATTERN = r"^[\w]+$"
EMAIL_PATTERN = r"([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)"
PASSWORD_PATTERN = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%]).+$'

MAIN_MENU = ["User Configuration", "Question Pool","Quiz Settings", "Generate Report"]

_USERNAME_AND_PASSWORD = "./server/users.json"   # Stored as a list
_QUIZ_SETTING = "./server/quiz_settings.json"    # Stored as a dict
_QUESTION_POOL = "./server/question_pool.json"    # Stored as a list
_QUIZ_RESULTS = "./server/quiz_results.csv"      # Stored as a csv

# ==================================================================
#   Socket Programming Functions
# ==================================================================

HOST = "127.0.0.1"
PORT = 8181

# Steps to receive and process the server's response
def server_process(packet_input: dict) -> any:
    '''
    This function connect, sends and receives data from the server,
    then process the data.

    Args:
        packet_input (dict) : Packet to be sent to server.
    
    Returns:
        processed_input (any) : Returns either the data processed or the raw data.
    '''
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  
    connect_to_server(client)
    server_response = send_to_server(packet_input, client)
    exit_server(client)
    processed_input = process_input(server_response)
    return processed_input

def connect_to_server(client):
    '''
    This function attempts to connect to socket server.

    Args:
        client (obj) : Client socket object.
    '''
    try:
        client.connect((HOST, PORT))
    except:
        print("Connection Error")
        print(traceback.format_exc())
        sys.exit()
    print(f"[CONNECTION ESTABLISHED] Connected to {HOST}:{PORT}")

def send_to_server(packet: dict, client) -> dict:
    '''
    This function sends a packet to socket server.

    Args:
        packet (dict) : Packet to be sent to server.
        client (obj): Client socket object.
    
    Returns:
        received_message (dict): Raw server response.
    '''
    connected = True
    while connected:
        if len(packet) > 0:
            client.sendall(json.dumps(packet).encode("utf8"))
        else:
            print("Message can't be empty")
            continue    # Skips the bottom commands
        connected = False
        received_message = json.loads(client.recv(10000))
        print(f"[PROCESS] {HOST}:{PORT}, Packet type: {received_message['type']}")
        return received_message

# Sends a quit packet to close the connection
def exit_server(client):
    '''
    This function sends the server a quit packet to terminate the connection.

    Args:
        client (obj) : Client socket object.
    '''
    quit_connection = {"type":"quit"}
    client.sendall(json.dumps(quit_connection).encode("utf8"))
    print(f"[EXITED] Connection to {HOST}:{PORT} Exited")

# Processes the server_response 
def process_input(server_response: dict) -> any:
    '''
    This function processes the server's response and returns the data segment of the packet.

    Args:
        server_response (dict) : Server's response to client .
    
    Returns:
        output (any) : Outputs the data segment of the packet.
    '''
    output = None
    match server_response['type']:
        case "user_successfully_added":
            output = True

        case "user_already_exist":
            output = False

        case "updated_user_config":
            output = True

        case "returned_admin_quiz_setting":
            output = server_response['data']

        case "updated_quiz_setting":
            output = True

        case "returned_file_data":
            output = server_response['data']

        case "returned_admin_specific_settings":
            output = server_response['data']

        case "available_courses":
            output = server_response['data']

        case "returned_admin_question_pool":
            output = server_response['data']

        case "update_admin_question_pool":
            output = True

        case "previous_attempts":
            output = server_response['data']

        case _:
            print(server_response)
            input("Error")
    return output

# ==================================================================
#   General Functions
# ==================================================================

def get_input(user_input: str, visible_input: bool = True) -> str:
    '''
    This function basically clears the command line before requesting an input
    from the user.

    Args:
        user_input (str) : Used as a string for the input.
        visible_input (bool) : Allows user to see what they are typing. If True,
        text will be visible. Else, text will be hidden. (Default - True)
    
    Returns:
        output (str) : Returns the user inputted string.
    '''
    os.system("cls")
    if visible_input:
        output = input(user_input)
    else:
        output = getpass.getpass(user_input)
    return output

# Reads and empties value into "dictionary" variable
def read_file(file: str, option: str):
    '''
    Returns file content of the inputted file after reading it.

    Args:
        file (str) : Input file path.
        option (str) : Format it should read the file.
    Returns:
        (list or dict) : Returns the data of the file.
    '''
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


# Writes changes to the selected file
# "file_path" is the input file path that you want to edit
# "option" is the method of which you want to write to the file
# "input_variable" written into the file
def write_to_file(file_path: str, option: str, input_variable: any):
    # # Writes items into csv file 
    # Writes whatever that's in the "input_variable" onto the specified file 
    if option == "json":
        with open(file_path, "w") as f:
            json.dump(input_variable, f, indent=4)
    # Edits question pool from the question pool json file
    elif option == "edit_question":
        question_pool = read_file(file_path, option="json")
        for each_course in question_pool:
            for each_module in each_course['modules']:
                for each_topic in each_module['topics']:
                    if each_topic['topic_name'] == input_variable['topic']:
                        each_topic['questions'] = input_variable['questions']
        with open(file_path, "w") as f:
            json.dump(question_pool, f, indent=4)
        return
    elif option == "edit_course":
        question_pool = read_file(file_path, option="json")
        for each_course in question_pool:
            if each_course['course'] == input_variable:
                question_pool.remove(each_course)

# Returns the file content of "input_file_path"
def view_file_content(show_numbers: int, option: str, check=None):
    '''
    This function returns the file content from input_file_path.

    Args:
        show_numbers (int) : Enables sequence numbering in returned string.
            0 : Disables numbering.
            1 : Enables numbering.
        option (str) : Method to format the string.
        check (any) : Used for additional inputs. (Default = None)
    
    Returns:
        content (str) : Outputs the formatted strings.
    '''
    content = ""
    # Get the file information
    if option in ["course", "module", "topic", "question"]:
        packet = {"type": "admin_fetch_question_pool", "file": option}
        if check != None:
            packet.update(check)
        file_dictionary = server_process(packet)
        # Uses the data portion of the packet
        file_dictionary = file_dictionary['data']
    else:
        file_dictionary = server_process({"type": "admin_read_file", "file": option})

    if show_numbers == 1:
        match option:
            # Formats dictionary for settings with numbering
            case "setting":
                for i, item in enumerate(file_dictionary[check]):
                    if type(file_dictionary[check][item]) == list:
                        string = ""
                        for topic in file_dictionary[check][item]:
                            string += f"\n\t- \033[4;31;40m{topic['topic_name']}\033[0;37;40m" 
                        content += f"[ {i + 1} ] {item}: {string}\n"
                    else:
                        content += f"[ {i + 1} ] {item}: \033[4;31;40m{file_dictionary[check][item]}\033[0;37;40m\n"
            # Formats dictionary for users with numbering
            case "user":
                for i, item in enumerate(file_dictionary):
                    content += f"[ {i + 1} ] \033[4;31;40m{item['userID']}\033[0;37;40m\t|  {item['email']}\t\n" 
            
            # Formats dictionary for courses with numbering
            case "course":
                for i, item in enumerate(file_dictionary):
                    content += f"[ {i + 1} ] {item['course']}\n"
            
            # Formats dictionary for modules with numbering
            case "module":
                for i, item in enumerate(file_dictionary):
                    content += f"[ {i + 1} ] {item['module']}\n"
            
            # Formats dictionary for topics with numbering
            case "topic":
                for i, item in enumerate(file_dictionary):
                    content += f"[ {i + 1} ] {item['topic']}\n"

            # Formats dictionary for question with numbering
            case "question":
                print(file_dictionary)
                for i, item in enumerate(file_dictionary): 
                    sample = ""
                    for j, option in enumerate(item['options']):
                        sample += f"\n\t{chr(97 + j)}) {option}"
                    content += f"[ {i + 1} ] {item['question']}: {sample}\n\n\tCorrect Option: {item['correct_option']}\n\n"
    elif show_numbers == 0:
        match option:
            # Formats dictionary for settings w/o numbering
            case "setting":
                if check == "all_quiz":
                    content += "\tCourse\t|\tModule\t|\tQuiz\n"
                    content += f"{divider()}\n"
                    for element in file_dictionary:
                        content += f"[ - ]   {element['course']}\t|\t{element['module_name']}\t|\t{element['quiz_name']}\n"
                else:
                    for item in file_dictionary[check]:
                        if type(file_dictionary[check][item]) == list:
                            string = ""
                            for topic in file_dictionary[check][item]:
                                string += f"\n\t- \033[4;31;40m{topic['topic_name']}\033[0;37;40m" 
                            content += f"[ - ] {item}: {string}\n"
                        else:
                            content += f"[ - ] {item}: \033[4;31;40m{file_dictionary[check][item]}\033[0;37;40m\n"
            # Formats dictionary for users w/o numbering
            case "user":
                for item in file_dictionary:
                    content += f"[ - ] \033[4;31;40m{item['userID']}\033[0;37;40m\t|  {item['email']}\t\n" 
    
            # Formats dictionary for courses w/o numbering
            case "course":
                for item in file_dictionary:
                    content += f"[ - ] {item['course']}\n"
            
            # Formats dictionary for courses w/o numbering
            case "module":
                for item in file_dictionary:
                    content += f"[ - ] {item['module']}\n"
            
            # Formats dictionary for courses w/o numbering
            case "topic":
                for item in file_dictionary:
                    content += f"[ - ] {item['topic']}\n"

            # Formats dictionary for question w/o numbering
            case "question":
                for item in file_dictionary: 
                    sample = ""
                    for j, option in enumerate(item['options']):
                        sample += f"\n\t{chr(97 + j)}) {option}"
                    content += f"[ - ] {item['question']}: {sample}\n\n\tCorrect Option: {item['correct_option']}\n\n"
    return content

# Validates the input to ensure its in a proper format
def validation(user_input: any, expected_output: str, max_value: int = None) -> bool:
    '''
    This function is used to validate user_input 
    and ensure that it goes along with the expected_output.

    Args:
        user_input (any) : Value to be checked.
        expected_output (str) : The expected value or format type whenever validating. 
        (optional) int_check (int) : The maximum range the user_input can reach. 
        Expected output needs to be "int" to work. (Default - None)
    
    Returns:
        (bool) : If error was detected, return True. Else, return False
    '''
    if user_input == "":
        error_output("empty_input")
        return True # Immediately exits if any error is detected
    match expected_output:
        case "str":
            if user_input.isdigit():
                error_output("input")
                return True
            elif not re.search(PATTERN, user_input): # If there are any special symbols
                error_output("special")
                return True
        case "int":
            if user_input.isalpha():
                error_output("input")
                return True
            elif not re.search(PATTERN, user_input):
                error_output("special")
                return True
            elif max_value:
                if int(user_input) <= 0 or int(user_input) > int(max_value):
                    error_output("max")
                    return True
        case "email":
            if not re.search(EMAIL_PATTERN, user_input):
                error_output("email")
                return True
        case "password":
            if not re.search(PASSWORD_PATTERN, user_input):
                error_output("password")
                return True
        case _:
            pass
    return False

# Prints the text file with some UI.
# Needs to happen after "read_file()" has been executed
def print_menu(option_name: str, check=None): 
    '''
    This functions prints out selected file with a UI.

    Args:
        option_name (str) : Used to select the file to read from.
        check (any): Used for additional inputs. (Default = None)
    '''
    content = f"{divider()}\n\t\t\033[1;37;40m {option_name.capitalize()}\033[0;37;40m\n{divider()}\n"
    content += view_file_content(0, option_name, check)
    content += f"{divider()}\n\tSelect one to edit.\n{divider()}\n"
    content += f"[ 1 ] Add New {option_name.capitalize()}\n[ 2 ] Edit {option_name.capitalize()}\n[ 3 ] Delete {option_name.capitalize()}\n[ X ] Back to Main\n{divider()}\n"
    user_input = get_input(content)
    return user_input

# Used for easy maintainence of error outputs
def error_output(error_type: str, optional=None):
    '''
    This function proccesses error_type and return an error message.

    Args:
        error_type (str) : type of error (Default - None).
    '''
    match error_type:
        case "option":             # Wrong option selected
            string = "\033[1;37;41mPlease select a valid option.\033[0;37;40m\n"

        case "empty_input":        # Empty input
            string = f"\033[1;37;41mEmpty input, please try again\033[0;37;40m\n"

        case "range":
            string = f"\033[1;37;41mPlease that is within the range.\033[0;37;40m\n"

        case "input":              # Invalid input
            string = "\033[1;37;41mPlease enter a valid input\033[0;37;40m\n"

        case "max":                # Maximum value exceeded                        [Unique to admin.py]
            string = "\033[1;37;41mThe value you entered exceeded the maximum integer value!\033[0;37;40m\n"

        case "empty_assessment":   # Empty component                                [Unique to admin.py]
            string = "\033[1;37;41mPlease enter an topic for the assessment component\033[0;37;40m\n"

        case "duplicate":          # Duplicate entry                               [Unique to admin.py]
            string = "\033[1;37;41mDuplicate entry, please try again\033[0;37;40m\n"

        case "special":            # Input field can't contain special characters  [Unique to admin.py]
            string = "\033[1;37;41mInput value can't contain special characters!\033[0;37;40m\n"

        case "short":              # Input value was too short         
            string = "\033[1;37;41mLength of input was too short\033[0;37;40m\n"

        case "long":               # Input value was too long           
            string = "\033[1;37;41mLength of input was too long\033[0;37;40m\n"
        
        case "username_match":     # Same username is found in the database        
            string = "\033[1;37;41mUsername exists already, please try another name\033[0;37;40m\n"

        case "letter":             # Input value must contain letters              [Unique to admin.py]
            string = "\033[1;37;41mMust have at least one uppercase and lowercase character\033[0;37;40m\n"

        case "password":           # Doesn't meet the password criteria  
            string = "\033[1;37;41mMissing one of the criteria listed below, please try again\033[0;37;40m\nAt least one number\nAt least one uppercase and one lowercase character\nAt least one special symbol !@#$%\nShould be 4 - 20 characters long\n"
        
        case "email":              # Email in wrong format                         [Unique to admin.py]
            string = "\033[1;37;41mFormat of email was incorrect, please try again\033[0;37;40m\n"

        case "course":             # Course not found in database                  [Unique to admin.py]
            string = f"\033[1;37;41mCourse not found, please select from {optional}\033[0;37;40m\n"

        case "bad_input":          # Bad Input --> Refers to EOFERROR (Occurs only when CTRL+Z is inputted)
            string = "\033[1;37;41mBad Input, program restarted\033[0;37;40m\n"
    
        case "login_failed":         # Login failed/password incorrect
            string = "\033[1;37;41mLogin failed, please try again.\033[0;37;40m\n"
    getpass.getpass(string)

# Used to create a dynamic divider that changes size according to the size of the terminal
def divider():
    '''
    Returns a dynamic divider depending on the size of the terminal.
    '''
    column, row = os.get_terminal_size()
    output = f"{EMPTY:-^{column}}"
    return output

# Hashes the user's password
def user_password_hashing(userInput: str): 
    output = hashlib.sha256(userInput.encode())
    return output.hexdigest()

# ============================================================================================
#   Main Page Functions
# ============================================================================================

# Prints page with a list, checks whether is input is in range of list
# "input_list" parameter is for dynamic changing of the menu
def print_main(input_list: list):
    '''
    This function prints out the main page from a main_menu list.

    Args:
        input_list (list) : Used as reference for printing out the menu.
    '''
    content = f"{divider()}\n\t\t\t\033[1;37;40m Main \033[0;37;40m\n{divider()}\n"
    for i, element in enumerate(input_list):
        content += f"[ {i+1} ] {element}\n"
    content += f"[ X ] Exit Application\n{divider()}\n"
    return content

# Main logical system for selection page
def main_logic(content: str):
    '''
    This function is used for the main logic of the selection page.

    Args:
        content (str) : Used to select the file to read from.
    '''
    sub_loop = True
    stored_value = get_input(content)
    match stored_value.upper():
        case "X":
            getpass.getpass("\033[0;32;40mLogging out...\033[0;37;40m")
            return False
        case "1":
            user_config_subloop(sub_loop)
        case "2":
            course_info_subloop(sub_loop)
        case "3":
            quiz_setting_subloop(sub_loop)
        case "4":
            generate_report_subloop(sub_loop)
        case _:
            error_output("option")

# ===================================================================================================
#   User Configuration Functions
# ===================================================================================================

def user_config_logic():
    userInput = print_menu("user")
    # Loads up the JSON file into a dictionary 
    user_info = server_process({"type": "admin_read_file", "file": "user"})
    valueCap = userInput.upper()
    match valueCap:
        case "X": # Closes menu
            return False
        case "1":   # Adds user
            add_user()
        case "2":   # Edit user
            edit_user(user_info)
        case "3":   # Delete user
            delete_user(user_info)
        case _:
            error_output("input")

# Add users to the server
def add_user():
    '''
    This function registers a new user into the server's database.
    '''
    course_list = server_process({"type": "get_courses"})
    available_courses = ""
    for i, element in enumerate(course_list):
        available_courses += f"\n[ {i + 1} ] {element}"
    while True:
        userID_input = get_input(f"{divider()}\n\t\tRegistering User\n{divider()}\nuserID: _\ncourse:\nemail:\npassword:\n{divider()}\n")
        if userID_input.upper() == "X":
            return False
        elif validation(userID_input, "str"):
            continue
        break
    while True:
        course_input = get_input(f"{divider()}\n\t\tRegistering User\n{divider()}\nuserID: {userID_input}\ncourse: _\nemail:\npassword:\n\nAvailable Courses: {available_courses}\n{divider()}\n")
        if course_input.upper() == "X":
            return False
        elif validation(course_input, "int", len(course_list)):
            continue
        print(course_input)
        break
    while True:
        email_input = get_input(f"{divider()}\n\t\tRegistering User\n{divider()}\nuserID: {userID_input}\ncourse: {course_list[int(course_input) - 1]}\nemail: _\npassword:\n{divider()}\n")
        if email_input.upper() == "X":
            return False
        elif validation(email_input, "email"):
            continue
        break
    while True:
        password_input = get_input(f"{divider()}\n\t\tRegistering User\n{divider()}\nuserID: {userID_input}\ncourse: {course_list[int(course_input) - 1]}\nemail: {email_input}\npassword: _\n{divider()}\n", False)
        if password_input.upper() == "X":
            return False
        elif validation(password_input, "password"):
            continue
        verify_pw_input = get_input(f"{divider()}\n\t\tRegistering User\n{divider()}\nuserID: {userID_input}\ncourse: {course_list[int(course_input) - 1]}\nemail: {email_input}\npassword: {len(password_input) * '*'}\n{divider()}\nPlease Re-enter your password\n", False)
        if verify_pw_input.upper() == "X":
            return False
        elif password_input == verify_pw_input:
            packet = {
                "type": "add_user",
                "userID": userID_input,
                "course": course_list[int(course_input) - 1],
                "email": email_input,
                "password": user_password_hashing(password_input)
            }
            server_response = server_process(packet)
            if server_response:
                getpass.getpass("User successfully added to server")
                return False
            else:
                getpass.getpass("User already exist in the database")

# Edits either the email or password of a user
def edit_user(input_list: list):
    '''
    This function retrieves and edits a user's information, then sends it onto the server's database.

    Args:
        input_list (list) : Input for the user information database.
    '''
    if len(input_list) == 0:
        input("User List is empty, please register some users.")
        return
    while True:
        selected_user_index = get_input(f"{divider()}\n\t\tEditing User\n{divider()}\n{view_file_content(1, 'user')}{divider()}\n\t\tSelect a User\n{divider()}\n[ X ] Back to Menu\n{divider()}\n")
        if selected_user_index.upper() == "X":
            return
        elif validation(selected_user_index, "int", len(input_list)):
            continue
        elif selected_user_index.isdigit():
            selection_for_user(int(selected_user_index) - 1)
            return
        else:
            error_output("input")

# Shows the selected user
def user_display(input_list: list, index: int):
    '''
    This function returns a formatted version of the user's data.

    Args: 
        input_list (list) : Input for the user's information
    '''
    user_details = input_list[index]
    string = f"userID\t\t|  \033[4;31;40m{user_details['userID']}\033[0;37;40m\n"
    string += f"email\t\t|  \033[4;31;40m{user_details['email'][:10]}...\033[0;37;40m\n"
    string += f"hashed password\t|  \033[4;31;40m{user_details['password_SHA256'][:10]}...\033[0;37;40m\n"
    string += f"course\t\t|  \033[4;31;40m{user_details['current_course']}\033[0;37;40m"
    return string

# Used to select a user to edit
def selection_for_user(user_index: int):
    '''
    This function is used for the selection of the user 
    that will be edited. It will also be fetching data from the server,
    ensuring that the current data is up to date.

    Args:
        input_list (list) : List that will be edited and referenced from.
        user_index (int) : Index of the previously selected user.

    Returns:
        (None) : Returns only to exti the function
    '''
    while True:
        # Fetches the data from the server to ensure that it remains updated
        user_info = server_process({"type": "admin_read_file", "file": "user"})
        selected = user_display(user_info, user_index)
        user_selection = get_input(f"{divider()}\n\t\tEditing User\n{divider()}\n{selected}\n{divider()}\nSelect a User\n{divider()}\n[ 1 ] Change Email\n[ 2 ] Change Password\n[ 3 ] Change Course\n[ X ] Back to Menu\n{divider()}\n")
        if user_selection.upper() == "X":
            return
        elif validation(user_selection, "int", 3):
            continue
        else:
            edit_user_parameters(user_selection, user_info, user_index)

# Used to edit specific settings for a user
def edit_user_parameters(selection: str, input_list: list, index: int):
    '''
    This function is used to edit the selected user's settings such
    as courses, password and email. It would then send the data changes
    over to the server where it would be automatically updated.

    Args:
        selection (str) : User selected what they want to edit
        input_list (list) : The entire user list that was fetched from the server.
        index (int) : Selected user's index

    '''
    match selection:
        case "1":   # Change email
            while True:
                new_email = get_input(f"{divider()}\n\t\tEditing Email\n{divider()}\n\tEmail\t|\t\033[4;31;40m{input_list[index]['email']}\033[0;37;40m\n{divider()}\nPlease input your new email\n{divider()}\n[ X ] Back to Menu\n{divider()}\n")
                if new_email.upper() == "X":
                    return
                elif validation(new_email, "email"):
                    continue
                break
            
            while True:
                confirm_change = get_input(f"{divider()}\n\t\tConfirm Changes?\n{divider()}\n\tOld email\t|\t{input_list[index]['email']}\n\tNew email\t|\t\033[1;37;40m{new_email}\033[0;37;40m\n{divider()}\n[ C ] Confirm \n[ X ] Cancel Changes\n{divider()}\n")
                # Check if the user wants to exit the menu
                if confirm_change.upper() == "X":
                    return
                elif validation(confirm_change, "str"):
                    continue
                elif confirm_change.upper() == "C":
                    input_list[index]["email"] = new_email
                    server_response = server_process({"type": "admin_write_user", "user_config": input_list})
                    if server_response:
                        get_input("\033[0;32;40mYour changes have been saved!\033[0;37;40m\nPress Enter to Continue\n")
                        return
                break 
        case "2":   # Change password
            while True:
                new_password = get_input(f"{divider()}\n\t\tEditing Password\n{divider()}\n\tPassword\t|\t\033[4;31;40m{input_list[index]['password_SHA256'][:10]}...\033[0;37;40m\n{divider()}\nPlease input your new password\n{divider()}\n[ X ] Back to Menu\n{divider()}\n", False)
                if new_password.upper() == "X":
                    return
                elif validation(new_password, "password"):
                    continue
                verify_pw_input = get_input(f"{divider()}\n\t\tEditing Password\n{divider()}\n\tPassword\t|\t\033[4;31;40m{input_list[index]['password_SHA256'][:10]}...\033[0;37;40m\n{divider()}\nPlease re-enter your new password\n{divider()}\n[ X ] Back to Menu\n{divider()}\n", False)
                if verify_pw_input.upper() == "X":
                    return
                elif verify_pw_input == new_password:
                    break
            while True:
                confirm_change = get_input(f"{divider()}\n\t\tConfirm Changes?\n{divider()}\n\tOld Password\t|\t\033[4;31;40m{input_list[index]['password_SHA256'][:10]}\033[0;37;40m\n\tNew password\t|\t\033[1;37;40m{user_password_hashing(new_password)[:10]}...\033[0;37;40m\n{divider()}\n[ C ] Confirm \n[ X ] Cancel Changes\n{divider()}\n")
                # Check if the user wants to exit the menu
                if confirm_change.upper() == "X":
                    return
                elif validation(confirm_change, "str"):
                    continue
                elif confirm_change.upper() == "C":
                    input_list[index]["password_SHA256"] = user_password_hashing(new_password)
                    server_response = server_process({"type": "admin_write_user", "user_config": input_list})
                    if server_response:
                        get_input("\033[0;32;40mYour changes have been saved!\033[0;37;40m\nPress Enter to Continue\n")                       
                else:
                    error_output("input")
                    continue
        case "3":   # Change course
            course_list = server_process({"type": "get_courses"})
            available_courses = ""
            for i, element in enumerate(course_list):
                available_courses += f"\n[ {i + 1} ] {element}"

            while True:
                new_course = get_input(f"{divider()}\n\t\tEditing Course\n{divider()}\n\tCourse\t|\t\033[4;31;40m{input_list[index]['current_course']}\n\033[0;37;40m{divider()}{available_courses}\n[ X ] Back to Menu\n{divider()}\nPlease input your new course\n")
                if new_course.upper() == "X":
                    return 
                elif validation(new_course, "int", len(course_list)):
                    continue
                input_list[index]["current_course"] = course_list[int(new_course) - 1]
                server_response = server_process({"type": "admin_write_user", "user_config": input_list})
                if server_response:
                    get_input("\033[0;32;40mYour changes have been saved!\033[0;37;40m\nPress Enter to Continue\n", False)
                break
        case _:
            error_output("input") 

# Deletes user from the server
def delete_user(input_list: list):
    '''
    This functions delete a user from the server.

    Args:
        input_list (list) : The entire user list that was fetched from the server.
    '''
    if len(input_list) == 0:
        input("User List is empty, please register some users.")
        return
    while True:
        user_index = get_input(f"{divider()}\n\t\tDeleting User\n{divider()}\n{view_file_content(1, 'user')}{divider()}\nWhich user do you wish to delete?\n{divider()}\n[ X ] Back to Menu\n{divider()}\n")
        # Check if the user wants to exit the menu
        if user_index.upper() == "X":
            return
        elif not user_index.isdigit():
            error_output("input")
            continue
        else:
            # Formatting for display during "delete_check"
            selected_user = input_list[int(user_index) - 1]

            # Formats the input for display
            content = f"  userID\t|  email\t\t|  Hashed Password\t|\n{EMPTY:-^60}\n"
            content += f"  {selected_user['userID']}\t|  {selected_user['email'][:10]}...\t|  {selected_user['password_SHA256'][:10]}...\t|\n" 
        
        while True:
            delete_check = get_input(f"{divider()}\n\t\tDeleting User\n{divider()}\n{content}\n{divider()}\nPlease confirm your selection\n{divider()}\n[ C ] Confirm\t[ X ] Back to Menu\n{divider()}\n")
            
            # Check if the user wants to exit the menu
            if delete_check.upper() == "X":
                break
            elif delete_check.upper() == "C":
                input_list.pop(int(user_index) - 1)
                server_response = server_process({"type": "admin_write_user", "user_config": input_list})
                if server_response:
                    get_input("\033[0;31;40mUser has been deleted!\033[0;37;40m\nPress Enter to Continue\n", False) 
                break
            else:
                error_output("option")
                continue

# ===================================================================================================
#   Course Functions
# ===================================================================================================

# Course Menu
def course_logic():
    '''
    This is the course menu.
    '''
    userInput = print_menu("course")
    # Loads up the JSON file into a dictionary 
    course_info = read_file(_QUESTION_POOL, "json")
    valueCap = userInput.upper()
    match valueCap:
        case "X":   # Closes menu
            return False
        case "1":   # Add course
            add_course(course_info)
        case "2":   # Edit course
            edit_course(course_info)
        case "3":   # Delete course
            delete_course(course_info)
        case _:
            error_output("option")

def add_course(input_list: list):
    '''
    This functions adds in a new course as well as other components such as modules and topics

    Args:
        input_list (list) : The entire course list that was fetched from the server.
    '''
    while True:
        new_course_input = get_input(f"{divider()}\n\t\tAdd Courses\n{divider()}\ncourse_name: _\nmodule_name:\ntopic_name:\nmarks_for_each_question: \nquestions:\n{divider()}\n[ X ] Back to the Menu\n{divider()}\n")
        if new_course_input.upper() == "X":
            return False
        elif validation(new_course_input, "str"):
            continue
        break

    module_list = []
    while True:
        new_module = add_module(new_course_input, input_list)
        if new_module == False: # Exited the program
            return False
        elif isinstance(new_module, tuple) and new_module[0] == True: # Exited the menu
            module_list.append(new_module[1])      
            break
        else:
            module_list.append(new_module)
            break

    formatted_string = ""
    for i, element in enumerate(module_list):
        formatted_string += f"\nmodule_name: {element['module_name']}"
        for topic in element['topics']:
            formatted_string += f"\n  topic_name: {topic['topic_name']}"
            for question in topic['questions']:
                formatted_string += f"\n    question_name: {question['question_name']}"
                formatted_string += f"\n    correct_option {question['correct_option']}"
                formatted_string += f"\n    options:"
                for i, option in enumerate(question['options']):
                    formatted_string += f"\n      {chr(ord('a') + i)}) {option}"
            formatted_string += f"\n  marks_for_each_question: {topic['marks_for_each_question']}"

    # Confirm the creation of the course
    while True:
        confirm = get_input(f"{divider()}\n\t\tAdd Courses\n{divider()}\ncourse_name: {new_course_input}\nmodules:{formatted_string}\n{divider()}\nConfirm the creation of course\n{divider()}\n[ C ] Confirm Course\n[ X ] Back to the Menu\n{divider()}\n")
        if confirm.upper() == "X":
            return False
        elif validation(confirm, "str"):
            continue
        elif confirm.upper() == "C":
            course = {
                "course": new_course_input,
                "modules": module_list
            }
            input_list.append(course)
            write_to_file(_QUESTION_POOL, "json", input_list)
            return

# Edit course information
def edit_course(input_list: list):
    '''
    This function edits the course information as well as module details.

    Args:
        input_dict (dict) : The entire course list that was fetched from the server.
    '''
    while True:
        edit_course_input = get_input(f"{divider()}\n\t\tEdit Courses\n{divider()}\n{view_file_content(1, 'course')}{divider()}\n[ X ] Back to the Menu\n{divider()}\n")
        if edit_course_input.upper() == "X":
            return False
        elif validation(edit_course_input, "int", len(input_list)):
            continue
        check = module_logic(input_list[int(edit_course_input) - 1]['course'])
        if check == False:
            return False
        return check

# Delete selected course
def delete_course(input_list: list):
    '''
    This funcition deletes a course from the server.

    Args:
        input_list (list) : The entire course list that was fetched from the server.
    '''
    while True:
        course_list = []
        for course in input_list:
            course_list.append(course['course'])
        delete_course_input = get_input(f"{divider()}\n\t\tDelete Course\n{divider()}\n{view_file_content(1, 'course')}{divider()}\n[ X ] Back to the Menu\n{divider()}\n")
        if delete_course_input.upper() == "X":
            return False
        elif validation(delete_course_input, "int", len(course_list)):
            continue
        break
    
    while True:
        confirm_change = get_input(f"{divider()}\033[0;31;40mConfirm the deletion of the course\n\033[0;37;40m{divider()}\nCourse: {course_list[int(delete_course_input) - 1]}\n{divider()}\n[ C ] Confirm\n[ X ] Back to the Menu\n{divider()}\n")
        if confirm_change.upper() == "X":
            return False
        elif validation(confirm_change, "str"):
            continue
        elif confirm_change.upper() == "C":
            input_list.pop(int(delete_course_input) - 1)
            write_to_file(_QUESTION_POOL, "json", input_list)
            break
        

# ===================================================================================================
#   Module Functions
# ===================================================================================================

# Module Menu
def module_logic(course_input: str):
    data = False
    # The second value is used for server interaction
    userInput = print_menu("module", {"course_name": course_input})

    module_info = read_file(_QUESTION_POOL, "json")
    valueCap = userInput.upper()
    match valueCap:
        case "X":   # Closes menu
            return False
        case "1":   # Add module
            data = add_module(course_input, module_info)
        case "2":   # Edit module
            data = edit_module(course_input, module_info)
        case "3":   # Delete module
            data = delete_module(course_input, module_info)
        case _:
            error_output("option")

def add_module(course_input: str, input_list: list):
    while True:
        new_module_input = get_input(f"{divider()}\n\t\tAdd Modules\n{divider()}\ncourse_name: {course_input}\nmodule_name: _\ntopic_name:\nmarks_for_each_question:\nquestions:\n{divider()}\n[ X ] Back to the Menu\n{divider()}\n")
        if new_module_input.upper() == "X":
            return False
        elif validation(new_module_input, "str"):
            continue
        break
    
    topic_list = []
    while True:
        new_topic = add_topic(course_input, new_module_input)
        if new_topic == False:
            return False
        elif isinstance(new_topic, tuple) and new_topic[0] == True:
            topic_list.append(new_topic[1]) # Append the topic to the list
            break
        else:
            topic_list.append(new_topic)

    formatted_string = ""
    if len(topic_list) <= 0:
        formatted_string = f"\n- No topics added yet"
    else:
        for topic in topic_list:
            formatted_string += f"\n    topic_name: {topic['topic_name']}"
            for question in topic['questions']:
                formatted_string += f"\n      question_name: {question['question_name']}"
                formatted_string += f"\n      correct_option {question['correct_option']}"
                formatted_string += f"\n      options:"
                for i, option in enumerate(question['options']):
                    formatted_string += f"\n      {chr(ord('a') + i)}) {option}"
            formatted_string += f"\n  marks_for_each_question: {topic['marks_for_each_question']}"

    while True:
        confirm = get_input(f"{divider()}\n\t\tAdd Modules\n{divider()}\ncourse_name: {course_input}\n  module_name: {new_module_input}{formatted_string}\n{divider()}\nConfirm the creation of module\n{divider()}\n[ C ] Confirm Module\n[ D ] Done Adding Modules\n[ X ] Back to the Menu\n{divider()}\n")
        if confirm.upper() == "X":
            return False
        elif validation(confirm, "str"):
            continue
        elif confirm.upper() == "C":
            module = {
                "module_name": new_module_input,
                "topics": topic_list
            }
            return module
        elif confirm.upper() == "D":
            module = {
                "module_name": new_module_input,
                "topics": topic_list
            }
            return (True, module)

def edit_module(course_input: str, input_list: list):
    while True:
        edit_module_input = get_input(f"{divider()}\n\t\tEdit Modules\n{divider()}\n{view_file_content(1, 'module',{'course_name': course_input})}{divider()}\n[ X ] Back to the Menu\n{divider()}\n")
        if edit_module_input.upper() == "X":
            return
        elif validation(edit_module_input, "int", len(input_list)):
            continue

        server_list = server_process({"type": "admin_fetch_question_pool", "file": "module", 'course_name': course_input})
        check = topic_logic(course_input, server_list['data'][int(edit_module_input) - 1]['module'])
        if check == False:
            return False
        return check

def delete_module(course_input: str, input_list: list):
    while True:
        module_list = []
        for each_course in input_list:
            if each_course['course'] != course_input:
                break
            for each_module in each_course['modules']:
                module_list.append(each_module['module_name'])
        delete_module_input = get_input(f"{divider()}\n\t\tDelete Module\n{divider()}\n{view_file_content(1, 'module',{'course_name': course_input})}{divider()}\n[ X ] Back to the Menu\n{divider()}\n")
        if delete_module_input.upper() == "X":
            return False
        elif validation(delete_module_input, "int", len(module_list)):
            continue
        break

    while True:
        confirm_change = get_input(f"{divider()}\n\t\tDelete Module\n{divider()}\nModule: {module_list[int (delete_module_input) - 1]}\n{divider()}\n[ C ] Confirm Deletion\n[ X ] Back to the Menu\n{divider()}\n")
        if confirm_change.upper() == "X":
            return False
        elif validation(confirm_change, "str"):
            continue
        elif confirm_change.upper() == "C":
            for each_course in input_list:
                if each_course['course'] != course_input:
                    break
                for each_module in each_course['modules']:
                    if each_module['module_name'] == module_list[int(delete_module_input) - 1]:
                        each_course['modules'].remove(each_module)
                        break
            write_to_file(_QUESTION_POOL, "json", input_list)
            break

# ===================================================================================================
#   Topic Functions
# ===================================================================================================

# Topic Menu
def topic_logic(course_input: str, module_input: str):
    userInput = print_menu("topic", {'course_name': course_input, 'module': module_input})

    topic_info = read_file(_QUESTION_POOL, "json")
    valueCap = userInput.upper()
    match valueCap:
        case "X":   # Closes menu
            return False
        case "1":   # Add topic
            add_topic(course_input, module_input)
        case "2":   # Edit topic
            edit_topic(course_input, module_input, topic_info)
        case "3":   # Delete topic
            delete_topic(course_input, module_input, topic_info)
        case _:
            error_output("option")

def add_topic(course_input: str, module_input: str):
    # Topic name
    while True:
        new_topic_name_input = get_input(f"{divider()}\n\t\tAdd Topics\n{divider()}\ncourse_name: {course_input}\n  module_name: {module_input}\n    topic_name: _\n    marks_for_each_question:\n    questions:\n{divider()}\n[ X ] Back to the Menu\n{divider()}\n")
        if new_topic_name_input.upper() == "X":
            return False
        elif validation(new_topic_name_input, "str"):
            continue
        break
    # Marks allocated for each question within the topic
    while True:
        marks = get_input(f"{divider()}\n\t\tAdd Topics\n{divider()}\ncourse_name: {course_input}\n  module_name: {module_input}\n    topic_name: {new_topic_name_input}\n    marks_for_each_question: _\n    questions:\n{divider()}\nPlease allocate the marks for each question within this topic\n{divider()}\n[ X ] Back to the Menu\n{divider()}\n")
        if marks.upper() == "X":
            return False
        elif validation(marks, "int"):
            continue
        break
    
    question_list = []
    while True:
        new_questions = add_question(course_input, module_input, new_topic_name_input)
        if new_questions == False:
            return False
        elif isinstance(new_questions, tuple) and new_questions[0] == True:  # True if the completed adding questions.
            question_list.append(new_questions[1])  # Append the new question that got added
            for question in question_list:
                question.pop("method")
            break
        else:
            question_list.append(new_questions)

    formatted_string = ""
    for question in question_list:
        formatted_string += f"\n\n      question_name: {question['question_name']}"
        formatted_string += f"\n      correct_option {question['correct_option']}"
        formatted_string += f"\n      options:"
        for i, option in enumerate(question['options']):
            formatted_string += f"\n        {chr(ord('a') + i)}) {option}"

    while True:
        confirm = get_input(f"{divider()}\n\t\tAdd Topics\n{divider()}\ncourse_name: {course_input}\n  module_name: {module_input}\n    topic_name: {new_topic_name_input}\n    marks_for_each_question: {marks}\n    questions:{formatted_string}\n{divider()}\nConfirm the creation of topic\n{divider()}\n[ C ] Confirm Topic\n[ D ] Done Adding Topics\n[ X ] Back to the Menu\n{divider()}\n")
        if confirm.upper() == "X":
            return False
        elif validation(confirm, "str"):
            continue
        elif confirm.upper() == "C":
            topic = {
                "topic_name": new_topic_name_input,
                "questions": question_list,
                "marks_for_each_question": int(marks)
            }
            return topic
        elif confirm.upper() == "D":
            topic = {
                "topic_name": new_topic_name_input,
                "questions": question_list,
                "marks_for_each_question": int(marks)
            }
            return (True, topic)

def edit_topic(course_input, module_input, input_list: list):
    while True:
        edit_topic = get_input(f"{divider()}\n\t\tEdit Modules\n{divider()}\n{view_file_content(1, 'topic',{'course_name': course_input, 'module': module_input})}{divider()}\n[ X ] Back to the Menu\n{divider()}\n")
        if edit_topic.upper() == "X":
            return False
        elif validation(edit_topic, "int", len(input_list)):
            continue

        topic_dict = server_process({"type": "admin_fetch_question_pool", "file": "topic", "course_name": course_input, "module": module_input})

        topic_list = topic_dict['data']

        edit_selected = get_input(f"{divider()}\n\t\tEdit Modules\n{divider()}\n[ 1 ] Topic Name: {topic_list[int(edit_topic) - 1]['topic']}\n[ 2 ] Marks for Each Question: {topic_list[int(edit_topic) - 1]['marks_for_each_question']}\n[ 3 ] Questions\n{divider()}\n[ X ] Back to the Menu\n{divider()}\n")

        match edit_selected:
            case "1":   # Edit topic name
                while True:
                    new_topic = get_input(f"{divider()}\n\t\tEdit Topic Name\n{divider()}\nOld Topic Name: {topic_list[int(edit_topic) - 1]['topic']}\nNew Topic Name: _\n{divider()}\n[ X ] Back to the Menu\n{divider()}\n")
                    if new_topic.upper() == "X":
                        return False
                    elif validation(new_topic, "str"):
                        continue
                    break

                while True:
                    check = get_input(f"{divider()}\n\t\tEdit Topic Name\n{divider()}\nOld Topic Name: {topic_list[int(edit_topic) - 1]['topic']}\nNew Topic Name: {new_topic}\n{divider()}\n[ X ] Back to the Menu\n{divider()}\n")
                    if check.upper() == "X":
                        return False
                    elif validation(check, "str"):
                        continue
                    elif check.upper() == "C":
                        topic = {
                            "old_topic_name": topic_list[int(edit_topic) - 1]['topic'],
                            "new_topic_name": new_topic,
                            "course_name": course_input,
                            "module": module_input
                        }
                        return topic
            case "2":   # Edit marks for each question
                while True:
                    marks = get_input(f"{divider()}\n\t\tEdit Topic Name\n{divider()}\nOld marks per question: {topic_list[int(edit_topic) - 1]['marks_for_each_question']}\nNew marks per question: _\n{divider()}\n[ X ] Back to the Menu\n{divider()}\n")
                    if marks.upper() == "X":
                        return False
                    elif validation(marks, "int"):
                        continue
                    break

                while True:
                    check = get_input(f"{divider()}\n\t\tEdit Topic Name\n{divider()}\nOld marks per question: {topic_list[int(edit_topic) - 1]['topic']}\nNew marks per question: {marks}\n{divider()}\n[ X ] Back to the Menu\n{divider()}\n")
                    if check.upper() == "X":
                        return False
                    elif validation(check, "str"):
                        continue
                    elif check.upper() == "C":
                        topic = {
                            "topic_name": topic_list[int(edit_topic) - 1]['topic'],
                            "marks_for_each_question": marks,
                            "course_name": course_input,
                            "module": module_input
                        }
                        return topic
            case "3":   # Edit questions
                server_list = server_process({"type": "admin_fetch_question_pool", "file": "topic", 'course_name': course_input, 'module': module_input})
                check = question_logic(course_input, module_input, server_list['data'][int(edit_topic) - 1]['topic'])
                if check == False:
                    return False
                return check

def delete_topic(course_input, module_input, input_list: list):
    '''
    This function deletes topics from the question_pool.json file
    '''
    while True:
        topic_list = []
        for each_course in input_list:
            if each_course['course'] != course_input:
                break
            for each_module in each_course['modules']:
                if each_module['module_name'] != module_input:
                    continue
                for each_topic in each_module['topics']:
                    topic_list.append(each_topic['topic_name'])
        delete_topic = get_input(f"{divider()}\n\t\tDelete Topics\n{divider()}\n{view_file_content(1, 'topic', {'course_name': course_input, 'module': module_input})}{divider()}\n[ X ] Back to the Menu\n{divider()}\n")
        if delete_topic.upper() == "X":
            return False
        elif validation(delete_topic, "int", len(topic_list)):
            continue
        break
        
    while True:
        delete_selected = get_input(f"{divider()}\n\t\tDelete Topics\n{divider()}\nTopic Name: {topic_list[int(delete_topic) - 1]}\n{divider()}\n[ C ] Confirm Deletion\n[ X ] Back to the Menu\n{divider()}\n")
        if delete_selected.upper() == "X":
            return False
        elif validation(delete_selected, "str"):
            continue
        elif delete_selected.upper() == "C":
            for each_course in input_list:
                if each_course['course'] != course_input:
                    continue
                for each_module in each_course['modules']:
                    if each_module['module_name'] != module_input:
                        continue
                    for each_topic in each_module['topics']:
                        if each_topic['topic_name'] == topic_list[int(delete_topic) - 1]:
                            each_module['topics'].remove(each_topic)
                            break
            write_to_file(_QUESTION_POOL, "json", input_list)
            break
       

# ===================================================================================================
#   Question Pool Functions
# ===================================================================================================
# Admin user would need to select the course and the module before being able to edit the question pool

# Logicial system for question pool
def question_logic(course_input: str, module_input: str, topic_input: str):
    userInput = print_menu("question", {"course_name": course_input, "module": module_input, "topic": topic_input})
    # Loads up the JSON file into a dictionary 
    valueCap = userInput.upper()
    match valueCap:
        case "X":   # Closes menu
            return False
        case "1":   # Add question
            add_question(course_input, module_input, topic_input)
        case "2":   # Edits question
            edit_question(course_input, module_input, topic_input)
        case "3":   # Delete question
            delete_question(course_input, module_input, topic_input)   
        case _:
            error_output("option")

# Add question into the "question_pool.json"
def add_question(course_input: str, module_input: str, topic_input: str) -> list:
    # Number of options for this question
    while True:
        print_option = ""
        no_of_options = get_input(f"{divider()}\nHow many options do you want? [ 3 - 5 options ]\n{divider()}\n[ X ] Back to Menu\n{divider()}\n")
        
        # Check if the user wants to exit the menu
        if no_of_options.upper() == "X":
            return False
        if no_of_options.isdigit():
            if int(no_of_options) <= 2 or int(no_of_options) > 6:
                error_output("range")
                continue
            else:
                for i in range(int(no_of_options)):
                    print_option += f"{chr(97 + i)})\n"
        else:
            error_output("input")
            continue
        break
    
    # Question input check
    while True:
        question = get_input(f"{divider()}\n\t\t\tAdding Question\n{divider()}\nQuestion: \n\nOptions: \n{print_option}\n\nAnswer: \n\n{divider()}\n[ X ] Back to Menu\n{divider()}\nInput Question: ")
        
        # Check if the user wants to exit the menu
        if question.upper() == "X":
            return False
        # Check for the length of the question
        elif len(question) < 5:
            error_output("short")
            continue
        elif len(question) > 70:
            error_output("long")
            continue
        break
    # Option input check
    if True:
        options_listing = [""] * int(no_of_options)
        string = print_option

        for i in range(int(no_of_options)):
            options = get_input(f"{divider()}\n\t\t\tAdding Options\n{divider()}\nQuestion: {question}\n\nOptions: \n{string}\n\n Answer: \n\n{divider()}\n[ X ] Back to Menu\n{divider()}\nInput Options: ")
            
            # Check if the user wants to exit the menu
            if options.upper() == "X":
                return False
            elif len(options) > 70:
                error_output("long")
            else:
                string = ""
                options_listing[i] = options
                for j, element in enumerate(options_listing):
                    string += f"{chr(97 + j)}) {element}\n"
    # Answer input check
    while True:
        answer = get_input(f"{divider()}\n\t\t\tAdding Answers\n{divider()}\nQuestion: {question}\n\nOptions: \n{string}\n\nAnswer: \n\n{divider()}\n[ X ] Back to Menu\n{divider()}\nCorrect Answer: ")
        
        # Check if the user wants to exit the menu
        if answer.upper() == "X":
            return False
        for i, element in enumerate(options_listing):
            if chr(97 + i) == answer.lower():
                answer = element
                break
        else:
            error_output("option")
            continue
        break
            
    # Confirm check
    while True:
        confirm_change = get_input(f"{divider()}\n\t\t\tConfirming Question\n{divider()}\nquestion: {question}\n\noptions: \n{string}\n\ncorrect_option: {answer}\n\n{divider()}\n[ C ] Confirm Question\n[ D ] Done Adding Questions\n[ X ] Back to Menu\n{divider()}\n", False)
        
        # Check if the user wants to exit the menu
        if confirm_change.upper() == "X":
            return False
        elif validation(confirm_change, "str"):
            continue
        elif confirm_change.upper() == "C":
            question = {
                "method": "add_question",   # Used the server would know how to handle with the data
                "question_name": question,
                "correct_option": answer,
                "options": options_listing
            }
            get_input("\033[0;32;40mYour changes have been saved!\033[0;37;40m\nPress Enter to Continue\n", False)
            return question
        elif confirm_change.upper() == "D":
            question = {
                "method": "add_question",   # Used the server would know how to handle with the data
                "question_name": question,
                "correct_option": answer,
                "options": options_listing
            }
            return (True, question)
        else:
            error_output("option")
            continue
    
# Edits question from "question_pool"
def edit_question(course_input, module_input, topic_input): 
    question_pool = read_file(_QUESTION_POOL, "json")

    # Gets values of the question to be edited
    for each_course in question_pool:
        if each_course["course"] != course_input:
            continue
        for each_module in each_course["modules"]:
            if each_module["module_name"] != module_input:
                continue
            for each_topic in each_module["topics"]:
                if each_topic["topic_name"] != topic_input:
                    continue
                question_list = each_topic["questions"]
                break
            break
    
    # Question input check
    if len(question_list) == 0:
        input("Question Pool is empty, please add some questions")
        return
    while True:
        edit_index = selection_of_question("Editing Question",course_input, module_input, topic_input, question_list)
        
        # Checks if the string is empty
        if edit_index == "":
            error_output("empty_input")
        
        # Execute if its not an integer       
        elif isinstance(edit_index, str) and not edit_index.isdigit():
            if edit_index.upper() == "X":
                return  
            else:
                error_output("input")
        
        # Execute if its not integer       
        elif isinstance(edit_index, int):
            
            while True:
                # Displays the selected question
                selected_question_display = question_display(edit_index, question_list)
                user_selection = get_input(f"{divider()}\n\t\tEditing Question\n{divider()}\n{selected_question_display}\n{divider()}\nWhat do you want to edit?\n{divider()}\n[ 1 ] Question Content\n[ 2 ] Question Options\n[ 3 ] Question Answer\n[ X ] Back to Menu\n{divider()}\n")
                if user_selection.upper() == "X":
                    return
                elif user_selection.isdigit():
                    selection_for_question_pool(user_selection, edit_index, question_list, topic_input)
                    return
                else:
                    error_output("input")
                    continue
        else:
            error_output("option")

# Use to display the selected question 
# "selected_index" is the selected question index
def question_display(selected_index: int, question_list: list):
    # Gets the values of the current dictionary
    string = f"\tQuestion  |  {question_list[selected_index]['question_name']}\n{divider()}\n"
    # Formats the options
    for i, element in enumerate(question_list[selected_index]['options']):
        string += f"\t{chr(i + 97)})\t|  {element}\n"
    string += f"{divider()}\n\tAnswer\t|  {question_list[selected_index]['correct_option']}\n"
    return string
    
# Logic for changing of the question content
def selection_for_question_pool(input_string: str, index: int, question_list: list, topic_input: str):
    '''
    This function is for the selection of what the user wants to edit

    Args:
        input_string  (str): The input from the user
        index  (int): The index of the question
        question_list (list) : The list of questions
        topic_input (str): The topic of the question
    '''
    # Gets the values of the current dictionary
    value_list = list(dictionary.values())

    local_loop = True
    # Displays the selected question
    selected_question_display = question_display(index, question_list)
    # Used to change the question content
    if input_string == "1":
        while local_loop:
            new_question_content = get_input(f"{divider()}\n\t\tEditing Question Content\n{divider()}\n{selected_question_display}\n{divider()}\n[ X ] Back to Menu\n{divider()}\n")
            
            # Check if the user wants to exit the menu
            if new_question_content.upper() == "X":
                local_loop = False
                break
            elif validation(new_question_content, "str"):
                continue
            break

        while local_loop:
            confirm_change = get_input(f"{divider()}\n\t\tConfirm Changes?\n{divider()}\n{selected_question_display}\nOriginal:\t{question_list[index]['question_name']}\nNew:\t\t\033[1;37;40m{new_question_content}\033[0;37;40m\n{divider()}\n[ C ] Confirm \n[ X ] Cancel Changes\n{divider()}\n")
            
            # Check if the user wants to exit the menu
            if confirm_change.upper() == "X":
                local_loop = False
            elif confirm_change == "":
                error_output("empty_input")
                continue
            elif confirm_change.upper() == "C":
                question_list[index]['question_name'] = new_question_content
                packet = {"topic": topic_input, "questions": question_list}
                print(question_list)
                write_to_file(_QUESTION_POOL, "edit_question", packet)
                get_input("\033[0;32;40mYour changes have been saved!\033[0;37;40m\nPress Enter to Continue\n", False)                       
            else:
                error_output("input")
                continue
            break  

    # Used to change the options
    if input_string == "2":
        while local_loop:
            option_number = get_input(f"{divider()}\n\t\tEditing Question Options\n{divider()}\n{selected_question_display}\n{divider()}\n[ X ] Back to Menu\n{divider()}\n")

            # Check if the user wants to exit the menu
            if option_number.upper() == "X":
                local_loop = False
            elif option_number == "":
                error_output("empty_input")
                continue
            # If its user input is in the list, return True
            elif check_user_input(option_number, question_list[index]['options']):
                while True:
                    list_index =  ord(option_number) - 97
                    new_option_content = get_input(f"{divider()}\n\t\tEditing Question Options\n{divider()}\n{selected_question_display}\nSelected Option | {option_number}\n\tOption\t| {question_list[index]['options'][list_index]}\n\tNew\t|\n{divider()}\n[ X ] Back to Menu\n{divider()}\n")
                    
                    # Check if the user wants to exit the menu
                    if new_option_content.upper() == "X":
                        break
                    elif validation(new_option_content, "str"):
                        continue
                    break
            else:
                error_output("input")
                continue
            break

        while local_loop:
            confirm_change = get_input(f"{divider()}\n\t\tConfirm Changes?\n{divider()}\n{selected_question_display}\nSelected Option | {option_number}\n\tOption\t| {question_list[index]['options'][list_index]}\n\tNew\t| \033[1;37;40m{new_option_content}\033[0;37;40m\n{divider()}\n[ C ] Confirm\n[ X ] Back to Menu\n{divider()}\n")
            
            # Check if the user wants to exit the menu
            if confirm_change.upper() == "X":
                local_loop = False
            elif confirm_change == "":
                error_output("empty_input")
                continue
            elif confirm_change.upper() == "C":
                # Changes the answer if correct option content gets changed
                question_list[index]['options'][list_index] = new_option_content
                packet = {"topic": topic_input, "questions": question_list}
                write_to_file(_QUESTION_POOL, "edit_question", packet)
                get_input("\033[0;32;40mYour changes have been saved!\033[0;37;40m\nPress Enter to Continue\n", False)                                    
            else:
                error_output("input")
                continue
            break

    # Used to change the answer of the question
    if input_string == "3":
        while local_loop:
            new_answer_content = get_input(f"{divider()}\n\t\tEditing Question Answer\n{divider()}\n{selected_question_display}\n{divider()}\n[ X ] Back to Menu\n{divider()}\n")
            
            # Check if the user wants to exit the menu
            if new_answer_content.upper() == "X":
                local_loop = False
            elif validation(new_answer_content, "str"):
                continue
            elif check_user_input(new_answer_content, question_list[index]['options']):
                list_index = ord(new_answer_content) - 97
                break
            else:
                error_output("input")
                continue

        while local_loop:
            confirm_change = get_input(f"{divider()}\n\t\tConfirm Changes?\n{divider()}\n{selected_question_display}\nOriginal:\t{question_list[index]['correct_option']}\nNew:\t\t\033[1;37;40m{question_list[index]['options'][list_index]}\033[0;37;40m\n{divider()}\n[ C ] Confirm \n[ X ] Cancel Changes\n{divider()}\n")
            
            # Check if the user wants to exit the menu
            if confirm_change.upper() == "X":
                local_loop = False
            elif confirm_change == "":
                error_output("empty_input")  
            elif confirm_change.upper() == "C":
                question_list[index]['correct_option'] = question_list[index]['options'][list_index]
                packet = {"topic": topic_input, "questions": question_list}
                write_to_file(_QUESTION_POOL, "edit_question", packet)
                input("\033[0;32;40mYour changes have been saved!\033[0;37;40m\nPress Enter to Continue\n")                       
                break
            else:
                error_output("input")
                continue

# Checks if the user's selected option in inside the range of options 
# For any question. Due to the flexibility of the number of options the admin can set.
def check_user_input(user_input: str, question_data: list) -> bool:
    '''
    This function checks if the user's selected option in inside the range of options.

    Args:
        user_input (str) : User's current input.
        question_data (list) : List that will be used as reference.

    Returns:
        True or False.
    '''
    check_list = []
    for i, option in enumerate(question_data):
        check_list.extend(chr(97 + i))
    for check in check_list:
        if check == user_input.lower():
            return True
    return False

# Deletes question from "question_pool"
def delete_question(course_input, module_input, topic_input):
    question_pool = read_file(_QUESTION_POOL, "json")

    # Gets values of the question to be edited
    for each_course in question_pool:
        if each_course["course"] != course_input:
            continue
        for each_module in each_course["modules"]:
            if each_module["module_name"] != module_input:
                continue
            for each_topic in each_module["topics"]:
                if each_topic["topic_name"] != topic_input:
                    continue
                question_list = each_topic["questions"]
                break
            break

    if len(question_list) == 0:
        input("Question Pool is empty, please add some questions")
        return
    while True:
        os.system("cls")
        deleting_index = selection_of_question("Deleting Question", course_input, module_input, topic_input, question_list)
        
        # Check if the user wants to exit the menu
        if deleting_index == "X":
            return
        else:
            deleting_index = int(deleting_index)
            string = ""
            for j, element in enumerate(question_list[deleting_index]['options']):
                string += f"{chr(97 + j)}) {element}\n"    

        while True:
            delete_check = get_input(f"{divider()}\n\t\tPlease confirm your selection\n{divider()}\n{question_list[deleting_index]['question_name']}\n{string}\n{question_list[deleting_index]['correct_option']}\n{divider()}\n[ C ] Confirm\t\t[ X ] Back to Menu\n{divider()}\n")
            if delete_check.upper() == "X":
                break
            elif delete_check.upper() == "C":
                question_list.remove(question_list[deleting_index])
                packet = {"topic": topic_input, "questions": question_list}
                write_to_file(_QUESTION_POOL, "edit_question", packet)
                get_input("\033[0;31;40mOption has been deleted!\033[0;37;40m\nPress Enter to Continue\n", False) 
                break 
            else:
                error_output("option")
                continue
        return

# Returns the index value for menu navigation
# Checks if the inputted value is within range of the available options
# 
# "title" parameter needs to be a string for the printing
def selection_of_question(title: str, course_input, module_input, topic_input, question_list_input):
    while True:
        value_number = get_input(f"{divider()}\n\t\t{title}\n{divider()}\n{view_file_content(1, 'question', {'course_name': course_input, 'module': module_input, 'topic': topic_input})}{divider()}\n[ X ] Back to Menu\n{divider()}\n")
        
        # Check if the user wants to exit the menu
        if value_number.upper() == "X":
            return "X"
        elif validation(value_number, "int", len(question_list_input)):
            continue
        else:
            return (int(value_number) - 1)

# ===================================================================================================
#   Quiz Settings Functions
# ===================================================================================================
# [NOTE] Quiz Settings values can only be a integer, float and boolean.
# The only exception for this rule is for the assessment componenet, where it is stored as a list.

# Logicial system for quiz setting
def setting_logic():
    '''
    This function is used to select settings related to any quiz that are in the system.
    '''
    # Loads up the JSON file into a dictionary 
    quiz_setting = server_process({"type": "admin_read_file", "file": "setting"})
    userInput = print_menu("setting", "all_quiz")
    valueCap = userInput.upper()
    match valueCap:
        case "X": # Return to selection menu
            return False
        case "1": # Add Setting
            add_new_quiz_setting(quiz_setting)
        case "2": # Edit Setting
            edit_quiz_setting(quiz_setting)
        case "3": # Delete Setting
            delete_quiz_setting(quiz_setting)
        case _:
            error_output("option")

# Adding a new quiz with its own quiz settings
def add_new_quiz_setting(input_list: list):
    '''
    This function is used to add a new quiz setting which will be 
    used to set the quiz.
    It will prompt the user to key in each data for the new quiz setting.
    '''
    # course
    while True:
        # Fetches all the courses from the server
        fetched_courses = server_process({"type": "admin_fetch_specific_setting", "setting": "course"})
        available_courses = ""
        for i, course in enumerate(fetched_courses):
            available_courses += f"\n[ {i + 1} ] {course}"
        course_input = get_input(f"{divider()}\ncourse: _\nmodule:\nquiz_name:\nassessment_component:\ntime_in_minutes:\nmaximum_number_of_attempts:\nrandomize_option:\nshow_quiz:\n{divider()}Please select the course for the quiz\n{divider()}{available_courses}\n[ X ] Back to Menu\n{divider()}\n")
        if course_input.upper() == "X":
            return
        elif validation(course_input, "int", len(fetched_courses)):
            continue
        selected_course = fetched_courses[int(course_input) - 1]
        break

    # module_name
    while True:
        # Fetches all the modules from the selected course from the server
        fetched_modules = server_process({"type": "admin_fetch_specific_setting", "setting": "module", "course": selected_course})
        available_modules = ""
        for i, module in enumerate(fetched_modules):
            available_modules += f"\n[ {i + 1} ] {module}"
        module_input = get_input(f"{divider()}\ncourse: {selected_course}\nmodule: _\nquiz_name:\nassessment_component:\ntime_in_minutes:\nmaximum_number_of_attempts:\nrandomize_option:\nshow_quiz:\n{divider()}Please select the module for the quiz\n{divider()}{available_modules}\n[ X ] Back to Menu\n{divider()}\n")
        if module_input.upper() == "X":
            return
        elif validation(module_input, "int", len(fetched_modules)):
            continue
        selected_module = fetched_modules[int(module_input) - 1]
        break

    # quiz_name
    while True:
        input_quiz_name = get_input(f"{divider()}\ncourse: {selected_course}\nmodule: {selected_module}\nquiz_name: _\nassessment_component:\ntime_in_minutes:\nmaximum_number_of_attempts:\nrandomize_option:\nshow_quiz:\n{divider()}Please create a name for the quiz\n{divider()}\n[ X ] Back to Menu\n{divider()}\n")
        if input_quiz_name.upper() == "X":
            return
        elif validation(input_quiz_name, "str"):
            continue
        break

    # Variables assessment component
    input_asessment_component = []

    # assessment_component        
    while True:
        fetched_topics = server_process({"type": "admin_fetch_specific_setting", "setting": "assessment_component", "course": selected_course, "module": selected_module})
        available_topics = ""
        # Prints out all topics that selected course and module
        for i, component in enumerate(fetched_topics):
            available_topics += f"\n[ {i + 1} ] {component['topic']}"
        
        assessment_component_data = ""
        # Prints out the current list of assessment component if assessment_component isn't empty
        if len(input_asessment_component) != 0:
            for element in input_asessment_component:
                assessment_component_data += f"\n\t- {element['topic_name']}: {element['number_of_questions']} questions"

        topic_input = get_input(f"{divider()}\ncourse: {selected_course}\nmodule: {selected_module}\nquiz_name: {input_quiz_name}\nassessment_component: {assessment_component_data}\ntime_in_minutes:\nmaximum_number_of_attempts:\nrandomize_option:\nshow_quiz:\n{divider()}Please select your topics for the quiz\n{divider()}{available_topics}\n{divider()}\n[ C ] Completed editing component\n[ X ] Back to Menu\n{divider()}\n")
        if topic_input.upper() == "X":
            return
        elif topic_input.upper() == "C":
            if input_asessment_component == []:
                error_output("empty_assessment")
                continue
            break
        elif validation(topic_input, "int", len(fetched_topics)):
            continue
        else:
            while True:
                number_of_qn_input = get_input(f"{divider()}\ncourse: {selected_course}\nmodule: {selected_module}\nquiz_name: {input_quiz_name}\nassessment_component: {assessment_component_data}\ntime_in_minutes:\nmaximum_number_of_attempts:\nrandomize_option:\nshow_quiz:\n{divider()}Please input the max number of question for the selected topic\n{divider()}\n[ X ] Back to Menu\n{divider()}\n")
                if number_of_qn_input.upper() == "X":
                    return
                elif validation(number_of_qn_input, "int"):
                    continue
                elif int(number_of_qn_input) > fetched_topics[int(topic_input) - 1]["max_number_of_questions"]:
                    error_output("max")
                    continue
                break
            # Checks if the topic is already in the list
            if fetched_topics[int(topic_input) - 1]["topic"] in [component["topic_name"] for component in input_asessment_component]:  
                error_output("duplicate")
                continue
            input_asessment_component.append({"topic_name": fetched_topics[int(topic_input) - 1]['topic'], "number_of_questions": number_of_qn_input})
    
    # time_in_minutes
    while True:
        quiz_time_input = get_input(f"{divider()}\ncourse: {selected_course}\nmodule: {selected_module}\nquiz_name: {input_quiz_name}\nassessment_component: {assessment_component_data}\ntime_in_minutes:\nmaximum_number_of_attempts:\nrandomize_option:\nshow_quiz:\n{divider()}Please input the time for your quiz in minutes\n{divider()}\n[ X ] Back to Menu\n{divider()}\n")
        if quiz_time_input.upper() == "X":
            return
        elif validation(quiz_time_input, "int"):
            continue
        break
    # maximum_number_of_attempts
    attempt_types = ["single", "multiple", "unlimited"]
    attempt_options = ""
    for i, element in enumerate(attempt_types):
        attempt_options += f"\n[ {i + 1} ] {element}"
    while True:
        quiz_attempt_input = get_input(f"{divider()}\ncourse: {selected_course}\nmodule: {selected_module}\nquiz_name: {input_quiz_name}\nassessment_component: {assessment_component_data}\ntime_in_minutes: {quiz_time_input}\nmaximum_number_of_attempts:\nrandomize_option:\nshow_quiz:\n{divider()}Please select which attempt type you want to set the quiz\n{divider()}{attempt_options}\n[ X ] Back to Menu\n{divider()}\n")
        if quiz_attempt_input.upper() == "X":
            return
        elif validation(quiz_attempt_input, "int"):
            continue
        match int(quiz_attempt_input):
            case 1:
                max_attempt = 1
            case 2:
                quiz_attempt_input = get_input(f"{divider()}\ncourse: {selected_course}\nmodule: {selected_module}\nquiz_name: {input_quiz_name}\nassessment_component: {assessment_component_data}\ntime_in_minutes: {quiz_time_input}\nmaximum_number_of_attempts:\nrandomize_option:\nshow_quiz:\n{divider()}Please input the max number of attempts for your quiz\n{divider()}\n[ X ] Back to Menu\n{divider()}\n")
                if quiz_attempt_input.upper() == "X":
                    return
                elif validation(quiz_attempt_input, "int"):
                    continue
                max_attempt = quiz_attempt_input
            case 3:
                max_attempt = "unlimited"
        break
    
    # randomize_options
    while True:
        quiz_randomize_input = get_input(f"{divider()}\ncourse: {selected_course}\nmodule: {selected_module}\nquiz_name: {input_quiz_name}\nassessment_component: {assessment_component_data}\ntime_in_minutes: {quiz_time_input}\nmaximum_number_of_attempts: {max_attempt}\nrandomize_option:\nshow_quiz:\n{divider()}Please select if you want to randomize the options for your quiz\n{divider()}\n[ 1 ] Randomize\n[ 2 ] Do not randomize\n[ X ] Back to Menu\n{divider()}\n")
        if quiz_randomize_input.upper() == "X":
            return
        elif validation(quiz_randomize_input, "int"):
            continue
        match int(quiz_randomize_input):
            case 1:
                randomize = True
            case 2:
                randomize = False
        break
    
    # show_quiz
    while True:
        quiz_show_input = get_input(f"{divider()}\ncourse: {selected_course}\nmodule: {selected_module}\nquiz_name: {input_quiz_name}\nassessment_component: {assessment_component_data}\ntime_in_minutes: {quiz_time_input}\nmaximum_number_of_attempts: {max_attempt}\nrandomize_option: {randomize}\nshow_quiz:\n{divider()}Please select if you want to show the quiz to the students\n{divider()}\n[ 1 ] Show\n[ 2 ] Do not show\n[ X ] Back to Menu\n{divider()}\n")
        if quiz_show_input.upper() == "X":
            return
        elif validation(quiz_show_input, "int"):
            continue
        match int(quiz_show_input):
            case 1:
                show_quiz = True
            case 2:
                show_quiz = False
        break
    
    # Add to quiz_setting
    data = {
        "course": selected_course, 
        "module_name": selected_module, 
        "quiz_name": input_quiz_name, 
        "assessment_component": input_asessment_component, 
        "time_in_minutes": quiz_time_input, 
        "maximum_number_of_attempts": max_attempt, 
        "randomize_option": randomize, 
        "show_quiz": show_quiz
        }
    input_list.append(data)
    server_process({"type": "admin_write_settings", "quiz_setting": input_list})

# Select the quiz setting you want to edit.
def edit_quiz_setting(input_list: list) -> int | bool:
    '''
    This function is used to select the quiz setting which you want to edit.
    Returns an integer value for the index of the quiz setting.

    Args:
        input_list (list) : Input for the quiz setting database.
    
    Returns: 
        (int | bool) : Returns int when a setting has been selected. Returns bool when exiting the selection.
    '''
    while True:
        content = f"{divider()}\n\t\t\033[1;37;40m Setting\033[0;37;40m\n{divider()}\n"
        content += "\tCourse\t|\tModule\t|\tQuiz\n"
        content += f"{divider()}\n"
        for i, element in enumerate(input_list):
            content += f"[ {i + 1} ]   {element['course']}\t|\t{element['module_name']}\t|\t{element['quiz_name']}\n"
        content += f"{divider()}\n\tSelect quiz setting to edit\n{divider()}\n[ X ] Back to Main\n{divider()}\n"
        check = get_input(content)
        if check.upper() == "X":
            return False
        elif validation(check, "int", len(input_list)):
            continue
        break
    setting_index = int(check) - 1
    # ensures that the variable can only be a bool and is equalled to "False"
    if setting_index == False and isinstance(setting_index, bool): 
        return False
    else:
        # This will be used to edit the selected quiz setting
        while True:
            # Prints out the edit settings screen of the selected quiz setting
            userInput = print_menu("setting", setting_index)  
            valueCap = userInput.upper()
            match valueCap:
                case "X": # Return to selection menu
                    return 
                case "1": # Add Setting
                    add_setting(input_list, setting_index)
                case "2": # Edit Setting
                    edit_setting(input_list, setting_index)
                case "3": # Delete Setting
                    delete_setting(input_list, setting_index)
                case _:
                    error_output("option")

# Deletes an existing quiz setting
def delete_quiz_setting(input_list: list):
    '''
    This function is used to delete an existing quiz setting.

    Args:
        input_list (list) : Input for the quiz setting database.
    '''
    while True:
        content = f"{divider()}\n\t\t\033[1;37;40m Setting\033[0;37;40m\n{divider()}\n"
        content += "\tCourse\t|\tModule\t|\tQuiz\n"
        content += f"{divider()}\n"
        for i, element in enumerate(input_list):
            content += f"[ {i + 1} ]   {element['course']}\t|\t{element['module_name']}\t|\t{element['quiz_name']}\n"
        content += f"{divider()}\n\tSelect quiz setting to delete\n{divider()}\n[ X ] Back to Main\n{divider()}\n"
        deleting_quiz_input = get_input(content)
        if deleting_quiz_input.upper() == "X":
            return 
        elif validation(deleting_quiz_input, "int", len(input_list)):
            continue
        while True:
            content = f"{divider()}\n\t\t\033[1;37;40m Setting\033[0;37;40m\n{divider()}\n"
            content += "\tCourse\t|\tModule\t|\tQuiz\n"
            content += f"{divider()}\n"
            content += f"[ {int(deleting_quiz_input)} ]   {input_list[int(deleting_quiz_input) - 1]['course']}\t|\t{input_list[int(deleting_quiz_input) - 1]['module_name']}\t|\t{input_list[int(deleting_quiz_input) - 1]['quiz_name']}\n"
            content += f"{divider()}\nPlease confirm that you're deleting the correct quiz. \n[NOTE] that this is permanent and cannot be undone.\n{divider()}\n[ C ] Confirm deletion\n[ X ] Back to Main\n{divider()}\n"
            confirm = get_input(content)
            if confirm.upper() == "X":
                return
            elif validation(confirm, "str"):
                continue
            elif confirm.upper() == "C":
                # Deletes selected quiz setting
                input_list.pop(int(deleting_quiz_input) - 1)
                # Sends the new edits to the server to update the database
                server_process({"type": "admin_write_settings", "quiz_setting": input_list})
                return

# [NOTE] Any additional setting added would need to be manually added for proper functionality
# Add new settings into "quiz_settings.json"
def add_setting(input_list: list, input_index: int):
    '''
    This functions can add specific quiz settings into the quiz_setting.json for certain quizzes.

    Args:
        input_list (list) : Input for the quiz setting database.
        input_index (int) : Used to specify which quiz setting is being edited.
    '''
    while True:
        new_setting_name = get_input(f"{divider()}\n\t\t\tAdding Setting\n{divider()}\nSetting Name: _\nSetting Value: \n{divider()}\n[ X ] Back to Menu\n{divider()}\n")
        if new_setting_name.upper() == "X":
            return
        elif validation(new_setting_name, "str"):
            continue
        break
    while True:
        new_setting_value = get_input(f"{divider()}\n\t\t\tAdding Setting\n{divider()}\nSetting Name: {new_setting_name}\nSetting Value: _\n{divider()}\n[ X ] Back to Menu\n{divider()}\n")
        if new_setting_value.upper() == "X":
            return
        elif validation(new_setting_name, "str"):
            continue
        break
    while True:
        finalCheck = get_input(f"{divider()}\n\t\t\tAdding Setting\n{divider()}\nSetting Name: {new_setting_name}\nSetting Value: {new_setting_value}\n{divider()}\n[ C ] Confirm\t\t[ X ] Exit\n{divider()}\n")
        if finalCheck.upper() == "X":
            return
        elif finalCheck.upper() == "C":
            # If the two checks above are valid, the new value would be added into the settings file.
            input_list[input_index][new_setting_name] = new_setting_value
            server_response = server_process({"type": "admin_write_settings", "quiz_setting": input_list})
            if server_response:
                get_input("\033[0;32;40mYour changes have been saved!\033[0;37;40m\nPress Enter to Continue\n", False)
        else:
            error_output("option")
            continue
        break

# Edits the varies quiz settings value from the server.py
def edit_setting(input_list: list, input_index: int):
    '''
    This functions can edit specific quiz settings into the quiz_setting.json for certain quizzes.

    Args:
        input_list (list) : Input for the quiz setting database.
        input_index (int) : Used to specify which quiz setting is being edited.
    '''
    while True:
        local_loop = True   # Used to loop through the quiz settings
        course_changed = False      # Used to check if the course has changed
        module_changed = False      # Used to check if the module has changed
        select_key = selection_of_setting("Editing Settings", input_list, input_index)
        if select_key.upper() == "X":
            return  

        # Get the values from the server to compared with the local values.
        # Check for the courses that are available in the server.
        server_response = server_process({"type": "admin_fetch_specific_setting", "setting": "course"})
        if input_list[input_index][select_key] in server_response:
            course_string = ""
            for i, course in enumerate(server_response):
                course_string += f"\n[ {i + 1} ] {course}"
            while local_loop:
                new_value = get_input(f"{divider()}\nName: {select_key}\nValue: \033[1;37;40m>>> {input_list[input_index][select_key]} <<<\033[0;37;40m\n{divider()}{course_string}\n[ X ] Back to Menu\n{divider()}\nPlease input new value: ")
                if new_value.upper() == "X":
                    local_loop = False   
                    break
                elif validation(new_value, "int", len(server_response)):
                    continue
                break
            while local_loop:
                confirm_change = get_input(f"{divider()}\n\t\tConfirm Changes?\n{divider()}\nName: {select_key}\nValue: \033[1;37;40m>>> {server_response[int(new_value) - 1]} <<<\033[0;37;40m\n{divider()}\n[ C ] Confirm \n[ X ] Cancel Changes\n{divider()}\n")
                if confirm_change.upper() == "X":
                    local_loop = False
                    break
                elif validation(confirm_change, "str"):
                    continue
                elif confirm_change.upper() == "C":
                    input_list[input_index][select_key] = server_response[int(new_value) - 1]
                    course_changed = True
                    select_key = 'module_name'  # Used to change the key to the next setting
                    break
                else:
                    error_output("input")
        
        # Check for the modules that are available for the selected course or if the course has been changed
        server_response = server_process({"type": "admin_fetch_specific_setting", "setting": "module", "course": input_list[input_index]['course']})
        if input_list[input_index][select_key] in server_response or course_changed:
            module_string = ""
            for i, course in enumerate(server_response):
                module_string += f"\n[ {i + 1} ] {course}"
            while local_loop:
                new_value = get_input(f"{divider()}\nName: {select_key}\nValue: \033[1;37;40m>>> {input_list[input_index][select_key]} <<<\033[0;37;40m\n{divider()}{module_string}\n[ X ] Back to Menu\n{divider()}\nPlease input new value: ")
                if new_value.upper() == "X":
                    local_loop = False   
                    break
                elif validation(new_value, "int", len(server_response)):
                    continue
                break
            while local_loop:
                confirm_change = get_input(f"{divider()}\n\t\tConfirm Changes?\n{divider()}\nName: {select_key}\nValue: \033[1;37;40m>>> {server_response[int(new_value) - 1]} <<<\033[0;37;40m\n{divider()}\n[ C ] Confirm \n[ X ] Cancel Changes\n{divider()}\n")
                if confirm_change.upper() == "X":
                    local_loop = False
                    break
                elif validation(confirm_change, "str"):
                    continue
                elif confirm_change.upper() == "C":
                    input_list[input_index][select_key] = server_response[int(new_value) - 1]
                    module_changed = True
                    select_key = 'assessment_component'
                    break
                else:
                    error_output("input")
        
        # Checks for the type of the setting that will be edited or if the module has been changed
        if isinstance(input_list[input_index][select_key], list) or module_changed:
            assessment_component_str = ""
            for i, element in enumerate(input_list[input_index][select_key]):
                assessment_component_str += f"\n[ {i + 1} ] {element['topic_name']}: {element['number_of_question']} questions"
            
            while local_loop:
                # Select the topic to edit
                selected_topic_index = get_input(f"{divider()}\nName: {select_key}\nTopics: \033[1;37;40m{assessment_component_str}\033[0;37;40m\n{divider()}\nPlease select a topic to edit\n{divider()}\n[ X ] Back to Menu\n{divider()}\n")
                if selected_topic_index.upper() == "X":
                    local_loop = False   
                    break
                elif validation(selected_topic_index, "int", len(input_list[input_index][select_key])):
                    continue
                break
            while local_loop:
                # Get the maximum number of questions for the selected topic
                server_response = server_process({"type": "admin_fetch_specific_setting", "setting": "assessment_component", "course": input_list[input_index]['course'], "module": input_list[input_index]['module_name']})
                # For easier readability.
                topic = input_list[input_index][select_key][int(selected_topic_index) - 1]
                new_value = get_input(f"{divider()}\nTopic: {topic['topic_name']}\nTotal Number of Qn for topic: {server_response[int(selected_topic_index) - 1]['max_number_of_questions']}\nNum of Qn: \033[1;37;40m>>> {topic['number_of_question']} <<<\033[0;37;40m\n{divider()}\n[ X ] Back to Menu\n{divider()}\nPlease input new value: ")
                if new_value.upper() == "X":
                    local_loop = False   
                    break
                # Validation for the new value, ensuring that is doesn't exceed the maximum number of question we have in the question pool
                elif validation(new_value, "int", server_response[int(selected_topic_index) - 1]['max_number_of_questions']): 
                    continue
                break

            while local_loop:
                confirm_change = get_input(f"{divider()}\n\t\tConfirm Changes?\n{divider()}\nTopic: {topic['topic_name']}\nNum of Qn: \033[1;37;40m>>> {new_value} <<<\033[0;37;40m\n{divider()}\n[ C ] Confirm \n[ X ] Cancel Changes\n{divider()}\n")
                if confirm_change.upper() == "X":
                    local_loop = False
                    break
                elif validation(confirm_change, "str"):
                    continue
                elif confirm_change.upper() == "C":
                    topic['number_of_question'] = int(new_value)
                    server_response = server_process({"type": "admin_write_settings", "quiz_setting": input_list}) 
                    if server_response:
                        get_input("\033[0;32;40mYour changes have been saved!\033[0;37;40m\nPress Enter to Continue\n", False)
                    return
                else:
                    error_output("input")
                continue
        elif isinstance(input_list[input_index][select_key], bool):
            while local_loop:
                new_value = get_input(f"{divider()}\nName: {select_key}\nValue: \033[1;37;40m>>> {input_list[input_index][select_key]} <<<\033[0;37;40m\n{divider()}\n[ 1 ] True\n[ 2 ] False\n[ X ] Back to Menu\n{divider()}\nPlease input new value: ")
                if new_value.upper() == "X":
                    local_loop = False 
                    break  
                elif validation(new_value, "int", 3):
                    continue
                match int(new_value):
                    case 1:
                        new_value = True
                    case 2:
                        new_value = False
                break
            while local_loop:
                confirm_change = get_input(f"{divider()}\n\t\tConfirm Changes?\n{divider()}\nName: {select_key}\nValue: \033[1;37;40m>>> {new_value} <<<\033[0;37;40m\n{divider()}\n[ C ] Confirm \n[ X ] Cancel Changes\n{divider()}\n")
                if confirm_change.upper() == "X":
                    local_loop = False
                    break
                elif validation(confirm_change, "str"):
                    continue
                elif confirm_change.upper() == "C":
                    input_list[input_index][select_key] = new_value
                    server_response = server_process({"type": "admin_write_settings", "quiz_setting": input_list}) 
                    if server_response:
                        get_input("\033[0;32;40mYour changes have been saved!\033[0;37;40m\nPress Enter to Continue\n", False)
                    return
                else:
                    error_output("input")
                continue
        elif isinstance(input_list[input_index][select_key], int):
            while local_loop:
                new_value = get_input(f"{divider()}\nName: {select_key}\nValue: \033[1;37;40m>>> {input_list[input_index][select_key]} <<<\033[0;37;40m\n{divider()}\n[ X ] Back to Menu\n{divider()}\nPlease input new value: ")
                if new_value.upper() == "X":
                    local_loop = False   
                    break
                elif validation(new_value, "int"):
                    continue
                break
            while local_loop:
                confirm_change = get_input(f"{divider()}\n\t\tConfirm Changes?\n{divider()}\nName: {select_key}\nValue: \033[1;37;40m>>> {new_value} <<<\033[0;37;40m\n{divider()}\n[ C ] Confirm \n[ X ] Cancel Changes\n{divider()}\n")
                if confirm_change.upper() == "X":
                    local_loop = False
                    break
                elif validation(confirm_change, "str"):
                    continue
                elif confirm_change.upper() == "C":
                    input_list[input_index][select_key] = int(new_value)
                    server_response = server_process({"type": "admin_write_settings", "quiz_setting": input_list}) 
                    if server_response:
                        get_input("\033[0;32;40mYour changes have been saved!\033[0;37;40m\nPress Enter to Continue\n", False)
                    return
                else:
                    error_output("input")
                continue
        elif isinstance(input_list[input_index][select_key], str):
            while local_loop:
                new_value = get_input(f"{divider()}\nName: {select_key}\nValue: \033[1;37;40m>>> {input_list[input_index][select_key]} <<<\033[0;37;40m\n{divider()}\n[ X ] Back to Menu\n{divider()}\nPlease input new value: ")
                if new_value.upper() == "X":
                    local_loop = False   
                    break
                elif validation(new_value, "str"):
                    continue
                break
            while local_loop:
                confirm_change = get_input(f"{divider()}\n\t\tConfirm Changes?\n{divider()}\nName: {select_key}\nValue: \033[1;37;40m>>> {new_value} <<<\033[0;37;40m\n{divider()}\n[ C ] Confirm \n[ X ] Cancel Changes\n{divider()}\n")
                if confirm_change.upper() == "X":
                    local_loop = False
                    break
                elif validation(confirm_change, "str"):
                    continue
                elif confirm_change.upper() == "C":
                    input_list[input_index][select_key] = new_value
                    server_response = server_process({"type": "admin_write_settings", "quiz_setting": input_list}) 
                    if server_response:
                        get_input("\033[0;32;40mYour changes have been saved!\033[0;37;40m\nPress Enter to Continue\n", False)
                    return
                else:
                    error_output("input")
                continue

# Deletes settings from "quiz_settings.json"
def delete_setting(input_list: list, input_index: int): 
    '''
    This functions can delete specific quiz settings into the quiz_setting.json for certain quizzes.

    Args:
        input_list (list) : Input for the quiz setting database.
        input_index (int) : Used to specify which quiz setting is being edited.
    '''
    while True:
        deleting_key = selection_of_setting("Deleting Setting", input_list, input_index) # will return a dictionary key
        if deleting_key == "X":
            return
        while True:
            delete_check = get_input(f"{divider()}\n\t\tPlease confirm your selection\n{divider()}\n[ - ] {deleting_key}: {input_list[input_index][deleting_key]}\n{divider()}\n[ C ] Confirm\t\t[ X ] Back to Menu\n{divider()}\n")
            # Check if the user wants to exit the menu
            if delete_check.upper() == "X":
                break
            elif validation(delete_check, "str"):
                continue
            elif delete_check.upper() == "C":
                input_list[input_index].pop(deleting_key)
                server_response = server_process({"type": "admin_write_settings", "quiz_setting": input_list})
                if server_response:
                    get_input("\033[0;31;40mOption has been deleted!\033[0;37;40m\nPress Enter to Continue\n", False)  
                break
            else:
                error_output("option")
                continue
        return

# Returns the key name of the selected item
def selection_of_setting(title: str, input_list: list, input_index: int):
    '''
    This function returns the key name of the selected item. The key name will be used in places 
    such as editing and deleting.

    Args:
        title (str) : Used for printing the title in the UI.
        input_list (list) : Input for the quiz setting database.
        input_index (int) : Used to specify which quiz setting is being edited.
    
    Returns:
        (str) : Returns either "X" or a key value.
    '''
    dict_list = list(input_list[input_index].keys())
    while True:
        value_number = get_input(f"{divider()}\n\t\t{title}\n{divider()}\n{view_file_content(1, 'setting', input_index)}{divider()}\n[ X ] Back to Menu\n{divider()}\n")
        # Check if the user wants to exit the menu
        if value_number.upper() == "X": 
            return "X"
        elif validation(value_number, "int", len(dict_list)):
            continue
        else:
            return dict_list[int(value_number) - 1]

# ========================================================================
#   Generate Report Functions
# ========================================================================

# Logical system for generating report
def generate_report_logic():
    data = generate_report()
    if data == False:
        return False

# Retrieving and generating a data report
def generate_report():
    
    question_pool = read_file(_QUESTION_POOL, "json")
    while True:
        course_list = []
        for course in question_pool:
            course_list.append(course['course'])

        print(course_list)
        available_courses = ""
        for i, item in enumerate(course_list):
            available_courses += f"\n[ { i + 1} ] {item}"
        course_index = get_input(f"{divider()}\n\t\tCourse Name\n{divider()}{available_courses}\n[ X ] Back to Menu\n{divider()}\n")
        if course_index.upper() == "X":
            return False
        elif validation(course_index, "int", len(course_list)):
            continue
        break

    while True:
        module_list = []
        for each_course in question_pool:
            if each_course['course'] != course_list[int(course_index) - 1]:
                continue
            for each_module in each_course['modules']:
                module_list.append(each_module['module_name'])
        print(module_list)
        available_modules = ""
        for i, item in enumerate(module_list):
            available_modules += f"\n[ { i + 1} ] {item}"
        module_name = get_input(f"{divider()}\n\t\tModule Name\n{divider()}{available_modules}\n[ X ] Back to Menu\n{divider()}\n")
        if module_name.upper() == "X":
            return False
        elif validation(module_name, "int", len(module_list)):
            continue
        break

    while True:
        topic_list = []
        for each_course in question_pool:
            if each_course['course'] != course_list[int(course_index) - 1]:
                continue
            for each_module in each_course['modules']:
                if each_module['module_name'] != module_list[int(module_name) - 1]:
                    continue
                for each_topic in each_module['topics']:
                    topic_list.append(each_topic['topic_name'])

        available_topics = ""
        for i, item in enumerate(topic_list):
            available_topics += f"\n[ { i + 1} ] {item}"
        assessment_component_index = get_input(f"{divider()}\n\t\tAssessment Component\n{divider()}{available_topics}\n[ X ] Back to Menu\n{divider()}\n")
        if assessment_component_index.upper() == "X":
            return False
        elif validation(assessment_component_index, "int", len(topic_list)):
            continue
        break

    setting = {"course": course_list[int(course_index) - 1], "module_name": module_list[int(module_name) - 1], "assessment_component": topic_list[int(assessment_component_index) - 1]}
    server_response = server_process({"type": "admin_previous_attempts", "quiz_setting": setting})

    content = ""
    if server_response == "no-attempts":
        content = "\nThere are no previous attempts."
        get_input(f"{divider()}\n\t\tView Attempts\n{divider()}{content}\n{divider()}\nPress Enter to return back...\n{divider()}\n")
        return
    else:
        for i, element in enumerate(server_response):
            content += f"\n[ {i + 1} ] {element['userID']} - {element['module']}: {element['quiz']}, Grade: {element['grade']}"
    while True:
        view_attempt = get_input(f"{divider()}\n\t\tView Attempts\n{divider()}{content}\n{divider()}\n[ X ] Back to Menu\n{divider()}\n")
        if view_attempt.upper() == "X":
            return
        elif validation(view_attempt, "int", len(server_response)):
            continue
        attempt_data = server_response[int(view_attempt) - 1]
        no_of_qn =  int(attempt_data['qn-answered-correct']) + int(attempt_data['qn-answered-wrong'])
        get_input(f"{divider()}\n\t\t{attempt_data['userID']}'s Attempt\n{divider()}\nCourse: {attempt_data['course']}\nModule: {attempt_data['module']}\nQuiz: {attempt_data['quiz']}\n\nScore: \033[4;31;40m{attempt_data['total-marks']}/{attempt_data['total-possible-marks']}\033[0;37;40m\nGrade: \033[4;31;40m{attempt_data['grade']}\033[0;37;40m\n{divider()}\nPress Enter to Continue...", False)
        for i in range(no_of_qn):
            get_input(f"{divider()}\n\t\t{attempt_data['userID']}'s Attempt\n{divider()}\nQ{i + 1}: {attempt_data['question-' + str(i + 1)]}\n\nYour Answer: \033[4;31;40m{attempt_data['user-answer-' + str(i + 1)]}\033[0;37;40m\n{divider()}\nPress Enter to Continue...", False)

# ========================================================================
#   Sub Program Loops
# ========================================================================
def user_config_subloop(input_loop: bool):
    while input_loop:
        check = user_config_logic()
        if check == False:
            input_loop = False

def course_info_subloop(input_loop: bool):
    while input_loop:
        check = course_logic()
        if check == False:
            input_loop = False

def quiz_setting_subloop(input_loop: bool):
    while input_loop:
        check = setting_logic()
        if check == False:
            input_loop = False

def generate_report_subloop(input_loop: bool):
    while input_loop:
        check = generate_report_logic()
        if check == False:
            input_loop = False

# ========================================================================
#   Login Page Functions
# ========================================================================

# Prompts a Admin login upon loading of the program
def login_menu():
    # plaintext is "1Qwer$#@!" w/o quotations. [For Reference purposes]
    password_hashed = "cf1274bedc756b5335653619ecd82fc16171ccecf5e687c7aeafae41e750d768" 

    loop = True
    while loop:
        userInput = get_input(f"{divider()}\n\t\t\033[1;37;40mAdmin Login Page\033[0;37;40m\n{divider()}\n[ X ] Exit Program\n{divider()}>>>", False)
        if userInput.upper() == "X":
            while True:
                userConfirm = get_input(f"{divider()}\n\033[1;37;40m\t\tAre you sure want to quit?\033[0;37;40m\n{divider()}\n[ Y ] Yes\t\t[ N ] No\n{divider()}\n")
                if userConfirm.upper() == "Y":
                    print("\033[0;32;40mGoodbye\033[0;37;40m")
                    loop = False
                    return False
                elif userConfirm.upper() == "N":
                    return
                else:
                    error_output("option")
        # checks for the correct password
        elif user_password_hashing(userInput) == password_hashed:
            getpass.getpass("\033[1;37;42mLogin was successful!\033[0;37;40m")
            main_menu(main_loop=True)
        else:
            error_output("login_failed")  
    

# Try loop is used in order to catch any bad inputs the user might have done within the stack
def main_menu(main_loop: bool):
    while main_loop:
        string = print_main(MAIN_MENU)
        check_variable = main_logic(string)
        if check_variable == False:  # execute if value is False
            main_loop = False

# ========================================================================
#   Main Program Loop
# ========================================================================

def main():
    while True:
        try:
            loop = login_menu()
            main_menu(loop)
            if loop == False:
                break 
        except:
            input(traceback)
            error_output("bad_input")

if __name__ == "__main__":
    main()
