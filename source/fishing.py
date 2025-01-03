# fishing.py
# Copyright (c) 2025 by @Cromha
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
import text_handling
import time_handling
import terminal_handling
import logger_sys
from colors import *
from terminal_handling import cout, cinput
# external imports
import time
import random


def fishing_loop(fishing_location, player, save_file, map_zone, zone, time_elapsing_coefficient, item):
    logger_sys.log_message(f"INFO: Starting fishing loop")
    still_fishing = True

    # Set some variables
    global fishing_equipment, equipped_rod, equipped_lure
    fishing_equipment = "None"
    equipped_rod = ""
    equipped_lure = ""

    if fishing_location not in player["caught fishes"]["$stats$"]["seas and lakes went fishing"]:
        player["caught fishes"]["$stats$"]["seas and lakes went fishing"] += [fishing_location]
    logger_sys.log_message(f"INFO: Added map zone '{fishing_location}' to player's fishing locations")

    while still_fishing:
        # Temporary store the player's elapsed time game
        # days data in another variable, to update it in
        # the camping loop but not interfere with the main loop
        elapsed_time = player["elapsed time game days"]

        # get start time
        start_time = time.time()
        logger_sys.log_message(f"INFO: [CAMPING LOOP] Getting start time: '{start_time}'")

        text_handling.clear_prompt()
        text_handling.print_separator('=')
        day_time = time_handling.get_day_time(elapsed_time)
        cout(f"DAY TIME: {day_time}")
        date = time_handling.date_prettifier(
            time_handling.addition_to_date(player["starting date"], int(elapsed_time))
        )
        cout(
            "DATE: " + COLOR_STYLE_BRIGHT + COLOR_MAGENTA +
            str(date) + COLOR_RESET_ALL
        )
        text_handling.print_separator('=')
        cout(
            "LOCATION: " + zone[map_zone]["name"] + " (" + COLOR_STYLE_BRIGHT + COLOR_GREEN +
            str(player["x"]) + COLOR_RESET_ALL + ", " + COLOR_STYLE_BRIGHT + COLOR_GREEN +
            str(player["y"]) + COLOR_RESET_ALL + ")"
        )
        cout(
            "INVENTORY: " + COLOR_STYLE_BRIGHT + COLOR_CYAN +
            str(len(player["inventory"]) + 1) + COLOR_RESET_ALL + "/" +
            COLOR_STYLE_BRIGHT + COLOR_CYAN + str(player["inventory slots"]) + COLOR_RESET_ALL
        )
        text_handling.print_separator('=')
        cout("EXP: " + COLOR_STYLE_BRIGHT + COLOR_GREEN + str(round(player["xp"], 2)) + COLOR_RESET_ALL)
        cout("GOLD: " + COLOR_STYLE_BRIGHT + COLOR_YELLOW + str(round(player["gold"], 2)) + COLOR_RESET_ALL)

        bars = 25
        remaining_symbol = "█"
        lost_symbol = "_"
        remaining_bars = round(player["health"] / player["max health"] * bars)
        lost_bars = bars - remaining_bars

        if player["health"] > .66 * player["max health"]:
            health_color = COLOR_GREEN
        elif player["health"] > .33 * player["max health"]:
            health_color = COLOR_YELLOW
        else:
            health_color = COLOR_RED

        cout(
            f"HEALTH of {save_file.split('save_', 1)[1].replace('.yaml', '')}: " +
            f"{player["health"]} / {player["max health"]}"
        )
        cout(
                f"|{health_color}{COLOR_STYLE_BRIGHT}{remaining_bars * remaining_symbol}" +
                f"{lost_bars * lost_symbol}{COLOR_RESET_ALL}|"

        )
        text_handling.print_separator('=')

        cout(
            "FISHING LOCATION: " + COLOR_STYLE_BRIGHT + COLOR_CYAN +
            fishing_location + COLOR_RESET_ALL
        )
        cout("FISHING EQUIPMENT: " + fishing_equipment + COLOR_RESET_ALL)

        # fishing drops
        fishing_stats = {}
        fishing_drops = zone[fishing_location]["fishing"]
        total_drops = len(fishing_drops)
        for drop in fishing_drops:
            if drop not in list(fishing_stats):
                fishing_stats[drop] = 1 / total_drops * 100
            else:
                fishing_stats[drop] += 1 / total_drops * 100

        cout("FISHING DROPS: {")
        count = 1
        for drop in list(fishing_stats):
            text = (
                f" -" + COLOR_BLUE + COLOR_STYLE_BRIGHT + drop + COLOR_RESET_ALL + " : " +
                COLOR_BACK_MAGENTA + COLOR_STYLE_BRIGHT + str(round(fishing_stats[drop]))
                + " %" + COLOR_RESET_ALL
            )
            if not count == len(list(fishing_stats)):
                cout(text)
            else:
                cout(text + "}")
            count += 1

        text_handling.print_separator('=')
        cout("  - [G]ear Up")
        cout("  - [F]ish")
        cout("  - [E]xit")
        text_handling.print_separator('=')
        cout("")
        choice = cinput(COLOR_GREEN + COLOR_STYLE_BRIGHT + "> " + COLOR_RESET_ALL).lower()
        cout("")
        logger_sys.log_message(f"INFO: Player has chosen choice '{choice}'")
        if choice.startswith('g'):
            # Check for fishing rods and lures in the player's inventory
            logger_sys.log_message(f"INFO: Searching for fishing rods in player's inventory")
            at_least_one_fishing_rod = False
            at_least_one_lure = False
            fishing_rods = []
            lures = []
            for which_item in player["inventory"]:
                if item[which_item]["type"] == "Fishing Rod":
                    fishing_rods += [which_item]
                    at_least_one_fishing_rod = True
                elif item[which_item]["type"] == "Lure":
                    lures += [which_item]
                    at_least_one_lure = True

            if not at_least_one_fishing_rod or not at_least_one_lure:
                cout(
                    COLOR_YELLOW + "You don't own the required fishing equipment. You need at least one fishing" +
                    " rod and a lure in order to fish! You can find them in a selling place." + COLOR_RESET_ALL
                )
                time.sleep(2)
            else:
                cout("You own the following fishing rods, please choose one to equip:")
                chosen_rod = terminal_handling.show_menu(fishing_rods)
                cout("You own the following lures, place choose one to equip:")
                chosen_lure = terminal_handling.show_menu(lures)
                cout()
                cout(f"You successfully equipped your {chosen_rod} with your {chosen_lure}!")

                # Actually equip the player with the fishing rod
                logger_sys.log_message(
                    f"INFO: Equipped player with fishing rod '{chosen_rod}' and lure '{chosen_lure}'"
                )
                equipped_rod = chosen_rod
                equipped_lure = chosen_lure
                fishing_equipment = (
                    "Rod: " + COLOR_STYLE_BRIGHT + COLOR_ORANGE_4 + chosen_rod + COLOR_RESET_ALL +
                    ", Lure: " + COLOR_STYLE_BRIGHT + COLOR_ORANGE_4 + chosen_lure + COLOR_RESET_ALL
                )
        elif choice.startswith('f'):
            if fishing_equipment == "None":
                cout(
                    COLOR_YELLOW + "You don't have any fishing rod and lure equipped. You need at least one" +
                    " fishing rod and a lure in order to fish!" + COLOR_RESET_ALL
                )
                time.sleep(2)
            else:
                # Waiting time
                loading = (
                    25 / item[equipped_rod]["speed coefficient"] /
                    item[equipped_lure]["speed coefficient"]
                )
                while loading > 0:
                    cout("Fishing///", end='\r')
                    time.sleep(.25)
                    cout("Fishing|//", end='\r')
                    time.sleep(.25)
                    cout("Fishing||/", end='\r')
                    time.sleep(.25)
                    cout("Fishing|||", end='\r')
                    time.sleep(.25)
                    cout("Fishing/||", end='\r')
                    time.sleep(.25)
                    cout("Fishing//|", end='\r')
                    time.sleep(.25)
                    cout("Fishing///", end='\r')
                    time.sleep(.25)
                    loading -= 1
                # Determine the caught fish
                # (Double chances for catches that're preferred by the player's equipped lure)
                catching_possibilities = []
                catching_possibilities2 = zone[fishing_location]["fishing"]
                encountered_fishes = []
                for i in catching_possibilities2:
                    encountered_fishes += [i]
                    catching_possibilities += [i]
                    if i in item[equipped_lure]["preferred types"] and i not in encountered_fishes:
                        catching_possibilities += [i]
                caught_fish = random.choice(catching_possibilities)
                cout(f"\nFish on!")
                time.sleep(2)
                fish_weight = 1
                if "fishing weight" in item[caught_fish]:
                    fish_weight = item[caught_fish]["fishing weight"]
                if player["difficulty mode"] == 0:
                    fish_weight = fish_weight * 5
                elif player["difficulty mode"] == 2:
                    fish_weight = fish_weight * 10
                else:
                    fish_weight = fish_weight * 7
                total_weight = fish_weight

                player_stamina = item[equipped_rod]["rod strength"]
                if player["difficulty mode"] == 0:
                    player_stamina = player_stamina * 9.25
                elif player["difficulty mode"] == 2:
                    player_stamina = player_stamina * 4.25
                else:
                    player_stamina = player_stamina * 6.25
                total_stamina = player_stamina

                # Small UI inside fishing UI
                global still_fishing2, fish_caught
                still_fishing2 = True
                fish_caught = False
                while still_fishing2:
                    text_handling.clear_prompt()
                    text_handling.print_separator("=")

                    bars = 25
                    remaining_symbol = "█"
                    lost_symbol = "_"

                    remaining_energy_bars = round(fish_weight / total_weight * bars)
                    lost_energy_bars = bars - remaining_energy_bars

                    if remaining_energy_bars > bars:
                        remaining_energy_bars = bars

                    if fish_weight > .66 * total_weight:
                        health_color = COLOR_STYLE_BRIGHT + COLOR_BLUE
                    elif fish_weight > .33 * total_weight:
                        health_color = COLOR_STYLE_BRIGHT + COLOR_CYAN
                    else:
                        health_color = COLOR_STYLE_BRIGHT + COLOR_MAGENTA

                    cout(
                        f"FISH ENERGY: {round(fish_weight)}"
                    )
                    cout(
                        f"|{health_color}{remaining_energy_bars * remaining_symbol}" +
                        f"{lost_symbol * lost_energy_bars}{COLOR_RESET_ALL}|"
                    )

                    remaining_stamina_bars = round(player_stamina / total_stamina * bars)
                    lost_stamina_bars = bars - remaining_stamina_bars

                    if remaining_stamina_bars > bars:
                        remaining_stamina_bars = bars

                    if player_stamina > .66 * total_stamina:
                        health_color = COLOR_STYLE_BRIGHT + COLOR_GREEN
                    elif player_stamina > .33 * total_stamina:
                        health_color = COLOR_STYLE_BRIGHT + COLOR_YELLOW
                    else:
                        health_color = COLOR_STYLE_BRIGHT + COLOR_RED

                    cout(f"{save_file.split('save_', 1)[1].replace('.yaml', '')}'s STAMINA: {round(player_stamina)}")
                    cout(
                        f"|{health_color}{remaining_stamina_bars * remaining_symbol}" +
                        f"{lost_symbol * lost_stamina_bars}{COLOR_RESET_ALL}|"
                    )
                    text_handling.print_separator("=")
                    cout("  - [P]ull")
                    cout("  - [D]efend")
                    cout("  - [G]ive up")
                    text_handling.print_separator('=')
                    cout("")
                    choice2 = cinput(COLOR_GREEN + COLOR_STYLE_BRIGHT + "> " + COLOR_RESET_ALL).lower()
                    cout("")

                    # determine some difficulty coefficients
                    coefficient = random.uniform(1.25, 2.25)
                    if player["difficulty mode"] == 0:
                        coefficient = random.uniform(1.75, 3)
                    if player["difficulty mode"] == 2:
                        coefficient = random.uniform(1.15, 1.75)

                    coefficient2 = random.uniform(1.25, 2.25)
                    if player["difficulty mode"] == 0:
                        coefficient2 = random.uniform(1.15, 1.75)
                    if player["difficulty mode"] == 2:
                        coefficient2 = random.uniform(1.17, 3)

                    if choice2.startswith('p'):

                        lost_energy = round(item[equipped_rod]["rod strength"] / coefficient)
                        lost_stamina = round(item[equipped_rod]["rod strength"] / coefficient2)
                        fish_weight -= lost_energy
                        player_stamina -= lost_stamina

                        cout(f"The fish lost {lost_energy} pts of energy!")
                        cout(f"You lost {lost_stamina} pts of stamina!")
                    elif choice2.startswith('d'):
                        recovered_energy = round((fish_weight / coefficient) / 1.5)
                        recovered_stamina = round(player_stamina / coefficient2)
                        fish_weight += recovered_energy
                        player_stamina += recovered_stamina

                        cout(f"The fish recovered {recovered_energy} pts of energy!")
                        cout(f"You recovered {recovered_stamina} pts of stamina!")
                    elif choice2.startswith('g'):
                        still_fishing2 = False
                    else:
                        cout(f"\nCommand '{choice}' isn't valid")
                    time.sleep(2)

                    # Determine if the player has won or lost the battle
                    if fish_weight <= 0:
                        cout(COLOR_GREEN + "You finally caught the fish!" + COLOR_RESET_ALL)
                        fish_caught = True
                        player["inventory"] += [caught_fish]
                        still_fishing2 = False
                        logger_sys.log_message(f"INFO: Player won battle against fish '{caught_fish}'")
                    elif player_stamina <= 0:
                        cout(COLOR_RED + "The fish was able to swim away!" + COLOR_RESET_ALL)
                        still_fishing2 = False
                        logger_sys.log_message(f"INFO: Player lost battle against fish '{caught_fish}'")
                if fish_caught:
                    cout(f"The fish you caught was a {caught_fish}!")

                # Update the player's fishing diary to contain that new stats
                if caught_fish not in player["caught fishes"]:
                    player["caught fishes"][caught_fish] = {
                        "species": caught_fish,
                        "number of catches": 1,
                        "number of occurrences": 1
                    }
                    logger_sys.log_message(f"INFO: Added an entry for fish '{caught_fish}' in player's fishing diary")
                else:
                    player["caught fishes"][caught_fish]["number of occurrences"] += 1
                    if fish_caught:
                        player["caught fishes"][caught_fish]["number of catches"] += 1
                    logger_sys.log_message(f"INFO: Updated fish '{caught_fish}' entry in player's fishing diary")

                player["caught fishes"]["$stats$"]["number of fish encountered"] += 1
                if fish_caught:
                    player["caught fishes"]["$stats$"]["number of fish caught"] += 1
                    player["caught fishes"]["$stats$"]["fish caught worth in gold"] += item[caught_fish]["gold"]
                logger_sys.log_message("INFO: Updated player's general fishing stats")
                exp_added = random.uniform(1, 6)
                player["xp"] += exp_added
                logger_sys.log_message(f"INFO: Added {exp_added} exp points to player for fishing")
                cout(f"You gained {round(exp_added, 2)} experience points for fishing!")
                time.sleep(2)
        elif choice.startswith('e'):
            still_fishing = False
        else:
            cout(f"\nCommand '{choice2}' isn't valid")
        time.sleep(2)

        # get end time
        end_time = time.time()
        logger_sys.log_message(f"INFO: [FISHING LOOP] Getting end time: '{end_time}'")

        # calculate elapsed time
        elapsed_time2 = end_time - start_time
        logger_sys.log_message(f"INFO: [FISHING LOOP] Getting elapsed time: '{elapsed_time2}'")

        game_elapsed_time = time_handling.return_game_day_from_seconds(elapsed_time2, time_elapsing_coefficient)
        game_elapsed_time = game_elapsed_time
        logger_sys.log_message(f"INFO: [FISHING LOOP] Getting elapsed time in game days: '{game_elapsed_time}'")

        elapsed_time += game_elapsed_time
