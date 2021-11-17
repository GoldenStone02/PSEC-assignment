import os
import re


# ==================================================================
#   Initialize Variables
# ==================================================================

empty = ""
divider = f"{empty:=^60}"

reg = re.compile("^[\w]+$")

quiz_setting_text = "./admin/quiz_settings.txt"
quiz_question_text = "./admin/question_pool.txt"
main_menu = ["Register User", "Question Pool", "Quiz Settings", "Generate Report"]
dictionary = {}
loop = True

# ==================================================================
#   General Functions
# ==================================================================

# Reads and empties value into "dictionary" variable
# "option" parameter used to define what format it should print in
def ReadFileContent(file: str, option):
    try:
        # Ensures that the file has been formatted correctly
        RemoveLineFeed(file)

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
        # Hard code setting values
        # with open(file, "w") as f:
        #     f.write("time: 60\nno_of_attempts: 2\nno_of_questions: 5")

# Removes linefeed that is in between lines in the file
def RemoveLineFeed(file: str):
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
# 
# "show_number" parameter is used to define the format of returning string.
# 
# "0" prints out file content without numbering
# "1" prints out with sequence numbering
def ViewFileContent(show_numbers: int):
    content = ""

    key_list = list(dictionary.keys())
    value_list = list(dictionary.values())
    
    if show_numbers == 1:
        for i, item in enumerate(key_list): 
            content += f"[ {i + 1} ] {item}: {value_list[i]}\n"
    elif show_numbers == 0:
        for i, item in enumerate(key_list):
            content += f"[ - ] {item}: {value_list[i]}\n"
    
    return content

# Prints the text file with some UI.
# Needs to happen after "ReadFileContent()" has been executed
def PrintFile(): 
    content = f"{divider}\n\t\t\t\033[1;37;40m Quiz Settings\033[0;37;40m\n{divider}\n"

    content += ViewFileContent(0)

    content += f"{divider}\n\t\tSelect one of the options\n{divider}\n"
    content += "[ A ] Add New Quiz Setting  [ D ] Delete Quiz Setting\n"
    content += "[ E ] Edit Quiz Setting     [ X ] Back to Main\n"
    content += f"{divider}\n"

    return content

# Checks whether the input is an integer or string
# If the input is a digit, return True
# if the input is a string, return False
def CheckIsDigit(input):
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
def PrintMain(inputList: list):
    content = f"{divider}\n\t\t\t\033[1;37;40m Main \033[0;37;40m\n{divider}\n"
    for i, element in enumerate(inputList):
        content += f"[ {i+1} ] {element}\n"
    content += f"[ X ] Exit Application\n{divider}\n"
    return content

# main logical system for selection page
# "menuList" is for 
def MainLogic(menuList: list, content: str):
    while True:
        stored_value = input(content)
        if CheckIsDigit(stored_value):
            if int(stored_value) in range(1, len(menuList) + 1):
                if stored_value == "1":
                    RegisterUser()
                elif stored_value == "2":
                    QuestionPool()
                elif stored_value == "3":
                    QuizSetting()
                elif stored_value == "4":
                    Report()
            else:
                input("\033[1;37;41mPlease select a valid option.\033[0;37;40m")               
        elif stored_value.upper() == "X":
            os.system("cls")
            while True:
                userConfirm = input(f"{divider}\n\033[1;37;40m\t\tAre you sure want to quit?\033[0;37;40m\n{divider}\n[ Y ] Yes\t\t[ N ] No\n{divider}\n")
                if userConfirm.upper() == "Y":
                    print("\033[0;32;40mGoodbye\033[0;37;40m")
                    global loop
                    loop = False
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


# ===================================================================================================
#   Quiz Settings Functions
# ===================================================================================================

# Logicial system for quiz setting
def SettingLogic(userInput: str):
    valueCap = str(userInput).upper()
    # Logical Circuit
    if valueCap == "X": # Close App
        global loop
        os.system("cls")
        loop = False
    elif valueCap == "A": # Add Setting
        AddSetting()
    elif valueCap == "E": # Edit Setting
        EditSetting()
    elif valueCap == "D": # Delete Setting
        DeleteSetting()
    else:
        input("\033[1;37;41mPlease select a valid option.\033[0;37;40m")

# Issue: Need to implement validation [Almost Complete]
# [Note] Need to write additional function in order to implement functionality to setting
def AddSetting(): 
    while True:
        while True:
            os.system("cls")
            new_setting_name = input(f"{divider}\n\t\t\tAdding Setting\n{divider}\nSetting Name: \nSetting Value: \n{divider}\n[ X ] Back to Menu\n{divider}\nSetting Name: ")

            # Exit out of loop
            if new_setting_name.upper() == "X":
                break
            if not new_setting_name.isalnum():
                input(f"\n\033[1;37;41mInput value can't contain special characters!\033[0;37;40m\n")
                continue
            elif new_setting_name[0].isdigit():
                input(f"\n\033[1;37;41mPlease start with a letter!\033[0;37;40m\n")
                continue
        
            # Exit loop once all checks return no errors
            break

        # Variable value check loop
        while True:
            os.system("cls")
            new_setting_value = input(f"{divider}\n\t\t\tAdding Setting\n{divider}\nSetting Name: {new_setting_name}\nSetting Value: \n{divider}\n[ X ] Back to Menu\n{divider}\nSetting Value: ")

            if new_setting_value.upper() == "X":
                break
            if new_setting_value == "":
                input(f"\n\033[1;37;41mPlease enter a valid into the input\033[0;37;40m\n")
                continue            
            elif not new_setting_value.isalnum():
                input(f"\n\033[1;37;41mInput value can't contain special characters!\033[0;37;40m\n")
                continue

            # Exit loop once all checks return no errors
            break

        # Check if the user wants to confirm the setting
        while True:
            os.system("cls")
            finalCheck = input(f"{divider}\n\t\t\tAdding Setting\n{divider}\nSetting Name: {new_setting_name}\nSetting Value: {new_setting_value}\n{divider}\n[ C ] Confirm?\t\t[ X ] Exit\n{divider}\n")
            
            if finalCheck.upper() == "X":
                break
            elif finalCheck.upper() == "C":
                input("\033[0;32;40mYour changes have been saved!\033[0;37;40m\nPress Enter to Continue\n")
            else:
                input("\n\033[1;37;41mPlease input one of the options\033[0;37;40m\n")
            input(f"loop2: {True}")
            break
        break
    # Checks if the program aborted at any point 
    if True:
        with open(quiz_setting_text, "a") as f:
            f.write(f"{new_setting_name}: {new_setting_value}")

# Issue: Still need to Implement!!
def EditSetting():
    key_list = list(dictionary.keys())
    while True:
        edit_index = SelectSetting("Editing Settings")

        if not CheckIsDigit(edit_index): # execute if its not an integer
            if edit_index.upper() == "X":
                break        
        elif CheckIsDigit(edit_index): # execute if its an integer
            while True:
                selector = input(f"{divider}\nWhat do you want to change?\n{divider}\n[ 1 ] Setting Name\n[ 2 ] Setting Value\n{divider}\n[ X ] Back to Menu\n{divider}\n")
                if CheckIsDigit(selector):
                    if selector == "1":
                        while True:
                            os.system("cls")
                            new_name = input(f"{divider}\nSetting Name: \033[1;37;40m{key_list[edit_index]}\033[0;37;40m\nSetting Value: {dictionary[key_list[edit_index]]}\n{divider}\n[ X ] Back to Menu\n{divider}\nInput new name: ")
                            # Exit out of loop
                            if new_name.upper() == "X":
                                break
                            if not new_name.isalnum():
                                input(f"\n\033[1;37;41mInput value can't contain special characters!\033[0;37;40m\n")
                                continue
                            elif new_name[0].isdigit():
                                input(f"\n\033[1;37;41mPlease start with a letter!\033[0;37;40m")
                                continue    

                            break
                        while True:
                            os.system("cls")
                            confirm_change = input(f"{divider}\n\t\tConfirm Changes?\n{divider}\nSetting Name: \033[1;37;40m{new_name}\033[0;37;40m\nSetting Value: {dictionary[key_list[edit_index]]}\n{divider}\n[ C ] Confirm \n[ X ] Cancel Changes\n{divider}\n")
                            if confirm_change.upper() == "X":
                                break
                            if confirm_change == "":
                                input(f"\n\033[1;37;41mPlease enter a valid into the input\033[0;37;40m\n")
                                continue            
                            elif not confirm_change.isalnum():
                                input(f"\n\033[1;37;41mInput value can't contain special characters!\033[0;37;40m\n")
                                continue                            
                            break                 
                    elif selector == "2":
                        input("option 2")
                    else:
                        input(f"{divider}\n\033[1;37;41mPlease enter a value within the range.\033[0;37;40m")
                else:
                    if selector.upper() == "X":
                        break
                    input(f"edit_index: {edit_index}, settings: {dictionary}")
                    # Changing dictionary key
                    dictionary["example"] = dictionary.pop(key_list[edit_index])
                    input(f"edit_index: {edit_index}, settings: {dictionary}")
                    
                    # Changing dictionary value
                    dictionary[key_list[edit_index]] = "example"
                    input(f"edit_index: {edit_index}, settings: {dictionary}")
        else:
            input("\n\033[1;37;41mPlease input one of the options\033[0;37;40m\n")
        
        
        
        


# Issue: Just deletes everything in the file [Solved]
def DeleteSetting(): 
    while True:
        os.system("cls")

        deleting_index = SelectSetting("Delete Setting")

        if deleting_index == "X":
            return

        while True:
            os.system("cls")
            finalCheck = input(f"{divider}\n{ViewFileContent(1)}\n{divider}\n[ C ] Confirm?\t\t[ X ] Back to Menu\n{divider}\n")
            
            if finalCheck.upper() == "X":
                break
            elif finalCheck.upper() == "C":
                with open(quiz_setting_text, "r") as f:
                    lines = f.read().splitlines()
                
                with open(quiz_setting_text, "w") as f:
                    for number, line in enumerate(lines):
                        if number != deleting_index:
                            f.write(line + '\n')   
                input("\033[0;31;40mOption has been deleted!\033[0;37;40m\nPress Enter to Continue\n")  
                break     
            else:
                input(f"{divider}\n\033[1;37;41mPlease select an option.\033[0;37;40m") 
        break

# Returns index value for menu navigation
# "title" parameter needs to be a string for the printing
def SelectSetting(title: str): 
    while True:
        value_number = input(f"{divider}\n\t\t\t{title}\n{divider}\n{ViewFileContent(1)}{divider}\n[ X ] Back to Menu\n{divider}\n")
        os.system("cls")
        try:
            value = int(value_number)
        except ValueError:
            if value_number.upper() == "X": 
                return "X"
            else:
                print(f"{divider}\n\033[1;37;41mPlease select an option.\033[0;37;40m")
        else:
            if int(value_number) > len(dictionary) or int(value_number) <= 0:
                print(f"{divider}\n\033[1;37;41mPlease enter a value within the range.\033[0;37;40m")
            else:
                return (value - 1)

# ========================================================================
#   Generate Report Functions
# ========================================================================

# ========================================================================
#   Sub Program Loops
# ========================================================================
def RegisterUser():
    input("Register User")

def QuestionPool():
    ReadFileContent(quiz_question_text, "question")
    questPool = PrintFile()
    input(questPool)

def QuizSetting():
    while loop:
        os.system("cls")
        ReadFileContent(quiz_setting_text, "settings")
        quizSettings = PrintFile()    
        adminInput = input(quizSettings)
        SettingLogic(adminInput)

def Report():
    input("Generate Report")
# ========================================================================
#   Main Program Loop
# ========================================================================

while loop:
    string = PrintMain(main_menu)
    MainLogic(main_menu, string)
