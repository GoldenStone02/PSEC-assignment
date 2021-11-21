import os
import re


# ==================================================================
#   Initialize Variables
# ==================================================================
dictionary = {}

EMPTY = ""
DIVIDER = f"{EMPTY:=^60}"

PATTERN = r"^[\w]+$"
PASSWORD_PATTERN = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\\d)(?=.*[!@#$%]).+$"

_QUIZ_SETTING_TEXT = "./admin/quiz_settings.txt"
_QUIZ_QUESTION_TEXT = "./admin/question_pool.txt"
MAIN_MENU = ["Register User", "Question Pool", "Quiz Settings", "Generate Report"]
LOOP = True

# ==================================================================
#   General Functions
# ==================================================================

# Reads and empties value into "dictionary" variable
# "option" parameter used to define what format it should print in
def read_file_content(file: str, option):
    try:
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

                current_line_list = stripped_lines.split(": ")
                dictionary[f"option {i + 1}"] = [current_line_list[0],current_line_list[1]]
        # Format used for question pool dictionary
        elif option == "question":
            for i, line in enumerate(file_content):
                stripped_lines = line.strip()
                if stripped_lines == "":
                    continue
                
                current_line_list = stripped_lines.split("||")

                # Pushes each line into a dictionary
                dictionary[f"question {i+1}"] = [
                    current_line_list[0],   # Question Content
                    current_line_list[1:5], # Question Options
                    current_line_list[5]    # Question Answer
                ]

    except FileNotFoundError:
        print("File Doesn't Exist")

def write_file(file: str):
    value_list = list(dictionary.values())

    with open(file, "w") as f:
        for line in value_list:
            f.write(f"{line[0]}: {line[1]}\n")

# Removes linefeed that is in between lines in the file
def remove_linefeed(file: str):
    temp = []
    with open(file, "r") as f:
        file_lines = f.readlines()
    
    # Remove linefeed
    # Ensures that if there is a linefeed in between variables
    # It will get removed, preventing any fatal errors in the system
    for line in file_lines:
        if line == "\n":
            continue
        temp.append(line.strip())
    
    # Rewrites file
    with open(file, "w") as f:
        for line in temp:
            f.write(line + "\n")

# returns the file content using "dictionary"
# 
# "show_number" parameter is used to define the format of returning string.
# 
# "0" prints out file content without numbering
# "1" prints out with sequence numbering
def view_file_content(show_numbers: int, option: str):
    content = ""

    value_list = list(dictionary.values())

    if show_numbers == 1:
        #   How the dictionary would look like:
        # {
        #     "option 1": ["time", "60"],
        #     "option 2": ["no_of_question", "5"],
        #     "option 3": ["no_of_attempt", "2"],
        # } 
        if option == "settings":
            for i, item in enumerate(value_list): 
                content += f"[ {i + 1} ] {value_list[i][0]}: {value_list[i][1]}\n"
        elif option == "question":
            for i, item in enumerate(value_list): 
                sample = ""
                for j, option in enumerate(value_list[i][1]):
                    sample += f"\n{chr(97 + j)}) {option}"
                content += f"[ {i + 1} ] {value_list[i][0]}: {sample}\n"

    elif show_numbers == 0:
        if option == "settings":
            for item in value_list:
                content += f"[ - ] {item[0]}: {item[1]}\n"
        elif option == "question":
            for item in value_list:
                sample = ""
                for j, option in enumerate(item[1]):
                    sample += f"\n{chr(97 + j)}) {option}"
                content += f"{item[0]}: {sample}\n\n"
    
    return content

# Prints the text file with some UI.
# Needs to happen after "ReadFileContent()" has been executed
def print_file(name: str): 

    option_name = ""

    if name == "Question Pool":
        option_name = "question"
    elif name == "Quiz Settings":
        option_name = "settings"

    content = f"{DIVIDER}\n\t\t\t\033[1;37;40m {name}\033[0;37;40m\n{DIVIDER}\n"

    content += view_file_content(0, option_name)

    content += f"{DIVIDER}\n\t\tSelect one of the options\n{DIVIDER}\n"
    content += f"[ 1 ] Add New {name}\n[ 2 ] Edit {name}\n[ 3 ] Delete {name}\n[ X ] Back to Main\n{DIVIDER}\n"

    return content

# Checks whether the input is an integer or string
# If the input is a digit, return True
# if the input is a string, return False
def check_if_digit(input):
    try:
        int(input)
        return True
    except ValueError:
        return False

# ============================================================================================
#   Main Page Functions
# ============================================================================================

# prints page with a list, checks whether is input is in range of list
# "inputList" parameter is for dynamic changing of the menu
def print_main(inputList: list):
    content = f"{DIVIDER}\n\t\t\t\033[1;37;40m Main \033[0;37;40m\n{DIVIDER}\n"
    for i, element in enumerate(inputList):
        content += f"[ {i+1} ] {element}\n"
    content += f"[ X ] Exit Application\n{DIVIDER}\n"
    return content

# main logical system for selection page
# "menuList" is meant for easily change within the UI.
def main_logic(menuList: list, content: str):
    while True:
        global LOOP
        LOOP = True
        stored_value = input(content)
        if check_if_digit(stored_value):
            if int(stored_value) in range(1, len(menuList) + 1):
                if stored_value == "1":
                    register_user()
                elif stored_value == "2":
                    question_pool()
                elif stored_value == "3":
                    quiz_setting()
                elif stored_value == "4":
                    generate_report()
            else:
                input("\033[1;37;41mPlease select a valid option.\033[0;37;40m")
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
                    print("\033[1;37;41mPlease select a valid option.\033[0;37;40m")
                os.system("cls")
            return
        else:
            input("\033[1;37;41mPlease select a valid option.\033[0;37;40m") 

# ========================================================================
#   Register User Functions
# ========================================================================

def register_logic():
    return

def add_user():
    return

# ===================================================================================================
#   Question Pool Functions
# ===================================================================================================

# Logicial system for question pool
def question_logic(userInput: str):
    valueCap = str(userInput).upper()
    if valueCap == "X":
        global LOOP
        LOOP = False
    elif valueCap == "1":
        add_question()
    elif valueCap == "2":
        edit_question()
    elif valueCap == "3":
        delete_question()
    else:
        input("\033[1;37;41mPlease select a valid option.\033[0;37;40m")

def add_question():
    while True:
        options_output = ""
        while options_output == "":
            os.system("cls")
            no_of_options = input("How many options do you want? ")
            if no_of_options.isdigit():
                if int(no_of_options) < 0 or int(no_of_options) > 5:
                    input("\033[1;37;41mPlease enter a value within the range.\033[0;37;40m")
                else:
                    for i in range(int(no_of_options)):
                        options_output += f"{chr(97 + i)})\n"
            else:
                input("\033[1;37;41mPlease select a valid option.\033[0;37;40m")

        input(f"{DIVIDER}\n\t\t\tAdding Question\n{DIVIDER}\nQuestion: \n\nOptions: \n{options_output}{DIVIDER}\n[ X ] Back to Menu\n{DIVIDER}\nInput Question: ")
        break
    return

def edit_question():
    return

def delete_question():
    return

# ===================================================================================================
#   Quiz Settings Functions
# ===================================================================================================

# Logicial system for quiz setting
def setting_logic(userInput: str):
    valueCap = str(userInput).upper()
    # Logical Circuit
    if valueCap == "X": # Close App
        global LOOP
        os.system("cls")
        LOOP = False
    elif valueCap == "1": # Add Setting
        add_setting()
    elif valueCap == "2": # Edit Setting
        edit_setting()
    elif valueCap == "3": # Delete Setting
        delete_setting()
    else:
        input("\033[1;37;41mPlease select a valid option.\033[0;37;40m")


def add_setting(): 
    while True:
        local_loop = True
        # Name check
        while local_loop:
            os.system("cls")
            new_setting_name = input(f"{DIVIDER}\n\t\t\tAdding Setting\n{DIVIDER}\nSetting Name: \nSetting Value: \n{DIVIDER}\n[ X ] Back to Menu\n{DIVIDER}\nSetting Name: ")

            if new_setting_name.upper() == "X":
                local_loop = False
                break
            if not re.search(PATTERN, new_setting_name):
                input(f"\n\033[1;37;41mInput value can't contain special characters!\033[0;37;40m\n")
                continue
            elif new_setting_name[0].isdigit():
                input(f"\n\033[1;37;41mPlease start with a letter!\033[0;37;40m\n")
                continue
            break

        # Value check
        while local_loop:
            os.system("cls")
            new_setting_value = input(f"{DIVIDER}\n\t\t\tAdding Setting\n{DIVIDER}\nSetting Name: {new_setting_name}\nSetting Value: \n{DIVIDER}\n[ X ] Back to Menu\n{DIVIDER}\nSetting Value: ")

            if new_setting_value.upper() == "X":
                local_loop = False
                break
            if new_setting_value == "":
                input(f"\n\033[1;37;41mPlease enter a valid into the input\033[0;37;40m\n")
                continue            
            elif not re.search(PATTERN, new_setting_value):
                input(f"\n\033[1;37;41mInput value can't contain special characters!\033[0;37;40m\n")
                continue
            break

        # Check if the user wants to confirm the setting
        while local_loop:
            os.system("cls")
            finalCheck = input(f"{DIVIDER}\n\t\t\tAdding Setting\n{DIVIDER}\nSetting Name: {new_setting_name}\nSetting Value: {new_setting_value}\n{DIVIDER}\n[ C ] Confirm?\t\t[ X ] Exit\n{DIVIDER}\n")
            
            if finalCheck.upper() == "X":
                local_loop = False
                break
            elif finalCheck.upper() == "C":
                input("\033[0;32;40mYour changes have been saved!\033[0;37;40m\nPress Enter to Continue\n")
            else:
                input("\n\033[1;37;41mPlease input one of the options\033[0;37;40m\n")
            break

        # Checks if the program aborted at any point 
        if local_loop:
            with open(_QUIZ_SETTING_TEXT, "a") as f:
                f.write(f"{new_setting_name}: {new_setting_value}")
        else:
            break

# Issue: Need to implement to writing to file
def edit_setting():
    value_list = list(dictionary.values())

    while True:
        os.system("cls")
        edit_index = select_setting("Settings")

        if not check_if_digit(edit_index): # execute if its not an integer
            if edit_index.upper() == "X":
                break        
        elif check_if_digit(edit_index): # execute if its an integer
            while True:
                os.system("cls")
                selector = input(f"{DIVIDER}\nWhat do you want to change?\n{DIVIDER}\nName: {value_list[edit_index][0]}\nValue: {value_list[edit_index][1]}\n{DIVIDER}\n[ 1 ] Setting Name\n[ 2 ] Setting Value\n{DIVIDER}\n[ X ] Back to Menu\n{DIVIDER}\n")
                if check_if_digit(selector):
                    loop2 = True
                    # Used to change setting name
                    if selector == "1":
                        while loop2:
                            os.system("cls")
                            new_name = input(f"{DIVIDER}\nName: \033[1;37;40m>>> {value_list[edit_index][0]} <<<\033[0;37;40m\nValue: {value_list[edit_index][1]}\n{DIVIDER}\n[ X ] Back to Menu\n{DIVIDER}\nPlease input a new name: ")
                            if new_name.upper() == "X":
                                loop2 = False
                                break
                            if new_name == "":
                                input(f"\n\033[1;37;41mPlease enter a valid into the input\033[0;37;40m\n")
                                continue 
                            elif not re.search(PATTERN, new_name):
                                input(f"\n\033[1;37;41mInput value can't contain special characters!\033[0;37;40m\n")
                                continue
                            elif new_name[0].isdigit():
                                input(f"\n\033[1;37;41mPlease start with a letter!\033[0;37;40m")
                                continue    
                            break
                        while loop2:
                            os.system("cls")
                            confirm_change = input(f"{DIVIDER}\n\t\tConfirm Changes?\n{DIVIDER}\nName: \033[1;37;40m>>> {new_name} <<<\033[0;37;40m\nValue: {value_list[edit_index][1]}\n{DIVIDER}\n[ C ] Confirm \n[ X ] Cancel Changes\n{DIVIDER}\n")
                            if confirm_change.upper() == "X":
                                loop2 = False
                                break
                            if confirm_change == "":
                                input(f"\n\033[1;37;41mPlease enter a valid into the input\033[0;37;40m\n")
                                continue            
                            elif not re.search(PATTERN, confirm_change):
                                input(f"\n\033[1;37;41mInput value can't contain special characters!\033[0;37;40m\n")
                                continue 
                            elif confirm_change.upper() == "C":
                                input("\033[0;32;40mYour changes have been saved!\033[0;37;40m\nPress Enter to Continue\n")                              
                            break
                        if loop2:
                            # Change the name of item
                            value_list[edit_index][0] = new_name
                            write_file(_QUIZ_SETTING_TEXT)   

                    # Used to change the setting value             
                    elif selector == "2":
                        while loop2:
                            os.system("cls")
                            new_value = input(f"{DIVIDER}\nName: {value_list[edit_index][0]}\nValue: \033[1;37;40m>>> {value_list[edit_index][1]} <<<\033[0;37;40m\n{DIVIDER}\n[ X ] Back to Menu\n{DIVIDER}\nPlease input new value: ")
                            if new_value.upper() == "X":
                                loop2 = False
                                break
                            if not re.search(PATTERN, new_value):
                                input(f"\n\033[1;37;41mInput value can't contain special characters!\033[0;37;40m\n")
                                continue
                            break
                        while loop2:
                            os.system("cls")
                            confirm_change = input(f"{DIVIDER}\n\t\tConfirm Changes?\n{DIVIDER}\nSetting Name: {value_list[edit_index][0]}\nSetting Value: \033[1;37;40m>>> {new_value} <<<\033[0;37;40m\n{DIVIDER}\n[ C ] Confirm \n[ X ] Cancel Changes\n{DIVIDER}\n")
                            if confirm_change.upper() == "X":
                                break
                            if confirm_change == "":
                                input(f"\n\033[1;37;41mPlease enter a valid into the input\033[0;37;40m\n")
                                continue            
                            elif not re.search(PATTERN, confirm_change):
                                input(f"\n\033[1;37;41mInput value can't contain special characters!\033[0;37;40m\n")
                                continue     
                            elif confirm_change.upper() == "C":
                                input("\033[0;32;40mYour changes have been saved!\033[0;37;40m\nPress Enter to Continue\n")                       
                            break    
                        if loop2:
                            # Changes the value of the item
                            value_list[edit_index][1] = new_value
                            write_file(_QUIZ_SETTING_TEXT)                       
                    else:
                        input(f"{DIVIDER}\n\033[1;37;41mPlease enter a value within the range.\033[0;37;40m")
                else:
                    if selector.upper() == "X":
                        break         
        else:
            input("\n\033[1;37;41mPlease input one of the options\033[0;37;40m\n")


# Issue: Just deletes everything in the file [Solved]
def delete_setting(): 
    value_list = list(dictionary.values())
    while True:
        os.system("cls")

        deleting_index = select_setting("Delete Setting")

        if deleting_index == "X":
            return

        while True:
            os.system("cls")
            finalCheck = input(f"{DIVIDER}\n\t\tPlease confirm your selection\n{DIVIDER}\n[ - ] {value_list[deleting_index][0]}: {value_list[deleting_index][1]}\n{DIVIDER}\n[ C ] Confirm\t\t[ X ] Back to Menu\n{DIVIDER}\n")
            
            if finalCheck.upper() == "X":
                break
            elif finalCheck.upper() == "C":
                with open(_QUIZ_SETTING_TEXT, "r") as f:
                    lines = f.read().splitlines()
                
                with open(_QUIZ_SETTING_TEXT, "w") as f:
                    for number, line in enumerate(lines):
                        if number != deleting_index:
                            f.write(line + '\n')   
                input("\033[0;31;40mOption has been deleted!\033[0;37;40m\nPress Enter to Continue\n")  
                break     
            else:
                input(f"{DIVIDER}\n\033[1;37;41mPlease select an option.\033[0;37;40m") 
        break

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
                print(f"{DIVIDER}\n\033[1;37;41mPlease select an option.\033[0;37;40m")
        else:
            if int(value_number) > len(dictionary) or int(value_number) <= 0:
                print(f"{DIVIDER}\n\033[1;37;41mPlease enter a value within the range.\033[0;37;40m")
            else:
                return (value - 1)

# ========================================================================
#   Generate Report Functions
# ========================================================================

# ========================================================================
#   Sub Program Loops
# ========================================================================
def register_user():
    input("Register User")

def question_pool():
    while LOOP:
        read_file_content(_QUIZ_QUESTION_TEXT, option="question")
        questPool = print_file("Question Pool")
        adminInput = input(questPool)
        question_logic(adminInput)

def quiz_setting():
    while LOOP:
        os.system("cls")
        read_file_content(_QUIZ_SETTING_TEXT, option="settings")
        quizSettings = print_file("Quiz Settings")    
        adminInput = input(quizSettings)
        setting_logic(adminInput)

def generate_report():
    input("Generate Report")
# ========================================================================
#   Main Program Loop
# ========================================================================

while LOOP:
    string = print_main(MAIN_MENU)
    main_logic(MAIN_MENU, string)
