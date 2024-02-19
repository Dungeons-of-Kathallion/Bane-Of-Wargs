import logger_sys
import uuid_handling
import colors
from colorama import Fore, Back, Style, init, deinit
from colors import *

# initialize colorama
init()

# Handling Functions

def get_healing_effect_changes(effect_data):
    health_changes = 0
    max_health_changes = 0

    if "augmentation" in list(effect_data["health change"]):
        augmentation = effect_data["health change"]["augmentation"]
        health_changes += augmentation
    if "diminution" in list(effect_data["health change"]):
        diminution = effect_data["health change"]["diminution"]
        health_changes -= diminution
    if "max health" in list(effect_data["health change"]):
        if "augmentation" in list(effect_data["health change"]["max health"]):
            augmentation = effect_data["health change"]["max health"]["augmentation"]
            max_health_changes += augmentation
        if "diminution" in list(effect_data["health change"]["max health"]):
            diminution = effect_data["health change"]["max health"]["diminution"]
            max_health_changes -= diminution

    return health_changes, max_health_changes

def healing_effect(effect_data, player):
    # Generate a UUID for that new
    # effect
    effect_uuid = str(uuid_handling.generate_random_uuid())

    # If this effect has a timer, create
    # the effect dictionary that will be
    # added to the player save data and then
    # handled by the main.py function
    #
    # If not, just apply the effects of that
    # effect one by one
    if "effect time" in effect_data:
        effects = {}

        # Create the applied effects dictionary
        if effect_data["type"] == 'healing':
            health_changes, max_health_changes = get_healing_effect_changes(effect_data)

            effects = {
                "health changes": health_changes,
                "max health changes": max_health_changes
            }

        effect_dictionary = {
            "effect duration": effect_data["effect time"],
            "effect starting time": player["elapsed time game days"],
            "type": effect_data["type"],
            "already applied": False,
            "before stats": {
                "health": player["health"],
                "max health": player["max health"]
            },
            "effects": effects
        }

        # Add the effect dictionary to the player
        # active effects dictionary
        player["active effects"][effect_uuid] = effect_dictionary
    else:
        if effect_data["health change"] != None:
            health_changes, max_health_changes = get_healing_effect_changes(effect_data)

            if health_changes >= 999:
                player["health"] = player["max health"]
            else:
                player["health"] += health_changes
                player["max health"] += max_health_changes


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

                logger_sys.log_message(f"INFO: Running consumable effect with '{current_effect_type}' parameter;\n{current_effect_data}")

                if current_effect_type == "healing":
                    healing_effect(current_effect_data, player)

                count += 1

        else:
            logger_sys.log_message(f"INFO: Found no effects for consumable '{consumable_name}'")


def print_consumable_effects(current_effect_type, current_effect_data):
    # Print the type of that effect, and then,
    # depending on its type, print out in the game
    # UI formatted info about that effect
    logger_sys.log_message(f"INFO: Printing consumable effect data '{current_effect_data}' formatted info")
    print(f"   Type: {COLOR_CYAN}{current_effect_type}{COLOR_RESET_ALL}")
    if current_effect_type == 'healing':
        if "effect time" in current_effect_data:
            duration_time = current_effect_data["effect time"]
            print(f"   Duration Time: {COLOR_BACK_BLUE}{duration_time}{COLOR_RESET_ALL}")
        if current_effect_data["health change"] != None:
            print(f"   Health Changes: ")

            health_changes, max_health_changes = get_healing_effect_changes(current_effect_data)

            if health_changes >= 999:
                print(f"     health -> {COLOR_MAGENTA}MAX HEALTH{COLOR_RESET_ALL}")
            elif health_changes > 0:
                print(f"     health + {COLOR_GREEN}{health_changes}{COLOR_RESET_ALL}")
            elif health_changes == 0:
                print(f"     health + {COLOR_BLUE}{health_changes}{COLOR_RESET_ALL}")
            else:
                print(f"     health + {COLOR_RED}{health_changes}{COLOR_RESET_ALL}")

            if max_health_changes > 0:
                print(f"     max health + {COLOR_GREEN}{max_health_changes}{COLOR_RESET_ALL}")
            elif max_health_changes == 0:
                print(f"     max health + {COLOR_BLUE}{max_health_changes}{COLOR_RESET_ALL}")
            else:
                print(f"     max health + {COLOR_RED}{max_health_changes}{COLOR_RESET_ALL}",)


# deinitialize colorama
deinit()
