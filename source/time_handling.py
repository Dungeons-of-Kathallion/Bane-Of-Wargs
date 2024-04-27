# time_handling.py
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
from colors import *
from terminal_handling import cout
# external imports
import calendar
import time
from datetime import datetime, timedelta


# Constants
COEFFICIENT = (1 / 720)
TRAVELING_WAIT = (1 / 7.3)

# Handling Functions


def addition_to_date(date, addition):
    # Get month, day and year and then
    # calculate the addition and return
    # the value
    logger_sys.log_message(f"INFO: Calculating addition of {addition} days to date {date}")
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
    logger_sys.log_message(f"INFO: Calculated addition of {addition} days to date {date} --> {future_date}")

    return future_date


def date_prettifier(date):
    # Get month, day and year and then
    # prettify them and return the value
    logger_sys.log_message(f"INFO: Prettifying date {date}")
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

    if day.startswith("0"):
        day = day.replace("0", "")
    formatted_date = f"{day} {month}, year {year}"
    logger_sys.log_message(f"INFO: Prettified date {date} -- > {formatted_date}")

    return formatted_date


def get_day_time(game_days):
    # calculate day time
    day_time = COLOR_BLUE + COLOR_STYLE_BRIGHT + "▲ MORNING" + COLOR_RESET_ALL  # .25 = morning .50 = day .75 = evening .0 = night
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
    logger_sys.log_message(f"INFO: Calculated day time of game day decimal '{game_days}' --> '{day_time}'")

    return day_time


def return_game_day_from_seconds(seconds, time_elapsing_coefficient):
    logger_sys.log_message(
        f"INFO: Calculating in-game days from seconds '{seconds}'" +
        f", with coefficient '{time_elapsing_coefficient * COEFFICIENT}'"
    )
    game_days = seconds * COEFFICIENT * time_elapsing_coefficient  # 12 minutes irl = one whole game day (1=720*x)

    return game_days


def traveling_wait(traveling_coefficient):
    traveling_time = traveling_coefficient * TRAVELING_WAIT
    logger_sys.log_message(f"INFO: Running traveling waiting time: {traveling_time * 5} seconds of wait")
    cout("...", end="\r")
    time.sleep(traveling_time)
    cout("ø..", end="\r")
    time.sleep(traveling_time)
    cout(".ø.", end="\r")
    time.sleep(traveling_time)
    cout("..ø", end="\r")
    time.sleep(traveling_time)
    cout("...")
    time.sleep(traveling_time)
