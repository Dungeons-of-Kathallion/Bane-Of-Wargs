# player_handling.py
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
import logger_sys
import yaml_handling
import text_handling
from terminal_handling import cout
from colors import *
# external imports
import time
import appdirs
from sys import exit


# Handling Functions
program_dir = str(appdirs.user_config_dir(appname='Bane-Of-Wargs'))


def player_death(preferences, save_file):
    text = "You just died and your save has been rested to its older state."
    logger_sys.log_message("INFO: Player just died")
    cout(COLOR_RED + COLOR_STYLE_BRIGHT, end="")
    text_handling.print_long_string(text)
    cout(COLOR_RESET_ALL, end="")
    time.sleep(3)
    logger_sys.log_message("INFO: Resetting player save")
    with open(save_file, "r") as f:
        player = yaml_handling.safe_load(f)
    dumped = yaml_handling.dump(player)
    logger_sys.log_message(f"INFO: Dumping player save data: '{dumped}'")

    save_file_quit = save_file
    with open(save_file_quit, "w") as f:
        f.write(dumped)
    logger_sys.log_message(f"INFO: Dumping player save data to save '{save_file_quit}'")

    dumped = yaml_handling.dump(preferences)
    logger_sys.log_message(f"INFO: Dumping player preferences data: '{dumped}'")

    with open(program_dir + '/preferences.yaml', 'w') as f:
        f.write(dumped)
    logger_sys.log_message(f"INFO: Dumping player preferences to file '" + program_dir + "/preferences.yaml'")
    text_handling.clear_prompt()
    logger_sys.log_message("INFO: PROGRAM RUN END")
    exit(0)
