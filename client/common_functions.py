# Common functions between admin and user files
import os
import getpass 

def get_input(user_input: str, visible_input: bool = True) -> str:
    """
    This function basically clears the command line before requesting an input
    from the user.

    Parameters:
        user_input (str) : Used as a string for the input.
        visible_input (bool) : Allows user to see what they are typing. If True,
        text will be visible. Else, text will be hidden. (Default - True)
    
    Returns:
        output (str) : Returns the user inputted string.
    """
    os.system("cls")
    if visible_input:
        output = input(user_input)
    else:
        output = getpass.getpass(user_input)
    return output