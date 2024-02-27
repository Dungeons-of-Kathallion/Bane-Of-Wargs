import logger_sys
import appdirs
import colors
import time
from colorama import Fore, Back, Style, init, deinit
from colors import *

# initialize colorama
init()

# Load program directory
program_dir = str(appdirs.user_config_dir(appname='Bane-Of-Wargs'))


# Handling Functions

def load_script(
    current_utility, preferences, player, map, item, drinks, enemy, npcs,
    start_player, lists, zone, dialog, mission, mounts, start_time,
    generic_text_replacements, plugin=False
):
    logger_sys.log_message(f"INFO: Player is using utility item '{current_utility}'")
    if plugin:
        with open(
            program_dir + '/plugins/' + preferences["latest preset"]["plugin"] +
            '/scripts/' + item[current_utility]["script name"]
        ) as f:
            execute_script(
                f, current_utility, player, map, item, drinks, enemy, npcs,
                start_player, lists, zone, dialog, mission, mounts, start_time,
                generic_text_replacements
            )
    else:
        with open(
            program_dir + '/game/scripts/' + item[current_utility]["script name"]
        ) as f:
            execute_script(
                f, current_utility, player, map, item, drinks, enemy, npcs,
                start_player, lists, zone, dialog, mission, mounts, start_time,
                generic_text_replacements
            )


def execute_script(
    file, current_utility, player, map, item, drinks, enemy, npcs,
    start_player, lists, zone, dialog, mission, mounts, start_time,
    generic_text_replacements
):
    global_arguments = {}
    if "arguments" in item[current_utility]:
        arguments = item[current_utility]['arguments']
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
    try:
        exec(file.read(), global_arguments)
    except Exception as error:
        print(COLOR_RED + "ERROR: " + COLOR_STYLE_BRIGHT + error + COLOR_RESET_ALL)
        time.sleep(5)


# deinitialize colorama
deinit()
