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
# Input file:   C:\PSEC_project\question_pool.txt
#               C:\PSEC_project\quiz_settings.txt
#               C:\PSEC_project\userid_pswd.csv
#               C:\PSEC_project\quiz_results.csv
# 
# Output file:  C:\PSEC_project\userid_pswd.csv
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
# Module /      os, re, hashlib, csv, time
#
# Known issues:	eg. no validation of input value
#
import os, hashlib, random, csv
import time

# ==============================================================================================================================
#   Initialize variables
# ==============================================================================================================================

dictionary = {}
csv_dict_list = []

EMPTY = ""
DIVIDER = f"{EMPTY:=^60}"

MAIN_USER_MENU = ["Log In", "Reset Password"]
START_MENU = ["Begin Quiz"]

_USERNAME_AND_PASSWORD = "./admin/userid_pswd.csv"
_QUIZ_SETTING_TEXT = "./admin/quiz_settings.txt"
_QUIZ_QUESTION_TEXT = "./admin/question_pool.txt"
_QUIZ_RESULTS = "./admin/quiz_results.csv"

MAIN_LOOP = True
SUB_LOOP = True

# ==============================================================================================================================
#   General Functions
# ==============================================================================================================================

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

# Returns the file content using "dictionary"
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


# Writes into a csv file with the given inputs.
def write_csv(file: str, dict_input: dict):
    # Fieldnames are the key values of the first item in the dictionary.
    fields = dict_input[0].keys()

    # Writes to the csv file with the correct headings and value
    with open(file, "w", newline="") as csvfile:
        csvwriter = csv.DictWriter(csvfile, fieldnames=fields)
        csvwriter.writeheader()
        csvwriter.writerows(dict_input)


# Returns content
def print_file(name: str):
    option_name = ""
    content = f"{DIVIDER}\n\t\t\t\033[1;37;40m {name}\033[0;37;40m\n{DIVIDER}\n"

    if name == "Log In":
        option_name = "login"
        content += f"Question\n{DIVIDER}\n[ P ] Previous Question\t[ N ] Next Question\n[ X ] Back to Menu\n{DIVIDER}\n"

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
    string = ""
    if error_message == "option":               # Wrong option selected
        string += "\033[1;37;41mPlease select a valid option.\033[0;37;40m"

    elif error_message == "empty_input":        # Empty input
        string += f"\033[1;37;41mEmpty input, please try again\033[0;37;40m"

    elif error_message == "input":              # Invalid input
        string += f"\033[1;37;41mPlease enter a valid input.\033[0;37;40m"

    elif error_message == "range":              # Input value not within range
        string += "\033[1;37;41mPlease enter a value within the range.\033[0;37;40m"

    # 
    elif error_message == "username":           # User not found in database    [Unique to user.py]
        string += f"\033[1;37;41mUsername could not be found.\033[0;37;40m"

    elif error_message == "password":           # Password input was incorrect  [Unique to user.py]
        string += f"\033[1;37;41mPassword is incorrect.\033[0;37;40m"

    elif error_message == "admin":              # Account locked when user enters wrong password 3 times [ISSUE] Doesn't lock account
        string += f"\033[1;37;41mAccount has been locked\033[0;37;40m"

    elif error_message == "previous":           # No more questions in front of selected question
        string += f"\033[1;37;41mYou are at the first question!!\033[0;37;40m"
    
    elif error_message == "next":               # No more questions after selected question
        string += f"\033[1;37;41mYou are at the last question!!\033[0;37;40m"
    
    elif error_message == "no_attempts":        # No more attempts remaining  
        string += f"\033[1;37;41mYou have no remaining attempt\033[0;37;40m"
    
    elif error_message == "bad_input":          # Bad Input --> Refers to EOFERROR (Occurs only when CTRL+Z is inputted)
        string += f"\033[1;37;41mBad Input, program restarted\033[0;37;40m"
    
    input(string)

    
# ===========================================================================================================================
#   User Page Function
# ===========================================================================================================================

# User navigation menu
def user_menu(inputList: list):
    content = f"{DIVIDER}\n\t\t\t\033[1;37;40m Main \033[0;37;40m\n{DIVIDER}\n"
    for i, element in enumerate(inputList):
        content += f"[ {i+1} ] {element}\n"
    content += f"[ X ] Exit Application\n{DIVIDER}\n"
    return content

# Logicial Flow for user menu
def user_logic(userpage_list, content: str):
    while True:
        os.system("cls")
        global MAIN_LOOP, SUB_LOOP
        SUB_LOOP = True
        stored_value = input(content)
        if check_if_digit(stored_value):
            if int(stored_value) in range(1, len(userpage_list) + 1):
                if stored_value == "1":
                    login_subloop()
                elif stored_value == "2":
                    reset_password()
            else:
                error_output("range")
        elif stored_value.upper() == "X":
            while True:
                os.system("cls")
                userConfirm = input(f"{DIVIDER}\n\033[1;37;40m\t\tAre you sure want to quit?\033[0;37;40m\n{DIVIDER}\n[ Y ] Yes\t\t[ N ] No\n{DIVIDER}\n")
                if userConfirm.upper() == "Y":
                    print("\033[0;32;40mGoodbye\033[0;37;40m")
                    MAIN_LOOP = False
                    break
                elif userConfirm.upper() == "N":
                    break
                else:
                    error_output("option")
            return
        elif stored_value == "":
            error_output("empty_input")
        else:
            error_output("option")


# =========================================================================================================================
#   Login Functions
# =========================================================================================================================

# Log In Logicial Flow
def login_menu():
    while True:
        os.system("cls")
        user_username_input = input(f"{DIVIDER}\n\t\t\tLog In\n{DIVIDER}\nUsername: \nPassword: \n{DIVIDER}\n[ X ] Back to Menu\n{DIVIDER}\nEnter your username: ")
        if user_username_input.upper() == "X":
            global SUB_LOOP
            SUB_LOOP = False
            return
        elif user_username_input == "":
            error_output("empty_input")
        # Checks if the username input is inside the database
        elif check_username(user_username_input):
            # Counter for number of attempts before a user's account is locked 
            count = 3
            while count != 0:
                os.system("cls")
                password_input = input(f"{DIVIDER}\n\t\t\tLog In\n{DIVIDER}\nUsername: {user_username_input} \nPassword: \n{DIVIDER}\n[ X ] Back to Menu\n{DIVIDER}\nEnter your password: ")
                if password_input.upper() == "X":
                    SUB_LOOP = False
                    return
                elif check_password(user_username_input, password_input):
                    quiz_menu(user_username_input) # Starting of the quiz
                    return
                else:
                    count -= 1
                    error_output("password")
                    continue
            if count == 0:
                os.system("cls")
                # [ISSUE] Need a way to lock the user's account
                error_output("admin")
                break
        else:
            error_output("username")
            continue

# Check if username exist in the file
def check_username(username: str):
    read_file_content(_USERNAME_AND_PASSWORD, option="csv")
    for i in csv_dict_list:
        if username == i["user"]:
            return True
    return False

# Hashes the password for safe keeping in the .csv file
def user_password_hashing(given_input: str): 
    output = hashlib.sha256(given_input.encode())
    return output.hexdigest()

# Checks if the hashed matches the password
def check_password(username: str, password: str):
    read_file_content(_USERNAME_AND_PASSWORD, option="csv")
    for i in csv_dict_list:
        if username == i["user"]:
            if user_password_hashing(password) == i["password"]:
                return True
            else:
                return False

#  NOT IMPLEMENTED [ISSUE]
def reset_password():
    read_file_content(_USERNAME_AND_PASSWORD, option="csv")
    input("Reset Password")
    return

# ========================================================================================================================
#   Question Function
# ========================================================================================================================

# Display the quiz menu for the user.
# "username" is a string to identify the user
def quiz_menu(username: str):
    while True:
        os.system("cls")
        user_input = input(f"{DIVIDER}\n\t\t\tQuiz Menu\n{DIVIDER}\nUser Logged In as: \033[1;37;40m{username}\033[0;37;40m\n\nNumber of Attempts Left: {remaining_attempt(username)}\nTime for the quiz: {check_amount_of_time()} mins\nNumber of Question: {check_number_of_question()}\n{DIVIDER}\n[ 1 ] Start Quiz\n[ X ] Back to Menu\n{DIVIDER}\n")
        if user_input.upper() == "X":
            return
        elif user_input == "1":
            if remaining_attempt(username) == 0:
                error_output("no_attempts")
                continue
            start_quiz(username) # Starts the quiz once the user confirms
        else:
            error_output("option")


# Gets the remaining amount of attempt the current user can do.
def remaining_attempt(username: str):
    no_of_attempt_allowed =  check_number_of_attempts() 
    count = 0
    read_file_content(_QUIZ_RESULTS, option="csv")
    for i in csv_dict_list:
        if i["User"] == username:
            count += 1
    if no_of_attempt_allowed - count < 0:
        return 0
    return no_of_attempt_allowed - count


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
        user_selection = input(f"{DIVIDER}\n\t\t\tQuiz\n{DIVIDER}\nTime left: {timer(starttime)[0]} min {timer(starttime)[1]} sec\n{DIVIDER}\n{selected_question}Your Answer: {temp_list[selected_question_index][4]}\n{DIVIDER}\n[ P ] Previous Question\t\t[ N ] Next Question\n[ S ] Save & Submit\n{DIVIDER}\n")
        
        # If time is up, save and submit the users answer
        # OR
        # If user inputs "S", save and submit the answer
        if user_selection.upper() == "S" or (timer(starttime)[0] <= 0 and timer(starttime)[1] <= 0):
            value = save_user_answer(temp_list)
            push_result(username, value)
            show_result(value)
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
def save_user_answer(input_list: list):
    # elements in "question_data" list
    # index 0: question identification value
    # index 1: question content
    # index 2: question options
    # index 3: question answer
    # index 4: user's answer
    questions_tested = []
    answered_correct = 0
    answered_wrong = 0
    total_questions = 0
    for question_data in input_list:
        try:
            total_questions += 1
            index = ord(question_data[4]) - 97

        # TypeError occurs when user didn't answer the question
        except TypeError: 
            question_data[4] = "Didn't Answer"
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
# input_list[1]: total_marks
def push_result(username: str, input_list: list):
    read_file_content(_QUIZ_QUESTION_TEXT, option="question")
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
    read_file_content(_QUIZ_RESULTS, option="csv")

    # Pushes all the elements into a dictionary for printing
    new_dict = format_into_dict(username, input_list)
    csv_dict_list.append(new_dict)
    write_csv(_QUIZ_RESULTS, csv_dict_list)

# Formats the data into a dictionary for csv printing
def format_into_dict(username: str, input_list: list):
    # input_list[0]: question_list
    # input_list[1]: total_mark
    result = {
        "User": username,
        "No. Qn answered correct": input_list[1],
        "No. Qn answered wrong": input_list[2],
        "Total Marks": input_list[3] * 2,
        "Date of Attempt": time.ctime()
    }
    for i, element in enumerate(input_list[0]):
        result[f"Question {i + 1}"] = element[1]
        result[f"Answer {i + 1}"] = element[2] 
        result[f"User Answer {i + 1}"] = element[3]
    
    return result

# Returns a string to display the user's result
def show_result(input_list: list):
    string = ""
    
    # Get the amount of marks awarded for the quiz
    user_marks = input_list[1] * 2

    # Get the total possible marks
    total = input_list[3] * 2
    percentage = user_marks/total * 100
    if percentage >= 80:
        string += "well done"
    elif percentage > 40:
        string += "good work, you could be better. fix yourself"
    else:
        string += "poor, try harder next time"
    input(string)
    return

# Returns the remaining time left in a tuple
def timer(starting_time: float):
    endtime = time.time() - starting_time
    total_allowed_time = float(check_amount_of_time()) * 60
    time_left_min = int((total_allowed_time - endtime)/60)
    time_left_sec = int((((total_allowed_time - endtime)/60) - time_left_min) * 60)
    return time_left_min, time_left_sec


# Returns the amount of time set within the settings
def check_amount_of_time():
    read_file_content(_QUIZ_SETTING_TEXT, option="settings")
    value_list = list(dictionary.values())
    for i in value_list:
        if i[0] == "1": # ID of "time"
            return i[2]

# Number of question to be used in the quiz
def check_number_of_question():
    read_file_content(_QUIZ_SETTING_TEXT, option="settings")
    value_list = list(dictionary.values())
    for i in value_list:
        if i[0] == "2": # ID of "no_of_question"
            return i[2]

# Checks the number of attempts set for the quiz
def check_number_of_attempts():
    read_file_content(_QUIZ_SETTING_TEXT, option="settings")
    value_list = list(dictionary.values())
    for i in value_list:
        if i[0] == "3": # ID of "no_of_attempt"
            return int(i[2])

# Checks if the admin set the answers to appear randomly
def check_randomize_option():
    read_file_content(_QUIZ_SETTING_TEXT, option="settings")
    value_list = list(dictionary.values())
    for i in value_list:
        if i[0] == "4": # ID of "randomize_answer"
            if i[2].lower() == "true":
                return True
            return False

# Randomly selects question from the question pool
# Returns a nested list
# 
# ask_question_list[0]: index of where the question appears in the dictionary
# ask_question_list[1]: question content
# ask_question_list[2]: options for the question
# ask_question_list[3]: correct answer to the question
def selection_random_question():
    read_file_content(_QUIZ_QUESTION_TEXT, option="question")
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
def login_subloop():
    while SUB_LOOP:
        read_file_content(_USERNAME_AND_PASSWORD, option="login")
        login_menu()
    
# ==============================================================================================================================
#   Main Program Loop
# ==============================================================================================================================
# Try loop is used in order to catch any bad inputs the user might have done within the stack
while MAIN_LOOP:
    try:
        while MAIN_LOOP:
            string = user_menu(MAIN_USER_MENU)
            user_logic(MAIN_USER_MENU, string)
    except:
        error_output("bad_input")