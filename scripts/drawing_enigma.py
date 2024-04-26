# drawing_enigma.py
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
import appdirs
import time
import text_handling
import terminal_handling
from colors import *
from terminal_handling import cout, cinput


# Handling functions
program_dir = str(appdirs.user_config_dir(appname='Bane-Of-Wargs'))


def run(enemy, player, preferences):
    completed = False

    chosen_enemy = ""
    while chosen_enemy not in player["enemies list"]:
        chosen_enemy = list(enemy)[
            random.randint(0, len(list(enemy))) - 1
        ]
    chosen_enemy_data = enemy[chosen_enemy]

    options = [chosen_enemy]
    count = 0
    while count < 4:
        random_enemy = list(enemy)[random.randint(0, len(list(enemy)) - 1)]
        if random_enemy not in options:
            options += [random_enemy]
            count += 1
    random.shuffle(options)

    while not completed:
        text_handling.clear_prompt()
        text_handling.print_enemy_thumbnail(chosen_enemy, preferences)
        cout(f"\n{COLOR_STYLE_BRIGHT}Which enemy is this?{COLOR_RESET_ALL}")

        choice = terminal_handling.show_menu(options)
        if choice == chosen_enemy:
            cout(f"\n{COLOR_CYAN}Right answer!{COLOR_RESET_ALL}")
            completed = True
            return completed
        else:
            cout(f"\n{COLOR_YELLOW}Wrong answer!{COLOR_RESET_ALL}")
            time.sleep(2)


# Actually run the action, and tells the game which arguments to use
run(enemy, player, preferences)
