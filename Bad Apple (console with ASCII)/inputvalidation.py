import re

def get_int(prompt, **kwargs):
    """
    Prompts user for an input, expecting an int
    Repeats until an int is properly inputted, then returns the int

    **kwargs:
    min: Set min value acceptable
    max: Set max value acceptable
    """
    while True:
        user_input = input(prompt)

        if re.search(r"\d", user_input):
            try:
                user_input = int(user_input)
            except ValueError:
                pass
            else:
                if kwargs:
                    if kwargs.get('min', 0):
                        if user_input >= kwargs['min']:
                            return user_input
                        else:
                            continue
                    
                    if kwargs.get('max', 0):
                        if user_input <= kwargs['max']:
                            return user_input
                        else:
                            continue
                else:
                    return user_input


def get_float(prompt, **kwargs):
    '''
    Prompts user for an input, expecting a float
    Repeats until an float is properly inputted, then returns the float

    **kwargs:
    min: Set min value acceptable
    max: Set max value acceptable
    '''
    while True:
        user_input = input(prompt)

        if re.search(r"\d", user_input):
            try:
                user_input = float(user_input)
            except ValueError:
                pass
            else:
                if kwargs:
                    if kwargs.get('min', 0):
                        if user_input >= kwargs['min']:
                            return user_input
                        else:
                            continue
                    
                    if kwargs.get('max', 0):
                        if user_input <= kwargs['max']:
                            return user_input
                        else:
                            continue
                else:
                    return user_input


def get_number(prompt, **kwargs):
    '''
    Prompts user for an input, expecting a number
    Returns an int or float depending on the number inputted
    Repeats until an number is properly inputted, then returns the number

    **kwargs:
    min: Set min value acceptable
    max: Set max value acceptable
    '''
    while True:
        user_input = input(prompt)

        if re.search(r"\d", user_input):
            try:
                check_type = [int(user_input), float(user_input)]
            except ValueError:
                pass
            else:
                if kwargs:
                    if kwargs.get('min', 0):
                        if user_input >= kwargs['min']:
                            return user_input
                        else:
                            continue
                    
                    if kwargs.get('max', 0):
                        if user_input <= kwargs['max']:
                            return user_input
                        else:
                            continue
                else:
                    return user_input


def get_string(prompt):
    """
    Prompts user for an input, expecting a string
    Repeats until an string is properly inputted, then returns the string
    """
    while True:
        try:
            return str(input(prompt))
        except:
            pass


def get_bool(prompt):
    """
    Prompts user for a True/False answer
    Repeats until user inputs True or False, ignoring caps, then returns True or False
    """
    while True:
        user_input = input(prompt)

        if user_input.title() == 'True':
            return True
        elif user_input.title() == 'False':
            return False


def get_yn(prompt):
    """
    Prompts user for a yes/no answer
    Repeats until the first letter of the input is y/n, ignoring caps, then returns 'y' / 'n'
    """
    while True:
        user_input = input(prompt)

        if user_input[0].lower() == 'y':
            return 'y'
        elif user_input[0].lower() == 'n':
            return 'n'


def get_tf(prompt):
    """
    Prompts user for a True/False answer
    Repeats until the first letter of the input is t/f, ignoring caps, then returns True or False
    """
    while True:
        user_input = input(prompt)

        if user_input[0].lower() == 't':
            return True
        elif user_input[0].lower() == 'f':
            return False


def get_word(prompt):
    """
    Prompts user for a single word of only alphabet letters
    Repeats until a word is properly inputted, then returns the word as a string
    """
    while True:
        user_input = input(prompt)

        if user_input.isalpha():
            return user_input


def test(prompt):
    while True:
        user_input = input(prompt)

        return int(user_input)