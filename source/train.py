# source imports
import terminal_handling
import text_handling
import time_handling
import logger_sys
from colors import *
from terminal_handling import cout, cinput
# external imports
import random
import time


def training_loop(mount_uuid, player, item, mounts, stable, time_elapsing_coefficient):
    logger_sys.log_message(f"INFO: Starting training loop of mount '{mount_uuid}'")
    still_training = True
    current_mount_type = str(player["mounts"][str(mount_uuid)]["mount"])
    current_mount_feeds = mounts[current_mount_type]["feed"]["food"]
    current_mount_data = mounts[current_mount_type]
    elapsed_time = 0
    mount_name = player["mounts"][mount_uuid]["name"]
    while still_training:
        start_time = time.time()
        # get current time
        current_time = time_handling.get_day_time(
            player["elapsed time game days"] +
            time_handling.return_game_day_from_seconds(elapsed_time, time_elapsing_coefficient)
        )
        elapsed_hours = int(time_handling.return_game_day_from_seconds(
            elapsed_time, time_elapsing_coefficient
        ) * 24)
        owed_gold = round(
            stable["training gold"] * time_handling.return_game_day_from_seconds(elapsed_time, time_elapsing_coefficient), 2
        )
        text_handling.clear_prompt()
        text_handling.print_separator('=')
        cout(f"DAY TIME: {current_time}")
        cout(f"CURRENT MOUNT: {mount_name}")
        text_handling.print_separator('=')
        cout(f"ELAPSED TIME: {elapsed_hours}hr(s)")
        cout(f"OWED GOLD: {COLOR_YELLOW}{owed_gold}{COLOR_RESET_ALL}")
        text_handling.print_separator('=')

        bars = 25
        remaining_symbol = "█"
        lost_symbol = "_"
        remaining_bars = round(player["mounts"][mount_uuid]["level"] / current_mount_data["levels"]["max level"] * bars)
        lost_bars = bars - remaining_bars

        cout(
            f"LEVEL of {mount_name}: {round(player["mounts"][mount_uuid]["level"], 1)}" +
            f"/{current_mount_data["levels"]["max level"]}"
        )
        cout(
                f"|{COLOR_GREEN}{COLOR_STYLE_BRIGHT}{remaining_bars * remaining_symbol}" +
                f"{lost_bars * lost_symbol}{COLOR_RESET_ALL}|"

        )
        text_handling.print_separator('=')
        cout("  - [F]eed")
        cout("  - [T]rain")
        cout("  - [E]xit")
        text_handling.print_separator('=')
        cout("")
        choice = cinput(COLOR_GREEN + COLOR_STYLE_BRIGHT + "> " + COLOR_RESET_ALL).lower()
        cout("")
        logger_sys.log_message(f"INFO: Player has chosen choice '{choice}'")
        if choice.startswith('f'):
            # For starters, get the mount feeding items,
            # and than do some checks and finally, up the
            # mount level by a random amount, divided by the
            # mount feeding needs. Also add some experience
            # points to the player.
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
            cout("MOUNT FEEDING ITEMS:")
            cout(mount_feeding_items_text)
            text_handling.print_separator(text)
            which_food = str(cinput(COLOR_GREEN + COLOR_STYLE_BRIGHT + "> " + COLOR_RESET_ALL))
            cout("")
            can_be_bought = False
            if "items" in stable["stable"]["sells"]:
                if which_food in stable["stable"]["sells"]["items"]:
                    can_be_bought = True
            if which_food in mount_feeding_items and which_food in player["inventory"]:
                player["inventory"].remove(which_food)
                logger_sys.log_message(f"INFO: Removing item '{which_food}' from player inventory")
                exp = random.randint(1, 4)
                player["xp"] += exp
                cout(f"You gained {exp} experience points")
                logger_sys.log_message(f"INFO: Adding {exp} experience to player")
                level = round(
                    random.uniform(.02, .10), 3
                ) / mounts[current_mount_type]["feed"]["feed needs"]
                player["mounts"][player["current mount"]]["level"] += level
                cout(f"Your mount gained {round(level, 1)} level points")
                logger_sys.log_message(f"INFO: Adding {level} levels to mount '{mount_uuid}'")
            elif can_be_bought:
                gold = round(item[which_food]["gold"] * stable["cost value"], 2)
                text = (
                    "You don't own any of that food but the current stable " +
                    f"sell this food at {gold} gold coins."
                )
                cout(COLOR_YELLOW, end="")
                text_handling.print_long_string(text)
                cout(COLOR_RESET_ALL, end="")
                confirmation = cinput("Do you want to buy that food to feed this mount? (y/n) ")
                cout("")
                if confirmation.lower().startswith("y"):
                    if gold <= player["gold"]:
                        player["gold"] -= gold
                        logger_sys.log_message(f"INFO: Player has bought food '{which_food}' for {gold} gold")
                        level = round(
                            random.uniform(.02, .10), 3
                        ) / mounts[current_mount_type]["feed"]["feed needs"]
                        player["mounts"][player["current mount"]]["level"] += level
                        logger_sys.log_message(f"INFO: Adding {level} levels to mount '{mount_uuid}'")
                        exp = random.randint(1, 4)
                        player["xp"] += exp
                        logger_sys.log_message(f"INFO: Adding {exp} experience to player")
                        cout(f"You gained {exp} experience points")
                        cout(f"Your mount gained {round(level, 1)} level points")
                    else:
                        cout(COLOR_YELLOW + "You don't have enough gold to buy this food." + COLOR_RESET_ALL)
            else:
                text = ("You cannot feed your mount with this food or you don't own that" +
                        " food and the current stable doesn't sell this food.")
                cout(COLOR_YELLOW, end="")
                text_handling.print_long_string(text)
                cout(COLOR_RESET_ALL, end="")
        elif choice.startswith('t'):
            # Begin the training loop, that lasts 30
            # seconds. Every 2 seconds, the mount gets
            # its level upped by a small random amount
            # as the player experience too
            loading = 15
            exp_total = 0
            level_total = 0
            while loading > 0:
                cout("Training...", end='\r')
                time.sleep(.25)
                cout("Training*..", end='\r')
                time.sleep(.25)
                cout("Training.*.", end='\r')
                time.sleep(.25)
                cout("Training..*", end='\r')
                time.sleep(.25)
                cout("Training..*", end='\r')
                time.sleep(.25)
                cout("Training.*.", end='\r')
                time.sleep(.25)
                cout("Training*..", end='\r')
                time.sleep(.25)
                cout("Training...", end='\r')
                time.sleep(.25)
                level = round(random.uniform(.01, .09), 3)
                player["mounts"][player["current mount"]]["level"] += level
                logger_sys.log_message(f"INFO: Adding {level} levels to mount '{mount_uuid}'")
                exp = round(random.uniform(.01, .13), 1)
                player["xp"] += exp
                logger_sys.log_message(f"INFO: Adding {exp} experience to player")
                loading -= 1
                exp_total += exp
                level_total += level
            cout(f"You gained {round(exp_total, 2)} experience points")
            cout(f"Your mount gained {round(level_total, 1)} level points")
        elif choice.startswith('e'):
            still_training = False
        else:
            cout(f"\nCommand '{choice}' isn't valid")
        time.sleep(2)
        elapsed_time += time.time() - start_time

    # Calculate elapsed time and make
    # the player pay for the training
    elapsed_time = round(elapsed_time, 2)
    game_elapsed_time = time_handling.return_game_day_from_seconds(elapsed_time, time_elapsing_coefficient)
    game_elapsed_time = round(game_elapsed_time, 2)
    logger_sys.log_message(f"INFO: Getting elapsed game time in training loop: {game_elapsed_time}")
    gold = stable["training gold"] * game_elapsed_time
    logger_sys.log_message(f"INFO: Getting gold amount to be paid: {gold}")
    player["gold"] -= gold
    gold = round(gold, 2)
    hours = round(game_elapsed_time * 24, 2)
    cout(f"{COLOR_YELLOW}You paid {gold} gold coins for {hours} hours of training{COLOR_RESET_ALL}")
    time.sleep(2)
    logger_sys.log_message(f"INFO: Player paid {gold} gold for {hours} in-game hours of training.")
