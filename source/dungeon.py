# source imports
import text_handling
import logger_sys
import enemy_handling
import script_handling
import item_handling
from colors import *
from terminal_handling import cout, cinput
# external imports
import time


def dungeon_loop(
    player, current_dungeon, lists, enemy, start_player, item, start_time, preferences,
    npcs, drinks, zone, mounts, dialog, mission, map_location, text_replacements_generic,
    player_damage_coefficient, enemies_damage_coefficient, previous_player, save_file,
    map, map_zone
):
    logger_sys.log_message(f"INFO: Starting dungeon loop of dungeon '{current_dungeon["dungeon"]["name"]}'")
    still_in_dungeon = True
    current_room = 1
    # Get some dungeon rooms stats
    rooms = {}
    for room in list(current_dungeon["dungeon"]["rooms"]):
        room_data = current_dungeon["dungeon"]["rooms"][room]
        rooms[str(room_data["room digit"])] = room
    while still_in_dungeon:
        # Reload player stats
        # Calculate player global armor protection
        # and stores it in a player variable
        global_armor_protection = 0

        # First, get every item in the player equipment
        # and add their protection value to the global
        # armor protection new created variable
        held_item_list = [
            'held boots', 'held chestplate',
            'held leggings', 'held shield'
        ]
        for i in held_item_list:
            item_name = player[i]
            if item_name != " ":
                global_armor_protection += item[item_name]["armor protection"]

        # Then, calculate the player ridden mount -- if he has
        # one -- protection stat and add it to the global armor
        # protection variable
        if player["current mount"] in player["mounts"]:
            global_armor_protection += player["mounts"][player["current mount"]]["stats"]["resistance addition"]

        player["armor protection"] = round(global_armor_protection, 2)

        # Calculate player global agility and stores
        # it in a player variable
        global_agility = 0

        # First, get every item in the player equipment
        # and add their agility value to the global agility
        # new created variable
        held_item_list = [
            'held boots', 'held chestplate', 'held item',
            'held leggings', 'held shield'
        ]
        for i in held_item_list:
            item_name = player[i]
            if item_name != " ":
                global_agility += item[item_name]["agility"]

        # Then, calculate the player ridden mount -- if he has
        # one -- agility stat and add it to the global agility
        # variable
        if player["current mount"] in player["mounts"]:
            global_agility += player["mounts"][player["current mount"]]["stats"]["agility addition"]

        player["agility"] = round(global_agility, 2)  # here we round the actual value
        # All the checks for the player active effects
        # are done here
        #
        # If the player has any active effects, load
        # them one by one and update them depending
        # on their dictionary content and type
        player_damage_coefficient = 1
        if player["held item"] != " ":
            player["critical hit chance"] = item[player["held item"]]["critical hit chance"]
        else:
            player["critical hit chance"] = 0
        if player["active effects"] != {}:
            for i in list(player["active effects"]):
                current_effect = player["active effects"][i]
                effect_over = False
                # Run the actions for every effect type
                if current_effect["type"] == 'healing':
                    # Check if the effect duration's over
                    if (
                        (
                            current_effect["effect duration"] + current_effect["effect starting time"]
                        ) < player["elapsed time game days"]
                    ):
                        # Remove that effect from the player
                        # active effects and set the player
                        # modified stats to before the effect
                        # happened
                        player["active effects"].pop(i)
                        player["health"] = current_effect["before stats"]["health"]
                        player["max health"] = current_effect["before stats"]["max health"]
                        effect_over = True
                    # Check if the effect has already been
                    # applied or not
                    if not current_effect["already applied"] and not effect_over:
                        # Apply that effect changes now
                        if current_effect["effects"]["health changes"] >= 999:
                            player["health"] = player["max health"]
                        else:
                            player["health"] += current_effect["effects"]["health changes"]
                        player["max health"] += current_effect["effects"]["max health changes"]
                        player["active effects"][i]["already applied"] = True
                elif current_effect["type"] == 'protection':
                    # Check if the effect duration's over
                    if (
                        (
                            current_effect["effect duration"] + current_effect["effect starting time"]
                        ) < player["elapsed time game days"] and current_effect["effect duration"] != 999
                    ):
                        # Remove that effect from the player
                        # active effects
                        player["active effects"].pop(i)
                        effect_over = True
                    # Apply the effect effects if the
                    # effect isn't over
                    if not effect_over:
                        player["armor protection"] = player["armor protection"] * current_effect[
                            "effects"
                        ]["protection coefficient"]
                elif current_effect["type"] == 'strength':
                    # Check if the effect duration's over
                    if (
                        (
                            current_effect["effect duration"] + current_effect["effect starting time"]
                        ) < player["elapsed time game days"] and current_effect["effect duration"] != 999
                    ):
                        # Remove that effect from the player
                        # active effects
                        player["active effects"].pop(i)
                        effect_over = True
                    # Apply the effect effects if the
                    # effect isn't over
                    if not effect_over:
                        player["critical hit chance"] = player["critical hit chance"] * current_effect["effects"][
                            "critical hit chance coefficient"
                        ]
                        # If the player already has an effect that changes
                        # the damage coefficient and that's greater, don't
                        # apply the current effect coefficient
                        # = keep the greater one
                        if not player_damage_coefficient > current_effect["effects"]["damage coefficient"]:
                            player_damage_coefficient = current_effect["effects"]["damage coefficient"]
                elif current_effect["type"] == 'agility':
                    # Check if the effect duration's over
                    if (
                        (
                            current_effect["effect duration"] + current_effect["effect starting time"]
                        ) < player["elapsed time game days"] and current_effect["effect duration"] != 999
                    ):
                        # Remove that effect from the player
                        # active effects
                        player["active effects"].pop(i)
                        effect_over = True
                    # Apply the effect effects if the
                    # effect isn't over
                    if not effect_over:
                        player["agility"] = player["agility"] * current_effect[
                            "effects"
                        ]["agility coefficient"]

        # Get some stats
        # Calculate player progress of the dungeon
        progression = int((current_room - 1) * 100 / current_dungeon["dungeon"]["rooms number"])

        bars = 10
        remaining_symbol = "█"
        lost_symbol = "_"
        remaining_bars = round(current_room / current_dungeon["dungeon"]["rooms number"] * bars - 1)
        lost_bars = bars - remaining_bars

        text_handling.clear_prompt()
        text_handling.print_separator('=')
        cout(f"Defy the dungeon '{current_dungeon["dungeon"]["name"]}'!")
        text_handling.print_separator('=')
        cout(
            f"PROGRESS: {progression}% |{COLOR_CYAN}{COLOR_STYLE_BRIGHT}{remaining_bars * remaining_symbol}" +
            f"{lost_bars * lost_symbol}{COLOR_RESET_ALL}|"

        )
        text_handling.print_separator('=')
        color_room = COLOR_BLUE
        if current_room == current_dungeon["dungeon"]["rooms number"]:
            color_room = COLOR_GREEN
        cout(
            f"CURRENT ROOM: {color_room}{current_room}{COLOR_RESET_ALL}/" +
            f"{COLOR_GREEN}{current_dungeon["dungeon"]["rooms number"]}{COLOR_RESET_ALL}"
        )

        # Check if the player has completed the dungeon
        if current_room > current_dungeon["dungeon"]["rooms number"]:
            return True

        current_room_data = current_dungeon["dungeon"]["rooms"][str(rooms[str(current_room)])]
        type_room = current_room_data["room type"]
        if type_room == "boss-fight":
            type_room = COLOR_ORANGE_5 + "Boss Fight"
        elif type_room == "fight":
            type_room = COLOR_YELLOW + "Fight"
        elif type_room == "enigma":
            type_room = COLOR_MAGENTA + "Enigma"
        cout(
            "TYPE: " +
            str(type_room + COLOR_RESET_ALL)
        )
        text_handling.print_separator('=')
        cout("  - [S]tart Room")
        if "dungeon map" in current_dungeon["dungeon"]:
            cout("  - [C]heck Dungeon Map")
        cout("  - [U]se Item")
        cout("  - [P]ause Game")
        if not current_dungeon["dungeon"]["no escape"]:
            cout("  - [E]xit Dungeon")
        text_handling.print_separator('=')
        cout()
        action = cinput(COLOR_GREEN + COLOR_STYLE_BRIGHT + "> " + COLOR_RESET_ALL).lower()
        cout()
        logger_sys.log_message(f"Player has chosen action '{action}'")
        if action.startswith('s'):
            logger_sys.log_message(
                f"Loading dungeon '{current_dungeon["dungeon"]["name"]}' room {current_room}" +
                f" --> is a '{type_room}{COLOR_RESET_ALL}' room type"
            )
            if type_room == COLOR_ORANGE_5 + "Boss Fight" or type_room == COLOR_YELLOW + "Fight":
                enemy_handling.spawn_enemy(
                    map_location, current_room_data["room fight data"]["enemy list spawn"],
                    enemy, item, lists, start_player, map, player, preferences, drinks, npcs,
                    zone, mounts, mission, dialog, player_damage_coefficient,
                    text_replacements_generic, start_time, previous_player, save_file,
                    enemies_damage_coefficient,
                    no_run_away=current_room_data["room fight data"]["no run away"]
                )
                if "item reward" in current_room_data["room fight data"]:
                    logger_sys.log_message(
                        "INFO: Adding to player inventory items " +
                        f"'{current_room_data["room fight data"]["item reward"]}'"
                    )
                    for i in current_room_data["room fight data"]["item reward"]:
                        player["inventory"] += [i]
                        player["inventory slots remaining"] -= 1
                    cout(COLOR_CYAN + "You received items!" + COLOR_RESET_ALL)
                    time.sleep(2)
                if "gold reward" in current_room_data["room fight data"]:
                    gold = current_room_data["room fight data"]["gold reward"]
                    logger_sys.log_message(f"INFO: Adding to player {gold} gold")
                    player["gold"] += gold
                    cout(COLOR_CYAN + f"You received {gold} gold!" + COLOR_RESET_ALL)
                    time.sleep(2)
            else:
                cout(" ")
                plugin = False
                if preferences["latest preset"]["type"] == 'plugin':
                    plugin = True
                script_handling.load_script(
                    current_room_data["room enigma data"], preferences, player, map, item,
                    drinks, enemy, npcs, start_player, lists, zone, dialog, mission, mounts,
                    start_time, text_replacements_generic, plugin
                )
                cinput()
            current_room += 1
        elif action.startswith('c') and "dungeon map" in current_dungeon["dungeon"]:
            if preferences["latest preset"]["type"] == "plugin":
                plugin = preferences["latest preset"]["plugin"]
            else:
                plugin = False
            cout("╔" + ("═" * 53) + "╗")
            map_data = {
                "map": current_dungeon["dungeon"]["dungeon map"]
            }
            text_handling.print_map_art(map_data, plugin_name=plugin)
            cout("╚" + ("═" * 53) + "╝")
            cinput()
        elif action.startswith('u'):
            text_handling.print_separator('=')
            player_inventory_displayed = []
            count = 0
            for i in player["inventory"]:
                zeroes = len(str(len(player["inventory"])))
                removed = len(str(count))
                player_inventory_displayed += [f"{"0" * (zeroes - removed)}{count}> {i}"]
                count += 1
            cout("INVENTORY:")
            for line in player_inventory_displayed:
                cout(line)
            text = '='
            text_handling.print_separator(text)
            item_input = cinput(COLOR_GREEN + COLOR_STYLE_BRIGHT + "$ " + COLOR_RESET_ALL)
            error = False
            try:
                which_item_index = int(item_input)
                which_item = player["inventory"][which_item_index]
            except Exception as e:
                error = True
            if not error:  # use item
                item_handling.use_item(
                    which_item, item, player, preferences, drinks,
                    enemy, npcs, start_player, lists, zone, dialog, mission,
                    mounts, text_replacements_generic, item, map_location,
                    player_damage_coefficient, previous_player, save_file,
                    start_time, enemies_damage_coefficient, map
                )
                text = '='
                text_handling.print_separator(text)
        elif action.startswith('p'):
            logger_sys.log_message("INFO: Pausing game")
            cout("Press enter to unpause game...")
            pause_start = time.time()
            cinput()
            pause_end = time.time()
            start_time -= pause_end - pause_start
            logger_sys.log_message(f"INFO: Finished pausing game --> game pause have lasted {pause_end - pause_start} seconds")
        elif action.startswith('e') and not current_dungeon["dungeon"]["no escape"]:
            cout("Are you sure you want to qui the dungeon?")
            ask = cinput("All your progress here will be reset (y/n) ").lower()
            if ask.startswith('y'):
                logger_sys.log_message("INFO: Exiting dungeon and resetting progress")
                still_in_dungeon = False
                return False
        else:
            cout(COLOR_YELLOW + f"Action '{action}' isn't valid!" + COLOR_RESET_ALL)
            time.sleep(2)
