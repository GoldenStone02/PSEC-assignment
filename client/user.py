# StudentID:	p2008493
# Name:	        Ng Jun Han
# Class:		DISM/FT/1B/05   
# Assessment:	CA1 
# 
# Script name:	user.py
# 
# Purpose:	The purpose of the script is for the user to take a quiz whilst needing little knowledge on 
#           knowing how to operate the quiz. With the script also storing the user's attempt data for later
#           analysis by the administrator.
#
# Usage syntax:	Run with play button / command line, eg. py read-cmd-line 1 2 3
# 
# Input file:   
# 
# 
# Output file:  
# 
# 
# Python ver:	Python 3
#
# Reference:	This program is adapted from the following:
#                   a) Generating non-repeating random numbers in Python
#                   https://www.tutorialspoint.com/How-to-generate-non-repeating-random-numbers-in-Python
# 
#                   b) Python time ctime() method
#                   https://www.tutorialspoint.com/python/time_ctime.htm
# 
#                   c) w3schools -Python random shuffle() method
#                   https://www.w3schools.com/python/ref_random_shuffle.asp
# 
#                   d) How to read and create csv files using python
#                   https://linuxconfig.org/how-to-read-and-create-csv-files-using-python
#                   
# Library/
# package/	
# Module /      sys, socket, os, traceback, threading, re, hashlib, time, json, getpass
#
# Known issues:	N/A

import sys, socket, traceback
import os
import re
import hashlib
import time
import json
import getpass

# ==============================================================================================================================
#   Initialize variables
# ==============================================================================================================================

EMPTY = ""

MAIN_USER_MENU = ["Log In", "Register User", "Reset Password"]

PATTERN = r"^[\w]+$"
EMAIL_PATTERN = r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+"
PASSWORD_PATTERN = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%]).+$'

# ==============================================================================================================================
#   Socket Programming Functions
# ==============================================================================================================================

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
        processed_input (any) : Outputs the processed socket server's response
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
    # print(f"[CONNECTION ESTABLISHED] Connected to {HOST}:{PORT}")

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
        received_message = json.loads(client.recv(5120))
        # print(f"[PROCESS] {HOST}:{PORT}, Packet type: {received_message['type']}")
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
    # print(f"[EXITED] Connection to {HOST}:{PORT} Exited")

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
        case "available_courses":
            output = server_response['data']
        case "reset_pw_status":
            if server_response['data'] == "success":
                output = True
            else:
                output = False
        case "login_status":
            if server_response['data'] == "success":
                output = True
            else:
                output = False
        case "returned_quiz_settings":
            output = server_response['data']
        case "returned_question_pool":
            output = server_response['data'] 
        case "returned_no_of_attempts":
            output = server_response['data']
        case "user_results":
            output = server_response['data']
        case "previous_attempts":
            output = server_response['data']
        case _:
            input("Error")
    return output

# ==============================================================================================================================
#   General Functions
# ==============================================================================================================================

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
                    error_output("option")
                    return True
        case "email":
            if not re.search(EMAIL_PATTERN, user_input):
                error_output("email")
                return True
        case "password":
            if not re.search(PASSWORD_PATTERN, user_input):
                error_output("password")
                return True
        case "attempts":
            if user_input == "unlimited":
                pass
            if isinstance(user_input, int) and user_input <= 0:
                error_output("no_attempts")
                return True
        case _:
            pass
    return False

# Used for easy maintainence of error outputs
def error_output(error_type: str):
    '''
    This function proccesses error_type and return an error message.

    Args:
        error_type (str) : type of error (Default - None).
    '''
    match error_type:
        case "option":             # Wrong option selected
            string = "\033[1;37;41mPlease select a valid option.\033[0;37;40m"

        case "empty_input":        # Empty input
            string = "\033[1;37;41mEmpty input, please try again\033[0;37;40m"

        case "input":              # Invalid input
            string = "\033[1;37;41mPlease enter a valid input.\033[0;37;40m"

        case "special":            # Input field can't contain special characters 
            string = "\033[1;37;41mInput value can't contain special characters!\033[0;37;40m\n"

        case "email":              # Email is not found in database             [Unique to user.py]
            string = "\033[1;37;41mEmail is not linked to userID\033[0;37;40m"

        case "incorrect":          # The userID or password is incorrect        [Unique to user.py]
            string = "\033[1;37;41mUserID or password is incorrect. Please try again\033[0;37;40m"

        case "username_match":     # Same username is found in the database        
            string = "\033[1;37;41mUsername exists already, please try another name\033[0;37;40m\n"

        case "password":           # Doesn't meet the password criteria  
            string = "\033[1;37;41mMissing one of the criteria listed below, please try again\033[0;37;40m\nAt least one number\nAt least one uppercase and one lowercase character\nAt least one special symbol !@#$%\nShould be 4 - 20 characters long\n"

        case "pw_not_same":        # The passwords are not the same
            string = "\033[1;37;41mPasswords are not the same.\033[0;37;40m\n"

        case "reset_password":     # Reset password was not
            string = "\033[1;37;41mPasswords are not the same.\033[0;37;40m\n"

        case "admin":              # Occurs when user enters wrong password 3 times
            string = "\033[1;37;41mSession Timed Out. Restarting Program\033[0;37;40m"

        case "user_alr_exist":     # User already exist in the database
            string = "\033[1;37;41mUser already exist in the database!\033[0;37;40m"

        case "previous":           # No more questions in front of selected question
            string = "\033[1;37;41mYou are at the first question!!\033[0;37;40m"
    
        case "next":               # No more questions after selected question
            string = "\033[1;37;41mYou are at the last question!!\033[0;37;40m"
    
        case "no_attempts":        # No more attempts remaining  
            string = "\033[1;37;41mYou have no remaining attempt\033[0;37;40m"
    
        # Not in use currently
        case "bad_input":          # Bad Input --> Refers to EOFERROR (Occurs only when CTRL+Z is inputted)
            string = "\033[1;37;41mBad Input, program restarted\033[0;37;40m"
    getpass.getpass(string, False)

# Used to create a dynamic divider that changes size according to the size of the terminal
def divider():
    '''
    Returns a dynamic divider depending on the size of the terminal.
    '''
    column, row = os.get_terminal_size()
    output = f"{EMPTY:-^{column}}"
    return output

# ===========================================================================================================================
#   User Page Function
# ===========================================================================================================================

# Returns user navigation menu
def user_menu(inputList: list):
    content = f"{divider()}\n\t\t\t\033[1;37;40m Main \033[0;37;40m\n{divider()}\n"
    for i, element in enumerate(inputList):
        content += f"[ {i+1} ] {element}\n"
    content += f"[ X ] Exit Application\n{divider()}\n"
    return content

# Logicial Flow for user menu
def user_logic():
    sub_loop = True
    while True:
        stored_value = get_input(user_menu(MAIN_USER_MENU))
        match stored_value.upper():
            case "X":
                while True:
                    userConfirm = get_input(f"{divider()}\n\033[1;37;40m\t\tAre you sure want to quit?\033[0;37;40m\n{divider()}\n[ Y ] Yes\t\t[ N ] No\n{divider()}\n")
                    if userConfirm.upper() == "Y":
                        print("\033[0;32;40mGoodbye\033[0;37;40m")
                        return False
                    elif userConfirm.upper() == "N":
                        break
                    else:
                        error_output("option")
            case "1":
                login_subloop(sub_loop)
            case "2":
                register_user_subloop(sub_loop)
            case "3":
                reset_subloop(sub_loop)
            case _:
                error_output("option")

# =========================================================================================================================
#   Menu Functions
# =========================================================================================================================

# Adds users to the backend server
def register_user():
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
                error_output("user_alr_exist")
        else:
            error_output("pw_not_same")

# Logging in to account
def login_menu():
    # Counter for number of attempts before a user's session is timed out 
    count = 3
    while count != 0:
        userID_input = get_input(f"{divider()}\n\t\t\tLog In\n{divider()}\nuserID: _\nPassword: \n{divider()}\n[ X ] Back to Menu\n{divider()}\nEnter your userID: ")
        if userID_input.upper() == "X":
            return False
        elif validation(userID_input, "str"):
            continue

        password_input = get_input(f"{divider()}\n\t\t\tLog In\n{divider()}\nuserID: {userID_input} \nPassword: _\n{divider()}\n[ X ] Back to Menu\n{divider()}\nEnter your password: ", False)
        if password_input.upper() == "X":
            return False
        elif validation(password_input, ""): # only checks for if the value is empty
            continue
        packet = {
            "type": "user_login",
            "userID": userID_input,
            "password": user_password_hashing(password_input)
        }
        server_response = server_process(packet)
        if server_response == True:     # Enter quiz menu after successful login
            while True:
                quiz_setting = show_quizzes(userID_input)
                check = quiz_selection_menu(userID_input, quiz_setting)
                if check == False:
                    return
        else:
            error_output("incorrect")
            count -= 1
    # Time out the user if he/she fails to input the correct password 
    if count == 0:
        os.system("cls")
        error_output("admin")
        return False

# Hashes the password for safe keeping in the .csv file
def user_password_hashing(given_input: str): 
    output = hashlib.sha256(given_input.encode())
    return output.hexdigest()

# Resets the user password if they can provide their email
def reset_password():
    while True:
        userID_input = get_input(f"{divider()}\n\t\tReset Password\n{divider()}\nuserID: _\nReset Email:\nPassword:\n{divider()}\n[ X ] Back to Menu\n{divider()}\n")
        if userID_input.upper() == "X":
            return False
        elif validation(userID_input, "str"):
            continue
        break
    while True:
        email_input = get_input(f"{divider()}\n\t\tReset Password\n{divider()}\nuserID: {userID_input}\nReset Email: _\nPassword:\n{divider()}\n[ X ] Back to Menu\n{divider()}\n")
        if email_input.upper == "X":
            return False
        elif validation(email_input, "email"):
            continue
        break
    while True:
        password_input = get_input(f"{divider()}\n\t\tReset Password\n{divider()}\nuserID: {userID_input}\nReset Email: {email_input}\nPassword: _\n{divider()}\n[ X ] Back to Menu\n{divider()}\n", False)
        if password_input.upper() == "X":
            return False
        elif validation(password_input, "password"):
            continue
        verify_pw_input = get_input(f"{divider()}\n\t\tReset Password\n{divider()}\nuserID: {userID_input}\nReset Email: {email_input}\nPassword: {len(password_input) * '*'}\n{divider()}\nPlease Re-enter your password\n", False)
        if verify_pw_input.upper() == "X":
            return False
        elif password_input == verify_pw_input:
            packet = {
                "type": "reset_password",
                "userID": userID_input,
                "email": email_input,
                "password": user_password_hashing(password_input)
            }
            server_response = server_process(packet)
            if server_response:
                getpass.getpass("Password for user has been successfully resetted")
                return False
            else:
                error_output("reset_password")
        else:
            error_output("pw_not_same")

# ========================================================================================================================
#   Quiz Functions
# ========================================================================================================================

# Show all the available quizzes
def show_quizzes(userID: str) -> dict:
    '''
    This function fetches and checks for the available quizzes for the user for their appropriate course.
    The user would then select a quiz to enter.
    Returns the quiz setting for the user's selected quiz.

    Args: 
        userID (str) : UserID of logged in user.
    
    Returns:
        (dict) : Returns the selected quiz setting data.
    '''
    # Returns only the data portion of the dictionary packet.
    quiz_settings_list = server_process({"type": "quiz_settings", "userID": userID})
    quiz_list = ""
    for i, quiz in enumerate(quiz_settings_list):
        quiz_list += f"\n[ {i + 1} ] {quiz['module_name']} - {quiz['quiz_name']}"
    while True:
        user_input = get_input(f"{divider()}\n\t\tQuiz Menu\n{divider()}\nLogged In as: \033[1;37;40m{userID}\033[0;37;40m\nCourse: \033[1;37;40m{quiz_settings_list[0]['course']}\033[0;37;40m\n{quiz_list}\n[ X ] Back to Menu\n{divider()}\n")
        if user_input.upper() == "X":
            return False
        elif validation(user_input, "int", len(quiz_settings_list)): 
            # continues if there is an error detected with the value
            continue
        return quiz_settings_list[int(user_input) - 1]

# Display the quiz menu for the user before starting.
def quiz_selection_menu(userID: str, quiz_setting: dict | bool):
    if quiz_setting == False:   # Exit function if the previous function returned an exit 
        return False
    components = ""
    total_no_of_qn = 0
    for i in quiz_setting['assessment_component']:
        components += f"\t- {i['topic_name']}\n"
        total_no_of_qn += i['number_of_question']
    while True:
        num_of_attempts_left = check_attempts(userID, quiz_setting)
        user_input = get_input(f"{divider()}\n\t\tQuiz Menu\n{divider()}\nLogged In as: \033[1;37;40m{userID}\033[0;37;40m\nModule: \033[1;37;40m{quiz_setting['module_name']}\033[0;37;40m\nQuiz: \033[1;37;40m{quiz_setting['quiz_name']}\033[0;37;40m\nAssessment Component: \n{components}\nNumber of Attempts Left: \033[4;31;40m{num_of_attempts_left}\033[0;37;40m\nTime for the quiz: \033[4;31;40m{quiz_setting['time_in_minutes']} mins\033[0;37;40m\nNumber of Question: \033[4;31;40m{total_no_of_qn}\033[0;37;40m\n{divider()}\n[ 1 ] Start Quiz\n[ 2 ] View Previous Attempts\n[ X ] Back to Menu\n{divider()}\n")
        if user_input.upper() == "X":   # Exits back to the quiz selection
            return
        elif validation(user_input, "int", 2):
            continue
        elif user_input == "1":
            if validation(num_of_attempts_left, "attempts"):
                continue
            start_quiz(userID, quiz_setting) # Starts the quiz once the user confirms
        elif user_input == "2":
            view_previous_attempts(userID, quiz_setting)
        else:
            input("what")

# Checks if the user has sufficient attempts
def check_attempts(userID: str, quiz_setting: dict) -> int:
    server_response = server_process({"type": "show_attempts", "userID": userID, "quiz_setting": quiz_setting})
    return server_response

def check_options(user_input: str, current_question: dict) -> bool:
    '''
    This function checks if the input value in within the range of the options. E.g. range is "a" to "d", so it'll only accept values in that range

    Args:
        user_input (str) : Selected option by the user
        current_question (dict) : Used to find the range of the options

    Returns:
        (bool) : Returns True if option is found, else return False
    '''
    string = ""
    for i in range(len(current_question['options'])):
        string += f"{chr(ord('a') + i)}"
    if user_input in string:
        return True
    error_output("option")
    return False

def format_question_data(question_pool: list, question_index: int) -> str:
    '''
    This function formats the inputted question data into a question.

    Args:
        question_pool (list) : The question data retrieved from the server.
        index (int) : Selected index of the question pool.
    
    Returns:
        (str) : Formatted String
    '''
    string = f"{question_pool[question_index]['question_name']}"
    for alpha, option in enumerate(question_pool[question_index]['options']):
        string += f"\n  {chr(ord('a') + alpha)}) {option}"
    return string

def quiz_menu(userID: str, quiz_setting: dict, question_pool: list):
    '''
    This functions shows the quiz menu, where the user engages with the quiz.

    Args:
        userID (str) : Used as user submission details
        quiz_setting (dict) : Used as quiz submission details
        question_pool (list) : Used for storing of user's answers and submission 

    Returns:
        (bool) : If quiz was successfully submitted, return True. Else, return False
    '''
    current_question = 0                        # index for the first question
    last_question = len(question_pool) - 1      # index for last question
    start_time = time.time()
    while True:
        timer = start_timer(start_time, quiz_setting['time_in_minutes'])
        if timer[0] <= 0 and timer[1] <= 0:
            # Automatically exits and submit the quiz answers.
            get_input("Time's up", False)
            submit(userID, quiz_setting, question_pool, True)
            return
        if question_pool[current_question]['user_answer'] == None:
            context = ""
        else:
            context = f"\nYour Answer: {question_pool[current_question]['user_answer']}"
        user_input = get_input(f"{divider()}\n\t\t{quiz_setting['course']}: {quiz_setting['quiz_name']}\n{divider()}\nTime Left: {timer[0]} min {timer[1]} sec\n\n{format_question_data(question_pool, current_question)}\n{context}\n{divider()}\n[ P ] Previous\t[ N ] Next\n[ S ] Submit\n{divider()}\n")

        if validation(user_input, "str"):   
            continue
        elif user_input.upper() == "P":
            if current_question == 0:
                error_output("previous")
                continue
            else:
                current_question -= 1
        elif user_input.upper() == "N":
            if current_question == last_question:
                error_output("next")
                continue
            else:
                current_question += 1
        elif user_input.upper() == "S":
            # User requested to submit the answers.
            check = submit(userID, quiz_setting, question_pool)
            if check: return
        # Saves user's selected option
        elif check_options(user_input, question_pool[current_question]):    
            question_pool[current_question]['user_answer'] = question_pool[current_question]['options'][ord(user_input) - ord("a")]
            if current_question != last_question:
                current_question += 1
            else:
                # Prompt user submit when at the last question
                check = submit(userID, quiz_setting, question_pool)
                if check: return
        else:
            continue

# Checks and submits the user's answers to the server for processing
def submit(userID: str, quiz_setting: dict, question_pool: list, time_up: bool = False):
    '''
    This functions processes the submission details such as userID, quiz setting and question pool
    before sending it to the server. If there are any unanswered questions, it would confirm with the 
    user before the attempt is submitted.

    Args:
        userID (str) : Used to keep track of user's attempts.
        quiz_setting (dict) : Used to know what were the configurations to the quiz.
        question_pool (list) : Question list where the user's answers are stored.
        time_up (bool) : If True, time is up and user doesn't need to confirm to submit the quiz

    Returns:
        (bool) : If user wants to return to the quiz, return False. Else, return True
    '''
    if time_up:     # If timer is up, immediately submit the user's answers.
        data = {
            "type": "submitted_user_attempt",
            "userID": userID,
            "quiz_setting": quiz_setting,
            "user_answer": question_pool
        }
        user_results = server_process(data)
        show_results(userID, quiz_setting, user_results)
    else:
        # show the unanswered questions if there are any.
        qn_completed_list = ""
        no_of_incompleted = 0
        for i, element in enumerate(question_pool):
            if element['user_answer'] is None:
                qn_completed_list += f"\n\tQ{i + 1} [   ]"
                no_of_incompleted += 1
            else:
                qn_completed_list += f"\n\tQ{i + 1} [ x ]"
        while True:
            submit = get_input(f"{divider()}\n\t\tConfirm Submission\n{divider()}Completed Questions:{qn_completed_list}\n{divider()}\n[ C ] Confirm Submission\n[ X ] Cancel Submission\n{divider()}\n")
            if validation(submit, "str"):
                continue
            elif submit.upper() == "X":
                return False
            elif submit.upper() == "C":
                data = {
                    "type": "submitted_user_attempt",
                    "userID": userID,
                    "quiz_setting": quiz_setting,
                    "user_answer": question_pool
                }
                user_results = server_process(data)
                show_results(userID, quiz_setting, user_results)
                return True
            else:
                error_output("input")

# Starts the quiz for the signed user.
def start_quiz(userID: str, quiz_setting: dict):
    # Fetch the server for a list of random question that matches the quiz criteria
    question_pool = server_process({"type": "question_pool", "data": quiz_setting})
    quiz_menu(userID, quiz_setting, question_pool)

def view_previous_attempts(userID: str, quiz_setting: dict):
    '''
    This function is used to see the user's previous attempts at a particular quiz.

    Args:
        userID (str) : Used to filter for that user's previous attempts
        quiz_setting (dict) : Used to find what quiz the user was taking

    '''
    content = ""
    server_response = server_process({"type": "previous_attempts", "userID": userID, "quiz_setting": quiz_setting})
    if server_response == "no-attempts":
        content = "\nThere are no previous attempts."
        get_input(f"{divider()}\n\t\tView Attempts\n{divider()}{content}\n{divider()}\nPress Enter to return back...\n{divider()}\n")
        return
    else:
        for i, element in enumerate(server_response):
            content += f"\n[ {i + 1} ] Attempt {i + 1} - {element['module']}: {element['quiz']}, Grade: {element['grade']}"
    while True:
        view_attempt = get_input(f"{divider()}\n\t\tView Attempts\n{divider()}{content}\n{divider()}\n[ X ] Back to Menu\n{divider()}\n")
        if view_attempt.upper() == "X":
            return
        elif validation(view_attempt, "int", len(server_response)):
            continue
        attempt_data = server_response[int(view_attempt) - 1]
        no_of_qn =  int(attempt_data['qn-answered-correct']) + int(attempt_data['qn-answered-wrong'])
        get_input(f"{divider()}\n\t\tAttempt #{view_attempt}\n{divider()}\nModule: {attempt_data['module']}\nQuiz: {attempt_data['quiz']}\n\nScore: \033[4;31;40m{attempt_data['total-marks']}/{attempt_data['total-possible-marks']}\033[0;37;40m\nGrade: \033[4;31;40m{attempt_data['grade']}\033[0;37;40m\n{divider()}\nPress Enter to Continue...", False)
        for i in range(no_of_qn):
            get_input(f"{divider()}\n\t\tAttempt #{view_attempt}\n{divider()}\nQ{i + 1}: {attempt_data['question-' + str(i + 1)]}\n\nYour Answer: \033[4;31;40m{attempt_data['user-answer-' + str(i + 1)]}\033[0;37;40m\n{divider()}\nPress Enter to Continue...", False)

def show_results(userID: str, quiz_setting: dict, server_response: dict):
    '''
    This function will show the current user their results for the quiz they just took.

    Args:
        userID (str) : UserID that will be used to search for the quiz.
        quiz_setting (dict) : Used 
        server_response (dict) : User's score for the quiz.
    '''
    print(server_response[2], server_response[3])
    grade = server_response[2]/server_response[3] * 100
    get_input(f"{divider()}\n\t\tResults\n{divider()}\nLogged In as: \033[1;37;40m{userID}\033[0;37;40m\nModule: \033[1;37;40m{quiz_setting['module_name']}\033[0;37;40m\nQuiz: \033[1;37;40m{quiz_setting['quiz_name']}\033[0;37;40m\n\nGrade: {grade:.2f}\nScore: {server_response[2]}/{server_response[3]}\n{divider()}\nPress Enter to Continue\n", False)

# Returns the remaining time left in a tuple
def start_timer(starting_time: float, allowed_in_minutes: int):
    endtime = time.time() - starting_time
    total_allowed_time_in_sec = float(allowed_in_minutes) * 60
    time_left_min = int((total_allowed_time_in_sec - endtime)/60)
    time_left_sec = int((((total_allowed_time_in_sec - endtime)/60) - time_left_min) * 60)
    return time_left_min, time_left_sec

# ==============================================================================================================================
#   Sub Program Loop
# ==============================================================================================================================
def register_user_subloop(subloop: bool):
    while subloop:
        check = register_user()
        if check == False:
            subloop = False

def login_subloop(sub_loop: bool):
    while sub_loop:
        check = login_menu()
        if check == False:
            sub_loop = False
    
def reset_subloop(sub_loop: bool):
    while sub_loop:
        check = reset_password()
        if check == False:
            sub_loop = False

# ==============================================================================================================================
#   Main Program Loop
# ==============================================================================================================================
# Try loop is used in order to catch any bad inputs the user might have done within the stack
def main():
    main_loop = True
    while main_loop:
        check = user_logic()
        if check == False:
            main_loop = False

if __name__ == "__main__":
    main()
