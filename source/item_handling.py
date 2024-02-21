import logger_sys
import script_handling
import text_handling
import consumable_handling


# Handling Function


def use_item(
    which_item, item_data, player, preferences, drinks,
    enemy, npcs, start_player, lists, zone, dialog, mission, mounts
):
    # Load the global items data and load the
    # chosen item data and stores it to a variable
    logger_sys.log_message(f"INFO: Using item '{which_item}'")
    which_item_data = item_data[which_item]
    which_item_type = which_item_data["type"]
    if which_item_type == "Consumable" or which_item_type == "Food":
        consumable_handling.consume_consumable(item_data, which_item, player)
        logger_sys.log_message(f"INFO: Item '{which_item}' is an item of type '{which_item_type}' --> consuming it")
    elif (
        which_item_type == "Weapon" or which_item_type.lower().startswith("Armor Piece: ")
    ):
        equip_item(which_item, player, which_item_type)
        logger_sys.log_message(f"INFO: Item '{which_item}' is an item of type '{which_item_type}' --> equipping it")
    elif which_item_type == "Utility":
        logger_sys.log_message(f"INFO: Item '{which_item}' is an item of type '{which_item_type}' --> loading its script")
        print(" ")
        if preferences["latest preset"]["type"] == 'plugin':
            script_handling.load_script(
                which_item, preferences, player, map, item_data, drinks, enemy, npcs,
                start_player, lists, zone, dialog, mission, mounts, plugin=True
            )
        else:
            script_handling.load_script(
                which_item, preferences, player, map, item_data, drinks, enemy, npcs,
                start_player, lists, zone, dialog, mission, mounts
            )


def equip_item(item_name, player, equipment_type):
    # equip the item in one of the player slot, depending
    # on the equipment type
    slot = None

    if equipment_type == "Weapon":
        slot = "held item"
    elif equipment_type == "Armor Piece: Chestplate":
        slot = "held chestplate"
    elif equipment_type == "Armor Piece: Leggings":
        slot = "held leggings"
    elif equipment_type == "Armor Piece: Boots":
        slot = "held boots"
    elif equipment_type == "Armor Piece: Shield":
        slot = "held shield"

    if equipment_type == "Weapon" or equipment_type == "Armor Piece: Shield":
        print("You are now holding ", text_handling.a_an_check(item_name))
    else:
        print("You are now wearing ", text_handling.a_an_check(item_name))

    logger_sys.log_message(f"INFO: Equipping item '{item_name}' of type '{equipment_type}' to player slot '{slot}'")
    player[slot] = item_name