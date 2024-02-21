import yaml
import random
import os
import sys
import time
import term_menu
import text_handling
import time_handling
from colors import *
from colorama import Fore, Back, Style, init, deinit

# initialize colorama
init()


def training_loop(mount_uuid, player, item, mounts, stable, time_elapsing_coefficient):
    still_training = True
    current_mount_type = str(player["mounts"][str(mount_uuid)]["mount"])
    current_mount_feeds = mounts[current_mount_type]["feed"]["food"]
    while still_training:
        options = ['Feed', 'Train', 'Exit']
        choice = term_menu.show_menu(options)
        if choice == 'Feed':
            # get player possible feeding items
            count = 0
            player_feeding_items = []
            while count < len(player["inventory"]):
                current_item = str(player["inventory"][count])
                if current_item in current_mount_feeds and current_item not in player_feeding_items:
                    player_feeding_items += [current_item]

                count += 1
            player_feeding_items_text = str(player_feeding_items)
            if player_feeding_items == []:
                player_feeding_items_text = "['None']"
            player_feeding_items_text = player_feeding_items_text.replace("'", '')
            player_feeding_items_text = player_feeding_items_text.replace("[", ' -')
            player_feeding_items_text = player_feeding_items_text.replace("]", '')
            player_feeding_items_text = player_feeding_items_text.replace(", ", '\n -')
            text = '='
            text_handling.print_separator(text)
            print("FEEDING ITEMS:")
            print(player_feeding_items_text)
            text_handling.print_separator(text)
            which_food = str(input(COLOR_GREEN + COLOR_STYLE_BRIGHT + "> " + COLOR_RESET_ALL))
            if which_food in player_feeding_items and which_food in player["inventory"]:
                player["inventory"].remove(which_food)
                player["xp"] += random.randint(1, 4)
                if player["current mount"] in player["mounts"]:
                    player["mounts"][player["current mount"]]["level"] += round(
                        random.uniform(.02, .10), 3
                    ) / mounts[current_mount_type]["feed"]["feed needs"]
            else:
                text = COLOR_YELLOW + "You cannot feed your mount with this food or you don't own that food." + COLOR_RESET_ALL
                text_handling.print_long_string(text)
        elif choice == 'Train':
            # get start time
            start_time = time.time()

            loading = 15
            print(" ")
            while loading > 0:
                print("Training...", end='\r')
                time.sleep(.25)
                print("Training*..", end='\r')
                time.sleep(.25)
                print("Training.*.", end='\r')
                time.sleep(.25)
                print("Training..*", end='\r')
                time.sleep(.25)
                print("Training..*", end='\r')
                time.sleep(.25)
                print("Training.*.", end='\r')
                time.sleep(.25)
                print("Training*..", end='\r')
                time.sleep(.25)
                print("Training...", end='\r')
                time.sleep(.25)
                player["mounts"][player["current mount"]]["level"] += round(random.uniform(.01, .09), 3)
                player["xp"] += round(random.uniform(.01, .13), 1)
                loading -= 1

            # get end time
            end_time = time.time()

            # calculate elapsed time
            elapsed_time = end_time - start_time
            elapsed_time = round(elapsed_time, 2)
            game_elapsed_time = time_handling.return_game_day_from_seconds(elapsed_time, time_elapsing_coefficient)
            game_elapsed_time = round(game_elapsed_time, 2)
            player["gold"] -= stable["training gold"] * game_elapsed_time
        else:
            still_training = False
