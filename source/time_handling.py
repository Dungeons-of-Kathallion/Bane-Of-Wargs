import logger_sys
import colors
from colorama import Fore, Back, Style, init, deinit
from colors import *

# initialize colorama
init()


# Constants
COEFFICIENT = .001389

# Handling Functions

def get_day_time(game_days):
    # calculate day time
    day_time = "PLACEHOLDER"  # .25 = morning .50 = day .75 = evening .0 = night
    day_time_decimal = "." + str(game_days).split(".", 1)[1]
    day_time_decimal = float(day_time_decimal)
    if day_time_decimal < .25 and day_time_decimal > .0:
        day_time = COLOR_RED + COLOR_STYLE_BRIGHT + "☾ NIGHT" + COLOR_RESET_ALL
    elif day_time_decimal > .25 and day_time_decimal < .50:
        day_time = COLOR_BLUE + COLOR_STYLE_BRIGHT + "▲ MORNING" + COLOR_RESET_ALL
    elif day_time_decimal > .50 and day_time_decimal < .75:
        day_time = COLOR_GREEN + COLOR_STYLE_BRIGHT + "☼ DAY" + COLOR_RESET_ALL
    elif day_time_decimal > .75 and day_time_decimal:
        day_time = COLOR_YELLOW + COLOR_STYLE_BRIGHT + "▼ EVENING" + COLOR_RESET_ALL

    return day_time


def return_game_day_from_seconds(seconds):
    game_days = seconds * COEFFICIENT # 180 seconds irl = .25 days in-game

    return game_days


# deinitialize colorama
deinit()
