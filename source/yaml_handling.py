# yaml_handling.py
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
import logger_sys
from terminal_handling import cout
from colors import *
# external imports
import yaml
import itertools
import time


# Handling functions


def safe_load(file, crash=True) -> dict:
    output = None
    try:
        output = yaml.safe_load(file)
    except Exception as debug:
        cout(
            COLOR_RED + "ERROR: " + COLOR_STYLE_BRIGHT +
            " failed to parse yaml file! Check logs for further information." +
            COLOR_RESET_ALL
        )
        logger_sys.log_message(f"ERROR: Failed to parse yaml file '{file}'")
        logger_sys.log_message(f"DEBUG: {debug}")
        time.sleep(2)
        if crash:
            text_handling.exit_game()
    return output


def dump(data, crash=True) -> str:
    output = None
    try:
        output = yaml.dump(data)
    except Exception as debug:
        cout(
            COLOR_RED + "ERROR: " + COLOR_STYLE_BRIGHT +
            " failed to dump data! Check logs for further information." +
            COLOR_RESET_ALL
        )
        logger_sys.log_message(f"ERROR: Failed to dump data '{dict(itertools.islice(data.items(), 7))}...'")
        logger_sys.log_message(f"DEBUG: {debug}")
        time.sleep(2)
        if crash:
            text_handling.exit_game()
    return output
