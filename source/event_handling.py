# event_handling.py
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
import mission_handling
import time_handling
import dialog_handling
import enemy_handling
import script_handling
import logger_sys
from colors import *
from terminal_handling import cout, cinput
# external imports
import random


# Handling Functions

def event_triggering_checks(event_id, event, player, map, zone):
    logger_sys.log_message(f"INFO: Checking if event '{event_id}' can be triggered")
    trigger = True
    event_data = event[event_id]
    conditions = event_data["source"]

    if not event_data["repeat"] and event_id in player["triggered events"]:
        trigger = False
    else:
        finished = False
        while trigger and not finished:
            # 'map point' checks
            if "map point" in conditions:
                if search(player["x"], player["y"], map) not in conditions["map point"]:
                    trigger = False

            # 'map zone' checks
            if "map zone" in conditions:
                if player["map zone"] not in conditions["map zone"]:
                    trigger = False

            # 'region' checks
            if "region" in conditions:
                if zone[player["map zone"]]["type"] not in conditions["region"]:
                    trigger = False

            # 'date' checks
            if "date" in conditions:
                if (
                    time_handling.addition_to_date(
                        player["starting date"], int(player["elapsed time game days"])
                    ) != conditions["date"]
                ):
                    trigger = False

            # 'player attributes' checks
            if "player attributes" in conditions:
                for attribute in conditions["player attributes"]:
                    if attribute not in player["attributes"]:
                        trigger = False

            # 'has items' checks
            if "has items" in conditions:
                for i in conditions["has items"]:
                    if i not in player["inventory"]:
                        trigger = False

            # 'has missions <offered/active>' checks
            if "has missions offered" in conditions:
                for i in conditions["has missions offered"]:
                    if i not in player["offered missions"]:
                        trigger = False
            if "has missions active" in conditions:
                for i in conditions["has missions active"]:
                    if i not in player["active missions"]:
                        trigger = False

            # 'random' checks
            if "random" in conditions:
                if conditions["random"] < random.uniform(0, 1):
                    trigger = False

            finished = True

    logger_sys.log_message(f"INFO: Checked if event '{event_id}' can be triggered --> {trigger}")
    return trigger


def trigger_event(
    event_id, event, player, mission, dialog, preferences,
    text_replacements_generic, drinks, item, enemy, npcs,
    start_player, lists, zone, mounts, start_time,
    map, save_file, map_location, player_damage_coefficient,
    previous_player, enemies_damage_coefficient
):
    logger_sys.log_message(f"INFO: Triggering event '{event_id}' actions")
    event_data = event[event_id]
    actions = event_data["actions"]

    if "run dialog" in actions:
        dialog_handling.print_dialog(
            actions["run dialog"], dialog, preferences, text_replacements_generic,
            player, drinks, item, enemy, npcs, start_player, lists, zone,
            mission, mounts, start_time, map, save_file
        )
    if "add attributes" in actions:
        for attribute in actions["add attributes"]:
            player["attributes"] += [attribute]
    if "give item" in actions:
        for i in actions["give item"]:
            player["inventory"] += [i]
    if "remove item" in actions:
        for i in actions["remove item"]:
            if i in player["inventory"]:
                player["inventory"] -= [i]
    if "player health" in actions:
        player["health"] += actions["player health"]
    if "player max health" in actions:
        player["max health"] += actions["player max health"]
    if "player gold" in actions:
        player["gold"] += actions["player gold"]
    if "player exp" in actions:
        player["xp"] += actions["player exp"]
    if "enemy spawn" in actions:
        enemy_handling.spawn_enemy(
            map_location, actions["enemy spawn"], enemy, item, lists, start_player, map, player,
            preferences, drinks, npcs, zone, mounts, mission, dialog, player_damage_coefficient,
            text_replacements_generic, start_time, previous_player, save_file,
            enemies_damage_coefficient
        )
    if "use drink" in actions:
        for drink in actions["use drink"]:
            if drinks[drink]["healing level"] == 999:
                player["health"] = player["max health"]
            else:
                player["health"] += drinks[drink]["healing level"]
    if "add to diary" in actions:
        if "known zones" in actions["add to diary"]:
            for i in actions["add to diary"]["known zones"]:
                player["visited zones"] += [i]
        if "known enemies" in actions["add to diary"]:
            for i in actions["add to diary"]["known enemies"]:
                player["enemies list"] += [i]
        if "known npcs" in actions["add to diary"]:
            for i in actions["add to diary"]["known npcs"]:
                player["met npcs names"] += [i]
    if "remove to diary" in actions:
        if "known zones" in actions["remove to diary"]:
            for i in actions["remove to diary"]["known zones"]:
                if i in player["visited zones"]:
                    player["visited zones"] -= [i]
        if "known enemies" in actions["remove to diary"]:
            for i in actions["remove to diary"]["known enemies"]:
                if i in player["enemies list"]:
                    player["enemies list"] -= [i]
        if "known npcs" in actions["remove to diary"]:
            for i in actions["remove to diary"]["known npcs"]:
                if i in player["met npcs names"]:
                    player["met npcs names"] -= [i]

    if "run scripts" in actions:
        plugin = preferences["latest preset"]["type"] == "plugin"
        count = 0
        for script in actions["run scripts"]:
            current_script_data = actions["run scripts"][count]
            script_handling.load_script(
                current_script_data, preferences,  player, map, item, drinks, enemy, npcs,
                start_player, lists, zone, dialog, mission, mounts, start_time,
                text_replacements_generic, plugin
            )
            count += 1

    if "fail mission" in actions:
        for i in actions["fail mission"]:
            if i in player["active missions"]:
                logger_sys.log_message(f"INFO: Executing failing triggers of mission '{i}'")
                mission_handling.execute_triggers(
                    mission[i], player, 'on fail', dialog, preferences,
                    text_replacements_generic, drinks, item, enemy, npcs,
                    start_player, lists, zone, mission, mounts, start_time, map,
                    save_file
                )
                cout(
                    COLOR_RED + COLOR_STYLE_BRIGHT + "You failed mission '" +
                    mission[i]["name"] + "'" + COLOR_RESET_ALL
                )
                player["active missions"].remove(i)


def search(x, y, map):
    logger_sys.log_message(f"INFO: Searching for map point corresponding to coordinates x:{x}, y:{y}")
    global map_location
    map_point_count = int(len(list(map)))
    for i in range(0, map_point_count):
        point_i = map["point" + str(i)]
        point_x, point_y = point_i["x"], point_i["y"]
        if point_x == x and point_y == y:
            map_location = i
            return map_location
