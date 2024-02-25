import logger_sys
import colors
import calendar
from datetime import datetime, timedelta
from colorama import Fore, Back, Style, init, deinit
from colors import *

# initialize colorama
init()


# Constants
COEFFICIENT = .001389

# Handling Functions


def addition_to_date(date, addition):
    # Get month, day and year and then
    # calculate the addition and return
    # the value
    separated_date = date.split('-', 2)
    month = separated_date[0]
    day = separated_date[1]
    year = separated_date[2]

    date = datetime(int(year), int(month), int(day))

    future_date = str(date + timedelta(days=round(addition)))
    future_date = future_date.split('-', 2)

    new_month = future_date[1]
    new_day = future_date[2].replace(' 00:00:00', '')
    new_year = future_date[0]

    future_date = f"{new_month}-{new_day}-{new_year}"

    return future_date


def date_prettifier(date):
    # Get month, day and year and then
    # prettify them and return the value
    separated_date = date.split('-', 2)
    month = calendar.month_name[int(separated_date[0])]
    day = separated_date[1]
    year = separated_date[2]

    # some formatting stuff

    if (
        day == '11' or
        day == '12' or
        day == '13'
    ):
        day = f"{day}th"
    elif day.endswith('1'):
        day = f"{day}st"
    elif day.endswith('2'):
        day = f"{day.strip('2')}2nd"  # so spell checks is happy ;)
    elif day.endswith('3'):
        day = f"{day}rd"
    else:
        day = f"{day}th"
    formatted_date = f"{day} {month}, year {year}"

    return formatted_date


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


def return_game_day_from_seconds(seconds, time_elapsing_coefficient):
    game_days = seconds * COEFFICIENT * time_elapsing_coefficient  # 180 seconds irl = .25 days in-game

    return game_days


# deinitialize colorama
deinit()
