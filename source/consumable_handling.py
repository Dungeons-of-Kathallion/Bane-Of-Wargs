import logger_sys
import colors
from colorama import Fore, Back, Style, init, deinit
from colors import *

# initialize colorama
init()

# Handling Functions

def healing_effect(effect_data, player_data):
    pass


def consume_consumable(item_data, consumable_name, player):
    # First, load the consumable data and stores
    # it in a variable, then remove the item
    # from the player's inventory
    logger_sys.log_message(f"INFO: Loading consumable '{consumable_name}' data")
    consumable_data = item_data[consumable_name]
    logger_sys.log_message(f"INFO: Loaded consumable '{consumable_name}' data:\n{consumable_data}")
    player["inventory"].remove(consumable_name)
    logger_sys.log_message(f"INFO: Removing item '{consumable_name}' form the player inventory")

    # If the consumable is a food, load the
    # health regeneration and apply them
    if consumable_data["type"] == "Food":
        if consumable_data["healing level"] == 999:
            player["health"] = player["max health"]
        else:
            player["health"] += consumable_data["healing level"]
        player["max health"] += consumable_data["max bonus"]
    else:

        # Then, load the consumable effects 1 by 1
        # and apply the effects 1 by 1
        logger_sys.log_message(f"INFO: Getting consumable '{consumable_name}' effects")

        if consumable_data["effects"] != None:
            effects = consumable_data["effects"]
            logger_sys.log_message(f"INFO: Loaded consumable '{consumable_name}' effects:\n{effects}")
            count = 0
            for effect in consumable_data["effects"]:
                current_effect_data = consumable_data["effects"][count]
                current_effect_type = current_effect_data["type"]

                if current_effect_type == "healing":
                    healing_effect(current_effect_data, player)

                count += 1

        else:
            logger_sys.log_message(f"INFO: Found no effects for consumable '{consumable_name}'")


def print_consumable_effects(current_effect_type, current_effect_data):
    print(f"   Type: {COLOR_CYAN}{current_effect_type}{COLOR_RESET_ALL}")
    if current_effect_type == 'healing':
        print(f"   Health Changes: ")
        augmentation = 0
        health_changes = 0
        max_health_changes = 0
        if "augmentation" in list(current_effect_data["health change"]):
            augmentation = current_effect_data["health change"]["augmentation"]
            if augmentation >= 999:
                augmentation = "MAX HEALTH"
        if "diminution" in list(current_effect_data["health change"]):
            health_changes -= current_effect_data["health change"]["diminution"]

        if augmentation == "MAX HEALTH":
            print(f"     health -> {COLOR_MAGENTA}MAX HEALTH{COLOR_RESET_ALL}")
        elif health_changes >= 0:
            print(f"     health + {COLOR_GREEN}{health_changes}{COLOR_RESET_ALL}")
        else:
            print(f"     health + {COLOR_RED}{health_changes}{COLOR_RESET_ALL}")

        if "max health" in list(current_effect_data["health change"]):
            if "augmentation" in list(current_effect_data["health change"]["max health"]):
                max_health_changes += current_effect_data["health change"]["max health"]["augmentation"]
            if "diminution" in list(current_effect_data["health change"]["max health"]):
                max_health_changes -= current_effect_data["health change"]["max health"]["diminution"]

        if max_health_changes >= 0:
            print(f"     max health + {COLOR_GREEN}{max_health_changes}{COLOR_RESET_ALL}")
        else:
            print(f"     max health + {COLOR_RED}{max_health_changes}{COLOR_RESET_ALL}",)


# deinitialize colorama
deinit()
