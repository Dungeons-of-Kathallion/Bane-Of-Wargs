# source imports
import logger_sys
import text_handling
import terminal_handling.py
from colors import *


# Handling functions
def init_npc(map_location, player, npcs, drinks, item, preferences, map):
    current_npc = str(map["point" + str(map_location)]["npc"])
    logger_sys.log_message(f"INFO: Current map point 'point{map_location}' has npc: '{current_npc}'")
    current_npc = current_npc.replace('[', '')
    current_npc = current_npc.replace(']', '')
    current_npc = current_npc.replace("'", '')
    logger_sys.log_message(f"INFO: Adding npc '{current_npc}' to player 'met npcs' and 'met npcs names' save attributes")
    player["met npcs"].append(map_location)
    player["met npcs names"].append(str(npcs[current_npc]["name"]))
    print(" ")
    text = '='
    text_handling.print_separator(text)
    print(str(npcs[current_npc]["name"]) + ":")
    text = '='
    text_handling.print_separator(text)
    count = 0
    npc_speech = npcs[current_npc]["speech"]
    npc_speech_len = len(npc_speech)
    logger_sys.log_message(f"INFO: Printing npc '{current_npc}' dialog")
    while count < npc_speech_len:
        text = str(npcs[current_npc]["speech"][int(count)])
        text_handling.print_speech_text_effect(text, preferences)
        count += 1
    text = '='
    text_handling.print_separator(text)
    options = []
    logger_sys.log_message(f"INFO: Display npc '{current_npc}' information to GUI")
    if "None" not in npcs[current_npc]["sells"]["drinks"]:
        print("DRINKS SELLS:")
        count = 0
        npc_drinks = npcs[current_npc]["sells"]["drinks"]
        npc_drinks_len = len(npc_drinks)
        while count < npc_drinks_len:
            current_drink = str(npcs[current_npc]["sells"]["drinks"][int(count)])
            print(
                " -" + npcs[current_npc]["sells"]["drinks"][int(count)] + " " +
                COLOR_YELLOW + COLOR_STYLE_BRIGHT +
                str(round(drinks[current_drink]["gold"] * npcs[current_npc]["cost value"], 2)) +
                COLOR_RESET_ALL
            )
            count += 1
        options += ['Buy Drink']
    if "None" not in npcs[current_npc]["sells"]["items"]:
        print("ITEMS SELLS")
        count = 0
        npc_items = npcs[current_npc]["sells"]["items"]
        npc_items_len = len(npc_items)
        while count < npc_items_len:
            current_item = str(npcs[current_npc]["sells"]["items"][int(count)])
            print(
                " -" + npcs[current_npc]["sells"]["items"][int(count)] + " " + COLOR_YELLOW +
                COLOR_STYLE_BRIGHT + str(round(item[current_item]["gold"] * npcs[current_npc]["cost value"], 2)) +
                COLOR_RESET_ALL
            )
            count += 1
        options += ['Buy Item']
    if "None" not in npcs[current_npc]["buys"]["items"]:
        print("ITEMS BUYS:")
        count = 0
        npc_items = npcs[current_npc]["buys"]["items"]
        npc_items_len = len(npc_items)
        while count < npc_items_len:
            current_item = str(npcs[current_npc]["buys"]["items"][int(count)])
            print(
                " -" + npcs[current_npc]["buys"]["items"][int(count)] + " " + COLOR_YELLOW +
                COLOR_STYLE_BRIGHT + str(round(item[current_item]["gold"] * npcs[current_npc]["cost value"], 2)) +
                COLOR_RESET_ALL
            )
            count += 1
        options += ['Sell Item']
    options += ['Exit']
    text = '='
    text_handling.print_separator(text)
    p = True
    while p:
        logger_sys.log_message(f"INFO: Starting player interaction with npc '{current_npc}'")
        choice = terminal_handling.py.show_menu(options)
        if choice == 'Buy Drink':
            which_drink = input("Which drink do you want to buy from him? ")
            if (
                which_drink in npcs[current_npc]["sells"]["drinks"]
                and (drinks[which_drink]["gold"] * npcs[current_npc]["cost value"]) < player["gold"]
            ):
                logger_sys.log_message(
                    f"INFO: Player bought drink '{which_drink}' from npc '{current_npc}', causing the player to loose " +
                    str(drinks[which_drink]["gold"] * npcs[current_npc]["cost value"]) + " gold"
                )
                player["gold"] -= drinks[which_drink]["gold"] * npcs[current_npc]["cost value"]
                if drinks[which_drink]["healing level"] == 999:
                    player["health"] = player["max health"]
                else:
                    player["health"] += drinks[which_drink]["healing level"]
            else:
                text = (
                    COLOR_YELLOW + "You cannot buy that items because it would cause your gold to be negative." +
                    COLOR_RESET_ALL
                )
                text_handling.print_long_string(text)
        elif choice == 'Buy Item':
            which_item = input("Which item do you want to buy from him? ")
            if (
                which_item in npcs[current_npc]["sells"]["items"]
                and (item[which_item]["gold"] * npcs[current_npc]["cost value"]) < player["gold"]
            ):
                if player["inventory slots remaining"] > 0:
                    logger_sys.log_message(
                        f"INFO: Player bought item '{which_item}' from npc '{current_npc}', causing him, to loose " + str(
                            item[which_item]["gold"] * npcs[current_npc]["cost value"]
                        ) + " gold"
                    )
                    player["inventory slots remaining"] -= 1
                    player["inventory"].append(which_item)
                    player["gold"] -= item[which_item]["gold"] * npcs[current_npc]["cost value"]
                else:
                    text = (
                        COLOR_YELLOW + "You cannot buy that items because it would cause your inventory slots to be negative." +
                        COLOR_RESET_ALL
                    )
                    text_handling.print_long_string(text)
            else:
                text = (
                    COLOR_YELLOW + "You cannot buy that items because it would cause your gold to be negative." +
                    COLOR_RESET_ALL
                )
                text_handling.print_long_string(text)
        elif choice == 'Sell Item':
            which_item = input("Which item do you want to sell him? ")
            if (
                which_item in npcs[current_npc]["buys"]["items"]
                and (item[which_item]["gold"] * npcs[current_npc]["cost value"]) < player["gold"]
                and which_item in player["inventory"]
            ):
                logger_sys.log_message(
                    "INFO: Player has sold item '{witch_item}' to npc '{current_npc}' for " +
                    str(item[which_item]["gold"] * npcs[current_npc]["cost value"]) + " gold"
                )
                player["inventory slots remaining"] -= 1
                player["gold"] += item[which_item]["gold"] * npcs[current_npc]["cost value"]
                player["inventory"].remove(which_item)
                which_item_number_inventory = 0
                count = 0
                p = True
                while p:
                    if count >= len(player["inventory"]) + 1:
                        p = False
                    else:
                        selected_item = player["inventory"][count - 1]
                        if str(selected_item) == str(which_item):
                            which_item_number_inventory += 1
                    count += 1
                if which_item_number_inventory <= 1:
                    logger_sys.log_message("INFO: Checking if player sold item was equipped")
                    if which_item == player["held item"]:
                        player["held item"] = " "
                    if which_item == player["held chestplate"]:
                        player["held chestplate"] = " "
                    if which_item == player["held boots"]:
                        player["held boots"] = " "
                    if which_item == player["held leggings"]:
                        player["held leggings"] = " "
                    if which_item == player["held shield"]:
                        player["held shield"] = " "
            else:
                text = (
                    COLOR_YELLOW + "You cannot buy that items because it would cause " +
                    "your gold to be negative or because you don't own that item." + COLOR_RESET_ALL
                )
                text_handling.print_long_string(text)
        else:
            p = False
