import logger_sys
import text_handling
import appdirs
import sys
import time
import random
from colorama import Fore, Back, Style, deinit, init
from colors import *

# Initialize colorama
init()

# Get program directory
program_dir = str(appdirs.user_config_dir(appname='Bane-Of-Wargs'))

# Functions to handle dialogs


def print_dialog(current_dialog, dialog, preferences, text_replacements_generic, player, drinks):
    current_dialog_name = current_dialog
    logger_sys.log_message(f"INFO: Printing dialog '{current_dialog_name}'")
    current_dialog = dialog[str(current_dialog)]
    dialog_len = len(current_dialog["phrases"])
    if "scene" in current_dialog:
        current_dialog_scene = str(current_dialog["scene"])
        logger_sys.log_message(
            f"INFO: Printing dialog '{
                current_dialog_name
            }' scene at '{program_dir}/game/imgs/{current_dialog_scene}.txt'"
        )
        if preferences["latest preset"]["type"] == 'vanilla':
            with open(program_dir + '/game/imgs/' + str(current_dialog["scene"]) + '.txt') as f:
                to_print = str(f.read())
                to_print = to_print.replace('$RED', '\033[0;31m')
                to_print = to_print.replace('$GREEN', '\033[0;32m')
                to_print = to_print.replace('$YELLOW', '\033[0;33m')
                to_print = to_print.replace('$BLUE', '\033[0;34m')
                to_print = to_print.replace('$PURPLE', '\033[0;34m')
                to_print = to_print.replace('$CYAN', '\033[0;36m')
                to_print = to_print.replace('$WHITE', '\033[0;37m')
                to_print = to_print.replace('$BLACK', '\033[0;30m')
                to_print = to_print.replace('$BROWN', '\033[0;33m')
                to_print = to_print.replace('$GRAY', '\033[1;30m')
                print(to_print)
        else:
            current_plugin = str(preferences["latest preset"]["plugin"])
            logger_sys.log_message(
                f"INFO: Printing dialog '{
                    current_dialog_name
                }' scene at '{program_dir}/plugins/{current_plugin}/imgs/{current_dialog_scene}.txt'"
            )
            with open(
                program_dir + '/plugins/' + str(preferences["latest preset"]["plugin"]) +
                '/imgs/' + str(current_dialog["scene"]) + '.txt'
            ) as f:
                to_print = str(f.read())
                to_print = to_print.replace('$RED', '\033[0;31m')
                to_print = to_print.replace('$GREEN', '\033[0;32m')
                to_print = to_print.replace('$YELLOW', '\033[0;33m')
                to_print = to_print.replace('$BLUE', '\033[0;34m')
                to_print = to_print.replace('$PURPLE', '\033[0;34m')
                to_print = to_print.replace('$CYAN', '\033[0;36m')
                to_print = to_print.replace('$WHITE', '\033[0;37m')
                to_print = to_print.replace('$BLACK', '\033[0;30m')
                to_print = to_print.replace('$BROWN', '\033[0;33m')
                to_print = to_print.replace('$GRAY', '\033[1;30m')
                print(to_print)
    count = 0
    logger_sys.log_message(f"INFO: Printing dialog '{current_dialog_name}' phrases")
    while count < dialog_len:
        text = str(current_dialog["phrases"][int(count)])
        count = 0
        while count < len(list(text_replacements_generic)):
            current_text_replacement = str(list(text_replacements_generic)[count])
            text = text.replace(current_text_replacement, str(text_replacements_generic[current_text_replacement]))
            count += 1
        text_handling.print_speech_text_effect(text, preferences)
        count += 1
    if current_dialog["use actions"]:
        logger_sys.log_message(f"INFO: Executing dialog '{current_dialog_name}' actions on the player")
        actions = current_dialog["actions"]
        if "give item" in actions:
            given_items = actions["give item"]
            given_items_len = len(given_items)
            count = 0
            logger_sys.log_message(f"INFO: Giving to the player items '{given_items}'")
            while count < given_items_len:
                selected_item = given_items[count]
                player["inventory"].append(selected_item)
                count += 1
        if "add attributes" in actions:
            count = 0
            added_attributes = actions["add attributes"]
            added_attributes_len = len(added_attributes)
            logger_sys.log_message(f"INFO: Adding attributes '{added_attributes}' to the player")
            while count < added_attributes_len:
                selected_attribute = added_attributes[count]
                player["attributes"].append(selected_attribute)
                count += 1
        if "health modification" in actions:
            if "diminution" in actions["health modification"]:
                logger_sys.log_message(
                    "INFO: Removing " + actions["health modification"]["diminution"] +
                    " hp from the player's health"
                )
                player["health"] -= actions["health modification"]["diminution"]
            if "augmentation" in actions["health modification"]:
                logger_sys.log_message(
                    "INFO: Adding " + actions["health modification"]["augmentation"] +
                    " hp from the player's health"
                )
                player["health"] += actions["health modification"]["augmentation"]
            if "max health" in actions["health modification"]:
                if "diminution" in actions["health modification"]["max health"]:
                    logger_sys.log_message(
                        "INFO: Removing " + actions["health modification"]["max health"]["diminution"] +
                        " hp from the player's max health"
                        )
                    player["max health"] -= actions["health modification"]["max health"]["diminution"]
                if "augmentation" in actions["health modification"]["max health"]:
                    logger_sys.log_message(
                        "INFO: Adding " + actions["health modification"]["max health"]["augmentation"] +
                        " hp from the player's max health"
                        )
                    player["max health"] += actions["health modification"]["max health"]["augmentation"]
        if "gold modification" in actions:
            if "diminution" in actions["gold modification"]:
                logger_sys.log_message("INFO: Removing " + actions["gold modification"]["diminution"] + " gold to the player")
                player["gold"] -= actions["gold modification"]["diminution"]
            if "augmentation" in actions["gold modification"]:
                logger_sys.log_message("INFO: Adding " + actions["gold modification"]["diminution"] + " gold to the player")
                player["gold"] += actions["gold modification"]["augmentation"]
        if "remove item" in actions:
            removed_items = actions["remove item"]
            removed_items_len = len(removed_items)
            count = 0
            logger_sys.log_message(f"INFO: Removing items '{removed_items}' from player's inventory")
            while count < removed_items_len:
                selected_item = removed_items[count]
                player["inventory"].remove(selected_item)
                count += 1
        if "add to diary" in actions:
            if "known zones" in actions["add to diary"]:
                added_visited_zones = actions["add to diary"]["known zones"]
                added_visited_zones_len = len(added_visited_zones)
                count = 0
                logger_sys.log_message(f"INFO: Adding zones '{added_visited_zones}' to player's visited zones")
                while count < added_visited_zones_len:
                    selected_zone = added_visited_zones[count]
                    player["visited zones"].append(selected_zone)
                    count += 1
            if "known enemies" in actions["add to diary"]:
                added_known_enemies = actions["add to diary"]["known enemies"]
                added_known_enemies_len = len(added_known_enemies)
                count = 0
                logger_sys.log_message(f"INFO: Adding enemies '{added_known_enemies}' to player's known enemies")
                while count < added_known_enemies_len:
                    selected_enemy = added_known_enemies[count]
                    player["enemies list"].append(selected_enemy)
                    count += 1
            if "known npcs" in actions["add to diary"]:
                added_known_npcs = actions["add to diary"]["known npcs"]
                added_known_npcs_len = len(added_known_npcs)
                count = 0
                logger_sys.log_message(f"INFO: Adding npcs '{added_known_npcs}' to player's known npcs")
                while count < added_known_npcs_len:
                    selected_npc = added_known_npcs[count]
                    player["met npcs name"].append(selected_npc)
                    count += 1
        if "remove to diary" in actions:
            if "known zones" in actions["remove to diary"]:
                removed_visited_zones = actions["remove to diary"]["known zones"]
                removed_visited_zones_len = len(removed_visited_zones)
                count = 0
                logger_sys.log_message(f"INFO: Removing zones '{added_visited_zones}' to player's visited zones")
                while count < removed_visited_zones_len:
                    selected_zone = removed_visited_zones[count]
                    player["visited zones"].remove(selected_zone)
                    count += 1
            if "known enemies" in actions["remove to diary"]:
                removed_known_enemies = actions["remove to diary"]["known enemies"]
                removed_known_enemies_len = len(removed_known_enemies)
                count = 0
                logger_sys.log_message(f"INFO: Removing enemies '{added_known_enemies}' to player's known enemies")
                while count < removed_known_enemies_len:
                    selected_enemy = removed_known_npcs[count]
                    player["enemies list"].remove(selected_enemy)
                    count += 1
            if "known npcs" in actions["remove to diary"]:
                removed_known_npcs = actions["remove to diary"]["known npcs"]
                removed_known_npcs_len = len(removed_known_npcs)
                count = 0
                logger_sys.log_message(f"INFO: Removing npcs '{added_known_npcs}' to player's known npcs")
                while count < removed_known_npcs_len:
                    selected_npc = removed_known_npcs[count]
                    player["met npcs name"].append(selected_npc)
                    count += 1
        if "use drink" in actions:
            used_drinks = actions["use drink"]
            used_drinks_len = len(used_drinks)
            count = 0
            logger_sys.log_message(f"INFO: Using drinks '{used_drinks}'")
            while count < used_drinks_len:
                selected_drink = used_drinks_len[count]
                if drinks[selected_drink]["healing level"] == 999:
                    player["health"] = player["max health"]
                else:
                    player["health"] += drinks[selected_drink]["healing level"]


# Deinitialize colorama
deinit()
