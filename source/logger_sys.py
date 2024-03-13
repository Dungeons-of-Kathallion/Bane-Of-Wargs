# external imports
import appdirs
import yaml
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
        preferences = yaml.safe_load(log_file)

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
