# levers_enigma.py
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

import random
import text_handling
import terminal_handling
import time
from colors import *
from terminal_handling import cout, cinput


def print_scene(levers):
    lines = ""
    if levers["lever 1"] and levers["lever 2"] and levers["lever 3"]:
        lines += "\n\n"
        lines += "    ######    ######    ######\n"
        lines += "    #%%%##    #%%%##    #%%%##\n"
        lines += "    ##%%%#    ##%%%#    ##%%%#\n"
        lines += "    ###%%%    ###%%%    ###%%%\n"
        lines += "        %%%       %%%       %%%\n"
        lines += "        [II]      [II]      [II]"
    elif levers["lever 1"] and levers["lever 2"] and not levers["lever 3"]:
        lines += "                            [II]\n"
        lines += "                            %%%\n"
        lines += "    ######    ######    ###%%%\n"
        lines += "    #%%%##    #%%%##    ##%%%#\n"
        lines += "    ##%%%#    ##%%%#    #%%%##\n"
        lines += "    ###%%%    ###%%%    ######\n"
        lines += "        %%%       %%%\n"
        lines += "        [II]      [II]"
    elif levers["lever 1"] and not levers["lever 2"] and not levers["lever 3"]:
        lines += "                  [II]      [II]\n"
        lines += "                  %%%       %%%\n"
        lines += "    ######    ###%%%    ###%%%\n"
        lines += "    #%%%##    ##%%%#    ##%%%#\n"
        lines += "    ##%%%#    #%%%##    #%%%##\n"
        lines += "    ###%%%    ######    ######\n"
        lines += "        %%%\n"
        lines += "        [II]"
    elif levers["lever 1"] and not levers["lever 2"] and levers["lever 3"]:
        lines += "                  [II]\n"
        lines += "                  %%%\n"
        lines += "    ######    ###%%%    ######\n"
        lines += "    #%%%##    ##%%%#    #%%%##\n"
        lines += "    ##%%%#    #%%%##    ##%%%#\n"
        lines += "    ###%%%    ######    ###%%%\n"
        lines += "        %%%                 %%%\n"
        lines += "        [II]                [II]"
    elif not levers["lever 1"] and levers["lever 2"] and levers["lever 3"]:
        lines += "        [II]\n"
        lines += "        %%%\n"
        lines += "    ###%%%    ######    ######\n"
        lines += "    ##%%%#    #%%%##    #%%%##\n"
        lines += "    #%%%##    ##%%%#    ##%%%#\n"
        lines += "    ######    ###%%%    ###%%%\n"
        lines += "                  %%%       %%%\n"
        lines += "                  [II]      [II]"
    elif not levers["lever 1"] and levers["lever 2"] and not levers["lever 3"]:
        lines += "        [II]                [II]\n"
        lines += "        %%%                 %%%\n"
        lines += "    ###%%%    ######    ###%%%\n"
        lines += "    ##%%%#    #%%%##    ##%%%#\n"
        lines += "    #%%%##    ##%%%#    #%%%##\n"
        lines += "    ######    ###%%%    ######\n"
        lines += "                  %%%\n"
        lines += "                  [II]"
    elif not levers["lever 1"] and not levers["lever 2"] and levers["lever 3"]:
        lines += "        [II]      [II]\n"
        lines += "        %%%       %%%\n"
        lines += "    ###%%%    ###%%%    ######\n"
        lines += "    ##%%%#    ##%%%#    #%%%##\n"
        lines += "    #%%%##    #%%%##    ##%%%#\n"
        lines += "    ######    ######    ###%%%\n"
        lines += "                            %%%\n"
        lines += "                            [II]"
    elif not levers["lever 1"] and not levers["lever 2"] and not levers["lever 3"]:
        lines += "        [II]      [II]      [II]\n"
        lines += "        %%%       %%%       %%%\n"
        lines += "    ###%%%    ###%%%    ###%%%\n"
        lines += "    ##%%%#    ##%%%#    ##%%%#\n"
        lines += "    #%%%##    #%%%##    #%%%##\n"
        lines += "    ######    ######    ######"
        lines += "\n"
    lines = lines.replace("#", COLOR_GRAY_4 + "#")
    lines = lines.replace("%", COLOR_CYAN + "/")
    lines = lines.replace("[II]", COLOR_WHITE + "[" + COLOR_YELLOW + "II" + COLOR_WHITE + "]")
    cout(lines + COLOR_RESET_ALL)


def run():
    completed = False
    levers = {
        "lever 1": True,
        "lever 2": False,
        "lever 3": False
    }
    while not completed:
        text_handling.clear_prompt()
        text_handling.print_separator("=")
        print_scene(levers)
        text_handling.print_separator("=")
        cout()

        if not levers["lever 1"] and levers["lever 2"] and not levers["lever 3"]:
            completed = True
            cout(f"\n{COLOR_CYAN}You completed the enigma! You pass the room.{COLOR_RESET_ALL}")
            time.sleep(3)
            return True

        options = ['Switch Lever 1', 'Switch Lever 2', 'Switch Lever 3']
        action = terminal_handling.show_menu(options)
        if action == options[0]:
            if levers["lever 1"]:
                levers["lever 1"] = False
            else:
                levers["lever 1"] = True
        elif action == options[1]:
            if levers["lever 2"]:
                levers["lever 2"] = False
            else:
                levers["lever 2"] = True
        elif action == options[2]:
            if levers["lever 3"]:
                levers["lever 3"] = False
            else:
                levers["lever 3"] = True


# Actually run the action, and tells the game which arguments to use
run()
