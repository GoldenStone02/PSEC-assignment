import os 
import re

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


def login_user():
    return

# ==================================================================
#   Main Page Function
# ==================================================================

def print_main(inputList: list):
    content = f"{DIVIDER}\n\t\t\t\033[1;37;40m Main \033[0;37;40m\n{DIVIDER}\n"
    for i, element in enumerate(inputList):
        content += f"[ {i+1} ] {element}\n"
    content += f"[ X ] Exit Application\n{DIVIDER}\n"
    return content
def main_logic():
    return

# ==================================================================
#   Question Function
# ==================================================================

def quiz_timer():
    return

# ==================================================================
#   Main Program Loop
# ==================================================================
while LOOP:
    string = print_main(MAIN_USER_MENU)