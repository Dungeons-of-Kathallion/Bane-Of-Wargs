import colors
import logger_sys
import random
import text_handling
import uuid_handling
import weapon_upgrade_handling
import train
import term_menu
import time
from colorama import Fore, Back, Style, init, deinit
from colors import *

# initialize colorama
init()

# Handling functions


# Information printing functions
def print_zone_news(zone, map_zone):
    logger_sys.log_message(f"INFO: Printing map zone '{map_zone}' news")
    print("NEWS:")
    village_news = zone[map_zone]["news"]
    village_news_len = len(village_news)
    choose_rand_news = random.randint(0, (village_news_len - 1))
    choose_rand_news = village_news[int(choose_rand_news)]
    text_handling.print_long_string(choose_rand_news)
    text = '='
    text_handling.print_separator(text)


def print_forge_information(map_zone, zone, item):
    current_forge = zone[map_zone]
    current_forge_name = current_forge["name"]
    logger_sys.log_message(f"INFO: Printing current forge '{current_forge_name}' information to GUI")
    print(COLOR_STYLE_BRIGHT + str(current_forge["name"]) + ":" + COLOR_RESET_ALL)
    text = current_forge["description"]
    text_handling.print_long_string(text)
    print(" ")
    if "None" not in current_forge["forge"]["buys"]:
        print("METAL BUYS:")
        count = 0
        metal_buys = current_forge["forge"]["buys"]
        metal_buys_len = len(metal_buys)
        while count < metal_buys_len:
            current_metal = str(metal_buys[count])
            print(
                " -" + current_metal + " " + COLOR_YELLOW + COLOR_STYLE_BRIGHT +
                str(round(item[current_metal]["gold"] * current_forge["cost value"], 2)) + COLOR_RESET_ALL
            )
            count += 1
    if "None" not in current_forge["forge"]["sells"]:
        print("METAL SELLS:")
        count = 0
        metal_sells = current_forge["forge"]["sells"]
        metal_sells_len = len(metal_sells)
        while count < metal_sells_len:
            current_metal = str(metal_sells[count])
            print(
                " -" + current_metal + " " + COLOR_YELLOW + COLOR_STYLE_BRIGHT +
                str(round(item[current_metal]["gold"] * current_forge["cost value"], 2)) + COLOR_RESET_ALL
            )
            count += 1
    text = '='
    text_handling.print_separator(text)


def print_blacksmith_information(map_zone, zone, item):
    current_black_smith = zone[map_zone]
    current_black_smith_name = current_black_smith["name"]
    logger_sys.log_message(f"INFO: Printing current blacksmith '{current_black_smith_name}' information to GUI")
    print(COLOR_STYLE_BRIGHT + str(current_black_smith["name"]) + ":" + COLOR_RESET_ALL)
    text = current_black_smith["description"]
    text_handling.print_long_string(text)
    print("")
    if "None" not in current_black_smith["blacksmith"]["buys"]:
        print("EQUIPMENT BUYS:")
        count = 0
        weapon_buys = current_black_smith["blacksmith"]["buys"]
        weapon_buys_len = len(weapon_buys)
        while count < weapon_buys_len:
            current_weapon = str(weapon_buys[int(count)])
            print(
                " -" + current_weapon + " " + COLOR_YELLOW + COLOR_STYLE_BRIGHT +
                str(round(item[current_weapon]["gold"] * current_black_smith["cost value"], 2)) + COLOR_RESET_ALL
            )
            count += 1
    if "None" not in current_black_smith["blacksmith"]["orders"]:
        print("EQUIPMENT ORDERS:")
        count = 0
        weapon_orders = current_black_smith["blacksmith"]["orders"]
        weapon_orders_len = len(weapon_orders)
        while count < weapon_orders_len:
            current_weapon = str(list(weapon_orders)[int(count)])
            current_weapon_materials = current_black_smith["blacksmith"]["orders"][current_weapon]["needed materials"]
            count2 = 0
            global_current_weapon_materials = []
            current_weapon_materials_num = len(current_weapon_materials)
            while count2 < current_weapon_materials_num:
                current_material = current_weapon_materials[count2]

                global_current_weapon_materials += [current_material]

                count2 += 1

            count2 = 0
            count3 = 0

            while count2 < len(global_current_weapon_materials):
                current_material = global_current_weapon_materials[count2]
                current_material_number = str(global_current_weapon_materials.count(current_material))

                if global_current_weapon_materials.count(current_material) > 1:
                    while count3 < global_current_weapon_materials.count(current_material):
                        global_current_weapon_materials.remove(current_material)
                        count3 += 1
                    global_current_weapon_materials = [
                        sub.replace(
                            current_material, current_material + "X" + current_material_number
                        ) for sub in global_current_weapon_materials
                    ]

                count2 += 1

            global_current_weapon_materials = str(global_current_weapon_materials)
            global_current_weapon_materials = global_current_weapon_materials.replace("'", '')
            global_current_weapon_materials = global_current_weapon_materials.replace("[", '')
            global_current_weapon_materials = global_current_weapon_materials.replace("]", '')
            print(
                " -" + current_weapon + " " + COLOR_YELLOW + COLOR_STYLE_BRIGHT +
                str(round(item[current_weapon]["gold"] * current_black_smith["cost value"], 2)) +
                COLOR_RESET_ALL + COLOR_GREEN + COLOR_STYLE_BRIGHT +
                " (" + COLOR_RESET_ALL + global_current_weapon_materials +
                COLOR_GREEN + COLOR_STYLE_BRIGHT + ")" + COLOR_RESET_ALL
            )
            count += 1
    text = '='
    text_handling.print_separator(text)


def print_stable_information(map_zone, zone, mounts, item, player, map_location):
    current_stable = zone[map_zone]
    current_stable_name = current_stable["name"]
    print(COLOR_STYLE_BRIGHT + str(current_stable["name"]) + ":" + COLOR_RESET_ALL)
    logger_sys.log_message(f"INFO: Printing current stable '{current_stable_name}' information to GUI")
    text = current_stable["description"]
    text_handling.print_long_string(text)
    print(" ")
    print("DEPOSIT COST/DAY: " + COLOR_YELLOW + COLOR_STYLE_BRIGHT + str(current_stable["deposit gold"]) + COLOR_RESET_ALL)
    print("TRAINING COST/DAY: " + COLOR_YELLOW + COLOR_STYLE_BRIGHT + str(current_stable["training gold"]) + COLOR_RESET_ALL)
    options = ['Train Mount', '']
    if "None" not in current_stable["stable"]["sells"]["mounts"]:
        print("MOUNTS SELLS:")
        count = 0
        stable_mounts = current_stable["stable"]["sells"]["mounts"]
        stable_mounts_len = len(stable_mounts)
        while count < stable_mounts_len:
            current_mount = str(stable_mounts[int(count)])
            print(
                " -" + current_stable["stable"]["sells"]["mounts"][int(count)] + " " + COLOR_YELLOW +
                COLOR_STYLE_BRIGHT + str(round(mounts[current_mount]["gold"] * current_stable["cost value"], 2)) +
                COLOR_RESET_ALL
            )
            count += 1
    if "None" not in current_stable["stable"]["sells"]["items"]:
        options += ['Buy Item']
        print("ITEMS SELLS:")
        count = 0
        stable_items = current_stable["stable"]["sells"]["items"]
        stable_items_len = len(stable_items)
        while count < stable_items_len:
            current_mount = str(stable_items[int(count)])
            print(
                " -" + current_stable["stable"]["sells"]["items"][int(count)] + " " + COLOR_YELLOW +
                COLOR_STYLE_BRIGHT + str(round(item[current_mount]["gold"] * current_stable["cost value"], 2)) +
                COLOR_RESET_ALL
            )
            count += 1
    print(" ")
    deposited_mounts_num = 0
    count = 0
    mounts_list_len = len(player["mounts"])
    deposited_mounts_names = []
    if "None" not in list(player["mounts"]):
        while count < mounts_list_len:
            selected_mount = list(player["mounts"])[count]
            selected_mount = str(selected_mount)
            if (
                player["mounts"][selected_mount]["location"] == "point" +
                str(map_location)
                and player["mounts"][selected_mount]["is deposited"]
            ):
                deposited_mounts_num += 1
                deposited_mounts_names += [str(player["mounts"][selected_mount]["name"])]
            count += 1
    else:
        deposited_mounts_names = 0
        deposited_mounts_num = 0
    deposited_mounts_names = str(deposited_mounts_names)
    deposited_mounts_names = deposited_mounts_names.replace('[', '(')
    deposited_mounts_names = deposited_mounts_names.replace(']', COLOR_RESET_ALL + ')')
    deposited_mounts_names = deposited_mounts_names.replace("'", COLOR_GREEN + COLOR_STYLE_BRIGHT)
    deposited_mounts_names = deposited_mounts_names.replace(',', COLOR_RESET_ALL + ',')
    if deposited_mounts_num == 0:
        print("MOUNTS DEPOSITED HERE: " + COLOR_BLUE + COLOR_STYLE_BRIGHT + str(deposited_mounts_num) + COLOR_RESET_ALL)
    else:
        print(
            "MOUNTS DEPOSITED HERE: " + COLOR_BLUE + COLOR_STYLE_BRIGHT +
            str(deposited_mounts_num) + COLOR_RESET_ALL + " " + deposited_mounts_names
        )
    text = '='
    text_handling.print_separator(text)


def print_hostel_information(map_zone, zone, item, drinks):
    current_hostel = zone[map_zone]
    current_hostel_name = current_hostel["name"]
    logger_sys.log_message(f"INFO: Printing current hostel '{current_hostel_name}' information to GUI")
    print(COLOR_STYLE_BRIGHT + str(current_hostel["name"]) + ":" + COLOR_RESET_ALL)
    text = current_hostel["description"]
    text_handling.print_long_string(text)
    print(" ")
    print("SLEEP COST: " + COLOR_YELLOW + COLOR_STYLE_BRIGHT + str(current_hostel["sleep gold"]) + COLOR_RESET_ALL)
    if "None" not in current_hostel["sells"]["drinks"]:
        print("DRINKS SELLS:")
        count = 0
        hostel_drinks = current_hostel["sells"]["drinks"]
        hostel_drinks_len = len(hostel_drinks)
        while count < hostel_drinks_len:
            current_drink = str(current_hostel["sells"]["drinks"][int(count)])
            print(
                " -" + current_hostel["sells"]["drinks"][int(count)] + " " + COLOR_YELLOW +
                COLOR_STYLE_BRIGHT + str(round(drinks[current_drink]["gold"] * current_hostel["cost value"], 2)) +
                COLOR_RESET_ALL
            )
            count += 1
    if "None" not in current_hostel["sells"]["items"]:
        print("ITEMS SELLS")
        count = 0
        hostel_items = current_hostel["sells"]["items"]
        hostel_items_len = len(hostel_items)
        while count < hostel_items_len:
            current_item = str(current_hostel["sells"]["items"][int(count)])
            print(
                " -" + current_hostel["sells"]["items"][int(count)] + " " + COLOR_YELLOW +
                COLOR_STYLE_BRIGHT + str(round(item[current_item]["gold"] * current_hostel["cost value"], 2)) +
                COLOR_RESET_ALL
            )
            count += 1
    if "None" not in current_hostel["buys"]["items"]:
        print("ITEMS BUYS:")
        count = 0
        hostel_items = current_hostel["buys"]["items"]
        hostel_items_len = len(hostel_items)
        while count < hostel_items_len:
            current_item = str(current_hostel["buys"]["items"][int(count)])
            print(
                " -" + current_hostel["buys"]["items"][int(count)] + " " + COLOR_YELLOW +
                COLOR_STYLE_BRIGHT + str(round(item[current_item]["gold"] * current_hostel["cost value"], 2)) +
                COLOR_RESET_ALL
            )
            count += 1
    text = '='
    text_handling.print_separator(text)

# Interactions functions


def interaction_hostel(map_zone, zone, player, drinks, item):
    logger_sys.log_message(f"INFO: Current map zone '{map_zone}' is an hostel --> can interact")
    text = '='
    text_handling.print_separator(text)
    logger_sys.log_message(f"INFO: Adding correct interactions options depending on the hostel '{map_zone}' capabilities")
    options = ['Sleep']
    if "None" not in zone[map_zone]["sells"]["drinks"]:
        options += ['Buy Drink']
    if "None" not in zone[map_zone]["sells"]["items"]:
        options += ['Buy Item']
    if "None" not in zone[map_zone]["buys"]["items"]:
        options += ['Sell Item']
    options += ['Exit']
    continue_hostel_actions = True
    logger_sys.log_message("INFO: Starting loop of hostel actions")
    while continue_hostel_actions:
        choice = term_menu.show_menu(options)
        logger_sys.log_message(f"INFO: Player has chosen option '{choice}'")
        if choice == 'Sleep':
            print("Are you sure you want to spend the night here? It will ")
            ask = input("cost you " + str(zone[map_zone]["sleep gold"]) + " gold (y/n) ")
            text = '='
            text_handling.print_separator(text)
            if ask.lower().startswith('y'):
                logger_sys.log_message("INFO: Starting player sleeping process")
                if int(player["gold"]) > int(zone[map_zone]["sleep gold"]):
                    sleep_gold = int(zone[map_zone]["sleep gold"])
                    logger_sys.log_message(f"INFO: Removed {sleep_gold} from player --> sleep costs")
                    player["gold"] -= zone[map_zone]["sleep gold"]
                    loading = 7
                    print(" ")
                    while loading > 0:
                        print("Sleeping... Zzz", end='\r')
                        time.sleep(.25)
                        print("Sleeping... zZz", end='\r')
                        time.sleep(.25)
                        print("Sleeping... zzZ", end='\r')
                        time.sleep(.25)
                        print("Sleeping... zzz", end='\r')
                        time.sleep(.25)
                        print("Sleeping... Zzz", end='\r')
                        time.sleep(.25)
                        print("Sleeping... zZz", end='\r')
                        time.sleep(.25)
                        print("Sleeping... zzZ", end='\r')
                        time.sleep(.25)
                        print("Sleeping... zzz", end='\r')
                        time.sleep(.25)
                        player["health"] += random.randint(1, 7)
                        loading -= 1
                    logger_sys.log_message("INFO: Finished sleeping process")
                    logger_sys.log_message("INFO: Updating correct day time to morning")
                    day_time = float(float(round(player["elapsed time game days"] + 1, 0)) + .25)
                    player["elapsed time game days"] = float(float(round(player["elapsed time game days"] + 1, 0)) + .25)
                    continue_hostel_actions = False
                    if player["health"] > player["max health"]:
                        player["health"] = player["max health"]
                else:
                    logger_sys.log_message("INFO: Canceling sleeping process --> player doesn't own enough gold")
                    print(COLOR_YELLOW + "You don't own enough gold to sleep here." + COLOR_RESET_ALL)
        elif choice == 'Buy Drink':
            which_drink = input("Which drink do you want to buy? ")
            logger_sys.log_message(f"INFO: Player has chosen drink '{which_drink}' to drink")
            if (
                which_drink in zone[map_zone]["sells"]["drinks"]
                and (drinks[which_drink]["gold"] * zone[map_zone]["cost value"]) < player["gold"]
            ):
                drink_cost = str(drinks[which_drink]["gold"] * zone[map_zone]["cost value"])
                logger_sys.log_message(f"INFO: Buying drink '{which_drink}' --> removed {drink_cost} gold from player")
                player["gold"] -= drinks[which_drink]["gold"] * zone[map_zone]["cost value"]
                if drinks[which_drink]["healing level"] == 999:
                    logger_sys.log_message("INFO: Healed player to max health")
                    player["health"] = player["max health"]
                else:
                    healing_level = drinks[which_drink]["healing level"]
                    logger_sys.log_message(f"INFO: Healed player {healing_level} hp")
                    player["health"] += drinks[which_drink]["healing level"]
            else:
                text = (
                    COLOR_YELLOW + "You cannot buy that items because it would cause your gold to be negative." + COLOR_RESET_ALL
                )
                logger_sys.log_message(f"INFO: Canceling buying process of drink '{which_drink}' --> doesn't have enough gold")
                text_handling.print_long_string(text)
        elif choice == 'Buy Item':
            which_item = input("Which item do you want to buy? ")
            logger_sys.log_message(f"INFO: Player has chosen item '{which_item}' to buy")
            if (
                which_item in zone[map_zone]["sells"]["items"]
                and (item[which_item]["gold"] * zone[map_zone]["cost value"]) < player["gold"]
            ):
                if player["inventory slots remaining"] > 0:
                    player["inventory slots remaining"] -= 1
                    logger_sys.log_message(f"INFO: Adding item '{which_item}' to player inventory")
                    player["inventory"].append(which_item)
                    item_cost = str(item[which_item]["gold"] * zone[map_zone]["cost value"])
                    logger_sys.log_message(f"INFO: Removing {item_cost} gold from player")
                    player["gold"] -= item[which_item]["gold"] * zone[map_zone]["cost value"]
                else:
                    logger_sys.log_message("INFO: Canceling buying process --> doesn't have enough inventory slots")
                    text = (
                        COLOR_YELLOW + "You cannot buy that items because it would cause your inventory slots to be negative." +
                        COLOR_RESET_ALL
                    )
                    text_handling.print_long_string(text)
            else:
                logger_sys.log_message("INFO: Canceling buying process --> doesn't have enough gold")
                text = (
                    COLOR_YELLOW + "You cannot buy that items because it would cause your gold to be negative." +
                    COLOR_RESET_ALL
                )
                text_handling.print_long_string(text)
        elif choice == 'Sell Item':
            which_item = input("Which item do you want to sell? ")
            logger_sys.log_message(f"INFO: Player has chosen item '{which_item}' to sell")
            if (
                which_item in zone[map_zone]["buys"]["items"]
                and (item[which_item]["gold"] * zone[map_zone]["cost value"]) < player["gold"]
                and which_item in player["inventory"]
            ):
                logger_sys.log_message(f"INFO: Removing item '{which_item}' from player inventory")
                player["inventory slots remaining"] -= 1
                gold = str(item[which_item]["gold"] * zone[map_zone]["cost value"])
                logger_sys.log_message(f"INFO: Adding to player {gold} gold")
                player["gold"] += item[which_item]["gold"] * zone[map_zone]["cost value"]
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
                logger_sys.log_message(f"INFO: Canceling selling process --> doesn't own item '{which_item}'")
                text = COLOR_YELLOW + "You cannot sell that items because you don't own any of this item." + COLOR_RESET_ALL
                text_handling.print_long_string(text)
        else:
            continue_hostel_actions = False


def interaction_stable(map_zone, zone, player, item, drinks, mounts, map_location, preferences):
    logger_sys.log_message(f"INFO: Current map zone '{map_zone}' is a stable --> can interact")
    options = ["Train Mount", "Deposit Mount", "Ride Mount"]
    if "None" not in zone[map_zone]["stable"]["sells"]["mounts"]:
        options += ["Buy Mount"]
    if "None" not in zone[map_zone]["stable"]["sells"]["drinks"]:
        options += ["Buy Drink"]
    if "None" not in zone[map_zone]["stable"]["sells"]["items"]:
        options += ["Buy Item"]
    options += ["Exit"]
    active_stable_menu = True
    text = '='
    text_handling.print_separator(text)
    logger_sys.log_message("INFO: Starting stable interaction loop")
    while active_stable_menu:
        action = term_menu.show_menu(options)
        logger_sys.log_message(f"INFO: Player has chosen option '{action}'")
        if action == 'Buy Item':
            which_item = input("Which item do you want to buy? ")
            logger_sys.log_message(f"INFO: Player has chosen item '{which_item}' to buy")
            if (
                which_item in zone[map_zone]["stable"]["sells"]["items"]
                and (item[which_item]["gold"] * zone[map_zone]["cost value"]) < player["gold"]
            ):
                if player["inventory slots remaining"] > 0:
                    logger_sys.log_message(f"INFO: Adding item '{which_item}' from player inventory")
                    player["inventory slots remaining"] -= 1
                    player["inventory"].append(which_item)
                    gold = str(item[which_item]["gold"] * zone[map_zone]["cost value"])
                    logger_sys.log_message(f"INFO: Removing {gold} gold from player")
                    player["gold"] -= item[which_item]["gold"] * zone[map_zone]["cost value"]
                else:
                    logger_sys.log_message("INFO: Canceling buying process -> doesn't gas enough inventory slots")
                    text = (
                        COLOR_YELLOW + "You cannot buy that items because it would cause your inventory slots to be negative." +
                        COLOR_RESET_ALL
                    )
                    text_handling.print_long_string(text)
            else:
                logger_sys.log_message("INFO: Canceling buying process --> doesn't has enough gold")
                text = (
                    COLOR_YELLOW + "You cannot buy that items because it would cause your gold to be negative." + COLOR_RESET_ALL
                )
                text_handling.print_long_string(text)
        elif action == 'Buy Drink':
            which_drink = input("Which drink do you want to buy? ")
            logger_sys.log_message(f"INFO: Player has chosen drink '{which_drink}' to buy")
            if (
                which_drink in zone[map_zone]["stable"]["sells"]["drinks"]
                and (drinks[which_drink]["gold"] * zone[map_zone]["cost value"]) < player["gold"]
            ):
                gold = str(drinks[which_drink]["gold"] * zone[map_zone]["cost value"])
                logger_sys.log_message(f"INFO: Removing {gold}  gold from player")
                player["gold"] -= drinks[which_drink]["gold"] * zone[map_zone]["cost value"]
                if drinks[which_drink]["healing level"] == 999:
                    logger_sys.log_message(f"INFO: Consuming drink '{which_drink}' --> healing player to max health")
                    player["health"] = player["max health"]
                else:
                    healing_level = drinks[which_drink]["healing level"]
                    logger_sys.log_message(f"INFO: Consuming drink '{which_drink}' --> healing player {healing_level} hp")
                    player["health"] += drinks[which_drink]["healing level"]
            else:
                logger_sys.log_message("INFO: Canceling buying process --> doesn't have enough gold")
                text = (
                    COLOR_YELLOW + "You cannot buy that items because it would cause your gold to be negative." + COLOR_RESET_ALL
                )
                text_handling.print_long_string(text)
        elif action == 'Buy Mount':
            which_mount = input("Which mount do you want to buy? ")
            logger_sys.log_message(f"INFO: Player has chosen mount '{which_mount}' to buy")
            if which_mount in zone[map_zone]["stable"]["sells"]["mounts"]:
                mount_cost = (mounts[which_mount]["gold"] * zone[map_zone]["cost value"])
                if mount_cost < player["gold"]:
                    logger_sys.log_message(f"INFO: Removing player {mount_cost} gold")
                    player["gold"] -= mount_cost
                    generated_mount_uuid = uuid_handling.generate_random_uuid()
                    print("How you mount should be named ?")
                    new_mount_name = input(COLOR_GREEN + COLOR_STYLE_BRIGHT + "> " + COLOR_RESET_ALL)
                    logger_sys.log_message(f"INFO: Player has chosen name '{new_mount_name}' for its new mount")
                    mounts_names_list = []
                    count = 0
                    if "None" not in list(player["mounts"]):
                        mounts_list_len = len(player["mounts"])
                        while count < mounts_list_len:
                            selected_mount = list(player["mounts"])[count]
                            selected_mount = str(selected_mount)
                            mounts_names_list.append(str(player["mounts"][selected_mount]["name"]))
                            count += 1
                    if new_mount_name in mounts_names_list:
                        logger_sys.log_message(f"INFO: Canceling buying process --> already has a mount name '{new_mount_name}'")
                        print(COLOR_YELLOW + "You already have a mount named like that." + COLOR_RESET_ALL)
                        text = '='
                        text_handling.print_separator(text)
                    else:
                        logger_sys.log_message("INFO: Creating new mount stats")
                        mount_stats = {
                            "agility addition": mounts[which_mount]["stats"]["agility addition"],
                            "resistance addition": mounts[which_mount]["stats"]["resistance addition"]
                        }
                        mount_dict = {
                            "deposited day": round(player["elapsed time game days"], 2),
                            "is deposited": True,
                            "level": 0,
                            "location": "point" + str(map_location),
                            "mount": str(which_mount),
                            "name": str(new_mount_name),
                            "stats": mount_stats
                        }
                        logger_sys.log_message(f"INFO: Created new mount stats: '{mount_dict}'")
                        player["mounts"][generated_mount_uuid] = mount_dict
                        logger_sys.log_message(f"INFO: Deposited new mount at map zone '{map_zone}'")
                        text = (
                            "Your mount is currently deposited at the " + zone[map_zone]["name"] +
                            "\nYou can ride it whenever you want."
                        )
                        text_handling.print_speech_text_effect(text, preferences)
                        text = '='
                        text_handling.print_separator(text)
                else:
                    logger_sys.log_message("INFO: Canceling buying process --> doesn't has enough gold")
                    print(COLOR_YELLOW + "You don't own enough gold to buy that mount" + COLOR_RESET_ALL)
            else:
                logger_sys.log_message(
                    f"INFO: Canceling buying process --> current stable '{
                        map_zone
                    }' doesn't sell mount '{which_mount}'"
                )
                print(COLOR_YELLOW + "The current stable do not sell this mount" + COLOR_RESET_ALL)
        elif action == 'Deposit Mount':
            if player["current mount"] != " ":
                current_mount_uuid = str(player["current mount"])
                mount_data = player["mounts"][current_mount_uuid]
                current_mount = mount_data["name"]
                current_mount_type = mount_data["mount"]
                # check if required stables are in the stable attributes
                required_mount_stable = str(mounts[str(mount_data["mount"])]["stable"]["required stable"])
                if required_mount_stable in zone[map_zone]["stable"]["stables"]:
                    ask = input("Do you want to deposit your current mount " + mount_data["name"] + " ? (y/n) ")
                    if ask.lower().startswith('y'):
                        logger_sys.log_message(
                            f"INFO: Depositing currently player ridden mount '{
                                current_mount
                            }' to map zone '{map_zone}"
                        )
                        player["current mount"] = " "
                        player["mounts"][current_mount_uuid]["is deposited"] = True
                        player["mounts"][current_mount_uuid]["deposited day"] = round(player["elapsed time game days"], 1)
                        player["mounts"][current_mount_uuid]["location"] = str("point" + str(map_location))
                    text = "="
                    text_handling.print_separator(text)
                else:
                    logger_sys.log_message(
                        f"INFO: Canceling depositing process --> current stable '{
                            map_zone
                        }' doesn't accept mounts of type '{current_mount_type}'"
                    )
                    print(COLOR_YELLOW + "This stable doesn't accept this type of mount." + COLOR_RESET_ALL)
            else:
                logger_sys.log_message("INFO: Canceling depositing process --> doesn't ride any mounts by now")
                print(COLOR_YELLOW + "You don't have any mounts to deposit here." + COLOR_RESET_ALL)
        elif action == 'Train Mount':
            if player["current mount"] != ' ':
                current_mount_uuid = str(player["current mount"])
                logger_sys.log_message("INFO: Starting mount training of mount '{current_mount_uuid}'")
                train.training_loop(current_mount_uuid, player, item, mounts, zone[map_zone])
            else:
                logger_sys.log_message("INFO: Canceling mount train process --> doesn't ride any mounts by now")
                text = (
                    COLOR_YELLOW + "You're not riding any mounts currently. You need to ride one to train it." + COLOR_RESET_ALL
                )
                text_handling.print_long_string(text)
        elif action == 'Ride Mount':
            if player["current mount"] == ' ':
                logger_sys.log_message(f"INFO: Getting player deposited mounts at stable '{map_zone}'")
                # get player total mounts at this place
                deposited_mounts_num = 0
                count = 0
                mounts_list_len = len(player["mounts"])
                deposited_mounts_names = []
                if "None" not in list(player["mounts"]):
                    while count < mounts_list_len:
                        selected_mount = list(player["mounts"])[count]
                        selected_mount = str(selected_mount)
                        if (
                            player["mounts"][selected_mount]["location"] == "point" +
                            str(map_location) and player["mounts"][selected_mount]["is deposited"]
                        ):
                            deposited_mounts_num += 1
                            deposited_mounts_names += [str(player["mounts"][selected_mount]["name"])]
                        count += 1
                else:
                    deposited_mounts_names = None
                    deposited_mounts_num = 0
                deposited_mounts_names_list = deposited_mounts_names
                deposited_mounts_names = str(deposited_mounts_names)
                deposited_mounts_names = deposited_mounts_names.replace("'", '')
                deposited_mounts_names = deposited_mounts_names.replace("[", ' -')
                deposited_mounts_names = deposited_mounts_names.replace("]", '')
                deposited_mounts_names = deposited_mounts_names.replace(", ", '\n -')
                print("MOUNTS AT THIS STABLE:")
                print(deposited_mounts_names)
                text = '='
                text_handling.print_separator(text)
                which_mount = input(COLOR_GREEN + COLOR_STYLE_BRIGHT + "> " + COLOR_RESET_ALL)
                logger_sys.log_message(f"INFO: Player has chosen mount '{which_mount}' to ride")
                if which_mount in deposited_mounts_names_list:
                    # get what is the uuid of the mount of this name
                    count = 0
                    continue_searching = True
                    which_mount_uuid = ""
                    while count < len(list(player["mounts"])) and continue_searching:
                        selected_mount_uuid = list(player["mounts"])[count]
                        selected_mount_data = player["mounts"][selected_mount_uuid]
                        if selected_mount_data["name"] == which_mount:
                            continue_searching = False
                            which_mount_uuid = str(selected_mount_uuid)
                        count += 1
                    mount_take_back_cost = round(
                        (
                            player["elapsed time game days"] - player["mounts"][which_mount_uuid]["deposited day"]
                        ) * zone[map_zone]["deposit gold"], 2
                    )
                    print(
                        "If you take back this mount it will cost you " + COLOR_YELLOW +
                        COLOR_STYLE_BRIGHT + str(mount_take_back_cost) + COLOR_RESET_ALL + " gold. "
                    )
                    ask = input("(y/n) ")
                    if player["gold"] > mount_take_back_cost:
                        if ask.lower().startswith('y'):
                            logger_sys.log_message(f"INFO: Removing {mount_take_back_cost} gold from player")
                            player["gold"] -= mount_take_back_cost
                            player["current mount"] = str(which_mount_uuid)
                            player["mounts"][which_mount_uuid]["is deposited"] = False
                            player["mounts"][which_mount_uuid]["deposited day"] = 0
                            player["mounts"][which_mount_uuid]["location"] = "point" + str(map_location)
                    else:
                        logger_sys.log_message("INFO: Canceling taking back process --> doesn't has enough gold")
                        print(COLOR_YELLOW + "You don't own enough gold to take back your mount." + COLOR_RESET_ALL)
                else:
                    logger_sys.log_message(
                        "INFO: Canceling taking back process --> doesn't own that mount " +
                        "or the mount isn't deposited at this current location"
                    )
                    text = (
                        COLOR_YELLOW + "You don't own that mount or the mount isn't deposited at this current location" +
                        COLOR_RESET_ALL
                    )
                    text_handling.print_long_string(text)
            else:
                logger_sys.log_message(f"INFO: Canceling taking back process --> already riding mount '{which_mount}'")
                text = (
                    COLOR_YELLOW + "You are currently already riding a mount. You need " +
                    "to deposit your current mount before riding an other one." + COLOR_RESET_ALL
                )
                text_handling.print_long_string(text)
        else:
            active_stable_menu = False


def interaction_blacksmith(map_zone, zone, item, player):
    logger_sys.log_message(f"INFO: Current map zone '{map_zone}' is a blacksmith --> can interact")
    text = '='
    text_handling.print_separator(text)

    options = ['Sell Equipment', 'Order Equipment', 'Upgrade Equipment', 'Check Order', 'Exit']
    continue_blacksmith_actions = True
    logger_sys.log_message("INFO: Starting blacksmith interact loop")
    while continue_blacksmith_actions:
        action = term_menu.show_menu(options)
        logger_sys.log_message(f"INFO: Player has chosen option '{action}'")
        if action == 'Sell Equipment':
            which_weapon = input("Which equipment do you want to sell? ")
            logger_sys.log_message(f"INFO: Player has chosen item '{which_weapon}' to sell")
            if which_weapon in zone[map_zone]["blacksmith"]["buys"] and which_weapon in player["inventory"]:
                gold = str(item[which_weapon]["gold"] * zone[map_zone]["cost value"])
                player["gold"] += item[which_weapon]["gold"] * zone[map_zone]["cost value"]
                logger_sys.log_message(f"INFO: Adding to player {gold} gold")
                player["inventory"].remove(which_weapon)
                logger_sys.log_message(f"INFO: Removing item '{which_weapon}' from player inventory")
            else:
                text = (
                    COLOR_YELLOW + "You cannot sell that equipment because you " +
                    "dont own any of that weapon or because the current blacksmith doesn't buy this weapon." +
                    COLOR_RESET_ALL
                )
                logger_sys.log_message(
                    f"INFO: Canceling selling process --> current blacksmith '{
                        map_zone
                    }' doesn't sell item '{which_weapon}' or player doesn't own item '{which_weapon}'"
                )
                text_handling.print_long_string(text)
        elif action == 'Order Equipment':
            which_weapon = input("Which equipment do you want to order? ")
            logger_sys.log_message(f"INFO: Player has chosen item '{which_weapon}' to order")
            if (
                which_weapon in zone[map_zone]["blacksmith"]["orders"]
                and player["gold"] > zone[map_zone]["blacksmith"]["orders"][which_weapon]["gold"]
            ):
                required_items = False
                count = 0
                required_items_number = 0
                fake_player_inventory = player["inventory"]
                while count < len(fake_player_inventory):
                    selected_item = fake_player_inventory[count]
                    if selected_item in zone[map_zone]["blacksmith"]["orders"][which_weapon]["needed materials"]:
                        required_items_number += 1
                    count += 1
                if required_items_number == len(zone[map_zone]["blacksmith"]["orders"][which_weapon]["needed materials"]):
                    required_items = True
                    logger_sys.log_message("INFO: Player has required items --> continuing")
                if required_items:
                    gold = str(zone[map_zone]["blacksmith"]["orders"][which_weapon]["gold"])
                    logger_sys.log_message(f"INFO: Removing from player {gold} gold")
                    player["gold"] -= zone[map_zone]["blacksmith"]["orders"][which_weapon]["gold"]
                    count = 0
                    remaining_items_to_remove = len(zone[map_zone]["blacksmith"]["orders"][which_weapon]["needed materials"])
                    while count < len(player["inventory"]) and remaining_items_to_remove != 0:
                        selected_item = zone[map_zone]["blacksmith"]["orders"][which_weapon]["needed materials"][count]
                        logger_sys.log_message(f"INFO: Removing from player inventory item '{selected_item}'")
                        player["inventory"].remove(selected_item)
                        remaining_items_to_remove -= 1
                        count += 1
                    order_uuid = uuid_handling.generate_random_uuid()
                    logger_sys.log_message(f"INFO: Creating order '{order_uuid}' dictionary")
                    order_dict = {
                        "paid gold": int(gold),
                        "ordered weapon": which_weapon,
                        "ordered day": player["elapsed time game days"],
                        "ordered blacksmith": zone[map_zone]["name"],
                        "time needed": zone[map_zone]["blacksmith"]["orders"][which_weapon]["time needed"],
                        "has taken back order": "false"
                    }
                    logger_sys.log_message(f"Created order '{order_uuid}' dictionary: '{order_dict}'")
                    player["orders"][order_uuid] = order_dict
                    text = (
                        "You'll be able to get your finished order in " + COLOR_MAGENTA +
                        COLOR_STYLE_BRIGHT + str(zone[map_zone]["blacksmith"]["orders"][which_weapon]["time needed"]) +
                        COLOR_RESET_ALL + " days."
                    )
                    text_handling.print_long_string(text)
                else:
                    logger_sys.log_message("INFO: Canceling ordering process --> doesn't have necessary items")
                    text = (
                        COLOR_YELLOW + "You cannot order that equipment because you dont have the necessary items." +
                        COLOR_RESET_ALL
                    )
                    text_handling.print_long_string(text)
            else:
                logger_sys.log_message("INFO: Canceling ordering process --> doesn't has enough gold")
                text = COLOR_YELLOW + "You cannot order that weapon because you dont own enough gold." + COLOR_RESET_ALL
                text_handling.print_long_string(text)
        elif action == 'Upgrade Equipment':
            which_weapon = input("Which equipment do you want to upgrade? ")
            logger_sys.log_message(f"INFO: Player has chosen equipment '{which_weapon}' to upgrade")
            if which_weapon in player["inventory"]:
                item_next_upgrade_name = str(weapon_upgrade_handling.check_weapon_next_upgrade_name(which_weapon, item))
                if item_next_upgrade_name != 'None':
                    if player["gold"] > item[item_next_upgrade_name]["gold"]:
                        finished = False
                        has_required_items = True
                        player_fake_inventory = player["inventory"]
                        required_items = []
                        for i in player_fake_inventory:
                            if i in item[item_next_upgrade_name]["for this upgrade"]:
                                required_items.append(i)
                        while has_required_items and not finished:
                            for i in item[item_next_upgrade_name]["for this upgrade"]:
                                if required_items.count(i) < item[item_next_upgrade_name]["for this upgrade"].count(i):
                                    has_required_items = False
                            finished = True
                        if has_required_items:
                            gold = str(item[item_next_upgrade_name]["gold"])
                            logger_sys.log_message(f"INFO: Removing from player {gold} gold")
                            player["gold"] -= item[item_next_upgrade_name]["gold"]
                            player["inventory"].remove(which_weapon)
                            count = 0
                            remaining_items_to_remove = len(item[str(item_next_upgrade_name)]["for this upgrade"])
                            while count < len(player["inventory"]) and remaining_items_to_remove > 0:
                                selected_item = item[str(item_next_upgrade_name)]["for this upgrade"][count]
                                player["inventory"].remove(selected_item)
                                remaining_items_to_remove -= 1
                                count += 1
                            order_uuid = uuid_handling.generate_random_uuid()
                            logger_sys.log_message(f"INFO: Creating order '{order_uuid}' dictionary")
                            order_dict = {
                                "paid gold": item[str(item_next_upgrade_name)]["gold"],
                                "ordered weapon": str(item_next_upgrade_name),
                                "ordered day": player["elapsed time game days"],
                                "ordered blacksmith": zone[map_zone]["name"],
                                "time needed": round(random.uniform(.55, 3.55), 2),
                                "has taken back order": "false"
                            }
                            logger_sys.log_message(f"Created order '{order_uuid}' dictionary: '{order_dict}'")
                            player["orders"][order_uuid] = order_dict
                            text = (
                                "You'll be able to get your finished order in " + COLOR_MAGENTA +
                                COLOR_STYLE_BRIGHT + str(player["orders"][order_uuid]["time needed"]) +
                                COLOR_RESET_ALL + " days."
                            )
                            text_handling.print_long_string(text)
                        else:
                            logger_sys.log_message("INFO: Canceling upgrading process --> doesn't has the necessary items")
                            print(COLOR_YELLOW + "You don't own the necessary items to upgrade" + COLOR_RESET_ALL)
                    else:
                        logger_sys.log_message("INFO: Canceling upgrading process --> doesn't has enough gold")
                        print(COLOR_YELLOW + "You don't have enough gold to upgrade." + COLOR_RESET_ALL)
                else:
                    logger_sys.log_message(
                        f"INFO: Canceling upgrading process --> cannot upgrade equipment '{which_weapon}' further"
                        )
                    print(
                        COLOR_YELLOW + "You cannot upgrade this equipment further." + COLOR_RESET_ALL
                    )
            else:
                logger_sys.log_message(f"INFO: Canceling upgrading process --> player doesn't own any '{
                    which_weapon
                }' in its inventory")
                print(COLOR_YELLOW + "You don't own that equipment" + COLOR_RESET_ALL)
        elif action == 'Check Order':
            player_orders = player["orders"]
            logger_sys.log_message(f"INFO: Printing player orders: '{player_orders}'")
            player_orders_numbers = len(list(player_orders))
            player_orders_to_collect = []
            player_orders_number = []
            count = 0
            while count < player_orders_numbers:
                skip = False
                selected_order_name = list(player_orders)[count]
                if selected_order_name == "None":
                    skip = True
                if not skip:
                    selected_order = player["orders"][selected_order_name]
                    try:
                        ordered_blacksmith = selected_order["ordered blacksmith"]
                        ordered_weapon = selected_order["ordered weapon"]
                    except Exception:
                        print(ordered_blacksmith, ordered_weapon)
                    if ordered_blacksmith == zone[map_zone]["name"]:
                        ordered_weapon_syntax = ordered_weapon + " {" + str(count) + "}"
                        player_orders_to_collect += [ordered_weapon_syntax]
                        player_orders_number += [str(count)]
                count += 1
            player_orders_to_collect = str(player_orders_to_collect)
            logger_sys.log_message(f"INFO: Printing player orders to collect: '{player_orders_to_collect}'")
            player_orders_to_collect = player_orders_to_collect.replace("'", '')
            player_orders_to_collect = player_orders_to_collect.replace("[", ' -')
            player_orders_to_collect = player_orders_to_collect.replace("]", '')
            player_orders_to_collect = player_orders_to_collect.replace(", ", '\n -')
            print("ORDERS:")
            print(player_orders_to_collect)
            text = '='
            text_handling.print_separator(text)
            which_order = input(COLOR_GREEN + COLOR_STYLE_BRIGHT + "> " + COLOR_RESET_ALL)
            logger_sys.log_message(f"INFO: Player has chosen order '{which_order}'")
            if which_order in player_orders_number:
                current_order_uuid = str(list(player["orders"])[int(which_order)])
                text = '='
                text_handling.print_separator(text)

                time_left = round(
                    player["orders"][current_order_uuid]["ordered day"] +
                    player["orders"][current_order_uuid]["time needed"] - player["elapsed time game days"], 1
                )
                if time_left <= 0:
                    time_left = "READY TO COLLECT"
                logger_sys.log_message(f"INFO: Printing order '{current_order_uuid}' information to GUI")
                print(
                    "ORDERED EQUIPMENT: " + COLOR_RED +
                    str(player["orders"][current_order_uuid]["ordered weapon"]) + COLOR_RESET_ALL
                )
                print(
                    "PAID GOLD: " + COLOR_YELLOW + COLOR_STYLE_BRIGHT +
                    str(round(player["orders"][current_order_uuid]["paid gold"], 1)) + COLOR_RESET_ALL
                )
                print(
                    "ORDERED DAY: " + COLOR_MAGENTA + COLOR_STYLE_BRIGHT +
                    str(round(player["orders"][current_order_uuid]["ordered day"], 1)) + COLOR_RESET_ALL
                )
                print("TIME LEFT: " + COLOR_CYAN + COLOR_STYLE_BRIGHT + str(time_left) + COLOR_RESET_ALL)

                text = '='
                text_handling.print_separator(text)
                options_order = ['Cancel Order']
                if time_left == "READY TO COLLECT":
                    options_order += ['Collect Order']
                options_order += ['Exit']
                action = term_menu.show_menu(options_order)
                logger_sys.log_message(f"INFO: Player has chosen option '{action}'")
                if action == 'Cancel Order':
                    text = (
                        "Are you sure you want to cancel this order? You will receive " +
                        "75% of the gold you paid and you won't be able"
                    )
                    text_handling.print_long_string(text)
                    ask = input(" to get your given items back. (y/n)")
                    if ask.lower().startswith('y'):
                        # give player 75% of paid gold
                        gold = player["orders"][current_order_uuid]["paid gold"]
                        gold2 = player["orders"][current_order_uuid]["paid gold"] * (75 / 100)
                        logger_sys.log_message(f"INFO: Giving back player 75% of the paid gold: {gold} * 100 / 75 = {gold2}")
                        player["gold"] += player["orders"][current_order_uuid]["paid gold"] * (75 / 100)
                        # remove order from player orders
                        player["orders"].pop(current_order_uuid)
                if action == 'Collect Order':
                    order = str(player["orders"][current_order_uuid]["ordered weapon"])
                    logger_sys.log_message(f"INFO: Collecting order --> adding to player inventory item '{order}'")
                    player["inventory"].append(str(player["orders"][current_order_uuid]["ordered weapon"]))
                    # remove order from player orders
                    player["orders"].pop(current_order_uuid)
            else:
                logger_sys.log_message(
                    f"INFO: Canceling collecting order process --> player has no order '{
                        which_order
                    }' at map zone '{map_zone}'"
                )
                print(COLOR_YELLOW + "You don't have this order currently at this place." + COLOR_RESET_ALL)
        else:
            continue_blacksmith_actions = False


def interaction_forge(map_zone, zone, player, item):
    logger_sys.log_message(f"INFO: map zone '{map_zone}' is a forge --> can interact")
    current_forge = zone[map_zone]
    text = '='
    text_handling.print_separator(text)
    options = []
    if "None" not in current_forge["forge"]["buys"]:
        options += ['Sell Metals']
    if "None" not in current_forge["forge"]["sells"]:
        options += ['Buy Metals']
    options += ['Exit']
    continue_forge_actions = True
    logger_sys.log_message("INFO: Starting forge interact loop")
    while continue_forge_actions:
        choice = term_menu.show_menu(options)
        logger_sys.log_message(f"INFO: Player has chosen option '{choice}'")
        if choice == 'Sell Metals':
            which_metal = input("Which metal do you want to sell? ")
            logger_sys.log_message(f"INFO: Player has chosen metal '{which_metal}' to buy")
            if which_metal in current_forge["forge"]["buys"]:
                metal_count = int(input("How many count of this metal you want to sell? "))
                logger_sys.log_message(f"INFO: Player has chosen to sell '{metal_count}' of the metal '{which_metal}'")
                if player["inventory"].count(which_metal) >= metal_count:
                    gold = item[which_metal]["gold"] * current_forge["cost value"] * metal_count
                    logger_sys.log_message(f"INFO: Adding {gold} gold to player")
                    player["gold"] += item[which_metal]["gold"] * current_forge["cost value"] * metal_count
                    count = 0
                    while count < metal_count:
                        logger_sys.log_message(f"INFO: Removing from player inventory item '{which_metal}'")
                        player["inventory"].remove(which_metal)
                        count += 1
                else:
                    logger_sys.log_message(
                        f"INFO: Canceling selling process --> doesn't has {
                            metal_count
                        } '{which_metal}' in player's inventory"
                    )
                    print(COLOR_YELLOW + "You don't own that many count of this metal" + COLOR_RESET_ALL)
            else:
                logger_sys.log_message(
                    f"INFO: Canceling selling process --> current forge '{map_zone}' doesn't sell metal '{which_metal}'"
                )
                print(COLOR_YELLOW + "The current forge doesn't buys this metal" + COLOR_RESET_ALL)
        elif choice == 'Buy Metals':
            which_metal = input("Which metal do you want to buy? ")
            logger_sys.log_message(f"INFO: Player has chosen item '{which_metal}' to buy")
            if which_metal in current_forge["forge"]["sells"]:
                metal_count = int(input("How many count of this metal you want to buy? "))
                if player["gold"] >= item[which_metal]["gold"] * current_forge["cost value"] * metal_count:
                    gold = item[which_metal]["gold"] * current_forge["cost value"] * metal_count
                    logger_sys.log_message(f"INFO: Removing from player {gold} gold")
                    player["gold"] -= item[which_metal]["gold"] * current_forge["cost value"] * metal_count
                    count = 0
                    while count < metal_count:
                        logger_sys.log_message(f"INFO: Adding to player inventory item '{which_metal}")
                        player["inventory"].append(which_metal)
                        count += 1
                else:
                    logger_sys.log_message(f"INFO: Canceling buying process --> doesn't have enough gold")
                    print(COLOR_YELLOW + "You don't own enough gold to buy that many metal" + COLOR_RESET_ALL)
            else:
                logger_sys.log_message(
                    f"INFO: Canceling buying process --> current forge '{
                        map_zone
                    }' doesn't sell item '{which_metal}'"
                )
                print(COLOR_YELLOW + "The current forge doesn't sells this metal" + COLOR_RESET_ALL)
        else:
            continue_forge_actions = False


# deinitialize colorama
deinit()
