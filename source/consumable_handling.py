import logger_sys

# Handling Functions

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
    if item_data["type"] == "Food":
        if item_data["healing level"] == 999:
            player["health"] = player["max health"]
        else:
            player["health"] += item_data["healing level"]
        player["max health"] += item_data["max bonus"]

    # Then, load the consumable effects 1 by 1
    # and apply the effects 1 by 1
    logger_sys.log_message(f"INFO: Getting consumable '{consumable_name}' effects")

    if consumable_data["effects"] != None:
        effects = consumable_data["effects"]
        logger_sys.log_message(f"INFO: Loaded consumable '{consumable_name}' effects:\n{effects}")
        print(consumable_data["effects"])

    else:
        logger_sys.log_message(f"INFO: Found no effects for consumable '{consumable_name}'")
