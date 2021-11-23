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
#
#
# Library/
# package/	
# Module /      os, re, hashlib, csv, time
#
# Known issues:	eg. no validation of input value
#
import os, re, hashlib,  csv, time

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
        input(f"\n\033[1;37;41mAccount Has been locked\033[0;37;40m\n")

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
                    quiz_menu(username_input) # Starting of the quiz
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

def user_password_hashing(userInput: str): 
    output = hashlib.sha256(userInput.encode())
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

def quiz_menu(userInput: str):
    input(dictionary)
    input(f"{DIVIDER}\n\t\tQuiz Menu\n{DIVIDER}\n{userInput}\n{DIVIDER}\n[ 1 ] Start Quiz\n[ X ] Back to Menu\n{DIVIDER}\n")
    quiz_timer()

def start_quiz():
    return

# returns the amount of time set within the settings
def quiz_timer():
    read_file_content(_QUIZ_SETTING_TEXT, "settings")
    value_list = list(dictionary.values())
    for i in value_list:
        if i[0] == "1":
            input(i[2])
            return i[2]

def randomize_answer():
    return

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