"""
item_handling.py
----------------
Copyright (c) 2024 by @Cromha

Bane Of Wargs is free software: you can redistribute it and/or modify it under the terms
of the GNU General Public License as published by the Free Software Foundation, either
version 3 of the License, or (at your option) any later version.

Bane Of Wargs is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with this program.
If not, see <https://www.gnu.org/licenses/>.
"""

import logger_sys
import script_handling
import text_handling
import consumable_handling
from terminal_handling import cout, cinput


def use_item(
    which_item: str,
    item_data: dict,
    player: dict,
    preferences: dict,
    drinks: dict,
    enemy: dict,
    npcs: dict,
    start_player: dict,
    lists: dict,
    zone: dict,
    dialog: dict,
    mission: dict,
    mounts: dict,
    text_replacements_generic: dict,
    item: dict,
    map_location: dict,
    player_damage_coefficient: float,
    previous_player: dict,
    save_file: str,
    start_time: float,
    enemies_damage_coefficient: float,
    map_object: dict,
) -> None:
    """
    Handle usage of a given item by the player. Depending on the item type, it will:
      - be consumed (if it's a "Consumable" or "Food"),
      - be equipped (if it's a "Weapon" or "Armor Piece: <something>"),
      - or load a corresponding script (if it's "Utility").

    :param which_item: The name/key of the item to be used.
    :param item_data: Global dictionary mapping item names to their definition data.
    :param player: Dictionary containing player's data (stats, equipment, etc.).
    :param preferences: Global user preferences dictionary.
    :param drinks: Possibly a dictionary of drink definitions (for synergy with items).
    :param enemy: The main or current enemy data dictionary.
    :param npcs: Dictionary storing NPC data in the world.
    :param start_player: Snapshot of the player at the start (for rewinding or references).
    :param lists: A general dictionary storing game lists, arrays, references, etc.
    :param zone: Dictionary referencing the current zone or region data in the game.
    :param dialog: Dialogue data or references to text lines for conversation.
    :param mission: Dictionary containing mission/quest states.
    :param mounts: Dictionary with data about player mounts or ridable creatures.
    :param text_replacements_generic: Replacements for textual placeholders in strings.
    :param item: Full dictionary of all item references in the game.
    :param map_location: Contains data about the player's location in the map world.
    :param player_damage_coefficient: A multiplier or coefficient for player damage.
    :param previous_player: Possibly the player's data from a previous state or checkpoint.
    :param save_file: The path to the current save file or save reference.
    :param start_time: A float indicating when the game session started.
    :param enemies_damage_coefficient: A multiplier or coefficient for enemy damage.
    :param map_object: Dictionary or reference to the game map object data.
    """
    logger_sys.log_message(f"INFO: Attempting to use item '{which_item}'.")

    # Retrieve item metadata.
    which_item_data = item_data.get(which_item)
    if not which_item_data:
        logger_sys.log_message(f"ERROR: Item '{which_item}' not found in item_data.")
        cout(f"The item '{which_item}' does not exist.")
        return

    which_item_type = which_item_data.get("type", "Unknown")

    # Distinguish between recognized item types
    if which_item_type in ("Consumable", "Food"):
        logger_sys.log_message(f"INFO: Item '{which_item}' of type '{which_item_type}'. Consuming now.")
        consumable_handling.consume_consumable(
            all_items=item,
            consumed_item=which_item,
            player=player,
            dialog=dialog,
            preferences=preferences,
            text_replacements=text_replacements_generic,
            lists=lists,
            map_location=map_location,
            enemy=enemy,
            item_data=item,
            drinks=drinks,
            start_player=start_player,
            npcs=npcs,
            zone=zone,
            mounts=mounts,
            mission=mission,
            player_damage_coefficient=player_damage_coefficient,
            previous_player=previous_player,
            save_file=save_file,
            map_object=map_object,
            start_time=start_time,
            enemies_damage_coefficient=enemies_damage_coefficient,
        )
    elif which_item_type == "Weapon" or which_item_type.lower().startswith("armor piece: "):
        logger_sys.log_message(f"INFO: Item '{which_item}' is equipable. Equipping.")
        equip_item(item_name=which_item, player=player, equipment_type=which_item_type)
    elif which_item_type == "Utility":
        logger_sys.log_message(f"INFO: Item '{which_item}' is 'Utility'. Loading script.")
        cout(" ")

        plugin_mode = False
        if preferences.get("latest preset", {}).get("type") == "plugin":
            plugin_mode = True

        script_handling.load_script(
            item[which_item],
            preferences=preferences,
            player=player,
            map_object=map_object,
            item_data=item_data,
            drinks=drinks,
            enemy=enemy,
            npcs=npcs,
            start_player=start_player,
            lists=lists,
            zone=zone,
            dialog=dialog,
            mission=mission,
            mounts=mounts,
            start_time=start_time,
            text_replacements=text_replacements_generic,
            save_file=save_file,
            player_damage_coefficient=player_damage_coefficient,
            enemies_damage_coefficient=enemies_damage_coefficient,
            previous_player=previous_player,
            plugin=plugin_mode,
        )
        cinput()
    else:
        logger_sys.log_message(f"WARNING: Item '{which_item}' has unrecognized type '{which_item_type}'. Doing nothing.")
        cout(f"You can't use this item right now ({which_item_type}).")


def equip_item(item_name: str, player: dict, equipment_type: str) -> None:
    """
    Equips the specified item to the corresponding slot on the player, 
    depending on whether it's a weapon or a piece of armor. Updates the player's dictionary accordingly.

    :param item_name: The name (or ID) of the item to be equipped.
    :param player: The dictionary storing player data, including the relevant equipment slots.
    :param equipment_type: The string describing the item type, e.g., 'Weapon', 'Armor Piece: Shield', etc.
    """
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

    # fallback if unrecognized armor piece
    if slot is None:
        logger_sys.log_message(
            f"WARNING: The item '{item_name}' is recognized as armor but the sub-type is unknown. Using 'held item' as fallback slot."
        )
        slot = "held item"

    # Display feedback to the user
    if equipment_type == "Weapon" or equipment_type == "Armor Piece: Shield":
        cout("You are now holding " + text_handling.a_an_check(item_name))
    else:
        cout("You are now wearing " + text_handling.a_an_check(item_name))

    # Log
    logger_sys.log_message(f"INFO: Equipping '{item_name}' of type '{equipment_type}' to slot '{slot}' on player.")
    # Actually equip
    player[slot] = item_name

