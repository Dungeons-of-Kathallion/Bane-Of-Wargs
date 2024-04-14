# health_generator.py
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
from colors import *
from terminal_handling import cout, cinput


def dialog_action(player):
    print(" ")
    text_handling.print_separator("=")
    how_many_exp = cinput("How many exp would you like to spend?\n")
    # Check if the player entered a number
    try:
        how_many_exp = float(how_many_exp)

        # First, check that the player has the experience that he said, then
        # if the player has enough experience, we
        if player["xp"] < how_many_exp:
            cout(COLOR_YELLOW + "You don't have enough experience for this action!" + COLOR_RESET_ALL)
        else:
            player["xp"] -= how_many_exp
            health_regeneration = round(how_many_exp / round(random.uniform(2.8, 4.3), 2))
            player["health"] += health_regeneration
    except Exception as error:
        cout("Please enter a number")

    text_handling.print_separator("=")

# Actually run the action, and tells the game which arguments to use
dialog_action(player)
