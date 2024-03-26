# source imports
import battle
import logger_sys
import terminal_handling
import text_handling
from colors import *
from terminal_handling import cout
# external imports
import random
import appdirs
import yaml
import time
from sys import exit


program_dir = str(appdirs.user_config_dir(appname='Bane-Of-Wargs'))
# Handling function


def generate_enemies_from_list(lists, list_enemies, player):
    # First, we settle up some variables.
    # Then, we choose which entry to choose. After
    # determining the entry to choose, we determine
    # how many enemies to spawn and then, finally,
    # we generate the list of enemies to spawn.
    list_enemies = lists[list_enemies]
    enemies = []
    chosen_entry = None
    enemies_number = None
    difficulty = None

    count = 0
    finished = False
    while not finished:
        entry = list_enemies[list(list_enemies)[count]]
        if entry["chance"] > random.uniform(0, 1):
            chosen_entry = entry
            finished = True
        count += 1
        if count > len(list(list_enemies)) - 1:  # forces to choose
            count = 0

    if player["difficulty mode"] == 0:
        difficulty = "easy"
    elif player["difficulty mode"] == 1:
        difficulty = "normal"
    else:
        difficulty = "hard"

    enemies_number = random.randint(
        chosen_entry["enemies rate"][difficulty]["min"],
        chosen_entry["enemies rate"][difficulty]["max"]
    )

    count = 0
    while len(enemies) < enemies_number:
        enemy_id = list(chosen_entry["enemies spawns"])[count]
        enemy = chosen_entry["enemies spawns"][enemy_id]
        if enemy > random.uniform(0, 1):
            enemies += [enemy_id]

        count += 1
        if count > len(list(chosen_entry["enemies spawns"])) - 1:  # forces to choose
            count = 0

    return enemies, entry


def spawn_enemy(
    map_location, list_enemies, enemy, item, lists, start_player, map, player,
    preferences, drinks, npcs, zone, mounts, mission, dialog, player_damage_coefficient,
    text_replacements_generic, start_time, previous_player, save_file,
    enemies_damage_coefficient
):
    already_encountered = False
    logger_sys.log_message(f"INFO: Choosing random enemies from the list '{list_enemies}'")
    enemies, entry_data = generate_enemies_from_list(lists, list_enemies, player)
    enemies_remaining = len(enemies)
    while enemies_remaining > 0:

        enemies_total_inventory = []
        for entry in enemies:
            entry = enemy[entry]["inventory"]
            for i in entry:
                enemies_total_inventory += [i]

        enemies_items_number = len(enemies_total_inventory)
        logger_sys.log_message("INFO: Choosing randomly the item that will drop from the enemies")
        chosen_item = enemies_total_inventory[random.randint(0, enemies_items_number - 1)]

        logger_sys.log_message("INFO: Calculating battle risk for the player")
        risk = 0
        for chosen_enemy in enemies:
            risk += battle.calculate_player_risk(
                player, item, enemies_remaining, enemy[chosen_enemy], enemy, player_damage_coefficient,
                enemies_damage_coefficient
            )
        risk = int(risk / len(enemies))
        if not already_encountered:
            logger_sys.log_message("INFO: Display enemy encounter text")
            battle.encounter_text_show(
                player, item, enemy, map, map_location, enemies_remaining, lists,
                risk, preferences, drinks, npcs, zone, mounts, mission,
                start_player, dialog, text_replacements_generic, player_damage_coefficient,
                previous_player, save_file, start_time, enemies_damage_coefficient,
                entry_data, enemies
            )
            already_encountered = True
        logger_sys.log_message("INFO: Starting the fight")
        battle.fight(
            player, item, enemy, map, map_location, enemies_remaining, lists,
            preferences, drinks, npcs, start_player, zone, dialog, mission, mounts,
            player_damage_coefficient, start_time, text_replacements_generic,
            previous_player, save_file, enemies_damage_coefficient, risk,
            entry_data, enemies
        )
        enemies_remaining -= 1

    if player["health"] > 0:

        if random.randint(0, 3) >= 2.5:
            chosen_item = "Gold"

        if chosen_item == "Gold":
            cout("Your enemy dropped some " + chosen_item)
        else:
            cout("Your enemy dropped " + text_handling.a_an_check(chosen_item))
        options = ['Grab Item', 'Continue']
        drop = terminal_handling.show_menu(options)
        text = '='
        text_handling.print_separator(text)
        if drop == 'Grab Item':
            if chosen_item == "Gold":
                player["gold"] += round(random.uniform(1.00, 6.30), 2)
            else:
                if chosen_item in player["inventory"] and item[chosen_item]["type"] == "Utility":
                    cout("You cannot take that item")
                elif player["inventory slots remaining"] == 0:
                    cout("You cannot take that item, you don't have enough slots in your inventory")
                else:
                    player["inventory"].append(chosen_item)
        cout(" ")
    else:
        text = "You just died and your save have been rested to its older state."
        logger_sys.log_message("INFO: Player just died")
        cout(COLOR_RED + COLOR_STYLE_BRIGHT, end="")
        text_handling.print_long_string(text)
        cout(COLOR_RESET_ALL, end="")
        time.sleep(3)
        logger_sys.log_message("INFO: Resetting player save")
        with open(save_file, "r") as f:
            player = yaml.safe_load(f)
        dumped = yaml.dump(player)
        logger_sys.log_message(f"INFO: Dumping player save data: '{dumped}'")

        save_file_quit = save_file
        with open(save_file_quit, "w") as f:
            f.write(dumped)
        logger_sys.log_message(f"INFO: Dumping player save data to save '{save_file_quit}'")

        dumped = yaml.dump(preferences)
        logger_sys.log_message(f"INFO: Dumping player preferences data: '{dumped}'")

        with open(program_dir + '/preferences.yaml', 'w') as f:
            f.write(dumped)
        logger_sys.log_message(f"INFO: Dumping player preferences to file '" + program_dir + "/preferences.yaml'")
        text_handling.clear_prompt()
        logger_sys.log_message(f"INFO: PROGRAM RUN END")
        exit(0)
