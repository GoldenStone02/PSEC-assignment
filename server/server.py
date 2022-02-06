# StudentID:	p2008493
# Name:	        Ng Jun Han
# Class:		DISM/FT/1B/05   
# Assessment:	CA1 
# 
# Script name:	server.py
# 
# Purpose:	The purpose of the script is for the user to retrieve the quiz settings, question pool, and user data without needing
#           to have the files downloaded onto the user's computer. With the script managing all the request that is coming from the 
#           client user.
#
# Usage syntax:	Run with play button / command line, eg. py read-cmd-line 1 2 3
# 
# Input file:   C:\PSEC_project\server\courses.json
#               C:\PSEC_project\server\quiz_settings.json
#               C:\PSEC_project\server\users.json
#               C:\PSEC_project\server\quiz_results.csv
# 
# Output file:  C:\PSEC_project\server\courses.json
#               C:\PSEC_project\server\quiz_settings.json
#               C:\PSEC_project\server\users.json
#               C:\PSEC_project\server\quiz_results.csv
# 
# 
# Python ver:	Python 3
#
# Reference:	This program is adapted from the following:
#                   a) Socket Programming with Multi-Threading in Python
#                   https://www.tutorialspoint.com/socket-programming-with-multi-threading-in-python
# 
#                   
# Library/
# package/	
# Module /      sys, socket, traceback, threading, json, csv, random, time
#
# Known issues:	N/A

import sys
import socket
import traceback
import threading
import json
import csv
import random
import time

# ==============================================================================================================================
#   Initialize variables
# ==============================================================================================================================

HOST = "127.0.0.1"
PORT = 8181

_USERNAME_AND_PASSWORD = "./server/users.json"   # Stored as a list
_QUIZ_SETTING = "./server/quiz_settings.json"    # Stored as a dict
_QUESTION_POOL = "./server/question_pool.json"    # Stored as a list
_QUIZ_RESULTS = "./server/quiz_results.csv"      # Stored as a csv

# ==============================================================================================================================
#   General Functions
# ==============================================================================================================================

def main():
    start_server(HOST, PORT)

# Reads and empties value into "dictionary" variable
def read_file(file: str, option: str):
    '''
    Returns file content of the inputted file after reading it.

    Parameters:
        file (str) : Input file path.
        option (str) : Format it should read the file.
    Returns:
        (list or dict) : Returns the data of the file.
    '''
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

# Writes to server files
def write_to_file(input_variable: any, file_path: str, option: str, optional_parameter: list = None):
    '''
    Writes the inputted variable to the file.

    Args: 
        input_variable (any) : The variable to be written to the file.
        file_path (str) : The file path to be written to.
        option (str) : The format of the file.
    '''
    if option == "csv":
        index = 0
        for i, item in enumerate(input_variable):
            if len(item) > index:
                index = i
        # Fieldnames are the key values of the first item in the dictionary.
        fields = optional_parameter
        # Writes to the csv file with the correct headings and value
        with open(file_path, "w", newline="") as csvfile:
            csvwriter = csv.DictWriter(csvfile, fieldnames=fields)
            csvwriter.writeheader()
            csvwriter.writerows(input_variable)
    elif option == "json":
        with open(file_path, "w") as f:
            json.dump(input_variable, f, indent=4)

# ==============================================================================================================================
#   Socket Programming Functions
# ==============================================================================================================================

# Starts the server
def start_server(host, port):
    print("[STARTING] Server is starting...")
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    try:
        server.bind((host, port))
    except:
        print("Bind failed. Error : " + str(sys.exc_info()))
        sys.exit()
    server.listen(20) # listening up to 20 different clients
    print("[LISTENING] Socket now listening")
    # infinite loop- do not reset for every requests
    while True:
        connection, address = server.accept()   # Server would wait here until a new connection is received
        ip, port = str(address[0]), str(address[1])
        print(f"[NEW CONNECTION] Connected with {ip}:{port}")
        try:
            # Server attempts to start a thread with target function "clientThread()"
            thread = threading.Thread(target=clientThread, args=(connection, ip, port))
            thread.start()
        except:
            print("Thread did not start.")
            traceback.print_exc()

# Handler for client machine
def clientThread(connection, ip, port, max_buffer_size = 10000):
    is_active = True
    while is_active:
        client_input = receive_input(connection, max_buffer_size)
        if client_input == "quit":
            # Closes the connection of current thread
            connection.close()
            print(f"[CLOSED] Connection with {ip}:{port} closed")
            is_active = False
        else:
            # Send the message after dumping it and encoding it.
            connection.sendall(json.dumps(client_input).encode("utf8"))  
            print(f"[PROCESS] {ip}:{port}. Sent to Client, Packet type: '{client_input['type']}'")

# Receives input from client machine
def receive_input(connection, max_buffer_size):
    client_input = connection.recv(max_buffer_size)
    decoded_input = client_input.decode("utf8")
    result = process_input(decoded_input)
    return result

# Processes the input from the client
def process_input(client_request):
    '''
    Processes the input from the client.
    
    Args:
        client_request (str) : The input from the client.
    '''
    client_request = json.loads(client_request)
    match client_request['type']:
        case "quit":            # terminates the connection
            response = "quit"
      
        case "get_courses":     # Returns a list of the available courses
            question_database = read_file(_QUESTION_POOL, "json")
            course_list = []
            for attempt in question_database:
                course_list.append(attempt['course'])
            print(course_list)
            response = {
                "type": "available_courses",
                "data": course_list
            }
       
        case "add_user":    # This one is used by both admin.py and user.py
            check = register_user(client_request)
            if check:
                response = {
                    "type": "user_successfully_added"
                }
            else:
                response = {
                    "type": "user_already_exist"
                }
       
        case "reset_password":  # Resets the password
            user_database = read_file(_USERNAME_AND_PASSWORD, "json")
            changed = False
            for user in user_database:
                if user['userID'] == client_request['userID'] and user['email'] == client_request['email']:
                    user['password_SHA256'] = client_request['password']    # Changes the password to the client's changed password
                    changed = True
                    continue
            write_to_file(user_database, _USERNAME_AND_PASSWORD, "json")
            if changed:
                response = {
                    "type": "reset_pw_status",
                    "data": "success"
                }
            else:
                response = {
                    "type": "reset_pw_status",
                    "data": "failed"
                }
        
        case "show_attempts":   # Show the number of attempt of the given user
            no_of_attempts = show_no_of_attempts(client_request['userID'], client_request['quiz_setting'])
            response = {
                "type": "returned_no_of_attempts",
                "data": no_of_attempts
            }
        
        case "user_login":    # Checks if the user is registered and if the password is correct
            server_response = check_credentials(client_request)
            if server_response == True:
                response = {
                    "type": "login_status",
                    "data": "success"
                    }
            else:
                response = {
                    "type": "login_status",
                    "data": "failed"
                }
        
        case "quiz_settings":   # Get the quiz settings
            response_list = get_quiz_settings(client_request)
            response = {
                "type": "returned_quiz_settings",
                "data": response_list
            }
            print(json.dumps(response, indent=2), type(response))
        
        case "question_pool":   # Get the question pool
            # Read the quiz setting then select the questions in the format stated by the question pool
            processed_question_pool = fetch_questions(client_request['data'])
            response = {
                "type": "returned_question_pool",
                "data": processed_question_pool
            }
        
        case "submitted_user_attempt":  # Calculate the score and update the database
            user_quiz_result = calculate_user_result(client_request['quiz_setting'], client_request['user_answer'])
            user_attempt = format_attempt(client_request['userID'], client_request['quiz_setting'], client_request['user_answer'], user_quiz_result)
            quiz_results = read_file(_QUIZ_RESULTS, "csv")

            # This section below is used for ensure that no matter how many question a quiz has, it will still be added into the quiz_results.csv w/o any errors
            field = []
            # Gets the headers of the first element in the quiz_results csv file
            for attempt in quiz_results[0]:
                field.append(attempt)
            
            # Checks to see if the headers are the same as the current headers
            if field == [] or len(field) < len(user_attempt.keys()):
                field.clear()
                for key in user_attempt:
                    field.append(key)   # Uses the new headers from the recent attempt.

            # Adds the user attempt into the csv dictionary
            quiz_results.append(user_attempt)

            # Changes the data field with "NA" if the data field is empty.
            for attempt in quiz_results:
                for key in attempt:
                    if attempt[key] == "" or attempt[key] == None:
                        attempt[key] = "NA"

            # Writes the dictionary into the csv file
            write_to_file(quiz_results, _QUIZ_RESULTS, "csv", field)
            response = {
                "type": "user_results",
                "data": user_quiz_result
            }
        
        case "previous_attempts":   # Show the user's previous attempts
            previous_attempts = show_previous_attempts(client_request['userID'], client_request['quiz_setting'])
            response = {
                "type": "previous_attempts",
                "data": previous_attempts
            }
        # =====================================================================================================================
        # Everything below are requests that will be made by the admin.py client
        # =====================================================================================================================
        
        case "admin_quiz_setting":  # Gets the quiz settings for the admin
            quiz_settings =  read_file(_QUIZ_SETTING, "json")
            response = {
                "type": "returned_admin_quiz_setting",
                "data": quiz_settings
            }
        
        case "admin_fetch_specific_setting":   # Fetches specific quiz setting data such as courses and modules
            specific_setting = fetch_specific_settings(client_request)
            response = {
                "type": "returned_admin_specific_settings",
                "data": specific_setting
            }
        
        case "admin_write_settings":    # Writes the quiz settings into the database
            write_to_file(client_request['quiz_setting'], _QUIZ_SETTING, "json")
            print(json.dumps(client_request['quiz_setting'], indent=2))
            response = {
                "type": "updated_quiz_setting"
            }
        
        case "admin_write_user":    # Update the user configurations into the database
            write_to_file(client_request['user_config'], _USERNAME_AND_PASSWORD, "json")
            print(json.dumps(client_request['user_config'], indent=2))
            response = {
                "type": "updated_user_config"
            }
        
        case "admin_read_file":     # Reads the specified file from the database
            file_type = client_request['file']
            match file_type:
                case "user":
                    file = _USERNAME_AND_PASSWORD
                case "setting":
                    file = _QUIZ_SETTING
                case "course":
                    file = _QUESTION_POOL
                case "question":
                    file = _QUESTION_POOL
            file_data = read_file(file, "json")
            print(json.dumps(file_data, indent=2))
            response = {
                "type": "returned_file_data",
                "data": file_data
            }
        
        case "admin_fetch_question_pool":   # Fetches the question pool
            print(client_request)
            data = fetch_question_pool_data(client_request)
            response = {
                "type": "returned_admin_question_pool",
                "data": data
            }
        case "admin_previous_attempts":   # Fetches the previous attempts
            previous_attempts = admin_show_previous_attempts(client_request['quiz_setting'])
            response = {
                "type": "previous_attempts",
                "data": previous_attempts
            }
    return response



# ==============================================================================================================================
#   Server Processing Functions
# ==============================================================================================================================

# Formats the client_request data into a proper user format
def register_user(client_request: dict):
    '''
    This function is used to register a new user into the system.
    
    Args:
        client_request: A dictionary containing the user's information.
    '''
    users_database = read_file(_USERNAME_AND_PASSWORD, "json")
    user_exist = False
    for user in users_database:
        if user['userID'] == client_request['userID']:
            user_exist = True
    if not user_exist:
        new_user = {
            "userID": client_request['userID'],
            "email": client_request['email'],
            "password_SHA256": client_request['password'],
            "current_course": client_request['course']
        }
        users_database.append(new_user)
        print(json.dumps(users_database, indent=2))
        write_to_file(users_database, _USERNAME_AND_PASSWORD, "json")
        return True
    else:
        return False

# Show the previous attempt of the user
def show_previous_attempts(userID: str, quiz_setting: dict):
    '''
    This function is used to show the previous attempts of the user.
    
    Args:
        userID (str) : The user's ID.
        quiz_setting (dict) : The quiz setting that the user is in.
    
    Returns:
        A list of previous attempts.
    '''
    quiz_results = read_file(_QUIZ_RESULTS, "csv")
    users_attempts = []
    for attempt in quiz_results:
        if attempt['userID'] == userID and attempt['module'] == quiz_setting['module_name'] and attempt['quiz'] == quiz_setting['quiz_name']:
            users_attempts.append(attempt)
    if len(users_attempts) == 0:
        return "no-attempts"
    return users_attempts

# Show the previous attempt of the user
def admin_show_previous_attempts(quiz_setting: dict):
    '''
    This function is used to show the previous attempts of the user.
    
    Args:
        userID (str) : The user's ID.
        quiz_setting (dict) : The quiz setting that the user is in.
    
    Returns:
        A list of previous attempts.
    '''
    quiz_results = read_file(_QUIZ_RESULTS, "csv")
    users_attempts = []
    for attempt in quiz_results:
        if attempt['course'] == quiz_setting['course'] and attempt['module'] == quiz_setting['module_name'] and quiz_setting['assessment_component'] in attempt['topics-tested'].split(","):
            users_attempts.append(attempt)
    if len(users_attempts) == 0:
        return "no-attempts"
    return users_attempts

# Show the number of attempt of the user
def show_no_of_attempts(userID: str, quiz_setting: dict):
    '''
    This function is used to show the number of attempts of the user.
    
    Args:
        userID (str) : The user's ID.
        quiz_setting (dict) : The quiz setting that the user is in.
        
    Returns:
        The number of attempts.
    '''
    quiz_result = read_file(_QUIZ_RESULTS, "csv")
    attempt_count = 0
    for attempt in quiz_result:
        if userID == attempt['userID'] and attempt['module'] == quiz_setting['module_name'] and attempt['quiz'] == quiz_setting['quiz_name']:
            attempt_count += 1
    if quiz_setting['maximum_number_of_attempts'] == "unlimited":
        return "unlimited"
    else:
        return quiz_setting['maximum_number_of_attempts'] - attempt_count

# Gets the quiz setting from the json files
def get_quiz_settings(client_request: dict):
    '''
    This functions gets the list of quiz settings in quiz_settings.json. 

    Parameters:
        client_request (dict) : Packet that is used to query for the questions in a course.
    
    Returns:
        response_list (list) : Return a list of all the quiz settings the user has access to.
    '''
    userid_database = read_file(_USERNAME_AND_PASSWORD, "json")
    for user in userid_database:
        if user['userID'] == client_request['userID']:
            course = user['current_course']

    database = read_file(_QUIZ_SETTING, "json")
    response_list = []
    for element in database:
        # Only show quizzes that are allowed to be shown
        if element['show_quiz'] == True and element['course'] == course:
            response_list.append(element)
    return response_list

# Checks the userID and password against the files
def check_credentials(client_request: dict) -> bool:
    server_user_files = read_file(_USERNAME_AND_PASSWORD, "json")
    for element in server_user_files:
        if check_userID(element, client_request) and check_password(element, client_request):
            print(f"[PROCESS] {element['userID']} Login Successful")
            return True
    return False

# Checks if the userID already exist in the database
def check_userID(user_server_files, client_request) -> bool:
    if user_server_files['userID'] == client_request['userID']:
        return True
    return False

# Check if the password is correct
def check_password(user_server_files, client_request) -> bool:
    if user_server_files['password_SHA256'] == client_request['password']:
        return True
    return False

# Fetches for specific data from the quiz_setting.json file
def fetch_specific_settings(client_request: dict) -> list:
    '''
    This function is used to fetch the quiz setting from the quiz_setting.json file.
    
    Args:
        client_request: A dictionary containing the quiz setting.
    
    Returns:
        A list containing the specified quiz setting.
    '''
    question_database = read_file(_QUESTION_POOL, "json")
    setting_type = client_request['setting']
    setting_list = []   # Used to add elements of the specific setting to the list
    match setting_type:
        case "course":
            for each_course in question_database:
                setting_list.append(each_course['course'])
        case "module":
            for each_course in question_database:
                if each_course['course'] != client_request['course']:
                    continue
                for each_module in each_course['modules']:
                    setting_list.append(each_module['module_name'])
        case "assessment_component":
            for each_course in question_database:
                if each_course['course'] != client_request["course"]:
                    continue
                for each_module in each_course['modules']:
                    if each_module['module_name'] != client_request["module"]:
                        continue
                    for each_topic in each_module['topics']:
                        setting_list.append({"topic": each_topic['topic_name'], "max_number_of_questions": len(each_topic['questions'])})
    return setting_list

# Compares the client requested quiz and the question pool.
def fetch_questions(client_request: dict) -> dict:
    '''
    This function fetches questions from the question_pool.json, 
    randomizes the question order, and the options if randomize_option is true.

    Parameters:
        client_request (dict) : Quiz setting data that's used for reference to retrieve 
        the correct questions for any given quiz.
    
    Returns:
        processed_question_list (dict) : Returns the processed question pool.
    '''
    question_list = search_for_question(client_request)
    random.shuffle(question_list)   # Randomizes the questions
    for question in question_list:  # Adds user_answer for people to answer
        question["user_answer"] = None
    processed_question_list = randomize_options(client_request, question_list)
    print(json.dumps(processed_question_list, indent=2), "\n\n")
    
    print("Number of question: ",len(processed_question_list))
    return processed_question_list

# Fetches specific portions of the question pool database
def fetch_question_pool_data(client_request: dict) -> list:
    '''
    This function fetches specific data from the question_pool.json file.

    Args:
        client_request (dict) : A dictionary containing the selection criterias.
    '''
    question_pool = read_file(_QUESTION_POOL, "json")
    dictionary = {}
    returned_qn_pool_list = []
    match client_request['file']:
        case "course":
            for each_course in question_pool:
                returned_qn_pool_list.append({"course": each_course['course']})
            dictionary = {
                "data": returned_qn_pool_list
            }
        case "module":
            for each_course in question_pool:
                if each_course['course'] != client_request['course_name']:
                    continue
                for each_module in each_course['modules']:
                    returned_qn_pool_list.append({"module": each_module['module_name']})
            dictionary = {
                "course": client_request['course_name'],
                "data": returned_qn_pool_list
            }
        case "topic":
            for each_course in question_pool:
                if each_course['course'] != client_request['course_name']:
                    continue
                for each_module in each_course['modules']:
                    if each_module['module_name'] != client_request['module']:
                        continue
                    for each_topic in each_module['topics']:
                        returned_qn_pool_list.append({
                            "topic": each_topic['topic_name'],
                            "marks_for_each_question": each_topic['marks_for_each_question']
                        })
            dictionary = {
                "course": client_request['course_name'],
                "module": client_request['module'],
                "data": returned_qn_pool_list
            }
        case "question":    # Returns the question pool for that specific question
            for each_course in question_pool:
                if each_course['course'] != client_request['course_name']:
                    continue
                for each_module in each_course['modules']:
                    if each_module['module_name'] != client_request['module']:
                        continue
                    for each_topic in each_module['topics']:
                        if each_topic['topic_name'] != client_request['topic']:
                            continue
                        for each_question in each_topic['questions']:
                            returned_qn_pool_list.append({
                                "question": each_question['question_name'], 
                                "correct_option": each_question['correct_option'],
                                "options": each_question['options']})
            dictionary = {
                "course": client_request['course_name'],
                "module": client_request['module'],
                "topic": client_request['topic'],
                "data": returned_qn_pool_list
            }
    return dictionary

# Search for questions that are for a given topic for the quiz
def search_for_question(client_request: dict) -> list:
    '''
    This function searches through the question pool database and finds
    the questions, given the quiz setting file, "client_request" for that specific quiz.

    Parameters:
        client_request (dict) : Quiz setting that is used to search for the question
        database.
    
    Returns:
        question_list (list) : Returns the list of questions that are in the given topics
        for the quiz.
    '''
    question_database = read_file(_QUESTION_POOL, "json")
    question_list = []
    for course_db in question_database:
        # If course is not a match, continues the for loop
        if course_db['course'] != client_request["course"]:    
            continue
        for module_db in course_db['modules']:
            # If module is not a match, continues the for loop
            if module_db['module_name'] != client_request["module_name"]:     
                continue
            for topic_db in module_db['topics']:
                for topic_in_settings in client_request["assessment_component"]:
                    if topic_db['topic_name'] == topic_in_settings['topic_name']:
                        question_db_list = random.sample(topic_db['questions'], topic_in_settings['number_of_question'])
                        for element in question_db_list:
                            element['topic_name'] = topic_db['topic_name']
                        question_list.extend(question_db_list)
                        continue
    return question_list

# Randomized option if the randomize_option is True.
def randomize_options(client_request: dict, question_list: list) -> list:
    '''
    This functions checks if the given setting for the quiz has randomize_option 
    set to True or False.

    Parameters:
        client_request (dict) : Quiz setting data that is used to check the boolean, randomize_option
        question_list (list) : Question pool list 
    
    Returns:
        question_list (list) : Randomizes the option for questions if boolean, randomize_option is True. 
        Else, the options for each question would be left untouched.
    '''
    if client_request['randomize_options'] != True:
        # Returns the question_list unaltered
        return question_list

    # Shuffles the options for each question
    for question in question_list:      
        random.shuffle(question['options'])
    return question_list

# Calculate the user's score
def calculate_user_result(quiz_setting: dict, user_answer: list) -> tuple:
    '''
    This function is used to calculate how much marks the user got for the quiz, as well
    as other information that will be used for statistical analysis.

    Args:
        quiz_setting (dict) : Used to find the topic list for the quiz. 
        user_answer (list) : Used to calculate user's result for the quiz.
    
    Returns:
        (tuple) : Returns the number of questions answered correctly, number of 
        questions answered wrongly and the total marks
    '''
    question_database = read_file(_QUESTION_POOL, "json")
    topics_db_list = []     # Stores the topic_name and the marks per question for that topic
    answered_correct = 0
    answered_wrong = 0
    total_possible_marks = 0
    total_marks = 0
    for course_db in question_database:
        # If course is not a match, continues the for loop
        if course_db['course'] != quiz_setting["course"]:    
            continue
        for module_db in course_db['modules']:
            # If module is not a match, continues the for loop
            if module_db['module_name'] != quiz_setting["module_name"]:     
                continue
            for topic_db in module_db['topics']:
                topics_db_list.append({'topic_name': topic_db['topic_name'], 'marks_for_each_question': topic_db['marks_for_each_question']})
    for answer in user_answer:   
        for topic_db in topics_db_list:
            if topic_db['topic_name'] != answer['topic_name']:
                continue
            else:
                if answer['user_answer'] == answer['correct_option']:
                    total_marks += topic_db['marks_for_each_question']
                    total_possible_marks += topic_db['marks_for_each_question']
                    answered_correct += 1
                else:
                    total_possible_marks += topic_db['marks_for_each_question']
                    answered_wrong += 1 
    return (answered_correct, answered_wrong, total_marks, total_possible_marks)

# Formatting the attempt for csv
def format_attempt(userID: str, quiz_setting: dict, user_answer: list, user_quiz_result: tuple):
    '''
    This function formats the inputs into a dictionary that will be written into the quiz_result.csv
    using csv.DictWriter.

    Args:
        userID (str) : Used to identify whose attempt is being logged into the database.
        quiz_settings (dict) : Retrieve information such as the course, module and topics tested.
        user_answer (list) : Used for storing of user's answers.
        user_quiz_results (tuple) : Contains information such as total_possible_marks and total_marks.

    Returns:
        attempt (dict) : Attempt that will be appended to the quiz_result.csv
    '''
    topics_list = []
    for topic in quiz_setting["assessment_component"]:
        topics_list.append(topic['topic_name'])
    attempt = {
        "userID" : userID,
        "course": quiz_setting['course'],
        "module": quiz_setting['module_name'],
        "quiz": quiz_setting['quiz_name'],
        "topics-tested": ",".join(i for i in topics_list),
        "grade": round(user_quiz_result[2]/user_quiz_result[3] * 100, 2),
        "qn-answered-correct": user_quiz_result[0],
        "qn-answered-wrong": user_quiz_result[1],
        "total-marks": user_quiz_result[2],
        "total-possible-marks": user_quiz_result[3],
        "date-of-attempt": time.ctime()
    }
    for i, answer in enumerate(user_answer):
        attempt[f'question-{i + 1}'] = answer['question_name']
        attempt[f'correct-answer-{i + 1}'] = answer['correct_option']
        attempt[f'user-answer-{i + 1}'] = answer['user_answer']
    print(json.dumps(attempt, indent=2))
    return attempt

if __name__ == "__main__":
    main()
