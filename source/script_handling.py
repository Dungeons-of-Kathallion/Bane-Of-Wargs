# script_handling.py
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
from colors import *
from terminal_handling import cout
# external imports
import appdirs
import time
import subprocess


# Load program directory
program_dir = str(appdirs.user_config_dir(appname='Bane-Of-Wargs'))


# Handling Functions

def load_script(
    script_data, preferences, player, map, item, drinks, enemy, npcs,
    start_player, lists, zone, dialog, mission, mounts, start_time,
    generic_text_replacements, save_file, player_damage_coefficient,
    enemies_damage_coefficient, previous_player, plugin=False
):
    with open(
        program_dir + '/temp/scripts/' + script_data["script name"]
    ) as f:
        execute_script(
            script_data, f, player, map, item, drinks, enemy, npcs,
            start_player, lists, zone, dialog, mission, mounts, start_time,
            generic_text_replacements, preferences, save_file,
            player_damage_coefficient, enemies_damage_coefficient,
            previous_player
        )


def execute_script(
    script_data, file, player, map, item, drinks, enemy, npcs,
    start_player, lists, zone, dialog, mission, mounts, start_time,
    generic_text_replacements, preferences, save_file,
    player_damage_coefficient, enemies_damage_coefficient,
    previous_player
):
    logger_sys.log_message(
        f"INFO: Starting execution process of script '{file}'"
    )
    global_arguments = {}
    logger_sys.log_message(
        f"INFO: Loading script '{file}' required arguments"
    )
    if "arguments" in script_data:
        arguments = script_data['arguments']
        count = 0
        for argument in arguments:
            argument_variable = None
            succeeded = True
            if argument == "player":
                argument_variable = player
            elif argument == "map":
                argument_variable = map
            elif argument == "item":
                argument_variable = item
            elif argument == "drinks":
                argument_variable = drinks
            elif argument == "enemy":
                argument_variable = enemy
            elif argument == "npcs":
                argument_variable = npcs
            elif argument == "start_player":
                argument_variable = start_player
            elif argument == "lists":
                argument_variable = lists
            elif argument == "zone":
                argument_variable = zone
            elif argument == "dialog":
                argument_variable = dialog
            elif argument == "mission":
                argument_variable = mission
            elif argument == "mounts":
                argument_variable = mounts
            elif argument == "start_time":
                argument_variable = start_time
            elif argument == "generic_text_replacements":
                argument_variable = generic_text_replacements
            elif argument == "preferences":
                argument_variable = preferences
            elif argument == "map_location":
                argument_variable = search(player["x"], player["y"], map)
            elif argument == "save_file":
                argument_variable = save_file
            elif argument == "previous_player":
                argument_variable = previous_player
            elif argument == "player_damage_coefficient":
                argument_variable = player_damage_coefficient
            elif argument == "enemies_damage_coefficient":
                argument_variable = enemies_damage_coefficient
            elif type(argument) is type({}):  # if it's a custom set variable
                argument_variable = argument[list(arguments[count])[0]]
                argument = list(arguments[count])[0]
            else:
                succeeded = False

            if succeeded:
                global_arguments[str(argument)] = argument_variable
            count += 1
    arguments_list = list(global_arguments)
    logger_sys.log_message(
        f"INFO: Loaded script '{file}' required arguments:\n{arguments_list}"
    )
    logger_sys.log_message(
        f"INFO: Executing script '{file}' with arguments '{arguments_list}'"
    )
    try:
        exec(file.read(), global_arguments)
    except Exception as error:
        cout(COLOR_RED + "ERROR: " + COLOR_STYLE_BRIGHT + str(error) + COLOR_RESET_ALL)
        logger_sys.log_message(
            f"ERROR: An error occurred when executing script '{file}' " +
            f"'with arguments '{arguments_list}'"
        )
        logger_sys.log_message(f"DEBUG: error message --> '{error}'")
        time.sleep(5)


def install_requirement(module):
    # Determine is the user python command
    # is either 'python' or either 'python3',
    # then install the input module using that
    # determined command sooner
    executable = "python"
    try:
        subprocess.check_call(
            ["python", "-V"],
            stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT
        )
    except Exception as error:
        executable = "python3"

    retcode = subprocess.check_call(
        [executable, "-m", "pip", "install", module],
        stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT
    )


def search(x, y, map):
    logger_sys.log_message(f"INFO: Searching for map point corresponding to coordinates x:{x}, y:{y}")
    global map_location
    map_point_count = int(len(list(map)))
    for i in range(0, map_point_count):
        point_i = map["point" + str(i)]
        point_x, point_y = point_i["x"], point_i["y"]
        if point_x == x and point_y == y:
            map_location = i
            return map_location
