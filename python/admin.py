# StudentID:	p2008493
# Name:	        Ng Jun Han
# Class:		DISM/FT/1B/05   
# Assessment:	CA1 
# 
# Script name:	admin.py
# 
# Purpose:	The purpose of the script is to allow an administer to edit and change the settings within 
#           the files without having to manual search through every file to find the correct setting
#           or text to change.
#
# Usage syntax:	Run with play button / command line, eg. py read-cmd-line 1 2 3
# 
# Input file:   C:\PSEC_project\question_pool.txt
#               C:\PSEC_project\quiz_settings.txt
#               C:\PSEC_project\userid_pswd.csv
#               C:\PSEC_project\quiz_results.csv
# 
# Output file:  C:\PSEC_project\question_pool.txt
#               C:\PSEC_project\quiz_settings.txt
#               C:\PSEC_project\userid_pswd.csv
#               C:\PSEC_project\quiz_results.csv
# 
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
# Module /      os, re, csv, hashlib, random
#
# Known issues:	eg. no validation of input value
#

import os, re, csv
import hashlib, random

# ==================================================================
#   Initialize Variables
# ==================================================================
dictionary = {}
csv_dict_list = []

EMPTY = ""
DIVIDER = f"{EMPTY:=^60}"

PATTERN = r"^[\w.]+$"
EMAIL_PATTERN = r"([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)"
PASSWORD_PATTERN = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%]).+$'

MAIN_MENU = ["Register User", "Question Pool", "Quiz Settings", "Generate Report"]

_USERNAME_AND_PASSWORD = "./admin/userid_pswd.csv"
_QUIZ_SETTING_TEXT = "./admin/quiz_settings.txt"
_QUIZ_QUESTION_TEXT = "./admin/question_pool.txt"
_QUIZ_RESULTS = "./admin/quiz_results.csv"

MAIN_LOOP = True
SUB_LOOP = True

# ==================================================================
#   General Functions
# ==================================================================

# Reads and empties value into "dictionary" variable
# "option" parameter used to define what format it should print in
def read_file_content(file: str, option):
    try:
        if option == "csv":
            csv_dict_list.clear()
            with open(file, 'r') as csvfile:
                # Uses DictReader for easy storing of the value
                for line in csv.DictReader(csvfile):
                    csv_dict_list.append(dict(line))
                
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

# Writes changes to the selected file
def writes_to_file(file: str, option: str, index=None):
    value_list = list(dictionary.values())

    # Deletes items from text file
    if option == "delete":
        with open(file, "r") as f:
            lines = f.read().splitlines()
        
        with open(file, "w") as f:
            for number, line in enumerate(lines):
                if number != index:
                    f.write(line + '\n')  

    # Writes items into csv file 
    elif option == "csv":
        # Fieldnames are the key values of the first item in the dictionary.
        fields = csv_dict_list[0].keys()

        # Writes to the csv file with the correct headings and value
        with open(file, "w", newline="") as csvfile:
            csvwriter = csv.DictWriter(csvfile, fieldnames=fields)
            csvwriter.writeheader()
            csvwriter.writerows(csv_dict_list)
    
    # Deletes items from csv files
    elif option == "delete_csv":
        # Removes the user from the csv file
        csv_dict_list.pop(index) 

        # Fieldnames are the key values of the first item in the dictionary.
        fields = csv_dict_list[0].keys()

        # Writes to the csv file with the correct headings and value
        with open(file, "w", newline="") as csvfile:
            csvwriter = csv.DictWriter(csvfile, fieldnames=fields)
            csvwriter.writeheader()
            csvwriter.writerows(csv_dict_list)
    
    # Edit setting variables from the settings text file
    elif option == "edit_setting":
        with open(file, "w") as f:
            for line in value_list:
                f.write(f"{line[0]}||{line[1]}||{line[2]}\n")

# Writes into a csv file with the given inputs.
def writes_to_csv(file: str, dict_input: dict):

    # Fieldnames are the key values of the first item in the dictionary.
    fields = dict_input[0].keys()

    # Writes to the csv file with the correct headings and value
    with open(file, "w", newline="") as csvfile:
        csvwriter = csv.DictWriter(csvfile, fieldnames=fields)
        csvwriter.writeheader()
        csvwriter.writerows(dict_input)

# Removes linefeed that is in between lines in the file
def remove_linefeed(file: str):
    temp = []
    with open(file, "r") as f:
        file_lines = f.readlines()
    
    # Remove linefeed
    # Ensures that if there is a linefeed in between variables
    for line in file_lines:
        if line == "\n":
            continue
        temp.append(line.strip())
    
    # Rewrites file
    with open(file, "w") as f:
        for line in temp:
            f.write(line + "\n")

# Returns the file content using "dictionary"
# "show_number" parameter is used to define the format of returning string.
# "0" prints out file content without numbering
# "1" prints out with sequence numbering
def view_file_content(show_numbers: int, option: str):
    content = ""

    value_list = list(dictionary.values())

    if show_numbers == 1:
        # Formats dictionary for settings with numbering
        if option == "settings":
            for i, item in enumerate(value_list): 
                content += f"[ {i + 1} ] {value_list[i][1]}: {value_list[i][2]}\n"

        # Formats dictionary for csv with numbering
        elif option == "csv":
            # Gets the header keys
            headers = list(csv_dict_list[0].keys())
            header_text = "\t"

            # Formats for printing
            for head in headers:
                header_text += head + "\t|\t"
            content += f"{header_text}\n"

            for i, sub_dict in enumerate(csv_dict_list):
                # Reads from csv formatter
                csv_list = list(sub_dict.values())
                content += f"[ {i + 1} ] {csv_list[0]}\t|{csv_list[1][:10]}\t|\t{csv_list[2][:10]}...\t|\n" 

        # Formats dictionary for question with numbering
        elif option == "question":
            for i, item in enumerate(value_list): 
                sample = ""
                for j, option in enumerate(value_list[i][1]):
                    sample += f"\n\t{chr(97 + j)}) {option}"
                content += f"[ {i + 1} ] {value_list[i][0]}: {sample}\n\n"

    elif show_numbers == 0:
        # Formats dictionary for settings w/o numbering
        if option == "settings":
            for item in value_list:
                content += f"[ - ] {item[1]}: {item[2]}\n"

        # Formats dictionary for csv w/o numbering
        elif option == "csv":
            # Gets the header keys
            headers = list(csv_dict_list[0].keys())
            header_text = "\t"

            # Formats for printing
            for head in headers:
                header_text += head + "\t|\t"
            content += f"{header_text}\n"

            # Gets the values of each user stored in the system
            for sub_dict in csv_dict_list:
                # Reads from csv formatter
                csv_list = list(sub_dict.values())
                
                # Formats the input for display
                content += f"[ - ] {csv_list[0]}\t|{csv_list[1][:10]}\t|\t{csv_list[2][:10]}...\t|\n" 
   
        # Formats dictionary for question w/o numbering
        elif option == "question":
            for item in value_list:
                sample = ""
                for j, option in enumerate(item[1]):
                    sample += f"\n{chr(97 + j)}) {option}"
                content += f"{item[0]}: {sample}\n\n"
    
    return content

# Prints the text file with some UI.
# Needs to happen after "ReadFileContent()" has been executed
def print_menu(name: str): 
    option_name = ""

    # Allows for dynamic change of the program using only one UI
    if name == "Question":
        option_name = "question"
    elif name == "Quiz Settings":
        option_name = "settings"
    elif name == "User":
        option_name = "csv"
    

    content = f"{DIVIDER}\n\t\t\t\033[1;37;40m {name}\033[0;37;40m\n{DIVIDER}\n"

    content += view_file_content(0, option_name)

    content += f"{DIVIDER}\n\t\tSelect one of the options\n{DIVIDER}\n"
    content += f"[ 1 ] Add New {name}\n[ 2 ] Edit {name}\n[ 3 ] Delete {name}\n[ X ] Back to Main\n{DIVIDER}\n"

    user_input = input(content)
    return user_input

# Checks whether the input is an integer or string
# If the input is a digit, return True
# if the input is a string, return False
def check_if_digit(userInput):
    if str(userInput).isdigit():
       return True
    return False 


# Used for easy maintainence of error outputs
def error_output(error_message: str):
    string = ""
    if error_message == "option":
        string += "\033[1;37;41mPlease select a valid option.\033[0;37;40m"

    elif error_message == "input":
        string += "\n\033[1;37;41mPlease enter a valid input\033[0;37;40m\n"

    elif error_message == "range":
        string += "\033[1;37;41mPlease enter a value within the range.\033[0;37;40m"

    elif error_message == "special":
        string += "\n\033[1;37;41mInput value can't contain special characters!\033[0;37;40m\n"

    elif error_message == "short":
        string += "\n\033[1;37;41mLength of input was too short\033[0;37;40m\n"

    elif error_message == "long":
        string += "\n\033[1;37;41mLength of input was too long\033[0;37;40m\n"
    
    elif error_message == "letter":
        string += "\n\033[1;37;41mMust have at least one uppercase and lowercase character\033[0;37;40m\n"

    elif error_message == "password":
        string += "\n\033[1;37;41mMissing one of the criteria, please try again\033[0;37;40m\n"
    
    elif error_message == "email":
        string += "\n\033[1;37;41mFormat of email was incorrect, please try again\033[0;37;40m\n"

    elif error_message == "bad_input":
        string += "\n\033[1;37;41mBad Input, program restarted\033[0;37;40m\n"
    
    input(string)


# ============================================================================================
#   Main Page Functions
# ============================================================================================

# Prints page with a list, checks whether is input is in range of list
# "input_list" parameter is for dynamic changing of the menu
def print_main(input_list: list):
    content = f"{DIVIDER}\n\t\t\t\033[1;37;40m Main \033[0;37;40m\n{DIVIDER}\n"
    for i, element in enumerate(input_list):
        content += f"[ {i+1} ] {element}\n"
    content += f"[ X ] Exit Application\n{DIVIDER}\n"
    return content

# Main logical system for selection page
# "menu_list" is meant for easily change within the UI.
def main_logic(menu_list: list, content: str):
    global MAIN_LOOP, SUB_LOOP
    SUB_LOOP = True
    stored_value = input(content)
    if check_if_digit(stored_value):
        if int(stored_value) in range(1, len(menu_list) + 1):
            if stored_value == "1":
                register_user_subloop()
            elif stored_value == "2":
                question_pool_subloop()
            elif stored_value == "3":
                quiz_setting_subloop()
            elif stored_value == "4":
                generate_report_subloop()
        else:
            error_output("option")
    elif stored_value.upper() == "X":
        os.system("cls")
        while True:
            userConfirm = input(f"{DIVIDER}\n\033[1;37;40m\t\tAre you sure want to quit?\033[0;37;40m\n{DIVIDER}\n[ Y ] Yes\t\t[ N ] No\n{DIVIDER}\n")
            if userConfirm.upper() == "Y":
                print("\033[0;32;40mGoodbye\033[0;37;40m")
                MAIN_LOOP = False
                return
            elif userConfirm.upper() == "N":
                return
            else:
                error_output("option")
            os.system("cls")
    else:
        error_output("option")

# ===================================================================================================
#   Register User Functions
# ===================================================================================================

def register_logic(userInput: str):
    valueCap = str(userInput).upper()
    if valueCap == "X":
        global SUB_LOOP
        SUB_LOOP = False
        return
    elif valueCap == "1":
        add_user()
    elif valueCap == "2":
        edit_user()
    elif valueCap == "3":
        delete_user()
    else:
        error_output("input")
        return

# Add users to "userid_passwd.csv"
def add_user():
    while True:
        # Username check
        while True:
            os.system("cls")
            username = input(f"{DIVIDER}\n\t\t\tRegistering User\n{DIVIDER}\nUsername: \nEmail: \nPassword: \n{DIVIDER}\n[ X ] Back to Menu\n{DIVIDER}\nUsername: ")

            if username.upper() == "X":
                return
            elif not re.search(PATTERN, username):
                error_output("special")
                continue
            break

        # Email check
        while True:
            os.system("cls")
            email = input(f"{DIVIDER}\n\t\t\tRegistering User\n{DIVIDER}\nUsername: {username}\nEmail: \nPassword: \n{DIVIDER}\n[ X ] Back to Menu\n{DIVIDER}\nEnter email: ")
            if email.upper() == "X":
                return
            elif not re.search(EMAIL_PATTERN, email):
                error_output("email")
                continue
            break

        while True:
            # Password check
            while True:
                os.system("cls")
                password = input(f"{DIVIDER}\n\t\t\tRegistering User\n{DIVIDER}\nUsername: {username}\nEmail: {email}\nPassword: \n{DIVIDER}\n[ X ] Back to Menu\n{DIVIDER}\nAt least one number\nAt least one uppercase and one lowercase character\nAt least one special symbol !@#$%\nShould be 4 - 20 characters long\nPassword: ")

                if password.upper() == "X":
                    return
                elif password == "":
                    error_output("option")
                    continue            
                elif len(password) < 4:
                    error_output("short")
                    continue
                elif len(password) > 20:
                    error_output("long")
                    continue
                elif not re.search(PASSWORD_PATTERN, password):
                    error_output("password")
                    continue
                break

            # Password double check
            while True:
                os.system("cls")
                password2 = input(f"{DIVIDER}\n\t\t\tRegistering User\n{DIVIDER}\nUsername: {username}\nEmail: {email}\nPassword: \n{DIVIDER}\n[ X ] Back to Menu\n{DIVIDER}\nPlease reenter your password: ")

                if password2.upper() == "X":
                    return
                elif password2 == "":
                    error_output("option")
                    continue
                elif password == password2:
                    # Check if the user wants to confirm the setting
                    while True:
                        os.system("cls")
                        finalCheck = input(f"{DIVIDER}\n\t\t\tRegistering User\n{DIVIDER}\nUsername: {username}\nEmail: {email}\nPassword: {password}\n{DIVIDER}\n[ C ] Confirm\t\t[ X ] Exit\n{DIVIDER}\n")
                        
                        if finalCheck.upper() == "X":
                            return
                        elif finalCheck.upper() == "C":
                            input("\033[0;32;40mYour changes have been saved!\033[0;37;40m\nPress Enter to Continue\n")
                            break
                        else:
                            error_output("option")
                            continue
                    user_dict = {
                        "user": username,
                        "email": email,
                        "password": user_password_hashing(password)
                    }

                    # Adds the new value into the list 
                    csv_dict_list.append(user_dict)
                    writes_to_csv(_USERNAME_AND_PASSWORD, csv_dict_list)
                    return
                else: 
                    error_output("input")
                    continue

# Edits either the email or password from "userid_passwd.csv":
# Don't change the username as it might effect "quiz_result" [ISSUE]
def edit_user():
    input("Change User")
    return

# Deletes user from "userid_passwd.csv"
def delete_user():
    if len(csv_dict_list) == 0:
        input("User List is empty, please register some users.")
        return
    while True:
        os.system("cls")
        deleting_index = input(f"{DIVIDER}\nDeleting User\n{DIVIDER}\n{view_file_content(1, 'csv')}\n{DIVIDER}\nWhich user do you wish to delete?\n{DIVIDER}\n[ X ] Back to Menu\n{DIVIDER}\n")
        if deleting_index.upper() == "X":
            return
        elif not check_if_digit(deleting_index):
            error_output("input")
            continue
        else:
            # Formatting for display during "delete_check"
            # Reads from csv formatter
            csv_list = list(csv_dict_list[int(deleting_index) - 1].values())
            
            # Gets the header keys
            headers = list(csv_dict_list[int(deleting_index) - 1].keys())
            header_text = "\t"

            # Formats for printing
            for head in headers:
                header_text += head + "\t|\t"
            
            # Formats the input for display
            content = f"{header_text}\n"
            content += f"[ {deleting_index} ] {csv_list[0]}\t|{csv_list[1][:10]}\t|\t{csv_list[2][:10]}...\t|\n" 
        
        while True:
            os.system("cls")
            delete_check = input(f"{DIVIDER}\nDeleting User\n{DIVIDER}\n{content}\n{DIVIDER}\nPlease confirm your selection\n{DIVIDER}\n[ C ] Confirm\t[ X ] Back to Menu\n{DIVIDER}\n")
            if delete_check.upper() == "X":
                break
            elif delete_check.upper() == "C":
                writes_to_file(_USERNAME_AND_PASSWORD, "delete_user", int(deleting_index)) 
                input("\033[0;31;40mUser has been deleted!\033[0;37;40m\nPress Enter to Continue\n") 
                break 
            else:
                error_output("option")
                continue

# Hashes the user's password
def user_password_hashing(userInput: str): 
    output = hashlib.sha256(userInput.encode())
    return output.hexdigest()

# ===================================================================================================
#   Question Pool Functions
# ===================================================================================================

# Logicial system for question pool
def question_logic(userInput: str):
    valueCap = str(userInput).upper()
    if valueCap == "X":
        global SUB_LOOP
        SUB_LOOP = False
        return
    elif valueCap == "1":
        add_question()
    elif valueCap == "2":
        edit_question()
    elif valueCap == "3":
        delete_question()
    else:
        error_output("option")

# Add question into the "question_pool.txt"
def add_question():
    while True:
        while True:
            os.system("cls")
            print_option = ""
            no_of_options = input(f"{DIVIDER}\nHow many options do you want? [ 3 - 5 options ]\n{DIVIDER}\n[ X ] Back to Menu\n{DIVIDER}\n")
            if no_of_options.upper() == "X":
                return
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
            os.system("cls")
            question = input(f"{DIVIDER}\n\t\t\tAdding Question\n{DIVIDER}\nQuestion: \n\nOptions: \n{print_option}\n\nAnswer: \n\n{DIVIDER}\n[ X ] Back to Menu\n{DIVIDER}\nInput Question: ")
            if question.upper() == "X":
                return
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
                os.system("cls")
                options = input(f"{DIVIDER}\n\t\t\tAdding Options\n{DIVIDER}\nQuestion: {question}\n\nOptions: \n{string}\n\n Answer: \n\n{DIVIDER}\n[ X ] Back to Menu\n{DIVIDER}\nInput Options: ")
                if options.upper() == "X":
                    return
                elif len(options) > 70:
                    error_output("long")
                else:
                    string = ""
                    options_listing[i] = options
                    for j, element in enumerate(options_listing):
                        string += f"{chr(97 + j)}) {element}\n"
        # Answer input check
        while True:
            os.system("cls")
            answer = input(f"{DIVIDER}\n\t\t\tAdding Answers\n{DIVIDER}\nQuestion: {question}\n\nOptions: \n{string}\n\nAnswer: \n\n{DIVIDER}\n[ X ] Back to Menu\n{DIVIDER}\nCorrect Answer: ")
            if answer.upper() == "X":
                return
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
            confirm_change = input(f"{DIVIDER}\n\t\t\tConfirming Question\n{DIVIDER}\nQuestion: {question}\n\nOptions: \n{string}\n\nAnswer: {answer}\n\n{DIVIDER}\n[ C ] Confirm\t\t[ X ] Back to Menu\n{DIVIDER}\n")
            if confirm_change.upper() == "X":
                return
            elif confirm_change.upper() == "C":
                input("\033[0;32;40mYour changes have been saved!\033[0;37;40m\nPress Enter to Continue\n")
            else:
                error_output("option")
                continue
            break
        
        # Formatting of questions into question pool
        string = f"{question}||"
        for element in options_listing:
            string += f"{element}||"
        string += f"{answer}"

        with open(_QUIZ_QUESTION_TEXT, "a") as f:
            f.write(string)
        return
    
# Edits question from "question_pool"
# [ISSUE]
def edit_question(): 
    return

# Deletes question from "question_pool"
def delete_question():
    value_list = list(dictionary.values())
    if len(value_list) == 0:
        input("Question Pool is empty, please add some questions")
        return
    while True:
        os.system("cls")
        deleting_index = input(f"{DIVIDER}\nWhich question do you want to delete?\n{DIVIDER}\n{view_file_content(1, 'question')}{DIVIDER}\n[ X ] Back to Menu\n{DIVIDER}\n")
        if deleting_index.upper() == "X":
            return
        elif not deleting_index.isdigit():
            error_output("input")
        else:
            deleting_index = int(deleting_index) - 1
            string = ""
            for j, element in enumerate(value_list[deleting_index][1]):
                string += f"{chr(97 + j)}) {element}\n"    

        while True:
            os.system("cls")
            delete_check = input(f"{DIVIDER}\n\t\tPlease confirm your selection\n{DIVIDER}\n{value_list[deleting_index][0]}\n{string}\n{DIVIDER}\n[ C ] Confirm\t\t[ X ] Back to Menu\n{DIVIDER}\n")
            if delete_check.upper() == "X":
                break
            elif delete_check.upper() == "C":
                writes_to_file(_QUIZ_QUESTION_TEXT, "delete", deleting_index) 
                input("\033[0;31;40mOption has been deleted!\033[0;37;40m\nPress Enter to Continue\n") 
                break 
            else:
                error_output("option")
                continue
        return

# ===================================================================================================
#   Quiz Settings Functions
# ===================================================================================================

# Logicial system for quiz setting
def setting_logic(userInput: str):
    valueCap = str(userInput).upper()
    # Logical Circuit
    if valueCap == "X": # Close App
        global SUB_LOOP
        SUB_LOOP = False
        os.system("cls")
        return
    elif valueCap == "1": # Add Setting
        add_setting()
    elif valueCap == "2": # Edit Setting
        edit_setting()
    elif valueCap == "3": # Delete Setting
        delete_setting()
    else:
        error_output("option")

# Add settings into "quiz_settings.txt"
def add_setting(): 
    while True:
        # Name check
        while True:
            os.system("cls")
            new_setting_name = input(f"{DIVIDER}\n\t\t\tAdding Setting\n{DIVIDER}\nSetting Name: \nSetting Value: \n{DIVIDER}\n[ X ] Back to Menu\n{DIVIDER}\nSetting Name: ")

            if new_setting_name.upper() == "X":
                return
            elif not re.search(PATTERN, new_setting_name):
                error_output("special")
                continue
            break

        # Value check
        while True:
            os.system("cls")
            new_setting_value = input(f"{DIVIDER}\n\t\t\tAdding Setting\n{DIVIDER}\nSetting Name: {new_setting_name}\nSetting Value: \n{DIVIDER}\n[ X ] Back to Menu\n{DIVIDER}\nSetting Value: ")

            if new_setting_value.upper() == "X":
                return
            elif new_setting_value == "":
                error_output("option")
                continue            
            elif not re.search(PATTERN, new_setting_value):
                error_output("special")
                continue
            break

        # Check if the user wants to confirm the setting
        while True:
            os.system("cls")
            finalCheck = input(f"{DIVIDER}\n\t\t\tAdding Setting\n{DIVIDER}\nSetting Name: {new_setting_name}\nSetting Value: {new_setting_value}\n{DIVIDER}\n[ C ] Confirm\t\t[ X ] Exit\n{DIVIDER}\n")
            
            if finalCheck.upper() == "X":
                return
            elif finalCheck.upper() == "C":
                input("\033[0;32;40mYour changes have been saved!\033[0;37;40m\nPress Enter to Continue\n")
            else:
                error_output("option")
            break

        # Checks if the program aborted at any point 
        with open(_QUIZ_SETTING_TEXT, "a") as f:
            r = random.randint(1,1000000)
            f.write(f"{r}||{new_setting_name}||{new_setting_value}")
        return

# Edits settings from "quiz_settings.txt"
def edit_setting():
    value_list = list(dictionary.values())

    while True:
        os.system("cls")
        edit_index = select_setting("Settings")

        if not check_if_digit(edit_index): # execute if its not an integer
            if edit_index.upper() == "X":
                return  
        elif check_if_digit(edit_index): # execute if its an integer
            while True:
                os.system("cls")
                selector = input(f"{DIVIDER}\nWhat do you want to change?\n{DIVIDER}\nName: {value_list[edit_index][1]}\nValue: {value_list[edit_index][2]}\n{DIVIDER}\n[ 1 ] Setting Name\n[ 2 ] Setting Value\n{DIVIDER}\n[ X ] Back to Menu\n{DIVIDER}\n")
                if check_if_digit(selector):
                    local_loop = True
                    # Used to change setting name
                    if selector == "1":
                        while local_loop:
                            os.system("cls")
                            new_name = input(f"{DIVIDER}\nName: \033[1;37;40m>>> {value_list[edit_index][1]} <<<\033[0;37;40m\nValue: {value_list[edit_index][2]}\n{DIVIDER}\n[ X ] Back to Menu\n{DIVIDER}\nPlease input a new name: ")
                            
                            if new_name.upper() == "X":
                                local_loop = False
                                break
                            if new_name == "":
                                error_output("input")
                                continue 
                            elif not re.search(PATTERN, new_name):
                                error_output("special")
                                continue 
                            break

                        while local_loop:
                            os.system("cls")
                            confirm_change = input(f"{DIVIDER}\n\t\tConfirm Changes?\n{DIVIDER}\nName: \033[1;37;40m>>> {new_name} <<<\033[0;37;40m\nValue: {value_list[edit_index][2]}\n{DIVIDER}\n[ C ] Confirm \n[ X ] Cancel Changes\n{DIVIDER}\n")
                            
                            if confirm_change.upper() == "X":
                                local_loop = False
                                break
                            if confirm_change == "":
                                error_output("input")
                                continue            
                            elif not re.search(PATTERN, confirm_change):
                                error_output("special")
                                continue 
                            elif confirm_change.upper() == "C":
                                input("\033[0;32;40mYour changes have been saved!\033[0;37;40m\nPress Enter to Continue\n")                              
                            break

                        if local_loop:
                            # Change the name of item
                            value_list[edit_index][1] = new_name
                            writes_to_file(_QUIZ_SETTING_TEXT, "edit_setting")   

                    # Used to change the setting value             
                    elif selector == "2":
                        while local_loop:
                            os.system("cls")
                            new_value = input(f"{DIVIDER}\nName: {value_list[edit_index][1]}\nValue: \033[1;37;40m>>> {value_list[edit_index][2]} <<<\033[0;37;40m\n{DIVIDER}\n[ X ] Back to Menu\n{DIVIDER}\nPlease input new value: ")
                            if new_value.upper() == "X":
                                local_loop = False
                                break
                            if not re.search(PATTERN, new_value):
                                error_output("special")
                                continue
                            break

                        while local_loop:
                            os.system("cls")
                            confirm_change = input(f"{DIVIDER}\n\t\tConfirm Changes?\n{DIVIDER}\nSetting Name: {value_list[edit_index][1]}\nSetting Value: \033[1;37;40m>>> {new_value} <<<\033[0;37;40m\n{DIVIDER}\n[ C ] Confirm \n[ X ] Cancel Changes\n{DIVIDER}\n")
                            if confirm_change.upper() == "X":
                                break
                            if confirm_change == "":
                                error_output("input")
                                continue            
                            elif not re.search(PATTERN, confirm_change):
                                error_output("special")
                                continue     
                            elif confirm_change.upper() == "C":
                                input("\033[0;32;40mYour changes have been saved!\033[0;37;40m\nPress Enter to Continue\n")                       
                            break  

                        if local_loop:
                            # Changes the value of the item
                            value_list[edit_index][2] = new_value
                            writes_to_file(_QUIZ_SETTING_TEXT, "edit_setting")                       
                    else:
                        error_output("option")
                elif selector.upper() == "X":
                    return    
                else:
                    error_output("input")
                    continue
        else:
            error_output("option")

# Deletes settings from "quiz_settings.txt"
def delete_setting(): 
    value_list = list(dictionary.values())
    while True:
        os.system("cls")
        deleting_index = select_setting("Delete Setting")
        if deleting_index == "X":
            return

        while True:
            os.system("cls")
            delete_check = input(f"{DIVIDER}\n\t\tPlease confirm your selection\n{DIVIDER}\n[ - ] {value_list[deleting_index][1]}: {value_list[deleting_index][2]}\n{DIVIDER}\n[ C ] Confirm\t\t[ X ] Back to Menu\n{DIVIDER}\n")
            
            if delete_check.upper() == "X":
                break
            elif delete_check.upper() == "C":
                writes_to_file(_QUIZ_SETTING_TEXT, "delete", deleting_index) 
                input("\033[0;31;40mOption has been deleted!\033[0;37;40m\nPress Enter to Continue\n")  
                break
            else:
                error_output("option")
                continue
        return

# Returns index value for menu navigation
# "title" parameter needs to be a string for the printing
def select_setting(title: str): 
    while True:
        value_number = input(f"{DIVIDER}\n\t\t\t{title}\n{DIVIDER}\n{view_file_content(1, 'settings')}{DIVIDER}\n[ X ] Back to Menu\n{DIVIDER}\n")
        os.system("cls")
        try:
            value = int(value_number)
        except ValueError:
            if value_number.upper() == "X": 
                return "X"
            else:
                error_output("option")
        else:
            if int(value_number) > len(dictionary) or int(value_number) <= 0:
                error_output("range")
            else:
                return (value - 1)

# ========================================================================
#   Generate Report Functions
# ========================================================================

# Logical system for generating report
def generate_report_logic():
    return

# ========================================================================
#   Sub Program Loops
# ========================================================================
def register_user_subloop():
    while SUB_LOOP:
        os.system("cls")
        read_file_content(_USERNAME_AND_PASSWORD, option="csv")
        user = print_menu("User")
        register_logic(user)

def question_pool_subloop():
    while SUB_LOOP:
        os.system("cls")
        read_file_content(_QUIZ_QUESTION_TEXT, option="question")
        questPool = print_menu("Question")
        question_logic(questPool)

def quiz_setting_subloop():
    while SUB_LOOP:
        os.system("cls")
        read_file_content(_QUIZ_SETTING_TEXT, option="settings")
        quizSettings = print_menu("Quiz Settings")    
        setting_logic(quizSettings)

def generate_report_subloop():
    while SUB_LOOP:
        os.system("cls")
        read_file_content(_QUIZ_RESULTS, option="csv")
        input("Generate Report")
        generate_report_logic()

# ========================================================================
#   Main Program Loop
# ========================================================================

# Try loop is used in order to catch any bad inputs the user might have done within the stack
while MAIN_LOOP:
    try:
        while MAIN_LOOP:
            os.system("cls")
            string = print_main(MAIN_MENU)
            main_logic(MAIN_MENU, string)
    except:
        error_output("bad_input")
