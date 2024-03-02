# source imports
from colors import *
# external imports
import time
import sys


# Handling Function

def cout(__text: object = "", end="\n"):
    sys.stdout.write(str(__text) + str(end))
    sys.stdout.flush()


def cinput(__text: object = ""):
    return input(__text)


def show_menu(options, length=52):
    continue_action = True

    # Get how many choices there are
    choice_number = len(options)

    # Print the box with the choices displayed
    print("╭" + int(length) * '─' + '╮')

    count = 0
    while count < choice_number:
        number_of_spaces_remaining = (length - 2) - (2 + len(list(str(options[count]))))
        if len(str(count)) > 1:
            number_of_spaces_remaining -= 1
        print(
            "│ " + COLOR_GREEN + COLOR_STYLE_BRIGHT + str(count) +
            '> ' + COLOR_RESET_ALL + str(options[count]) + int(number_of_spaces_remaining) * ' ' + '│'
        )

        count += 1

    print("╰" + int(length) * '─' + '╯')

    while continue_action:
        error_happened = False
        # Get user's input and return the value
        # of the user's input. Also check if the
        # input is valid, if not, return warning
        get_input = cinput('$ ')
        try:
            input_type = str(type(int(get_input)))
        except Exception as error:
            input_type = '...'

        # Check if the input is an integer
        if input_type != "<class 'int'>":
            print(COLOR_YELLOW + f"Option '{get_input}' is not valid!" + COLOR_RESET_ALL)
            time.sleep(.5)
            error_happened = True

        # Check if the input is in the choices
        if not error_happened:
            if int(get_input) < 0 or int(get_input) > (choice_number - 1):
                print(COLOR_YELLOW + f"Option '{get_input}' is not valid!" + COLOR_RESET_ALL)
                time.sleep(.5)
                error_happened = True

        # Get the corresponding choice, depending
        # on the input number

        if not error_happened:
            user_input = options[int(get_input)]
            continue_action = False
        else:
            user_input = None

    return user_input
