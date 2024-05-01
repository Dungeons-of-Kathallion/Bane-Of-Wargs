# item_handling.py
# Copyright (c) 2024 by @Cromha
#
# Bane Of Wargs is free software: you can redistribute it and/or modify it under the
# terms of the GNU General Public License as published by the Free Software
# Foundation, either version 3 of the License, or (at your option) any later version.
#
# Bane Of Wargs is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
# PARTICULAR PURPOSE. See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with
# this program. If not, see <https://www.gnu.org/licenses/>.

# source imports
import logger_sys
import script_handling
import text_handling
import consumable_handling
from terminal_handling import cout, cinput


# Handling Function


def use_item(
    which_item, item_data, player, preferences, drinks,
    enemy, npcs, start_player, lists, zone, dialog, mission,
    mounts, text_replacements_generic, item, map_location,
    player_damage_coefficient, previous_player, save_file, start_time,
    enemies_damage_coefficient, map
):
    # Load the global items data and load the
    # chosen item data and stores it to a variable
    logger_sys.log_message(f"INFO: Using item '{which_item}'")
    which_item_data = item_data[which_item]
    which_item_type = which_item_data["type"]
    if which_item_type == "Consumable" or which_item_type == "Food":
        consumable_handling.consume_consumable(
            item, which_item, player,
            dialog, preferences, text_replacements_generic,
            lists, map_location, enemy, item, drinks,
            start_player, npcs, zone,
            mounts, mission, player_damage_coefficient, previous_player,
            save_file, map, start_time, enemies_damage_coefficient
        )
        logger_sys.log_message(f"INFO: Item '{which_item}' is an item of type '{which_item_type}' --> consuming it")
    elif (
        which_item_type == "Weapon" or which_item_type.lower().startswith("Armor Piece: ")
    ):
        equip_item(which_item, player, which_item_type)
        logger_sys.log_message(f"INFO: Item '{which_item}' is an item of type '{which_item_type}' --> equipping it")
    elif which_item_type == "Utility":
        logger_sys.log_message(f"INFO: Item '{which_item}' is an item of type '{which_item_type}' --> loading its script")
        cout(" ")
        plugin = False
        if preferences["latest preset"]["type"] == 'plugin':
            plugin = True
        script_handling.load_script(
            item[which_item], preferences, player, map, item_data, drinks, enemy, npcs,
            start_player, lists, zone, dialog, mission, mounts, start_time,
            text_replacements_generic, save_file, player_damage_coefficient,
            enemies_damage_coefficient, previous_player, plugin
        )
        cinput()


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
        cout("You are now holding " + text_handling.a_an_check(item_name))
    else:
        cout("You are now wearing " + text_handling.a_an_check(item_name))

    logger_sys.log_message(f"INFO: Equipping item '{item_name}' of type '{equipment_type}' to player slot '{slot}'")
    player[slot] = item_name
