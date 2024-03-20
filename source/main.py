# source imports
import battle
import check_yaml
import terminal_handling
import mission_handling
import dialog_handling
import enemy_handling
import data_handling
import npc_handling
import text_handling
import zone_handling
import weapon_upgrade_handling
import script_handling
import consumable_handling
import item_handling
import time_handling
import logger_sys
from colors import *
from time_handling import *
from consumable_handling import *
from terminal_handling import cout, cinput
# external imports
import random
import yaml
import os
import time
import fade
import subprocess
import tempfile
import appdirs
import io
import pydoc
from sys import exit
from rich.console import Console
from rich.markdown import Markdown
from rich.table import Table


logger_sys.log_message(f"INFO: GAME RUN START")
text_handling.clear_prompt()

# defines console for the rich module
# to work properly

console = Console()

# says you are not playing.
play = 0

fought_enemy = False

separator = COLOR_STYLE_BRIGHT + "###############################" + COLOR_RESET_ALL


def print_title():
    if preferences["theme"] == "OFF":
        with open(program_dir + '/game/imgs/Title' + str(preferences["title style"]) + '.txt', 'r') as f:
            cout(f.read())
    else:
        if preferences["theme"] == "blackwhite":
            with open(program_dir + '/game/imgs/Title' + str(preferences["title style"]) + '.txt', 'r') as f:
                faded_text = fade.blackwhite(f.read())
                cout(faded_text)
        elif preferences["theme"] == "purplepink":
            with open(program_dir + '/game/imgs/Title' + str(preferences["title style"]) + '.txt', 'r') as f:
                faded_text = fade.purplepink(f.read())
                cout(faded_text)
        elif preferences["theme"] == "greenblue":
            with open(program_dir + '/game/imgs/Title' + str(preferences["title style"]) + '.txt', 'r') as f:
                faded_text = fade.greenblue(f.read())
                cout(faded_text)
        elif preferences["theme"] == "water":
            with open(program_dir + '/game/imgs/Title' + str(preferences["title style"]) + '.txt', 'r') as f:
                faded_text = fade.water(f.read())
                cout(faded_text)
        elif preferences["theme"] == "fire":
            with open(program_dir + '/game/imgs/Title' + str(preferences["title style"]) + '.txt', 'r') as f:
                faded_text = fade.fire(f.read())
                cout(faded_text)
        elif preferences["theme"] == "pinkred":
            with open(program_dir + '/game/imgs/Title' + str(preferences["title style"]) + '.txt', 'r') as f:
                faded_text = fade.pinkred(f.read())
                cout(faded_text)
        elif preferences["theme"] == "purpleblue":
            with open(program_dir + '/game/imgs/Title' + str(preferences["title style"]) + '.txt', 'r') as f:
                faded_text = fade.purpleblue(f.read())
                cout(faded_text)
        elif preferences["theme"] == "brazil":
            with open(program_dir + '/game/imgs/Title' + str(preferences["title style"]) + '.txt', 'r') as f:
                faded_text = fade.brazil(f.read())
                cout(faded_text)
        elif preferences["theme"] == "random":
            with open(program_dir + '/game/imgs/Title' + str(preferences["title style"]) + '.txt', 'r') as f:
                faded_text = fade.random(f.read())
                cout(faded_text)


menu = True

# Check if player has the config folder if
# not, create it with all its required content
program_dir = str(appdirs.user_config_dir(appname='Bane-Of-Wargs'))
first_start = False
if not os.path.exists(program_dir):
    GAME_DATA_VERSION = 0.195
    os.mkdir(program_dir)
    # Open default config file and store the text into
    # a variable to write it into the user config file
    default_config_data = {
        "latest preset": {
            "plugin": " ",
            "save": " ",
            "type": 'vanilla'
        },
        "speed up": False,
        "theme": 'greenblue',
        "title style": 1,
        "auto update": False,
        "logging level": 2,
        "game data download": {
            "branch": "master",
            "repository": "Bane-Of-Wargs",
            "org": "Dungeons-Of-Kathallion"
        }
    }
    default_config_data = yaml.dump(default_config_data)
    with open(program_dir + '/preferences.yaml', 'w') as f:
        f.write(default_config_data)
    logger_sys.log_message(f"INFO: Created player preferences at '{program_dir}/preferences.yaml'")
    # Create the plugins, saves, game data folder in the config file
    logger_sys.log_message("INFO: Creating directory '{program_dir}/plugins'")
    os.mkdir(program_dir + "/plugins")
    logger_sys.log_message("INFO: Creating directory '{program_dir}/saves'")
    os.mkdir(program_dir + "/saves")
    logger_sys.log_message("INFO: Creating directory '{program_dir}/game'")
    os.mkdir(program_dir + "/game")
    logger_sys.log_message("INFO: Creating directory '{program_dir}/logs'")
    os.mkdir(program_dir + "/logs")
    logger_sys.log_message("INFO: Creating directory '{program_dir}/docs'")
    os.mkdir(program_dir + "/docs")
    logger_sys.log_message("INFO: Writing game data version to '{program_dir}/game/VERSION.bow'")
    with open(f"{program_dir}/game/VERSION.bow", 'w') as f:
        f.write(str(GAME_DATA_VERSION))
    first_start = True

# Download game data from github master branch
# and install them (auto-update)
logger_sys.log_message("INFO: Loading user preferences")
with open(program_dir + '/preferences.yaml', 'r') as f:
    preferences = yaml.safe_load(f)
    check_yaml.examine(program_dir + '/preferences.yaml')

# Compare the latest source code version with
# the current code version
logger_sys.log_message("INFO: Checking if game source code is up to date")
global latest_version
latest_version = None  # placeholder
SOURCE_CODE_VERSION = 0.195
latest_main_class = io.StringIO(data_handling.temporary_git_file_download(
    'source/main.py', 'https://github.com/Dungeons-of-Kathallion/Bane-Of-Wargs.git'
)).readlines()

if latest_main_class == []:  # if the file didn't download
    cout("Skipping game updating process...")
    time.sleep(1)
else:
    continuing = True
    count = 0
    while count < len(latest_main_class) and continuing:
        if latest_main_class[count].startswith('SOURCE_CODE_VERSION = '):
            latest_version = latest_main_class[count].split("= ", 1)[1]
            continuing = False
        count += 1

    if float(latest_version) > float(SOURCE_CODE_VERSION):
        latest_version = float(str(latest_version).replace('\n', ''))
        logger_sys.log_message("WARNING: The game source code is outdated")
        logger_sys.log_message(
            f"DEBUG: You're using version {SOURCE_CODE_VERSION} while the latest version is {latest_version}"
        )
        cout(
            COLOR_YELLOW + "WARNING: The game source code is outdated:\nYou're using " +
            f"version {SOURCE_CODE_VERSION} while the latest version is {latest_version}" +
            COLOR_RESET_ALL
        )
        time.sleep(3)
        text_handling.clear_prompt()

    # Get latest game data version
    logger_sys.log_message(f"INFO: Checking if game data at '{program_dir}/game/' is up to date")
    global latest_game_data_version
    latest_game_data_version = None
    try:
        with open(f'{program_dir}/game/VERSION.bow') as f:
            GAME_DATA_VERSION = f.read().replace('\n', '')
    except Exception as error:
        cout(f"ERROR: Couldn't find required file '{program_dir}/game/VERSION.bow'")
        cout(f"DEBUG: Please try to restart the game with the preferences option 'auto update' turned on")
        logger_sys.log_message(f"ERROR: Couldn't find required file '{program_dir}/game/VERSION.bow'")
        logger_sys.log_message(f"DEBUG: Please try to restart the game with the preferences option 'auto update' turned on")
        time.sleep(3)
        text_handling.exit_game()

    continuing = True
    count = 0
    while count < len(latest_main_class) and continuing:
        if latest_main_class[count].startswith('    GAME_DATA_VERSION = '):
            latest_game_data_version = latest_main_class[count].split("= ", 1)[1]
            continuing = False
        count += 1

    if preferences["auto update"] or first_start:
        data_handling.update_game_data(preferences, latest_game_data_version)

    # Compare the latest game data version with
    # the current game data version
    if float(GAME_DATA_VERSION) < float(latest_game_data_version):
        latest_game_data_version = float(str(latest_game_data_version).replace('\n', ''))
        logger_sys.log_message(f"WARNING: The game data at '{program_dir}' is outdated")
        logger_sys.log_message(
            f"DEBUG: You're using version {GAME_DATA_VERSION} while the latest version is {latest_game_data_version}"
        )
        cout(
            COLOR_YELLOW + f"WARNING: The game data at '{program_dir}' is outdated:\nYou're using " +
            f"version {GAME_DATA_VERSION} while the latest version is {latest_game_data_version}" +
            COLOR_RESET_ALL
        )
        time.sleep(3)
        cout("\nDo you want to update your game data right now?")
        want_to_update = terminal_handling.show_menu(["Yes", "No"])
        if want_to_update == "Yes":
            text_handling.clear_prompt()
            data_handling.update_game_data(preferences, latest_game_data_version)
        text_handling.clear_prompt()

# main menu start
while menu:
    global player, previous_player
    # Get player preferences
    logger_sys.log_message(f"INFO: Opening player '{program_dir}/preferences.yaml'")
    with open(program_dir + '/preferences.yaml', 'r') as f:
        preferences = yaml.safe_load(f)
        check_yaml.examine(program_dir + '/preferences.yaml')
    text_handling.clear_prompt()
    print_title()

    options = ['Play Game', 'Manage Saves', 'Preferences', 'Gameplay Guide', 'Check Logs', 'Quit']
    choice = terminal_handling.show_menu(options)
    text_handling.clear_prompt()

    print_title()

    if choice == 'Play Game':
        options = ['Use Latest Preset', 'Play Vanilla', 'Play Plugin']
        choice = terminal_handling.show_menu(options)
        using_latest_preset = False
        latest_preset = preferences["latest preset"]
        # Make these variables global
        global map, item, drinks, enemy, npcs, start_player
        global lists, zone, dialog, mission, mounts

        # load data files
        if choice == 'Use Latest Preset':
            logger_sys.log_message(f"INFO: Starting game with latest preset: {latest_preset}")
            using_latest_preset = True

            if preferences["latest preset"]["type"] == 'vanilla':
                (
                    map, item, drinks, enemy, npcs, start_player,
                    lists, zone, dialog, mission, mounts
                ) = data_handling.load_game_data('vanilla')
            else:

                what_plugin = preferences["latest preset"]["plugin"]
                (
                    map, item, drinks, enemy, npcs, start_player,
                    lists, zone, dialog, mission, mounts
                ) = data_handling.load_game_data('plugin', what_plugin)

            open_save = preferences["latest preset"]["save"]
            save_file = program_dir + "/saves/save_" + open_save + ".yaml"
            check_file = os.path.isfile(save_file)
            if not check_file:
                cout(COLOR_RED + COLOR_STYLE_BRIGHT + "ERROR: Couldn't find save file '" + save_file + "'" + COLOR_RESET_ALL)
                logger_sys.log_message(f"ERROR: Couldn't find save file '{save_file}'")
                play = 0
                text_handling.exit_game()
            logger_sys.log_message("INFO: Opening Save File")
            with open(save_file) as f:
                error_loading = False
                try:
                    player = yaml.safe_load(f)
                except Exception as error:
                    error_loading = True
                previous_player = player
                check_yaml.examine(save_file)
                if type(player) is not type({}) and not error_loading:
                    error_loading = True
                    error = 'not a yaml file'
                if error_loading:
                    cout(
                        COLOR_RED + "FATAL ERROR: " + COLOR_STYLE_BRIGHT +
                        "Save corrupted! Check logs files for further information" + COLOR_RESET_ALL
                    )
                    logger_sys.log_message(f"FATAL ERROR: Save '{save_file}' corrupted!")
                    logger_sys.log_message(
                        f"DEBUG: This could have been the result of closing the game at bad moments or " +
                        "a game bug. Please report the bug on the github repo: " +
                        "https://github.com/Dungeons-of-Kathallion/Bane-Of-Wargs/issues/new/choose"
                    )
                    logger_sys.log_message(f"DEBUG: error '{error}'")
                    time.sleep(5)
                    text_handling.exit_game()
            play = 1
            menu = False
            logger_sys.log_message("INFO: Starting game and exiting menu")

        elif choice == 'Play Plugin':
            text = "Please select a plugin to use"
            text_handling.print_speech_text_effect(text, preferences)
            res = []

            logger_sys.log_message(f"INFO: Searching for plugins in the '{program_dir}/plugins/' directory")
            for search_for_plugins in os.listdir(program_dir + "/plugins/"):
                res.append(search_for_plugins)

            what_plugin = cinput(
                COLOR_STYLE_BRIGHT + "Current plugins: " + COLOR_RESET_ALL +
                COLOR_GREEN + str(res) + COLOR_RESET_ALL + " "
            )
            logger_sys.log_message("INFO: Updating latest preset")
            preferences["latest preset"]["type"] = "plugin"
            preferences["latest preset"]["plugin"] = what_plugin

            (
                map, item, drinks, enemy, npcs, start_player,
                lists, zone, dialog, mission, mounts
            ) = data_handling.load_game_data('plugin', what_plugin)
        else:
            logger_sys.log_message("INFO: Updating latest preset")
            preferences["latest preset"]["type"] = "vanilla"
            preferences["latest preset"]["plugin"] = "none"

            (
                map, item, drinks, enemy, npcs, start_player,
                lists, zone, dialog, mission, mounts
            ) = data_handling.load_game_data('vanilla')

        if not using_latest_preset:
            text = "Please select an action:"
            text_handling.print_speech_text_effect(text, preferences)
            options = ['Open Save', 'New Save']
            choice = terminal_handling.show_menu(options)

            if choice == 'Open Save':
                res = []

                logger_sys.log_message(f"INFO: Searching for saves in the '{program_dir}/saves/' directory")
                for search_for_saves in os.listdir(program_dir + '/saves/'):
                    if search_for_saves.startswith("save_"):
                        res.append(search_for_saves)

                char1 = 'save_'
                char2 = '.yaml'

                for idx, ele in enumerate(res):
                    res[idx] = ele.replace(char1, '')

                for idx, ele in enumerate(res):
                    res[idx] = ele.replace(char2, '')

                text = "Please select a save to open."
                text_handling.print_speech_text_effect(text, preferences)
                open_save = cinput(
                    COLOR_STYLE_BRIGHT + "Current saves: " + COLOR_RESET_ALL +
                    COLOR_GREEN + str(res) + COLOR_RESET_ALL + " "
                )
                logger_sys.log_message("INFO: Updating latest preset")
                preferences["latest preset"]["save"] = open_save

                save_file = program_dir + "/saves/save_" + open_save + ".yaml"
                check_file = os.path.isfile(save_file)
                if not check_file:
                    cout(COLOR_RED + COLOR_STYLE_BRIGHT + "ERROR: Couldn't find save file '" + save_file + "'" + COLOR_RESET_ALL)
                    logger_sys.log_message(f"ERROR: Couldn't find save file '{save_file}'")
                    play = 0
                    text_handling.exit_game()
                logger_sys.log_message("INFO: Opening save file")
                with open(save_file) as f:
                    error_loading = False
                    try:
                        player = yaml.safe_load(f)
                    except Exception as error:
                        error_loading = True
                    previous_player = player
                    check_yaml.examine(save_file)
                    if type(player) is not type({}) and not error_loading:
                        error_loading = True
                        error = 'not a yaml file'
                    if error_loading:
                        cout(
                            COLOR_RED + "FATAL ERROR: " + COLOR_STYLE_BRIGHT +
                            "Save corrupted! Check logs files for further information" + COLOR_RESET_ALL
                        )
                        logger_sys.log_message(f"FATAL ERROR: Save '{save_file}' corrupted!")
                        logger_sys.log_message(
                            f"DEBUG: This could have been the result of closing the game at bad moments or " +
                            "a game bug. Please report the bug on the github repo: " +
                            "https://github.com/Dungeons-of-Kathallion/Bane-Of-Wargs/issues/new/choose"
                        )
                        logger_sys.log_message(f"DEBUG: error '{error}'")
                        time.sleep(5)
                        text_handling.exit_game()
                play = 1
                menu = False
            else:
                text = "Please name your adventurer: "
                text_handling.print_speech_text_effect(text, preferences)
                enter_save_name = cinput('> ')
                player = start_player
                save_name = program_dir + "/saves/save_" + enter_save_name + ".yaml"
                save_name_backup = program_dir + "/saves/~0 save_" + enter_save_name + ".yaml"
                check_file = os.path.isfile(save_name)
                logger_sys.log_message("INFO: Updating latest preset")
                preferences["latest preset"]["save"] = enter_save_name
                if check_file:
                    cout(
                        COLOR_RED + COLOR_STYLE_BRIGHT + "ERROR: Save file '" +
                        save_name + "'" + " already exists" + COLOR_RESET_ALL
                    )
                    logger_sys.log_message(f"ERROR: Save file '{save_name}' already exists")
                    play = 0
                    text_handling.exit_game()
                difficulty_modes = ['Easy', 'Normal', 'Hard']
                cout("\nPlease select a difficulty:")
                difficulty = difficulty_modes.index(terminal_handling.show_menu(difficulty_modes))
                player["difficulty mode"] = difficulty
                logger_sys.log_message(
                    "INFO: Player has chosen difficulty " +
                    f"'{difficulty_modes[difficulty]}'-->'{difficulty}'"
                )
                logger_sys.log_message("INFO: Dumping new save data")
                dumped = yaml.dump(player)
                logger_sys.log_message("INFO: Creating new save")
                with open(save_name, "w") as f:
                    f.write(dumped)
                with open(save_name_backup, "w") as f:
                    f.write(dumped)
                save_file = save_name
                logger_sys.log_message("INFO: Opening save")
                with open(save_file) as f:
                    error_loading = False
                    try:
                        player = yaml.safe_load(f)
                    except Exception as error:
                        error_loading = True
                    previous_player = player
                    if type(player) is not type({}) and not error_loading:
                        error_loading = True
                        error = 'not a yaml file'
                    if error_loading:
                        cout(
                            COLOR_RED + "FATAL ERROR: " + COLOR_STYLE_BRIGHT +
                            "Save corrupted! Check logs files for further information" + COLOR_RESET_ALL
                        )
                        logger_sys.log_message(f"FATAL ERROR: Save '{save_file}' corrupted!")
                        logger_sys.log_message(
                            f"DEBUG: This could have been the result of closing the game at bad moments or " +
                            "a game bug. Please report the bug on the github repo: " +
                            "https://github.com/Dungeons-of-Kathallion/Bane-Of-Wargs/issues/new/choose"
                        )
                        logger_sys.log_message(f"DEBUG: error '{error}'")
                        time.sleep(5)
                        text_handling.exit_game()
                play = 1
                menu = False
                logger_sys.log_message("INFO: Starting game and exiting menu")

    elif choice == 'Manage Saves':

        res = []

        logger_sys.log_message(f"INFO: Searching for saves in the '{program_dir}/saves/' directory")
        for search_for_saves in os.listdir(program_dir + '/saves/'):
            if search_for_saves.startswith("save_"):
                res.append(search_for_saves)

        char1 = 'save_'
        char2 = '.yaml'

        for idx, ele in enumerate(res):
            res[idx] = ele.replace(char1, '')

        for idx, ele in enumerate(res):
            res[idx] = ele.replace(char2, '')

        text = "Please choose an action."
        text_handling.print_speech_text_effect(text, preferences)
        options = ['Edit Save', 'Manage Save Backups', 'Delete Save']
        choice = terminal_handling.show_menu(options)
        if choice == 'Edit Save':
            text = "Please select a save to edit."
            text_handling.print_speech_text_effect(text, preferences)
            open_save = cinput(
                COLOR_STYLE_BRIGHT + "Current saves: " + COLOR_RESET_ALL +
                COLOR_GREEN + str(res) + COLOR_RESET_ALL + " "
            )
            check_file = os.path.isfile(program_dir + "/saves/save_" + open_save + ".yaml")
            if not check_file:
                cout(
                    COLOR_RED + COLOR_STYLE_BRIGHT + "ERROR: Save file '" +
                    program_dir + "/saves/save_" + open_save + ".yaml" +
                    "'" + " does not exists" + COLOR_RESET_ALL
                )
                logger_sys.log_message(f"ERROR: Save file '{program_dir}/saves/save_{open_save}.yaml' does not exists")
                play = 0
            text = "Select an action for the selected save."
            text_handling.print_speech_text_effect(text, preferences)
            options = ['Rename Save', 'Manually Edit Save']
            choice = terminal_handling.show_menu(options)
            if choice == 'Rename Save':
                rename_name = cinput("Select a new name for the save: ")
                os.rename(
                    program_dir + "/saves/save_" + open_save + ".yaml",
                    program_dir + "/saves/save_" + rename_name + ".yaml"
                )
                logger_sys.log_message(
                    f"INFO: Renaming save file '{program_dir}/saves/save_{open_save}.yaml'" +
                    f" to '{program_dir}/saves/save_{rename_name}.yaml'"
                )
            else:
                save_to_open = program_dir + "/saves/save_" + open_save + ".yaml"
                try:
                    editor = os.environ['EDITOR']
                except KeyError:
                    editor = 'nano'
                logger_sys.log_message(f"INFO: Manually editing save file '{save_to_open}' with editor '{editor}'")
                subprocess.call([editor, save_to_open])
        elif choice == "Manage Save Backups":
            text = "Please select a save to manage its backups."
            text_handling.print_speech_text_effect(text, preferences)
            open_save = cinput(
                COLOR_STYLE_BRIGHT + "Current saves: " + COLOR_RESET_ALL +
                COLOR_GREEN + str(res) + COLOR_RESET_ALL + " "
            )
            check_file = os.path.isfile(program_dir + "/saves/save_" + open_save + ".yaml")
            if not check_file:
                cout(
                    COLOR_RED + COLOR_STYLE_BRIGHT + "ERROR: Save file '" +
                    program_dir + "/saves/save_" + open_save + ".yaml" +
                    "'" + " does not exists" + COLOR_RESET_ALL
                )
                logger_sys.log_message(f"ERROR: Save file '{program_dir}/saves/save_{open_save}.yaml' does not exists")
                play = 0
            text = "Select an action for the selected save."
            text_handling.print_speech_text_effect(text, preferences)
            options = ['Create Backup', 'Load Backup']
            choice = terminal_handling.show_menu(options)
            if choice == "Create Backup":
                count = 0
                finished = False
                while count < 120 and not finished:
                    backup_name = program_dir + f"/saves/~{count} save_" + open_save + ".yaml"
                    if not os.path.isfile(backup_name):
                        with open(program_dir + "/saves/save_" + open_save + ".yaml", "r") as f:
                            data = yaml.safe_load(f)
                        with open(backup_name, "w") as f:
                            f.write(yaml.dump(data))
                        cout(f"Created backup of save at '{backup_name}'")
                        logger_sys.log_message(
                            f"INFO: Created backup of save at '{backup_name}'"
                        )
                        time.sleep(1.5)
                        finished = True

                    count += 1
                if not finished:
                    cout(COLOR_YELLOW + "Could not create backup!" + COLOR_RESET_ALL)
                    logger_sys.log_message(
                        "WARNING: Could not create a backup of save " +
                        f"'{program_dir + "/saves/save_" + open_save + ".yaml"}'"
                    )
                    logger_sys.log_message(
                        "DEBUG: This could happen because there're more than 120 backups " +
                        "of this save file, which is the maximum amount that can be handled by the game engine."
                    )
                    time.sleep(1.5)
            else:
                logger_sys.log_message(
                    f"INFO: Searching for backups of save '{program_dir + "/saves/save_" + open_save + ".yaml"}'"
                )
                finished = False
                backups = []
                for i in range(120):
                    current_backup = program_dir + f"/saves/~{i} save_" + open_save + ".yaml"
                    if os.path.isfile(current_backup):
                        backups += [current_backup]
                if backups == []:
                    logger_sys.log_message(
                        f"INFO: Found no backups of save '{program_dir + "/saves/save_" + open_save + ".yaml"}'"
                    )
                    cout(COLOR_YELLOW + "Could not find any backup of this save file" + COLOR_RESET_ALL)
                    time.sleep(1.5)
                    finished = True
                else:
                    logger_sys.log_message(
                        f"INFO: Found backups of save '{program_dir + "/saves/save_" + open_save + ".yaml"}'" +
                        f": {backups}"
                    )
                if not finished:
                    cout("Select a backup to load:")
                    selected_backup = terminal_handling.show_menu(backups, length=75)
                    with open(selected_backup, "r") as f:
                        data = yaml.safe_load(f)
                    with open(program_dir + "/saves/save_" + open_save + ".yaml", "w") as f:
                        f.write(yaml.dump(data))
                    logger_sys.log_message(
                        f"INFO: Loaded backup '{selected_backup}' data to save file '" +
                        f"{program_dir + "/saves/save_" + open_save + ".yaml"}'"
                    )
        else:
            text = "Please select a save to delete."
            text_handling.print_speech_text_effect(text, preferences)
            open_save = cinput(
                COLOR_STYLE_BRIGHT + "Current saves: " + COLOR_RESET_ALL +
                COLOR_GREEN + str(res) + COLOR_RESET_ALL + " "
            )
            check_file = os.path.isfile(program_dir + "/saves/save_" + open_save + ".yaml")
            if not check_file:
                cout(
                    COLOR_RED + COLOR_STYLE_BRIGHT + "ERROR: Save file '" +
                    program_dir + "/saves/save_" + open_save + ".yaml" +
                    "'" + " does not exists" + COLOR_RESET_ALL
                    )
                logger_sys.log_message(f"ERROR: Save file '{program_dir}/saves/save_{open_save}.yaml' does not exists")
                play = 0
            check = cinput("Are you sure you want to delete the following save (y/n)")
            if check.lower().startswith('y'):
                logger_sys.log_message(
                    f"WARNING: Deleting save file '{program_dir}/saves/save_{open_save}.yaml'" +
                    f" and save file backup '{program_dir}/saves/~0 save_{open_save}.yaml'"
                )
                os.remove(program_dir + "/saves/save_" + open_save + ".yaml")
                os.remove(program_dir + "/saves/~0 save_" + open_save + ".yaml")
    elif choice == 'Preferences':
        logger_sys.log_message(f"INFO: Manually editing preferences '{program_dir}/preferences.yaml'")
        logger_sys.log_message(f"DEBUG: Before editing preferences: {preferences}")
        data_handling.open_file(program_dir + "/preferences.yaml")
        with open(program_dir + '/preferences.yaml') as f:
            new_preferences = yaml.safe_load(f)
        logger_sys.log_message(f"DEBUG: After editing preferences: {new_preferences}")
    elif choice == 'Gameplay Guide':
        first_timer = time.time()
        logger_sys.log_message("INFO: Downloading game documentation")
        text = "Downloading game documentation..."
        text_handling.print_speech_text_effect(text, preferences)

        # Download documentation files
        file = 'Gameplay-Guide.md'
        md_file = data_handling.temporary_git_file_download(
            file, 'https://github.com/Dungeons-of-Kathallion/Bane-Of-Wargs.wiki.git'
        )

        last_timer = time.time()
        time_for_process = round(last_timer - first_timer, 4)
        logger_sys.log_message(f"INFO: Finished game documentation downloading process in {time_for_process} seconds")
        text = "Finished downloading process..."
        text_handling.print_speech_text_effect(text, preferences)

        # Actually display the markdown file
        # to the terminal with 'rich' module
        error_occurred = False

        text_handling.clear_prompt()

        try:
            md_text = Markdown(md_file)
            console.print(md_text)

            cinput()
        except Exception as error:
            error_occurred = True
            cout(
                COLOR_RED + COLOR_STYLE_BRIGHT + "ERROR: " + COLOR_RESET_ALL +
                COLOR_RED + f"file '{file}' does not exists" + COLOR_RESET_ALL
            )
            logger_sys.log_message(f"ERROR: file '{file}' does not exists --> canceling gameplay guide markdown printing")
        text_handling.clear_prompt()
    elif choice == 'Check Logs':
        # Get the logs directory content
        # and save the names in a list
        directory = f'{program_dir}/logs/'
        directory_content = os.listdir(directory)

        # Create the rich table
        table = Table(title=f"LOGS FILES: ({directory})")
        table.add_column("Input Number", style="cyan", no_wrap=True)
        table.add_column("Title", style="magenta")

        # Add one by one every files in
        # the logs directory
        count = 0
        for i in directory_content:
            table.add_row(str(count), str(i))

            count += 1
        console.print(table)

        # Get which log the player wants
        # to open and display it in the UI
        loop = True
        while loop:
            error_happened = False
            which_log_file = cinput(f"{COLOR_GREEN}{COLOR_STYLE_BRIGHT}>{COLOR_RESET_ALL} ")
            try:
                which_log_file = directory_content[int(which_log_file)]
            except Exception as error:
                error_happened = True
                cout(COLOR_YELLOW + "incorrect input" + COLOR_RESET_ALL)

            if not error_happened:
                loop = False
                text_handling.clear_prompt()
                with open(directory + which_log_file, 'r') as f:
                    content = f.read()

                    pydoc.pager(content)
    else:
        text_handling.clear_prompt()
        exit(0)


# function to search through the map file
def search(x, y):
    logger_sys.log_message(f"INFO: Searching for map point corresponding to coordinates x:{x}, y:{y}")
    global map_location
    map_point_count = int(len(list(map)))
    for i in range(0, map_point_count):
        point_i = map["point" + str(i)]
        point_x, point_y = point_i["x"], point_i["y"]
        if point_x == x and point_y == y:
            map_location = i
            return map_location


def add_gold(amount):
    logger_sys.log_message(f"INFO: Adding to player {amount} gold")
    player_gold = player["gold"]
    player_gold += float(amount)
    player["gold"] = round(player_gold, 2)


def remove_gold(amount):
    logger_sys.log_message(f"INFO: Removing to player {amount} gold")
    player_gold = player["gold"]
    player_gold -= float(amount)
    player["gold"] = round(player_gold, 2)


def check_for_key(direction):
    logger_sys.log_message("INFO: Checking for key at every next locations possible")
    map_point_count = len(list(map))
    if direction == "north":
        for i in range(0, map_point_count):
            point_i = map["point" + str(i)]
            point_x, point_y = point_i["x"], point_i["y"] - 1
            if point_x == player["x"] and point_y == player["y"]:
                future_map_location = i
    elif direction == "south":
        for i in range(0, map_point_count):
            point_i = map["point" + str(i)]
            point_x, point_y = point_i["x"], point_i["y"] + 1
            if point_x == player["x"] and point_y == player["y"]:
                future_map_location = i
    elif direction == "east":
        for i in range(0, map_point_count):
            point_i = map["point" + str(i)]
            point_x, point_y = point_i["x"] - 1, point_i["y"]
            if point_x == player["x"] and point_y == player["y"]:
                future_map_location = i
    elif direction == "west":
        for i in range(0, map_point_count):
            point_i = map["point" + str(i)]
            point_x, point_y = point_i["x"] + 1, point_i["y"]
            if point_x == player["x"] and point_y == player["y"]:
                future_map_location = i
    elif direction == "north-east":
        for i in range(0, map_point_count):
            point_i = map["point" + str(i)]
            point_x, point_y = point_i["x"] + 1, point_i["y"] + 1
            if point_x == player["x"] and point_y == player["y"]:
                future_map_location = i
    elif direction == "north-west":
        for i in range(0, map_point_count):
            point_i = map["point" + str(i)]
            point_x, point_y = point_i["x"] - 1, point_i["y"] + 1
            if point_x == player["x"] and point_y == player["y"]:
                future_map_location = i
    elif direction == "south-east":
        for i in range(0, map_point_count):
            point_i = map["point" + str(i)]
            point_x, point_y = point_i["x"] + 1, point_i["y"] - 1
            if point_x == player["x"] and point_y == player["y"]:
                future_map_location = i
    elif direction == "south-west":
        for i in range(0, map_point_count):
            point_i = map["point" + str(i)]
            point_x, point_y = point_i["x"] - 1, point_i["y"] - 1
            if point_x == player["x"] and point_y == player["y"]:
                future_map_location = i
    if "key" in map["point" + str(future_map_location)]:
        text = '='
        text_handling.print_separator(text)

        text = "You need the following key(s) to enter this location, if you decide to use them, you may loose them:"
        text_handling.print_long_string(text)

        keys_list = str(map["point" + str(future_map_location)]["key"]["required keys"])
        logger_sys.log_message(f"INFO: Entering map point 'point{future_map_location}' requires keys: {keys_list}")
        keys_list = keys_list.replace("'", '')
        keys_list = keys_list.replace("[", ' -')
        keys_list = keys_list.replace("]", '')
        keys_list = keys_list.replace(", ", '\n -')

        cout(keys_list)

        keys_len = len(map["point" + str(future_map_location)]["key"]["required keys"])

        text = '='
        text_handling.print_separator(text)

        options = ['Continue', 'Leave']
        choice = terminal_handling.show_menu(options)

        count = 0

        have_necessary_keys = True

        if choice == 'Continue':
            while count < keys_len and have_necessary_keys:

                chosen_key = map["point" + str(future_map_location)]["key"]["required keys"][int(count)]

                if chosen_key not in player["inventory"]:
                    have_necessary_keys = False
                else:
                    if map["point" + str(future_map_location)]["key"]["remove key"]:
                        player["inventory"].remove(chosen_key)
                        logger_sys.log_message(f"INFO: Removing from player inventory key '{chosen_key}'")

                count += 1

            if not have_necessary_keys:
                logger_sys.log_message("INFO: Player don't have necessary keys: passing")
                cout(" ")
                text = COLOR_YELLOW + "You don't have the necessary key(s) to enter this locations"
                text_handling.print_long_string(text)
                time.sleep(1.5)
            if have_necessary_keys:
                logger_sys.log_message("INFO: Player has necessary keys: letting him pass")
                if direction == "north":
                    player["y"] += 1
                elif direction == "south":
                    player["y"] -= 1
                elif direction == "east":
                    player["x"] += 1
                elif direction == "west":
                    player["x"] -= 1


# Loading text replacements
logger_sys.log_message("INFO: Loading generic texts replacements")
save_file_name_text_replacements = save_file.replace(program_dir + '/saves/save_', '')
save_file_name_text_replacements = save_file_name_text_replacements.replace('.yaml', '')
if str(player["current mount"]) == ' ':
    player_mount = None
    player_mount_nick = None
else:
    player_mount = player["mounts"][str(player["current mount"])]["mount"]
    player_mount_nick = player["mounts"][str(player["current mount"])]["name"]

text_replacements_generic = {
    "$name": save_file_name_text_replacements,
    "$currency": player["gold"],
    "$date": player["elapsed time game days"],
    "$location": f'{player["x"]}, {player["y"]}',
    "$coord_x": player["x"],
    "$coord_y": player["y"],
    "$location_zone": player["map zone"],
    "$mount": player_mount,
    "$mount_nick": player_mount_nick,
    "$weapon": player["held item"],
    "$chestplate": player["held chestplate"],
    "$leggins": player["held leggings"],
    "$boots": player["held boots"],
    "$shield": player["held shield"],
    "$health": player["health"],
    "$max_health": player["max health"],
    "$exp": player["xp"]
}
logger_sys.log_message(f"INFO: Loaded generic texts replacements: '{text_replacements_generic}'")


def check_for_item(item_name):
    logger_sys.log_message(f"INFO: Checking if item '{item_name}' actually exists")
    item_exist = False
    if str(item_name) in list(item):
        item_exist = True
    return item_exist


# gameplay here:
def run(play):
    if not preferences["speed up"]:
        # clear text
        text_handling.clear_prompt()

        logger_sys.log_message("INFO: Printing loading menu")
        cout(separator)
        cout(COLOR_GREEN + COLOR_STYLE_BRIGHT + "Reserved keys:" + COLOR_RESET_ALL)
        cout(COLOR_BLUE + COLOR_STYLE_BRIGHT + "N: " + COLOR_RESET_ALL + "Go north" + COLOR_RESET_ALL)
        cout(COLOR_BLUE + COLOR_STYLE_BRIGHT + "S: " + COLOR_RESET_ALL + "Go south" + COLOR_RESET_ALL)
        cout(COLOR_BLUE + COLOR_STYLE_BRIGHT + "E: " + COLOR_RESET_ALL + "Go east" + COLOR_RESET_ALL)
        cout(COLOR_BLUE + COLOR_STYLE_BRIGHT + "W: " + COLOR_RESET_ALL + "Go west" + COLOR_RESET_ALL)
        cout(COLOR_BLUE + COLOR_STYLE_BRIGHT + "D: " + COLOR_RESET_ALL + "Access to your diary.")
        cout(
            COLOR_BLUE + COLOR_STYLE_BRIGHT + "I: " + COLOR_RESET_ALL +
            "View items. When in this view, type the name of an item to examine it." +
            COLOR_RESET_ALL
        )
        cout(
            COLOR_BLUE + COLOR_STYLE_BRIGHT + "Y: " + COLOR_RESET_ALL +
            "View mounts. When in this view, type the name of the mount to examine it." +
            COLOR_RESET_ALL
        )
        cout(COLOR_BLUE + COLOR_STYLE_BRIGHT + "Z: " + COLOR_RESET_ALL + "Access to nearest hostel, stable or church.")
        cout(COLOR_BLUE + COLOR_STYLE_BRIGHT + "P: " + COLOR_RESET_ALL + "Pause game")
        cout(COLOR_BLUE + COLOR_STYLE_BRIGHT + "K: " + COLOR_RESET_ALL + "Save game")
        cout(COLOR_BLUE + COLOR_STYLE_BRIGHT + "Q: " + COLOR_RESET_ALL + "Quit & save game")
        cout(" ")
        cout(COLOR_GREEN + COLOR_STYLE_BRIGHT + "Hints:" + COLOR_RESET_ALL)
        cout("If you find an item on the ground, type the name of the item to take it.")
        cout(
            "Some items have special triggers, which will often" +
            " be stated in the description. Others can only be activated" +
            " in certain situations, like in combat."
        )
        cout(separator)
        cout(" ")

        loading = 4
        while loading > 0:
            cout("Loading game... ▁▁▁", end='\r')
            time.sleep(.15)
            cout("Loading game... ▁▁▃", end='\r')
            time.sleep(.15)
            cout("Loading game... ▁▃▅", end='\r')
            time.sleep(.15)
            cout("Loading game... ▃▅▅", end='\r')
            time.sleep(.15)
            cout("Loading game... ▅▅▅", end='\r')
            time.sleep(.15)
            cout("Loading game... ▅▅▃", end='\r')
            time.sleep(.15)
            cout("Loading game... ▅▃▁", end='\r')
            time.sleep(.15)
            cout("Loading game... ▃▁▁", end='\r')
            time.sleep(.15)
            cout("Loading game... ▁▁▁", end='\r')
            time.sleep(.15)
            loading -= 1

    # Mapping stuff

    while play == 1:
        global player, previous_player

        # get start time
        start_time = time.time()
        logger_sys.log_message(f"INFO: Getting start time: '{start_time}'")

        # get terminal size
        logger_sys.log_message("INFO: Getting terminal width and height size")
        terminal_rows, terminal_columns = os.popen('stty size', 'r').read().split()
        logger_sys.log_message(f"INFO: Got terminal width and height size: {terminal_rows}x{terminal_columns}")

        # clear text
        text_handling.clear_prompt()

        # All the actions to update the player
        # save data;
        # update player ridded mount location:
        if player["current mount"] in player["mounts"]:
            map_location = search(player["x"], player["y"])
            logger_sys.log_message(f"INFO: Updating player ridden mount location to map point 'point{map_location}'")
            player["mounts"][player["current mount"]]["location"] = "point" + str(map_location)

        logger_sys.log_message("INFO: Making sure player ridden mount level is not higher than its maximum")
        # if player current mount level is higher than its max,
        # set it back to its max level
        if player["current mount"] in player["mounts"]:
            current_mount_data = player["mounts"][str(player["current mount"])]
            current_mount_type = str(current_mount_data["mount"])
            if current_mount_data["level"] > mounts[current_mount_type]["levels"]["max level"]:
                player["mounts"][str(player["current mount"])]["level"] = mounts[current_mount_type]["levels"]["max level"]

        logger_sys.log_message("INFO: Updating player ridden mount stats following its level")
        # update player current mount stats following its level
        if player["current mount"] in player["mounts"]:
            current_mount_data = player["mounts"][str(player["current mount"])]
            current_mount_type = str(current_mount_data["mount"])
            if current_mount_data["level"] >= 1:
                player["mounts"][
                    str(player["current mount"])
                ]["stats"]["agility addition"] = round(
                    mounts[current_mount_type]["stats"]["agility addition"] +
                    (mounts[current_mount_type]["levels"][
                        "level stat additions"
                    ]["agility addition"] * (round(current_mount_data["level"]) - 1)), 3
                )
                player["mounts"][
                    str(player["current mount"])
                ]["stats"]["resistance addition"] = round(
                    mounts[current_mount_type]["stats"]["resistance addition"] +
                    (mounts[current_mount_type]["levels"][
                        "level stat additions"
                    ]["resistance addition"] * (round(current_mount_data["level"]) - 1)), 3
                )
                player["mounts"][
                    str(player["current mount"])
                ]["mph"] = (
                    mounts[current_mount_type]["mph"] + mounts[current_mount_type]["levels"][
                        "level stat additions"
                    ]["mph addition"] * round(current_mount_data["level"] - 1)
                )

        logger_sys.log_message("INFO: Verifying player equipped equipment is in the player's inventory")
        # verify if player worn equipment are in his inventory
        if str(player["held item"]) not in player["inventory"]:
            player["held item"] = " "
        if str(player["held chestplate"]) not in player["inventory"]:
            player["held chestplate"] = " "
        if str(player["held leggings"]) not in player["inventory"]:
            player["held leggings"] = " "
        if str(player["held boots"]) not in player["inventory"]:
            player["held boots"] = " "
        if str(player["held shield"]) not in player["inventory"]:
            player["held shield"] = " "

        logger_sys.log_message("INFO: Making sure player's health is an integer")
        # Round player health so it's an integer
        player["health"] = round(player["health"])

        # Calculate day time
        logger_sys.log_message("INFO: Calculating day time")
        global day_time
        day_time = time_handling.get_day_time(player["elapsed time game days"])

        logger_sys.log_message("INFO: Calculating player armor protection stat")
        # Calculate player global armor protection
        # and stores it in a player variable
        global_armor_protection = 0

        # First, get every item in the player equipment
        # and add their protection value to the global
        # armor protection new created variable
        held_item_list = [
            'held boots', 'held chestplate',
            'held leggings', 'held shield'
        ]
        for i in held_item_list:
            item_name = player[i]
            if item_name != " ":
                global_armor_protection += item[item_name]["armor protection"]

        # Then, calculate the player ridden mount -- if he has
        # one -- protection stat and add it to the global armor
        # protection variable
        if player["current mount"] in player["mounts"]:
            global_armor_protection += player["mounts"][player["current mount"]]["stats"]["resistance addition"]

        player["armor protection"] = round(global_armor_protection, 2)

        logger_sys.log_message("INFO: Calculating player agility stat")

        # Calculate player global agility and stores
        # it in a player variable
        global_agility = 0

        # First, get every item in the player equipment
        # and add their agility value to the global agility
        # new created variable
        held_item_list = [
            'held boots', 'held chestplate', 'held item',
            'held leggings', 'held shield'
        ]
        for i in held_item_list:
            item_name = player[i]
            if item_name != " ":
                global_agility += item[item_name]["agility"]

        # Then, calculate the player ridden mount -- if he has
        # one -- agility stat and add it to the global agility
        # variable
        if player["current mount"] in player["mounts"]:
            global_agility += player["mounts"][player["current mount"]]["stats"]["agility addition"]

        player["agility"] = round(global_agility, 2)  # here we round the actual value

        logger_sys.log_message("INFO: Calculating player remaining inventory slots and total inventory slots")
        # Calculate player inventory slots and also
        # remaining inventory slots and then write
        # it to the corresponding variables in the
        # player data dictionary variable
        player_inventory = player["inventory"]
        inventory_slots = 0
        inventory_slots_max = 0
        for i in player_inventory:
            # If the item isn't in the item dictionary, then
            # output a fatal error and shut down the program
            if i not in list(item):
                text = (
                    COLOR_RED + COLOR_STYLE_BRIGHT +
                    "FATAL ERROR: You have an item in your inventory that isn't" +
                    f" in the item data: '{i}' item doesn't exists. This could have been the " +
                    "result of using or not using a plugins. Verify you are using the" +
                    " right plugin for this save or manually remove that item from you " +
                    "player save data in the 'Manage Saves' in the main menu" +
                    COLOR_RESET_ALL
                )
                logger_sys.log_message(f"CRITICAL: Player have an item that doesn't exists: '{i}'")
                logger_sys.log_message(
                    "DEBUG: This could have been the " +
                    "result of using or not using a plugins. Verify you are using the" +
                    " right plugin for this save or manually remove that item from you " +
                    "player save data in the 'Manage Saves' in the main menu"
                )
                text_handling.print_long_string(text)
                time.sleep(10)
                text_handling.clear_prompt()
                text_handling.exit_game()
            else:
                inventory_slots -= 1
                if item[i]["type"] == "Bag":
                    inventory_slots += item[i]["inventory slots"]
                    inventory_slots_max += item[i]["inventory slots"]

        player["inventory slots remaining"] = inventory_slots
        player["inventory slots"] = inventory_slots_max

        map_location = search(player["x"], player["y"])
        logger_sys.log_message("INFO: Checking player location is valid")
        # check player map location
        if map_location is None:
            text = (
                COLOR_RED + COLOR_STYLE_BRIGHT +
                "FATAL ERROR: You are in an undefined location. This could have" +
                " been the result of using or not using a plugin. Verify you " +
                "are using the right plugin for this save or manually modify your " +
                "player coordinates in the 'Manage Saves' in the main menu. The game will close in 10 secs." +
                COLOR_RESET_ALL
            )
            logger_sys.log_message("CRITICAL: Player is in an undefined location.")
            logger_sys.log_message(
                "DEBUG: This could have been the result of using or not " +
                "using a plugin. Verify you are using the right plugin for this " +
                "save or manually modify your player coordinates in the 'Manage Saves' in the main menu."
            )
            text_handling.print_long_string(text)
            time.sleep(10)
            text_handling.clear_prompt()
            text_handling.exit_game()
        logger_sys.log_message("INFO: Getting player current map zone location")
        map_zone = map["point" + str(map_location)]["map zone"]
        logger_sys.log_message("INFO: Updating player 'map zone' in the save file")
        player["map zone"] = map_zone

        # check player map zone
        if map_zone not in list(zone):
            text = (
                COLOR_RED + COLOR_STYLE_BRIGHT +
                "FATAL ERROR: You are in an undefined map zone. This could have" +
                " been the result of using or not using a plugin. Verify you " +
                "are using the right plugin for this save. " +
                "The game will close in 10 secs." +
                COLOR_RESET_ALL
            )
            logger_sys.log_message("CRITICAL: Player is in an undefined map zone.")
            logger_sys.log_message(
                "DEBUG: This could have been the result of using or not " +
                "using a plugin. Verify you are using the right plugin for this " +
                "save."
            )
            text_handling.print_long_string(text)
            time.sleep(10)
            text_handling.clear_prompt()
            text_handling.exit_game()

        logger_sys.log_message(
            f"INFO: Checking if player current map point 'point{map_location}'" +
            f" and map zone '{map_zone}' are already known by the player"
        )
        # add current player location and map
        # zone to visited areas in the player
        # save file if there aren't there yet
        if map_location not in player["visited points"]:
            logger_sys.log_message(f"INFO: Adding current map point 'point{map_location}' to player visited points")
            player["visited points"].append(map_location)

        if map_zone not in player["visited zones"]:
            logger_sys.log_message(f"INFO: Adding current map zone '{map_zone}' to player visited map zones")
            player["visited zones"].append(map_zone)

        logger_sys.log_message("INFO: Printing GUI")
        text = '='
        text_handling.print_separator(text)

        cout("DAY TIME: " + day_time)
        cout(
            "LOCATION: " + map_zone + " (" + COLOR_STYLE_BRIGHT + COLOR_GREEN +
            str(player["x"]) + COLOR_RESET_ALL + ", " + COLOR_STYLE_BRIGHT + COLOR_GREEN +
            str(player["y"]) + COLOR_RESET_ALL + ")"
        )

        # Handle groceries stores randomly picked
        # sales and create the corresponding data
        # in the player dictionary data.
        groceries = []
        for i in list(zone):
            if zone[i]["type"] == "grocery":
                groceries += [i]

        for grocery in groceries:
            if grocery not in list(player["groceries data"]):
                items_sales = zone_handling.determine_grocery_sales(zone[grocery])
                player["groceries data"][grocery] = {
                    "date": int(player["elapsed time game days"]),
                    "items sales": items_sales
                }
            elif player["groceries data"][grocery]["date"] != int(player["elapsed time game days"]):
                items_sales = zone_handling.determine_grocery_sales(zone[grocery])
                player["groceries data"][grocery] = {
                    "date": int(player["elapsed time game days"]),
                    "items sales": items_sales
                }

        # Calculate the enemies global damage
        # coefficient, depending on the player
        # elapsed time in game-days
        #
        # Here's the calculation settings:
        # x < 25days  => .85
        # x < 45days  => .95
        # x < 50days  => 1
        # x < 80days  => 1.15
        # x < 100days => 1.25
        # x < 150days => 1.35
        # x < 220days => 1.45
        # x < 300days => 1.5
        global enemies_damage_coefficient
        enemies_damage_coefficient = 1  # placeholder
        if player["elapsed time game days"] < 25:
            enemies_damage_coefficient = .85
        elif player["elapsed time game days"] < 45:
            enemies_damage_coefficient = .95
        elif player["elapsed time game days"] < 50:
            enemies_damage_coefficient = 1
        elif player["elapsed time game days"] < 80:
            enemies_damage_coefficient = 1.15
        elif player["elapsed time game days"] < 100:
            enemies_damage_coefficient = 1.25
        elif player["elapsed time game days"] < 150:
            enemies_damage_coefficient = 1.35
        elif player["elapsed time game days"] < 220:
            enemies_damage_coefficient = 1.45
        elif player["elapsed time game days"] < 300:
            enemies_damage_coefficient = 1.5
        else:
            enemies_damage_coefficient = 1.5

        # Calculating traveling coefficient, depending
        # on the player inventory size and its mounts
        # stats, if he has one
        global traveling_coefficient
        traveling_coefficient = 1

        player_inventory_weight = len(player["inventory"]) / 100
        traveling_coefficient += player_inventory_weight

        if player["current mount"] != " ":
            mount_mph = player["mounts"][player["current mount"]]["mph"]
            traveling_coefficient -= mount_mph / 100

        # All the checks for the player active effects
        # are done here
        #
        # If the player has any active effects, load
        # them one by one and update them depending
        # on their dictionary content and type
        global player_damage_coefficient, time_elapsing_coefficient
        player_damage_coefficient = 1
        time_elapsing_coefficient = 1
        if player["held item"] != " ":
            player["critical hit chance"] = item[player["held item"]]["critical hit chance"]
        else:
            player["critical hit chance"] = 0
        if player["active effects"] != {}:
            for i in list(player["active effects"]):
                current_effect = player["active effects"][i]
                effect_over = False
                # Run the actions for every effect type
                if current_effect["type"] == 'healing':
                    # Check if the effect duration's over
                    if (
                        (
                            current_effect["effect duration"] + current_effect["effect starting time"]
                        ) < player["elapsed time game days"]
                    ):
                        # Remove that effect from the player
                        # active effects and set the player
                        # modified stats to before the effect
                        # happened
                        player["active effects"].pop(i)
                        player["health"] = current_effect["before stats"]["health"]
                        player["max health"] = current_effect["before stats"]["max health"]
                        effect_over = True
                    # Check if the effect has already been
                    # applied or not
                    if not current_effect["already applied"] and not effect_over:
                        # Apply that effect changes now
                        if current_effect["effects"]["health changes"] >= 999:
                            player["health"] = player["max health"]
                        else:
                            player["health"] += current_effect["effects"]["health changes"]
                        player["max health"] += current_effect["effects"]["max health changes"]
                        player["active effects"][i]["already applied"] = True
                elif current_effect["type"] == 'protection':
                    # Check if the effect duration's over
                    if (
                        (
                            current_effect["effect duration"] + current_effect["effect starting time"]
                        ) < player["elapsed time game days"] and current_effect["effect duration"] != 999
                    ):
                        # Remove that effect from the player
                        # active effects
                        player["active effects"].pop(i)
                        effect_over = True
                    # Apply the effect effects if the
                    # effect isn't over
                    if not effect_over:
                        player["armor protection"] = player["armor protection"] * current_effect[
                            "effects"
                        ]["protection coefficient"]
                elif current_effect["type"] == 'strength':
                    # Check if the effect duration's over
                    if (
                        (
                            current_effect["effect duration"] + current_effect["effect starting time"]
                        ) < player["elapsed time game days"] and current_effect["effect duration"] != 999
                    ):
                        # Remove that effect from the player
                        # active effects
                        player["active effects"].pop(i)
                        effect_over = True
                    # Apply the effect effects if the
                    # effect isn't over
                    if not effect_over:
                        player["critical hit chance"] = player["critical hit chance"] * current_effect["effects"][
                            "critical hit chance coefficient"
                        ]
                        # If the player already has an effect that changes
                        # the damage coefficient and that's greater, don't
                        # apply the current effect coefficient
                        # = keep the greater one
                        if not player_damage_coefficient > current_effect["effects"]["damage coefficient"]:
                            player_damage_coefficient = current_effect["effects"]["damage coefficient"]
                elif current_effect["type"] == 'agility':
                    # Check if the effect duration's over
                    if (
                        (
                            current_effect["effect duration"] + current_effect["effect starting time"]
                        ) < player["elapsed time game days"] and current_effect["effect duration"] != 999
                    ):
                        # Remove that effect from the player
                        # active effects
                        player["active effects"].pop(i)
                        effect_over = True
                    # Apply the effect effects if the
                    # effect isn't over
                    if not effect_over:
                        player["agility"] = player["agility"] * current_effect[
                            "effects"
                        ]["agility coefficient"]
                elif current_effect["type"] == 'time elapsing':
                    # Check if the effect duration's over
                    if (
                        (
                            current_effect["effect duration"] + current_effect["effect starting time"]
                        ) < player["elapsed time game days"] and current_effect["effect duration"] != 999
                    ):
                        # Remove that effect from the player
                        # active effects
                        player["active effects"].pop(i)
                        effect_over = True
                    # Apply the effect effects if the
                    # effect isn't over
                    if not effect_over:
                        # If the player already has an effect that changes
                        # the damage coefficient, make so that the global
                        # coefficient gets added that effect coefficient
                        if time_elapsing_coefficient != 1:
                            time_elapsing_coefficient = (
                                time_elapsing_coefficient * current_effect["effects"]["time elapsing coefficient"]
                            )
                        else:
                            time_elapsing_coefficient = current_effect["effects"]["time elapsing coefficient"]

        # UI Printing

        text = '='
        text_handling.print_separator(text)

        text_handling.print_zone_map(map_zone, zone, player, preferences)

        text = '='
        text_handling.print_separator(text)

        cout("DIRECTIONS: " + "          ACTIONS:")

        blocked_locations = map["point" + str(map_location)]["blocked"]
        if "North" not in blocked_locations:
            cout("Can go North ⬆    " + "    " + COLOR_BLUE + COLOR_STYLE_BRIGHT + "I: " + COLOR_RESET_ALL + "View items")
        else:
            cout("                  " + "    " + COLOR_BLUE + COLOR_STYLE_BRIGHT + "I: " + COLOR_RESET_ALL + "View items")
        if "South" not in blocked_locations:
            cout("Can go South ⬇    " + "    " + COLOR_BLUE + COLOR_STYLE_BRIGHT + "D: " + COLOR_RESET_ALL + "Check your diary")
        else:
            cout("                  " + "    " + COLOR_BLUE + COLOR_STYLE_BRIGHT + "D: " + COLOR_RESET_ALL + "Check your diary")
        if "East" not in blocked_locations:
            cout(
                "Can go East ➡    " + "     " + COLOR_BLUE + COLOR_STYLE_BRIGHT + "Z: " +
                COLOR_RESET_ALL + "Interact with zone"
            )
        else:
            cout(
                "                 " + "     " + COLOR_BLUE + COLOR_STYLE_BRIGHT +
                "Z: " + COLOR_RESET_ALL + "Interact with zone"
            )
        if "West" not in blocked_locations:
            cout("Can go West ⬅    " + "     " + COLOR_BLUE + COLOR_STYLE_BRIGHT + "Y: " + COLOR_RESET_ALL + "View owned mounts")
        else:
            cout("                 " + "     " + COLOR_BLUE + COLOR_STYLE_BRIGHT + "Y: " + COLOR_RESET_ALL + "View owned mounts")
        if "North-East" not in blocked_locations:
            cout(
                "Can go North-East ⬈" + "   " + COLOR_BLUE + COLOR_STYLE_BRIGHT +
                "X: " + COLOR_RESET_ALL + "Examine active effects"
            )
        else:
            cout(
                "                   " + "   " + COLOR_BLUE + COLOR_STYLE_BRIGHT +
                "X: " + COLOR_RESET_ALL + "Examine active effects"
            )
        if "North-West" not in blocked_locations:
            cout("Can go North-West ⬉" + "   " + COLOR_BLUE + COLOR_STYLE_BRIGHT + "P: " + COLOR_RESET_ALL + "Pause game")
        else:
            cout("                   " + "   " + COLOR_BLUE + COLOR_STYLE_BRIGHT + "P: " + COLOR_RESET_ALL + "Pause game")
        if "South-East" not in blocked_locations:
            cout(
                "Can go South-East ⬊" + "   " + COLOR_BLUE + COLOR_STYLE_BRIGHT + "K: " + COLOR_RESET_ALL + "Backup player save"
            )
        else:
            cout(
                "                   " + "   " + COLOR_BLUE + COLOR_STYLE_BRIGHT + "K: " + COLOR_RESET_ALL + "Backup player save"
            )
        if "South-West" not in blocked_locations:
            cout("Can go South-West ⬋" + "   " + COLOR_BLUE + COLOR_STYLE_BRIGHT + "Q: " + COLOR_RESET_ALL + "Quit & save game")
        else:
            cout("                   " + "   " + COLOR_BLUE + COLOR_STYLE_BRIGHT + "Q: " + COLOR_RESET_ALL + "Quit & save game")

        text = '='
        text_handling.print_separator(text)

        logger_sys.log_message("INFO: Checking if the start dialog should be displayed to the player")
        # player start dialog
        if not player["start dialog"]["heard start dialog"]:
            start_dialog = player["start dialog"]["dialog"]
            logger_sys.log_message(f"INFO: Displaying start dialog '{start_dialog}' to player")
            dialog_handling.print_dialog(
                start_dialog, dialog, preferences, text_replacements_generic, player, drinks,
                item, enemy, npcs, start_player, lists, zone,
                mission, mounts, start_time, map
            )
            text = '='
            text_handling.print_separator(text)

            player["start dialog"]["heard start dialog"] = True

        global is_in_village, is_in_hostel, is_in_stable, is_in_blacksmith
        global is_in_forge, is_in_church, is_in_castle, is_in_grocery_store
        global is_in_harbor
        is_in_village = False
        is_in_hostel = False
        is_in_stable = False
        is_in_blacksmith = False
        is_in_forge = False
        is_in_church = False
        is_in_castle = False
        is_in_grocery_store = False
        is_in_harbor = False
        logger_sys.log_message("INFO: Checking if player is in a village, hostel, stable, blacksmith or forge")
        if (
            zone[map_zone]["type"] == "village"
            or zone[map_zone]["type"] == "hostel"
            or zone[map_zone]["type"] == "stable"
            or zone[map_zone]["type"] == "blacksmith"
            or zone[map_zone]["type"] == "forge"
            or zone[map_zone]["type"] == "church"
            or zone[map_zone]["type"] == "castle"
            or zone[map_zone]["type"] == "grocery"
            or zone[map_zone]["type"] == "harbor"
        ):
            zone_handling.print_zone_news(zone, map_zone)
        logger_sys.log_message(f"INFO: Checking if a dialog is defined at map point 'point{map_location}'")
        if "dialog" in map["point" + str(map_location)] and map_location not in player["heard dialogs"]:
            current_dialog = map["point" + str(map_location)]["dialog"]
            has_required_attributes = True
            has_required_locations = True
            has_required_enemies = True
            has_required_npcs = True
            if "to display" in dialog[str(current_dialog)]:
                if "player attributes" in dialog[str(current_dialog)]["to display"]:
                    count = 0
                    required_attributes = dialog[str(current_dialog)]["to display"]["player attributes"]
                    required_attributes_len = len(required_attributes)
                    logger_sys.log_message(
                        f"INFO: Checking if player has required attributes '{required_attributes}'" +
                        f" to display dialog '{current_dialog}'"
                    )
                    while count < required_attributes_len and has_required_attributes:
                        selected_attribute = required_attributes[count]
                        if selected_attribute not in player["attributes"]:
                            has_required_attributes = False
                            logger_sys.log_message("INFO: Player doesn't have required attributes to display this dialog")
                        count += 1
                if "visited locations" in dialog[str(current_dialog)]["to display"]:
                    count = 0
                    required_locations = dialog[str(current_dialog)]["to display"]["visited locations"]
                    required_locations_len = len(required_attributes)
                    logger_sys.log_message(
                        f"INFO: Checking if player has required visited locations '{required_locations}'" +
                        f" to display dialog '{current_dialog}'"
                    )
                    while count < required_locations_len and has_required_locations:
                        selected_location = required_locations[count]
                        if selected_location not in player["visited points"]:
                            has_required_locations = False
                            logger_sys.log_message("INFO: Player doesn't have required visited locations to display this dialog")
                        count += 1
                if "known enemies" in dialog[str(current_dialog)]["to display"]:
                    count = 0
                    required_enemies = dialog[str(current_dialog)]["to display"]["known enemies"]
                    required_enemies_len = len(required_enemies)
                    logger_sys.log_message(
                        f"INFO: Checking if player has required known enemies '{required_enemies}'" +
                        f" to display dialog '{current_dialog}'"
                    )
                    while count < required_enemies_len and has_required_enemies:
                        selected_enemy = required_enemies[count]
                        if selected_enemy not in player["enemies list"]:
                            has_required_enemies = False
                            logger_sys.log_message("INFO: Player doesn't have required known enemies to display this dialog")
                        count += 1
                if "known npcs" in dialog[str(current_dialog)]["to display"]:
                    count = 0
                    required_npcs = dialog[str(current_dialog)]["to display"]["known npcs"]
                    required_npcs_len = len(required_npcs)
                    logger_sys.log_message(
                        f"INFO: Checking if player has required known npcs '{required_npcs}'" +
                        f" to display dialog '{current_dialog}'"
                    )
                    while count < required_npcs_len and has_required_npcs:
                        selected_npc = required_npcs[count]
                        if selected_npc not in player["met npcs names"]:
                            has_required_npcs = False
                            logger_sys.log_message("INFO: Player doesn't have required known npcs to display this dialog")
                        count += 1
            if has_required_attributes and has_required_locations and has_required_enemies and has_required_npcs:
                logger_sys.log_message(
                    f"INFO: Player has all required stuff to display dialog '{current_dialog}'" +
                    f" --> displaying it and adding map location '{map_location}' to the player's heard dialogs save list"
                )
                dialog_handling.print_dialog(
                    current_dialog, dialog, preferences, text_replacements_generic, player, drinks,
                    item, enemy, npcs, start_player, lists, zone,
                    mission, mounts, start_time, map
                )
                player["heard dialogs"].append(map_location)
                text = '='
                text_handling.print_separator(text)
            else:
                logger_sys.log_message(
                    f"INFO: Player doesn't have all required stuff to display dialog '{current_dialog}'" +
                    " --> passing"
                )
        logger_sys.log_message("INFO: Checking if the player is in a village")
        if zone[map_zone]["type"] == "village":
            is_in_village = True
        logger_sys.log_message("INFO: Checking if the player is in a forge")
        if zone[map_zone]["type"] == "forge":
            is_in_forge = True
            zone_handling.print_forge_information(map_zone, zone, item)
        logger_sys.log_message("INFO: Checking if the player is in a blacksmith")
        if zone[map_zone]["type"] == "blacksmith":
            is_in_blacksmith = True
            zone_handling.print_blacksmith_information(map_zone, zone, item)
        logger_sys.log_message("INFO: Checking if the player is in a stable")
        if zone[map_zone]["type"] == "stable":
            is_in_stable = True
            zone_handling.print_stable_information(map_zone, zone, mounts, item, player, map_location)
        logger_sys.log_message("INFO: Checking if the player is an hostel")
        if zone[map_zone]["type"] == "hostel":
            is_in_hostel = True
            zone_handling.print_hostel_information(map_zone, zone, item, drinks)
        logger_sys.log_message("INFO: Checking if the player is in a church")
        if zone[map_zone]["type"] == "church":
            is_in_church = True
        logger_sys.log_message("INFO: Checking if the player is in a castle")
        if zone[map_zone]["type"] == "castle":
            is_in_castle = True
        logger_sys.log_message("INFO: Checking if the player is in a grocery store")
        if zone[map_zone]["type"] == "grocery":
            zone_handling.print_grocery_information(map_zone, zone, item, player)
            is_in_grocery_store = True
        logger_sys.log_message("INFO: Checking if the player is in a harbor")
        if zone[map_zone]["type"] == "harbor":
            zone_handling.print_harbor_information(map_zone, zone, map)
            is_in_harbor = True
        cout("")
        logger_sys.log_message(f"INFO: Checking if an item is on the ground at map point 'point{map_location}'")
        if "item" in map["point" + str(map_location)] and map_location not in player["taken items"]:
            map_items = str(map["point" + str(map_location)]["item"])
            logger_sys.log_message(f"INFO: Current map point 'point{map_location}' has item '{map_items}'")
            map_items = map_items.replace('[', '')
            map_items = map_items.replace(']', '')
            map_items = map_items.replace("'", '')
            take_item = "There are these items on the ground: " + map_items
            cout(take_item)
            cout("")
        logger_sys.log_message(f"INFO: Checking if an npc is present at map point 'point{map_location}'")

        # Check if the player can get
        # a mission from current map
        # location

        logger_sys.log_message(f"INFO: Checking if the player can get a mission from current map location '{map_location}'")
        count = 0
        while count < len(list(mission)):
            current_mission_data = mission[list(mission)[count]]
            if int(current_mission_data["source"]) == int(map_location) and str(
                list(mission)[count]
            ) not in player["offered missions"]:
                logger_sys.log_message(f"INFO: Offering mission '{str(list(mission)[count])}' to player")
                mission_handling.offer_mission(
                    str(list(mission)[count]), player, mission, dialog, preferences,
                    text_replacements_generic, drinks, item, enemy, npcs,
                    start_player, lists, zone, mission, mounts, start_time, map
                )

            count += 1

        # Check if the player has a mission that
        # have a stopover at the current map location
        # If he does, at the current map location
        # to the player save to let the program
        # known that
        logger_sys.log_message(
            "INFO: Checking if the player has a mission that has a stopover" +
            f" at the current map location '{map_location}'"
        )

        count = 0
        while count < len(player["active missions"]):
            current_mission_data = mission[str(player["active missions"][count])]
            if "stopovers" in current_mission_data:
                if map_location in current_mission_data["stopovers"]:
                    logger_sys.log_message(
                        f"INFO: Adding current map location '{map_location}' to player" +
                        f" active mission data '{current_mission_data}'"
                    )
                    player["missions"][str(player["active missions"][count])]["stopovers went"].append(map_location)

            count += 1

        # Check if the player has every stopover
        # done for one of his mission to complete
        # If he does, modify the player save to
        # let the program know that
        logger_sys.log_message("INFO: Checking if the player has every stopover done for one of his missions to complete")

        count = 0
        while count < len(player["active missions"]):
            current_mission_data = mission[str(player["active missions"][count])]
            if "stopovers" in current_mission_data:
                if len(
                    player["missions"][str(player["active missions"][count])]["stopovers went"]
                ) == len(current_mission_data["stopovers"]):
                    player["missions"][str(player["active missions"][count])]["went to all stopovers"] = True

            count += 1

        # Check if player has a mission that requires to
        # be at current map location to complete
        logger_sys.log_message(
            "INFO: Checking if the player has a mission that requires " +
            f"to be at current map location '{map_location}' to complete"
        )
        count = 0

        while count < len(player["active missions"]):
            current_mission_data = mission[str(player["active missions"][count])]
            if current_mission_data["destination"] == map_location:
                logger_sys.log_message(f"INFO: Running mission completing checks for mission data '{current_mission_data}'")
                mission_handling.mission_completing_checks(
                    str(player["active missions"][count]), mission, player, dialog, preferences,
                    text_replacements_generic, drinks, item, enemy, npcs, start_player,
                    lists, zone, mission, mounts, start_time
                )

            count += 1

        # Check if player has required attributes to
        # fail a mission. If he does, then
        # remove the mission id from the player's
        # active missions save attribute to let the
        # program know that and run the 'on fail'
        # mission triggers
        logger_sys.log_message("INFO: Checking if a player has all required conditions to fail an active mission")
        count = 0

        while count < len(player["active missions"]):
            current_mission_data = mission[str(player["active missions"][count])]
            if "to fail" in current_mission_data:
                fail = mission_handling.mission_checks(current_mission_data, player, 'to fail')
                if not fail:
                    logger_sys.log_message(f"INFO: Executing failing triggers of mission data '{current_mission_data}'")
                    mission_handling.execute_triggers(
                        current_mission_data, player, 'on fail', dialog, preferences,
                        text_replacements_generic, drinks, item, enemy, npcs,
                        start_player, lists, zone, mission, mounts, start_time, map
                    )
                    cout(
                        COLOR_RED + COLOR_STYLE_BRIGHT + "You failed mission '" +
                        current_mission_data["name"] + "'" + COLOR_RESET_ALL
                    )
                    player["active missions"].remove(str(player["active missions"][count]))

            count += 1

        if "npc" in map["point" + str(map_location)] and map_location not in player["met npcs"]:
            npc_handling.init_npc(map_location, player, npcs, drinks, item, preferences, map)

        # Check if player current missions
        # have an enemy at current map point
        logger_sys.log_message(
            "INFO: Checking if the player has a mission that makes an enemy " +
            f"spawn at current map point 'point{map_location}'"
        )
        count = 0
        count2 = 0

        while count < len(player["active missions"]):
            current_mission_id = player["active missions"][count]
            current_mission_data = mission[player["active missions"][count]]
            if "enemies" in current_mission_data:
                while count2 < len(list(current_mission_data["enemies"])):
                    current_enemy_data = current_mission_data["enemies"][str(list(current_mission_data["enemies"])[count2])]
                    if current_enemy_data["location"] == map_location:
                        spawning_checks = True
                        spawning_checks_2 = False
                        if 'to spawn' in current_enemy_data:
                            spawning_checks = mission_handling.mission_checks(current_enemy_data, player, 'to spawn')
                        if 'to despawn' in current_enemy_data:
                            spawning_checks_2 = mission_handling.mission_checks(current_enemy_data, player, 'to despawn')
                        if spawning_checks and not spawning_checks_2:
                            logger_sys.log_message(
                                f"INFO: Spawning enemy from mission '{current_mission_id}' " +
                                f"with mission enemy data '{current_enemy_data}'"
                            )
                            enemy_handling.spawn_enemy(
                                map_location, lists[str(current_enemy_data["enemy category"])],
                                current_enemy_data["enemy number"], enemy, item, lists, start_player, map, player,
                                preferences, drinks, npcs, zone, mounts, mission, dialog, player_damage_coefficient,
                                text_replacements_generic, start_time, previous_player, save_file,
                                enemies_damage_coefficient
                            )
                            if "dialog" in current_enemy_data:
                                dialog_handling.print_dialog(
                                    current_enemy_data["dialog"], dialog, preferences, text_replacements_generic, player, drinks,
                                    item, enemy, npcs, start_player, lists, zone,
                                    mission, mounts, start_time, map
                                )

                    count2 += 1
            count += 1

        # Calculate enemy spawning change
        # variable, depending on the player
        # difficulty mode.
        #
        # Easy: 8%
        # Normal: 18%
        # Hard: 28%
        if player["difficulty mode"] == 0:
            enemy_spawning_chance = random.uniform(0, 1) > .92
        elif player["difficulty mode"] == 2:
            enemy_spawning_chance = random.uniform(0, 1) > .72
        else:
            enemy_spawning_chance = random.uniform(0, 1) > .82

        logger_sys.log_message(f"INFO: Checking if an enemy at map point 'point{map_location}'")
        if "enemy" in map["point" + str(map_location)] and map_location not in player["defeated enemies"]:
            logger_sys.log_message(f"INFO: Found enemies at map point 'point{map_location}'")
            enemy_handling.spawn_enemy(
                map_location, lists[map["point" + str(map_location)]["enemy type"]],
                map["point" + str(map_location)]["enemy"], enemy, item, lists, start_player, map, player,
                preferences, drinks, npcs, zone, mounts, mission, dialog, player_damage_coefficient,
                text_replacements_generic, start_time, previous_player, save_file,
                enemies_damage_coefficient
            )

        elif (
            day_time == COLOR_RED + COLOR_STYLE_BRIGHT + "☾ NIGHT" + COLOR_RESET_ALL
            and enemy_spawning_chance and zone[map_zone]["type"] != "hostel"
            and zone[map_zone]["type"] != "stable" and zone[map_zone]["type"] != "village"
            and zone[map_zone]["type"] != "blacksmith" and zone[map_zone]["type"] != "forge"
            and zone[map_zone]["type"] != "castle" and zone[map_zone]["type"] != "church"
            and zone[map_zone]["type"] != "grocery" and zone[map_zone]["type"] != "harbor"
        ):
            logger_sys.log_message("INFO: Checking if it's night time")
            logger_sys.log_message(
                "INFO: Checking if the player isn't in a village, an hostel, a stable, a blacksmith or a forge"
            )
            logger_sys.log_message("INFO: Calculating random chance of enemy spawning")
            logger_sys.log_message("INFO: Spawning enemies")
            if "enemy spawning" in list(zone[map_zone]):
                enemy_list_to_spawn = lists[str(zone[map_zone]["enemy spawning"])]
            else:
                enemy_list_to_spawn = lists["generic"]
            enemy_handling.spawn_enemy(
                map_location, enemy_list_to_spawn, round(random.uniform(1, 5)), enemy,
                item, lists, start_player, map, player,
                preferences, drinks, npcs, zone, mounts, mission, dialog, player_damage_coefficient,
                text_replacements_generic, start_time, previous_player, save_file,
                enemies_damage_coefficient
            )

        # Check if the player's in 'Easy' difficulty. If he
        # is, then automatically save the player data into
        # its save file
        if player["difficulty mode"] == 0:
            logger_sys.log_message(
                "INFO: autosaving player data into its save --> player's in 'Easy' difficulty mode"
            )
            logger_sys.log_message("INFO: Dumping player RAM save into its save file")
            dumped = yaml.dump(player)
            previous_player = player
            logger_sys.log_message(f"INFO: Dumping player save data: '{dumped}'")

            save_file_quit = save_file
            with open(save_file_quit, "w") as f:
                f.write(dumped)
                logger_sys.log_message(f"INFO: Dumping player save data to save '{save_file_quit}'")

            save_name_backup = save_file.replace('save_', '~0 save_')

            with open(save_name_backup, "w") as f:
                f.write(dumped)
                logger_sys.log_message(f"INFO: Dumping player save data to backup save '{save_name_backup}'")

            dumped = yaml.dump(preferences)
            logger_sys.log_message(f"INFO: Dumping player preferences data: '{dumped}'")

            with open(program_dir + '/preferences.yaml', 'w') as f:
                f.write(dumped)
            logger_sys.log_message(f"INFO: Dumping player preferences to file '" + program_dir + "/preferences.yaml'")

        command = cinput(COLOR_GREEN + COLOR_STYLE_BRIGHT + "> " + COLOR_RESET_ALL)
        cout(" ")

        logger_sys.log_message(f"INFO: Checking for utilities type items in the item dictionary")
        # Check for utilities keys
        utilities_list = []
        for i in list(item):
            current_item = item[i]
            if current_item["type"] == 'Utility':
                utilities_list.append(i)
        logger_sys.log_message(f"INFO: Found utilities items: '{utilities_list}'")

        # Saving oldest coordinates
        global player_x_old, player_y_old
        player_x_old = player["x"]
        player_y_old = player["y"]

        logger_sys.log_message(f"INFO: Player ran command '{command}'")
        logger_sys.log_message(f"INFO: Checking if a ground item is present at map point 'point{map_location}'")
        continued_command = False
        global pause_time
        pause_time = 0  # required variable
        if "item" in map["point" + str(map_location)] and command in map["point" + str(map_location)]["item"]:
            logger_sys.log_message(f"INFO: Found item '{command}' at map point 'point{map_location}'")
            if command in player["inventory"] and item[command]["type"] == "Utility":
                cout(COLOR_YELLOW + "You cannot take that item." + COLOR_RESET_ALL)
                time.sleep(1.5)
            elif player["inventory slots remaining"] == 0:
                cout(COLOR_YELLOW + "You cannot take that item because you're out of inventory slots." + COLOR_RESET_ALL)
                time.sleep(1.5)
            else:
                logger_sys.log_message(f"INFO: Adding item '{command}' to player inventory")
                logger_sys.log_message(f"INFO: Adding map point 'point{map_location}' to the player save attribute 'taken items'")
                player["inventory"].append(command)
                player["taken items"].append(map_location)

            continued_command = True
        elif command.lower().startswith('go'):
            cout(COLOR_YELLOW + "Rather than saying Go <direction>, simply say <direction>." + COLOR_RESET_ALL)
            time.sleep(1.5)
            continued_command = True
        elif command.lower().startswith('ne'):
            logger_sys.log_message(f"INFO: Checking if player can go north-east from map point 'point{map_location}'")
            next_point = search(player["x"] + 1, player["y"] + 1)
            if "North-East" in map["point" + str(map_location)]["blocked"] or next_point is None:
                cout(COLOR_YELLOW + "You cannot go that way." + COLOR_RESET_ALL)
                logger_sys.log_message(f"INFO: Refusing access to north-east: access blocked to map point 'point{next_point}'")
                time.sleep(1)
            elif "key" in map["point" + str(next_point)]:
                logger_sys.log_message(
                    f"INFO: Checking if a key is required for going north-east at map point 'point{next_point}'"
                )
                check_for_key("north-east")
            else:
                logger_sys.log_message(f"INFO: Moving player north-east to map point 'point{next_point}': successful checks")
                player["y"] += 1
                player["x"] += 1
            continued_command = True
        elif command.lower().startswith('nw'):
            logger_sys.log_message(f"INFO: Checking if player can go north-west from map point 'point{map_location}'")
            next_point = search(player["x"] - 1, player["y"] + 1)
            if "North-West" in map["point" + str(map_location)]["blocked"] or next_point is None:
                cout(COLOR_YELLOW + "You cannot go that way." + COLOR_RESET_ALL)
                logger_sys.log_message(f"INFO: Refusing access to north-west: access blocked to map point 'point{next_point}'")
                time.sleep(1)
            elif "key" in map["point" + str(next_point)]:
                logger_sys.log_message(
                    f"INFO: Checking if a key is required for going north-west at map point 'point{next_point}'"
                )
                check_for_key("north-west")
            else:
                logger_sys.log_message(f"INFO: Moving player north-west to map point 'point{next_point}': successful checks")
                player["y"] += 1
                player["x"] -= 1
            continued_command = True
        elif command.lower().startswith('se'):
            logger_sys.log_message(f"INFO: Checking if player can go south-east from map point 'point{map_location}'")
            next_point = search(player["x"] + 1, player["y"] - 1)
            if "South-East" in map["point" + str(map_location)]["blocked"] or next_point is None:
                cout(COLOR_YELLOW + "You cannot go that way." + COLOR_RESET_ALL)
                logger_sys.log_message(f"INFO: Refusing access to south-east: access blocked to map point 'point{next_point}'")
                time.sleep(1)
            elif "key" in map["point" + str(next_point)]:
                logger_sys.log_message(
                    f"INFO: Checking if a key is required for going south-east at map point 'point{next_point}'"
                )
                check_for_key("south-east")
            else:
                logger_sys.log_message(f"INFO: Moving player south-east to map point 'point{next_point}': successful checks")
                player["y"] -= 1
                player["x"] += 1
            continued_command = True
        elif command.lower().startswith('sw'):
            logger_sys.log_message(f"INFO: Checking if player can go south-west from map point 'point{map_location}'")
            next_point = search(player["x"] - 1, player["y"] - 1)
            if "South-West" in map["point" + str(map_location)]["blocked"] or next_point is None:
                cout(COLOR_YELLOW + "You cannot go that way." + COLOR_RESET_ALL)
                logger_sys.log_message(f"INFO: Refusing access to south-west: access blocked to map point 'point{next_point}'")
                time.sleep(1)
            elif "key" in map["point" + str(next_point)]:
                logger_sys.log_message(
                    f"INFO: Checking if a key is required for going south-west at map point 'point{next_point}'"
                )
                check_for_key("south-west")
            else:
                logger_sys.log_message(f"INFO: Moving player south-west to map point 'point{next_point}': successful checks")
                player["y"] -= 1
                player["x"] -= 1
            continued_command = True
        elif command.lower().startswith('n'):
            logger_sys.log_message(f"INFO: Checking if player can go north from map point 'point{map_location}'")
            next_point = search(player["x"], player["y"] + 1)
            if "North" in map["point" + str(map_location)]["blocked"] or next_point is None:
                cout(COLOR_YELLOW + "You cannot go that way." + COLOR_RESET_ALL)
                logger_sys.log_message(f"INFO: Refusing access to north: access blocked to map point 'point{next_point}'")
                time.sleep(1)
            elif "key" in map["point" + str(next_point)]:
                logger_sys.log_message(f"INFO: Checking if a key is required for going north at map point 'point{next_point}'")
                check_for_key("north")
            else:
                logger_sys.log_message(f"INFO: Moving player north to map point 'point{next_point}': successful checks")
                player["y"] += 1
            continued_command = True
        elif command.lower().startswith('s'):
            logger_sys.log_message(f"INFO: Checking if player can go south from map point 'point{map_location}'")
            next_point = search(player["x"], player["y"] - 1)
            if "South" in map["point" + str(map_location)]["blocked"] or next_point is None:
                cout(COLOR_YELLOW + "You cannot go that way." + COLOR_RESET_ALL)
                logger_sys.log_message(f"INFO: Refusing access to south: access blocked to map point 'point{next_point}'")
                time.sleep(1)
            elif "key" in map["point" + str(next_point)]:
                logger_sys.log_message(f"INFO: Checking if a key is required for going south at map point 'point{next_point}'")
                check_for_key("south")
            else:
                logger_sys.log_message(f"INFO: Moving player south to map point 'point{next_point}': successful checks")
                player["y"] -= 1
            continued_command = True
        elif command.lower().startswith('e'):
            logger_sys.log_message(f"INFO: Checking if player can go east from map point 'point{map_location}'")
            next_point = search(player["x"] + 1, player["y"])
            if "East" in map["point" + str(map_location)]["blocked"] or next_point is None:
                cout(COLOR_YELLOW + "You cannot go that way." + COLOR_RESET_ALL)
                logger_sys.log_message(f"INFO: Refusing access to east: access blocked to map point 'point{next_point}'")
                time.sleep(1)
            elif "key" in map["point" + str(next_point)]:
                logger_sys.log_message(f"INFO: Checking if a key is required for going east at map point 'point{next_point}'")
                check_for_key("east")
            else:
                logger_sys.log_message(f"INFO: Moving player east to map point 'point{next_point}': successful checks")
                player["x"] += 1
            continued_command = True
        elif command.lower().startswith('w'):
            logger_sys.log_message(f"INFO: Checking if player can go west from map point 'point{map_location}'")
            next_point = search(player["x"] - 1, player["y"])
            if "West" in map["point" + str(map_location)]["blocked"] or next_point is None:
                cout(COLOR_YELLOW + "You cannot go that way." + COLOR_RESET_ALL)
                logger_sys.log_message(f"INFO: Refusing access to west: access blocked to map point 'point{next_point}'")
                time.sleep(1)
            elif "key" in map["point" + str(next_point)]:
                logger_sys.log_message(f"INFO: Checking if a key is required for going west at map point 'point{next_point}'")
                check_for_key("west")
            else:
                logger_sys.log_message(f"INFO: Moving player west to map point 'point{next_point}': successful checks")
                player["x"] -= 1
            continued_command = True
        elif command.lower().startswith('d'):
            text = '='
            text_handling.print_separator(text)
            logger_sys.log_message("INFO: Displaying player diary menu")
            cout("ADVENTURER NAME: " + str(preferences["latest preset"]["save"]))
            cout(
                "ELAPSED DAYS: " + COLOR_STYLE_BRIGHT + COLOR_MAGENTA +
                str(round(player["elapsed time game days"], 1)) + COLOR_RESET_ALL
            )
            cout(
                "WALKED MILES: " + COLOR_STYLE_BRIGHT + COLOR_BACK_BLUE +
                str(player["walked miles"]) + COLOR_RESET_ALL
            )
            text = '='
            text_handling.print_separator(text)
            options = ['Visited Places', 'Encountered Monsters', 'Encountered People', 'Tasks']
            choice = terminal_handling.show_menu(options)
            logger_sys.log_message(f"INFO: Playing has chosen option '{choice}'")
            if choice == 'Visited Places':
                cout("VISITED PLACES: ")
                zones_list = str(player["visited zones"])
                logger_sys.log_message(f"INFO: Printing player visited places '{zones_list}'")
                zones_list = zones_list.replace("'", '')
                zones_list = zones_list.replace("[", ' -')
                zones_list = zones_list.replace("]", '')
                zones_list = zones_list.replace(", ", '\n -')
                cout(zones_list)
                text = '='
                text_handling.print_separator(text)
                which_zone = cinput(COLOR_GREEN + COLOR_STYLE_BRIGHT + "> " + COLOR_RESET_ALL)
                logger_sys.log_message(f"INFO: Player has chosen zone '{which_zone}' to check")
                if which_zone in player["visited zones"]:
                    logger_sys.log_message(f"INFO: Printing zone '{which_zone}' information to GUI")
                    text = '='
                    text_handling.print_separator(text)
                    text_handling.print_zone_map_alone(which_zone, zone)
                    distance = str(
                        zone_handling.get_map_point_distance_from_player(
                            map, player,
                            zone_handling.get_zone_nearest_point(map, player, which_zone)
                        )
                    )
                    cout("NAME: " + zone[which_zone]["name"])
                    cout(
                        "DISTANCE " + COLOR_BACK_BLUE + distance + " miles" + COLOR_RESET_ALL
                    )
                    if zone[which_zone]["type"] == "village":
                        village_point = zone_handling.get_zone_nearest_point(map, player, which_zone)
                        village_x = map[village_point]["x"]
                        village_y = map[village_point]["y"]
                        village_coordinates = (
                            "(" + COLOR_GREEN + COLOR_STYLE_BRIGHT + str(village_x) +
                            COLOR_RESET_ALL + ", " + COLOR_GREEN + COLOR_STYLE_BRIGHT +
                            str(village_y) + COLOR_RESET_ALL + ")"
                        )
                        cout("LOCATION: " + village_coordinates)
                        content_hostels = str(zone[which_zone]["content"]["hostels"])
                        content_hostels = content_hostels.replace('[', '')
                        content_hostels = content_hostels.replace(']', '')
                        content_hostels = content_hostels.replace("'", '')
                        text = "HOSTELS: " + content_hostels
                        text_handling.print_long_string(text)
                        content_blacksmiths = str(zone[which_zone]["content"]["blacksmiths"])
                        content_blacksmiths = content_blacksmiths.replace('[', '')
                        content_blacksmiths = content_blacksmiths.replace(']', '')
                        content_blacksmiths = content_blacksmiths.replace("'", '')
                        text = "BLACKSMITHS: " + content_blacksmiths
                        text_handling.print_long_string(text)
                        content_forges = str(zone[which_zone]["content"]["forges"])
                        content_forges = content_forges.replace('[', '')
                        content_forges = content_forges.replace(']', '')
                        content_forges = content_forges.replace("'", '')
                        text = "FORGES: " + content_forges
                        text_handling.print_long_string(text)
                        content_stables = str(zone[which_zone]["content"]["stables"])
                        content_stables = content_stables.replace('[', '')
                        content_stables = content_stables.replace(']', '')
                        content_stables = content_stables.replace("'", '')
                        text = "STABLES: " + content_stables
                        text_handling.print_long_string(text)
                        content_churches = str(zone[which_zone]["content"]["churches"])
                        content_churches = content_churches.replace('[', '')
                        content_churches = content_churches.replace(']', '')
                        content_churches = content_churches.replace("'", '')
                        text = "CHURCHES: " + content_churches
                        text_handling.print_long_string(text)
                        content_groceries = str(zone[which_zone]["content"]["groceries"])
                        content_groceries = content_groceries.replace('[', '')
                        content_groceries = content_groceries.replace(']', '')
                        content_groceries = content_groceries.replace("'", '')
                        text = "GROCERIES: " + content_groceries
                        text_handling.print_long_string(text)
                        current_harbors = str(zone[which_zone]["content"]["harbors"])
                        current_harbors = current_harbors.replace('[', '')
                        current_harbors = current_harbors.replace(']', '')
                        current_harbors = current_harbors.replace("'", '')
                        text = "HARBORS: " + current_harbors
                        text_handling.print_long_string(text)
                    elif zone[which_zone]["type"] == "hostel":
                        current_hostel = zone[which_zone]
                        hostel_point = zone_handling.get_zone_nearest_point(map, player, which_zone)
                        hostel_x = map[hostel_point]["x"]
                        hostel_y = map[hostel_point]["y"]
                        hostel_coordinates = (
                            "(" + COLOR_GREEN + COLOR_STYLE_BRIGHT + str(hostel_x) +
                            COLOR_RESET_ALL + ", " + COLOR_GREEN + COLOR_STYLE_BRIGHT +
                            str(hostel_y) + COLOR_RESET_ALL + ")"
                        )
                        cout("LOCATION: " + hostel_coordinates)
                        cout(
                            "SLEEP COST: " + COLOR_YELLOW + COLOR_STYLE_BRIGHT +
                            str(current_hostel["sleep gold"]) + COLOR_RESET_ALL
                        )
                        if "None" not in current_hostel["sells"]["drinks"]:
                            cout("DRINKS SALES:")
                            count = 0
                            hostel_drinks = current_hostel["sells"]["drinks"]
                            hostel_drinks_len = len(hostel_drinks)
                            while count < hostel_drinks_len:
                                current_drink = str(current_hostel["sells"]["drinks"][int(count)])
                                cout(
                                    " -" + current_hostel["sells"]["drinks"][int(count)] + " " +
                                    COLOR_YELLOW + COLOR_STYLE_BRIGHT +
                                    str(round(drinks[current_drink]["gold"] * current_hostel["cost value"], 2)) +
                                    COLOR_RESET_ALL
                                )
                                count += 1
                        if "None" not in current_hostel["sells"]["items"]:
                            cout("ITEMS SALES")
                            count = 0
                            hostel_items = current_hostel["sells"]["items"]
                            hostel_items_len = len(hostel_items)
                            while count < hostel_items_len:
                                current_item = str(current_hostel["sells"]["items"][int(count)])
                                cout(
                                    " -" + current_hostel["sells"]["items"][int(count)] + " " +
                                    COLOR_YELLOW + COLOR_STYLE_BRIGHT +
                                    str(round(item[current_item]["gold"] * current_hostel["cost value"], 2)) +
                                    COLOR_RESET_ALL
                                )
                                count += 1
                        if "None" not in current_hostel["buys"]["items"]:
                            cout("ITEMS RESALES:")
                            count = 0
                            hostel_items = current_hostel["buys"]["items"]
                            hostel_items_len = len(hostel_items)
                            while count < hostel_items_len:
                                current_item = str(current_hostel["buys"]["items"][int(count)])
                                cout(
                                    " -" + current_hostel["buys"]["items"][int(count)] + " " +
                                    COLOR_YELLOW + COLOR_STYLE_BRIGHT +
                                    str(round(item[current_item]["gold"] * current_hostel["cost value"], 2)) +
                                    COLOR_RESET_ALL
                                )
                                count += 1
                    elif zone[which_zone]["type"] == "stable":
                        current_stable = zone[which_zone]
                        stable_point = zone_handling.get_zone_nearest_point(map, player, which_zone)
                        stable_x = map[stable_point]["x"]
                        stable_y = map[stable_point]["y"]
                        stable_coordinates = (
                            "(" + COLOR_GREEN + COLOR_STYLE_BRIGHT + str(stable_x) +
                            COLOR_RESET_ALL + ", " + COLOR_GREEN + COLOR_STYLE_BRIGHT +
                            str(stable_y) + COLOR_RESET_ALL + ")"
                        )
                        cout("LOCATION: " + stable_coordinates)
                        cout(
                            "DEPOSIT COST/DAY: " + COLOR_YELLOW + COLOR_STYLE_BRIGHT +
                            str(current_stable["deposit gold"]) + COLOR_RESET_ALL
                        )
                        cout(
                            "TRAINING COST/DAY: " + COLOR_YELLOW + COLOR_STYLE_BRIGHT +
                            str(current_stable["training gold"]) + COLOR_RESET_ALL
                        )
                        options = ['Train Mount', '']
                        if "None" not in current_stable["stable"]["sells"]["mounts"]:
                            cout("MOUNTS SALES:")
                            count = 0
                            stable_mounts = current_stable["stable"]["sells"]["mounts"]
                            stable_mounts_len = len(stable_mounts)
                            while count < stable_mounts_len:
                                current_mount = str(current_stable["stable"]["sells"]["mounts"][int(count)])
                                cout(
                                    " -" + current_stable["stable"]["sells"]["mounts"][int(count)] + " " +
                                    COLOR_YELLOW + COLOR_STYLE_BRIGHT +
                                    str(round(mounts[current_mount]["gold"] * current_stable["cost value"], 2)) +
                                    COLOR_RESET_ALL
                                )
                                count += 1
                        if "None" not in current_stable["stable"]["sells"]["items"]:
                            options += ['Buy Item']
                            cout("ITEMS SALES:")
                            count = 0
                            stable_items = current_stable["stable"]["sells"]["items"]
                            stable_items_len = len(stable_items)
                            while count < stable_items_len:
                                current_mount = str(current_stable["stable"]["sells"]["items"][int(count)])
                                cout(
                                    " -" + current_stable["stable"]["sells"]["items"][int(count)] + " " +
                                    COLOR_YELLOW + COLOR_STYLE_BRIGHT +
                                    str(round(item[current_mount]["gold"] * current_stable["cost value"], 2)) +
                                    COLOR_RESET_ALL
                                )
                                count += 1
                        deposited_mounts_num = 0
                        count = 0
                        mounts_list_len = len(player["mounts"])
                        deposited_mounts_names = []
                        if "None" not in list(player["mounts"]):
                            while count < mounts_list_len:
                                selected_mount = list(player["mounts"])[count]
                                selected_mount = str(selected_mount)
                                if (
                                    player["mounts"][selected_mount]["location"] == "point" +
                                    str(map_location) and player["mounts"][selected_mount]["is deposited"]
                                ):
                                    deposited_mounts_num += 1
                                    deposited_mounts_names += [str(player["mounts"][selected_mount]["name"])]
                                count += 1
                        else:
                            deposited_mounts_names = 0
                            deposited_mounts_num = 0
                        deposited_mounts_names = str(deposited_mounts_names)
                        deposited_mounts_names = deposited_mounts_names.replace('[', '(')
                        deposited_mounts_names = deposited_mounts_names.replace(']', COLOR_RESET_ALL + ')')
                        deposited_mounts_names = deposited_mounts_names.replace("'", COLOR_GREEN + COLOR_STYLE_BRIGHT)
                        deposited_mounts_names = deposited_mounts_names.replace(',', COLOR_RESET_ALL + ',')
                        if deposited_mounts_num == 0:
                            cout(
                                "MOUNTS DEPOSITED HERE: " + COLOR_BLUE + COLOR_STYLE_BRIGHT +
                                str(deposited_mounts_num) + COLOR_RESET_ALL
                            )
                        else:
                            cout(
                                "MOUNTS DEPOSITED HERE: " + COLOR_BLUE + COLOR_STYLE_BRIGHT +
                                str(deposited_mounts_num) + COLOR_RESET_ALL + " " + deposited_mounts_names
                            )
                    elif zone[which_zone]["type"] == "blacksmith":
                        current_black_smith = zone[which_zone]
                        blacksmith_point = zone_handling.get_zone_nearest_point(map, player, which_zone)
                        blacksmith_x = map[blacksmith_point]["x"]
                        blacksmith_y = map[blacksmith_point]["y"]
                        black_smith_coordinates = (
                            "(" + COLOR_GREEN + COLOR_STYLE_BRIGHT + str(blacksmith_x) +
                            COLOR_RESET_ALL + ", " + COLOR_GREEN + COLOR_STYLE_BRIGHT +
                            str(blacksmith_y) + COLOR_RESET_ALL + ")"
                        )
                        cout("LOCATION: " + black_smith_coordinates)
                        if "None" not in current_black_smith["blacksmith"]["buys"]:
                            cout("EQUIPMENT RESALES:")
                            count = 0
                            weapon_buys = current_black_smith["blacksmith"]["buys"]
                            weapon_buys_len = len(weapon_buys)
                            while count < weapon_buys_len:
                                current_weapon = str(current_black_smith["blacksmith"]["buys"][int(count)])
                                cout(
                                    " -" + current_weapon + " " + COLOR_YELLOW + COLOR_STYLE_BRIGHT +
                                    str(round(item[current_weapon]["gold"] * current_black_smith["cost value"], 2)) +
                                    COLOR_RESET_ALL
                                )
                                count += 1
                        if "None" not in current_black_smith["blacksmith"]["orders"]:
                            cout("WEAPON ORDERS:")
                            count = 0
                            weapon_orders = current_black_smith["blacksmith"]["orders"]
                            weapon_orders_len = len(weapon_orders)
                            while count < weapon_orders_len:
                                current_weapon = str(list(current_black_smith["blacksmith"]["orders"])[int(count)])
                                global_current_weapon_materials = (
                                    weapon_upgrade_handling.detect_weapon_next_upgrade_items(current_weapon, item)
                                )
                                cout(
                                    " -" + current_weapon + " " + COLOR_YELLOW + COLOR_STYLE_BRIGHT +
                                    str(round(item[current_weapon]["gold"] * current_black_smith["cost value"], 2)) +
                                    COLOR_RESET_ALL + COLOR_GREEN + COLOR_STYLE_BRIGHT + " (" +
                                    COLOR_RESET_ALL + global_current_weapon_materials +
                                    COLOR_GREEN + COLOR_STYLE_BRIGHT + ")" + COLOR_RESET_ALL
                                )
                                count += 1
                    elif zone[which_zone]["type"] == "church":
                        church_point = zone_handling.get_zone_nearest_point(map, player, which_zone)
                        church_x = map[church_point]["x"]
                        church_y = map[church_point]["y"]
                        church_coordinates = (
                            "(" + COLOR_GREEN + COLOR_STYLE_BRIGHT + str(church_x) +
                            COLOR_RESET_ALL + ", " + COLOR_GREEN + COLOR_STYLE_BRIGHT +
                            str(church_y) + COLOR_RESET_ALL + ")"
                        )
                        cout("LOCATION: " + church_coordinates)
                    elif zone[which_zone]["type"] == "grocery":
                        grocery_point = zone_handling.get_zone_nearest_point(map, player, which_zone)
                        grocery_x = map[grocery_point]["x"]
                        grocery_y = map[grocery_point]["y"]
                        grocery_coordinates = (
                            "(" + COLOR_GREEN + COLOR_STYLE_BRIGHT + str(grocery_x) +
                            COLOR_RESET_ALL + ", " + COLOR_GREEN + COLOR_STYLE_BRIGHT +
                            str(grocery_y) + COLOR_RESET_ALL + ")"
                        )
                        cout("LOCATION: " + grocery_coordinates)
                        sold_items_list = player["groceries data"][which_zone]["items sales"]
                        sold_items = []
                        for i in sold_items_list:
                            sold_items += [
                                f" -{i} {COLOR_YELLOW}{round(zone[which_zone]["cost value"] * item[i]["gold"], 2)}" +
                                f"{COLOR_RESET_ALL}"
                            ]
                        cout("SOLD ITEMS:")
                        for i in sold_items:
                            cout(i)
                    elif zone[which_zone]["type"] == "harbor":
                        current_harbor = zone[which_zone]
                        harbor_point = zone_handling.get_zone_nearest_point(map, player, which_zone)
                        harbor_x = map[harbor_point]["x"]
                        harbor_y = map[harbor_point]["y"]
                        harbor_coordinates = (
                            "(" + COLOR_GREEN + COLOR_STYLE_BRIGHT + str(harbor_x) +
                            COLOR_RESET_ALL + ", " + COLOR_GREEN + COLOR_STYLE_BRIGHT +
                            str(harbor_y) + COLOR_RESET_ALL + ")"
                        )
                        cout("LOCATION: " + harbor_coordinates)
                        cout("TRAVELS:")
                        travels = []
                        count = 0
                        for travel in current_harbor["travels"]:
                            destination = map[f"point{current_harbor["travels"][travel]["destination"]}"]
                            destination = (
                                f"({COLOR_GREEN}{destination["x"]} {COLOR_RESET_ALL}," +
                                f"{COLOR_GREEN}{destination["y"]}{COLOR_RESET_ALL})"
                            )
                            travels += [
                                f" -{list(current_harbor["travels"])[count]} {destination}" +
                                f" {COLOR_YELLOW}{round(current_harbor["travels"][travel]["cost"], 2)}{COLOR_RESET_ALL}"
                            ]
                            count += 1
                        for travel in travels:
                            cout(travel)
                    elif zone[which_zone]["type"] == "forge":
                        current_forge = zone[which_zone]
                        forge_point = zone_handling.get_zone_nearest_point(map, player, which_zone)
                        forge_x = map[forge_point]["x"]
                        forge_y = map[forge_point]["y"]
                        forge_coordinates = (
                            "(" + COLOR_GREEN + COLOR_STYLE_BRIGHT + str(forge_x) +
                            COLOR_RESET_ALL + ", " + COLOR_GREEN + COLOR_STYLE_BRIGHT +
                            str(forge_y) + COLOR_RESET_ALL + ")"
                        )
                        cout("LOCATION: " + forge_coordinates)
                        if "None" not in current_forge["forge"]["buys"]:
                            cout("METAL RESALES:")
                            count = 0
                            metal_buys = current_forge["forge"]["buys"]
                            metal_buys_len = len(metal_buys)
                            while count < metal_buys_len:
                                current_metal = str(metal_buys[count])
                                cout(
                                    " -" + current_metal + " " + COLOR_YELLOW + COLOR_STYLE_BRIGHT +
                                    str(round(item[current_metal]["gold"] * current_forge["cost value"], 2)) +
                                    COLOR_RESET_ALL
                                )
                                count += 1
                        if "None" not in current_forge["forge"]["sells"]:
                            cout("METAL SALES:")
                            count = 0
                            metal_sells = current_forge["forge"]["sells"]
                            metal_sells_len = len(metal_sells)
                            while count < metal_sells_len:
                                current_metal = str(metal_sells[count])
                                cout(
                                    " -" + current_metal + " " + COLOR_YELLOW + COLOR_STYLE_BRIGHT +
                                    str(round(item[current_metal]["gold"] * current_forge["cost value"], 2)) +
                                    COLOR_RESET_ALL
                                )
                                count += 1
                    text = "DESCRIPTION: " + zone[which_zone]["description"]
                    text_handling.print_long_string(text)
                    text = '='
                    text_handling.print_separator(text)
                else:
                    cout(" ")
                    cout(COLOR_YELLOW + "You don't know about that place" + COLOR_RESET_ALL)
                    logger_sys.log_message(f"INFO: Player has chosen '{which_zone}', which he doesn't know about --> canceling")
                cinput()
            elif choice == 'Encountered Monsters':
                cout("ENCOUNTERED MONSTERS: ")
                enemies_list = str(player["enemies list"])
                logger_sys.log_message(f"INFO: Printing player known enemies: '{enemies_list}'")
                enemies_list = enemies_list.replace("'None', ", '')
                enemies_list = enemies_list.replace("'", '')
                enemies_list = enemies_list.replace("[", ' -')
                enemies_list = enemies_list.replace("]", '')
                enemies_list = enemies_list.replace(", ", '\n -')
                cout(enemies_list)
                text = '='
                text_handling.print_separator(text)
                which_enemy = cinput(COLOR_GREEN + COLOR_STYLE_BRIGHT + "> " + COLOR_RESET_ALL)
                logger_sys.log_message(f"INFO: Player has chosen enemy '{which_enemy}' to display information")
                if which_enemy == "None":
                    cout(" ")
                    cout(COLOR_YELLOW + "You don't know about that enemy." + COLOR_RESET_ALL)
                    time.sleep(1.5)
                elif which_enemy in player["enemies list"]:
                    logger_sys.log_message(f"INFO: Printing enemy '{which_enemy}' information")

                    text = '='
                    text_handling.print_separator(text)

                    text_handling.print_enemy_thumbnail(which_enemy, preferences)
                    cout(" ")

                    cout("NAME: " + which_enemy)

                    cout("PLURAL: " + enemy[which_enemy]["plural"])
                    enemy_average_damage = (
                        enemy[which_enemy]["damage"]["min damage"] * enemies_damage_coefficient +
                        enemy[which_enemy]["damage"]["max damage"] * enemies_damage_coefficient
                    ) / 2
                    enemy_average_health = (
                        enemy[which_enemy]["health"]["min spawning health"] + enemy[which_enemy]["health"]["max spawning health"]
                    ) / 2
                    cout(
                        "AVERAGE DAMAGE: " + COLOR_STYLE_BRIGHT + COLOR_CYAN + str(round(enemy_average_damage, 1)) +
                        COLOR_RESET_ALL
                    )
                    cout(
                        "AVERAGE HEALTH: " + COLOR_STYLE_BRIGHT + COLOR_RED + str(round(enemy_average_health, 1)) +
                        COLOR_RESET_ALL
                    )
                    cout(
                        "AGILITY: " + COLOR_STYLE_BRIGHT + COLOR_MAGENTA +
                        str(round(enemy[which_enemy]["agility"], 2)) + COLOR_RESET_ALL
                    )

                    # risk
                    risk = [0, 1, 2, 3, 4, 5, 6, 7, 8]
                    total = 0
                    for i in range(8):  # generate accurate risk
                        risk[i] = battle.calculate_player_risk(
                            player, item, 1, enemy[which_enemy], enemy,
                            player_damage_coefficient, enemies_damage_coefficient
                        )
                    for i in range(8):
                        total += risk[i]
                    risk = round(total / 8)
                    bars = 10
                    remaining_risk_symbol = "█"
                    lost_risk_symbol = "_"

                    remaining_risk_bars = round(risk / 100 * bars)
                    lost_risk_bars = bars - remaining_risk_bars

                    # print HP stats and possible actions for the player

                    if risk > .80 * 100:
                        health_color = COLOR_RED
                    elif risk > .60 * 100:
                        health_color = COLOR_ORANGE_4
                    elif risk > .45 * 100:
                        health_color = COLOR_YELLOW
                    elif risk > .30 * 100:
                        health_color = COLOR_GREEN
                    else:
                        health_color = COLOR_STYLE_BRIGHT + COLOR_GREEN

                    cout(f"RISK AGAINST ONE: {risk}%")
                    cout(
                        f"|{health_color}{remaining_risk_bars * remaining_risk_symbol}" +
                        f"{lost_risk_bars * lost_risk_symbol}{COLOR_RESET_ALL}|"
                    )

                    # drops
                    enemy_drops = str(enemy[which_enemy]["inventory"])
                    enemy_drops = enemy_drops.replace('[', '')
                    enemy_drops = enemy_drops.replace(']', '')
                    enemy_drops = enemy_drops.replace("'", '')
                    text = "DROPS: " + str(enemy_drops)
                    text_handling.print_long_string(text)

                    text = "DESCRIPTION: " + enemy[which_enemy]["description"]
                    text_handling.print_long_string(text)
                    text = '='
                    text_handling.print_separator(text)
                    cinput()
                else:
                    logger_sys.log_message(f"INFO: Player doesn't know about enemy '{which_enemy}' --> canceling")
                    cout(" ")
                    cout(COLOR_YELLOW + "You don't know about that enemy." + COLOR_RESET_ALL)
                    time.sleep(1.5)
            elif choice == 'Encountered People':
                cout("ENCOUNTERED PEOPLE: ")
                enemies_list = str(player["met npcs names"])
                logger_sys.log_message(f"INFO: Printing player encounter people: '{enemies_list}'")
                enemies_list = enemies_list.replace("'None', ", '')
                enemies_list = enemies_list.replace("'", '')
                enemies_list = enemies_list.replace("[", ' -')
                enemies_list = enemies_list.replace("]", '')
                enemies_list = enemies_list.replace(", ", '\n -')
                cout(enemies_list)
                text = '='
                text_handling.print_separator(text)
                which_npc = cinput(COLOR_GREEN + COLOR_STYLE_BRIGHT + "> " + COLOR_RESET_ALL)
                logger_sys.log_message(f"INFO: Player has chosen npc '{which_npc}' to display information about")
                if which_npc == "None":
                    cout(" ")
                    cout(COLOR_YELLOW + "You don't know about that people." + COLOR_RESET_ALL)
                    time.sleep(1.5)
                elif which_npc in player["met npcs names"]:
                    logger_sys.log_message(f"INFO: Printing npc '{which_npc}' information")

                    text = '='
                    text_handling.print_separator(text)

                    text_handling.print_npc_thumbnail(which_npc, preferences)
                    cout(" ")

                    cout("NAME: " + which_npc)

                    cout(
                        "COST VALUE: " + COLOR_YELLOW + COLOR_STYLE_BRIGHT +
                        str(npcs[which_npc]["cost value"]) + COLOR_RESET_ALL
                    )
                    sells_list_drinks = str(npcs[which_npc]["sells"]["drinks"])
                    sells_list_items = str(npcs[which_npc]["sells"]["items"])
                    buys_list = str(npcs[which_npc]["buys"]["items"])
                    sells_list_drinks = sells_list_drinks.replace("'None', ", '')
                    sells_list_drinks = sells_list_drinks.replace("'", '')
                    sells_list_drinks = sells_list_drinks.replace("[", '')
                    sells_list_drinks = sells_list_drinks.replace("]", '')
                    sells_list_items = sells_list_items.replace("'None', ", '')
                    sells_list_items = sells_list_items.replace("'", '')
                    sells_list_items = sells_list_items.replace("[", '')
                    sells_list_items = sells_list_items.replace("]", '')
                    buys_list = buys_list.replace("'None', ", '')
                    buys_list = buys_list.replace("'", '')
                    buys_list = buys_list.replace("[", '')
                    buys_list = buys_list.replace("]", '')
                    cout(" ")
                    cout("SELLS:")
                    text = "DRINKS: " + sells_list_drinks
                    text_handling.print_long_string(text)
                    text = "ITEMS: " + sells_list_items
                    text_handling.print_long_string(text)
                    cout(" ")
                    cout("BUYS:")
                    text = "ITEMS: " + buys_list
                    text_handling.print_long_string(text)

                    text = "DESCRIPTION: " + npcs[which_npc]["description"]
                    text_handling.print_long_string(text)
                    text = '='
                    text_handling.print_separator(text)
                    cinput()
                else:
                    cout(" ")
                    cout(COLOR_YELLOW + "You don't know about that enemy." + COLOR_RESET_ALL)
                    logger_sys.log_message(f"INFO: Player doesn't know about npc '{which_npc}' --> canceling")
                    time.sleep(1.5)
            elif choice == 'Tasks':
                cout("ACTIVE TASKS:")
                tasks_list = player["active missions"]
                if tasks_list is None:
                    tasks_list = ["You have no tasks"]
                logger_sys.log_message(f"INFO: Printing player active missions: '{tasks_list}'")

                if tasks_list != ["You have no tasks"]:
                    count = 0
                    while count < len(tasks_list):
                        current_task = tasks_list[count]
                        current_task_name = mission[str(current_task)]["name"]
                        tasks_list.remove(current_task)
                        if not mission[current_task]["invisible"]:
                            tasks_list.append(current_task_name)

                        count += 1

                tasks_list_str = str(tasks_list)
                tasks_list_str = tasks_list_str.replace("'None', ", '')
                tasks_list_str = tasks_list_str.replace("'", '')
                tasks_list_str = tasks_list_str.replace("[", ' -')
                tasks_list_str = tasks_list_str.replace("]", '')
                tasks_list_str = tasks_list_str.replace(", ", '\n -')

                cout(tasks_list_str)
                text = '='
                text_handling.print_separator(text)
                which_task = cinput(COLOR_GREEN + COLOR_STYLE_BRIGHT + "> " + COLOR_RESET_ALL)
                logger_sys.log_message(f"INFO: Player has chosen task '{which_task}' to display information about")
                if which_task in tasks_list:
                    logger_sys.log_message(f"INFO: Printing mission '{which_task}' information")

                    mission_id = mission_handling.get_mission_id_from_name(which_task, mission)

                    text = '='
                    text_handling.print_separator(text)
                    cout("NAME: " + mission[mission_id]["name"])
                    cout("DESCRIPTION:")
                    mission_handling.print_description(mission[mission_id], map)

                    destination_point = map["point" + str(mission[mission_id]["destination"])]
                    destination = str(
                        "X:" + COLOR_GREEN + COLOR_STYLE_BRIGHT + str(destination_point["x"]) +
                        COLOR_RESET_ALL + ", Y:" + COLOR_GREEN + COLOR_STYLE_BRIGHT +
                        str(destination_point["y"]) + COLOR_RESET_ALL
                    )

                    cout("")
                    cout("DESTINATION: " + destination)
                    if 'stopovers' in list(mission[mission_id]):
                        mission_stopovers = mission[mission_id]["stopovers"]
                        new_mission_stopovers = []
                        count = 0
                        while count < len(mission_stopovers):
                            current_map_point_data = map["point" + str(mission_stopovers[count])]
                            current_map_point_coordinates = "[X:" + str(
                                current_map_point_data["x"]
                            ) + ",Y:" + str(current_map_point_data["y"]) + "]"
                            new_mission_stopovers.append(current_map_point_coordinates)

                            count += 1
                        new_mission_stopovers = str(new_mission_stopovers)
                        cout("STOPOVERS: " + new_mission_stopovers)

                    text = '='
                    text_handling.print_separator(text)
                    options = ['Abort', 'Exit']
                    choice = terminal_handling.show_menu(options)
                    if choice == 'Abort':
                        wait = cinput("Are you sure you want to abort this mission? (y/n) ")
                        if wait.startswith('y'):
                            player["active missions"].remove(mission[mission_id]["name"])
                else:
                    cout("")
                    cout(COLOR_YELLOW + "You do not currently have a mission named like that" + COLOR_RESET_ALL)
                    logger_sys.log_message(f"INFO: Player doesn't know about mission '{which_task}' --> canceling")
                    time.sleep(1.5)
            continued_command = True
        elif command.lower().startswith('i'):
            text = '='
            text_handling.print_separator(text)
            logger_sys.log_message(f"INFO: Printing player armor protection, agility and critical hit chance stats")
            cout(
                "ARMOR PROTECTION: " + COLOR_GREEN + COLOR_STYLE_BRIGHT +
                str(round(player["armor protection"], 2)) + COLOR_RESET_ALL + COLOR_RED +
                COLOR_STYLE_BRIGHT + " (" + COLOR_RESET_ALL +
                "More it's higher, the less you'll take damages in fights" + COLOR_RED +
                COLOR_STYLE_BRIGHT + ")" + COLOR_RESET_ALL
            )
            cout(
                "AGILITY: " + COLOR_MAGENTA + COLOR_STYLE_BRIGHT + str(round(player["agility"], 2)) +
                COLOR_RESET_ALL + COLOR_RED + COLOR_STYLE_BRIGHT +
                " (" + COLOR_RESET_ALL + "More it's higher, the more you'll have a chance to dodge attacks" +
                COLOR_RED + COLOR_STYLE_BRIGHT + ")" + COLOR_RESET_ALL
            )
            if player["held item"] != " ":
                cout(
                    "CRITICAL HIT CHANCE: " + COLOR_CYAN + COLOR_STYLE_BRIGHT +
                    str(round(player["critical hit chance"] * 100, 2)) + "%" + COLOR_RESET_ALL +
                    COLOR_RED + COLOR_STYLE_BRIGHT + " (" + COLOR_RESET_ALL +
                    "More it's higher, the more you'll have a chance to deal critical attacks" +
                    COLOR_RED + COLOR_STYLE_BRIGHT + ")" + COLOR_RESET_ALL
                )
            cout(" ")
            logger_sys.log_message("INFO: Printing player equipped items")
            # equipment
            if player["held item"] != " ":
                cout("HELD WEAPON: " + COLOR_RED + COLOR_STYLE_BRIGHT + player["held item"] + COLOR_RESET_ALL)
            if player["held chestplate"] != " ":
                cout("WORN CHESTPLATE: " + COLOR_RED + COLOR_STYLE_BRIGHT + player["held chestplate"] + COLOR_RESET_ALL)
            if player["held leggings"] != " ":
                cout("WORN LEGGINGS: " + COLOR_RED + COLOR_STYLE_BRIGHT + player["held leggings"] + COLOR_RESET_ALL)
            if player["held boots"] != " ":
                cout("WORN BOOTS: " + COLOR_RED + COLOR_STYLE_BRIGHT + player["held boots"] + COLOR_RESET_ALL)
            if player["held shield"] != " ":
                cout("HELD SHIELD: " + COLOR_RED + COLOR_STYLE_BRIGHT + player["held shield"] + COLOR_RESET_ALL)
            logger_sys.log_message(f"INFO: Printing player inventory")
            player_inventory_displayed = []
            count = 0
            for i in player["inventory"]:
                zeros = len(str(len(player["inventory"])))
                removed = len(str(count))
                player_inventory_displayed += [f"{"0" * (zeros - removed)}{count}> {i}"]
                count += 1
            text = '='
            text_handling.print_separator(text)
            cout("INVENTORY:")
            for line in player_inventory_displayed:
                cout(line)
            text = '='
            text_handling.print_separator(text)
            which_item = cinput(COLOR_GREEN + COLOR_STYLE_BRIGHT + "$ " + COLOR_RESET_ALL)
            error = False
            try:
                which_item_index = int(which_item)
                which_item = player["inventory"][which_item_index]
            except Exception as e:
                error = True
            if not error:
                logger_sys.log_message(f"INFO: Player has chosen item '{which_item}' to display information about")
                text = '='
                text_handling.print_separator(text)
                logger_sys.log_message(f"INFO: Printing item '{which_item}' information")
                cout("")
                text_handling.print_item_thumbnail(item[which_item]["thumbnail"])
                text = '='
                text_handling.print_separator(text)
                if item[which_item]["type"] == "Weapon":
                    cout("NAME: " + item[which_item]["display name"])
                else:
                    cout("NAME: " + which_item)
                cout("TYPE: " + item[which_item]["type"])
                text = "DESCRIPTION: " + item[which_item]["description"]
                text_handling.print_long_string(text)
                if (
                    item[which_item]["type"] == "Armor Piece: Chestplate"
                    or item[which_item]["type"] == "Armor Piece: Boots"
                    or item[which_item]["type"] == "Armor Piece: Leggings"
                    or item[which_item]["type"] == "Armor Piece: Shield"
                ):
                    text = (
                        "             Armor pieces can protect you in fights, more " +
                        "the armor protection is higher, the more it protects you.")
                    text_handling.print_long_string(text)
                    item_next_upgrade = weapon_upgrade_handling.detect_weapon_next_upgrade_items(which_item, item)
                    cout(
                        "UPGRADE TIER: " + COLOR_GREEN + COLOR_STYLE_BRIGHT +
                        str(item[which_item]["upgrade tier"]) + COLOR_RESET_ALL + "/" +
                        str(weapon_upgrade_handling.check_weapon_max_upgrade(str(which_item), item))
                    )
                    cout("ITEMS FOR NEXT UPGRADE:\n" + str(item_next_upgrade))
                    cout(
                        "ARMOR PROTECTION: " + COLOR_GREEN + COLOR_STYLE_BRIGHT +
                        str(round(item[which_item]["armor protection"], 2)) + COLOR_RESET_ALL
                    )
                if item[which_item]["type"] == "Metal":
                    text = (
                        "              Metals are items that you buy in village " +
                        "forges that you often use to order weapons in blacksmith."
                    )
                if item[which_item]["type"] == "Primary Material":
                    text = (
                        "              Primary materials are items that you " +
                        "can find naturally but that you can also buy from many villages shops."
                    )
                    text_handling.print_long_string(text)
                if item[which_item]["type"] == "Weapon":
                    item_next_upgrade = weapon_upgrade_handling.detect_weapon_next_upgrade_items(which_item, item)
                    cout(
                        "UPGRADE TIER: " + COLOR_GREEN + COLOR_STYLE_BRIGHT +
                        str(item[which_item]["upgrade tier"]) + COLOR_RESET_ALL + "/" +
                        str(weapon_upgrade_handling.check_weapon_max_upgrade(str(which_item), item))
                    )
                    cout("ITEMS FOR NEXT UPGRADE:\n" + str(item_next_upgrade))
                    cout("DAMAGE: " + COLOR_CYAN + COLOR_STYLE_BRIGHT + str(item[which_item]["damage"]) + COLOR_RESET_ALL)
                    cout("DEFENSE: " + COLOR_CYAN + COLOR_STYLE_BRIGHT + str(item[which_item]["defend"]) + COLOR_RESET_ALL)
                    cout(
                        "CRITICAL HIT CHANCE: " + COLOR_MAGENTA + COLOR_STYLE_BRIGHT +
                        str(round(item[which_item]["critical hit chance"] * 100, 2)) + "%" + COLOR_RESET_ALL
                    )
                if item[which_item]["type"] == "Food":
                    cout(
                        "HEALTH BONUS: " + COLOR_STYLE_BRIGHT + COLOR_YELLOW +
                        str(item[which_item]["max bonus"]) + COLOR_RESET_ALL
                    )
                    healing_level = str(item[which_item]["healing level"])
                    if healing_level == '999':
                        healing_level = 'MAX HEALTH'
                    cout(
                        "HEALING: " + COLOR_STYLE_BRIGHT + COLOR_MAGENTA +
                        healing_level + COLOR_RESET_ALL
                    )
                if item[which_item]["type"] == "Consumable":
                    cout("")
                    cout("EFFECTS:")
                    logger_sys.log_message(f"INFO: Getting consumable '{which_item}' effects")
                    if item[which_item]["effects"] is not None:
                        count = 0
                        for effect in item[which_item]["effects"]:
                            current_effect_data = item[which_item]["effects"][count]
                            current_effect_type = current_effect_data["type"]
                            if current_effect_type not in INVISIBLE_EFFECTS:
                                cout(" -Effect " + str(count + 1) + ": {")
                                consumable_handling.print_consumable_effects(current_effect_type, current_effect_data)
                                cout("}")

                            count += 1
                    else:
                        cout(" -None")
                text = '='
                text_handling.print_separator(text)
                if str(
                    item[which_item]["type"]
                ) == 'Armor Piece: Chestplate' or str(
                    item[which_item]["type"]
                ) == 'Weapon' or str(
                    item[which_item]["type"]
                ) == 'Armor Piece: Leggings' or str(
                    item[which_item]["type"]
                ) == 'Armor Piece: Boots' or str(
                    item[which_item]["type"]
                ) == 'Armor Piece: Shield':
                    options = ['Equip', 'Get Rid', 'Exit']
                elif str(item[which_item]["type"]) == 'Consumable' or str(item[which_item]["type"]) == 'Food':
                    options = ['Consume', 'Get Rid', 'Exit']
                elif str(item[which_item]["type"]) == 'Map':
                    options = ['Examine Map', 'Get Rid', 'Exit']
                else:
                    options = ['Get Rid', 'Exit']
                choice = terminal_handling.show_menu(options)
                logger_sys.log_message(f"INFO: Player has chosen option '{choice}'")
                if choice == 'Equip':
                    item_handling.equip_item(which_item, player, item[which_item]["type"])
                elif choice == 'Consume':
                    consumable_handling.consume_consumable(
                        item, which_item, player,
                        dialog, preferences, text_replacements_generic,
                        lists, map_location, enemy, item, drinks,
                        start_player, npcs, zone,
                        mounts, mission, player_damage_coefficient, previous_player,
                        save_file, map, start_time, enemies_damage_coefficient
                    )
                elif choice == 'Examine Map':
                    if preferences["latest preset"]["type"] == "plugin":
                        plugin = preferences["latest preset"]["plugin"]
                    else:
                        plugin = False
                    cout("")
                    cout("╔" + ("═" * 53) + "╗")
                    text_handling.print_map_art(item[which_item], plugin_name=plugin)
                    cout("╚" + ("═" * 53) + "╝")
                    cinput()
                elif choice == 'Get Rid':
                    text = (
                        "You won't be able to get this item back if you " +
                        "throw it away. Are you sure you want to throw away this item"
                    )
                    text_handling.print_long_string(text)
                    ask = cinput("? (y/n) ")
                    if ask.lower().startswith('y'):
                        logger_sys.log_message(f"INFO: Getting rid of item '{which_item}'")
                        if item[which_item]["type"] == "Bag":
                            if (player["inventory slots remaining"] - item[which_item]["inventory slots"]) < 0:
                                text = (
                                    COLOR_YELLOW +
                                    "You cannot throw that item because it would " +
                                    "cause your remaining inventory slots to be negative" + COLOR_RESET_ALL
                                )
                                text_handling.print_long_string(text)
                                time.sleep(1.5)
                                cout(" ")
                        else:
                            del player["inventory"][which_item_index]
                            which_item_number_inventory = 0
                            count = 0
                            p = True
                            while p:
                                if count >= len(player["inventory"]) + 1:
                                    p = False
                                else:
                                    selected_item = player["inventory"][count - 1]
                                    if str(selected_item) == str(which_item):
                                        which_item_number_inventory += 1
                                count += 1
                            if which_item_number_inventory <= 1:
                                if which_item == player["held item"]:
                                    player["held item"] = " "
                                if which_item == player["held chestplate"]:
                                    player["held chestplate"] = " "
                                if which_item == player["held boots"]:
                                    player["held boots"] = " "
                                if which_item == player["held leggings"]:
                                    player["held leggings"] = " "
                                if which_item == player["held shield"]:
                                    player["held shield"] = " "
            else:
                logger_sys.log_message(f"INFO: Canceling item action --> player haven't entered valid input")
                cout(COLOR_YELLOW + "You do not have that item." + COLOR_RESET_ALL)
                time.sleep(1.5)
            continued_command = True
        elif command.lower().startswith('z'):
            logger_sys.log_message(f"INFO: Trying to interact with current zone '{map_zone}'")
            if zone[map_zone]["type"] == "hostel":
                zone_handling.interaction_hostel(
                    map_zone, zone, player, drinks, item, save_file, preferences, previous_player
                )
            elif zone[map_zone]["type"] == "stable":
                zone_handling.interaction_stable(
                    map_zone, zone, player, item, drinks, mounts, map_location, preferences, time_elapsing_coefficient
                )
            elif zone[map_zone]["type"] == "blacksmith":
                zone_handling.interaction_blacksmith(map_zone, zone, item, player)
            elif zone[map_zone]["type"] == "forge":
                zone_handling.interaction_forge(map_zone, zone, player, item)
            elif zone[map_zone]["type"] == "church":
                zone_handling.interaction_church(map_zone, zone, player, save_file, preferences, previous_player)
            elif zone[map_zone]["type"] == "grocery":
                zone_handling.interaction_grocery(map_zone, zone, player, item)
            elif zone[map_zone]["type"] == "harbor":
                zone_handling.interaction_harbor(map_zone, zone, map, player)
            else:
                logger_sys.log_message(f"INFO: Map zone '{map_zone}' cannot have interactions")
                text = (
                    "You cannot find any near hostel, stable, blacksmith, forge, church, grocery store, harbor or castle."
                )
                cout(COLOR_YELLOW, end="")
                text_handling.print_long_string(text)
                cout(COLOR_RESET_ALL, end="")
                time.sleep(1.5)
            continued_command = True
        elif command.lower().startswith('y'):
            if "mounts" in player and player["mounts"] != '':
                logger_sys.log_message("INFO: Printing player currently ridden mount")
                text = '='
                text_handling.print_separator(text)
                if "current mount" in player:
                    current_mount_uuid = str(player["current mount"])
                    if current_mount_uuid != ' ':
                        cout(
                            "RIDDED MOUNT: " + COLOR_GREEN + COLOR_STYLE_BRIGHT +
                            player["mounts"][current_mount_uuid]["name"] + COLOR_RESET_ALL +
                            " (" + player["mounts"][current_mount_uuid]["mount"] + ")"
                        )
                    else:
                        cout("RIDDED MOUNT: " + COLOR_RED + COLOR_STYLE_BRIGHT + "NONE" + COLOR_RESET_ALL)
                mounts_names_list = []
                count = 0
                if "None" not in list(player["mounts"]):
                    mounts_list_len = len(player["mounts"])
                    while count < mounts_list_len:
                        selected_mount = list(player["mounts"])[count]
                        selected_mount = str(selected_mount)
                        mounts_names_list.append(str(player["mounts"][selected_mount]["name"]))
                        count += 1
                    mounts_names_list_str = str(mounts_names_list)
                    logger_sys.log_message(f"INFO: Printing player mounts list: '{mounts_names_list}'")
                    mounts_names_list_str = mounts_names_list_str.replace("'", '')
                    mounts_names_list_str = mounts_names_list_str.replace("[", ' -')
                    mounts_names_list_str = mounts_names_list_str.replace("]", '')
                    mounts_names_list_str = mounts_names_list_str.replace(", ", '\n -')
                else:
                    mounts_names_list_str = "NONE"
                cout(" ")
                cout("OWNED MOUNTS:")
                cout(mounts_names_list_str)
                text = '='
                text_handling.print_separator(text)
                which_mount = cinput(COLOR_GREEN + COLOR_STYLE_BRIGHT + "> " + COLOR_RESET_ALL)
                logger_sys.log_message(f"INFO: Player has chosen option '{which_mount}' to examine")
                if which_mount in mounts_names_list:
                    text = '='
                    text_handling.print_separator(text)

                    # get what uuid is related to the mount name entered
                    mounts_list_len = len(player["mounts"])
                    count = 0
                    while count < mounts_list_len:
                        selected_mount = list(player["mounts"])[count]
                        selected_mount = str(selected_mount)
                        if str(player["mounts"][selected_mount]["name"]) == which_mount:
                            which_mount_data = player["mounts"][selected_mount]
                        count += 1

                    logger_sys.log_message(f"INFO: Printing player mount '{which_mount}' data: '{which_mount_data}'")
                    text_handling.print_enemy_thumbnail(str(mounts[which_mount_data["mount"]]["name"]), preferences)
                    cout(" ")

                    cout("GIVEN NAME: " + which_mount_data["name"])
                    cout("MOUNT: " + mounts[which_mount_data["mount"]]["name"])
                    cout("PLURAL: " + mounts[which_mount_data["mount"]]["plural"])
                    cout(" ")

                    which_mount_location = (
                        "(" + COLOR_GREEN + COLOR_STYLE_BRIGHT +
                        str(map[which_mount_data["location"]]["x"]) + COLOR_RESET_ALL +
                        ", " + COLOR_GREEN + COLOR_STYLE_BRIGHT +
                        str(map[which_mount_data["location"]]["y"]) + COLOR_RESET_ALL + ")"
                    )
                    cout("LOCATION: " + which_mount_location)
                    if which_mount_data["is deposited"]:
                        cout("STABLE: " + str(map[which_mount_data["location"]]["map zone"]))
                        deposited_day = time_handling.date_prettifier(
                            time_handling.addition_to_date(
                                player["starting date"], int(which_mount_data["deposited day"])
                            )
                        )
                        cout(
                            "DEPOSITED DAY: " + COLOR_MAGENTA + COLOR_STYLE_BRIGHT +
                            str(deposited_day) + COLOR_RESET_ALL
                        )
                    cout(" ")

                    cout("STATS:")
                    cout(
                        "  LEVEL: " + COLOR_GREEN + COLOR_STYLE_BRIGHT +
                        str(int(round(which_mount_data["level"], 0))) + COLOR_RESET_ALL +
                        "/" + str(int(round(mounts[str(which_mount_data["mount"])]["levels"]["max level"])))
                    )
                    cout(
                        "  AGILITY ADDITION: " + COLOR_MAGENTA + COLOR_STYLE_BRIGHT +
                        str(which_mount_data["stats"]["agility addition"]) + COLOR_RESET_ALL
                    )
                    cout(
                        "  RESISTANCE ADDITION: " + COLOR_CYAN + COLOR_STYLE_BRIGHT +
                        str(which_mount_data["stats"]["resistance addition"]) + COLOR_RESET_ALL
                    )
                    cout(
                        "  MPH: " + COLOR_BACK_BLUE + COLOR_STYLE_BRIGHT +
                        str(round(which_mount_data["mph"], 1)) + COLOR_RESET_ALL
                    )
                    cout(" ")

                    # get player possible feeding items
                    current_mount_feeds = mounts[which_mount_data["mount"]]["feed"]["food"]
                    player_feeding_items_text = str(current_mount_feeds)
                    player_feeding_items_text = player_feeding_items_text.replace("'", '')
                    player_feeding_items_text = player_feeding_items_text.replace("[", ' -')
                    player_feeding_items_text = player_feeding_items_text.replace("]", '')
                    player_feeding_items_text = player_feeding_items_text.replace(", ", '\n -')
                    cout("FEEDING ITEMS:")
                    cout(player_feeding_items_text)
                    cout(
                        "FEEDING NEEDS: " + COLOR_YELLOW + COLOR_STYLE_BRIGHT +
                        str(mounts[which_mount_data["mount"]]["feed"]["feed needs"]) + COLOR_RESET_ALL
                    )
                    cout("")

                    text = "DESCRIPTION: " + mounts[which_mount_data["mount"]]["description"]
                    text_handling.print_long_string(text)

                    text = '='
                    text_handling.print_separator(text)
                    options = ['Abandon', 'Rename', 'Exit']
                    choice = terminal_handling.show_menu(options)
                    logger_sys.log_message(f"INFO: Player has chosen option '{choice}'")
                    count = 0
                    continue_action = True
                    while count < len(list(player["mounts"])) and continue_action:
                        selected_mount_uuid = str(list(player["mounts"])[count])
                        if player["mounts"][selected_mount_uuid]["name"] == str(which_mount):
                            mount_uuid = selected_mount_uuid
                            continue_action = False
                        count += 1
                    if choice == 'Abandon':
                        cout("Are you sure you want to abandon this mount? You won't")
                        ask = cinput(" be able to find him after that. (y/n) ")
                        if ask.lower().startswith('y'):
                            logger_sys.log_message(f"INFO: Player is abandoning mount '{which_mount}'")
                            player["mounts"].pop(mount_uuid)
                            player["current mount"] = " "
                    elif choice == 'Rename':
                        cout("Select a new name for your mount")
                        new_name = cinput(COLOR_GREEN + COLOR_STYLE_BRIGHT + "> " + COLOR_RESET_ALL)
                        logger_sys.log_message(f"INFO: Player has chosen as a new name for mount '{which_mount}' '{new_name}'")
                        if new_name in mounts_names_list:
                            logger_sys.log_message("INFO: Canceling mount renaming process --> already has a mount name like hat")
                            cout(COLOR_YELLOW + "You already have a mount named like that." + COLOR_RESET_ALL)
                            time.sleep(1.5)
                        else:
                            player["mounts"][mount_uuid]["name"] = str(new_name)
                else:
                    logger_sys.log_message(
                        f"INFO: Canceling mount examining process --> " +
                        f"doesn't own any mount named '{which_mount}'"
                    )
                    cout(COLOR_YELLOW + "You don't have any mounts named like that." + COLOR_RESET_ALL)
                    time.sleep(1.5)
            else:
                logger_sys.log_message(f"INFO: Canceling mount examining process --> player doesn't own any mounts")
                cout(COLOR_YELLOW + "It seems you don't own any mounts." + COLOR_RESET_ALL)
                time.sleep(1.5)
            continued_command = True
        elif command.lower().startswith('x'):
            # First, we create the effects list of
            # dictionaries, and filter the invisible
            # effects type. Then, with that effects
            # database, it's printed to the main UI
            # with UI formatting.
            global active_effects
            active_effects = []
            for effect in player["active effects"]:
                effect = player["active effects"][effect]
                if effect["type"] not in INVISIBLE_EFFECTS:
                    active_effects += [effect]

            text_handling.print_separator('=')
            cout("ACTIVE EFFECTS:")

            if active_effects != []:
                count = 1
                for effect in active_effects:
                    cout(f" -Effect {count}:" + " {")
                    consumable_handling.print_active_effect_info(effect, player)
                    cout("}")

                    count += 1
            else:
                cout(" -None")

            text_handling.print_separator('=')
            cinput()
            continued_command = True
        elif command.lower().startswith('k'):
            if player["difficulty mode"] == 2:
                text = (
                    "You can't save the game this way in the 'Hard' difficulty mode." +
                    " You can only save the game when sleeping at an hostel or resting at a church."
                )
                cout(COLOR_YELLOW, end="")
                text_handling.print_long_string(text)
                cout(COLOR_RESET_ALL, end="")
                time.sleep(4)
            else:
                logger_sys.log_message("INFO: Dumping player RAM save into its save file")
                cout("Collecting player data...")
                dumped = yaml.dump(player)
                previous_player = player
                logger_sys.log_message(f"INFO: Dumping player save data: '{dumped}'")

                save_file_quit = save_file
                cout("Dumping player data to save files...")
                with open(save_file_quit, "w") as f:
                    f.write(dumped)
                    logger_sys.log_message(f"INFO: Dumping player save data to save '{save_file_quit}'")

                save_name_backup = save_file.replace('save_', '~0 save_')

                with open(save_name_backup, "w") as f:
                    f.write(dumped)
                    logger_sys.log_message(f"INFO: Dumping player save data to backup save '{save_name_backup}'")

                cout("Collecting player preferences...")
                dumped = yaml.dump(preferences)
                logger_sys.log_message(f"INFO: Dumping player preferences data: '{dumped}'")

                cout("Dumping player preferences to preferences file...")
                with open(program_dir + '/preferences.yaml', 'w') as f:
                    f.write(dumped)
                logger_sys.log_message(f"INFO: Dumping player preferences to file '" + program_dir + "/preferences.yaml'")
            continued_command = True
        elif command.lower().startswith('p'):
            logger_sys.log_message("INFO: Pausing game")
            cout("Press enter to unpause game...")
            pause_start = time.time()
            cinput()
            pause_end = time.time()
            pause_time = pause_end - pause_start
            logger_sys.log_message(f"INFO: Finished pausing game --> game pause have lasted {pause_time} seconds")
            continued_command = True
        elif command.lower().startswith('q'):
            continue_quit = True
            if player["difficulty mode"] == 2:
                cout("Are you sure you want to quit the game?")
                choice = cinput("Changes that haven't been saved will be lost forever! (y/n) ")
                text = (
                    "\nHint: in 'Hard' difficulty mode, you can save the game by " +
                    "sleeping in an hostel or resting at a church"
                )
                text_handling.print_long_string(text)
                time.sleep(4)
                if not choice.lower().startswith('y'):
                    continue_quit = False
            if continue_quit:
                logger_sys.log_message("INFO: Closing & Saving game")
                text_handling.print_separator('=')
                play = 0
            continued_command = True
        elif command.lower().startswith('$player$data$'):
            logger_sys.log_message("INFO: Displaying player data in a pager mode")
            choice = terminal_handling.show_menu(['Check', 'Edit'], length=12)
            player_data = str(yaml.dump(player))
            if choice == 'Check':
                to_display = player_data
                text_handling.clear_prompt()
                pydoc.pager(to_display)
            else:
                temporary_dir = tempfile.mkdtemp()
                temporary_file = temporary_dir + '/$player$data$.temp.yml'

                # Create a file with the dumped
                # player data in it, then open
                # it with a text editor
                with open(temporary_file, 'w') as f:
                    f.write(player_data)
                data_handling.open_file(temporary_file)

                # Get the file data and write it into
                # the 'player' dictionary variable
                with open(temporary_file, 'r') as f:
                    error_loading = False
                    try:
                        player = yaml.safe_load(f)
                    except Exception as error:
                        error_loading = True
                    previous_player = player
                    if type(player) is not type({}) and not error_loading:
                        error_loading = True
                        error = 'not a yaml file'
                    if error_loading:
                        cout(
                            COLOR_RED + "FATAL ERROR: " + COLOR_STYLE_BRIGHT +
                            "Save corrupted! Check logs files for further information" + COLOR_RESET_ALL
                        )
                        logger_sys.log_message(f"FATAL ERROR: Save '{save_file}' corrupted!")
                        logger_sys.log_message(
                            f"DEBUG: This could have been the result of closing the game at bad moments or " +
                            "a game bug. Please report the bug on the github repo: " +
                            "https://github.com/Dungeons-of-Kathallion/Bane-Of-Wargs/issues/new/choose"
                        )
                        logger_sys.log_message(f"DEBUG: error '{error}'")
                        time.sleep(5)
                        text_handling.exit_game()
            continued_command = True
        elif command.lower().startswith('$game$data$'):
            choices = [
                'map', 'item', 'drinks', 'enemy',
                'npcs', 'start_player', 'lists',
                'zone', 'dialog', 'mission', 'mounts'
            ]
            choice = terminal_handling.show_menu(choices, length=20)
            if choice == 'map':
                data = str(yaml.dump(map))
            elif choice == 'item':
                data = str(yaml.dump(item))
            elif choice == 'drinks':
                data = str(yaml.dump(drinks))
            elif choice == 'enemy':
                data = str(yaml.dump(enemy))
            elif choice == 'npcs':
                data = str(yaml.dump(npcs))
            elif choice == 'start_player':
                data = str(yaml.dump(start_player))
            elif choice == 'lists':
                data = str(yaml.dump(lists))
            elif choice == 'zone':
                data = str(yaml.dump(zone))
            elif choice == 'dialog':
                data = str(yaml.dump(dialog))
            elif choice == 'mission':
                data = str(yaml.dump(mission))
            else:
                data = str(yaml.dump(mounts))

            text_handling.clear_prompt()
            pydoc.pager(data)

            continued_command = True
        elif command.lower().startswith('$spawn$enemy$'):
            cout("Select an enemy to spawn")
            enemy_to_spawn = terminal_handling.show_menu(list(enemy))
            cout("How many enemies you want to be spawned?")
            number_of_enemies = int(terminal_handling.show_menu(['1', '2', '3', '4', '6', '8', '12'], length=7))
            enemy_handling.spawn_enemy(
                map_location, [enemy_to_spawn],
                number_of_enemies, enemy, item, lists, start_player, map, player,
                preferences, drinks, npcs, zone, mounts, mission, dialog, player_damage_coefficient,
                text_replacements_generic, start_time, previous_player, save_file,
                enemies_damage_coefficient
            )
            continued_command = True
        elif command.lower().startswith('$teleport$zone$'):
            cout("Select a map zone to spawn to")
            choice = terminal_handling.show_menu(list(zone))
            teleportation_point = zone_handling.get_zone_nearest_point(map, player, choice)
            player["x"] = map[teleportation_point]["x"]
            player["y"] = map[teleportation_point]["y"]
            continued_command = True
        else:
            continued_utility = False
            for current_utility in utilities_list:
                continued_command = True
                command_valid = command.lower().startswith(item[current_utility]["key"].lower())
                if command_valid and current_utility in player["inventory"]:
                    plugin = preferences["latest preset"]["type"] == "plugin"
                    script_handling.load_script(
                        item[current_utility], preferences, player, map, item, drinks, enemy, npcs,
                        start_player, lists, zone, dialog, mission, mounts, start_time,
                        text_replacements_generic, plugin
                    )
                    continued_utility = True
                    cinput()
                elif current_utility not in player["inventory"] and command_valid:
                    continued_utility = True
                    logger_sys.log_message(f"INFO: Canceling utility script --> doesn't have '{current_utility}' item")
                    cout(f"You do not have a '{current_utility}'.")
                    cout(" ")
                    cinput()
            if not continued_utility:
                logger_sys.log_message(f"INFO: chosen command '{command}' is not a valid command")
                cout("'" + command + "' is not a valid command")
                time.sleep(2)
                cout(" ")

        if not continued_command:
            logger_sys.log_message(f"INFO: chosen command '{command}' is not a valid command")
            cout("'" + command + "' is not a valid command")
            time.sleep(2)
            cout(" ")

        # Checking if the player has traveled, if
        # yes, run a traveling wait
        if (
            player["x"] != player_x_old or
            player["y"] != player_y_old
        ):
            time_handling.traveling_wait(traveling_coefficient)
            player["walked miles"] += 1

        # get end time
        end_time = time.time()
        logger_sys.log_message(f"INFO: Getting end time: '{end_time}'")

        # calculate elapsed time
        elapsed_time = end_time - start_time - pause_time
        logger_sys.log_message(f"INFO: Getting elapsed time: '{elapsed_time}'")

        game_elapsed_time = time_handling.return_game_day_from_seconds(elapsed_time, time_elapsing_coefficient)
        game_elapsed_time = game_elapsed_time
        logger_sys.log_message(f"INFO: Getting elapsed time in game days: '{game_elapsed_time}'")

        player["elapsed time seconds"] += elapsed_time
        player["elapsed time game days"] += game_elapsed_time


if play == 1:
    play = run(1)

# finish up and save
if player["difficulty mode"] != 2:
    dumped = yaml.dump(player)
    logger_sys.log_message(f"INFO: Dumping player save data: '{dumped}'")

    save_file_quit = save_file
    with open(save_file_quit, "w") as f:
        f.write(dumped)
        logger_sys.log_message(f"INFO: Dumping player save data to save '{save_file_quit}'")

    save_name_backup = save_file.replace('save_', '~0 save_')

    with open(save_name_backup, "w") as f:
        f.write(dumped)
        logger_sys.log_message(f"INFO: Dumping player save data to backup save '{save_name_backup}'")

    dumped = yaml.dump(preferences)
    logger_sys.log_message(f"INFO: Dumping player preferences data: '{dumped}'")

    with open(program_dir + '/preferences.yaml', 'w') as f:
        f.write(dumped)
    logger_sys.log_message(f"INFO: Dumping player preferences to file '" + program_dir + "/preferences.yaml'")

text_handling.clear_prompt()
logger_sys.log_message(f"INFO: GAME RUN END")
