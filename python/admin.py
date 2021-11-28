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
# Known issues:	UI gets bugged when a long string gets added.
#

import os, re, csv
import hashlib, random
from sre_constants import error

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
# "file" is the input file path that you want to edit
# "option" is the method of which you want to write to the file
# "index" is an optional input you could use, such as for deleting words
def writes_to_file(file: str, option: str, index=None):
    # Converts the dictionary into a list
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
    elif option == "delete_user":
        # Removes the user from the csv file
        csv_dict_list.pop(index) 

        # Fieldnames are the key values of the first item in the dictionary.
        fields = csv_dict_list[0].keys()

        # Writes to the csv file with the correct headings and value
        with open(file, "w", newline="") as csvfile:
            csvwriter = csv.DictWriter(csvfile, fieldnames=fields)
            csvwriter.writeheader()
            csvwriter.writerows(csv_dict_list)
    
    # Edits question pool from the question pool text file
    elif option == "edit_question":
        with open(file, "w") as f:
            for line in value_list:
                temp_string = ""
                for i in line[1]:
                    temp_string += f"{i}||"
                f.write(f"{line[0]}||{temp_string}{line[2]}\n")

    # Edit setting variables from the settings text file
    elif option == "edit_setting":
        with open(file, "w") as f:
            for line in value_list:
                f.write(f"{line[0]}||{line[1]}||{line[2]}\n")


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

    # Gets the values of the current dictionary
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
            content += f"{header_text}\n{DIVIDER}\n"

            # Gets the values of each user stored in the system
            for sub_dict in csv_dict_list:
                # Reads from csv formatter
                csv_list = list(sub_dict.values())
                
                # Formats the input for display
                content += f"[ - ] {csv_list[0]}\t|  {csv_list[1][:10]}\t|\t{csv_list[2][:10]}...\t|\n" 
   
        # Formats dictionary for question w/o numbering
        elif option == "question":
            for item in value_list:
                sample = ""
                for j, option in enumerate(item[1]):
                    sample += f"\n{chr(97 + j)}) {option}"
                content += f"{item[0]}: {sample}\n\nAnswer: {item[2]}\n\n"
    
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

    if error_message == "option":               # Wrong option selected
        string += "\033[1;37;41mPlease select a valid option.\033[0;37;40m"

    elif error_message == "empty_input":        # Empty input
        string += f"\033[1;37;41mEmpty input, please try again\033[0;37;40m"

    elif error_message == "input":              # Invalid input
        string += "\033[1;37;41mPlease enter a valid input\033[0;37;40m\n"

    elif error_message == "range":              # Input value not within range
        string += "\033[1;37;41mPlease enter a value within the range.\033[0;37;40m"

    elif error_message == "special":            # Input field can't contain special characters  [Unique to admin.py]
        string += "\033[1;37;41mInput value can't contain special characters!\033[0;37;40m\n"

    elif error_message == "short":              # Input value was too short         
        string += "\033[1;37;41mLength of input was too short\033[0;37;40m\n"

    elif error_message == "long":               # Input value was too long           
        string += "\033[1;37;41mLength of input was too long\033[0;37;40m\n"
    
    elif error_message == "letter":             # Input value must contain letters              [Unique to admin.py]
        string += "\033[1;37;41mMust have at least one uppercase and lowercase character\033[0;37;40m\n"

    elif error_message == "username_match":     # Same username is found in the database        [Unique to admin.py]
        string += "\033[1;37;41mUsername exists already, please try another name\033[0;37;40m\n"

    elif error_message == "password":           # Doesn't meet the password criteria  
        string += "\033[1;37;41mMissing one of the criteria, please try again\033[0;37;40m\n"
    
    elif error_message == "email":              # Email in wrong format                         [Unique to admin.py]
        string += "\033[1;37;41mFormat of email was incorrect, please try again\033[0;37;40m\n"

    elif error_message == "bad_input":          # Bad Input --> Refers to EOFERROR (Occurs only when CTRL+Z is inputted)
        string += "\033[1;37;41mBad Input, program restarted\033[0;37;40m\n"
    
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
            error_output("range")
    # Check if the user wants to exit the menu
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
    if valueCap == "X":     # Closes menu
        global SUB_LOOP
        SUB_LOOP = False
        return
    elif valueCap == "1":   # Adds user
        add_user()
    elif valueCap == "2":   # Edit user
        edit_user()
    elif valueCap == "3":   # Delete user
        delete_user()
    else:
        error_output("input")
        return

# Check if username exist in the file
def check_username(username: str):
    read_file_content(_USERNAME_AND_PASSWORD, option="csv")
    for i in csv_dict_list:
        if username == i["userID"]:
            return True
    return False


# Add users to "userid_passwd.csv"
def add_user():
    while True:
        # Username check
        while True:
            os.system("cls")
            username_input = input(f"{DIVIDER}\n\t\t\tRegistering User\n{DIVIDER}\nUsername: \nEmail: \nPassword: \n{DIVIDER}\n[ X ] Back to Menu\n{DIVIDER}\nUsername: ")
            # Check if the user wants to exit the menu
            if username_input.upper() == "X":
                return
            elif not re.search(PATTERN, username_input):
                error_output("special")
                continue
            elif check_username(username_input):
                error_output("username_match")
                continue
            break

        # Email check
        while True:
            os.system("cls")
            email_input = input(f"{DIVIDER}\n\t\t\tRegistering User\n{DIVIDER}\nUsername: {username_input}\nEmail: \nPassword: \n{DIVIDER}\n[ X ] Back to Menu\n{DIVIDER}\nEnter email: ")
            
            # Check if the user wants to exit the menu
            if email_input.upper() == "X":
                return
            elif not re.search(EMAIL_PATTERN, email_input):
                error_output("email")
                continue
            break

        while True:
            # Password check
            while True:
                os.system("cls")
                password_input = input(f"{DIVIDER}\n\t\t\tRegistering User\n{DIVIDER}\nUsername: {username_input}\nEmail: {email_input}\nPassword: \n{DIVIDER}\n[ X ] Back to Menu\n{DIVIDER}\nAt least one number\nAt least one uppercase and one lowercase character\nAt least one special symbol !@#$%\nShould be 4 - 20 characters long\nPassword: ")
                
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
                password2 = input(f"{DIVIDER}\n\t\t\tRegistering User\n{DIVIDER}\nUsername: {username_input}\nEmail: {email_input}\nPassword: \n{DIVIDER}\n[ X ] Back to Menu\n{DIVIDER}\nPlease re-enter your password: ")
                
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
                        finalCheck = input(f"{DIVIDER}\n\t\t\tRegistering User\n{DIVIDER}\nUsername: {username_input}\nEmail: {email_input}\nPassword: {password_input}\n{DIVIDER}\n[ C ] Confirm\t\t[ X ] Exit\n{DIVIDER}\n")
                        
                        # Check if the user wants to exit the menu
                        if finalCheck.upper() == "X":
                            return
                        elif finalCheck.upper() == "C":
                            input("\033[0;32;40mYour changes have been saved!\033[0;37;40m\nPress Enter to Continue\n")
                            break
                        else:
                            error_output("option")
                            continue

                    # Formats the values into a dictionary for writing into csv
                    user_dict = {
                        "userID": username_input,
                        "email": email_input,
                        "password": user_password_hashing(password_input)
                    }

                    # Adds the new value into the list 
                    csv_dict_list.append(user_dict)
                    writes_to_file(_USERNAME_AND_PASSWORD, "csv")
                    return
                else: 
                    error_output("input")
                    continue


# Edits either the email or password from "userid_passwd.csv":
# Don't change the username as it might effect "quiz_result"
def edit_user():
    if len(csv_dict_list) == 0:
        input("User List is empty, please register some users.")
        return
    while True:
        os.system("cls")
        selected_user_index = input(f"{DIVIDER}\n\t\tEditing User\n{DIVIDER}\n{view_file_content(1, 'csv')}\n{DIVIDER}\nSelect a User\n{DIVIDER}\n[ X ] Back to Menu\n{DIVIDER}\n")
        
        # Checks if the string is empty
        if selected_user_index.upper() == "X":
            return
        elif not check_if_digit(selected_user_index):
            error_output("input")
            continue
        elif check_if_digit(selected_user_index):
            selection_for_user(int(selected_user_index) - 1)
            return
        else:
            error_output("input")

# Shows the selected user
def user_display(index: int):
    user_details = csv_dict_list[index]

    string = f"userID\t\t|\t{user_details['userID']}\n"
    string += f"email\t\t|\t{user_details['email']}\n"
    string += f"password\t|\t{user_details['password'][:10]}...\n"
    return string

def selection_for_user(index: int):
    selected = user_display(index)
    while True:
        os.system("cls")
        user_selection = input(f"{DIVIDER}\n\t\tEditing User\n{DIVIDER}\n{selected}\n{DIVIDER}\nSelect a User\n{DIVIDER}\n[ 1 ] Change Email\n[ 2 ] Change Password\n[ X ] Back to Menu\n{DIVIDER}\n")
        if user_selection.upper() == "X":
            return
        elif user_selection == "":
            error_output("empty_input")
            continue
        elif int(user_selection) < 1 or int(user_selection) > 2:
            error_output("range")
            continue
        elif check_if_digit(user_selection):
            local_loop = True

            # Change email
            if user_selection == "1":
                while local_loop:
                    os.system("cls")
                    new_email = input(f"{DIVIDER}\n\t\tEditing Email\n{DIVIDER}\n\tEmail\t|\t{csv_dict_list[index]['email']}\n{DIVIDER}\nPlease input your new email\n{DIVIDER}\n[ X ] Back to Menu\n{DIVIDER}\n")
                    if new_email.upper() == "X":
                        local_loop = False
                    elif new_email == "":
                        error_output("empty_input")
                        continue
                    elif not re.search(EMAIL_PATTERN, new_email):
                        error_output("email")
                        continue
                    break
                
                while local_loop:
                    os.system("cls")
                    confirm_change = input(f"{DIVIDER}\n\t\tConfirm Changes?\n{DIVIDER}\n\tOld email\t|\t{csv_dict_list[index]['email']}\n\tNew email\t|\t\033[1;37;40m{new_email}\033[0;37;40m\n{DIVIDER}\n[ C ] Confirm \n[ X ] Cancel Changes\n{DIVIDER}\n")
                    
                    # Check if the user wants to exit the menu
                    if confirm_change.upper() == "X":
                        local_loop = False
                    elif confirm_change == "":
                        error_output("empty_input")
                        continue
                    elif confirm_change.upper() == "C":
                        input("\033[0;32;40mYour changes have been saved!\033[0;37;40m\nPress Enter to Continue\n")                       
                    else:
                        error_output("input")
                        continue
                    break 

                if local_loop:
                    csv_dict_list[index]["email"] = new_email
                    writes_to_file(_USERNAME_AND_PASSWORD, "csv")
            # Change password
            elif user_selection == "2":
                while local_loop:
                    os.system("cls")
                    new_password = input(f"{DIVIDER}\n\t\tEditing Password\n{DIVIDER}\n\tPassword\t|\t{csv_dict_list[index]['password'][:10]}...\n{DIVIDER}\nPlease input your new password\n{DIVIDER}\n[ X ] Back to Menu\n{DIVIDER}\n")
                    if new_password.upper() == "X":
                        local_loop = False
                    elif new_password == "":
                        error_output("empty_input")
                        continue
                    elif len(new_password) < 4:
                        error_output("short")
                        continue
                    elif len(new_password) > 20:
                        error_output("long")
                        continue
                    elif not re.search(PASSWORD_PATTERN, new_password):
                        error_output("password")
                        continue
                    break

                while local_loop:
                    os.system("cls")
                    password2 = input(f"{DIVIDER}\n\t\tEditing Password\n{DIVIDER}\n\tPassword\t|\t{csv_dict_list[index]['password'][:10]}...\n{DIVIDER}\nPlease reneter your new password\n{DIVIDER}\n[ X ] Back to Menu\n{DIVIDER}\n")
                    if password2.upper() == "X":
                        local_loop = False
                    elif password2 == "":
                        error_output("empty_input")
                        continue
                    elif password2 == new_password:
                        break

                while local_loop:
                    os.system("cls")
                    confirm_change = input(f"{DIVIDER}\n\t\tConfirm Changes?\n{DIVIDER}\n\tOld Password\t|\t{csv_dict_list[index]['password'][:10]}\n\tNew password\t|\t\033[1;37;40m{user_password_hashing(new_password)[:10]}...\033[0;37;40m\n{DIVIDER}\n[ C ] Confirm \n[ X ] Cancel Changes\n{DIVIDER}\n")
                    
                    # Check if the user wants to exit the menu
                    if confirm_change.upper() == "X":
                        local_loop = False
                    elif confirm_change == "":
                        error_output("empty_input")
                        continue
                    elif confirm_change.upper() == "C":
                        input("\033[0;32;40mYour changes have been saved!\033[0;37;40m\nPress Enter to Continue\n")                       
                    else:
                        error_output("input")
                        continue
                    break 

                if local_loop:
                    csv_dict_list[index]["password"] = user_password_hashing(new_password)
                    writes_to_file(_USERNAME_AND_PASSWORD, "csv")
                    return
        else:
            error_output("input") 

# Deletes user from "userid_passwd.csv"
def delete_user():
    if len(csv_dict_list) == 0:
        input("User List is empty, please register some users.")
        return
    while True:
        os.system("cls")
        deleting_index = input(f"{DIVIDER}\n\t\tDeleting User\n{DIVIDER}\n{view_file_content(1, 'csv')}\n{DIVIDER}\nWhich user do you wish to delete?\n{DIVIDER}\n[ X ] Back to Menu\n{DIVIDER}\n")
        
        # Check if the user wants to exit the menu
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
            
            # Check if the user wants to exit the menu
            if delete_check.upper() == "X":
                break
            elif delete_check.upper() == "C":
                writes_to_file(_USERNAME_AND_PASSWORD, "delete_user", int(deleting_index) - 1) 
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
    if valueCap == "X":     # Closes menu
        global SUB_LOOP
        SUB_LOOP = False
        return
    elif valueCap == "1":   # Add question
        add_question()
    elif valueCap == "2":   # Edits question
        edit_question()
    elif valueCap == "3":
        delete_question()   # Delete question
    else:
        error_output("option")


# Add question into the "question_pool.txt"
def add_question():
    while True:
        while True:
            os.system("cls")
            print_option = ""
            no_of_options = input(f"{DIVIDER}\nHow many options do you want? [ 3 - 5 options ]\n{DIVIDER}\n[ X ] Back to Menu\n{DIVIDER}\n")
            
            # Check if the user wants to exit the menu
            if no_of_options.upper() == "X":
                return
            if check_if_digit(no_of_options):
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
            
            # Check if the user wants to exit the menu
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
                
                # Check if the user wants to exit the menu
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
            
            # Check if the user wants to exit the menu
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
            
            # Check if the user wants to exit the menu
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
def edit_question(): 
    # Gets the values of the current dictionary
    value_list = list(dictionary.values())
    if len(value_list) == 0:
        input("Question Pool is empty, please add some questions")
        return
    while True:
        os.system("cls")
        edit_index = selection_of_question("Editing Question")
        
        # Checks if the string is empty
        if edit_index == "":
            error_output("empty_input")
        
        # Execute if its not an integer       
        elif not check_if_digit(edit_index):
            if edit_index.upper() == "X":
                return  
            else:
                error_output("input")
        
        # Execute if its not integer       
        elif check_if_digit(edit_index):
            
            while True:
                # Displays the selected question
                selected_question_display = question_display(edit_index)

                os.system("cls")
                user_selection = input(f"{DIVIDER}\n\t\tEditing Question\n{DIVIDER}\n{selected_question_display}\n{DIVIDER}\nWhat do you want to edit?\n{DIVIDER}\n[ 1 ] Question Content\n[ 2 ] Question Options\n[ 3 ] Question Answer\n[ X ] Back to Menu\n{DIVIDER}\n")
                if user_selection.upper() == "X":
                    return
                elif check_if_digit(user_selection):
                    selection_for_question_pool(user_selection, edit_index)
                else:
                    error_output("input")
                    continue
        else:
            error_output("option")

# Use to display the selected question 
# "selected_index" is the selected question index
# "text" is used for adding addition text for the user
# "selection" is for knowing whether is the user editing the options or the answer
# as long as "selection" has a value, it
def question_display(selected_index: int):
    # Gets the values of the current dictionary
    value_list = list(dictionary.values())
    DIVIDER_2 = f"{EMPTY:-^60}"
    
    # Used to add information into the for loop
    string = f"\n{DIVIDER_2}\n"
    for element in value_list[selected_index]:
        # Prints out the options using a for-loop
        if type(element) is list:
            for i, item in enumerate(element):
                string += f"\t{chr(i + 97)})\t|  {item}\n"
        # Prints out the answer
        elif element is value_list[selected_index][-1]:
            string += f"\tAnswer\t|  {element}\n"
        # Prints out the question
        else:
            string += f"      Question  |  {element}\n"
        # Adds a divider line between sections
        string += f"{DIVIDER_2}\n"
    return string
    
# Logic for changing of the question content
def selection_for_question_pool(input_string: str, index: int):
    # Gets the values of the current dictionary
    value_list = list(dictionary.values())

    local_loop = True
    # Displays the selected question
    selected_question_display = question_display(index)

    # Used to change the question content
    if input_string == "1":
        while local_loop:
            os.system("cls")
            new_question_content = input(f"{DIVIDER}\n\t\tEditing Question Content\n{DIVIDER}\n{selected_question_display}\n{DIVIDER}\n[ X ] Back to Menu\n{DIVIDER}\n")
            
            # Check if the user wants to exit the menu
            if new_question_content.upper() == "X":
                local_loop = False
            elif new_question_content == "":
                error_output("empty_input")
                continue
            elif "||" in new_question_content:
                error_output("special")
                continue
            break

        while local_loop:
            os.system("cls")
            confirm_change = input(f"{DIVIDER}\n\t\tConfirm Changes?\n{DIVIDER}\n{selected_question_display}\nOriginal:\t{value_list[index][0]}\nNew:\t\t\033[1;37;40m{new_question_content}\033[0;37;40m\n{DIVIDER}\n[ C ] Confirm \n[ X ] Cancel Changes\n{DIVIDER}\n")
            
            # Check if the user wants to exit the menu
            if confirm_change.upper() == "X":
                local_loop = False
            elif confirm_change == "":
                error_output("empty_input")
                continue
            elif confirm_change.upper() == "C":
                input("\033[0;32;40mYour changes have been saved!\033[0;37;40m\nPress Enter to Continue\n")                       
            else:
                error_output("input")
                continue
            break  

        if local_loop:
            value_list[index][0] = new_question_content
            writes_to_file(_QUIZ_QUESTION_TEXT, "edit_question")

    # Used to change the options
    if input_string == "2":
        while local_loop:
            os.system("cls")
            option_number = input(f"{DIVIDER}\n\t\tEditing Question Options\n{DIVIDER}\n{selected_question_display}\n{DIVIDER}\n[ X ] Back to Menu\n{DIVIDER}\n")

            # Check if the user wants to exit the menu
            if option_number.upper() == "X":
                local_loop = False
            elif option_number == "":
                error_output("empty_input")
                continue
            # If its user input is in the list, return True
            elif check_user_input(option_number, value_list[index][1]):
                while True:
                    os.system("cls")
                    list_index =  ord(option_number) - 97
                    new_option_content = input(f"{DIVIDER}\n\t\tEditing Question Options\n{DIVIDER}\n{selected_question_display}\nSelected Option | {option_number}\n\tOption\t| {value_list[index][1][list_index]}\n\tNew\t|\n{DIVIDER}\n[ X ] Back to Menu\n{DIVIDER}\n")
                    
                    # Check if the user wants to exit the menu
                    if new_option_content.upper() == "X":
                        break
                    elif new_option_content == "":
                        error_output("empty_input")
                        continue
                    elif "||" in new_option_content:
                        error_output("special")
                        continue
                    break
            else:
                error_output("input")
                continue
            break

        while local_loop:
            os.system("cls")
            confirm_change = input(f"{DIVIDER}\n\t\tConfirm Changes?\n{DIVIDER}\n{selected_question_display}\nSelected Option | {option_number}\n\tOption\t| {value_list[index][1][list_index]}\n\tNew\t| \033[1;37;40m{new_option_content}\033[0;37;40m\n{DIVIDER}\n[ C ] Confirm\n[ X ] Back to Menu\n{DIVIDER}\n")
            
            # Check if the user wants to exit the menu
            if confirm_change.upper() == "X":
                local_loop = False
            elif confirm_change == "":
                error_output("empty_input")
                continue
            elif confirm_change.upper() == "C":
                input("\033[0;32;40mYour changes have been saved!\033[0;37;40m\nPress Enter to Continue\n")                                    
            else:
                error_output("input")
                continue
            break

        if local_loop:
            # Changes the answer if correct option content gets changed
            if value_list[index][1][list_index] == value_list[index][2]:
                value_list[index][2] = new_option_content
            value_list[index][1][list_index] = new_option_content
            writes_to_file(_QUIZ_QUESTION_TEXT, "edit_question")

    # Used to change the answer of the question
    if input_string == "3":
        while local_loop:
            os.system("cls")
            new_answer_content = input(f"{DIVIDER}\n\t\tEditing Question Answer\n{DIVIDER}\n{selected_question_display}\n{DIVIDER}\n[ X ] Back to Menu\n{DIVIDER}\n")
            
            # Check if the user wants to exit the menu
            if new_answer_content.upper() == "X":
                local_loop = False
            elif new_answer_content == "":
                error_output("empty_input")
                continue
            elif "||" in new_answer_content:
                error_output("special")
                continue
            elif check_user_input(new_answer_content, value_list[index][1]):
                list_index = ord(new_answer_content) - 97
                break
            else:
                error_output("input")
                continue

        while local_loop:
            os.system("cls")
            confirm_change = input(f"{DIVIDER}\n\t\tConfirm Changes?\n{DIVIDER}\n{selected_question_display}\nOriginal:\t{value_list[index][2]}\nNew:\t\t\033[1;37;40m{value_list[index][1][list_index]}\033[0;37;40m\n{DIVIDER}\n[ C ] Confirm \n[ X ] Cancel Changes\n{DIVIDER}\n")
            
            # Check if the user wants to exit the menu
            if confirm_change.upper() == "X":
                local_loop = False
            elif confirm_change == "":
                error_output("empty_input")  
            elif confirm_change.upper() == "C":
                input("\033[0;32;40mYour changes have been saved!\033[0;37;40m\nPress Enter to Continue\n")                       
                break
            else:
                error_output("input")
                continue

        if local_loop:
            # Saves the answer as the correct option text
            value_list[index][2] = value_list[index][1][list_index]
            writes_to_file(_QUIZ_QUESTION_TEXT, "edit_question")
    return


# Deletes question from "question_pool"
def delete_question():
    value_list = list(dictionary.values())
    if len(value_list) == 0:
        input("Question Pool is empty, please add some questions")
        return
    while True:
        os.system("cls")
        deleting_index = selection_of_question("Deleting Question")
        
        # Check if the user wants to exit the menu
        if deleting_index == "X":
            return
        else:
            deleting_index = int(deleting_index) - 1
            string = ""
            for j, element in enumerate(value_list[deleting_index][1]):
                string += f"{chr(97 + j)}) {element}\n"    

        while True:
            os.system("cls")
            delete_check = input(f"{DIVIDER}\n\t\tPlease confirm your selection\n{DIVIDER}\n{value_list[deleting_index][0]}\n{string}\n{value_list[deleting_index][2]}\n{DIVIDER}\n[ C ] Confirm\t\t[ X ] Back to Menu\n{DIVIDER}\n")
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


# Returns the index value for menu navigation
# Checks if the inputted value is within range of the available options
# 
# "title" parameter needs to be a string for the printing
def selection_of_question(title: str):
    value_list = list(dictionary.values())
    while True:
        os.system("cls")
        value_number = input(f"{DIVIDER}\n\t\t{title}\n{DIVIDER}\n{view_file_content(1, 'question')}{DIVIDER}\n[ X ] Back to Menu\n{DIVIDER}\n")
        
        # Check if the user wants to exit the menu
        if value_number.upper() == "X":
            return "X"
        elif not check_if_digit(value_number):
            error_output("input")
        elif  int(value_number) <= 0 or int(value_number) > len(dictionary): 
            error_output("range")
        else:
            return (int(value_number) - 1)

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
                error_output("empty_input")
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
        edit_index = selection_of_setting("Editing Settings")

        # Execute if its not an integer
        if not check_if_digit(edit_index): 
            if edit_index.upper() == "X":
                return  
            else:
                error_output("input")

        # Execute if its an integer        
        elif check_if_digit(edit_index): 
            while True:
                os.system("cls")
                user_selection = input(f"{DIVIDER}\nWhat do you want to edit?\n{DIVIDER}\nName: {value_list[edit_index][1]}\nValue: {value_list[edit_index][2]}\n{DIVIDER}\n[ 1 ] Setting Name\n[ 2 ] Setting Value\n{DIVIDER}\n[ X ] Back to Menu\n{DIVIDER}\n")
                if user_selection.upper() == "X":
                    return    
                elif check_if_digit(user_selection):
                    selection_for_edit_setting(user_selection, edit_index)
                else:
                    error_output("input")
                    continue
        else:
            error_output("option")

# Logic for changing of name or value of a setting.
def selection_for_edit_setting(input_string: str, index: int):
    value_list = list(dictionary.values())
    local_loop = True
    # Used to change setting name
    if input_string == "1":
        while local_loop:
            os.system("cls")
            new_name = input(f"{DIVIDER}\nName: \033[1;37;40m>>> {value_list[index][1]} <<<\033[0;37;40m\nValue: {value_list[index][2]}\n{DIVIDER}\n[ X ] Back to Menu\n{DIVIDER}\nPlease input a new name: ")
            
            if new_name.upper() == "X":
                local_loop = False
            elif new_name == "":
                error_output("empty_input")
                continue 
            elif not re.search(PATTERN, new_name):
                error_output("special")
                continue 
            break

        while local_loop:
            os.system("cls")
            confirm_change = input(f"{DIVIDER}\n\t\tConfirm Changes?\n{DIVIDER}\nName: \033[1;37;40m>>> {new_name} <<<\033[0;37;40m\nValue: {value_list[index][2]}\n{DIVIDER}\n[ C ] Confirm \n[ X ] Cancel Changes\n{DIVIDER}\n")
            
            # Check if the user wants to exit the menu
            if confirm_change.upper() == "X":
                local_loop = False
            elif confirm_change == "":
                error_output("empty_input")
                continue
            elif confirm_change.upper() == "C":
                input("\033[0;32;40mYour changes have been saved!\033[0;37;40m\nPress Enter to Continue\n")                                    
                break
            else:
                error_output("input")
                continue

        if local_loop:
            # Change the name of item
            value_list[index][1] = new_name
            writes_to_file(_QUIZ_SETTING_TEXT, "edit_setting")   

    # Used to change the setting value             
    elif input_string == "2":
        while local_loop:
            os.system("cls")
            new_value = input(f"{DIVIDER}\nName: {value_list[index][1]}\nValue: \033[1;37;40m>>> {value_list[index][2]} <<<\033[0;37;40m\n{DIVIDER}\n[ X ] Back to Menu\n{DIVIDER}\nPlease input new value: ")
            if new_value.upper() == "X":
                local_loop = False   
            elif not re.search(PATTERN, new_value) or "||" in new_value:
                error_output("special")
                continue
            break

        while local_loop:
            os.system("cls")
            confirm_change = input(f"{DIVIDER}\n\t\tConfirm Changes?\n{DIVIDER}\nSetting Name: {value_list[index][1]}\nSetting Value: \033[1;37;40m>>> {new_value} <<<\033[0;37;40m\n{DIVIDER}\n[ C ] Confirm \n[ X ] Cancel Changes\n{DIVIDER}\n")
            if confirm_change.upper() == "X":
                local_loop = False
            elif confirm_change == "":
                error_output("empty_input")
                continue
            elif confirm_change.upper() == "C":
                input("\033[0;32;40mYour changes have been saved!\033[0;37;40m\nPress Enter to Continue\n")                       
                break              
            else:
                error_output("input")
                continue

        if local_loop:
            # Changes the value of the item
            value_list[index][2] = new_value
            writes_to_file(_QUIZ_SETTING_TEXT, "edit_setting") 
    else:
        error_output("option")     


# Deletes settings from "quiz_settings.txt"
def delete_setting(): 
    value_list = list(dictionary.values())
    while True:
        os.system("cls")
        deleting_index = selection_of_setting("Deleting Setting")
        if deleting_index == "X":
            return

        while True:
            os.system("cls")
            delete_check = input(f"{DIVIDER}\n\t\tPlease confirm your selection\n{DIVIDER}\n[ - ] {value_list[deleting_index][1]}: {value_list[deleting_index][2]}\n{DIVIDER}\n[ C ] Confirm\t\t[ X ] Back to Menu\n{DIVIDER}\n")
            # Check if the user wants to exit the menu
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
# Checks if the inputted value is within range of the available options
# 
# "title" parameter needs to be a string for the printing
def selection_of_setting(title: str): 
    while True:
        os.system("cls")
        value_number = input(f"{DIVIDER}\n\t\t\t{title}\n{DIVIDER}\n{view_file_content(1, 'settings')}{DIVIDER}\n[ X ] Back to Menu\n{DIVIDER}\n")
        # Check if the user wants to exit the menu
        if value_number.upper() == "X": 
            return "X"
        elif not check_if_digit(value_number):
            error_output("option")
        # 
        elif int(value_number) <= 0 or int(value_number) > len(dictionary):
            error_output("range")
        else:
            return (int(value_number) - 1)

# ========================================================================
#   Generate Report Functions
# ========================================================================

# Logical system for generating report
def generate_report_logic():
    data = generate_report()
    report_input = input(f"{DIVIDER}\n\t\tReport\n{DIVIDER}\n{data}\n{DIVIDER}\n[ X ] Back to Menu\n{DIVIDER}\n")
    if report_input.upper() == "X":
        global SUB_LOOP
        SUB_LOOP = False
        return
    elif report_input == "":
        error_output("empty_input")
    else: 
        error_output("input")
    return

# Retrieving and generating a data report
def generate_report():
    # Initalize variables for calculation
    string = ""
    total_marks = 0
    marks = []
    students = []
    question_correct = 0
    question_wrong = 0
    total_questions = 0

    # Retrieves the data from the list
    for attempt in csv_dict_list:
        # Gets the total marks 
        total_marks += int(attempt["Total Marks"])
        marks.append(int(attempt["Total Marks"]))

        total_questions += int(attempt["Total No. of Question"])

        question_correct += int(attempt["No. Qn answered correct"])
        question_wrong += int(attempt["No. Qn answered wrong"])

        # Add users into the "student" list
        if attempt["UserID"] not in students:
            students.append(attempt["UserID"])
    
    # Gettings the values
    total_attempts = len(csv_dict_list)
    no_of_students = len(students)
    percent_question_correct = question_correct / total_questions * 100
    percent_question_wrong = question_wrong / total_questions * 100
    average_marks = total_marks / total_attempts
    min_marks = min(marks)
    max_marks = max(marks)

    # Adds data into the string
    string += f"Total Number of Attempts:  \033[1;37;40m{total_attempts}\033[0;37;40m\n"
    string += f"Number of Students attempted:  \033[1;37;40m{no_of_students}\033[0;37;40m\n"
    string += f"Average Marks:  \033[1;37;40m{average_marks}\033[0;37;40m\n"
    string += f"Percentage of Question Correct:  \033[1;37;40m{percent_question_correct}%\033[0;37;40m\n"
    string += f"Percentage of Question Wrong:  \033[1;37;40m{percent_question_wrong}%\033[0;37;40m\n"
    string += f"Min marks: \033[1;37;40m{min_marks}\033[0;37;40m\n"
    string += f"Max marks:  \033[1;37;40m{max_marks}\033[0;37;40m\n"

    return string

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
