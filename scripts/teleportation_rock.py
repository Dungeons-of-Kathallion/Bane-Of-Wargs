# teleportation_rock.py
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

import time
import text_handling
from terminal_handling import cout, cinput

def teleportation_action(player, map):
    cout(" ")
    text_handling.print_separator("=")
    try:
        which_coordinates_x = int(cinput("Where would you like to be at x?\n"))
        which_coordinates_y = int(cinput("Where would you like to be at y?\n"))
        # Here we consider that the player will enter a correct input`, because this is an example

        # Check if a map point exists at player wish coordinates
        point_exists = False
        for i in list(map):
            if map[i]["x"] == which_coordinates_x and map[i]["y"] == which_coordinates_y:
                point_exists = True

        # Run the teleportation action
        if point_exists:
            cout("Teleporting...")
            time.sleep(5)
            player["x"], player["y"] = which_coordinates_x, which_coordinates_y
            cout("Teleported!")
        else:
            cout(f"Where you want to go does not exists...")
    except Exception as error:
        cout("Please enter integers as coordinates")
    text_handling.print_separator("=")

# Actually run the action, and tells the game which arguments to use
teleportation_action(player, map)
