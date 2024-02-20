import battle
import logger_sys
import random
import sys
import colors
import term_menu
import text_handling
from colors import *
from colorama import Fore, Back, Style, init, deinit

# initialize colorama
init()

# Handling function


def spawn_enemy(
    map_location, list_enemies, enemy_number, enemy, item, lists, start_player, map, player,
    preferences, drinks, npcs, zone, mounts, mission, dialog, player_damage_coefficient
):
    enemies_remaining = enemy_number
    already_encountered = False
    while enemies_remaining > 0:
        logger_sys.log_message(f"INFO: Choosing random enemy from the list '{list_enemies}'")
        choose_rand_enemy = random.randint(0, len(list_enemies) - 1)
        choose_rand_enemy = list_enemies[choose_rand_enemy]
        chosen_enemy = enemy[choose_rand_enemy]

        enemy_total_inventory = chosen_enemy["inventory"]

        enemy_items_number = len(enemy_total_inventory)
        logger_sys.log_message("INFO: Choosing randomly the item that will drop from the enemies")
        chosen_item = enemy_total_inventory[random.randint(0, enemy_items_number - 1)]
        logger_sys.log_message("INFO: Calculating battle risk for the player")
        defeat_percentage = battle.calculate_player_risk(
            player, item, enemies_remaining, chosen_enemy, enemy, player_damage_coefficient
        )
        logger_sys.log_message("INFO: Getting enemy stats")
        battle.get_enemy_stats(
            player, item, enemy, map, map_location, lists, choose_rand_enemy,
            chosen_enemy, chosen_item, enemy_items_number,
            enemy_total_inventory, enemies_remaining
            )
        if not already_encountered:
            logger_sys.log_message("INFO: Display enemy encounter text")
            battle.encounter_text_show(
                player, item, enemy, map, map_location, enemies_remaining, lists,
                defeat_percentage, preferences, drinks, npcs, zone, mounts, mission, start_player, dialog
            )
            already_encountered = True
        logger_sys.log_message("INFO: Starting the fight")
        battle.fight(
            player, item, enemy, map, map_location, enemies_remaining, lists,
            preferences, drinks, npcs, start_player, zone, dialog, mission, mounts,
            player_damage_coefficient
        )
        enemies_remaining -= 1

    if player["health"] > 0:

        if random.randint(0, 3) >= 2.5:
            chosen_item = "Gold"

        if chosen_item == "Gold":
            print("Your enemy dropped some " + chosen_item)
        else:
            print("Your enemy dropped " + text_handling.a_an_check(chosen_item))
        options = ['Grab Item', 'Continue']
        drop = term_menu.show_menu(options)
        text = '='
        text_handling.print_separator(text)
        if drop == 'Grab Item':
            if chosen_item == "Gold":
                player["gold"] += round(random.uniform(1.00, 6.30), 2)
            else:
                if chosen_item in player["inventory"] and item[chosen_item]["type"] == "Utility":
                    print("You cannot take that item")
                elif player["inventory slots remaining"] == 0:
                    print("You cannot take that item, you don't have enough slots in your inventory")
                else:
                    player["inventory"].append(chosen_item)
        print(" ")
        player["defeated enemies"].append(map_location)
    else:
        text = COLOR_RED + COLOR_STYLE_BRIGHT + "You just died and your save have been reset." + COLOR_RESET_ALL
        logger_sys.log_message("INFO: Player just died")
        text_handling.print_long_string(text)
        input()
        logger_sys.log_message("INFO: Resetting player save")
        player = start_player
        play = 0
        return play


# deinitialize colorama
deinit()
