# source imports
import text_handling
import logger_sys
import enemy_handling
import script_handling
from colors import *
from terminal_handling import cout, cinput
# external imports
import time

def dungeon_loop(player, current_dungeon, lists, enemy, start_player, item):
    logger_sys.log_message(f"INFO: Starting dungeon loop of dungeon '{current_dungeon["dungeon"]["name"]}'")
    still_in_dungeon = True
    current_room = 1
    # Get some dungeon rooms stats
    rooms = {}
    for room in list(current_dungeon["dungeon"]["rooms"]):
        room_data = current_dungeon["dungeon"]["rooms"][room]
        rooms[str(room_data["room digit"])] = room
    while still_in_dungeon:
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
        cout(f"CURRENT ROOM: {color_room}{current_room}{COLOR_RESET_ALL}/{COLOR_GREEN}{current_dungeon["dungeon"]["rooms number"]}{COLOR_RESET_ALL}")
        type_room = current_dungeon["dungeon"]["rooms"][str(rooms[str(current_room)])]["room type"]
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
        cout("  - [I]nventory")
        cout("  - [P]ause Game")
        cout("  - [E]xit Dungeon")
        text_handling.print_separator('=')
        cout("")
        action = cinput(COLOR_GREEN + COLOR_STYLE_BRIGHT + "> " + COLOR_RESET_ALL)
