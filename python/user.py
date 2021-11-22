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
# Module /      os, re, csv, time
#
# Known issues:	eg. no validation of input value
#
import os 
import re
import time

# ==================================================================
#   Initialize variables
# ==================================================================

dictionary = {}

EMPTY = ""
DIVIDER = f"{EMPTY:=^60}"

MAIN_USER_MENU = ["Log In", "Register User"]
START_MENU = ["Begin Quiz"]
_QUIZ_SETTING_TEXT = "./admin/quiz_settings.txt"
_QUIZ_QUESTION_TEXT = "./admin/question_pool.txt"
LOOP = True

# ==================================================================
#   General Functions
# ==================================================================

# Reads and empties value into "dictionary" variable
# "option" parameter used to define what format it should print in
def read_file_content(file: str, option):
    try:
        # Ensures that the file has been formatted correctly before reading the file.
        remove_linefeed(file)

        with open(file,"r") as f:
            # This method of reading file removes newlines or "\n"
            file_content = f.read().splitlines()

        # Clears to update the dictionary.
        dictionary.clear()

        # Format used for quiz settings dictionary
        if option == "settings":
            for line in file_content:
                stripped_lines = line.strip()

                # Skips line if the line is empty
                if stripped_lines == "":
                    continue

                current_line_list = stripped_lines.split(": ")
                dictionary[current_line_list[0]] = current_line_list[1]
        # Format used for question pool dictionary
        elif option == "question":
            for line in file_content:
                stripped_lines = line.strip()
                if stripped_lines == "":
                    continue
                
                current_line_list = stripped_lines.split("||")

                # Pushes each line into a dictionary
                dictionary[current_line_list[0]] = {
                    "options": current_line_list[1:5],
                    "answer": current_line_list[5]
                }
        
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
        input(f"\n\033[1;37;41mPlease enter a valid input\033[0;37;40m\n")

    elif error_message == "range":
        input("\033[1;37;41mPlease enter a value within the range.\033[0;37;40m")

    elif error_message == "special":
        input(f"\n\033[1;37;41mInput value can't contain special characters!\033[0;37;40m\n")


# ==================================================================
#   Login Functions
# ==================================================================

def login_user():
    input("Login User")



# ==================================================================
#   User Page Function
# ==================================================================

def print_user(inputList: list):
    content = f"{DIVIDER}\n\t\t\t\033[1;37;40m Main \033[0;37;40m\n{DIVIDER}\n"
    for i, element in enumerate(inputList):
        content += f"[ {i+1} ] {element}\n"
    content += f"[ X ] Exit Application\n{DIVIDER}\n"
    return content

def user_logic(userpage_list,content: str):
    while True:
        global LOOP
        LOOP = True
        stored_value = input(content)
        if check_if_digit(stored_value):
            if int(stored_value) in range(1, len(userpage_list) + 1):
                if stored_value == "1":
                    login_user()
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
                    LOOP = False
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
#   Question Function
# ==================================================================

def start_quiz():
    return

def quiz_timer():
    return

# ==================================================================
#   Main Program Loop
# ================================================================== 
while LOOP:
    string = print_user(MAIN_USER_MENU)
    user_logic(MAIN_USER_MENU, string)