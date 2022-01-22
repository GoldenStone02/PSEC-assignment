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
#               C:\PSEC_project\users.json
#               C:\PSEC_project\quiz_results.csv
# 
# Output file:  C:\PSEC_project\question_pool.json
#               C:\PSEC_project\quiz_settings.json
#               C:\PSEC_project\users.json
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
# Module /      os, re, csv, hashlib, json, getpass
#
# Known issues:	N/A
#

import os, re, csv, hashlib
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

MAIN_MENU = ["User Configuration", "Course Settings", "Question Pool", "Quiz Settings", "Generate Report"]

_USERNAME_AND_PASSWORD = "./server/users.json"   # Stored as a list
_QUIZ_SETTING = "./server/quiz_settings.json"    # Stored as a dict
_QUESTION_POOL = "./server/question_pool.json"    # Stored as a list
_QUIZ_RESULTS = "./server/quiz_results.csv"      # Stored as a csv

# ==================================================================
#   Socket Programming Functions
# ==================================================================

# if have time then, do

# ==================================================================
#   General Functions
# ==================================================================

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

# [ISSUE] Haven't converted everything into json yet

# Writes changes to the selected file
# "file_path" is the input file path that you want to edit
# "option" is the method of which you want to write to the file
# "input_variable" written into the file
def writes_to_file(file_path: str, option: str, input_variable: any):
    # # Writes items into csv file 
    # if option == "csv":
    #     # Fieldnames are the key values of the first item in the dictionary.
    #     fields = csv_dict_list[0].keys()

    #     # Writes to the csv file with the correct headings and value
    #     with open(file_path, "w", newline="") as csvfile:
    #         csvwriter = csv.DictWriter(csvfile, fieldnames=fields)
    #         csvwriter.writeheader()
    #         csvwriter.writerows(csv_dict_list)
    
    # Writes whatever that's in the "input_variable" onto the specified file 
    if option == "json":
        with open(file_path, "w") as f:
            json.dump(input_variable, f, indent=4)
    # Deletes items from json file
    elif option == "delete_setting":
        file_dict = read_file(file_path, option="json")
        for item in file_dict:
            if item == input_variable:
                del file_dict[item]
                break
        with open(file_path, "w") as f:
            json.dump(file_dict, f, indent=4)
    
    # Deletes items from json files
    elif option == "delete_user":
        file_dict = read_file(file_path, option="json")
        for item in file_dict:
            if item['userID'] == input_variable['userID']:
                deleting_index = file_dict.index(item)
                del file_dict[deleting_index]
        with open(file_path, "w") as f:
            json.dump(file_dict, f, indent=4)
    # Edits question pool from the question pool json file
    elif option == "edit_question":
        return


# Returns the file content using "dictionary"
# "show_number" parameter is used to define the format of returning string.
# "0" prints out file content without numbering
# "1" prints out with sequence numbering
# "option" is used to identify what menu the user's on and prints out that specific menu
# "input_file_path" is the filepath
# "check" is used as an additional variable
def view_file_content(show_numbers: int, option: str, input_file_path: str, check=None):
    content = ""
    # Get the file information
    file_dictionary = read_file(input_file_path, option="json")

    # [ISSUE] Need to properly format the string
    if show_numbers == 1:
        match option:
            # Formats dictionary for settings with numbering
            case "setting":
                for i, item in enumerate(file_dictionary[check]):
                    if type(file_dictionary[check][item]) == dict:
                        content += f"[ {i + 1} ] {item}: Edit to view info\n"
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

            # Formats dictionary for question with numbering
            case "question":
                for i, item in enumerate(file_dictionary): 
                    sample = ""
                    for j, option in enumerate(file_dictionary[i][1]):
                        sample += f"\n\t{chr(97 + j)}) {option}"
                    content += f"[ {i + 1} ] {file_dictionary[i][0]}: {sample}\n\n"
    elif show_numbers == 0:
        match option:
            # Formats dictionary for settings w/o numbering
            case "setting":
                for item in file_dictionary[check]:
                    if type(file_dictionary[check][item]) == dict:
                        content += f"[ - ] {item}: Edit to view info\n"
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

            # Formats dictionary for question w/o numbering
            case "question":
                for item in file_dictionary:
                    sample = ""
                    for j, option in enumerate(item['modules']):
                        sample += f"\n{chr(97 + j)}) {option}"
                    content += f"{item[0]}: {sample}\n\nAnswer: {item[2]}\n\n"
    return content


# Prints the text file with some UI.
# Needs to happen after "read_file()" has been executed
# "file_path" is used to know where to retrieve the data
# "check" is used as an additional input if there need be
def print_menu(file_path: str, check=None): 
    # Allows for dynamic change of the program using only one UI
    if file_path == _USERNAME_AND_PASSWORD:
        option_name = "User"
    elif file_path == _QUIZ_SETTING:
        option_name = "Setting"
    elif file_path == _QUESTION_POOL:
        if check == "course":
            option_name = "Course"
        elif check == "question":
            option_name = "Question"

    content = f"{dynamic_divider()}\n\t\t\033[1;37;40m {option_name}\033[0;37;40m\n{dynamic_divider()}\n"
    content += view_file_content(0, option_name.lower(), file_path, check)
    content += f"{dynamic_divider()}\n\tSelect one of the options\n{dynamic_divider()}\n"
    content += f"[ 1 ] Add New {option_name}\n[ 2 ] Edit {option_name}\n[ 3 ] Delete {option_name}\n[ X ] Back to Main\n{dynamic_divider()}\n"
    os.system("cls")
    user_input = input(content)
    return user_input


# Checks if the user's selected option in inside the range of options 
# For any question. Due to the flexibility of the number of options the admin can set.
# "given_user_input" is the user input that will be checked to see if the input is within the range of the options
# "question_data" is a list containing the question info, such as content, options and answer
def check_user_input(userInput: str, question_data: list) -> bool:
    check_list = []
    for i, option in enumerate(question_data):
        check_list.extend(chr(97 + i))
    for check in check_list:
        if check == userInput.lower():
            return True
    return False


# Used for easy maintainence of error outputs
def error_output(error_message: str, optional=None):
    match error_message:
        case "option":             # Wrong option selected
            string = "\033[1;37;41mPlease select a valid option.\033[0;37;40m\n"

        case "empty_input":        # Empty input
            string = f"\033[1;37;41mEmpty input, please try again\033[0;37;40m\n"

        case "input":              # Invalid input
            string = "\033[1;37;41mPlease enter a valid input\033[0;37;40m\n"

        case "range":              # Input value not within range
            string = "\033[1;37;41mPlease enter a value within the range.\033[0;37;40m\n"

        case "special":            # Input field can't contain special characters  [Unique to admin.py]
            string = "\033[1;37;41mInput value can't contain special characters!\033[0;37;40m\n"

        case "short":              # Input value was too short         
            string = "\033[1;37;41mLength of input was too short\033[0;37;40m\n"

        case "long":               # Input value was too long           
            string = "\033[1;37;41mLength of input was too long\033[0;37;40m\n"
        
        case "letter":             # Input value must contain letters              [Unique to admin.py]
            string = "\033[1;37;41mMust have at least one uppercase and lowercase character\033[0;37;40m\n"

        case "username_match":     # Same username is found in the database        [Unique to admin.py]
            string = "\033[1;37;41mUsername exists already, please try another name\033[0;37;40m\n"

        case "password":           # Doesn't meet the password criteria  
            string = "\033[1;37;41mMissing one of the criteria, please try again\033[0;37;40m\n"
        
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
def dynamic_divider():
    column, row = os.get_terminal_size()
    output = f"{EMPTY:=^{column}}"
    return output


# ============================================================================================
#   Main Page Functions
# ============================================================================================

# Prints page with a list, checks whether is input is in range of list
# "input_list" parameter is for dynamic changing of the menu
def print_main(input_list: list):
    content = f"{dynamic_divider()}\n\t\t\t\033[1;37;40m Main \033[0;37;40m\n{dynamic_divider()}\n"
    for i, element in enumerate(input_list):
        content += f"[ {i+1} ] {element}\n"
    content += f"[ X ] Exit Application\n{dynamic_divider()}\n"
    return content


# Main logical system for selection page
# "menu_list" is meant for easily change within the UI.
# "input_loop" is used as the 
def main_logic(content: str):
    sub_loop = True
    stored_value = input(content)
    match stored_value.upper():
        case "X":
            getpass.getpass("\033[0;32;40mLogging out...\033[0;37;40m")
            return False
        case "1":
            register_user_subloop(sub_loop)
        case "2":
            course_info_subloop(sub_loop)
        case "3":       # Check if I want this to be here
            question_pool_subloop(sub_loop)
        case "4":
            quiz_setting_subloop(sub_loop)
        case "5":
            generate_report_subloop(sub_loop)
        case _:
            error_output("option")

# ===================================================================================================
#   Register User Functions
# ===================================================================================================

# [ISSUE] Not functional at this time
def register_logic():
    userInput = print_menu(_USERNAME_AND_PASSWORD)
    # Loads up the JSON file into a dictionary 
    user_info = read_file(_USERNAME_AND_PASSWORD, "json")

    valueCap = userInput.upper()
    match valueCap:
        case "X": # Closes menu
            return False
        case "1":   # Adds user
            add_user(user_info)
        case "2":   # Edit user
            edit_user(user_info)
        case "3":   # Delete user
            delete_user(user_info)
        case _:
            error_output("input")

# Check if username exist in the file
def check_username(username: str):
    users = read_file(_USERNAME_AND_PASSWORD, option="json")
    for i in users:
        if username == i["userID"]:
            return True
    return False

# Add users to "users.json"
# Each user requires a userID, password, email, current course.
# Checks for the user's course in order to get the eligible modules
# "input_list" is the list of users inside "users.json"
def add_user(input_list: list):
    while True:
        # Username check
        while True:
            os.system("cls")
            userid_input = input(f"{dynamic_divider()}\n\t\t\tRegistering User\n{dynamic_divider()}\nUserID: \nCourse: \nEmail: \nPassword: \n{dynamic_divider()}\n[ X ] Back to Menu\n{dynamic_divider()}\nEnter in a UserID: ")
            # Check if the user wants to exit the menu
            if userid_input.upper() == "X":
                return
            elif not re.search(PATTERN, userid_input):
                error_output("special")
                continue
            elif check_username(userid_input):
                error_output("username_match")
                continue
            break
        
        course_list, course_list_string = check_user_courses()
        # Course check
        while True:
            os.system("cls")
            course_number_input = input(f"{dynamic_divider()}\n\t\t\tRegistering User\n{dynamic_divider()}\nUserID: {userid_input}\nCourse: \nEmail: \nPassword: \n{dynamic_divider()}\nAvailable Courses:\n{course_list_string}{dynamic_divider()}\n[ X ] Back to Menu\n{dynamic_divider()}\nEnter in your course: ")
            
            # Check if the user wants to exit the menu
            if course_number_input.upper() == "X":
                return
            elif not course_number_input.isdigit():
                error_output("input")
                continue
            elif int(course_number_input) <= 0 or int(course_number_input) > len(course_list):
                error_output("course", course_list)
                continue
            break
        
        # Convert the course number into course name
        course_input = course_list[int(course_number_input) - 1]

        # Email check
        while True:
            os.system("cls")
            email_input = input(f"{dynamic_divider()}\n\t\t\tRegistering User\n{dynamic_divider()}\nUserID: {userid_input}\nCourse: {course_input}\nEmail: \nPassword: \n{dynamic_divider()}\n[ X ] Back to Menu\n{dynamic_divider()}\nEnter your email: ")
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
                password_input = getpass.getpass(f"{dynamic_divider()}\n\t\t\tRegistering User\n{dynamic_divider()}\nUserID: {userid_input}\nCourse: {course_input}\nEmail: {email_input}\nPassword: \n{dynamic_divider()}\n[ X ] Back to Menu\n{dynamic_divider()}\nAt least one number\nAt least one uppercase and one lowercase character\nAt least one special symbol !@#$%\nShould be 4 - 20 characters long\nEnter in your password: ")
                
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
                password2 = getpass.getpass(f"{dynamic_divider()}\n\t\t\tRegistering User\n{dynamic_divider()}\nUserID: {userid_input}\nCourse: {course_input}\nEmail: {email_input}\nPassword: \n{dynamic_divider()}\n[ X ] Back to Menu\n{dynamic_divider()}\nPlease re-enter your password: ")
                
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
                        finalCheck = input(f"{dynamic_divider()}\n\t\t\tRegistering User\n{dynamic_divider()}\nUserID: {userid_input}\nCourse: {course_input}\nEmail: {email_input}\nPassword: {len(password_input) * '*'}\n{dynamic_divider()}\n[ C ] Confirm\t\t[ X ] Exit\n{dynamic_divider()}\n")
                        
                        # Check if the user wants to exit the menu
                        if finalCheck.upper() == "X":
                            return
                        elif finalCheck.upper() == "C":
                            input("\033[0;32;40mYour changes have been saved!\033[0;37;40m\nPress Enter to Continue\n")
                            break
                        else:
                            error_output("option")
                            continue

                    # Formats the values into a dictionary for writing into json file
                    user_dict = {
                        "userID": userid_input,
                        "email": email_input,
                        "password_SHA256": user_password_hashing(password_input),
                        "current_course": course_input,
                        "modules": check_user_modules(course_input)
                    }

                    # Adds the new value into the list 
                    input_list.append(user_dict)
                    writes_to_file(_USERNAME_AND_PASSWORD, "json", input_list)
                    return
                else: 
                    error_output("input")
                    continue


# Edits either the email or password from "users.json":
# Not allowed to change the username as it might effect "quiz_result"
def edit_user(input_list: list):
    if len(input_list) == 0:
        input("User List is empty, please register some users.")
        return
    while True:
        os.system("cls")
        selected_user_index = input(f"{dynamic_divider()}\n\t\tEditing User\n{dynamic_divider()}\n{view_file_content(1, 'user', _USERNAME_AND_PASSWORD)}{dynamic_divider()}\n\t\tSelect a User\n{dynamic_divider()}\n[ X ] Back to Menu\n{dynamic_divider()}\n")
        
        # Checks if the string is empty
        if selected_user_index.upper() == "X":
            return
        elif not selected_user_index.isdigit():
            error_output("input")
            continue
        elif selected_user_index.isdigit():
            selection_for_user(input_list, int(selected_user_index) - 1)
            return
        else:
            error_output("input")

# Shows the selected user
def user_display(input_list: list, index: int):
    user_details = input_list[index]

    string = f"userID\t\t|  \033[4;31;40m{user_details['userID']}\033[0;37;40m\n"
    string += f"email\t\t|  \033[4;31;40m{user_details['email'][:10]}...\033[0;37;40m\n"
    string += f"hashed password\t|  \033[4;31;40m{user_details['password_SHA256'][:10]}...\033[0;37;40m\n"
    string += f"course\t\t|  \033[4;31;40m{user_details['current_course']}\033[0;37;40m"
    return string

def selection_for_user(input_list: list, index: int):
    selected = user_display(input_list, index)
    while True:
        os.system("cls")
        user_selection = input(f"{dynamic_divider()}\n\t\tEditing User\n{dynamic_divider()}\n{selected}\n{dynamic_divider()}\nSelect a User\n{dynamic_divider()}\n[ 1 ] Change Email\n[ 2 ] Change Password\n[ 3 ] Change Course\n[ X ] Back to Menu\n{dynamic_divider()}\n")
        if user_selection.upper() == "X":
            return
        elif user_selection == "":
            error_output("empty_input")
            continue
        elif int(user_selection) < 1 or int(user_selection) > 3:
            error_output("range")
            continue
        else:
            edit_user_parameters(user_selection, input_list, index)

# Used to edit specific settings for a user
def edit_user_parameters(selection: str, input_list: list, index: int):
    local_loop = True
    match selection:
    # Change email
        case "1":
            while local_loop:
                os.system("cls")
                new_email = input(f"{dynamic_divider()}\n\t\tEditing Email\n{dynamic_divider()}\n\tEmail\t|\t{input_list[index]['email']}\n{dynamic_divider()}\nPlease input your new email\n{dynamic_divider()}\n[ X ] Back to Menu\n{dynamic_divider()}\n")
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
                confirm_change = input(f"{dynamic_divider()}\n\t\tConfirm Changes?\n{dynamic_divider()}\n\tOld email\t|\t{input_list[index]['email']}\n\tNew email\t|\t\033[1;37;40m{new_email}\033[0;37;40m\n{dynamic_divider()}\n[ C ] Confirm \n[ X ] Cancel Changes\n{dynamic_divider()}\n")
                
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
                input_list[index]["email"] = new_email
                writes_to_file(_USERNAME_AND_PASSWORD, "json", input_list)
        # Change password
        case "2":
            while local_loop:
                os.system("cls")
                new_password = getpass.getpass(f"{dynamic_divider()}\n\t\tEditing Password\n{dynamic_divider()}\n\tPassword\t|\t{input_list[index]['password_SHA256'][:10]}...\n{dynamic_divider()}\nPlease input your new password\n{dynamic_divider()}\n[ X ] Back to Menu\n{dynamic_divider()}\n")
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
                password2 = getpass.getpass(f"{dynamic_divider()}\n\t\tEditing Password\n{dynamic_divider()}\n\tPassword\t|\t{input_list[index]['password_SHA256'][:10]}...\n{dynamic_divider()}\nPlease reneter your new password\n{dynamic_divider()}\n[ X ] Back to Menu\n{dynamic_divider()}\n")
                if password2.upper() == "X":
                    local_loop = False
                elif password2 == "":
                    error_output("empty_input")
                    continue
                elif password2 == new_password:
                    break

            while local_loop:
                os.system("cls")
                confirm_change = input(f"{dynamic_divider()}\n\t\tConfirm Changes?\n{dynamic_divider()}\n\tOld Password\t|\t{input_list[index]['password_SHA256'][:10]}\n\tNew password\t|\t\033[1;37;40m{user_password_hashing(new_password)[:10]}...\033[0;37;40m\n{dynamic_divider()}\n[ C ] Confirm \n[ X ] Cancel Changes\n{dynamic_divider()}\n")
                
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
                input_list[index]["password_SHA256"] = user_password_hashing(new_password)
                writes_to_file(_USERNAME_AND_PASSWORD, "json", input_list)
                return
        case "3":
            while local_loop:
                os.system("cls")
                new_course = input(f"test\n{input_list}")
                if new_course.upper() == "X":
                    local_loop = False
                elif new_course == "":
                    error_output("empty_input")
                    continue
                
        case _:
            error_output("input") 

# Deletes user from "userid_passwd.json"
def delete_user(input_list: list):
    if len(input_list) == 0:
        input("User List is empty, please register some users.")
        return
    while True:
        os.system("cls")
        user_index = input(f"{dynamic_divider()}\n\t\tDeleting User\n{dynamic_divider()}\n{view_file_content(1, 'user', _USERNAME_AND_PASSWORD)}{dynamic_divider()}\nWhich user do you wish to delete?\n{dynamic_divider()}\n[ X ] Back to Menu\n{dynamic_divider()}\n")
        
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
            os.system("cls")
            delete_check = input(f"{dynamic_divider()}\n\t\tDeleting User\n{dynamic_divider()}\n{content}\n{dynamic_divider()}\nPlease confirm your selection\n{dynamic_divider()}\n[ C ] Confirm\t[ X ] Back to Menu\n{dynamic_divider()}\n")
            
            # Check if the user wants to exit the menu
            if delete_check.upper() == "X":
                break
            elif delete_check.upper() == "C":
                writes_to_file(_USERNAME_AND_PASSWORD, "delete_user", selected_user) 
                input("\033[0;31;40mUser has been deleted!\033[0;37;40m\nPress Enter to Continue\n") 
                break
            else:
                error_output("option")
                continue

# returns available courses and the list of courses
def check_user_courses():
    # Loads in course information for reference
    course_info = read_file(_QUESTION_POOL, option="json")
        
    # Appends all course into a list
    course_list = []
    course_list_string = ""
    for item in course_info:
        course_list.append(item['course'])
    
    for i, course in enumerate(course_list):
        course_list_string += f"[ {i + 1} ] {course}\n"
    return course_list,course_list_string

# return available modules for the selected course
def check_user_modules(current_course):
    course_info = read_file(_QUESTION_POOL, "json")
    output = []
    for element in course_info:
        if element['course'] == current_course:
            for module in element['modules']:
                module_dict = {
                    "module_name": module['module_name'],
                    "grade": None
                }
                output.append(module_dict)
    return output

# Hashes the user's password
def user_password_hashing(userInput: str): 
    output = hashlib.sha256(userInput.encode())
    return output.hexdigest()

# ===================================================================================================
#   Course Functions
# ===================================================================================================

def course_logic():
    userInput = print_menu(_QUESTION_POOL, "course")
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


# Add a new course into the 
def add_course(input_list: list):
    while True:
        os.system("cls")
        new_course = input(f"{dynamic_divider()}\n\t\tAdd Courses\n{dynamic_divider()}\n{view_file_content(0, 'course', _QUESTION_POOL)}{dynamic_divider()}\n[ X ] Back to the Menu\n{dynamic_divider()}\n")
        if new_course.upper() == "X":
            return
        elif new_course.isdigit():
            pass
        elif not new_course.isdigit():
            for element in input_list:
                if new_course.lower() == element['course'].lower():
                    print(element)
                    error_output("range")
                    continue


# Edit course information
def edit_course(input_list: list):
    while True:
        os.system("cls")
        edit_course = input(f"{dynamic_divider()}\n\t\tEdit Courses\n{dynamic_divider()}\n{view_file_content(1, 'course', _QUESTION_POOL)}{dynamic_divider()}\n[ X ] Back to the Menu\n{dynamic_divider()}\n")
        if edit_course.upper() == "X":
            return
        elif len(edit_course) < 0 or len(edit_course) > len(input_list):
            error_output("range")


# Delete selected course
def delete_course(input_list: list):
    return

# ===================================================================================================
#   Question Pool Functions
# ===================================================================================================
# Admin user would need to select the course and the module before being able to edit the question pool
# [ISSUE] Need to fully overhaul this system in order for the course system to function

# Logicial system for question pool
def question_logic(userInput: str):
    userInput = print_menu(_QUESTION_POOL, "question")
    # Loads up the JSON file into a dictionary 
    user_info = read_file(_QUESTION_POOL, "json")

    valueCap = userInput.upper()
    match valueCap:
        case "X":   # Closes menu
            return False
        case "1":   # Add question
            add_question()
        case "2":   # Edits question
            edit_question()
        case "3":   # Delete question
            delete_question()   
        case _:
            error_output("option")


# Add question into the "question_pool.json"
def add_question():
    while True:
        while True:
            os.system("cls")
            print_option = ""
            no_of_options = input(f"{dynamic_divider()}\nHow many options do you want? [ 3 - 5 options ]\n{dynamic_divider()}\n[ X ] Back to Menu\n{dynamic_divider()}\n")
            
            # Check if the user wants to exit the menu
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
            question = input(f"{dynamic_divider()}\n\t\t\tAdding Question\n{dynamic_divider()}\nQuestion: \n\nOptions: \n{print_option}\n\nAnswer: \n\n{dynamic_divider()}\n[ X ] Back to Menu\n{dynamic_divider()}\nInput Question: ")
            
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
                options = input(f"{dynamic_divider()}\n\t\t\tAdding Options\n{dynamic_divider()}\nQuestion: {question}\n\nOptions: \n{string}\n\n Answer: \n\n{dynamic_divider()}\n[ X ] Back to Menu\n{dynamic_divider()}\nInput Options: ")
                
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
            answer = input(f"{dynamic_divider()}\n\t\t\tAdding Answers\n{dynamic_divider()}\nQuestion: {question}\n\nOptions: \n{string}\n\nAnswer: \n\n{dynamic_divider()}\n[ X ] Back to Menu\n{dynamic_divider()}\nCorrect Answer: ")
            
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
            confirm_change = input(f"{dynamic_divider()}\n\t\t\tConfirming Question\n{dynamic_divider()}\nQuestion: {question}\n\nOptions: \n{string}\n\nAnswer: {answer}\n\n{dynamic_divider()}\n[ C ] Confirm\t\t[ X ] Back to Menu\n{dynamic_divider()}\n")
            
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

        with open(_QUESTION_POOL, "a") as f:
            f.write(string)
        return
    

# Edits question from "question_pool"
def edit_question(): 
    # Gets the values of the current dictionary
    if len(dictionary) == 0:
        input("Question Pool is empty, please add some questions")
        return
    while True:
        os.system("cls")
        edit_index = selection_of_question("Editing Question")
        
        # Checks if the string is empty
        if edit_index == "":
            error_output("empty_input")
        
        # Execute if its not an integer       
        elif not edit_index.isdigit():
            if edit_index.upper() == "X":
                return  
            else:
                error_output("input")
        
        # Execute if its not integer       
        elif edit_index.isdigit():
            
            while True:
                # Displays the selected question
                selected_question_display = question_display(edit_index)

                os.system("cls")
                user_selection = input(f"{dynamic_divider()}\n\t\tEditing Question\n{dynamic_divider()}\n{selected_question_display}\n{dynamic_divider()}\nWhat do you want to edit?\n{dynamic_divider()}\n[ 1 ] Question Content\n[ 2 ] Question Options\n[ 3 ] Question Answer\n[ X ] Back to Menu\n{dynamic_divider()}\n")
                if user_selection.upper() == "X":
                    return
                elif user_selection.isdigit():
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
    string = f"\n{DIVIDER_2}\n"

    # Formats the options
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
            new_question_content = input(f"{dynamic_divider()}\n\t\tEditing Question Content\n{dynamic_divider()}\n{selected_question_display}\n{dynamic_divider()}\n[ X ] Back to Menu\n{dynamic_divider()}\n")
            
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
            confirm_change = input(f"{dynamic_divider()}\n\t\tConfirm Changes?\n{dynamic_divider()}\n{selected_question_display}\nOriginal:\t{value_list[index][0]}\nNew:\t\t\033[1;37;40m{new_question_content}\033[0;37;40m\n{dynamic_divider()}\n[ C ] Confirm \n[ X ] Cancel Changes\n{dynamic_divider()}\n")
            
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
            writes_to_file(_QUESTION_POOL, "edit_question")

    # Used to change the options
    if input_string == "2":
        while local_loop:
            os.system("cls")
            option_number = input(f"{dynamic_divider()}\n\t\tEditing Question Options\n{dynamic_divider()}\n{selected_question_display}\n{dynamic_divider()}\n[ X ] Back to Menu\n{dynamic_divider()}\n")

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
                    new_option_content = input(f"{dynamic_divider()}\n\t\tEditing Question Options\n{dynamic_divider()}\n{selected_question_display}\nSelected Option | {option_number}\n\tOption\t| {value_list[index][1][list_index]}\n\tNew\t|\n{dynamic_divider()}\n[ X ] Back to Menu\n{dynamic_divider()}\n")
                    
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
            confirm_change = input(f"{dynamic_divider()}\n\t\tConfirm Changes?\n{dynamic_divider()}\n{selected_question_display}\nSelected Option | {option_number}\n\tOption\t| {value_list[index][1][list_index]}\n\tNew\t| \033[1;37;40m{new_option_content}\033[0;37;40m\n{dynamic_divider()}\n[ C ] Confirm\n[ X ] Back to Menu\n{dynamic_divider()}\n")
            
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
            writes_to_file(_QUESTION_POOL, "edit_question")

    # Used to change the answer of the question
    if input_string == "3":
        while local_loop:
            os.system("cls")
            new_answer_content = input(f"{dynamic_divider()}\n\t\tEditing Question Answer\n{dynamic_divider()}\n{selected_question_display}\n{dynamic_divider()}\n[ X ] Back to Menu\n{dynamic_divider()}\n")
            
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
            confirm_change = input(f"{dynamic_divider()}\n\t\tConfirm Changes?\n{dynamic_divider()}\n{selected_question_display}\nOriginal:\t{value_list[index][2]}\nNew:\t\t\033[1;37;40m{value_list[index][1][list_index]}\033[0;37;40m\n{dynamic_divider()}\n[ C ] Confirm \n[ X ] Cancel Changes\n{dynamic_divider()}\n")
            
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
            writes_to_file(_QUESTION_POOL, "edit_question")
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
            delete_check = input(f"{dynamic_divider()}\n\t\tPlease confirm your selection\n{dynamic_divider()}\n{value_list[deleting_index][0]}\n{string}\n{value_list[deleting_index][2]}\n{dynamic_divider()}\n[ C ] Confirm\t\t[ X ] Back to Menu\n{dynamic_divider()}\n")
            if delete_check.upper() == "X":
                break
            elif delete_check.upper() == "C":
                writes_to_file(_QUESTION_POOL, "delete", deleting_index) 
                input("\033[0;31;40mOption has been deleted!\033[0;37;40m\nPress Enter to Continue\n") 
                break 
            else:
                error_output("option")
                continue
        return

# [ISSUE] Not fully converted
# Returns the index value for menu navigation
# Checks if the inputted value is within range of the available options
# 
# "title" parameter needs to be a string for the printing
def selection_of_question(title: str):
    value_list = list(dictionary.values())
    while True:
        os.system("cls")
        value_number = input(f"{dynamic_divider()}\n\t\t{title}\n{dynamic_divider()}\n{view_file_content(1, 'question')}{dynamic_divider()}\n[ X ] Back to Menu\n{dynamic_divider()}\n")
        
        # Check if the user wants to exit the menu
        if value_number.upper() == "X":
            return "X"
        elif not value_number.isdigit():
            error_output("input")
        elif  int(value_number) <= 0 or int(value_number) > len(dictionary): 
            error_output("range")
        else:
            return (int(value_number) - 1)

# ===================================================================================================
#   Quiz Settings Functions
# ===================================================================================================
# [NOTE] Quiz Settings values can only be a integer, float and boolean.
# The only exception for this rule is for the assessment componenet, where it is stored as a list.

# Logicial system for quiz setting
def setting_logic():
    # Loads up the JSON file into a dictionary 
    quiz_setting: list = read_file(_QUIZ_SETTING, option="json")
    index_return = select_quiz(quiz_setting)
    # ensures that the variable can only be a bool and is equalled to "False"
    if index_return == False and isinstance(index_return, bool): 
        return False
    else:
        while True:
            # Prints out the edit settings screen of the selected quiz setting
            userInput = print_menu(_QUIZ_SETTING, index_return)  
            valueCap = userInput.upper()
            match valueCap:
                case "X": # Return to selection menu
                    return 
                case "1": # Add Setting
                    add_setting(quiz_setting)
                case "2": # Edit Setting
                    edit_setting(quiz_setting, index_return)
                case "3": # Delete Setting
                    delete_setting(quiz_setting, index_return)
                case _:
                    error_output("option")

# Select the quiz setting you want to edit.
def select_quiz(input_list: list):
    while True:
        content = f"{dynamic_divider()}\n\t\t\033[1;37;40m Setting\033[0;37;40m\n{dynamic_divider()}\n"
        content += "      \t  Course\t   |  Module\t  | Quiz\n"
        content += f"{dynamic_divider()}\n"
        for i, element in enumerate(input_list):
            content += f"[ {i + 1} ] {element['course']} | {element['module_name']} | {element['quiz_name']}\n"
        content += f"{dynamic_divider()}\n\tSelect quiz setting to edit\n{dynamic_divider()}\n[ X ] Back to Main\n{dynamic_divider()}\n"

        os.system("cls")
        check = input(content)
        if check.upper() == "X":
            return False
        elif check.isalpha():
            error_output("input")
            continue
        elif check == "":
            error_output("empty_input")
            continue
        elif int(check) < 0 or int(check) > len(input_list):
            error_output("range")
            continue
        return int(check) - 1


# [NOTE] Any additional setting added would need to be manually added for proper functionality
# Add settings into "quiz_settings.json"
def add_setting(input_list: list): 
    while True:
        # Name check
        while True:
            os.system("cls")
            new_setting_name = input(f"{dynamic_divider()}\n\t\t\tAdding Setting\n{dynamic_divider()}\nSetting Name: \nSetting Value: \n{dynamic_divider()}\n[ X ] Back to Menu\n{dynamic_divider()}\nSetting Name: ")

            if new_setting_name.upper() == "X":
                return
            elif not re.search(PATTERN, new_setting_name):
                error_output("special")
                continue
            break

        # Value check
        while True:
            os.system("cls")
            new_setting_value = input(f"{dynamic_divider()}\n\t\t\tAdding Setting\n{dynamic_divider()}\nSetting Name: {new_setting_name}\nSetting Value: \n{dynamic_divider()}\n[ X ] Back to Menu\n{dynamic_divider()}\nSetting Value: ")

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
            finalCheck = input(f"{dynamic_divider()}\n\t\t\tAdding Setting\n{dynamic_divider()}\nSetting Name: {new_setting_name}\nSetting Value: {new_setting_value}\n{dynamic_divider()}\n[ C ] Confirm\t\t[ X ] Exit\n{dynamic_divider()}\n")
            
            if finalCheck.upper() == "X":
                return
            elif finalCheck.upper() == "C":
                input("\033[0;32;40mYour changes have been saved!\033[0;37;40m\nPress Enter to Continue\n")
            else:
                error_output("option")
                continue
            break

        # If the two checks above are valid, the new value would be added into the settings file.
        with open(_QUIZ_SETTING, "w") as f:
            input_list[new_setting_name] = new_setting_value
            json.dump(input_list, f, indent=4)
        return


# Edits the value of the settings from "quiz_settings.json"
# "input_list" is the data from "quiz_settings.json"
# "input_index" is the quiz setting which you are editing
def edit_setting(input_list: list, input_index: int):
    while True:
        os.system("cls")
        edit_key = selection_of_setting("Editing Settings", input_list, input_index)
        # Execute if "edit_key" is "X"
        if edit_key.upper() == "X":
            return  
        local_loop = True
        checking = check_type(input_list[input_index][edit_key])
        while local_loop:
            os.system("cls")
            new_value = input(f"{dynamic_divider()}\nName: {edit_key}\nValue: \033[1;37;40m>>> {input_list[input_index][edit_key]} <<<\033[0;37;40m\n{dynamic_divider()}\n[ X ] Back to Menu\n{dynamic_divider()}\nPlease input new value: ")
            if new_value.upper() == "X":
                local_loop = False   
            elif not re.search(PATTERN, new_value):
                error_output("special")
                continue
            break

        while local_loop:
            os.system("cls")
            confirm_change = input(f"{dynamic_divider()}\n\t\tConfirm Changes?\n{dynamic_divider()}\nName: {edit_key}\nValue: \033[1;37;40m>>> {new_value} <<<\033[0;37;40m\n{dynamic_divider()}\n[ C ] Confirm \n[ X ] Cancel Changes\n{dynamic_divider()}\n")
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
            input_list[input_index][edit_key] = new_value
            writes_to_file(_QUIZ_SETTING, "json", input_list) 


# Deletes settings from "quiz_settings.json"
# "input_dict" is a dictonary from "quiz_settings.json"
def delete_setting(input_list: list, input_index: int): 
    while True:
        os.system("cls")
        deleting_key = selection_of_setting("Deleting Setting", input_list, input_index) # will return a dictionary key
        if deleting_key == "X":
            return

        while True:
            os.system("cls")
            delete_check = input(f"{dynamic_divider()}\n\t\tPlease confirm your selection\n{dynamic_divider()}\n[ - ] {deleting_key}: {input_list[deleting_key]}\n{dynamic_divider()}\n[ C ] Confirm\t\t[ X ] Back to Menu\n{dynamic_divider()}\n")
            # Check if the user wants to exit the menu
            if delete_check.upper() == "X":
                break
            elif delete_check.upper() == "C":
                writes_to_file(_QUIZ_SETTING, "delete_setting", deleting_key)

                input("\033[0;31;40mOption has been deleted!\033[0;37;40m\nPress Enter to Continue\n")  
                break
            else:
                error_output("option")
                continue
        return


# Returns the key name of the selected item
# Used to check if the inputted value is within range of the available options
# 
# "title" parameter needs to be a string for the printing
# "input_dict" parameter is used to know what is the updated dictionary
def selection_of_setting(title: str, input_list: list, input_index: int): 
    dict_list = list(input_list[input_index].keys())

    while True:
        os.system("cls")
        value_number = input(f"{dynamic_divider()}\n\t\t{title}\n{dynamic_divider()}\n{view_file_content(1, 'setting', _QUIZ_SETTING, input_index)}{dynamic_divider()}\n[ X ] Back to Menu\n{dynamic_divider()}\n")
        # Check if the user wants to exit the menu
        if value_number.upper() == "X": 
            return "X"
        elif not value_number.isdigit():
            error_output("input")
        elif int(value_number) <= 0 or int(value_number) > len(dict_list):
            error_output("range")
        else:
            return dict_list[int(value_number) - 1]

# Used for checking the type of an object
def check_type(input: any):
    check = type(input)
    if check is str: return str
    elif check is int: return int
    elif check is bool: return bool
    elif check is list: return list
    

# ========================================================================
#   Generate Report Functions
# ========================================================================

# Logical system for generating report
def generate_report_logic():
    data = generate_report()
    report_input = input(f"{dynamic_divider()}\n\t\tReport\n{dynamic_divider()}\n{data}\n{dynamic_divider()}\n[ X ] Back to Menu\n{dynamic_divider()}\n")
    if report_input.upper() == "X":
        return False
    elif report_input == "":
        error_output("empty_input")
    else: 
        error_output("input")
    return

# Retrieving and generating a data report
def generate_report():
    # Reads data from csv file
    quiz_result_list = read_file(_QUIZ_RESULTS, option="csv")

    # Initalize variables for calculation
    string = ""
    total_marks = 0
    marks = []
    students = []
    question_correct = 0
    question_wrong = 0
    total_questions = 0

    # Retrieves the data from the list
    for attempt in quiz_result_list:
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
    total_attempts = len(quiz_result_list)
    no_of_students = len(students)
    percent_question_correct = question_correct / total_questions * 100
    percent_question_wrong = question_wrong / total_questions * 100
    average_marks = total_marks / total_attempts
    min_marks = min(marks)
    max_marks = max(marks)

    # Adds data into the string
    string += f"Total Number of Attempts:  \033[1;37;40m{total_attempts}\033[0;37;40m\n"
    string += f"Number of Students attempted:  \033[1;37;40m{no_of_students}\033[0;37;40m\n"
    string += f"Average Marks:  \033[1;37;40m{average_marks:.2f}\033[0;37;40m\n"
    string += f"Percentage of Question Correct:  \033[1;37;40m{percent_question_correct:.2f}%\033[0;37;40m\n"
    string += f"Percentage of Question Wrong:  \033[1;37;40m{percent_question_wrong:.2f}%\033[0;37;40m\n"
    string += f"Min marks: \033[1;37;40m{min_marks}\033[0;37;40m\n"
    string += f"Max marks: \033[1;37;40m{max_marks}\033[0;37;40m\n"

    return string

# Plot the data into a graph/diagram
def plot_data():
    return

# ========================================================================
#   Sub Program Loops
# ========================================================================
def register_user_subloop(input_loop: bool):
    while input_loop:
        os.system("cls")
        check = register_logic()
        if check == False:
            input_loop = False

def course_info_subloop(input_loop: bool):
    while input_loop:
        os.system("cls")
        check = course_logic()
        if check == False:
            input_loop = False

# Not sure if this will be used
def question_pool_subloop(input_loop: bool):
    while input_loop:
        os.system("cls")
        check = question_logic()
        if check == False:
            input_loop = False

def quiz_setting_subloop(input_loop: bool):
    while input_loop:
        os.system("cls")
        check = setting_logic()
        if check == False:
            input_loop = False

def generate_report_subloop(input_loop: bool):
    while input_loop:
        os.system("cls")
        check = generate_report_logic()
        if check == False:
            input_loop = False

# ========================================================================
#   Login Page Functions
# ========================================================================

# Prompts a Admin login upon loading of the program
def login_menu():
    # plaintext is "1qwer$#@!" w/o quotations. [For Reference purposes]
    password_hashed = "9153cae78e7f43377a079644f24ff39ebb82ce481e08f09732d1009bd01ad159" 

    loop = True
    while loop:
        os.system("cls")
        userInput = getpass.getpass(f"{dynamic_divider()}\n\t\t\033[1;37;40mAdmin Login Page\033[0;37;40m\n{dynamic_divider()}\n[ X ] Exit Program\n{dynamic_divider()}>>>")
        if userInput.upper() == "X":
            while True:
                os.system("cls")
                userConfirm = input(f"{dynamic_divider()}\n\033[1;37;40m\t\tAre you sure want to quit?\033[0;37;40m\n{dynamic_divider()}\n[ Y ] Yes\t\t[ N ] No\n{dynamic_divider()}\n")
                if userConfirm.upper() == "Y":
                    print("\033[0;32;40mGoodbye\033[0;37;40m")
                    loop = False
                    return
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
        os.system("cls")
        string = print_main(MAIN_MENU)
        check_variable = main_logic(string)
        if check_variable == False:  # execute if value is False
            main_loop = False

# ========================================================================
#   Main Program Loop
# ========================================================================

def main():
    main_menu(main_loop=True)
    # login_menu()

if __name__ == "__main__":
    main()
