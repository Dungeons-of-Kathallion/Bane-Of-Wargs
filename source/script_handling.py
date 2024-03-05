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
    if plugin:
        with open(
            program_dir + '/plugins/' + preferences["latest preset"]["plugin"] +
            '/scripts/' + script_data["script name"]
        ) as f:
            execute_script(
                script_data, f, player, map, item, drinks, enemy, npcs,
                start_player, lists, zone, dialog, mission, mounts, start_time,
                generic_text_replacements
            )
    else:
        with open(
            program_dir + '/game/scripts/' + script_data["script name"]
        ) as f:
            execute_script(
                script_data, f, player, map, item, drinks, enemy, npcs,
                start_player, lists, zone, dialog, mission, mounts, start_time,
                generic_text_replacements
            )


def execute_script(
    script_data, file, player, map, item, drinks, enemy, npcs,
    start_player, lists, zone, dialog, mission, mounts, start_time,
    generic_text_replacements
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
    arguments_list = list(global_arguments)
    logger_sys.log_message(
        f"INFO: Loaded script '{file}' required arguments:\n{arguments_list}"
    )
    logger_sys.log_message(
        f"INFO: Executing script '{file}' with arguments '{global_arguments}'"
    )
    try:
        exec(file.read(), global_arguments)
    except Exception as error:
        cout(COLOR_RED + "ERROR: " + COLOR_STYLE_BRIGHT + str(error) + COLOR_RESET_ALL)
        logger_sys.log_message(
            f"ERROR: An error occurred when executing script '{file}' " +
            f"'with arguments '{global_arguments}'"
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
