# source imports
import term_menu
import text_handling
import time_handling
import logger_sys
from colors import *
# external imports
import random
import time


def training_loop(mount_uuid, player, item, mounts, stable, time_elapsing_coefficient):
    logger_sys.log_message(f"INFO: Starting training loop of mount '{mount_uuid}'")
    still_training = True
    current_mount_type = str(player["mounts"][str(mount_uuid)]["mount"])
    current_mount_feeds = mounts[current_mount_type]["feed"]["food"]
    # get start time
    start_time = time.time()
    logger_sys.log_message(f"INFO: Getting start time of training loop: {start_time}")
    while still_training:
        options = ['Feed', 'Train', 'Exit']
        choice = term_menu.show_menu(options)
        logger_sys.log_message(f"INFO: Player has chosen to '{choice}'")
        if choice == 'Feed':
            # get player possible feeding items
            count = 0
            logger_sys.log_message("INFO: Getting mount feeding items")
            mount_feeding_items = mounts[player["mounts"][mount_uuid]["mount"]]["feed"]["food"]
            mount_feeding_items_text = str(mount_feeding_items)
            logger_sys.log_message(f"INFO: Got mount feeding items: {mount_feeding_items}")
            if mount_feeding_items == []:
                mount_feeding_items_text = "['None']"
            mount_feeding_items_text = mount_feeding_items_text.replace("'", '')
            mount_feeding_items_text = mount_feeding_items_text.replace("[", ' -')
            mount_feeding_items_text = mount_feeding_items_text.replace("]", '')
            mount_feeding_items_text = mount_feeding_items_text.replace(", ", '\n -')
            text = '='
            text_handling.print_separator(text)
            print("MOUNT FEEDING ITEMS:")
            print(mount_feeding_items_text)
            text_handling.print_separator(text)
            which_food = str(input(COLOR_GREEN + COLOR_STYLE_BRIGHT + "> " + COLOR_RESET_ALL))
            can_be_bought = False
            if "items" in stable["stable"]["sells"]:
                if which_food in stable["stable"]["sells"]["items"]:
                    can_be_bought = True
            if which_food in mount_feeding_items and which_food in player["inventory"]:
                player["inventory"].remove(which_food)
                logger_sys.log_message(f"INFO: Removing item '{which_food}' from player inventory")
                exp = random.randint(1, 4)
                player["xp"] += exp
                logger_sys.log_message(f"INFO: Adding {exp} experience to player")
                if player["current mount"] in player["mounts"]:
                    level = round(
                        random.uniform(.02, .10), 3
                    ) / mounts[current_mount_type]["feed"]["feed needs"]
                    player["mounts"][player["current mount"]]["level"] += level
                    logger_sys.log_message(f"INFO: Adding {level} levels to mount '{mount_uuid}'")
            elif can_be_bought:
                gold = round(item[which_food]["gold"] * stable["cost value"], 2)
                text = (
                    "You don't own any of that food but the current stable " +
                    f"sell this food at {gold} gold coins."
                )
                print(COLOR_YELLOW, end="")
                text_handling.print_long_string(text)
                print(COLOR_RESET_ALL, end="")
                confirmation = input("Do you want to buy that food to feed this mount? (y/n) ")
                if confirmation.lower().startswith("y"):
                    if gold <= player["gold"]:
                        player["gold"] -= gold
                        logger_sys.log_message(f"INFO: Player has food '{which_food}' for {gold} gold")
                        level = round(
                            random.uniform(.02, .10), 3
                        ) / mounts[current_mount_type]["feed"]["feed needs"]
                        player["mounts"][player["current mount"]]["level"] += level
                        logger_sys.log_message(f"INFO: Adding {level} levels to mount '{mount_uuid}'")
                    else:
                        print(COLOR_YELLOW + "You don't have enough gold to buy this food." + COLOR_RESET_ALL)
            else:
                text = ("You cannot feed your mount with this food or you don't own that" +
                        " food and the current stable doesn't sell this food.")
                print(COLOR_YELLOW, end="")
                text_handling.print_long_string(text)
                print(COLOR_RESET_ALL, end="")
        elif choice == 'Train':
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
                level = round(random.uniform(.01, .09), 3)
                player["mounts"][player["current mount"]]["level"] += level
                logger_sys.log_message(f"INFO: Adding {level} levels to mount '{mount_uuid}'")
                exp = round(random.uniform(.01, .13), 1)
                player["xp"] += exp
                logger_sys.log_message(f"INFO: Adding {exp} experience to player")
                loading -= 1
        else:
            still_training = False
    # get end time
    end_time = time.time()
    logger_sys.log_message(f"INFO: Getting end time of training loop: {end_time}")

    # calculate elapsed time
    elapsed_time = end_time - start_time
    elapsed_time = round(elapsed_time, 2)
    game_elapsed_time = time_handling.return_game_day_from_seconds(elapsed_time, time_elapsing_coefficient)
    game_elapsed_time = round(game_elapsed_time, 2)
    logger_sys.log_message(f"INFO: Getting elapsed game time in training loop: {game_elapsed_time}")
    gold = stable["training gold"] * game_elapsed_time
    logger_sys.log_message(f"INFO: Getting gold amount to be paid: {gold}")
    player["gold"] -= gold
    gold = round(gold, 2)
    hours = round(game_elapsed_time * 24, 2)
    print(f"{COLOR_YELLOW}You paid {gold} gold coins for {hours} hours of training{COLOR_RESET_ALL}")
    logger_sys.log_message(f"INFO: Player paid {gold} gold for {hours} in-game hours of training.")
