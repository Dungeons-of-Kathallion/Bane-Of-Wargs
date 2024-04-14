# terminal_handling.py
# Copyright (c) 2024 by @Cromha
#
# Bane Of Wargs is free software: you can redistribute it and/or modify it under the
# terms of the GNU General Public License as published by the Free Software
# Foundation, either version 3 of the License, or (at your option) any later version.
#
# Bane Of Wargs is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
# PARTICULAR PURPOSE. See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with
# this program. If not, see <https://www.gnu.org/licenses/>.

# source imports
from colors import *
# external imports
import time
import sys


# Handling Function

def cout(__text: object = "", end="\n"):
    # Write to stdout the text and flush
    sys.stdout.write(str(__text) + str(end))
    sys.stdout.flush()


def cinput(__text: object = ""):
    # Ask basic input
    return input(__text)


def cinput_int(__text: object = ""):
    # Extended version of original cinput,
    # to only accept integer values
    global __input, __var
    __var = False

    while not __var:
        __var = True
        try:
            __input = int(cinput(__text))
        except ValueError as error:
            cout(COLOR_YELLOW + "Input isn't valid!" + COLOR_RESET_ALL)
            __var = False

    return __input


def cinput_multi(__text: object = "", __type: object = "list"):
    # Extended version of the original cinput,
    # to return a list or string, making the
    # user able to enter multi-line input
    global __var, __return
    __var = True
    if __type == "list":
        __return = []
    else:
        __return = ""

    while __var:
        try:
            __input = cinput(__text)
            if __type == "list":
                __return += [__input]
            else:
                __return += __input + "\n"
        except EOFError as error:
            __var = False

    return __return


def show_menu(options, length=52):
    continue_action = True

    # Get how many choices there are
    choice_number = len(options)

    # Print the box with the choices displayed
    cout("╭" + int(length) * '─' + '╮')

    count = 0
    while count < choice_number:
        number_of_spaces_remaining = (length - 2) - (2 + len(list(str(options[count]))))
        if len(str(count)) > 1:
            number_of_spaces_remaining -= 1
        cout(
            "│ " + COLOR_GREEN + COLOR_STYLE_BRIGHT + str(count) +
            '> ' + COLOR_RESET_ALL + str(options[count]) + int(number_of_spaces_remaining) * ' ' + '│'
        )

        count += 1

    cout("╰" + int(length) * '─' + '╯')

    while continue_action:
        error_happened = False
        # Get user's input and return the value
        # of the user's input. Also check if the
        # input is valid, if not, return warning
        get_input = cinput(COLOR_GREEN + COLOR_STYLE_BRIGHT + '$ ' + COLOR_RESET_ALL)
        try:
            input_type = str(type(int(get_input)))
        except Exception as error:
            input_type = '...'

        # Check if the input is an integer
        if input_type != "<class 'int'>":
            cout(COLOR_YELLOW + f"Option '{get_input}' is not valid!" + COLOR_RESET_ALL)
            time.sleep(.5)
            error_happened = True

        # Check if the input is in the choices
        if not error_happened:
            if int(get_input) < 0 or int(get_input) > (choice_number - 1):
                cout(COLOR_YELLOW + f"Option '{get_input}' is not valid!" + COLOR_RESET_ALL)
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
