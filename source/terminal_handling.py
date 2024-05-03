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
import os
import re
import sys
import colorsys
from rich.console import Console


# Handling Function

def cout(__text: object = "", end="\n"):
    # Write to stdout the text and flush
    sys.stdout.write(format_string_color(format_string_separator(__text)) + str(end))
    sys.stdout.flush()


def cinput(__text: object = ""):
    # Ask basic input
    return input(format_string_separator(__text))


def cinput_int(__text: object = ""):
    # Extended version of original cinput,
    # to only accept integer values
    global __input, __var
    __var = False

    while not __var:
        __var = True
        try:
            __input = int(cinput(format_string_separator(__text)))
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


def format_string_separator(text: str) -> str:
    # First, apply a regex to the string a extract every
    # number in the string. Then, replace in the string each
    # extracted number by himself, but formatted with thousands
    # separators.

    text = str(text)  # make sure it's a string
    __numbers = []
    __regex = r'[\d]+[.\d]+|[\d]*[.][\d]+|[\d]+'
    if re.search(__regex, text) is not None:
        for catch in re.finditer(__regex, text):
            __numbers += [catch[0]]
    for number in __numbers:
        if number.isnumeric():
            text = text.replace(str(number), f"{int(number):,}")
        else:
            try:
                text = text.replace(str(number), f"{float(number):,}")
            except Exception as err:
                pass
    return text


def format_string_color(text: str) -> str:
    # First, we go through each character in the
    # string and find out if it's the beginning of
    # a RGB ANSI color code. If it does, save the gotten
    # number to a list index.
    # Then, depending on the user's terminal color system,
    # fix the color so that it can be displayed.

    __color_codes = []
    __color_system = get_terminal_color_system()
    text = str(text)  # make sure it's a string
    count = 0
    for character in text:
        try:
            if text[count:].startswith(r'[38;2'):
                __color_codes += [text[count:].split("m", 1)[0]]
        except Exception as error:
            continue
        count += 1

    for color in __color_codes:
        color_rgb = get_color_rgb(color)
        matchings = {}

        # If the user's terminal color system is either 'standard' or '256',
        # find the closest standard color to the original color, and replace
        # it, so it's compatible
        if __color_system == "standard" or __color_system == "256":
            for match in STANDARD_COLORS:
                # Get the match rgb code, and then compare it with the
                # original color code. Store that 'matching score' into
                # a dictionary
                match_rgb = get_color_rgb(match)

                red_difference = abs(color_rgb[0] - match_rgb[0])  # make it positive
                green_difference = abs(color_rgb[1] - match_rgb[1])  # make it positive
                blue_difference = abs(color_rgb[2] - match_rgb[2])  # make it positive
                matchings[match] = red_difference + green_difference + blue_difference
        # Elif the user's using legacy windows terminal, find the closest standard color
        # to the original color, and replace it, so it's compatible
        elif __color_system == "windows":
            for match in LEGACY_COLORS:
                # Get the match rgb code, and then compare it with the
                # original color code. Store that 'matching score' into
                # a dictionary
                match_rgb = get_color_rgb(match)

                red_difference = abs(color_rgb[0] - match_rgb[0])  # make it positive
                green_difference = abs(color_rgb[1] - match_rgb[1])  # make it positive
                blue_difference = abs(color_rgb[2] - match_rgb[2])  # make it positive
                matchings[match] = red_difference + green_difference + blue_difference
        # If the user's using a truecolor terminal color system,
        # skip the replace process
        else:
            matchings[color] = 1

        if __color_system != "truecolor":
            closest_matching = min(matchings, key=matchings.get)
            text = text.replace(
                color + "m", STANDARD_COLORS[
                    list(matchings.keys()).index(closest_matching)
                ]
            )

    return text


def get_color_rgb(color_code: str) -> list:
    color_r = int(color_code.split("38;2;", 1)[1].split(";", 1)[0])
    color_g = int(color_code.split("38;2;", 1)[1].split(";", 2)[1])
    color_b = int(color_code.split("38;2;", 1)[1].split(";", 2)[2].replace("m", ""))

    return [color_r, color_g, color_b]


def get_size() -> tuple:
    return os.get_terminal_size()


def get_terminal_color_system() -> str:
    return Console().color_system
