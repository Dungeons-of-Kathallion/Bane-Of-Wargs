import appdirs
import logger_sys
import check_yaml
import colors
import os
import yaml
import time
import text_handling
from colorama import Fore, Back, Style, init, deinit
from colors import *

# initialize colorama
init()

# Get program add directory
program_dir = str(appdirs.user_config_dir(appname='Bane-Of-Wargs'))

# Handling functions


def load_game_data(which_type, what_plugin=None):

    # Check if the which_type variable is valid,
    # so if it is not either 'vanilla' or
    # 'plugin' which is inputted, send error
    # and stop the program immediately
    if which_type != 'vanilla' and which_type != 'plugin':
        logger_sys.log_message(f"ERROR: Yaml data loading inputted key '{which_type}' is not valid --> crashing program")
        print(
            f"{COLOR_RED}ERROR: {COLOR_STYLE_BRIGHT}Yaml" +
            f"data loading inputted key '{which_type}' is not valid --> crashing program{COLOR_RESET_ALL}"
        )
        time.sleep(5)
        text_handling.exit_game()

    # If the inputted which_type is vanilla, then just
    # load the vanilla game data

    if which_type == 'vanilla':
        logger_sys.log_message("INFO: Loading vanilla game data")
        with open(program_dir + "/game/data/map.yaml") as f:
            map = yaml.safe_load(f)
            check_yaml.examine(program_dir + '/game/data/map.yaml')

        with open(program_dir + "/game/data/items.yaml") as f:
            item = yaml.safe_load(f)
            check_yaml.examine(program_dir + '/game/data/items.yaml')

        with open(program_dir + "/game/data/drinks.yaml") as f:
            drinks = yaml.safe_load(f)
            check_yaml.examine(program_dir + '/game/data/drinks.yaml')

        with open(program_dir + "/game/data/enemies.yaml") as f:
            enemy = yaml.safe_load(f)
            check_yaml.examine(program_dir + '/game/data/enemies.yaml')

        with open(program_dir + "/game/data/npcs.yaml") as f:
            npcs = yaml.safe_load(f)
            check_yaml.examine(program_dir + '/game/data/npcs.yaml')

        with open(program_dir + "/game/data/start.yaml") as f:
            start_player = yaml.safe_load(f)
            check_yaml.examine(program_dir + '/game/data/start.yaml')

        with open(program_dir + "/game/data/lists.yaml") as f:
            lists = yaml.safe_load(f)
            check_yaml.examine(program_dir + '/game/data/lists.yaml')

        with open(program_dir + "/game/data/zone.yaml") as f:
            zone = yaml.safe_load(f)
            check_yaml.examine(program_dir + '/game/data/zone.yaml')

        with open(program_dir + "/game/data/dialog.yaml") as f:
            dialog = yaml.safe_load(f)
            check_yaml.examine(program_dir + '/game/data/dialog.yaml')

        with open(program_dir + "/game/data/mission.yaml") as f:
            mission = yaml.safe_load(f)
            check_yaml.examine(program_dir + '/game/data/mission.yaml')

        with open(program_dir + "/game/data/mounts.yaml") as f:
            mounts = yaml.safe_load(f)
            check_yaml.examine(program_dir + '/game/data/mounts.yaml')

    else:
        logger_sys.log_message(f"INFO: Loading plugin '{what_plugin}' data")
        check_file = os.path.exists(program_dir + "/plugins/" + what_plugin)
        if not check_file:
            print(COLOR_RED + COLOR_STYLE_BRIGHT + "ERROR: Couldn't find plugin '" + what_plugin + "'" + COLOR_RESET_ALL)
            logger_sys.log_message(f"ERROR: Couldn't find plugin '{what_plugin}'")
            play = 0
            text_handling.exit_game()
        with open(program_dir + "/plugins/" + what_plugin + "/map.yaml") as f:
            map = yaml.safe_load(f)
            check_yaml.examine(program_dir + "/plugins/" + what_plugin + "/map.yaml")

        with open(program_dir + "/plugins/" + what_plugin + "/items.yaml") as f:
            item = yaml.safe_load(f)
            check_yaml.examine(program_dir + "/plugins/" + what_plugin + "/items.yaml")

        with open(program_dir + "/plugins/" + what_plugin + "/drinks.yaml") as f:
            drinks = yaml.safe_load(f)
            check_yaml.examine(program_dir + "/plugins/" + what_plugin + "/drinks.yaml")

        with open(program_dir + "/plugins/" + what_plugin + "/enemies.yaml") as f:
            enemy = yaml.safe_load(f)
            check_yaml.examine(program_dir + "/plugins/" + what_plugin + "/enemies.yaml")

        with open(program_dir + "/plugins/" + what_plugin + "/npcs.yaml") as f:
            npcs = yaml.safe_load(f)
            check_yaml.examine(program_dir + "/plugins/" + what_plugin + "/npcs.yaml")

        with open(program_dir + "/plugins/" + what_plugin + "/start.yaml") as f:
            start_player = yaml.safe_load(f)
            check_yaml.examine(program_dir + "/plugins/" + what_plugin + "/start.yaml")

        with open(program_dir + "/plugins/" + what_plugin + "/lists.yaml") as f:
            lists = yaml.safe_load(f)
            check_yaml.examine(program_dir + "/plugins/" + what_plugin + "/lists.yaml")

        with open(program_dir + "/plugins/" + what_plugin + "/zone.yaml") as f:
            zone = yaml.safe_load(f)
            check_yaml.examine(program_dir + "/plugins/" + what_plugin + "/zone.yaml")

        with open(program_dir + "/plugins/" + what_plugin + "/dialog.yaml") as f:
            dialog = yaml.safe_load(f)
            check_yaml.examine(program_dir + "/plugins/" + what_plugin + "/dialog.yaml")

        with open(program_dir + "/plugins/" + what_plugin + "/mission.yaml") as f:
            mission = yaml.safe_load(f)
            check_yaml.examine(program_dir + "/plugins/" + what_plugin + "/mission.yaml")

        with open(program_dir + "/plugins/" + what_plugin + "/mounts.yaml") as f:
            mounts = yaml.safe_load(f)
            check_yaml.examine(program_dir + "/plugins/" + what_plugin + "/mounts.yaml")

    return map, item, drinks, enemy, npcs, start_player, lists, zone, dialog, mission, mounts


# deinitialize colorama
deinit()
