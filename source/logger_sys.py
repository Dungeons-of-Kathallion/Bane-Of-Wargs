# logging_sys.py
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
import yaml_handling
# external imports
import appdirs
from datetime import *


program_dir = str(appdirs.user_config_dir(appname='Bane-Of-Wargs'))


# Handling functions


def write_message(message):
    with open(f'{program_dir}/logs/{date.today()}.log', 'a') as log_file:
        log_file.write(f'{datetime.now()}: {message}\n')


def log_message(message):
    # Open the user's preferences and get the logging
    # level. Then, determines the message logging level
    # and check if the message should be logged.
    with open(f'{program_dir}/preferences.yaml', 'r') as log_file:
        preferences = yaml_handling.safe_load(log_file)

    info = "INFO: " in message
    debug = "DEBUG: " in message
    warning = "WARNING: " in message
    error = (
        "ERROR: " in message or
        "CRITICAL ERROR: " in message or
        "FATAL ERROR: " in message
    )
    if preferences["logging level"] == 1:
        write_message(message)
    elif preferences["logging level"] == 2 and not info:
        write_message(message)
    elif preferences["logging level"] == 3 and error:
        write_message(message)
    else:
        return False
