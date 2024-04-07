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


def safe_load(file, crash=False) -> dict:
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
        if not crash:
            text_handling.exit_game()
    return output


def dump(data, crash=False) -> str:
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
        if not crash:
            text_handling.exit_game()
    return output
