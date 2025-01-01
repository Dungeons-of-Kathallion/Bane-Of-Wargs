# zone_handling.py
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
import text_handling
import uuid_handling
import weapon_upgrade_handling
import train
import dungeon
import terminal_handling
import time_handling
import dialog_handling
import yaml_handling
from colors import *
from terminal_handling import cout, cinput, cinput_int
# external imports
import random
import time
import appdirs


program_dir = str(appdirs.user_config_dir(appname='Bane-Of-Wargs'))
ZONE_COLORS_DICT = {
    0: COLOR_GREENS_4 + '╬',
    1: COLOR_GREENS_5 + '╬',
    2: COLOR_GREEN + '╬',
    3: COLOR_GREENS_12 + '╬',
    4: COLOR_GREENS_2 + '↟',
    5: COLOR_GREENS_1 + '⇞',
    6: COLOR_GRAY_4 + '▲',
    7: COLOR_GRAY_5 + '▲',
    8: COLOR_GRAY_3 + '▲',
    9: COLOR_GRAY_1 + '▲',
    10: COLOR_YELLOW_6 + '≡',
    11: COLOR_YELLOW_7 + '≡',
    12: COLOR_YELLOW_7 + '≡',
    13: COLOR_ORANGE_5 + '≡',
    14: COLOR_ORANGE_3 + '≡',
    15: COLOR_ORANGE_4 + '≡',
    16: COLOR_ORANGE_4 + '≡',
    17: COLOR_ORANGE_6 + '≡',
    18: COLOR_ORANGE_6 + '≡',
    19: COLOR_ORANGE_7 + '≡',
    20: COLOR_MAGENTA_7 + '#',
    21: COLOR_YELLOW_8 + '≡',
    22: COLOR_GREENS_20 + '«',
    23: COLOR_YELLOW_3 + '«',
    24: COLOR_RED_1 + '«',
    25: COLOR_RED_0 + '«',
    26: COLOR_BLUE_5 + '⌂',
    27: COLOR_BLUE_13 + '⌂',
    28: COLOR_BLUE_13 + '⟰',
    29: COLOR_BLUE_13 + '⟰',
    30: COLOR_BLUE_13 + '⥣',
    31: COLOR_BLUE_13 + '⤊',
    32: COLOR_BLUE_13 + '±',
    33: COLOR_CYAN_3 + '≈',
    34: COLOR_CYAN_1 + '≈',
    35: COLOR_GREENS_0 + '#',
    36: COLOR_BLUE_13 + '⟰',
    37: COLOR_BLUE_14 + '⇭',
    38: COLOR_BLUE_14 + '±'
}
SELLING_ZONES = [
    "hostel",
    "forge",
    "stable",
    "blacksmith",
    "grocery",
    "harbor"
]


# Handling functions


def get_cost(cost, dropoff, round_cost=True):
    cost = cost - cost * dropoff
    if round_cost:
        return round(cost, 2)
    else:
        return cost


# Information printing functions
def print_zone_news(zone, map_zone, player):
    logger_sys.log_message(f"INFO: Printing map zone '{map_zone}' news")
    cout("NEWS:")
    village_news = zone[map_zone]["news"]
    village_news_len = len(village_news)
    choose_rand_news = random.randint(0, (village_news_len - 1))
    choose_rand_news = village_news[int(choose_rand_news)]
    text_handling.print_long_string(choose_rand_news)
    if (
        zone[map_zone]["type"] in SELLING_ZONES and
        player["discounts"][map_zone]["dropoff"] is not None
    ):
        cout(COLOR_RED + COLOR_STYLE_BRIGHT + "!!!SALES DISCOUNT!!!" + COLOR_RESET_ALL)
        text = (
            f"A @{COLOR_GREEN}@-{int(player['discounts'][map_zone]['dropoff'] * 100)}%@{COLOR_RESET_ALL}@ " +
            f"dropoff on every item's happening at @\033[38;2;255;128;0m@{zone[map_zone]['name']}@{COLOR_RESET_ALL}@" +
            f"! Only @{COLOR_BACK_BLUE}@{round(player['discounts'][map_zone]['remaining time'] * 24)} " +
            f"hours@{COLOR_RESET_ALL}@ remain!"
        )
        text_handling.print_long_string(text)
        cout(COLOR_RED + COLOR_STYLE_BRIGHT + "!!!SALES DISCOUNT!!!" + COLOR_RESET_ALL)
    text = '='
    text_handling.print_separator(text)


def print_forge_information(map_zone, zone, item, player):
    current_forge = zone[map_zone]
    current_forge_name = current_forge["name"]
    logger_sys.log_message(f"INFO: Printing current forge '{current_forge_name}' information to GUI")
    cout(COLOR_STYLE_BRIGHT + str(current_forge["name"]) + ":" + COLOR_RESET_ALL)
    text = current_forge["description"]
    text_handling.print_long_string(text)
    cout(" ")
    # Check if there's a discount active at this
    # map zone
    if player["discounts"][map_zone]["dropoff"] is not None:
        dropoff = player["discounts"][map_zone]["dropoff"]
    else:
        dropoff = 0
    if "None" not in current_forge["forge"]["buys"]:
        cout("METAL RESALES:")
        count = 0
        metal_buys = current_forge["forge"]["buys"]
        metal_buys_len = len(metal_buys)
        while count < metal_buys_len:
            current_metal = str(metal_buys[count])
            cout(
                " -" + current_metal + " " + COLOR_YELLOW + COLOR_STYLE_BRIGHT +
                str(get_cost(round(item[current_metal]["gold"] * current_forge["cost value"], 2), dropoff)) + COLOR_RESET_ALL
            )
            count += 1
    if "None" not in current_forge["forge"]["sells"]:
        cout("METAL SALES:")
        count = 0
        metal_sells = current_forge["forge"]["sells"]
        metal_sells_len = len(metal_sells)
        while count < metal_sells_len:
            current_metal = str(metal_sells[count])
            cout(
                " -" + current_metal + " " + COLOR_YELLOW + COLOR_STYLE_BRIGHT +
                str(get_cost(round(item[current_metal]["gold"] * current_forge["cost value"], 2), dropoff)) + COLOR_RESET_ALL
            )
            count += 1
    text = '='
    text_handling.print_separator(text)


def print_blacksmith_information(map_zone, zone, item, player):
    current_black_smith = zone[map_zone]
    current_black_smith_name = current_black_smith["name"]
    logger_sys.log_message(f"INFO: Printing current blacksmith '{current_black_smith_name}' information to GUI")
    cout(COLOR_STYLE_BRIGHT + str(current_black_smith["name"]) + ":" + COLOR_RESET_ALL)
    text = current_black_smith["description"]
    text_handling.print_long_string(text)
    cout("")
    # Check if there's a discount active at this
    # map zone
    if player["discounts"][map_zone]["dropoff"] is not None:
        dropoff = player["discounts"][map_zone]["dropoff"]
    else:
        dropoff = 0
    if "None" not in current_black_smith["blacksmith"]["buys"]:
        cout("EQUIPMENT RESALES:")
        count = 0
        weapon_buys = current_black_smith["blacksmith"]["buys"]
        weapon_buys_len = len(weapon_buys)
        while count < weapon_buys_len:
            current_weapon = str(weapon_buys[int(count)])
            cout(
                " -" + current_weapon + " " + COLOR_YELLOW + COLOR_STYLE_BRIGHT +
                str(
                    get_cost(round(item[current_weapon]["gold"] * current_black_smith["cost value"], 2), dropoff)
                ) + COLOR_RESET_ALL
            )
            count += 1
    if "None" not in current_black_smith["blacksmith"]["orders"]:
        cout("EQUIPMENT ORDERS:")
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

            global_current_weapon_materials = text_handling.multiple_items_in_list_formatting(
                global_current_weapon_materials
            )
            global_current_weapon_materials = str(global_current_weapon_materials)
            global_current_weapon_materials = global_current_weapon_materials.replace("'", '')
            global_current_weapon_materials = global_current_weapon_materials.replace("[", '')
            global_current_weapon_materials = global_current_weapon_materials.replace("]", '')
            cout(
                " -" + current_weapon + " " + COLOR_YELLOW + COLOR_STYLE_BRIGHT +
                str(get_cost(round(zone[map_zone]["blacksmith"]["orders"][current_weapon]["gold"]), dropoff)) +
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
    cout(COLOR_STYLE_BRIGHT + str(current_stable["name"]) + ":" + COLOR_RESET_ALL)
    logger_sys.log_message(f"INFO: Printing current stable '{current_stable_name}' information to GUI")
    text = current_stable["description"]
    text_handling.print_long_string(text)
    cout(" ")
    # Check if there's a discount active at this
    # map zone
    if player["discounts"][map_zone]["dropoff"] is not None:
        dropoff = player["discounts"][map_zone]["dropoff"]
    else:
        dropoff = 0
    cout(
        "DEPOSIT COST/DAY: " + COLOR_YELLOW + COLOR_STYLE_BRIGHT + str(get_cost(current_stable["deposit gold"], dropoff)) +
        COLOR_RESET_ALL
    )
    cout(
        "TRAINING COST/DAY: " + COLOR_YELLOW + COLOR_STYLE_BRIGHT + str(get_cost(current_stable["training gold"], dropoff)) +
        COLOR_RESET_ALL
    )
    options = ['Train Mount', '']
    if "None" not in current_stable["stable"]["sells"]["mounts"]:
        cout("MOUNTS SALES:")
        count = 0
        stable_mounts = current_stable["stable"]["sells"]["mounts"]
        stable_mounts_len = len(stable_mounts)
        while count < stable_mounts_len:
            current_mount = str(stable_mounts[int(count)])
            cout(
                " -" + current_stable["stable"]["sells"]["mounts"][int(count)] + " " + COLOR_YELLOW +
                COLOR_STYLE_BRIGHT + str(
                    get_cost(round(mounts[current_mount]["gold"] * current_stable["cost value"], 2), dropoff)
                ) +
                COLOR_RESET_ALL
            )
            count += 1
    if "None" not in current_stable["stable"]["sells"]["items"]:
        options += ['Buy Item']
        cout("ITEMS SALES:")
        count = 0
        stable_items = current_stable["stable"]["sells"]["items"]
        stable_items_len = len(stable_items)
        while count < stable_items_len:
            current_mount = str(stable_items[int(count)])
            cout(
                " -" + current_stable["stable"]["sells"]["items"][int(count)] + " " + COLOR_YELLOW +
                COLOR_STYLE_BRIGHT + str(
                    get_cost(round(item[current_mount]["gold"] * current_stable["cost value"], 2), dropoff)
                ) +
                COLOR_RESET_ALL
            )
            count += 1
    cout(" ")
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
        cout("MOUNTS DEPOSITED HERE: " + COLOR_BLUE + COLOR_STYLE_BRIGHT + str(deposited_mounts_num) + COLOR_RESET_ALL)
    else:
        cout(
            "MOUNTS DEPOSITED HERE: " + COLOR_BLUE + COLOR_STYLE_BRIGHT +
            str(deposited_mounts_num) + COLOR_RESET_ALL + " " + deposited_mounts_names
        )
    text = '='
    text_handling.print_separator(text)


def print_hostel_information(map_zone, zone, item, drinks, player):
    current_hostel = zone[map_zone]
    current_hostel_name = current_hostel["name"]
    logger_sys.log_message(f"INFO: Printing current hostel '{current_hostel_name}' information to GUI")
    cout(COLOR_STYLE_BRIGHT + str(current_hostel["name"]) + ":" + COLOR_RESET_ALL)
    text = current_hostel["description"]
    text_handling.print_long_string(text)
    cout(" ")
    # Check if there's a discount active at this
    # map zone
    if player["discounts"][map_zone]["dropoff"] is not None:
        dropoff = player["discounts"][map_zone]["dropoff"]
    else:
        dropoff = 0
    cout(
        "SLEEP COST: " + COLOR_YELLOW + COLOR_STYLE_BRIGHT + str(get_cost(current_hostel["sleep gold"], dropoff)) +
        COLOR_RESET_ALL
    )
    if "None" not in current_hostel["sells"]["drinks"]:
        cout("DRINKS SALES:")
        count = 0
        hostel_drinks = current_hostel["sells"]["drinks"]
        hostel_drinks_len = len(hostel_drinks)
        while count < hostel_drinks_len:
            current_drink = str(current_hostel["sells"]["drinks"][int(count)])
            cout(
                " -" + current_hostel["sells"]["drinks"][int(count)] + " " + COLOR_YELLOW +
                COLOR_STYLE_BRIGHT + str(
                    get_cost(round(drinks[current_drink]["gold"] * current_hostel["cost value"], 2), dropoff)
                ) +
                COLOR_RESET_ALL
            )
            count += 1
    if "None" not in current_hostel["sells"]["items"]:
        cout("ITEMS SALES")
        count = 0
        hostel_items = current_hostel["sells"]["items"]
        hostel_items_len = len(hostel_items)
        while count < hostel_items_len:
            current_item = str(current_hostel["sells"]["items"][int(count)])
            cout(
                " -" + current_hostel["sells"]["items"][int(count)] + " " + COLOR_YELLOW +
                COLOR_STYLE_BRIGHT + str(get_cost(round(item[current_item]["gold"] * current_hostel["cost value"], 2), dropoff)) +
                COLOR_RESET_ALL
            )
            count += 1
    if "None" not in current_hostel["buys"]["items"]:
        cout("ITEMS RESALES:")
        count = 0
        hostel_items = current_hostel["buys"]["items"]
        hostel_items_len = len(hostel_items)
        while count < hostel_items_len:
            current_item = str(current_hostel["buys"]["items"][int(count)])
            cout(
                " -" + current_hostel["buys"]["items"][int(count)] + " " + COLOR_YELLOW +
                COLOR_STYLE_BRIGHT + str(get_cost(round(item[current_item]["gold"] * current_hostel["cost value"], 2), dropoff)) +
                COLOR_RESET_ALL
            )
            count += 1
    text = '='
    text_handling.print_separator(text)


def print_grocery_information(map_zone, zone, item, player):
    current_grocery = zone[map_zone]
    current_grocery_name = current_grocery["name"]
    logger_sys.log_message(f"INFO: Printing current grocery '{current_grocery_name}' information to GUI")
    cout(COLOR_STYLE_BRIGHT + str(current_grocery["name"]) + ":" + COLOR_RESET_ALL)
    text = current_grocery["description"]
    text_handling.print_long_string(text)
    cout()
    # Check if there's a discount active at this
    # map zone
    if player["discounts"][map_zone]["dropoff"] is not None:
        dropoff = player["discounts"][map_zone]["dropoff"]
    else:
        dropoff = 0
    cout("ITEMS SALES:")
    sold_items_list = player["groceries data"][map_zone]["items sales"]
    sold_items = []
    for i in sold_items_list:
        sold_items += [
            f" -{i} {COLOR_YELLOW}{get_cost(round(zone[map_zone]['cost value'] * item[i]['gold'], 2), dropoff)}" +
            COLOR_RESET_ALL
        ]
    for i in sold_items:
        cout(i)
    text = '='
    text_handling.print_separator(text)


def print_harbor_information(map_zone, zone, map, player):
    current_harbor = zone[map_zone]
    current_harbor_name = current_harbor["name"]
    logger_sys.log_message(f"INFO: Printing current harbor '{current_harbor_name}' information to GUI")
    cout(COLOR_STYLE_BRIGHT + str(current_harbor["name"]) + ":" + COLOR_RESET_ALL)
    text = current_harbor["description"]
    text_handling.print_long_string(text)
    cout()
    # Check if there's a discount active at this
    # map zone
    if player["discounts"][map_zone]["dropoff"] is not None:
        dropoff = player["discounts"][map_zone]["dropoff"]
    else:
        dropoff = 0
    cout("TRAVELS:")
    travels = []
    count = 0
    for travel in current_harbor["travels"]:
        destination = map[f"point{current_harbor['travels'][travel]['destination']}"]
        destination = f"({COLOR_GREEN}{destination['x']} {COLOR_RESET_ALL},{COLOR_GREEN}{destination['y']}{COLOR_RESET_ALL})"
        time = str(
            str(round(
                time_handling.return_game_day_from_seconds(current_harbor['travels'][travel]['travel time'], 1) * 24, 1
            )) + "hrs"
        )
       travels += [
            f" -{list(current_harbor['travels'])[count]} {destination}" +
            f" {COLOR_YELLOW}{get_cost(round(current_harbor['travels'][travel]['cost'], 2), dropoff)}{COLOR_RESET_ALL}" +
            f" - {COLOR_CYAN}{time}{COLOR_RESET_ALL}"
        ]
        count += 1
    for travel in travels:
        cout(travel)
    text = '='
    text_handling.print_separator(text)


# Interactions functions


def interaction_hostel(map_zone, zone, player, drinks, item, save_file, preferences, previous_player):
    logger_sys.log_message(f"INFO: Current map zone '{map_zone}' is an hostel --> can interact")
    # Check if there's a discount active at this
    # map zone
    if player["discounts"][map_zone]["dropoff"] is not None:
        dropoff = player["discounts"][map_zone]["dropoff"]
    else:
        dropoff = 0
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
        choice = terminal_handling.show_menu(options)
        logger_sys.log_message(f"INFO: Player has chosen option '{choice}'")
        if choice == 'Sleep':
            cout("Are you sure you want to spend the night here? It will ")
            ask = cinput("cost you " + str(zone[map_zone]["sleep gold"]) + " gold (y/n) ")
            text = '='
            text_handling.print_separator(text)
            if ask.lower().startswith('y'):
                if player["difficulty mode"] >= 1:
                    logger_sys.log_message("INFO: Dumping player RAM save into its save file")
                    dumped = yaml_handling.dump(player)
                    previous_player = player
                    logger_sys.log_message(f"INFO: Dumping player save data: '{dumped}'")

                    save_file_quit = save_file
                    with open(save_file_quit, "w") as f:
                        f.write(dumped)
                        logger_sys.log_message(f"INFO: Dumping player save data to save '{save_file_quit}'")

                    save_name_backup = save_file.replace('save_', '~0 save_')

                    with open(save_name_backup, "w") as f:
                        f.write(dumped)
                        logger_sys.log_message(f"INFO: Dumping player save data to backup save '{save_name_backup}'")

                    dumped = yaml_handling.dump(preferences)
                    logger_sys.log_message(f"INFO: Dumping player preferences data: '{dumped}'")

                    with open(program_dir + '/preferences.yaml', 'w') as f:
                        f.write(dumped)
                    logger_sys.log_message(f"INFO: Dumping player preferences to file '" + program_dir + "/preferences.yaml'")
                logger_sys.log_message("INFO: Starting player sleeping process")
                if int(player["gold"]) > int(get_cost(zone[map_zone]["sleep gold"], dropoff)):
                    sleep_gold = get_cost(zone[map_zone]["sleep gold"], dropoff, False)
                    logger_sys.log_message(f"INFO: Removed {sleep_gold} from player --> sleep costs")
                    player["gold"] -= sleep_gold
                    loading = 7
                    cout(" ")
                    while loading > 0:
                        cout("Sleeping... Zzz", end='\r')
                        time.sleep(.25)
                        cout("Sleeping... zZz", end='\r')
                        time.sleep(.25)
                        cout("Sleeping... zzZ", end='\r')
                        time.sleep(.25)
                        cout("Sleeping... zzz", end='\r')
                        time.sleep(.25)
                        cout("Sleeping... Zzz", end='\r')
                        time.sleep(.25)
                        cout("Sleeping... zZz", end='\r')
                        time.sleep(.25)
                        cout("Sleeping... zzZ", end='\r')
                        time.sleep(.25)
                        cout("Sleeping... zzz", end='\r')
                        time.sleep(.25)
                        player["health"] += random.randint(1, 7)
                        loading -= 1
                    logger_sys.log_message("INFO: Finished sleeping process")
                    logger_sys.log_message("INFO: Updating correct day time to morning")
                    player["elapsed time game days"] = float(float(round(player["elapsed time game days"] + 1, 0)) + .25)
                    continue_hostel_actions = False
                    if player["health"] > player["max health"]:
                        player["health"] = player["max health"]
                else:
                    logger_sys.log_message("INFO: Canceling sleeping process --> player doesn't own enough gold")
                    cout(COLOR_YELLOW + "You don't own enough gold to sleep here." + COLOR_RESET_ALL)
        elif choice == 'Buy Drink':
            which_drink = cinput("Which drink do you want to buy? ")
            logger_sys.log_message(f"INFO: Player has chosen drink '{which_drink}' to drink")
            if (
                which_drink in zone[map_zone]["sells"]["drinks"]
                and get_cost(drinks[which_drink]["gold"] * zone[map_zone]["cost value"], dropoff) < player["gold"]
            ):
                drink_cost = get_cost(
                    drinks[which_drink]["gold"] * zone[map_zone]["cost value"], dropoff, False
                )
                logger_sys.log_message(f"INFO: Buying drink '{which_drink}' --> removed {drink_cost} gold from player")
                player["gold"] -= drink_cost
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
            which_item = cinput("Which item do you want to buy? ")
            logger_sys.log_message(f"INFO: Player has chosen item '{which_item}' to buy")
            if (
                which_item in zone[map_zone]["sells"]["items"]
                and get_cost(item[which_item]["gold"] * zone[map_zone]["cost value"], dropoff) < player["gold"]
            ):
                if player["inventory slots remaining"] > 0:
                    player["inventory slots remaining"] -= 1
                    logger_sys.log_message(f"INFO: Adding item '{which_item}' to player inventory")
                    player["inventory"].append(which_item)
                    item_cost = get_cost(item[which_item]["gold"] * zone[map_zone]["cost value"], dropoff, False)
                    logger_sys.log_message(f"INFO: Removing {item_cost} gold from player")
                    player["gold"] -= item_cost
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
            which_item = cinput("Which item do you want to sell? ")
            logger_sys.log_message(f"INFO: Player has chosen item '{which_item}' to sell")
            if (
                which_item in zone[map_zone]["buys"]["items"]
                and which_item in player["inventory"]
            ):
                logger_sys.log_message(f"INFO: Removing item '{which_item}' from player inventory")
                player["inventory slots remaining"] += 1
                gold = get_cost(item[which_item]["gold"] * zone[map_zone]["cost value"], dropoff, False)
                logger_sys.log_message(f"INFO: Adding to player {gold} gold")
                player["gold"] += gold
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


def interaction_stable(map_zone, zone, player, item, drinks, mounts, map_location, preferences, time_elapsing_coefficient):
    logger_sys.log_message(f"INFO: Current map zone '{map_zone}' is a stable --> can interact")
    # Check if there's a discount active at this
    # map zone
    if player["discounts"][map_zone]["dropoff"] is not None:
        dropoff = player["discounts"][map_zone]["dropoff"]
    else:
        dropoff = 0
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
        action = terminal_handling.show_menu(options)
        logger_sys.log_message(f"INFO: Player has chosen option '{action}'")
        if action == 'Buy Item':
            which_item = cinput("Which item do you want to buy? ")
            logger_sys.log_message(f"INFO: Player has chosen item '{which_item}' to buy")
            if (
                which_item in zone[map_zone]["stable"]["sells"]["items"]
                and get_cost(item[which_item]["gold"] * zone[map_zone]["cost value"], dropoff) < player["gold"]
            ):
                if player["inventory slots remaining"] > 0:
                    logger_sys.log_message(f"INFO: Adding item '{which_item}' from player inventory")
                    player["inventory slots remaining"] -= 1
                    player["inventory"].append(which_item)
                    gold = get_cost(item[which_item]["gold"] * zone[map_zone]["cost value"], dropoff, False)
                    logger_sys.log_message(f"INFO: Removing {gold} gold from player")
                    player["gold"] -= gold
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
            which_drink = cinput("Which drink do you want to buy? ")
            logger_sys.log_message(f"INFO: Player has chosen drink '{which_drink}' to buy")
            if (
                which_drink in zone[map_zone]["stable"]["sells"]["drinks"]
                and get_cost(drinks[which_drink]["gold"] * zone[map_zone]["cost value"], dropoff) < player["gold"]
            ):
                gold = get_cost(drinks[which_drink]["gold"] * zone[map_zone]["cost value"], dropoff, False)
                logger_sys.log_message(f"INFO: Removing {gold} gold from player")
                player["gold"] -= gold
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
            which_mount = cinput("Which mount do you want to buy? ")
            logger_sys.log_message(f"INFO: Player has chosen mount '{which_mount}' to buy")
            if which_mount in zone[map_zone]["stable"]["sells"]["mounts"]:
                mount_cost = get_cost(mounts[which_mount]["gold"] * zone[map_zone]["cost value"], dropoff, False)
                if mount_cost < player["gold"]:
                    logger_sys.log_message(f"INFO: Removing player {mount_cost} gold")
                    player["gold"] -= mount_cost
                    generated_mount_uuid = uuid_handling.generate_random_uuid()
                    cout("How you mount should be named ?")
                    new_mount_name = cinput(COLOR_GREEN + COLOR_STYLE_BRIGHT + "> " + COLOR_RESET_ALL)
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
                        cout(COLOR_YELLOW + "You already have a mount named like that." + COLOR_RESET_ALL)
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
                            "stats": mount_stats,
                            "mph": mounts[which_mount]["mph"],
                            "health": mounts[which_mount]["stats"]["health"],
                            "current health": mounts[which_mount]["stats"]["health"],
                            "last day health automatically reduced": round(player["elapsed time game days"], 2),
                            "last day health recovered": round(player["elapsed time game days"], 2)
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
                    cout(COLOR_YELLOW + "You don't own enough gold to buy that mount" + COLOR_RESET_ALL)
            else:
                logger_sys.log_message(
                    f"INFO: Canceling buying process --> current stable '{map_zone}'" +
                    f" doesn't sell mount '{which_mount}'"
                )
                cout(COLOR_YELLOW + "The current stable do not sell this mount" + COLOR_RESET_ALL)
        elif action == 'Deposit Mount':
            if player["current mount"] != " ":
                current_mount_uuid = str(player["current mount"])
                mount_data = player["mounts"][current_mount_uuid]
                current_mount = mount_data["name"]
                current_mount_type = mount_data["mount"]
                # check if required stables are in the stable attributes
                required_mount_stable = str(mounts[str(mount_data["mount"])]["stable"]["required stable"])
                if required_mount_stable in zone[map_zone]["stable"]["stables"]:
                    ask = cinput("Do you want to deposit your current mount " + mount_data["name"] + " ? (y/n) ")
                    if ask.lower().startswith('y'):
                        logger_sys.log_message(
                            f"INFO: Depositing currently player ridden mount '{current_mount}'" +
                            f" to map zone '{map_zone}"
                        )
                        player["current mount"] = " "
                        player["mounts"][current_mount_uuid]["is deposited"] = True
                        player["mounts"][current_mount_uuid]["deposited day"] = round(player["elapsed time game days"], 1)
                        player["mounts"][current_mount_uuid]["location"] = str("point" + str(map_location))
                    text = "="
                    text_handling.print_separator(text)
                else:
                    logger_sys.log_message(
                        f"INFO: Canceling depositing process --> current stable '{map_zone}' " +
                        f"doesn't accept mounts of type '{current_mount_type}'"
                    )
                    cout(COLOR_YELLOW + "This stable doesn't accept this type of mount." + COLOR_RESET_ALL)
            else:
                logger_sys.log_message("INFO: Canceling depositing process --> doesn't ride any mounts by now")
                cout(COLOR_YELLOW + "You don't have any mounts to deposit here." + COLOR_RESET_ALL)
        elif action == 'Train Mount':
            if player["current mount"] != ' ':
                current_mount_uuid = str(player["current mount"])
                current_mount_type = str(player["mounts"][current_mount_uuid]["mount"])
                current_mount_data = mounts[current_mount_type]
                if current_mount_data["stable"]["required stable"] in zone[map_zone]["stable"]["stables"]:
                    logger_sys.log_message("INFO: Starting mount training of mount '{current_mount_uuid}'")
                    train.training_loop(
                        current_mount_uuid, player, item, mounts, zone[map_zone], time_elapsing_coefficient, dropoff
                    )
                    player["mounts"][current_mount_uuid]["last day health automatically reduced"] = round(
                        player["elapsed time game days"], 2
                    )
                    to_be_removed = round(
                        mounts[current_mount_type]["feed"]["feed needs"] * 1.015
                    )
                    player["mounts"][current_mount_uuid]["current health"] -= to_be_removed
                    logger_sys.log_message(
                        f"INFO: Removed {to_be_removed} health points to mount '{current_mount_uuid}' " +
                        "because it's finished training"
                    )
                else:
                    logger_sys.log_message(
                        f"INFO: Aborting mount training of mount '{current_mount_uuid}' " +
                        "--> the current stable isn't the right stable type"
                    )
                    cout(
                        COLOR_YELLOW + "The current stable doesn't have the right facilities for this mount" + COLOR_RESET_ALL
                    )
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
                cout("MOUNTS AT THIS STABLE:")
                cout(deposited_mounts_names)
                text = '='
                text_handling.print_separator(text)
                which_mount = cinput(COLOR_GREEN + COLOR_STYLE_BRIGHT + "> " + COLOR_RESET_ALL)
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
                    mount_take_back_cost = get_cost(round(
                        (
                            player["elapsed time game days"] - player["mounts"][which_mount_uuid]["deposited day"]
                        ) * zone[map_zone]["deposit gold"], 2
                    ), dropoff, False)
                    cout(
                        "If you take back this mount it will cost you " + COLOR_YELLOW +
                        COLOR_STYLE_BRIGHT + str(round(mount_take_back_cost, 2)) + COLOR_RESET_ALL + " gold. "
                    )
                    ask = cinput("(y/n) ")
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
                        cout(COLOR_YELLOW + "You don't own enough gold to take back your mount." + COLOR_RESET_ALL)
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
                logger_sys.log_message(f"INFO: Canceling taking back process --> already riding a mount")
                text = (
                    COLOR_YELLOW + "You are currently already riding a mount. You need " +
                    "to deposit your current mount before riding an other one." + COLOR_RESET_ALL
                )
                text_handling.print_long_string(text)
        else:
            active_stable_menu = False


def interaction_blacksmith(map_zone, zone, item, player):
    logger_sys.log_message(f"INFO: Current map zone '{map_zone}' is a blacksmith --> can interact")
    # Check if there's a discount active at this
    # map zone
    if player["discounts"][map_zone]["dropoff"] is not None:
        dropoff = player["discounts"][map_zone]["dropoff"]
    else:
        dropoff = 0
    text = '='
    text_handling.print_separator(text)

    options = ['Sell Equipment', 'Order Equipment', 'Upgrade Equipment', 'Check Order', 'Exit']
    continue_blacksmith_actions = True
    logger_sys.log_message("INFO: Starting blacksmith interact loop")
    while continue_blacksmith_actions:
        action = terminal_handling.show_menu(options)
        logger_sys.log_message(f"INFO: Player has chosen option '{action}'")
        if action == 'Sell Equipment':
            which_weapon = cinput("Which equipment do you want to sell? ")
            logger_sys.log_message(f"INFO: Player has chosen item '{which_weapon}' to sell")
            if which_weapon in zone[map_zone]["blacksmith"]["buys"] and which_weapon in player["inventory"]:
                player["inventory slots remaining"] += 1
                gold = get_cost(item[which_weapon]["gold"] * zone[map_zone]["cost value"], dropoff, False)
                player["gold"] += gold
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
                    f"INFO: Canceling selling process --> current blacksmith '{map_zone}' " +
                    f"doesn't sell item '{which_weapon}' or player doesn't own item '{which_weapon}'"
                )
                text_handling.print_long_string(text)
        elif action == 'Order Equipment':
            which_weapon = cinput("Which equipment do you want to order? ")
            logger_sys.log_message(f"INFO: Player has chosen item '{which_weapon}' to order")
            if (
                which_weapon in zone[map_zone]["blacksmith"]["orders"]
                and player["gold"] > get_cost(zone[map_zone]["blacksmith"]["orders"][which_weapon]["gold"], dropoff)
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
                    gold = get_cost(zone[map_zone]["blacksmith"]["orders"][which_weapon]["gold"], dropoff, False)
                    logger_sys.log_message(f"INFO: Removing from player {gold} gold")
                    player["gold"] -= gold
                    count = 0
                    remaining_items_to_remove = len(zone[map_zone]["blacksmith"]["orders"][which_weapon]["needed materials"])
                    while count < len(player["inventory"]) and remaining_items_to_remove != 0:
                        selected_item = zone[map_zone]["blacksmith"]["orders"][which_weapon]["needed materials"][count]
                        logger_sys.log_message(f"INFO: Removing from player inventory item '{selected_item}'")
                        player["inventory"].remove(selected_item)
                        player["inventory slots remaining"] += 1
                        remaining_items_to_remove -= 1
                        count += 1
                    order_uuid = uuid_handling.generate_random_uuid()
                    logger_sys.log_message(f"INFO: Creating order '{order_uuid}' dictionary")
                    order_dict = {
                        "paid gold": gold,
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
            which_weapon = cinput("Which equipment do you want to upgrade? ")
            logger_sys.log_message(f"INFO: Player has chosen equipment '{which_weapon}' to upgrade")
            if which_weapon in player["inventory"]:
                item_next_upgrade_name = str(weapon_upgrade_handling.check_weapon_next_upgrade_name(which_weapon, item))
                if item_next_upgrade_name != 'None':
                    if player["gold"] > get_cost(item[item_next_upgrade_name]["gold"], dropoff):
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
                            gold = get_cost(item[item_next_upgrade_name]["gold"], dropoff, False)
                            logger_sys.log_message(f"INFO: Removing from player {gold} gold")
                            player["gold"] -= gold
                            player["inventory"].remove(which_weapon)
                            count = 0
                            remaining_items_to_remove = len(item[str(item_next_upgrade_name)]["for this upgrade"])
                            while count < len(player["inventory"]) and remaining_items_to_remove > 0:
                                selected_item = item[str(item_next_upgrade_name)]["for this upgrade"][count]
                                player["inventory"].remove(selected_item)
                                player["inventory slots remaining"] -= 1
                                remaining_items_to_remove -= 1
                                count += 1
                            order_uuid = uuid_handling.generate_random_uuid()
                            logger_sys.log_message(f"INFO: Creating order '{order_uuid}' dictionary")
                            order_dict = {
                                "paid gold": gold,
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
                            cout(COLOR_YELLOW + "You don't own the necessary items to upgrade" + COLOR_RESET_ALL)
                    else:
                        logger_sys.log_message("INFO: Canceling upgrading process --> doesn't has enough gold")
                        cout(COLOR_YELLOW + "You don't have enough gold to upgrade." + COLOR_RESET_ALL)
                else:
                    logger_sys.log_message(
                        f"INFO: Canceling upgrading process --> cannot upgrade equipment '{which_weapon}' further"
                        )
                    cout(
                        COLOR_YELLOW + "You cannot upgrade this equipment further." + COLOR_RESET_ALL
                    )
            else:
                logger_sys.log_message(
                    "INFO: Canceling upgrading process --> player doesn't own any" +
                    f" '{which_weapon}' in its inventory"
                )
                cout(COLOR_YELLOW + "You don't own that equipment" + COLOR_RESET_ALL)
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
                        cout(ordered_blacksmith, ordered_weapon)
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
            cout("ORDERS:")
            cout(player_orders_to_collect)
            text = '='
            text_handling.print_separator(text)
            which_order = cinput(COLOR_GREEN + COLOR_STYLE_BRIGHT + "$ " + COLOR_RESET_ALL)
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
                cout(
                    "ORDERED EQUIPMENT: " + COLOR_RED +
                    str(player["orders"][current_order_uuid]["ordered weapon"]) + COLOR_RESET_ALL
                )
                cout(
                    "PAID GOLD: " + COLOR_YELLOW + COLOR_STYLE_BRIGHT +
                    str(round(player["orders"][current_order_uuid]["paid gold"], 2)) + COLOR_RESET_ALL
                )
                ordered_day = time_handling.date_prettifier(
                    time_handling.addition_to_date(
                        player["starting date"], int(player["orders"][current_order_uuid]["ordered day"])
                    )
                )
                cout(
                    "ORDERED DATE: " + COLOR_MAGENTA + COLOR_STYLE_BRIGHT +
                    ordered_day + COLOR_RESET_ALL
                )
                cout("TIME LEFT: " + COLOR_CYAN + COLOR_STYLE_BRIGHT + str(time_left) + COLOR_RESET_ALL)

                text = '='
                text_handling.print_separator(text)
                options_order = ['Cancel Order']
                if time_left == "READY TO COLLECT":
                    options_order += ['Collect Order']
                options_order += ['Exit']
                action = terminal_handling.show_menu(options_order)
                logger_sys.log_message(f"INFO: Player has chosen option '{action}'")
                if action == 'Cancel Order':
                    text = (
                        "Are you sure you want to cancel this order? You will receive " +
                        "75% of the gold you paid and you won't be able"
                    )
                    text_handling.print_long_string(text)
                    ask = cinput(" to get your given items back. (y/n)")
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
                    if player["inventory slots remaining"] > 0:
                        player["inventory"].append(str(player["orders"][current_order_uuid]["ordered weapon"]))
                        player["inventory slots remaining"] -= 1
                        # remove order from player orders
                        player["orders"].pop(current_order_uuid)
                    else:
                        logger_sys.log_message(
                            "INFO: Canceling collecting order process --> player hasn't " +
                            f"enough inventory slots remaining"
                        )
                        cout(COLOR_YELLOW + "You don't have enough inventory slots remaining." + COLOR_RESET_ALL)
            else:
                logger_sys.log_message(
                    "INFO: Canceling collecting order process --> player has no order " +
                    f"'{which_order}' at map zone '{map_zone}'"
                )
                cout(COLOR_YELLOW + "You don't have this order currently at this place." + COLOR_RESET_ALL)
        else:
            continue_blacksmith_actions = False


def interaction_forge(map_zone, zone, player, item):
    logger_sys.log_message(f"INFO: map zone '{map_zone}' is a forge --> can interact")
    # Check if there's a discount active at this
    # map zone
    if player["discounts"][map_zone]["dropoff"] is not None:
        dropoff = player["discounts"][map_zone]["dropoff"]
    else:
        dropoff = 0
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
        choice = terminal_handling.show_menu(options)
        logger_sys.log_message(f"INFO: Player has chosen option '{choice}'")
        if choice == 'Sell Metals':
            which_metal = cinput("Which metal do you want to sell? ")
            logger_sys.log_message(f"INFO: Player has chosen metal '{which_metal}' to sell")
            if which_metal in current_forge["forge"]["buys"]:
                cout(
                    f"You currently own {COLOR_CYAN}{player["inventory"].count(which_metal)}" +
                    f"{COLOR_RESET_ALL} of this metal."
                )
                metal_count = cinput_int("How many count of this metal you want to sell? ")
                logger_sys.log_message(f"INFO: Player has chosen to sell '{metal_count}' of the metal '{which_metal}'")
                if player["inventory"].count(which_metal) >= metal_count:
                    gold = get_cost(
                        item[which_metal]["gold"] * current_forge["cost value"] * metal_count, dropoff, False
                    )
                    logger_sys.log_message(f"INFO: Adding {gold} gold to player")
                    player["gold"] += gold
                    count = 0
                    while count < metal_count:
                        logger_sys.log_message(f"INFO: Removing from player inventory item '{which_metal}'")
                        player["inventory"].remove(which_metal)
                        player["inventory slots remaining"] += 1
                        count += 1
                else:
                    logger_sys.log_message(
                        "INFO: Canceling selling process --> doesn't has " +
                        f"{metal_count} '{which_metal}' in player's inventory"
                    )
                    cout(COLOR_YELLOW + "You don't own that many count of this metal" + COLOR_RESET_ALL)
            else:
                logger_sys.log_message(
                    f"INFO: Canceling selling process --> current forge '{map_zone}' doesn't sell metal '{which_metal}'"
                )
                cout(COLOR_YELLOW + "The current forge doesn't buys this metal" + COLOR_RESET_ALL)
        elif choice == 'Buy Metals':
            which_metal = cinput("Which metal do you want to buy? ")
            logger_sys.log_message(f"INFO: Player has chosen item '{which_metal}' to buy")
            if which_metal in current_forge["forge"]["sells"]:
                metal_count = cinput_int("How many count of this metal you want to buy? ")
                if player["gold"] >= get_cost(
                    item[which_metal]["gold"] * current_forge["cost value"] * metal_count, dropoff
                ):
                    if player["inventory slots remaining"] >= metal_count:
                        gold = get_cost(
                            item[which_metal]["gold"] * current_forge["cost value"] * metal_count, dropoff, False
                        )
                        logger_sys.log_message(f"INFO: Removing from player {gold} gold")
                        player["gold"] -= gold
                        count = 0
                        while count < metal_count:
                            logger_sys.log_message(f"INFO: Adding to player inventory item '{which_metal}")
                            player["inventory"].append(which_metal)
                            player["inventory slots remaining"] -= 1
                            count += 1
                    else:
                        logger_sys.log_message(
                            f"INFO: Canceling buying process --> doesn't have enough inventory slots"
                        )
                        cout(COLOR_YELLOW + "You don't enough remaining inventory slots" + COLOR_RESET_ALL)
                else:
                    logger_sys.log_message(f"INFO: Canceling buying process --> doesn't have enough gold")
                    cout(COLOR_YELLOW + "You don't own enough gold to buy that many metal" + COLOR_RESET_ALL)
            else:
                logger_sys.log_message(
                    f"INFO: Canceling buying process --> current forge '{map_zone}'" +
                    f" doesn't sell item '{which_metal}'"
                )
                cout(COLOR_YELLOW + "The current forge doesn't sells this metal" + COLOR_RESET_ALL)
        else:
            continue_forge_actions = False


def interaction_church(map_zone, zone, player, save_file, preferences, previous_player):
    logger_sys.log_message(f"INFO: map zone '{map_zone}' is a church --> can interact")
    current_church = zone[map_zone]
    text = '='
    text_handling.print_separator(text)
    options = ['Rest', 'Donate', 'Exchange EXP', 'Exit']
    continue_church_actions = True
    logger_sys.log_message("INFO: Starting church interact loop")
    while continue_church_actions:
        choice = terminal_handling.show_menu(options)
        logger_sys.log_message(f"INFO: Player has chosen option '{choice}'")
        if choice == 'Rest':
            if player["difficulty mode"] >= 1:
                logger_sys.log_message("INFO: Dumping player RAM save into its save file")
                dumped = yaml_handling.dump(player)
                previous_player = player
                logger_sys.log_message(f"INFO: Dumping player save data: '{dumped}'")

                save_file_quit = save_file
                with open(save_file_quit, "w") as f:
                    f.write(dumped)
                    logger_sys.log_message(f"INFO: Dumping player save data to save '{save_file_quit}'")

                save_name_backup = save_file.replace('save_', '~0 save_')

                with open(save_name_backup, "w") as f:
                    f.write(dumped)
                    logger_sys.log_message(f"INFO: Dumping player save data to backup save '{save_name_backup}'")

                dumped = yaml_handling.dump(preferences)
                logger_sys.log_message(f"INFO: Dumping player preferences data: '{dumped}'")

                with open(program_dir + '/preferences.yaml', 'w') as f:
                    f.write(dumped)
                logger_sys.log_message(f"INFO: Dumping player preferences to file '" + program_dir + "/preferences.yaml'")
            logger_sys.log_message("INFO: Starting player resting process")
            loading = 7
            cout(" ")
            while loading > 0:
                cout("Resting... -__", end='\r')
                time.sleep(.25)
                cout("Resting... _-_", end='\r')
                time.sleep(.25)
                cout("Resting... __-", end='\r')
                time.sleep(.25)
                cout("Resting... ___", end='\r')
                time.sleep(.25)
                cout("Resting... -__", end='\r')
                time.sleep(.25)
                cout("Resting... _-_", end='\r')
                time.sleep(.25)
                cout("Resting... __-", end='\r')
                time.sleep(.25)
                cout("Resting... ___", end='\r')
                time.sleep(.25)
                loading -= 1
            logger_sys.log_message("INFO: Finished resting process")
            continue_church_actions = False
            player["health"] += (
                player["max health"] * current_church["rest hp restoring percentage"]
            )
            if player["health"] > player["max health"]:
                player["health"] = player["max health"]
        elif choice == 'Donate':
            donations = ['25', '45', '65', '75', '85']
            how_much = int(terminal_handling.show_menu(donations, length=7))
            logger_sys.log_message(f"INFO: Player has chosen to donate {how_much} gold to the church")
            if how_much <= player["gold"]:
                player["gold"] -= how_much
                exp = round(how_much / 2.2, 2)
                player["xp"] += exp
                logger_sys.log_message(f"INFO: Player has gained {exp} experience for his donation")
            else:
                cout(COLOR_YELLOW + "You don't own that many gold" + COLOR_RESET_ALL)
                logger_sys.log_message(f"INFO: Canceling donation process --> doesn't own enough money")
        elif choice == 'Exchange EXP':
            exchanges = ['35', '40', '55', '75', '80', '125']
            how_much = int(terminal_handling.show_menu(exchanges, length=8))
            logger_sys.log_message(f"INFO: Player has chosen to exchange {how_much} experience")
            if how_much <= player["xp"]:
                player["xp"] -= how_much
                health_points = round(
                    (
                        current_church["exp exchange max health percentage"] * how_much
                    ) * random.uniform(.85, 1.15)
                )
                player["max health"] += health_points
                logger_sys.log_message(f"INFO: Player has gained {health_points} max health points")
            else:
                cout(COLOR_YELLOW + "You don't own that many EXP" + COLOR_RESET_ALL)
                logger_sys.log_message(f"INFO: Canceling EXP exchange process --> doesn't own enough EXP")
        else:
            continue_church_actions = False


def interaction_grocery(map_zone, zone, player, item):
    logger_sys.log_message(f"INFO: map zone '{map_zone}' is a grocery --> can interact")
    # Check if there's a discount active at this
    # map zone
    if player["discounts"][map_zone]["dropoff"] is not None:
        dropoff = player["discounts"][map_zone]["dropoff"]
    else:
        dropoff = 0
    current_grocery = zone[map_zone]
    text = '='
    text_handling.print_separator(text)
    options = ['Buy Item', 'Sell Item', 'Exit']
    continue_grocery_actions = True
    logger_sys.log_message("INFO: Starting grocery interact loop")
    while continue_grocery_actions:
        choice = terminal_handling.show_menu(options)
        logger_sys.log_message(f"INFO: Player has chosen option '{choice}'")
        if choice == "Buy Item":
            which_item = cinput("Which item do you want to buy? ")
            logger_sys.log_message(f"INFO: Player has chosen item '{which_item}' to buy")
            if which_item in player["groceries data"][map_zone]["items sales"]:
                if player["gold"] >= get_cost(
                    item[which_item]["gold"] * current_grocery["cost value"], dropoff
                ):
                    if player["inventory slots remaining"] > 0:
                        gold = get_cost(
                            item[which_item]["gold"] * current_grocery["cost value"], dropoff, False
                        )
                        logger_sys.log_message(f"INFO: Removing from player {gold} gold")
                        player["gold"] -= gold
                        logger_sys.log_message(f"INFO: Adding to player inventory item '{which_item}")
                        player["inventory"].append(which_item)
                        player["inventory slots remaining"] -= 1
                    else:
                        logger_sys.log_message(
                            f"INFO: Canceling buying process --> doesn't have enough inventory slots"
                        )
                        cout(COLOR_YELLOW + "You don't have enough space in your inventory" + COLOR_RESET_ALL)
                else:
                    logger_sys.log_message(f"INFO: Canceling buying process --> doesn't have enough gold")
                    cout(COLOR_YELLOW + "You don't own enough gold to buy that many item" + COLOR_RESET_ALL)
            else:
                logger_sys.log_message(
                    f"INFO: Canceling buying process --> current grocery '{map_zone}'" +
                    f" doesn't sell item '{which_item}'"
                )
                cout(COLOR_YELLOW + "The current grocery doesn't sells this item" + COLOR_RESET_ALL)
        elif choice == 'Sell Item':
            which_item = cinput("Which item do you want to sell? ")
            logger_sys.log_message(f"INFO: Player has chosen item '{which_item}' to sell")
            if which_item in player["inventory"]:
                cout(
                    f"You currently own {COLOR_CYAN}{player["inventory"].count(which_item)}" +
                    f"{COLOR_RESET_ALL} of this item."
                )
                item_number = cinput_int("How many items of that type do you want to sell? ")
                logger_sys.log_message(f"INFO: Player has chosen to sell '{item_number}' of the item '{which_item}'")
                if player["inventory"].count(which_item) >= item_number:
                    gold = get_cost(
                        (
                            item[which_item]["gold"] * current_grocery["cost value"]
                        ) * item_number * random.uniform(.85, 1.35), dropoff, False
                    )
                    cout(
                        f"\n{COLOR_YELLOW}You've found someone that accepted to buy " +
                        f"{item_number} of your \n'{which_item}' for a price of" +
                        f" {round(gold / item_number, 2)} gold coins per unit.{COLOR_RESET_ALL}"
                    )
                    logger_sys.log_message(f"INFO: Adding {gold} gold to player")
                    player["gold"] += gold
                    count = 0
                    while count < item_number:
                        logger_sys.log_message(f"INFO: Removing from player inventory item '{which_item}'")
                        player["inventory"].remove(which_item)
                        player["inventory slots remaining"] += 1
                        count += 1
                else:
                    logger_sys.log_message(
                        "INFO: Canceling selling process --> doesn't has " +
                        f"'{which_item}' in player's inventory"
                    )
                    cout(COLOR_YELLOW + "You don't own that many count of this item" + COLOR_RESET_ALL)
            else:
                logger_sys.log_message(
                    "INFO: Canceling selling process --> doesn't has " +
                    f"'{which_item}' in player's inventory"
                )
                cout(COLOR_YELLOW + "You don't own that many count of this item" + COLOR_RESET_ALL)
        else:
            continue_grocery_actions = False


def interaction_harbor(map_zone, zone, map, player):
    logger_sys.log_message(f"INFO: map zone '{map_zone}' is a harbor --> can interact")
    # Check if there's a discount active at this
    # map zone
    if player["discounts"][map_zone]["dropoff"] is not None:
        dropoff = player["discounts"][map_zone]["dropoff"]
    else:
        dropoff = 0
    current_harbor = zone[map_zone]
    text = '='
    text_handling.print_separator(text)
    options = ['Buy Ticket', 'Exit']
    continue_harbor_actions = True
    logger_sys.log_message("INFO: Starting harbor interact loop")
    while continue_harbor_actions:
        choice = terminal_handling.show_menu(options)
        logger_sys.log_message(f"INFO: Player has chosen option '{choice}'")
        if choice == "Buy Ticket":
            which_ticket = cinput("Which ticket do you want to buy? ")
            if which_ticket in list(current_harbor["travels"]):
                gold = get_cost(current_harbor["travels"][which_ticket]["cost"], dropoff, False)
                if player["gold"] >= gold:
                    player["gold"] -= gold
                    logger_sys.log_message(f"INFO: Removing from player {gold} gold")
                    destination = map[f"point{current_harbor['travels'][which_ticket]['destination']}"]
                    player["x"], player["y"] = destination["x"], destination["y"]
                    travel_time = current_harbor["travels"][which_ticket]["travel time"]
                    logger_sys.log_message("INFO: Starting player traveling process")
                    cout(" ")
                    overall_time = 0
                    while overall_time < travel_time:
                        starting_time = time.time()
                        cout("Traveling... >--", end='\r')
                        time.sleep(.25)
                        cout("Traveling... ->-", end='\r')
                        time.sleep(.25)
                        cout("Traveling... -->", end='\r')
                        time.sleep(.25)
                        cout("Traveling... ---", end='\r')
                        time.sleep(.25)
                        cout("Traveling... >--", end='\r')
                        time.sleep(.25)
                        cout("Traveling... ->-", end='\r')
                        time.sleep(.25)
                        cout("Traveling... -->", end='\r')
                        time.sleep(.25)
                        cout("Traveling... ---", end='\r')
                        time.sleep(.25)
                        overall_time += time.time() - starting_time
                    logger_sys.log_message("INFO: Finished traveling process")
                    continue_harbor_actions = False
                else:
                    logger_sys.log_message(
                        "INFO: Canceling ticket buying process --> player" +
                        f"doesn't have enough gold"
                    )
                    cout(COLOR_YELLOW + "You don't own enough gold to buy this ticket" + COLOR_RESET_ALL)
            else:
                logger_sys.log_message(
                    "INFO: Canceling ticket buying process --> current harbor" +
                    f"doesn't have a ticket named '{which_ticket}'"
                )
                cout(COLOR_YELLOW + "There isn't any ticket named that" + COLOR_RESET_ALL)
        else:
            continue_harbor_actions = False


def interaction_dungeon(
    map_zone, zone, map, player, dialog, item, preferences, text_replacements_generic,
    drinks, enemy, npcs, start_player, lists, mission, mounts, start_time,
    map_location, player_damage_coefficient, enemies_damage_coefficient, previous_player, save_file
):
    logger_sys.log_message(f"INFO: map zone '{map_zone}' is a dungeon --> can interact")
    current_dungeon = zone[map_zone]
    if map_zone not in player["completed dungeons"]:
        text = '='
        text_handling.print_separator(text)
        options = ['Enter Dungeon', 'Check Dungeon Map', 'Exit']
        if "dungeon map" not in current_dungeon["dungeon"]:
            options.remove(options[1])
        continue_dungeon_actions = True
        logger_sys.log_message("INFO: Starting dungeon interact loop")
        while continue_dungeon_actions:
            choice = terminal_handling.show_menu(options)
            logger_sys.log_message(f"INFO: Player has chosen option '{choice}'")
            if choice == 'Enter Dungeon':
                cout("\nAre you sure you want to enter the dungeon?")
                cout("You won't be able to exit the dungeon once in it,")
                ask = cinput("until you complete it. (y/n) ")
                if ask.lower().startswith('y'):
                    enter_dungeon = dungeon.dungeon_loop(
                        player, current_dungeon, lists, enemy, start_player, item, start_time, preferences,
                        npcs, drinks, zone, mounts, dialog, mission, map_location, text_replacements_generic,
                        player_damage_coefficient, enemies_damage_coefficient, previous_player, save_file,
                        map
                    )
                    text_handling.clear_prompt()
                    if enter_dungeon:  # check if the player has completed the dungeon and not just exited it
                        player["completed dungeons"] += [map_zone]
                        dialog_handling.print_dialog(
                            current_dungeon["dungeon"]["reward dialog"], dialog, preferences,
                            text_replacements_generic, player, drinks, item, enemy, npcs,
                            start_player, lists, zone, mission, mounts, start_time, map,
                            save_file, player_damage_coefficient, enemies_damage_coefficient,
                            previous_player
                        )
                        cinput("\nPress enter to continue...")
                    continue_dungeon_actions = False
            elif choice == 'Check Dungeon Map':
                cout("")
                cout("╔" + ("═" * 53) + "╗")
                map_data = {
                    "map": current_dungeon["dungeon"]["dungeon map"]
                }
                text_handling.print_map_art(map_data)
                cout("╚" + ("═" * 53) + "╝")
                cinput()
            else:
                continue_dungeon_actions = False
    else:
        cout(COLOR_YELLOW + "You've already completed this dungeon!" + COLOR_RESET_ALL)
        time.sleep(2)


# Other handling functions


def get_map_point_distance_from_player(map, player, current_map_point):
    point_x, point_y = map[current_map_point]["x"], map[current_map_point]["y"]
    point_x, point_y = text_handling.transform_negative_number_to_positive(
        point_x
    ), text_handling.transform_negative_number_to_positive(point_y)
    player_x, player_y = player["x"], player["y"]
    player_x, player_y = text_handling.transform_negative_number_to_positive(
        player_x
    ), text_handling.transform_negative_number_to_positive(player_y)

    point_distance_from_player = (point_x - player_x) + (point_y - player_y)
    point_distance_from_player = text_handling.transform_negative_number_to_positive(
        point_distance_from_player
    )
    return point_distance_from_player


def get_zone_nearest_point(map, player, map_zone_name):
    # Get matching points and then for each of them,
    # get their distance from the player location and
    # finally determine which one is the closest from the player
    closest_map_point = None
    matching_points = []
    distances = []
    for point in list(map):
        if map[point]["map zone"] == map_zone_name:
            matching_points += [point]

    for point in matching_points:
        point_distance_from_player = get_map_point_distance_from_player(
            map, player, point
        )
        distances += [point_distance_from_player]

    distances.sort()  # sort the list so that the lowest value is at index 0
    for point in matching_points:
        if get_map_point_distance_from_player(map, player, point) == distances[0]:
            closest_map_point = point

    return closest_map_point


def determine_grocery_sales(zone_data):
    # Get the length of the items and define
    # an approximate number of items that're
    # going to be sold. After that, randomly
    # choose the items to be sold
    sales_length = len(zone_data["items sold"])
    sales_length -= int(random.uniform(sales_length / 3, sales_length / 4.6))

    sales = []
    for i in range(sales_length):
        sale = zone_data["items sold"][i]
        if sale not in sales and random.uniform(0, 1) > .5:
            sales += [sale]

    return sales


def get_zone_color(zone_type):
    global zone_color
    zone_color = COLOR_BLACK
    try:
        with open(program_dir + '/game/schemas/zones_colors.yaml', 'r') as f:
            zones_colors = yaml_handling.safe_load(f)
            zone_code = zones_colors[str(zone_type)]
            zone_color = ZONE_COLORS_DICT[zone_code]
    except Exception as error:
        cout(COLOR_RED + "ERROR: " + COLOR_STYLE_BRIGHT + f"zone type '{zone_type}' isn't a valid zone type." + COLOR_RESET_ALL)
        cout(error)
        text_handling.exit_game()
    return zone_color
