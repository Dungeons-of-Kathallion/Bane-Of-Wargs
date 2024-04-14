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
    generic_text_replacements, plugin=False
):
    with open(
        program_dir + '/temp/scripts/' + script_data["script name"]
    ) as f:
        execute_script(
            script_data, f, player, map, item, drinks, enemy, npcs,
            start_player, lists, zone, dialog, mission, mounts, start_time,
            generic_text_replacements, preferences
        )


def execute_script(
    script_data, file, player, map, item, drinks, enemy, npcs,
    start_player, lists, zone, dialog, mission, mounts, start_time,
    generic_text_replacements, preferences
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
        if "player" in arguments:
            global_arguments["player"] = player
        if "map" in arguments:
            global_arguments["map"] = map
        if "item" in arguments:
            global_arguments["item"] = item
        if "drinks" in arguments:
            global_arguments["drinks"] = drinks
        if "enemy" in arguments:
            global_arguments["enemy"] = enemy
        if "npcs" in arguments:
            global_arguments["npcs"] = npcs
        if "start_player" in arguments:
            global_arguments["start_player"] = start_player
        if "lists" in arguments:
            global_arguments["lists"] = lists
        if "zone" in arguments:
            global_arguments["zone"] = zone
        if "dialog" in arguments:
            global_arguments["dialog"] = dialog
        if "mission" in arguments:
            global_arguments["mission"] = mission
        if "mounts" in arguments:
            global_arguments["mounts"] = mounts
        if "start_time" in arguments:
            global_arguments["start_time"] = start_time
        if "generic_text_replacements" in arguments:
            global_arguments["generic_text_replacements"] = generic_text_replacements
        if "preferences" in arguments:
            global_arguments["preferences"] = preferences
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
