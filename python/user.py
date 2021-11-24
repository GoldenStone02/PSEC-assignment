# StudentID:	p2008493
# Name:	        Ng Jun Han
# Class:		DISM/FT/1B/05   
# Assessment:	CA1 
# 
# Script name:	user.py
# 
# Purpose:	Describe purpose of script
#
# Usage syntax:	Run with play button / command line, eg. py read-cmd-line 1 2 3
# 
# Input file:	Specify full path, eg. d:/psec/p01/students.txt
# 
# Output file:	Specify full path, eg. console for d:/psec/p01/students.out
# 
# Python ver:	Python 3
#
# Reference:	This program is adapted from the following:
#                   a) Generating non-repeating random numbers in Python
#                   https://www.tutorialspoint.com/How-to-generate-non-repeating-random-numbers-in-Python
# 
#                   b) 
#                   
# Library/
# package/	
# Module /      os, re, hashlib, csv, time
#
# Known issues:	eg. no validation of input value
#
import os, hashlib, random, csv
import time, datetime

# ==================================================================
#   Initialize variables
# ==================================================================

dictionary = {}

EMPTY = ""
DIVIDER = f"{EMPTY:=^60}"

MAIN_USER_MENU = ["Log In", "Register User"]
START_MENU = ["Begin Quiz"]
_USERNAME_AND_PASSWORD = "./admin/userid_pswd.csv"
_QUIZ_SETTING_TEXT = "./admin/quiz_settings.txt"
_QUIZ_QUESTION_TEXT = "./admin/question_pool.txt"
_QUIZ_RESULTS = "./admin/quiz_result.csv"
MAIN_LOOP = True
SUB_LOOP = True

# ==================================================================
#   General Functions
# ==================================================================

# Reads and empties value into "dictionary" variable
# "option" parameter used to define what format it should print in
def read_file_content(file: str, option):
    try:
        if option == "login":
            with open(file, 'r') as csvfile:
                csvreader = csv.reader(csvfile)
                next(csvreader)
                for i, element in enumerate(csvreader):
                    dictionary[f"user {i + 1}"] = element
                
        else:
            # Ensures that the file has been formatted correctly
            remove_linefeed(file)

            with open(file,"r") as f:
                # This method of reading file removes newlines or "\n"
                file_content = f.read().splitlines()

            # Clears to update the dictionary.
            dictionary.clear()

            # Format used for quiz settings dictionary
            if option == "settings":
                for i, line in enumerate(file_content):
                    stripped_lines = line.strip()

                    # Skips line if the line is empty
                    if stripped_lines == "":
                        continue

                    current_line_list = stripped_lines.split("||")
                    dictionary[f"option {i + 1}"] = [current_line_list[0],current_line_list[1],current_line_list[2]]
            # Format used for question pool dictionary
            elif option == "question":
                for i, line in enumerate(file_content):
                    stripped_lines = line.strip()
                    if stripped_lines == "":
                        continue
                    
                    current_line_list = stripped_lines.split("||")

                    # Pushes each line into a dictionary
                    dictionary[f"question {i+1}"] = [
                        current_line_list[0],                               # Question Content
                        current_line_list[1:len(current_line_list) - 1],    # Question Options
                        current_line_list[len(current_line_list) - 1]       # Question Answer
                    ]
    except FileNotFoundError:
        print("File Doesn't Exist")

# Removes linefeed that is in between lines in the file
def remove_linefeed(file: str):
    temp = []
    with open(file, "r") as f:
        lines = f.readlines()
    
    # Remove linefeed
    # Ensures that if there is a linefeed in between variables
    # It will get removed, preventing any fatal errors in the system
    for line in lines:
        if line == "\n":
            continue
        temp.append(line.strip())
    
    # Rewrites file
    with open(file, "w") as f:
        for line in temp:
            f.write(line + "\n")

# returns the file content using "dictionary"
# "show_number" parameter is used to define the format of returning string.
# "0" prints out file content without numbering
# "1" prints out with sequence numbering
def view_file_content(show_numbers: int, option: str):
    content = ""

    value_list = list(dictionary.values())

    if show_numbers == 1:
        if option == "question":
            for i, item in enumerate(value_list): 
                sample = ""
                for j, option in enumerate(value_list[i][1]):
                    sample += f"\n\t{chr(97 + j)}) {option}"
                content += f"[ {i + 1} ] {value_list[i][0]}: {sample}\n\n"

    elif show_numbers == 0:
        if option == "question":
            for item in value_list:
                sample = ""
                for j, option in enumerate(item[1]):
                    sample += f"\n{chr(97 + j)}) {option}"
                content += f"{item[0]}: {sample}\n\n"
    
    return content

# writes into a csv file with the given inputs.
def write_csv(file: str, usernameInput, passwordInput):
    with open(file, "a", newline="") as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow([usernameInput, user_password_hashing(passwordInput)])

# returns content
def print_file(name: str):
    option_name = ""
    content = f"{DIVIDER}\n\t\t\t\033[1;37;40m {name}\033[0;37;40m\n{DIVIDER}\n"

    if name == "Quiz":
        option_name = "quiz"
        content += f"Question\n{DIVIDER}\n[ P ] Previous Question\t[ N ] Next Question\n[ X ] Back to Menu\n{DIVIDER}\n"
    # content += f"{DIVIDER}\n\t\tSelect one of the options\n{DIVIDER}\n"
    # content += f"[ 1 ] Add New {name}\n[ 2 ] Edit {name}\n[ 3 ] Delete {name}\n[ X ] Back to Main\n{DIVIDER}\n"

    return content

# Checks whether the input is an integer or string
# If the input is a digit, return True
# if the input is a string, return False
def check_if_digit(input):
    if input.strip().isdigit():
        return True
    else:
        return False

# Used for easy maintainence of error outputs
def error_output(error_message: str):
    if error_message == "option":
        input("\033[1;37;41mPlease select a valid option.\033[0;37;40m")

    elif error_message == "input":
        input(f"\n\033[1;37;41mPlease enter a valid input.\033[0;37;40m\n")

    elif error_message == "special":
        input(f"\n\033[1;37;41mInput value can't contain special characters!\033[0;37;40m\n")

    elif error_message == "username":
        input(f"\n\033[1;37;41mUsername could not be found.\033[0;37;40m\n")

    elif error_message == "password":
        input(f"\n\033[1;37;41mPassword is incorrect.\033[0;37;40m\n")

    elif error_message == "admin":
        input(f"\n\033[1;37;41mAccount has been locked\033[0;37;40m\n")

    elif error_message == "previous":
        input(f"\n\033[1;37;41mYou are at the first question!!\033[0;37;40m\n")
    
    elif error_message == "next":
        input(f"\n\033[1;37;41mYou are at the last question!!\033[0;37;40m\n")
    
# ==================================================================
#   User Page Function
# ==================================================================

# User navigation menu
def user_menu(inputList: list):
    content = f"{DIVIDER}\n\t\t\t\033[1;37;40m Main \033[0;37;40m\n{DIVIDER}\n"
    for i, element in enumerate(inputList):
        content += f"[ {i+1} ] {element}\n"
    content += f"[ X ] Exit Application\n{DIVIDER}\n"
    return content

# Logicial Flow for user menu
def user_logic(userpage_list,content: str):
    while True:
        global MAIN_LOOP, SUB_LOOP
        # Turns 
        SUB_LOOP = True
        stored_value = input(content)
        if check_if_digit(stored_value):
            if int(stored_value) in range(1, len(userpage_list) + 1):
                if stored_value == "1":
                    login_subloop()
                elif stored_value == "2":
                    input("Register User")
            else:
                error_output("option")
        elif stored_value.upper() == "X":
            os.system("cls")
            while True:
                userConfirm = input(f"{DIVIDER}\n\033[1;37;40m\t\tAre you sure want to quit?\033[0;37;40m\n{DIVIDER}\n[ Y ] Yes\t\t[ N ] No\n{DIVIDER}\n")
                if userConfirm.upper() == "Y":
                    print("\033[0;32;40mGoodbye\033[0;37;40m")
                    MAIN_LOOP = False
                    break
                elif userConfirm.upper() == "N":
                    break
                else:
                    error_output("option")
                os.system("cls")
            return
        else:
            error_output("option")


# ==================================================================
#   Login Functions
# ==================================================================

# Log In Logicial Flow
def login_menu():
    while True:
        os.system("cls")
        username_input = input(f"{DIVIDER}\n\t\t\tLog In\n{DIVIDER}\nUsername: \nPassword: \n{DIVIDER}\n[ X ] Back to Menu\n{DIVIDER}\nEnter your username: ")
        if username_input.upper() == "X":
            global SUB_LOOP
            SUB_LOOP = False
            return
        elif check_username(username_input):
            count = 3
            while count != 0:
                os.system("cls")
                password_input = input(f"{DIVIDER}\n\t\t\tLog In\n{DIVIDER}\nUsername: {username_input} \nPassword: \n{DIVIDER}\n[ X ] Back to Menu\n{DIVIDER}\nEnter your password: ")
                if password_input.upper() == "X":
                    SUB_LOOP = False
                    return
                elif check_password(username_input, password_input):
                    quiz_menu(username_input) # starting of the quiz
                    return
                else:
                    count -= 1
                    error_output("password")
                    continue
            if count == 0:
                error_output("admin")
                break
        else:
            error_output("username")
            continue

# check if username exist in the file
def check_username(username: str):
    value_list = list(dictionary.values())
    for i in value_list:
        if username == i[0]:
            return True
    return False

# hashes the password for safe keeping in the .csv file
def user_password_hashing(given_input: str): 
    output = hashlib.sha256(given_input.encode())
    return output.hexdigest()

# checks if the hashed matches the password
def check_password(username: str, password: str):
    value_list = list(dictionary.values())
    for i in value_list:
        if username == i[0]:
            if user_password_hashing(password) == i[1]:
                return True
            else:
                return False


# ==================================================================
#   Question Function
# ==================================================================

# display the quiz menu for the user.
# "username" is a string to identify the user
def quiz_menu(username: str):
    while True:
        os.system("cls")
        user_input = input(f"{DIVIDER}\n\t\t\tQuiz Menu\n{DIVIDER}\nUser Logged In as: \033[1;37;40m{username}\033[0;37;40m\n\nTime for the quiz: {amount_of_time()} mins\nNumber of Question: {number_of_question()}\n{DIVIDER}\n[ 1 ] Start Quiz\n[ X ] Back to Menu\n{DIVIDER}\n")
        if user_input.upper() == "X":
            return
        elif user_input == "1":
            start_quiz() # starts the quiz once the user confirms
        else:
            error_output("option")

# need to add some kind of notification to show what answers the user selected
# starts the quiz for the signed user.
def start_quiz():
    # selects the question randomly from the question pool
    question = selection_random_question()

    # selects the first question automatically
    selected_question_index = 0

    # creates a temporary list to store the user's answer while he is taking the quiz.
    temp_list = []
    for i in question:
        temp_list.append([i[0], i[2], ""])
    
    # starts the timer
    starttime = time.time()

    # main quiz loop
    while True:
        # formats the question to prepare for display.
        sample = ""
        for j, option in enumerate(question[selected_question_index][1]):
            sample += f"\n    {chr(97 + j)}) {option}"
        selected_question = f"q{selected_question_index + 1}) {question[selected_question_index][0]}: {sample}\n\n"

        os.system("cls")
        user_selection = input(f"{DIVIDER}\n\t\t\tQuiz\n{DIVIDER}\nTime left: {timer(starttime)[0]} min {timer(starttime)[1]} sec\n{DIVIDER}\n{selected_question}Your Answer: {temp_list[selected_question_index][2]}\n{DIVIDER}\n[ P ] Previous Question\t\t[ N ] Next Question\n[ S ] Save & Submit\n{DIVIDER}\n")
        
        # if time is up, save and submit the users answer
        # OR
        # if user inputs "S", save and submit the answer
        if user_selection.upper() == "S" or (timer(starttime)[0] <= 0 and timer(starttime)[1] <= 0):
            input("Save & Submit")
        elif user_selection.upper() == "P":
            if selected_question_index == 0:
                error_output("previous")
                continue
            else:
                selected_question_index -= 1
        elif user_selection.upper() == "N":
            if selected_question_index == (len(question) - 1):
                error_output("next")
                continue
            else:
                selected_question_index += 1
        elif check_user_input(user_selection, question[selected_question_index][1]):
            store_user_answer(user_selection, temp_list, selected_question_index)
        else:
            error_output("option")
            continue

# checks if the user's selected option in inside the range of options 
# for any question. Due to the flexibility of the number of options the admin can set.
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

# stores the user answer into a temporary list
def store_user_answer(userInput: str, question_pool: list, selected_question: int):
    question_pool[selected_question][2] = userInput


# check if the user's answer is correct or incorrect
def check_user_answer():
    return

# returns the remaining time left
def timer(starting_time: float):
    endtime = time.time() - starting_time
    total_allowed_time = float(amount_of_time()) * 60
    time_left_min = int((total_allowed_time - endtime)/60)
    time_left_sec = int((((total_allowed_time - endtime)/60) - time_left_min) * 60)
    # string = f"{time_left_min} min {time_left_sec} sec"
    return time_left_min, time_left_sec


# returns the amount of time set within the settings
def amount_of_time():
    read_file_content(_QUIZ_SETTING_TEXT, "settings")
    value_list = list(dictionary.values())
    for i in value_list:
        if i[0] == "1": # ID of "time"
            return i[2]

# number of question to be used in the quiz
def number_of_question():
    read_file_content(_QUIZ_SETTING_TEXT, "settings")
    value_list = list(dictionary.values())
    for i in value_list:
        if i[0] == "2": # ID of "no_of_question"
            return i[2]

# checks if the admin set the answers to appear randomly
def randomize_answer():
    read_file_content(_QUIZ_SETTING_TEXT, "settings")
    value_list = list(dictionary.values())
    for i in value_list:
        if i[0] == "4": # ID of "randomize_answer"
            if i[2].lower() == "true":
                return True
            return False

# randomly selects question from the question pool
def selection_random_question():
    read_file_content(_QUIZ_QUESTION_TEXT, "question")
    question_list = list(dictionary.values())
    ask_question_list = []

    # creates a list of random non-repeating index numbers for the question selection
    while len(ask_question_list) != int(number_of_question()):
        random_number = random.randint(0, len(question_list) - 1)
        if random_number not in ask_question_list: 
            ask_question_list.append(random_number)

    # replaces the index values with its corresponding question data
    for i, index in enumerate(ask_question_list):
        ask_question_list[i] = question_list[index]
    return ask_question_list

# pushes the answer to the "quiz_result" file.
def push_result():
    return

# ==================================================================
#   Sub Program Loop
# ==================================================================
def login_subloop():
    while SUB_LOOP:
        read_file_content(_USERNAME_AND_PASSWORD, "login")
        login_menu()
    
# ==================================================================
#   Main Program Loop
# ================================================================== 
while MAIN_LOOP:
    string = user_menu(MAIN_USER_MENU)
    user_logic(MAIN_USER_MENU, string)