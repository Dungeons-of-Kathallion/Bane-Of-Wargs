# camp.py
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
import text_handling
import time_handling
import logger_sys
from colors import *
from terminal_handling import cout, cinput
# external imports
import time


def camp_loop(player, save_file, map_zone, zone, time_elapsing_coefficient):
    logger_sys.log_message(f"INFO: Starting camping loop")
    still_camping = True
    while still_camping:
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
        cout("  - [R]est")
        cout("  - [H]eal")
        cout("  - [E]xit")
        text_handling.print_separator('=')
        cout("")
        choice = cinput(COLOR_GREEN + COLOR_STYLE_BRIGHT + "> " + COLOR_RESET_ALL).lower()
        cout("")
        logger_sys.log_message(f"INFO: Player has chosen choice '{choice}'")
        if choice.startswith('r'):
            loading = 25
            while loading > 0:
                cout("Resting...", end='\r')
                time.sleep(.25)
                cout("Resting,..", end='\r')
                time.sleep(.25)
                cout("Resting.,.", end='\r')
                time.sleep(.25)
                cout("Resting..,", end='\r')
                time.sleep(.25)
                cout("Resting...", end='\r')
                time.sleep(.25)
                cout("Resting,..", end='\r')
                time.sleep(.25)
                cout("Resting.,.", end='\r')
                time.sleep(.25)
                cout("Resting..,", end='\r')
                time.sleep(.25)
                loading -= 1
        elif choice.startswith('h'):
            # Heal all the of the player's health
            # Hard mode -- 2'50"
            # Normal mode -- 1'40"
            # Easy mode -- 1'10"
            if player["difficulty mode"] == 2:
                loading = 75
            elif player["difficulty mode"] == 0:
                loading = 30
            else:
                loading = 45
            while loading > 0:
                cout("Healing___", end='\r')
                time.sleep(.25)
                cout("Healing_-_", end='\r')
                time.sleep(.25)
                cout("Healing---", end='\r')
                time.sleep(.25)
                cout("Healing-_-", end='\r')
                time.sleep(.25)
                cout("Healing___", end='\r')
                time.sleep(.25)
                cout("Healing___", end='\r')
                time.sleep(.25)
                cout("Healing_-_", end='\r')
                time.sleep(.25)
                cout("Healing---", end='\r')
                time.sleep(.25)
                cout("Healing-_-", end='\r')
                time.sleep(.25)
                loading -= 1
            player["health"] = player["max health"]
        elif choice.startswith('e'):
            still_camping = False
        else:
            cout(f"\nCommand '{choice}' isn't valid")
        time.sleep(2)

        # get end time
        end_time = time.time()
        logger_sys.log_message(f"INFO: [CAMPING LOOP] Getting end time: '{end_time}'")

        # calculate elapsed time
        elapsed_time2 = end_time - start_time
        logger_sys.log_message(f"INFO: [CAMPING LOOP] Getting elapsed time: '{elapsed_time2}'")

        game_elapsed_time = time_handling.return_game_day_from_seconds(elapsed_time2, time_elapsing_coefficient)
        game_elapsed_time = game_elapsed_time
        logger_sys.log_message(f"INFO: [CAMPING LOOP] Getting elapsed time in game days: '{game_elapsed_time}'")

        elapsed_time += game_elapsed_time
