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
# Output file:  C:\PSEC_project\users.json
#               C:\PSEC_project\quiz_results.csv
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
# Module /      sys, socket, os, traceback, threading, re, hashlib, random, csv, time, json, getpass
#
# Known issues:	N/A

import sys, socket, os, traceback
import threading
import re, hashlib, random, csv
import time
import json
import getpass

# ==============================================================================================================================
#   Initialize variables
# ==============================================================================================================================

dictionary = {}
csv_dict_list = []

EMPTY = ""

MAIN_USER_MENU = ["Register User", "Log In", "Reset Password"]
START_MENU = ["Begin Quiz"]

PASSWORD_PATTERN = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%]).+$'

_USERNAME_AND_PASSWORD = "./server/users.json"
_QUIZ_SETTING = "./server/quiz_settings.json"
_COURSE_INFORMATION = "./server/question_pool.json"
_QUIZ_RESULTS = "./server/quiz_results.csv"

# ==============================================================================================================================
#   Socket Programming Functions
# ==============================================================================================================================

HOST = "127.0.0.1"
PORT = 8181

def server_process(packet_input: dict):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  
    connect_to_server(client)
    server_response = send_to_server(packet_input, client)
    exit_server(client)
    processed_input = process_input(server_response)
    return processed_input

def connect_to_server(client):
    try:
        client.connect((HOST, PORT))
    except:
        print("Connection Error")
        print(traceback.format_exc())
        sys.exit()
    print(f"[CONNECTION ESTABLISHED] Connected to {HOST}:{PORT}")

def send_to_server(user_input, client):
    connected = True
    while connected:
        if len(user_input) > 0:
            client.sendall(json.dumps(user_input).encode("utf8"))
        else:
            print("Message can't be empty")
            continue    # Skips the bottom commands
        connected = False
        received_message = json.loads(client.recv(5120))
        print(f"[PROCESS] {HOST}:{PORT}, Packet type: {received_message['type']}")
        return received_message

def exit_server(client):
    # Sends a quit packet to close the connection
    quit_connection = {"type":"quit"}
    client.sendall(json.dumps(quit_connection).encode("utf8"))
    print(f"[EXITED] Connection to {HOST}:{PORT} Exited")

# Processes the server_response 
def process_input(server_response):
    input(server_response)
    match server_response['type']:
        case "Login Failed":
            return False
        case "Login Success":
            return True
        case "Quiz Settings":
            pass
        case "Question Pool":
            pass
        case "Results":
            pass
        case _:
            input("Error")
    return server_response

# ==============================================================================================================================
#   General Functions
# ==============================================================================================================================

# Reads and empties value into "dictionary" variable
# "option" parameter used to define what format it should print in
def read_file(file: str, option):
    if option == "csv":
        csv_dict_list = []
        with open(file, 'r') as csvfile:
            # Uses DictReader for easy storing of the value
            for line in csv.DictReader(csvfile):
                csv_dict_list.append(dict(line))
    elif option == "json":
        # Loading of JSON file into the program
        with open(file,"r") as f:
            file_content = json.load(f)
        
        return file_content

# Writes into a csv file with the given inputs.
def write_csv(file: str, dict_input: dict):
    # Fieldnames are the key values of the first item in the dictionary.
    fields = dict_input[0].keys()

    # Writes to the csv file with the correct headings and value
    with open(file, "w", newline="") as csvfile:
        csvwriter = csv.DictWriter(csvfile, fieldnames=fields)
        csvwriter.writeheader()
        csvwriter.writerows(dict_input)

# Used for easy maintainence of error outputs
def error_output(error_message: str):
    string = ""
    if error_message == "option":               # Wrong option selected
        string += "\033[1;37;41mPlease select a valid option.\033[0;37;40m"

    elif error_message == "empty_input":        # Empty input
        string += "\033[1;37;41mEmpty input, please try again\033[0;37;40m"

    elif error_message == "input":              # Invalid input
        string += "\033[1;37;41mPlease enter a valid input.\033[0;37;40m"

    elif error_message == "range":              # Input value not within range
        string += "\033[1;37;41mPlease enter a value within the range.\033[0;37;40m"

    elif error_message == "email":              # Email is not found in database        [Unique to user.py]
        string += "\033[1;37;41mEmail is not linked to userID\033[0;37;40m"

    elif error_message == "incorrect":          # The userID or password is incorrect   [Unique to user.py]
        string += "\033[1;37;41mUserID or password is incorrect. Please try again\033[0;37;40m"

    elif error_message == "short":              # Input value was too short
        string += "\033[1;37;41mLength of input was too short\033[0;37;40m\n"

    elif error_message == "long":               # Input value was too long                      
        string += "\033[1;37;41mLength of input was too long\033[0;37;40m\n"

    elif error_message == "password":           # Doesn't meet the password criteria  
        string += "\033[1;37;41mMissing one of the criteria, please try again\033[0;37;40m\n"

    elif error_message == "admin":              # Occurs when user enters wrong password 3 times
        string += "\033[1;37;41mSession Timed Out. Restarting Program\033[0;37;40m"

    elif error_message == "previous":           # No more questions in front of selected question
        string += "\033[1;37;41mYou are at the first question!!\033[0;37;40m"
    
    elif error_message == "next":               # No more questions after selected question
        string += "\033[1;37;41mYou are at the last question!!\033[0;37;40m"
    
    elif error_message == "no_attempts":        # No more attempts remaining  
        string += "\033[1;37;41mYou have no remaining attempt\033[0;37;40m"
    
    elif error_message == "bad_input":          # Bad Input --> Refers to EOFERROR (Occurs only when CTRL+Z is inputted)
        string += "\033[1;37;41mBad Input, program restarted\033[0;37;40m"
    
    input(string)

# Used to create a dynamic divider that changes size according to the size of the terminal
def dynamic_divider():
    column, row = os.get_terminal_size()
    output = f"{EMPTY:=^{column}}"
    return output
    
# ===========================================================================================================================
#   User Page Function
# ===========================================================================================================================

# Returns user navigation menu
def user_menu(inputList: list):
    content = f"{dynamic_divider()}\n\t\t\t\033[1;37;40m Main \033[0;37;40m\n{dynamic_divider()}\n"
    for i, element in enumerate(inputList):
        content += f"[ {i+1} ] {element}\n"
    content += f"[ X ] Exit Application\n{dynamic_divider()}\n"
    return content

# Logicial Flow for user menu
def user_logic():
    sub_loop = True
    while True:
        os.system("cls")
        stored_value = input(user_menu(MAIN_USER_MENU))
        match stored_value.upper():
            case "X":
                while True:
                    os.system("cls")
                    userConfirm = input(f"{dynamic_divider()}\n\033[1;37;40m\t\tAre you sure want to quit?\033[0;37;40m\n{dynamic_divider()}\n[ Y ] Yes\t\t[ N ] No\n{dynamic_divider()}\n")
                    if userConfirm.upper() == "Y":
                        print("\033[0;32;40mGoodbye\033[0;37;40m")
                        return False
                    elif userConfirm.upper() == "N":
                        break
                    else:
                        error_output("option")
            case "1":
                register_user_subloop(sub_loop)
            case "2":
                login_subloop(sub_loop)
            case "3":
                reset_subloop(sub_loop)
            case _:
                error_output("option")


# =========================================================================================================================
#   Menu Functions
# =========================================================================================================================

# Adds users to the backend server
def register_user():
    return False

# Log In Logicial Flow
def login_menu():
    # Counter for number of attempts before a user's session is timed out 
    count = 3
    while count != 0:
        os.system("cls")
        username_input = input(f"{dynamic_divider()}\n\t\t\tLog In\n{dynamic_divider()}\nUserID: \nPassword: \n{dynamic_divider()}\n[ X ] Back to Menu\n{dynamic_divider()}\nEnter your userID: ")
        if username_input.upper() == "X":
            return False
        elif username_input == "":
            error_output("empty_input")
            continue

        os.system("cls")
        password_input = getpass.getpass(f"{dynamic_divider()}\n\t\t\tLog In\n{dynamic_divider()}\nUserID: {username_input} \nPassword: \n{dynamic_divider()}\n[ X ] Back to Menu\n{dynamic_divider()}\nEnter your password: ")
        if password_input.upper() == "X":
            return False
        elif password_input == "":
            error_output("empty_input")
            continue
        
        packet = {
            "type": "user_login",
            "userID": username_input,
            "password": user_password_hashing(password_input)
        }
    
        server_response = server_process(packet)
        if server_response == True:     # Enter quiz menu after successful login
            input("SUCCESS")
        else:
            error_output("incorrect")
            count -= 1

    # Time out the user if he/she fails to input the correct password 
    if count == 0:
        os.system("cls")
        error_output("admin")
        return False

def check_username():
    # placeholder function before removing it
    pass

# Check if email exist in the file
def check_email(email: str, input_dict: dict):
    for i in input_dict:
        if email == i["email"]:
            return True
    return False

# Hashes the password for safe keeping in the .csv file
def user_password_hashing(given_input: str): 
    output = hashlib.sha256(given_input.encode())
    return output.hexdigest()


# Resets the user password if they can provide their email
def reset_password():
    read_file(_USERNAME_AND_PASSWORD, option="json")
    while True:
        os.system("cls")
        username_input = input(f"{dynamic_divider()}\n\t\tReset Password\n{dynamic_divider()}\nUserID:\nReset Email:\n{dynamic_divider()}\n[ X ] Back to Menu\n{dynamic_divider()}\n")
        if username_input.upper() == "X":
            return False
        elif username_input == "":
            error_output("empty_input")
            continue
        elif check_username(username_input):
            while True:
                os.system("cls")
                email_input = input(f"{dynamic_divider()}\n\t\tReset Password\n{dynamic_divider()}\nUserID:\t{username_input}\nReset Email:\n{dynamic_divider()}\n[ X ] Back to Menu\n{dynamic_divider()}\n")
                if email_input.upper() == "X":
                    return False
                elif email_input == "":
                    error_output("empty_input")
                    continue
                elif check_email(email_input):
                    input("\033[0;32;40mSuccess! You're authorize change your password\033[0;37;40m\nPress Enter to Continue\n")
                    password_change(username_input)
                    return
                else:
                    error_output("email")
                    continue
        else:
            error_output("username")

# Changes the password for the user
def password_change(username: str):
    # Password check
    while True:
        os.system("cls")
        password_input = input(f"{dynamic_divider()}\n\t\t\tReset Password\n{dynamic_divider()}\nPassword: \n{dynamic_divider()}\n[ X ] Back to Menu\n{dynamic_divider()}\nAt least one number\nAt least one uppercase and one lowercase character\nAt least one special symbol !@#$%\nShould be 4 - 20 characters long\nPassword: ")
        
        # Check if the user wants to exit the menu
        if password_input.upper() == "X":
            return
        elif password_input == "":
            error_output("empty_input")
            continue            
        elif len(password_input) < 4:
            error_output("short")
            continue
        elif len(password_input) > 20:
            error_output("long")
            continue
        elif not re.search(PASSWORD_PATTERN, password_input):
            error_output("password")
            continue
        break

    # Password double check
    while True:
        os.system("cls")
        password2 = input(f"{dynamic_divider()}\n\t\t\tReset Password\n{dynamic_divider()}\nPassword: \n{dynamic_divider()}\n[ X ] Back to Menu\n{dynamic_divider()}\nPlease re-enter your password: ")
        
        # Check if the user wants to exit the menu
        if password2.upper() == "X":
            return
        elif password2 == "":
            error_output("empty_input")
            continue
        elif password_input == password2:
            # Check if the user wants to confirm the setting
           while True:
                os.system("cls")
                confirm_change = input(f"{dynamic_divider()}\n\t\tReset Password\n{dynamic_divider()}\nPassword: {password_input}\n{dynamic_divider()}\n[ C ] Confirm Reset\n[ X ] Back to Menu\n{dynamic_divider()}\n")
                if confirm_change.upper() == "X":
                    SUB_LOOP = False
                    return
                elif confirm_change == "":
                    error_output("empty_input")
                    continue
                elif confirm_change.upper() == "C":
                    input("\033[0;32;40mYour password have been reset!\nPlease check your email for the new password.\033[0;37;40m\nPress Enter to Continue\n")
                    for user in csv_dict_list:
                        if username == user["userID"]:

                            # User's password is changed
                            user["password"] = user_password_hashing(password_input)

                    # Writes the new password 
                    write_csv(_USERNAME_AND_PASSWORD, csv_dict_list)
                    return
                else:
                    error_output("input")
                    continue
 
            

# ========================================================================================================================
#   Quiz Functions
# ========================================================================================================================

# Show all the available quizzes
def show_quizzes(username: str):
    server_process({"type": "quiz_settings"})
    pass

# Display the quiz menu for the user.
# "username" is a string to identify the user
def quiz_menu(username: str):
    while True:
        os.system("cls")
        user_input = input(f"{dynamic_divider()}\n\t\t\tQuiz Menu\n{dynamic_divider()}\nLogged In as: \033[1;37;40m{username}\033[0;37;40m\n\nNumber of Attempts Left: 9999\nTime for the quiz: 9999 mins\nNumber of Question: 9999\n{dynamic_divider()}\n[ 1 ] Start Quiz\n[ X ] Back to Menu\n{dynamic_divider()}\n")
        if user_input.upper() == "X":
            return
        elif user_input == "1":
            # Check if the remaining no of attempt is zero.
            # if remaining_attempt(username) == 0:
            #     error_output("no_attempts")
            #     continue
            start_quiz(username) # Starts the quiz once the user confirms
        else:
            error_output("option")


# Need to add some kind of notification to show what answers the user selected
# Starts the quiz for the signed user.
def start_quiz(username: str):

    # Selects the question randomly from the question pool
    # Each element includes values 
    question = selection_random_question()

    # Selects the first question automatically
    selected_question_index = 0

    # Creates a temporary list to store the user's answer while he is taking the quiz.
    temp_list = []
    for i in question:
        # elements in "i" list
        # index 0: question identification value
        # index 1: question content
        # index 2: question options
        # index 3: question answer
        # index 4: user's answer
        i.append("")
        temp_list.append(i)
        # Needs to add every value of the list into the temp_list
    
    # Starts the timer
    starttime = time.time()

    # Main quiz loop
    while True:
        sample = ""
        
        # Prepares the option for displaying
        for j, option in enumerate(question[selected_question_index][2]):
            sample += f"\n    {chr(97 + j)}) {option}"
        
        # Formats the question to prepare for display.
        selected_question = f"q{selected_question_index + 1}) {question[selected_question_index][1]}: {sample}\n\n"

        os.system("cls")
        user_selection = input(f"{dynamic_divider()}\n\t\t\tQuiz\n{dynamic_divider()}\nTime left: {timer(starttime)[0]} min {timer(starttime)[1]} sec\n{dynamic_divider()}\n{selected_question}Your Answer: {temp_list[selected_question_index][4]}\n{dynamic_divider()}\n[ P ] Previous Question\t\t[ N ] Next Question\n[ S ] Save & Submit\n{dynamic_divider()}\n")
        
        # If time is up, save and submit the users answer
        # OR
        # If user inputs "S", save and submit the answer
        if user_selection.upper() == "S" or (timer(starttime)[0] <= 0 and timer(starttime)[1] <= 0):
            value = save_user_answer(temp_list)
            push_result(username, value)
            show_result(username, value)
            return
        # Goes to the previous question
        elif user_selection.upper() == "P":
            # If at the first question, return an error
            if selected_question_index == 0:
                error_output("previous")
                continue
            else:
                selected_question_index -= 1

        # Goes to the next question
        elif user_selection.upper() == "N":
            # If at the last question, return an error
            if selected_question_index == (len(question) - 1):
                error_output("next")
                continue
            else:
                selected_question_index += 1

        # Checks if the entered input is within range of the available options
        elif check_user_input(user_selection, question[selected_question_index][2]):
            # Stores the user answer into a temporary list whilst taking quiz
            temp_list[selected_question_index][4] = user_selection
        else:
            error_output("option")
            continue

# Checks if the user's selected option in inside the range of options 
# For any question. Due to the flexibility of the number of options the admin can set.
# 
# "given_user_input" is the user input that will be checked to see if the input is within the range of the options
# "question_data" is a list containing the question info, such as content, options and answer
def check_user_input(userInput: str, question_data: list):
    check_list = []
    for i, option in enumerate(question_data):
        check_list.extend(chr(97 + i))
    for check in check_list:
        if check == userInput.lower():
            return True
    return False

# Save the user's selected answers into the quiz_result.csv
# "input_list" is the list that stores the question data and the user's answer.
# 
# elements in "input_list" list
# index 0: question identification value
# index 1: question content
# index 2: question options
# index 3: question answer
# index 4: user's answer
def save_user_answer(input_list: list):
    questions_tested = []
    answered_correct = 0
    answered_wrong = 0
    total_questions = 0
    for question_data in input_list:
        # [ISSUE] Might have to relook the saving of data
        try:
            total_questions += 1
            index = ord(question_data[4]) - 97
        # TypeError occurs when user didn't answer the question
        except TypeError: 
            question_data[4] = "Didn't Answer"
            answered_wrong += 1
        else:
            if question_data[3] == question_data[2][index]:
                answered_correct += 1
            else:
                answered_wrong += 1
        # Gets the index value of the question answer from the options
        # if "randomize_options" is true
        question_answer =  chr(97 + question_data[2].index(question_data[3]))
        questions_tested.append([question_data[0], question_data[1], question_answer, question_data[4]])

    # Sorts the list by order for checking
    questions_tested.sort()

    # Outputs a tuple that can be accessed
    # index 0: question_tested
    # index 1: answered_correct
    # index 2: answered_wrong
    # index 3: total_questions
    return questions_tested, answered_correct, answered_wrong, total_questions

                
# Pushes the answer to the "quiz_result" file.
# 
# username: the username that the user inputted
# input_list[0]: questions_tested list
# input_list[1]: quesiions answered correct
# input_list[2]: questions answered wrong
# input_list[3]: total number of question
def push_result(username: str, input_list: list):
    read_file(_COURSE_INFORMATION, option="question")
    question_pool = list(dictionary.values())
    # Iterates over the entire question_pool to ensure that all question are being tracked
    for i, element in enumerate(question_pool):
        # Checks whether is the current item in the "input_list" list
        if element[0] in input_list[0][i][1]:
            pass
        else:
            # Gets the index value of the question answer from the options
            # This is extra formatting for the missing tested question
            question_answer = chr(97 + question_pool[i][1].index(question_pool[i][-1]))
            # Formats the missing value (aka those not tested) into the list
            formatted_missing_question = [i, question_pool[i][0], question_answer, "Not Tested"]
            input_list[0].insert(i, formatted_missing_question)

    # Reads the file to ensure that all values in the file has been stored.
    read_file(_QUIZ_RESULTS, option="csv")

    # Pushes all the elements into a dictionary for printing
    new_dict = format_into_dict(username, input_list)
    csv_dict_list.append(new_dict)
    write_csv(_QUIZ_RESULTS, csv_dict_list)

# Formats the data into a dictionary for csv printing
def format_into_dict(username: str, input_list: list):
    # input_list[0]: question_list
    # input_list[1]: total_mark
    result = {
        "UserID": username,
        "No. Qn answered correct": input_list[1],
        "No. Qn answered wrong": input_list[2],
        "Total No. of Question": input_list[3],
        "Total Marks": (input_list[3] * 2) - (input_list[2] * 2), # Calculate total marks
        "Date of Attempt": time.ctime()
    }
    for i, element in enumerate(input_list[0]):
        result[f"Question {i + 1}"] = element[1]
        result[f"Answer {i + 1}"] = element[2] 
        result[f"User Answer {i + 1}"] = element[3]
    
    return result

# Returns a string to display the user's result
# 
# elements in "input_list" list
# index 0: question_tested
# index 1: answered_correct
# index 2: answered_wrong
# index 3: total_questions
def show_result(username: str, input_list: list):
    string = ""
    
    # Get the amount of marks awarded for the quiz
    user_marks = input_list[1] * 2

    # Get the total possible marks
    total = input_list[3] * 2
    percentage = user_marks/total * 100

    string += f"{dynamic_divider()}\nUserID: {username}\n"
    string += f"Results: {percentage:.2f}%\n"
    string += f"Time of Submission: {time.ctime()}\n\n"
    if percentage >= 80:
        string += "Well Done!"
    elif percentage > 40:
        string += "Good Work! You could be better."
    else:
        string += "Poor! Try harder next time."
    string += f"\n{dynamic_divider()}\nPress enter to continue"
    input(string)
    return

###   TO BE CHANGED into JSON for CONFIGURATION   ###

# [NOTE] All the function below that are commented are retrieving quiz setting and doing calculations

# Placeholder functions, to be removed later on
def timer():
    pass

def check_number_of_question():
    pass

def check_randomize_option():
    pass

# # Returns the remaining time left in a tuple
# def timer(starting_time: float):
#     endtime = time.time() - starting_time
#     total_allowed_time = float(check_amount_of_time()) * 60
#     time_left_min = int((total_allowed_time - endtime)/60)
#     time_left_sec = int((((total_allowed_time - endtime)/60) - time_left_min) * 60)
#     return time_left_min, time_left_sec

# # Returns the amount of time set within the settings
# def check_amount_of_time():
#     read_file(_QUIZ_SETTING, option="json")
#     value_list = list(dictionary.values())
#     for i in value_list:
#         if i[0] == "1": # ID of "time"
#             return i[2]

# # Number of question to be used in the quiz
# def check_number_of_question():
#     read_file(_QUIZ_SETTING, option="settings")
#     value_list = list(dictionary.values())
#     for i in value_list:
#         if i[0] == "2": # ID of "no_of_question"
#             return i[2]

# # Checks the number of attempts set for the quiz
# def check_number_of_attempts():
#     read_file(_QUIZ_SETTING, option="settings")
#     value_list = list(dictionary.values())
#     for i in value_list:
#         if i[0] == "3": # ID of "no_of_attempt"
#             return int(i[2])

# # Checks if the admin set the answers to appear randomly
# def check_randomize_option():
#     read_file(_QUIZ_SETTING, option="settings")
#     value_list = list(dictionary.values())
#     for i in value_list:
#         if i[0] == "4": # ID of "randomize_answer"
#             if i[2].lower() == "true":
#                 return True
#             return False


###   END OF CONFIGURATION   ###

# Randomly selects question from the question pool
# Returns a nested list
# 
# ask_question_list[0]: index of where the question appears in the dictionary
# ask_question_list[1]: question content
# ask_question_list[2]: options for the question
# ask_question_list[3]: correct answer to the question
def selection_random_question():
    read_file(_COURSE_INFORMATION, option="question")
    question_list = list(dictionary.values())
    ask_question_list = []

    # Creates a list of random non-repeating index numbers for the question selection
    while len(ask_question_list) != int(check_number_of_question()):
        random_number = random.randint(0, len(question_list) - 1)
        if random_number not in ask_question_list: 
            ask_question_list.append(random_number)

    # Replaces the index values with its corresponding question data
    for i, index in enumerate(ask_question_list):
        # Adds the index value of the question
        # This is for later use when writing to csv
        question_list[index].insert(0, index)

        # Checks if randomize option has been enabled
        # If True, shuffle the options in the list
        if check_randomize_option():
            random.shuffle(question_list[index][2])

        # Writes the changes into the "ask_question_list" list
        ask_question_list[i] =  question_list[index]
    return ask_question_list


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
        read_file(_USERNAME_AND_PASSWORD, option="csv")
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
