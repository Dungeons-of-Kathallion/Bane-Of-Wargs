import random
import yaml
import battle
import check_yaml
import train
import map_item
import term_menu
import os
import sys
import time
import fade
import subprocess
import git
import readline
import traceback
import appdirs
import shutil
import fsspec
import logger_sys
from git import Repo
from colorama import Fore, Back, Style, deinit, init
from colors import *
from sys import exit

# initialize colorama
init()

os.system('clear')

# says you are not playing.
play = 0

fought_enemy = False

separator = COLOR_STYLE_BRIGHT + "###############################" + COLOR_RESET_ALL

def print_title():
    if preferences["theme"] == "OFF":
        with open(program_dir + '/game/imgs/Title' + str(preferences["title style"]) + '.txt', 'r') as f:
            print(f.read())
    else:
        if preferences["theme"] == "blackwhite":
            with open(program_dir + '/game/imgs/Title' + str(preferences["title style"]) + '.txt', 'r') as f:
                faded_text = fade.blackwhite(f.read())
                print(faded_text)
        elif preferences["theme"] == "purplepink":
            with open(program_dir + '/game/imgs/Title' + str(preferences["title style"]) + '.txt', 'r') as f:
                faded_text = fade.purplepink(f.read())
                print(faded_text)
        elif preferences["theme"] == "greenblue":
            with open(program_dir + '/game/imgs/Title' + str(preferences["title style"]) + '.txt', 'r') as f:
                faded_text = fade.greenblue(f.read())
                print(faded_text)
        elif preferences["theme"] == "water":
            with open(program_dir + '/game/imgs/Title' + str(preferences["title style"]) + '.txt', 'r') as f:
                faded_text = fade.water(f.read())
                print(faded_text)
        elif preferences["theme"] == "fire":
            with open(program_dir + '/game/imgs/Title' + str(preferences["title style"]) + '.txt', 'r') as f:
                faded_text = fade.fire(f.read())
                print(faded_text)
        elif preferences["theme"] == "pinkred":
            with open(program_dir + '/game/imgs/Title' + str(preferences["title style"]) + '.txt', 'r') as f:
                faded_text = fade.pinkred(f.read())
                print(faded_text)
        elif preferences["theme"] == "purpleblue":
            with open(program_dir + '/game/imgs/Title' + str(preferences["title style"]) + '.txt', 'r') as f:
                faded_text = fade.purpleblue(f.read())
                print(faded_text)
        elif preferences["theme"] == "brazil":
            with open(program_dir + '/game/imgs/Title' + str(preferences["title style"]) + '.txt', 'r') as f:
                faded_text = fade.brazil(f.read())
                print(faded_text)
        elif preferences["theme"] == "random":
            with open(program_dir + '/game/imgs/Title' + str(preferences["title style"]) + '.txt', 'r') as f:
                faded_text = fade.random(f.read())
                print(faded_text)

def print_speech_text_effect(text):
    text = str(text) + "\n"
    new_input = ""
    for i, letter in enumerate(text):
        if i % 54 == 0:
            new_input += '\n'
        new_input += letter
    if preferences["speed up"] == False:
        for character in new_input:
            sys.stdout.write(character)
            sys.stdout.flush()
            time.sleep(round(random.uniform(.05, .1), 2))
    else:
        for character in new_input:
            sys.stdout.write(character)
            sys.stdout.flush()
            time.sleep(.02)


def exit_game():
    time.sleep(1.5)
    print(COLOR_YELLOW + "Warning: closing game now" + COLOR_RESET_ALL)
    logger_sys.log_message("Warning: closing game now")
    time.sleep(.5)
    os.system('clear')
    exit(1)

menu = True

# Check if player has the config folder if
# not, create it with all its required content
program_dir = str(appdirs.user_config_dir(appname='Bane-Of-Wargs'))
if os.path.exists(program_dir) == False:
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
        "auto update": False
    }
    default_config_data = yaml.dump(default_config_data)
    with open(program_dir + '/preferences.yaml', 'w') as f:
        f.write(default_config_data)
    # Create the plugins, saves, game data folder in the config file
    os.mkdir(program_dir + "/plugins")
    os.mkdir(program_dir + "/saves")
    os.mkdir(program_dir + "/game")
    os.mkdir(program_dir + "/logs")

# Download game data from github master branch
# and install them (auto-update)
logger_sys.log_message("INFO: Downloading game data to update it")
print("Download game data...")
print("This may take a few seconds, sorry for the waiting.")
print("0/3", end="\r")

logger_sys.log_message("INFO: Downloading game yaml schemas files from github")
# Download yaml schema files
try:
    destination = program_dir + '/game/schemas'
    fs = fsspec.filesystem("github", org="Dungeons-Of-Kathallion", repo="Bane-Of-Wargs")
    fs.get(fs.ls("schemas/"), destination)
except Exception as error:
    print(COLOR_YELLOW + COLOR_STYLE_BRIGHT + "WARNING:" + COLOR_RESET_ALL + " an error occurred when trying to download game data to '" + destination + "'.")
    logger_sys.log_message(f"WARNING: An error occurred when downloading game data to '{destination}'.")
    logger_sys.log_message("DEBUG: " + str(error))
    print(COLOR_YELLOW + str(error) + COLOR_RESET_ALL)
    time.sleep(.5)

print("1/3", end="\r")

logger_sys.log_message("INFO: Downloading game data files from github")
# Download data files
try:
    destination = program_dir + '/game/data'
    fs = fsspec.filesystem("github", org="Dungeons-Of-Kathallion", repo="Bane-Of-Wargs")
    fs.get(fs.ls("data/"), destination)
except Exception as error:
    print(COLOR_YELLOW + COLOR_STYLE_BRIGHT + "WARNING:" + COLOR_RESET_ALL + " an error occurred when trying to download game data to '" + destination + "'.")
    logger_sys.log_message(f"WARNING: An error occurred when downloading game data to '{destination}'.")
    logger_sys.log_message("DEBUG: " + str(error))
    print(COLOR_YELLOW + str(error) + COLOR_RESET_ALL)
    time.sleep(.5)

print("2/3", end="\r")

logger_sys.log_message("INFO: Downloading game images .txt files from github")
# Download images .txt files
try:
    destination = program_dir + '/game/imgs'
    fs = fsspec.filesystem("github", org="Dungeons-Of-Kathallion", repo="Bane-Of-Wargs")
    fs.get(fs.ls("imgs/"), destination)
except Exception as error:
    print(COLOR_YELLOW + COLOR_STYLE_BRIGHT + "WARNING:" + COLOR_RESET_ALL + " an error occurred when trying to download game data to '" + destination + "'.")
    logger_sys.log_message(f"WARNING: An error occurred when downloading game data to '{destination}'.")
    logger_sys.log_message("DEBUG: " + str(error))
    print(COLOR_YELLOW + str(error) + COLOR_RESET_ALL)
    time.sleep(.5)

print("3/3")
print("Done")
logger_sys.log_message("INFO: Process of downloading game data to update it completed")

# main menu start
while menu:
    # Get player preferences
    logger_sys.log_message(f"INFO: Opening player '{program_dir}/preferences.yaml'")
    with open(program_dir + '/preferences.yaml', 'r') as f:
        preferences = yaml.safe_load(f)
        check_yaml.examine(program_dir + '/preferences.yaml')
    # try to update game
    if preferences["auto update"]:
        try:
            logger_sys.log_message("INFO: Updating Game")
            repo = Repo('.git')
            assert not repo.bare
            git = repo.git
            git.pull()
        except:
            logger_sys.log_message("WARNING: Failed to update game, passing")
            pass
    else: time.sleep(.5)
    os.system('clear')
    print_title()

    options = ['Play Game', 'Manage Saves', 'Preferences', 'Check Update', 'Quit']
    choice = term_menu.show_menu(options)
    os.system('clear')

    print_title()

    if choice == 'Play Game':
        options = ['Use Latest Preset', 'Play Vanilla', 'Play Plugin']
        choice = term_menu.show_menu(options)
        using_latest_preset = False
        latest_preset = preferences["latest preset"]

        # load data files
        if choice == 'Use Latest Preset':
            logger_sys.log_message(f"INFO: Starting game with latest preset: {latest_preset}")
            using_latest_preset = True
            if preferences["latest preset"]["type"] == 'vanilla':
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

                what_plugin = preferences["latest preset"]["plugin"]

                logger_sys.log_message(f"INFO: Loading plugin '{what_plugin}' data")
                check_file = os.path.exists(program_dir + "/plugins/" + what_plugin)
                if check_file == False:
                    print(COLOR_RED + COLOR_STYLE_BRIGHT + "ERROR: Couldn't find plugin '" + what_plugin + "'" + COLOR_RESET_ALL)
                    logger_sys.log_message(f"ERROR: Couldn't find plugin '{what_plugin}'")
                    play = 0
                    exit_game()
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

            open_save = preferences["latest preset"]["save"]
            save_file = program_dir + "/saves/save_" + open_save + ".yaml"
            check_file = os.path.isfile(save_file)
            if check_file == False:
                print(COLOR_RED + COLOR_STYLE_BRIGHT + "ERROR: Couldn't find save file '" + save_file + "'" + COLOR_RESET_ALL)
                logger_sys.log_message(f"ERROR: Couldn't find save file '{save_file}'")
                play = 0
                exit_game()
            logger_sys.log_message("INFO: Opening Save File")
            with open(save_file) as f:
                player = yaml.safe_load(f)
                check_yaml.examine(save_file)
            play = 1
            menu = False
            logger_sys.log_message("INFO: Starting game and exiting menu")

        elif choice == 'Play Plugin':
            text = "Please select a plugin to use"
            print_speech_text_effect(text)
            res = []

            logger_sys.log_message(f"INFO: Searching for plugins in the '{program_dir}/plugins/' directory")
            for search_for_plugins in os.listdir(program_dir + "/plugins/"):
                res.append(search_for_plugins)

            what_plugin = input(COLOR_STYLE_BRIGHT + "Current plugins: " + COLOR_RESET_ALL + COLOR_GREEN + str(res) + COLOR_RESET_ALL + " ")
            logger_sys.log_message("INFO: Updating latest preset")
            preferences["latest preset"]["type"] = "plugin"
            preferences["latest preset"]["plugin"] = what_plugin

            check_file = os.path.exists(program_dir + "/plugins/" + what_plugin )
            if check_file == False:
                print(COLOR_RED + COLOR_STYLE_BRIGHT + "ERROR: Couldn't find plugin '" + what_plugin + "'" + COLOR_RESET_ALL)
                logger_sys.log_message("ERROR: Couldn't find plugin '" + what_plugin + "'")
                play = 0
                exit_game()
            logger_sys.log_message(f"INFO: Loading plugin {what_plugin} data")
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
        else:
            logger_sys.log_message("INFO: Updating latest preset")
            preferences["latest preset"]["type"] = "vanilla"
            preferences["latest preset"]["plugin"] = "none"

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

        if using_latest_preset == False:
            text = "Please select an action:"
            print_speech_text_effect(text)
            options = ['Open Save', 'New Save']
            choice = term_menu.show_menu(options)

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
                print_speech_text_effect(text)
                open_save = input(COLOR_STYLE_BRIGHT + "Current saves: " + COLOR_RESET_ALL + COLOR_GREEN + str(res) + COLOR_RESET_ALL + " ")
                logger_sys.log_message("INFO: Updating latest preset")
                preferences["latest preset"]["save"] = open_save

                save_file = program_dir + "/saves/save_" + open_save + ".yaml"
                check_file = os.path.isfile(save_file)
                if check_file == False:
                    print(COLOR_RED + COLOR_STYLE_BRIGHT + "ERROR: Couldn't find save file '" + save_file + "'" + COLOR_RESET_ALL)
                    logger_sys.log_message(f"ERROR: Couldn't find save file '{save_file}'")
                    play = 0
                    exit_game()
                logger_sys.log_message("INFO: Opening save file")
                with open(save_file) as f:
                    player = yaml.safe_load(f)
                    check_yaml.examine(save_file)
                play = 1
                menu = False
            else:
                text = "Please name your save: "
                print_speech_text_effect(text)
                enter_save_name = input('> ')
                player = start_player
                dumped = yaml.dump(player)
                save_name = program_dir + "/saves/save_" + enter_save_name + ".yaml"
                save_name_backup = program_dir + "/saves/~0 save_" + enter_save_name + ".yaml"
                check_file = os.path.isfile(save_name)
                logger_sys.log_message("INFO: Updating latest preset")
                preferences["latest preset"]["save"] = "/save_" + enter_save_name + ".yaml"
                if check_file == True:
                    print(COLOR_RED + COLOR_STYLE_BRIGHT + "ERROR: Save file '" + save_name + "'" + " already exists" + COLOR_RESET_ALL)
                    logger_sys.log_message(f"ERROR: Save file '{save_name}' already exists")
                    play = 0
                    exit_game()
                logger_sys.log_message("INFO: Creating new save")
                with open(save_name, "w") as f:
                    f.write(dumped)
                with open(save_name_backup, "w") as f:
                    f.write(dumped)
                save_file = save_name
                logger_sys.log_message("INFO: Opening save")
                with open(save_file) as f:
                    player = yaml.safe_load(f)
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
        print_speech_text_effect(text)
        options = ['Edit Save', 'Delete Save']
        choice = term_menu.show_menu(options)
        if choice == 'Edit Save':
            text = "Please select a save to edit."
            print_speech_text_effect(text)
            open_save = input(COLOR_STYLE_BRIGHT + "Current saves: " + COLOR_RESET_ALL + COLOR_GREEN + str(res) + COLOR_RESET_ALL + " ")
            check_file = os.path.isfile(program_dir + "/saves/save_" + open_save + ".yaml")
            if check_file == False:
                print(COLOR_RED + COLOR_STYLE_BRIGHT + "ERROR: Save file '" + program_dir + "/saves/save_" + open_save + ".yaml" + "'" + " does not exists" + COLOR_RESET_ALL)
                logger_sys.log_message(f"ERROR: Save file '{program_dir}/saves/save_{open_save}.yaml' does not exists")
                play = 0
            text = "Select an action for the selected save."
            print_speech_text_effect(text)
            options = ['Rename Save', 'Manually Edit Save']
            choice = term_menu.show_menu(options)
            if choice == 'Rename Save':
                rename_name = input("Select a new name for the save: ")
                os.rename(program_dir + "/saves/save_" + open_save + ".yaml", program_dir + "/saves/save_" + rename_name + ".yaml")
                logger_sys.log_message(f"INFO: Renaming save file '{program_dir}/saves/save_{open_save}.yaml' to '{program_dir}/saves/save_{rename_name}.yaml'")
            else:
                save_to_open = program_dir + "/saves/save_" + open_save + ".yaml"
                try:
                    editor = os.environ['EDITOR']
                except KeyError:
                    editor = 'nano'
                logger_sys.log_message(f"INFO: Manually editing save file '{save_to_open}' with editor '{editor}'")
                subprocess.call([editor, save_to_open])
        else:
            text = "Please select a save to delete."
            print_speech_text_effect(text)
            open_save = input(COLOR_STYLE_BRIGHT + "Current saves: " + COLOR_RESET_ALL + COLOR_GREEN + str(res) + COLOR_RESET_ALL + " ")
            check_file = os.path.isfile(program_dir + "/saves/save_" + open_save + ".yaml")
            if check_file == False:
                print(COLOR_RED + COLOR_STYLE_BRIGHT + "ERROR: Save file '" + program_dir + "/saves/save_" + open_save + ".yaml" + "'" + " does not exists" + COLOR_RESET_ALL)
                logger_sys.log_message(f"ERROR: Save file '{prgram_dir}/saves/save_{open_save}.yaml' does not exists")
                play = 0
            check = input("Are you sure you want to delete the following save (y/n)")
            if check.lower().startswith('y'):
                logger_sys.log_message(f"WARNING: Deleting save file '{program_dir}/saves/save_{open_save}.yaml' and save file backup '{program_dir}/saves/~0 save_{open_save}.yaml'")
                os.remove(program_dir + "/saves/save_" + open_save + ".yaml")
                os.remove(program_dir + "/saves/~0 save_" + open_save + ".yaml")
    elif choice == 'Preferences':
        try:
            editor = os.environ['EDITOR']
        except KeyError:
            editor = 'nano'
        logger_sys.log_message(f"INFO: Manually editing preferences '{program_dir}/preferences.yaml' with {editor}")
        logger_sys.log_message(f"DEBUG: Before editing preferences: {preferences}")
        subprocess.call([editor, program_dir + "/preferences.yaml"])
        with open(program_dir + '/preferences.yaml') as f:
            new_preferences = yaml.safe_load(f)
        logger_sys.log_message(f"DEBUG: After editing preferences: {new_preferences}")
    elif choice == 'Check Update':
        logger_sys.log_message("INFO: Checking for updates from github repo")
        text = "Checking for updates..."
        print_speech_text_effect(text)
        try:
            repo = Repo('.git')
            assert not repo.bare
            git = repo.git
            git.pull()
        except:
            print(COLOR_RED + "ERROR: Could not update repo: something went wrong when pulling. Please try to pull the repo manually on the command line" + COLOR_RESET_ALL)
            logger_sys.log_message("ERROR: Could not update repo: something went wrong when pulling.")
            logger_sys.log_message("DEBUG: Please make sure you're playing using the source code from the github repository. You can also try to pull the repo manually from the command line.")
            time.sleep(5)
        text = "Finished Updating."
        print_speech_text_effect(text)
    else:
        os.system('clear')
        exit(1)

# function to search through the map file
def search(x, y):
    logger_sys.log_message(f"INFO: Searching for map point corresponding to coordinates x:{x}, y:{y}")
    global map_location
    map_point_count = int(len(list(map)))
    for i in range(0, map_point_count):
        point_i = map["point" + str(i)]
        point_x, point_y = point_i["x"], point_i["y"]
        # print(i, point_x, point_y, player)
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

def print_zone_map(zone_name):
    logger_sys.log_message(f"INFO: Printing zone map '{zone_name}' ascii art")
    to_print = zone[zone_name]["map"]["map full"]
    to_print = to_print.replace('$RED', '\033[0;31m')
    to_print = to_print.replace('$GREEN', '\033[0;32m')
    to_print = to_print.replace('$YELLOW', '\033[0;33m')
    to_print = to_print.replace('$BLUE', '\033[0;34m')
    to_print = to_print.replace('$PURPLE', '\033[0;34m')
    to_print = to_print.replace('$CYAN', '\033[0;36m')
    to_print = to_print.replace('$WHITE', '\033[0;37m')
    to_print = to_print.replace('$BLACK', '\033[0;30m')
    to_print = to_print.replace('$BROWN', '\033[0;33m')
    to_print = to_print.replace('$GRAY', '\033[1;30m')

    player_equipment = []

    logger_sys.log_message("INFO: Updating player equipped items")
    if player["held item"] != " ":
        player_equipment.append(player["held item"])
    if player["held chestplate"] != " ":
        player_equipment.append(player["held chestplate"])
    if player["held leggings"] != " ":
        player_equipment.append(player["held leggings"])
    if player["held boots"] != " ":
        player_equipment.append(player["held boots"])

    player_equipment = str(player_equipment)
    player_equipment = player_equipment.replace("'", "")

    count = 0
    logger_sys.log_message("INFO: Printing UI")
    for line in to_print.splitlines():
        if count == 0:
            print(line + " NAME: " + preferences["latest preset"]["save"])
        if count == 1:
            print(line + " HEALTH: " + COLOR_STYLE_BRIGHT + COLOR_BLUE + str(player["health"]) + COLOR_RESET_ALL + "/" + COLOR_STYLE_BRIGHT + COLOR_BLUE+ str(player["max health"]) + COLOR_RESET_ALL)
        if count == 2:
            print(line + " INVENTORY: " + COLOR_STYLE_BRIGHT + COLOR_CYAN + str(len(player["inventory"]) + 1) + COLOR_RESET_ALL + "/" + COLOR_STYLE_BRIGHT + COLOR_CYAN + str(player["inventory slots"]) + COLOR_RESET_ALL)
        if count == 3:
            print(line + " ELAPSED DAYS: " + COLOR_STYLE_BRIGHT + COLOR_MAGENTA + str(round(player["elapsed time game days"], 1)) + COLOR_RESET_ALL)
        if count == 4:
            print(line + " EXP: " + COLOR_STYLE_BRIGHT + COLOR_GREEN + str(round(player["xp"], 2)) + COLOR_RESET_ALL)
        if count == 5:
            print(line + " GOLD: " + COLOR_STYLE_BRIGHT + COLOR_YELLOW + str(round(player["gold"], 2)) + COLOR_RESET_ALL)
        count += 1

def print_zone_map_alone(zone_name):
    logger_sys.log_message(f"INFO: Printing zone map '{zone_name}' ascii art")
    to_print = zone[zone_name]["map"]["map full"]
    to_print = to_print.replace('$RED', '\033[0;31m')
    to_print = to_print.replace('$GREEN', '\033[0;32m')
    to_print = to_print.replace('$YELLOW', '\033[0;33m')
    to_print = to_print.replace('$BLUE', '\033[0;34m')
    to_print = to_print.replace('$PURPLE', '\033[0;34m')
    to_print = to_print.replace('$CYAN', '\033[0;36m')
    to_print = to_print.replace('$WHITE', '\033[0;37m')
    to_print = to_print.replace('$BLACK', '\033[0;30m')
    to_print = to_print.replace('$BROWN', '\033[0;33m')
    to_print = to_print.replace('$GRAY', '\033[1;30m')

    count = 0
    for line in to_print.splitlines():
        print(line)
        count += 1

def print_npc_thumbnail(npc):
    logger_sys.log_message(f"INFO: Printing NPC '{npc}' thumbnail")
    if preferences["latest preset"]["type"] == "vanilla":
        with open(program_dir + '/game/imgs/' + npc + ".txt") as f:
            to_print = str(f.read())
    else:
        with open(program_dir + '/plugins/' +  str(preferences["latest preset"]["plugin"]) + '/imgs/' + npc + ".txt") as f:
            to_print = str(f.read())
    to_print = to_print.replace('$RED', '\033[0;31m')
    to_print = to_print.replace('$GREEN', '\033[0;32m')
    to_print = to_print.replace('$YELLOW', '\033[0;33m')
    to_print = to_print.replace('$BLUE', '\033[0;34m')
    to_print = to_print.replace('$PURPLE', '\033[0;34m')
    to_print = to_print.replace('$CYAN', '\033[0;36m')
    to_print = to_print.replace('$WHITE', '\033[0;37m')
    to_print = to_print.replace('$BLACK', '\033[0;30m')
    to_print = to_print.replace('$BROWN', '\033[0;33m')
    to_print = to_print.replace('$GRAY', '\033[1;30m')

    count = 0
    for line in to_print.splitlines():
        print(line)
        count += 1

def print_enemy_thumbnail(enemy):
    logger_sys.log_message(f"INFO: Printing enemy '{enemy}' thumbnail")
    if preferences["latest preset"]["type"] == "vanilla":
        with open(program_dir + '/game/imgs/' + enemy + ".txt") as f:
            to_print = str(f.read())
    else:
        with open(program_dir + '/plugins/' +  str(preferences["latest preset"]["plugin"]) + '/imgs/' + enemy + ".txt") as f:
            to_print = str(f.read())
    to_print = to_print.replace('$RED', '\033[0;31m')
    to_print = to_print.replace('$GREEN', '\033[0;32m')
    to_print = to_print.replace('$YELLOW', '\033[0;33m')
    to_print = to_print.replace('$BLUE', '\033[0;34m')
    to_print = to_print.replace('$PURPLE', '\033[0;34m')
    to_print = to_print.replace('$CYAN', '\033[0;36m')
    to_print = to_print.replace('$WHITE', '\033[0;37m')
    to_print = to_print.replace('$BLACK', '\033[0;30m')
    to_print = to_print.replace('$BROWN', '\033[0;33m')
    to_print = to_print.replace('$GRAY', '\033[1;30m')

    count = 0
    for line in to_print.splitlines():
        print(line)
        count += 1

def check_for_key(direction):
    logger_sys.log_message("INFO: Checking for key at every next locations possible")
    map_point_count = int(len(list(map)))
    if direction == "north":
        for i in range(0, map_point_count):
            point_i = map["point" + str(i)]
            point_x, point_y = point_i["x"], point_i["y"] - 1
            # print(i, point_x, point_y, player)
            if point_x == player["x"] and point_y == player["y"]:
                future_map_location = i
    elif direction == "south":
        for i in range(0, map_point_count):
            point_i = map["point" + str(i)]
            point_x, point_y = point_i["x"], point_i["y"] + 1
            # print(i, point_x, point_y, player)
            if point_x == player["x"] and point_y == player["y"]:
                future_map_location = i
    elif direction == "east":
        for i in range(0, map_point_count):
            point_i = map["point" + str(i)]
            point_x, point_y = point_i["x"] - 1, point_i["y"]
            # print(i, point_x, point_y, player)
            if point_x == player["x"] and point_y == player["y"]:
                future_map_location = i
    elif direction == "west":
        for i in range(0, map_point_count):
            point_i = map["point" + str(i)]
            point_x, point_y = point_i["x"] + 1, point_i["y"]
            # print(i, point_x, point_y, player)
            if point_x == player["x"] and point_y == player["y"]:
                future_map_location = i
    if "key" in map["point" + str(future_map_location)]:
        text = '='
        print_separator(text)

        text = "You need the following key(s) to enter this location, if you decide to use them, you may loose them:"
        print_long_string(text)

        keys_list = str(map["point" + str(future_map_location)]["key"]["required keys"])
        logger_sys.log_message(f"INFO: Entering map point 'point{future_map_location}' requires keys: {keys_list}")
        keys_list = keys_list.replace("'", '')
        keys_list = keys_list.replace("[", ' -')
        keys_list = keys_list.replace("]", '')
        keys_list = keys_list.replace(", ", '\n -')

        print(keys_list)

        keys_len = len(map["point" + str(future_map_location)]["key"]["required keys"])

        text = '='
        print_separator(text)

        options = ['Continue', 'Leave']
        choice = term_menu.show_menu(options)

        count = 0

        have_necessary_keys = True

        if choice == 'Continue':
            while count < keys_len and have_necessary_keys == True:

                choosen_key = map["point" + str(future_map_location)]["key"]["required keys"][int(count)]

                if choosen_key not in player["inventory"]:
                    have_necessary_keys = False
                else:
                    if map["point" + str(future_map_location)]["key"]["remove key"]:
                        player["inventory"].remove(choosen_key)
                        logger_sys.log_message(f"INFO: Removing from player inventory key '{choosen_key}'")

                count += 1

            if not have_necessary_keys:
                logger_sys.log_message("INFO: Player don't have necessary keys: passing")
                print(" ")
                text = COLOR_YELLOW + "You don't have the necessary key(s) to enter this locations"
                print_long_string(text)
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

def print_separator(character):
    count = 0

    while count < 55:
        sys.stdout.write(COLOR_STYLE_BRIGHT + character + COLOR_RESET_ALL)
        sys.stdout.flush()
        count += 1
    sys.stdout.write('\n')

def overstrike_text(text):
    result = ""
    for character in text:
        result = result + character + '\u0336'
    print(str(result))

def print_long_string(text):
    new_input = ""
    for i, letter in enumerate(text):
        if i % 54 == 0:
            new_input += '\n'
        new_input += letter

    # this is just because at the beginning too a `\n` character gets added
    new_input = new_input[1:]
    print(str(new_input))

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

def print_dialog(current_dialog):
    current_dialog_name = current_dialog
    logger_sys.log_message(f"INFO: Printing dialog '{current_dialog_name}'")
    current_dialog = dialog[str(current_dialog)]
    dialog_len = len(current_dialog["phrases"])
    if "scene" in current_dialog:
        current_dialog_scene = str(current_dialog["scene"])
        logger_sys.log_message(f"INFO: Printing dialog '{current_dialog_name}' scene at '{program_dir}/game/imgs/{current_dialog_scene}.txt'")
        if preferences["latest preset"]["type"] == 'vanilla':
            with open(program_dir + '/game/imgs/' + str(current_dialog["scene"]) + '.txt') as f:
                to_print = str(f.read())
                to_print = to_print.replace('$RED', '\033[0;31m')
                to_print = to_print.replace('$GREEN', '\033[0;32m')
                to_print = to_print.replace('$YELLOW', '\033[0;33m')
                to_print = to_print.replace('$BLUE', '\033[0;34m')
                to_print = to_print.replace('$PURPLE', '\033[0;34m')
                to_print = to_print.replace('$CYAN', '\033[0;36m')
                to_print = to_print.replace('$WHITE', '\033[0;37m')
                to_print = to_print.replace('$BLACK', '\033[0;30m')
                to_print = to_print.replace('$BROWN', '\033[0;33m')
                to_print = to_print.replace('$GRAY', '\033[1;30m')
                print(to_print)
        else:
            current_plugin = str(preferences["latest preset"]["plugin"])
            logger_sys.log_message(f"INFO: Printing dialog '{current_dialog_name}' scene at '{program_dir}/plugins/{current_plugin}/imgs/{current_dialog_scene}.txt'")
            with open(program_dir + '/plugins/' + str(preferences["latest preset"]["plugin"]) + '/imgs/' + str(current_dialog["scene"]) + '.txt') as f:
                to_print = str(f.read())
                to_print = to_print.replace('$RED', '\033[0;31m')
                to_print = to_print.replace('$GREEN', '\033[0;32m')
                to_print = to_print.replace('$YELLOW', '\033[0;33m')
                to_print = to_print.replace('$BLUE', '\033[0;34m')
                to_print = to_print.replace('$PURPLE', '\033[0;34m')
                to_print = to_print.replace('$CYAN', '\033[0;36m')
                to_print = to_print.replace('$WHITE', '\033[0;37m')
                to_print = to_print.replace('$BLACK', '\033[0;30m')
                to_print = to_print.replace('$BROWN', '\033[0;33m')
                to_print = to_print.replace('$GRAY', '\033[1;30m')
                print(to_print)
    count = 0
    logger_sys.log_message(f"INFO: Printing dialog '{current_dialog_name}' phrases")
    while count < dialog_len:
        text = str(current_dialog["phrases"][int(count)])
        count = 0
        while count < len(list(text_replacements_generic)):
            current_text_replacement = str(list(text_replacements_generic)[count])
            text = text.replace(current_text_replacement, str(text_replacements_generic[current_text_replacement]))
            count += 1
        print_speech_text_effect(text)
        count += 1
    if current_dialog["use actions"] == True:
        logger_sys.log_message(f"INFO: Executing dialog '{current_dialog_name}' actions on the player")
        actions = current_dialog["actions"]
        if "give item" in actions:
            given_items = actions["give item"]
            given_items_len = len(given_items)
            count = 0
            logger_sys.log_message(f"INFO: Giving to the player items '{give_items}'")
            while count < given_items_len:
                selected_item = given_items[count]
                player["inventory"].append(selected_item)
                count += 1
        if "add attributes" in actions:
            count = 0
            added_attributes = actions["add attributes"]
            added_attributes_len = len(added_attributes)
            logger_sys.log_message(f"INFO: Adding attributes '{added_attributes}' to the player")
            while count < added_attributes_len:
                selected_attribute = added_attributes[count]
                player["attributes"].append(selected_attribute)
                count += 1
        if "health modification" in actions:
            if "diminution" in actions["health modification"]:
                logger_sys.log_message("INFO: Removing " + actions["health modification"]["diminution"] + " hp from the player's health")
                player["health"] -= actions["health modification"]["diminution"]
            if "augmentation" in actions["health modification"]:
                logger_sys.log_message("INFO: Adding " + actions["health modification"]["augmentation"] + " hp from the player's health")
                player["health"] += actions["health modification"]["augmentation"]
            if "max health" in actions["health modification"]:
                if "diminution" in actions["health modification"]["max health"]:
                    logger_sys.log_message("INFO: Removing " + actions["health modification"]["max health"]["diminution"] + " hp from the player's max health")
                    player["max health"] -= actions["health modification"]["max health"]["diminution"]
                if "augmentation" in actions["health modification"]["max health"]:
                    logger_sys.log_message("INFO: Adding " + actions["health modification"]["max health"]["augmentation"] + " hp from the player's max health")
                    player["max health"] += actions["health modification"]["max health"]["augmentation"]
        if "gold modification" in actions:
            if "diminution" in actions["gold modification"]:
                logger_sys.log_message("INFO: Removing " + actions["gold modification"]["diminution"] + " gold to the player")
                player["gold"] -= actions["gold modification"]["diminution"]
            if "augmentation" in actions["gold modification"]:
                logger_sys.log_message("INFO: Adding " + actions["gold modification"]["diminution"] + " gold to the player")
                player["gold"] += actions["gold modification"]["augmentation"]
        if "remove item" in actions:
            removed_items = actions["remove item"]
            removed_items_len = len(removed_items)
            count = 0
            logger_sys.log_message(f"INFO: Removing items '{removed_items}' from player's inventory")
            while count < removed_items_len:
                selected_item = removed_items[count]
                player["inventory"].remove(selected_item)
                count += 1
        if "add to diary" in actions:
            if "known zones" in actions["add to diary"]:
                added_visited_zones = actions["add to diary"]["known zones"]
                added_visited_zones_len = len(added_visited_zones)
                count = 0
                logger_sys.log_message(f"INFO: Adding zones '{added_visited_zones}' to player's visited zones")
                while count < added_visited_zones_len:
                    selected_zone = added_visited_zones[count]
                    player["visited zones"].append(selected_zone)
                    count += 1
            if "known enemies" in actions["add to diary"]:
                added_known_enemies = actions["add to diary"]["known enemies"]
                added_known_enemies_len = len(added_known_enemies)
                count = 0
                logger_sys.log_message(f"INFO: Adding enemies '{added_known_enemies}' to player's known enemies")
                while count < added_known_enemies_len:
                    selected_enemy = added_known_enemies[count]
                    player["enemies list"].append(selected_enemy)
                    count += 1
            if "known npcs" in actions["add to diary"]:
                added_known_npcs = actions["add to diary"]["known npcs"]
                added_known_npcs_len = len(added_known_npcs)
                count = 0
                logger_sys.log_message(f"INFO: Adding npcs '{added_known_npcs}' to player's known npcs")
                while count < added_known_npcs_len:
                    selected_npc = added_known_npcs[count]
                    player["met npcs name"].append(selected_npc)
                    count += 1
        if "remove to diary" in actions:
            if "known zones" in actions["remove to diary"]:
                removed_visited_zones = actions["remove to diary"]["known zones"]
                removed_visited_zones_len = len(removed_visited_zones)
                count = 0
                logger_sys.log_message(f"INFO: Removing zones '{added_visited_zones}' to player's visited zones")
                while count < removed_visited_zones_len:
                    selected_zone = removed_visited_zones[count]
                    player["visited zones"].remove(selected_zone)
                    count += 1
            if "known enemies" in actions["remove to diary"]:
                removed_known_enemies = actions["remove to diary"]["known enemies"]
                removed_known_enemies_len = len(removed_known_enemies)
                count = 0
                logger_sys.log_message(f"INFO: Removing enemies '{added_known_enemies}' to player's known enemies")
                while count < removed_known_enemies_len:
                    selected_enemy = removed_known_npcs[count]
                    player["enemies list"].remove(selected_enemy)
                    count += 1
            if "known npcs" in actions["remove to diary"]:
                removed_known_npcs = actions["remove to diary"]["known npcs"]
                removed_known_npcs_len = len(removed_known_npcs)
                count = 0
                logger_sys.log_message(f"INFO: Removing npcs '{added_known_npcs}' to player's known npcs")
                while count < removed_known_npcs_len:
                    selected_npc = removed_known_npcs[count]
                    player["met npcs name"].append(selected_npc)
                    count += 1
        if "use drink" in actions:
            used_drinks = actions["use drink"]
            used_drinks_len = len(used_drinks)
            count = 0
            logger_sys.log_message(f"INFO: Using drinks '{used_drinks}'")
            while count < used_drinks_len:
                selected_drink = used_drinks_len[count]
                if drinks[selected_drink]["healing level"] == 999:
                    player["health"] = player["max health"]
                else:
                    player["health"] += drinks[selected_drink]["healing level"]

def generate_random_uuid():
    logger_sys.log_message("INFO: Generating new random UUID using 'uuid.4' method")
    import uuid
    random_uuid = uuid.uuid4()
    random_uuid = str(random_uuid)
    random_uuid = random_uuid.replace('UUID', '')
    random_uuid = random_uuid.replace('(', '')
    random_uuid = random_uuid.replace(')', '')
    random_uuid = random_uuid.replace("'", '')
    logger_sys.log_message(f"INFO: Generated new random UUID: '{random_uuid}'")
    return random_uuid

def check_for_item(item_name):
    logger_sys.log_message(f"INFO: Checking if item '{item_name}' actually exists")
    item_exist = False
    if str(item_name) in list(item):
        item_exist = True
    return item_exist

def check_weapon_next_upgrade_name(item_name):
    logger_sys.log_message(f"INFO: Check for equipment '{item_name}' next upgrade")
    weapon_next_upgrade_name = str(item_name)
    check_weapon_max_upgrade_number = check_weapon_max_upgrade(str(weapon_next_upgrade_name))
    if item[weapon_next_upgrade_name]["upgrade tier"] == check_weapon_max_upgrade_number:
        weapon_next_upgrade_name = None
        logger_sys.log_message(f"INFO: No next upgrade found for equipment '{item_name}'")
    else:
        item_data = item[item_name]
        further_upgrade = True
        item_data = item[weapon_next_upgrade_name]
        # get logical weapon new upgrade name
        weapon_already_upgraded = False
        if "(" in str(item_name):
            weapon_already_upgraded = True

        if not weapon_already_upgraded:
            weapon_next_upgrade_name = str(item_name) + " (1)"
        else:
            weapon_next_upgrade_name = str(weapon_next_upgrade_name[ 0 : weapon_next_upgrade_name.index("(")]) + "(" + str(item_data["upgrade tier"] + 1) + ")"

        # check if the next upgrade actually exist
        item_upgrade_exist = check_for_item(weapon_next_upgrade_name)
        if not item_upgrade_exist:
            further_upgrade = False

        weapon_next_upgrade_name = str(weapon_next_upgrade_name)
        logger_sys.log_message(f"INFO: Found next upgrade for equipment '{item_name}': '{weapon_next_upgrade_name}'")

    return weapon_next_upgrade_name

def check_weapon_max_upgrade(item_name):
    logger_sys.log_message(f"INFO: Getting equipment '{item_name}' max upgrade")
    weapon_next_upgrade_name = str(item_name)
    item_data = item[item_name]
    further_upgrade = True

    while further_upgrade:
        item_data = item[weapon_next_upgrade_name]
        # get logical weapon new upgrade name
        weapon_already_upgraded = False
        if "(" in str(weapon_next_upgrade_name):
            weapon_already_upgraded = True

        if weapon_already_upgraded == False:
            weapon_next_upgrade_name = str(item_name) + " (1)"
        else:
            weapon_next_upgrade_name = str(weapon_next_upgrade_name[ 0 : weapon_next_upgrade_name.index("(")]) + "(" + str(item_data["upgrade tier"] + 1) + ")"

        # check if the next upgrade actually exist
        item_upgrade_exist = check_for_item(weapon_next_upgrade_name)
        if item_upgrade_exist == False:
            further_upgrade = False

    # correct max upgrade count
    weapon_next_upgrade_name_count = weapon_next_upgrade_name
    listOfWords = weapon_next_upgrade_name_count.split("(", 1)
    if len(listOfWords) > 0:
        weapon_next_upgrade_name_count = listOfWords[1]
    weapon_next_upgrade_name_count = int(weapon_next_upgrade_name_count.replace(")", ""))
    weapon_next_upgrade_name_count -= 1

    return weapon_next_upgrade_name_count

def detect_weapon_next_upgrade_items(item_name):
    logger_sys.log_message(f"INFO: Getting equipment '{item_name}' next upgrade items")
    weapon_next_upgrade_name = str(item_name)
    item_data = item[item_name]
    weapon_already_upgraded = False

    # get logical weapon new upgrade name
    if "(" in str(item_name):
        weapon_already_upgraded = True

    if not weapon_already_upgraded:
        weapon_next_upgrade_name = str(item_name) + " (1)"
    else:
        weapon_next_upgrade_name = str(weapon_next_upgrade_name[ 0 : weapon_next_upgrade_name.index("(")]) + "(" + str(item_data["upgrade tier"] + 1) + ")"

    # check if the next upgrade actually exist
    item_upgrade_exist = check_for_item(weapon_next_upgrade_name)
    if not item_upgrade_exist:
        weapon_next_upgrade_name = None

    # get next weapon upgrade needed items
    if weapon_next_upgrade_name != None:
        weapon_next_upgrade_items = item[str(weapon_next_upgrade_name)]["for this upgrade"]
    else:
        weapon_next_upgrade_items = "None"

    # format so that for example: Raw Iron, Raw Iron become Raw IronX2
    count = 0
    while count < len(weapon_next_upgrade_items):
        current_item = str(list(weapon_next_upgrade_items)[0])
        current_item_number = weapon_next_upgrade_items.count(current_item)

        count2 = 0
        if current_item_number > 1:
            while count2 < current_item_number - 1:
                weapon_next_upgrade_items.remove(current_item)
                count2 += 1
            weapon_next_upgrade_items = [sub.replace(current_item, current_item + "X" + str(current_item_number)) for sub in weapon_next_upgrade_items]

        count += 1

    # convert list to string and
    # format the string to look better

    weapon_next_upgrade_items = str(weapon_next_upgrade_items)
    weapon_next_upgrade_items = weapon_next_upgrade_items.replace("'", '')
    weapon_next_upgrade_items = weapon_next_upgrade_items.replace("[", '')
    weapon_next_upgrade_items = weapon_next_upgrade_items.replace("]", '')

    logger_sys.log_message(f"INFO: Found equipment '{item_name}' next upgrade items: '{weapon_next_upgrade_items}'")
    return weapon_next_upgrade_items

# check correct grammar for 'a' in front of a
# certain word. will return the right text like this:
# <a/an> <word>
def a_an_check(word):
    logger_sys.log_message(f"INFO: Checking correct grammar of 'a' in front of '{word}'")
    global to_return
    vowels = ['a', 'e', 'i', 'o', 'u']
    if word[0] in vowels:
        to_return = "an " + word
    else:
        to_return = "a " + word
    logger_sys.log_message(f"INFO: Checking correct grammar of 'a' in front of '{word}': '{to_return}'")
    return to_return

# gameplay here:
def run(play):
    if preferences["speed up"] != True:
        logger_sys.log_message("INFO: Printing loading menu")
        print(separator)
        print(COLOR_GREEN + COLOR_STYLE_BRIGHT + "Reserved keys:" + COLOR_RESET_ALL)
        print(COLOR_BLUE + COLOR_STYLE_BRIGHT + "N: "+ COLOR_RESET_ALL + "Go north" + COLOR_RESET_ALL)
        print(COLOR_BLUE + COLOR_STYLE_BRIGHT + "S: "+ COLOR_RESET_ALL + "Go south" + COLOR_RESET_ALL)
        print(COLOR_BLUE + COLOR_STYLE_BRIGHT + "E: " + COLOR_RESET_ALL + "Go east" + COLOR_RESET_ALL)
        print(COLOR_BLUE + COLOR_STYLE_BRIGHT + "W: " + COLOR_RESET_ALL + "Go west" + COLOR_RESET_ALL)
        print(COLOR_BLUE + COLOR_STYLE_BRIGHT + "D: " + COLOR_RESET_ALL + "Access to your diary.")
        print(COLOR_BLUE + COLOR_STYLE_BRIGHT + "I: " + COLOR_RESET_ALL + "View items. When in this view, type the name of an item to examine it." + COLOR_RESET_ALL)
        print(COLOR_BLUE + COLOR_STYLE_BRIGHT + "Y: " + COLOR_RESET_ALL + "View mounts. When in this view, type the name of the mount to examine it." + COLOR_RESET_ALL)
        print(COLOR_BLUE + COLOR_STYLE_BRIGHT + "Z: " + COLOR_RESET_ALL + "Access to nearest hostel, stable or church.")
        print(COLOR_BLUE + COLOR_STYLE_BRIGHT + "Q: " + COLOR_RESET_ALL + "Quit game")
        print(" ")
        print(COLOR_GREEN + COLOR_STYLE_BRIGHT + "Hints:" + COLOR_RESET_ALL)
        print("If you find an item on the ground, type the name of the item to take it.")
        print("Some items have special triggers, which will often be stated in the description. Others can only be activated in certain situations, like in combat.")
        print(separator)
        print(" ")

        loading = 4
        while loading > 0:
            print("Loading game... ▁▁▁", end='\r')
            time.sleep(.15)
            print("Loading game... ▁▁▃", end='\r')
            time.sleep(.15)
            print("Loading game... ▁▃▅", end='\r')
            time.sleep(.15)
            print("Loading game... ▃▅▅", end='\r')
            time.sleep(.15)
            print("Loading game... ▅▅▅", end='\r')
            time.sleep(.15)
            print("Loading game... ▅▅▃", end='\r')
            time.sleep(.15)
            print("Loading game... ▅▃▁", end='\r')
            time.sleep(.15)
            print("Loading game... ▃▁▁", end='\r')
            time.sleep(.15)
            print("Loading game... ▁▁▁", end='\r')
            time.sleep(.15)
            loading -= 1

    # Mapping stuff

    while play == 1:
        global player

        # get start time
        start_time = time.time()
        logger_sys.log_message(f"INFO: Getting start time: '{start_time}'")

        # get terminal size
        logger_sys.log_message("INFO: Getting terminal width and height size")
        terminal_rows, terminal_columns = os.popen('stty size', 'r').read().split()
        logger_sys.log_message(f"INFO: Got terminal width and height size: {terminal_rows}x{terminal_columns}")

        # clear text
        os.system('clear')


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
                player["mounts"][str(player["current mount"])]["stats"]["agility addition"] = round(mounts[current_mount_type]["stats"]["agility addition"] + ( mounts[current_mount_type]["levels"]["level stat additions"]["agility addition"] * ( round(current_mount_data["level"]) - 1 )), 3)
                player["mounts"][str(player["current mount"])]["stats"]["resistance addition"] = round(mounts[current_mount_type]["stats"]["resistance addition"] + ( mounts[current_mount_type]["levels"]["level stat additions"]["resistance addition"] * ( round(current_mount_data["level"]) - 1 )), 3)


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
        # always round player health to an integer amount
        player["health"] = int(round(player["health"]))

        logger_sys.log_message("INFO: Calculating day time")
        # calculate day time
        day_time = "PLACEHOLDER" # .25 = morning .50 = day .75 = evening .0 = night
        day_time_decimal = "." + str(player["elapsed time game days"]).split(".",1)[1]
        day_time_decimal = float(day_time_decimal)
        if day_time_decimal < .25 and day_time_decimal > .0:
            day_time = COLOR_RED + COLOR_STYLE_BRIGHT + "NIGHT" + COLOR_RESET_ALL
        elif day_time_decimal > .25 and day_time_decimal < .50:
            day_time = COLOR_BLUE + COLOR_STYLE_BRIGHT + "MORNING" + COLOR_RESET_ALL
        elif day_time_decimal > .50 and day_time_decimal < .75:
            day_time = COLOR_GREEN + COLOR_STYLE_BRIGHT + "DAY" + COLOR_RESET_ALL
        elif day_time_decimal > .75 and day_time_decimal:
            day_time = COLOR_YELLOW + COLOR_STYLE_BRIGHT + "EVENING" + COLOR_RESET_ALL


        logger_sys.log_message("INFO: Calculating player armor protection stat")
        # calculate player armor protection
        # and write it to the save file
        player_items = player["inventory"]
        player_items_number = len(player_items)
        count = 0
        global_armor_protection = 0
        p = True

        # loop to get player total armor protection
        while p:
            if count > ( player_items_number - 1 ):
                p = False
            if p == True:

                player_items_select = player_items[int(count)]

                if item[player_items_select]["type"] == "Armor Piece: Chestplate" and player["held chestplate"] == player_items_select:
                    item_armor_protection = item[player_items_select]["armor protection"]
                elif item[player_items_select]["type"] == "Armor Piece: Boots" and player["held boots"] == player_items_select:
                    item_armor_protection = item[player_items_select]["armor protection"]
                elif item[player_items_select]["type"] == "Armor Piece: Leggings" and player["held leggings"] == player_items_select:
                    item_armor_protection = item[player_items_select]["armor protection"]
                elif item[player_items_select]["type"] == "Armor Piece: Shield" and player["held shield"] == player_items_select:
                    item_armor_protection = item[player_items_select]["armor protection"]
                else:
                    item_armor_protection = 0

                global_armor_protection += item_armor_protection

                count += 1

        global_armor_protection = round(global_armor_protection, 2)
        if player["current mount"] in player["mounts"]:
            global_armor_protection += player["mounts"][player["current mount"]]["stats"]["resistance addition"]

        player["armor protection"] = round(global_armor_protection, 2)

        logger_sys.log_message("INFO: Calculating player agility stat")
        # calculate player agility and
        # write it to the save file
        player_items = player["inventory"]
        player_items_number = len(player_items)
        count = 0
        global_agility = 0
        p = True

        # loop to get player total agility
        while p:
            if count > ( player_items_number - 1 ):
                p = False
            if p == True:

                player_items_select = player_items[int(count)]

                if item[player_items_select]["type"] == "Armor Piece: Chestplate" and player["held chestplate"] == player_items_select:
                    item_agility = item[player_items_select]["agility"]
                elif item[player_items_select]["type"] == "Armor Piece: Boots" and player["held boots"] == player_items_select:
                    item_agility = item[player_items_select]["agility"]
                elif item[player_items_select]["type"] == "Armor Piece: Leggings" and player["held leggings"] == player_items_select:
                    item_agility = item[player_items_select]["agility"]
                elif item[player_items_select]["type"] == "Armor Piece: Shield" and player["held shield"] == player_items_select:
                    item_agility = item[player_items_select]["agility"]
                elif item[player_items_select]["type"] == "Weapon" and player["held item"] == player_items_select:
                    item_agility = item[player_items_select]["agility"]
                else:
                    item_agility = 0

                global_agility += item_agility

                count += 1

        global_agility = round(global_agility, 2)

        if player["current mount"] in player["mounts"]:
            global_agility += player["mounts"][player["current mount"]]["stats"]["agility addition"]

        player["agility"] = round(global_agility, 2)

        logger_sys.log_message("INFO: Calculating player remaining inventory slots and total inventory slots")
        # calculate remaining inventory slots
        # and write it to the save files
        p2 = True
        count2 = 0
        global_inventory_slots = 0
        player_items = player["inventory"]
        player_items_number = len(player_items)

        # loop to get player total inventory slots
        while p2:
            if count2 > ( player_items_number - 1 ):
                p2 = False
            if p2 == True:

                player_items_select = player_items[int(count2)]

                if item[player_items_select]["type"] == "Bag":
                    item_inventory_slot = item[player_items_select]["inventory slots"]
                else:
                    item_inventory_slot = 0

                global_inventory_slots += item_inventory_slot

                count2 += 1

            player["inventory slots"] = global_inventory_slots

        # calculate remaining item slots

        player["inventory slots remaining"] = int(player["inventory slots"]) - int(player_items_number)


        map_location = search(player["x"], player["y"])
        logger_sys.log_message("INFO: Checking player location is valid")
        # check player map location
        if map_location == None:
            text = COLOR_RED + COLOR_STYLE_BRIGHT + "FATAL ERROR: You are in an undefined location. This could have been the result of using or not using a plugin. Verify you are using the right plugin for this save or manually modify your player coordinates in the 'Manage Saves' in the main menu. The game will close in 10 secs." + COLOR_RESET_ALL
            logger_sys.log_message("CRITICAL: Player is in an undefined location.")
            logger_sys.log_message("DEBUG: This could have been the result of using or not using a plugin. Verify you are using the right plugin for this save or manually modify your player coordinates in the 'Manage Saves' in the main menu.")
            print_long_string(text)
            time.sleep(10)
            os.system('clear')
            exit_game()
        logger_sys.log_message("INFO: Getting player current map zone location")
        map_zone = map["point" + str(map_location)]["map zone"]
        logger_sys.log_message("INFO: Updating player 'map zone' in the save file")
        player["map zone"] = map_zone

        logger_sys.log_message(f"INFO: Checking if player current map point 'point{map_location}' and map zone '{map_zone}' are already known by the player")
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
        print_separator(text)

        print("DAY TIME: " + day_time)
        print("LOCATION: " + map_zone + " (" + COLOR_STYLE_BRIGHT + COLOR_GREEN + str(player["x"]) + COLOR_RESET_ALL + ", " + COLOR_STYLE_BRIGHT + COLOR_GREEN + str(player["y"]) + COLOR_RESET_ALL + ")")

        text = '='
        print_separator(text)

        print_zone_map(map_zone)

        text = '='
        print_separator(text)

        print("DIRECTIONS: " + "          ACTIONS:")

        if "North" not in map["point" + str(map_location)]["blocked"]:
            print("You can go North ▲" + "    " + COLOR_BLUE + COLOR_STYLE_BRIGHT + "I: " + COLOR_RESET_ALL + "View items")
        else:
            print( "                  " + "    " + COLOR_BLUE + COLOR_STYLE_BRIGHT + "I: " + COLOR_RESET_ALL + "View items")
        if "South" not in map["point" + str(map_location)]["blocked"]:
            print("You can go South ▼" + "    " + COLOR_BLUE + COLOR_STYLE_BRIGHT + "D: " + COLOR_RESET_ALL + "Check your diary")
        else:
            print( "                  " + "    " + COLOR_BLUE + COLOR_STYLE_BRIGHT + "D: " + COLOR_RESET_ALL + "Check your diary")
        if "East" not in map["point" + str(map_location)]["blocked"]:
            print("You can go East ►" + "     " + COLOR_BLUE + COLOR_STYLE_BRIGHT + "Z: " + COLOR_RESET_ALL + "Interact with zone (hostel...)")
        else:
            print("                 " + "     " + COLOR_BLUE + COLOR_STYLE_BRIGHT + "Z: " + COLOR_RESET_ALL + "Interact with zone (hostel...)")
        if "West" not in map["point" + str(map_location)]["blocked"]:
            print("You can go West ◄" + "     " + COLOR_BLUE + COLOR_STYLE_BRIGHT + "Q: " + COLOR_RESET_ALL + "Quit & save")
        else:
            print("                 " + "     " + COLOR_BLUE + COLOR_STYLE_BRIGHT + "Q: " + COLOR_RESET_ALL + "Quit & save")

        text = '='
        print_separator(text)

        logger_sys.log_message("INFO: Checking if the start dialog should be displayed to the player")
        # player start dialog
        if player["start dialog"]["heard start dialog"] == False:
            start_dialog = player["start dialog"]["dialog"]
            logger_sys.log_message("INFO: Displaying start dialog '{start_dialog}' to player")
            print_dialog(player["start dialog"]["dialog"])
            text = '='
            print_separator(text)

            player["start dialog"]["heard start dialog"] = True

        global is_in_village, is_in_hostel, is_in_stable, is_in_blacksmith, is_in_blacksmith
        is_in_village = False
        is_in_hostel = False
        is_in_stable = False
        is_in_blacksmith = False
        is_in_forge = False
        logger_sys.log_message("INFO: Checking if player is in a village, hostel, stable, blacksmith or forge")
        if zone[map_zone]["type"] == "village" or zone[map_zone]["type"] == "hostel" or zone[map_zone]["type"] == "stable" or zone[map_zone]["type"] == "blacksmith" or zone[map_zone]["type"] == "forge":
            logger_sys.log_message(f"INFO: Printing map zone '{map_zone}' news")
            print("NEWS:")
            village_news = zone[map_zone]["news"]
            village_news_len = len(village_news)
            choose_rand_news = random.randint(0, ( village_news_len - 1 ))
            choose_rand_news = village_news[int(choose_rand_news)]
            print_long_string(choose_rand_news)
            text = '='
            print_separator(text)
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
                    logger_sys.log_message(f"INFO: Checking if player has required attributes '{required_attributes}' to display dialog '{current_dialog}'")
                    while count < required_attributes_len and has_required_attributes == True:
                        selected_attribute = required_attributes[count]
                        if selected_attribute not in player["attributes"]:
                            has_required_attributes = False
                            logger_sys.log_message("INFO: Player doesn't have required attributes to display this dialog")
                        count += 1
                if "visited locations" in dialog[str(current_dialog)]["to display"]:
                    count = 0
                    required_locations = dialog[str(current_dialog)]["to display"]["visited locations"]
                    required_locations_len = len(required_attributes)
                    logger_sys.log_message(f"INFO: Checking if player has required visited locations '{required_locations}' to display dialog '{current_dialog}'")
                    while count < required_locations_len and has_required_locations == True:
                        selected_location = required_locations[count]
                        if selected_location not in player["visited points"]:
                            has_required_locations = False
                            logger_sys.log_message("INFO: Player doesn't have required visited locations to display this dialog")
                        count += 1
                if "known enemies" in dialog[str(current_dialog)]["to display"]:
                    count = 0
                    required_enemies = dialog[str(current_dialog)]["to display"]["known enemies"]
                    required_enemies_len = len(required_enemies)
                    logger_sys.log_message(f"INFO: Checking if player has required known enemies '{required_enemies}' to display dialog '{current_dialog}'")
                    while count < required_enemies_len and has_required_enemies == True:
                        selected_enemy = required_enemies[count]
                        if selected_enemy not in player["enemies list"]:
                            has_required_enemies = False
                            logger_sys.log_message("INFO: Player doesn't have required known enemies to display this dialog")
                        count += 1
                if "known npcs" in dialog[str(current_dialog)]["to display"]:
                    count = 0
                    required_npcs = dialog[str(current_dialog)]["to display"]["known npcs"]
                    required_npcs_len = len(required_npcs)
                    logger_sys.log_message(f"INFO: Checking if player has required known npcs '{required_npcs}' to display dialog '{current_dialog}'")
                    while count < required_npcs_len and has_required_npcs == True:
                        selected_npc = required_npcs[count]
                        if selected_npc not in player["met npcs names"]:
                            has_required_npcs = False
                            logger_sys.log_message("INFO: Player doesn't have required known npcs to display this dialog")
                        count += 1
            if has_required_attributes and has_required_locations and has_required_enemies and has_required_npcs:
                logger_sys.log_message(f"INFO: Player has all required stuff to display dialog '{current_dialog}' --> displaying it and adding map location '{map_location}' to the player's heard dialogs save list")
                print_dialog(current_dialog)
                player["heard dialogs"].append(map_location)
                text = '='
                print_separator(text)
            else:
                logger_sys.log_message("INFO: Player doesn't have all required stuff to display dialog '{current_dialog}' --> passing")
        logger_sys.log_message("INFO: Checking if the player is in a village")
        if zone[map_zone]["type"] == "village":
            is_in_village = True
        logger_sys.log_message("INFO: Checking if the player is in a forge")
        if zone[map_zone]["type"] == "forge":
            is_in_forge = True
            current_forge = zone[map_zone]
            current_forge_name = current_forge["name"]
            logger_sys.log_message(f"INFO: Printing current forge '{current_forge_name}' information to GUI")
            print(str(current_forge["name"]) + ":")
            text = current_forge["description"]
            print_long_string(text)
            print(" ")
            if "None" not in current_forge["forge"]["buys"]:
                print("METAL BUYS:")
                count = 0
                metal_buys = current_forge["forge"]["buys"]
                metal_buys_len = len(metal_buys)
                while count < metal_buys_len:
                    current_metal = str(metal_buys[count])
                    print(" -" + current_metal + " " + COLOR_YELLOW + COLOR_STYLE_BRIGHT + str(round(item[current_metal]["gold"] * current_forge["cost value"], 2)) + COLOR_RESET_ALL)
                    count += 1
            if "None" not in current_forge["forge"]["sells"]:
                print("METAL SELLS:")
                count = 0
                metal_sells = current_forge["forge"]["sells"]
                metal_sells_len = len(metal_sells)
                while count < metal_sells_len:
                    current_metal = str(metal_sells[count])
                    print(" -" + current_metal + " " + COLOR_YELLOW + COLOR_STYLE_BRIGHT + str(round(item[current_metal]["gold"] * current_forge["cost value"], 2)) + COLOR_RESET_ALL)
                    count += 1
            text = '='
            print_separator(text)
        logger_sys.log_message("INFO: Checking if the player is in a blacksmith")
        if zone[map_zone]["type"] == "blacksmith":
            is_in_blacksmith = True
            current_black_smith = zone[map_zone]
            current_black_smith_name = current_black_smith["name"]
            logger_sys.log_message(f"INFO: Printing current blacksmith '{current_black_smith_name}' information to GUI")
            print(str(current_black_smith["name"]) + ":")
            text = current_black_smith["description"]
            print_long_string(text)
            print("")
            if "None" not in current_black_smith["blacksmith"]["buys"]:
                print("EQUIPMENT BUYS:")
                count = 0
                weapon_buys = current_black_smith["blacksmith"]["buys"]
                weapon_buys_len = len(weapon_buys)
                while count < weapon_buys_len:
                    current_weapon = str(weapon_buys[int(count)])
                    print(" -" + current_weapon + " " + COLOR_YELLOW + COLOR_STYLE_BRIGHT + str(round(item[current_weapon]["gold"] * current_black_smith["cost value"], 2)) + COLOR_RESET_ALL)
                    count += 1
            if "None" not in current_black_smith["blacksmith"]["orders"]:
                print("EQUIPMENT ORDERS:")
                count = 0
                weapon_orders = current_black_smith["blacksmith"]["orders"]
                weapon_orders_len = len(weapon_orders)
                while count < weapon_orders_len:
                    current_weapon = str(list(weapon_orders)[int(count)])
                    current_weapon_materials = current_black_smith["blacksmith"]["orders"][current_weapon]["needed materials"]
                    count2 = 0
                    global_current_weapon_materials = []
                    current_weapon_materials_num = len(current_weapon_materials)
                    while count2 < current_weapon_materials_num:
                        current_material = current_weapon_materials[count2]

                        global_current_weapon_materials += [current_material]

                        count2 += 1

                    count2 = 0
                    count3 = 0

                    while count2 < len(global_current_weapon_materials):
                        current_material = global_current_weapon_materials[count2]
                        current_material_number = str(global_current_weapon_materials.count(current_material))

                        if global_current_weapon_materials.count(current_material) > 1:
                            while count3 < global_current_weapon_materials.count(current_material):
                                global_current_weapon_materials.remove(current_material)
                                count3 += 1
                            global_current_weapon_materials = [sub.replace(current_material, current_material + "X" + current_material_number) for sub in global_current_weapon_materials]

                        count2 += 1

                    global_current_weapon_materials = str(global_current_weapon_materials)
                    global_current_weapon_materials = global_current_weapon_materials.replace("'", '')
                    global_current_weapon_materials = global_current_weapon_materials.replace("[", '')
                    global_current_weapon_materials = global_current_weapon_materials.replace("]", '')
                    print(" -" + current_weapon + " " + COLOR_YELLOW + COLOR_STYLE_BRIGHT + str(round(item[current_weapon]["gold"] * current_black_smith["cost value"], 2)) + COLOR_RESET_ALL + COLOR_GREEN + COLOR_STYLE_BRIGHT + " (" + COLOR_RESET_ALL + global_current_weapon_materials + COLOR_GREEN + COLOR_STYLE_BRIGHT + ")" + COLOR_RESET_ALL)
                    count += 1
            text = '='
            print_separator(text)
        logger_sys.log_message("INFO: Checking if the player is in a stable")
        if zone[map_zone]["type"] == "stable":
            is_in_stable = True
            current_stable = zone[map_zone]
            current_stable_name = current_stable["name"]
            print(str(current_stable["name"]) + ":")
            logger_sys.log_message(f"INFO: Printing current stable '{current_stable_name}' information to GUI")
            text = current_stable["description"]
            print_long_string(text)
            print(" ")
            print("DEPOSIT COST/DAY: " + COLOR_YELLOW + COLOR_STYLE_BRIGHT + str(current_stable["deposit gold"]) + COLOR_RESET_ALL)
            print("TRAINING COST/DAY: " + COLOR_YELLOW + COLOR_STYLE_BRIGHT + str(current_stable["training gold"]) + COLOR_RESET_ALL)
            options = ['Train Mount', '']
            if "None" not in current_stable["stable"]["sells"]["mounts"]:
                print("MOUNTS SELLS:")
                count = 0
                stable_mounts = current_stable["stable"]["sells"]["mounts"]
                stable_mounts_len = len(stable_mounts)
                while count < stable_mounts_len:
                    current_mount = str(stable_mounts[int(count)])
                    print(" -" + current_stable["stable"]["sells"]["mounts"][int(count)] + " " + COLOR_YELLOW + COLOR_STYLE_BRIGHT + str(round(mounts[current_mount]["gold"] * current_stable["cost value"], 2)) + COLOR_RESET_ALL)
                    count += 1
            if "None" not in current_stable["stable"]["sells"]["items"]:
                options += ['Buy Item']
                print("ITEMS SELLS:")
                count = 0
                stable_items = current_stable["stable"]["sells"]["items"]
                stable_items_len = len(stable_items)
                while count < stable_items_len:
                    current_mount = str(stable_items[int(count)])
                    print(" -" + current_stable["stable"]["sells"]["items"][int(count)] + " " + COLOR_YELLOW + COLOR_STYLE_BRIGHT + str(round(item[current_mount]["gold"] * current_stable["cost value"], 2)) + COLOR_RESET_ALL)
                    count += 1
            print(" ")
            deposited_mounts_num = 0
            count = 0
            mounts_list_len = len(player["mounts"])
            deposited_mounts_names = []
            if "None" not in list(player["mounts"]):
                while count < mounts_list_len:
                        selected_mount = list(player["mounts"])[count]
                        selected_mount = str(selected_mount)
                        if player["mounts"][selected_mount]["location"] == "point" + str(map_location) and player["mounts"][selected_mount]["is deposited"] == True:
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
                print("MOUNTS DEPOSITED HERE: " + COLOR_BLUE + COLOR_STYLE_BRIGHT + str(deposited_mounts_num) + COLOR_RESET_ALL)
            else:
                print("MOUNTS DEPOSITED HERE: " + COLOR_BLUE + COLOR_STYLE_BRIGHT + str(deposited_mounts_num) + COLOR_RESET_ALL + " " + deposited_mounts_names)
            text = '='
            print_separator(text)
        logger_sys.log_message("INFO: Checking if the player is an hostel")
        if zone[map_zone]["type"] == "hostel":
            is_in_hostel = True
            current_hostel = zone[map_zone]
            current_hostel_name = current_hostel["name"]
            logger_sys.log_message(f"INFO: Printing current hostel '{current_hostel_name}' information to GUI")
            print(str(current_hostel["name"]) + ":")
            text = current_hostel["description"]
            print_long_string(text)
            print(" ")
            print("SLEEP COST: " + COLOR_YELLOW + COLOR_STYLE_BRIGHT + str(current_hostel["sleep gold"]) + COLOR_RESET_ALL)
            if "None" not in current_hostel["sells"]["drinks"]:
                print("DRINKS SELLS:")
                count = 0
                hostel_drinks = current_hostel["sells"]["drinks"]
                hostel_drinks_len = len(hostel_drinks)
                while count < hostel_drinks_len:
                    current_drink = str(current_hostel["sells"]["drinks"][int(count)])
                    print(" -" + current_hostel["sells"]["drinks"][int(count)] + " " + COLOR_YELLOW + COLOR_STYLE_BRIGHT + str(round(drinks[current_drink]["gold"] * current_hostel["cost value"], 2)) + COLOR_RESET_ALL)
                    count += 1
            if "None" not in current_hostel["sells"]["items"]:
                print("ITEMS SELLS")
                count = 0
                hostel_items = current_hostel["sells"]["items"]
                hostel_items_len = len(hostel_items)
                while count < hostel_items_len:
                    current_item = str(current_hostel["sells"]["items"][int(count)])
                    print(" -" + current_hostel["sells"]["items"][int(count)] + " " + COLOR_YELLOW + COLOR_STYLE_BRIGHT + str(round(item[current_item]["gold"] * current_hostel["cost value"], 2)) + COLOR_RESET_ALL)
                    count += 1
            if "None" not in current_hostel["buys"]["items"]:
                print("ITEMS BUYS:")
                count = 0
                hostel_items = current_hostel["buys"]["items"]
                hostel_items_len = len(hostel_items)
                while count < hostel_items_len:
                    current_item = str(current_hostel["buys"]["items"][int(count)])
                    print(" -" + current_hostel["buys"]["items"][int(count)] + " " + COLOR_YELLOW + COLOR_STYLE_BRIGHT + str(round(item[current_item]["gold"] * current_hostel["cost value"], 2)) + COLOR_RESET_ALL)
                    count += 1
            text = '='
            print_separator(text)
        print("")
        logger_sys.log_message(f"INFO: Checking if an item is on the ground at map point 'point{map_location}'")
        if "item" in map["point" + str(map_location)] and map_location not in player["taken items"]:
            map_items = str(map["point" + str(map_location)]["item"])
            logger_sys.log_message(f"INFO: Current map point 'point{map_location}' has item '{map_items}'")
            map_items = map_items.replace('[', '')
            map_items = map_items.replace(']', '')
            map_items = map_items.replace("'", '')
            take_item = "There are these items on the ground: " + map_items
            print(take_item)
            print("")
        logger_sys.log_message(f"INFO: Checking if an npc is present at map point 'point{map_location}'")
        if "npc" in map["point" + str(map_location)] and map_location not in player["met npcs"]:
            current_npc = str(map["point" + str(map_location)]["npc"])
            logger_sys.log_message(f"INFO: Current map point 'point{map_location}' has npc: '{current_npc}'")
            current_npc = current_npc.replace('[', '')
            current_npc = current_npc.replace(']', '')
            current_npc = current_npc.replace("'", '')
            logger_sys.log_message(f"INFO: Adding npc '{current_npc}' to player 'met npcs' and 'met npcs names' save attributes")
            player["met npcs"].append(map_location)
            player["met npcs names"].append(str(npcs[current_npc]["name"]))
            print(" ")
            text = '='
            print_separator(text)
            print(str(npcs[current_npc]["name"]) + ":")
            text = '='
            print_separator(text)
            count = 0
            npc_speech = npcs[current_npc]["speech"]
            npc_speech_len = len(npc_speech)
            logger_sys.log_message(f"INFO: Printing npc '{current_npc}' dialog")
            while count < npc_speech_len:
                text = str(npcs[current_npc]["speech"][int(count)])
                print_speech_text_effect(text)
                count += 1
            text = '='
            print_separator(text)
            options = []
            logger_sys.log_message(f"INFO: Display npc '{current_npc}' information to GUI")
            if "None" not in npcs[current_npc]["sells"]["drinks"]:
                print("DRINKS SELLS:")
                count = 0
                npc_drinks = npcs[current_npc]["sells"]["drinks"]
                npc_drinks_len = len(npc_drinks)
                while count < npc_drinks_len:
                    current_drink = str(npcs[current_npc]["sells"]["drinks"][int(count)])
                    print(" -" + npcs[current_npc]["sells"]["drinks"][int(count)] + " " + COLOR_YELLOW + COLOR_STYLE_BRIGHT + str(round(drinks[current_drink]["gold"] * npcs[current_npc]["cost value"], 2)) + COLOR_RESET_ALL)
                    count += 1
                options += ['Buy Drink']
            if "None" not in npcs[current_npc]["sells"]["items"]:
                print("ITEMS SELLS")
                count = 0
                npc_items = npcs[current_npc]["sells"]["items"]
                npc_items_len = len(npc_items)
                while count < npc_items_len:
                    current_item = str(npcs[current_npc]["sells"]["items"][int(count)])
                    print(" -" + npcs[current_npc]["sells"]["items"][int(count)] + " " + COLOR_YELLOW + COLOR_STYLE_BRIGHT + str(round(item[current_item]["gold"] * npcs[current_npc]["cost value"], 2)) + COLOR_RESET_ALL)
                    count += 1
                options += ['Buy Item']
            if "None" not in npcs[current_npc]["buys"]["items"]:
                print("ITEMS BUYS:")
                count = 0
                npc_items = npcs[current_npc]["buys"]["items"]
                npc_items_len = len(npc_items)
                while count < npc_items_len:
                    current_item = str(npcs[current_npc]["buys"]["items"][int(count)])
                    print(" -" + npcs[current_npc]["buys"]["items"][int(count)] + " " + COLOR_YELLOW + COLOR_STYLE_BRIGHT + str(round(item[current_item]["gold"] * npcs[current_npc]["cost value"], 2)) + COLOR_RESET_ALL)
                    count += 1
                options += ['Sell Item']
            options += ['Exit']
            text = '='
            print_separator(text)
            p = True
            while p:
                logger_sys.log_message(f"INFO: Starting player interaction with npc '{current_npc}'")
                choice = term_menu.show_menu(options)
                if choice == 'Buy Drink':
                    which_drink = input("Which drink do you want to buy from him? ")
                    if which_drink in npcs[current_npc]["sells"]["drinks"] and ( drinks[which_drink]["gold"] * npcs[current_npc]["cost value"] ) < player["gold"]:
                        logger_sys.log_message(f"INFO: Player bought drink '{which_drink}' from npc '{current_npc}', causing the player to loose " + str( drinks[which_drink]["gold"] * npcs[current_npc]["cost value"] ) + " gold")
                        remove_gold(str( drinks[which_drink]["gold"] * npcs[current_npc]["cost value"] ))
                        if drinks[which_drink]["healing level"] == 999:
                            player["health"] = player["max health"]
                        else:
                            player["health"] += drinks[which_drink]["healing level"]
                    else:
                        text = COLOR_YELLOW + "You cannot buy that items because it would cause your gold to be negative." + COLOR_RESET_ALL
                        print_long_string(text)
                elif choice == 'Buy Item':
                    which_item = input("Which item do you want to buy from him? ")
                    if which_item in npcs[current_npc]["sells"]["items"] and ( item[which_item]["gold"] * npcs[current_npc]["cost value"] ) < player["gold"]:
                        if player["inventory slots remaining"] > 0:
                            logger_sys.log_message("INFO: Player bought item '{which_item}' from npc '{current_npc}', causing him, to loose " + remove_gold(str( item[which_item]["gold"] * npcs[current_npc]["cost value"] )) + " gold")
                            player["inventory slots remaining"] -= 1
                            player["inventory"].append(which_item)
                            remove_gold(str( item[which_item]["gold"] * npcs[current_npc]["cost value"] ))
                        else:
                            text = COLOR_YELLOW + "You cannot buy that items because it would cause your inventory slots to be negative." + COLOR_RESET_ALL
                            print_long_string(text)
                    else:
                        text = COLOR_YELLOW + "You cannot buy that items because it would cause your gold to be negative." + COLOR_RESET_ALL
                        print_long_string(text)
                elif choice == 'Sell Item':
                    which_item = input("Which item do you want to sell him? ")
                    if which_item in npcs[current_npc]["buys"]["items"] and ( item[which_item]["gold"] * npcs[current_npc]["cost value"] ) < player["gold"] and which_item in player["inventory"]:
                        logger_sys.log_message("INFO: Player has sold item '{witch_item}' to npc '{current_npc}' for " + str( item[which_item]["gold"] * npcs[current_npc]["cost value"] ) + " gold")
                        player["inventory slots remaining"] -= 1
                        add_gold(str( item[which_item]["gold"] * npcs[current_npc]["cost value"] ))
                        player["inventory"].remove(which_item)
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
                            logger_sys.log_message("INFO: Checking if player sold item was equipped")
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
                        text = COLOR_YELLOW + "You cannot buy that items because it would cause your gold to be negative or because you don't own that item." + COLOR_RESET_ALL
                        print_long_string(text)
                else:
                    p = False
                """
                if which_item in npcs[current_npc]["sells"]["drinks"] and drinks[which_item]["gold"] < player["gold"]:
                    remove_gold(str(drinks[which_item]["gold"]))
                    if drinks[which_item]["healing level"] == 999:
                        player["health"] = player["max health"]
                    else:
                        player["health"] += drinks[which_item]["healing level"]
                elif which_item == 'q' or which_item == 'Q':
                    p = False
                else:
                    print("You don't have that item")
                time.sleep(.6)
                os.system('clear')
                """
        logger_sys.log_message(f"INFO: Checking if an enemy at map point 'point{map_location}'")
        if "enemy" in map["point" + str(map_location)] and map_location not in player["defeated enemies"]:
            logger_sys.log_message(f"INFO: Found enemies at map point 'point{map_location}'")
            enemies_remaining = map["point" + str(map_location)]["enemy"]
            already_encountered = False
            while enemies_remaining > 0:
                list_enemies = lists[ map["point" + str(map_location)]["enemy type"]]
                logger_sys.log_message(f"INFO: Choosing random enemy from the list '{list_enemies}'")
                choose_rand_enemy = random.randint(0, len(list_enemies) - 1)
                choose_rand_enemy = list_enemies[choose_rand_enemy]
                choosen_enemy = enemy[choose_rand_enemy]

                enemy_total_inventory = choosen_enemy["inventory"]

                enemy_items_number = len(enemy_total_inventory)
                logger_sys.log_message("INFO: Choosing randomly the item that will drop from the enemies")
                choosen_item = enemy_total_inventory[random.randint(0, enemy_items_number - 1)]
                logger_sys.log_message("INFO: Calculating battle risk for the player")
                defeat_percentage = battle.calculate_player_risk(player, item, enemies_remaining, choosen_enemy, enemy)
                logger_sys.log_message("INFO: Getting enemy stats")
                battle.get_enemy_stats(player, item, enemy, map, map_location, lists, choose_rand_enemy, choosen_enemy, choosen_item, enemy_items_number, enemy_total_inventory, enemies_remaining)
                if not already_encountered:
                    logger_sys.log_message("INFO: Display enemy encounter text")
                    battle.encounter_text_show(player, item, enemy, map, map_location, enemies_remaining, lists, defeat_percentage)
                    already_encountered = True
                logger_sys.log_message("INFO: Starting the fight")
                battle.fight(player, item, enemy, map, map_location, enemies_remaining, lists)
                enemies_remaining -= 1
            # if round(random.uniform(.20, .50), 2) > .35:
            list_enemies = lists[ map["point" + str(map_location)]["enemy type"]]

            if player["health"] > 0:

                if random.randint(0, 3) >= 2.5:
                    choosen_item = "Gold"

                if choosen_item == "Gold":
                    print("Your enemy dropped some " + choosen_item)
                else:
                    print("Your enemy dropped " + a_an_check(choosen_item))
                options = ['Grab Item', 'Continue']
                drop = term_menu.show_menu(options)
                text = '='
                print_separator(text)
                if drop == 'Grab Item':
                    if choosen_item == "Gold":
                        add_gold(round(random.uniform(1.00, 6.30), 2))
                    else:
                        if choosen_item in player["inventory"] and item[choosen_item]["type"] == "Utility":
                            print("You cannot take that item")
                        elif player["inventory slots remaining"] == 0:
                            print("You cannot take that item, you don't have enough slots in your inventory")
                        else:
                            player["inventory"].append(choosen_item)
                print(" ")
                player["defeated enemies"].append(map_location)
            else:
                text = COLOR_RED + COLOR_STYLE_BRIGHT + "You just died and your save have been reseted." + COLOR_RESET_ALL
                logger_sys.log_message("INFO: Player just died")
                print_long_string(text)
                finished = input()
                logger_sys.log_message("INFO: Resetting player save")
                player = start_player
                play = 0
                return play

        elif day_time == COLOR_RED + COLOR_STYLE_BRIGHT + "NIGHT" + COLOR_RESET_ALL and round(random.uniform(.20, .80), 3) > .7 and zone[map_zone]["type"] != "hostel" and zone[map_zone]["type"] != "stable" and zone[map_zone]["type"] != "village" and zone[map_zone]["type"] != "blacksmith" and zone[map_zone]["type"] != "forge":
            logger_sys.log_message("INFO: Checking if it's night time")
            logger_sys.log_message("INFO: Checking if the player isn't in a village, an hostel, a stable, a blacksmith or a forge")
            logger_sys.log_message("INFO: Calculating random chance of enemy spawning")
            logger_sys.log_message("INFO: Spawning enemies")
            enemies_remaining = random.randint(1, 4)
            already_encountered = False
            while enemies_remaining > 0:
                list_enemies = lists["generic"]
                choose_rand_enemy = random.randint(0, len(list_enemies) - 1)
                logger_sys.log_message(f"INFO: Choosing random enemy from the list '{list_enemies}'")
                choose_rand_enemy = list_enemies[choose_rand_enemy]
                choosen_enemy = enemy[choose_rand_enemy]

                enemy_total_inventory = choosen_enemy["inventory"]

                enemy_items_number = len(enemy_total_inventory)
                logger_sys.log_message("INFO: Choosing randomly the item that will drop from the enemies")
                choosen_item = enemy_total_inventory[random.randint(0, enemy_items_number - 1)]
                logger_sys.log_message("INFO: Calculating battle risk for the player")
                defeat_percentage = battle.calculate_player_risk(player, item, enemies_remaining, choosen_enemy, enemy)
                logger_sys.log_message("INFO: Getting enemy stats")
                battle.get_enemy_stats(player, item, enemy, map, map_location, lists, choose_rand_enemy, choosen_enemy, choosen_item, enemy_items_number, enemy_total_inventory, enemies_remaining)
                if not already_encountered:
                    logger_sys.log_message("INFO: Display enemy encounter text")
                    battle.encounter_text_show(player, item, enemy, map, map_location, enemies_remaining, lists, defeat_percentage)
                    already_encountered = True
                logger_sys.log_message("INFO: Starting the fight")
                battle.fight(player, item, enemy, map, map_location, enemies_remaining, lists)
                enemies_remaining -= 1
            # if round(random.uniform(.20, .50), 2) > .35:
            list_enemies = lists["generic"]

            if player["health"] > 0:

                if random.randint(0, 3) >= 2.5:
                    choosen_item = "Gold"

                if choosen_item == "Gold":
                    print("Your enemy dropped some " + choosen_item)
                else:
                    print("Your enemy dropped " + a_an_check(choosen_item))
                options = ['Grab Item', 'Continue']
                drop = term_menu.show_menu(options)
                text = '='
                print_separator(text)
                if drop == 'Grab Item':
                    if choosen_item == "Gold":
                        add_gold(round(random.uniform(1.00, 6.30), 2))
                    else:
                        if choosen_item in player["inventory"] and item[choosen_item]["type"] == "Utility":
                            print("You cannot take that item")
                        elif player["inventory slots remaining"] == 0:
                            print("You cannot take that item, you don't have enough slots in your inventory")
                        else:
                            player["inventory"].append(choosen_item)
                print(" ")
            else:
                text = COLOR_RED + COLOR_STYLE_BRIGHT + "You just died and your save have been reseted." + COLOR_RESET_ALL
                logger_sys.log_message("INFO: Player just died")
                print_long_string(text)
                finished = input()
                logger_sys.log_message("INFO: Resetting player save")
                player = start_player
                play = 0
                return play
        command = input("> ")
        print(" ")
        logger_sys.log_message(f"INFO: Player ran command '{command}'")
        logger_sys.log_message(f"INFO: Checking if a ground item is present at map point 'point{map_location}'")
        if "item" in map["point" + str(map_location)] and command in map["point" + str(map_location)]["item"]:
            logger_sys.log_message(f"INFO: Found item '{command}' at map point 'point{map_location}'")
            if command in player["inventory"] and item[command]["type"] == "Utility":
                print(COLOR_YELLOW + "You cannot take that item." + COLOR_RESET_ALL)
                time.sleep(1.5)
            elif player["inventory slots remaining"] == 0:
                print(COLOR_YELLOW + "You cannot take that item because you're out of inventory slots." + COLOR_RESET_ALL)
                time.sleep(1.5)
            else:
                logger_sys.log_message(f"INFO: Adding item '{command}' to player inventory")
                logger_sys.log_message(f"INFO: Adding map point 'point{map_location}' to the player save attribute 'taken items'")
                player["inventory"].append(command)
                player["taken items"].append(map_location)
        elif command.lower().startswith('go'):
            print(COLOR_YELLOW + "Rather than saying Go <direction>, simply say <direction>." + COLOR_RESET_ALL)
            time.sleep(1.5)
        elif command.lower().startswith('n'):
            logger_sys.log_message(f"INFO: Checking if player can go north from map point 'point{map_location}'")
            next_point = search(player["x"], player["y"] + 1)
            if "North" in map["point" + str(map_location)]["blocked"]:
                print(COLOR_YELLOW + "You cannot go that way." + COLOR_RESET_ALL)
                logger_sys.log_message(f"INFO: Refusing access to north: access blocked to map point 'point{next_point}'")
                time.sleep(1)
            elif "key" in map["point" + str(next_point)]:
                logger_sys.log_message(f"INFO: Checking if a key is required for going north at map point 'point{next_point}'")
                check_for_key("north")
            else:
                logger_sys.log_message(f"INFO: Moving player north to map point 'point{next_point}': successful checks")
                player["y"] += 1
        elif command.lower().startswith('s'):
            logger_sys.log_message(f"INFO: Checking if player can go south from map point 'point{map_location}'")
            next_point = search(player["x"], player["y"] - 1)
            if "South" in map["point" + str(map_location)]["blocked"]:
                print(COLOR_YELLOW + "You cannot go that way." + COLOR_RESET_ALL)
                logger_sys.log_message(f"INFO: Refusing access to south: access blocked to map point 'point{next_point}'")
                time.sleep(1)
            elif "key" in map["point" + str(next_point)]:
                logger_sys.log_message(f"INFO: Checking if a key is required for going south at map point 'point{next_point}'")
                check_for_key("south")
            else:
                logger_sys.log_message(f"INFO: Moving player south to map point 'point{next_point}': successful checks")
                player["y"] -= 1
        elif command.lower().startswith('e'):
            logger_sys.log_message(f"INFO: Checking if player can go east from map point 'point{map_location}'")
            next_point = search(player["x"] + 1, player["y"])
            if "East" in map["point" + str(map_location)]["blocked"]:
                print(COLOR_YELLOW + "You cannot go that way." + COLOR_RESET_ALL)
                logger_sys.log_message(f"INFO: Refusing access to east: access blocked to map point 'point{next_point}'")
                time.sleep(1)
            elif "key" in map["point" + str(next_point)]:
                logger_sys.log_message(f"INFO: Checking if a key is required for going east at map point 'point{next_point}'")
                check_for_key("east")
            else:
                logger_sys.log_message(f"INFO: Moving player east to map point 'point{next_point}': successful checks")
                player["x"] += 1
        elif command.lower().startswith('w'):
            logger_sys.log_message(f"INFO: Checking if player can go west from map point 'point{map_location}'")
            next_point = search(player["x"] - 1, player["y"])
            if "West" in map["point" + str(map_location)]["blocked"]:
                print(COLOR_YELLOW + "You cannot go that way." + COLOR_RESET_ALL)
                logger_sys.log_message(f"INFO: Refusing access to west: access blocked to map point 'point{next_point}'")
                time.sleep(1)
            elif "key" in map["point" + str(next_point)]:
                logger_sys.log_message(f"INFO: Checking if a key is required for going west at map point 'point{next_point}'")
                check_for_key("west")
            else:
                logger_sys.log_message(f"INFO: Moving player west to map point 'point{next_point}': successful checks")
                player["x"] -= 1
        elif command.lower().startswith('d'):
            text = '='
            print_separator(text)
            logger_sys.log_message("INFO: Displaying player diary menu")
            print("ADVENTURER NAME: " + str(preferences["latest preset"]["save"]))
            print("ELAPSED DAYS: " + COLOR_STYLE_BRIGHT + COLOR_MAGENTA + str(round(player["elapsed time game days"], 1)) + COLOR_RESET_ALL)
            text = '='
            print_separator(text)
            options = ['Visited Places', 'Encountered Monsters', 'Encountered People']
            choice = term_menu.show_menu(options)
            logger_sys.log_message(f"INFO: Playing has choosen option '{choice}'")
            if choice == 'Visited Places':
                print("VISITED PLACES: ")
                zones_list = str(player["visited zones"])
                logger_sys.log_message(f"INFO: Printing player visited places '{zones_list}'")
                zones_list = zones_list.replace("'", '')
                zones_list = zones_list.replace("[", ' -')
                zones_list = zones_list.replace("]", '')
                zones_list = zones_list.replace(", ", '\n -')
                print(zones_list)
                text = '='
                print_separator(text)
                which_zone = input("> ")
                logger_sys.log_message(f"INFO: Player has choosen zone '{which_zone}' to check")
                if which_zone in player["visited zones"]:
                    logger_sys.log_message(f"INFO: Printing zone '{which_zone}' information to GUI")
                    text = '='
                    print_separator(text)
                    print_zone_map_alone(which_zone)
                    print("NAME: " + zone[which_zone]["name"])
                    if zone[which_zone]["type"] == "village":
                        village_point = zone[which_zone]["location"]
                        village_coordinates = "(" + COLOR_GREEN + COLOR_STYLE_BRIGHT + str(map["point" + str(village_point)]["x"]) + COLOR_RESET_ALL + ", " + COLOR_GREEN + COLOR_STYLE_BRIGHT + str(map["point" + str(village_point)]["y"]) + COLOR_RESET_ALL + ")"
                        print("LOCATION: " + village_coordinates)
                        content_hostels = str(zone[which_zone]["content"]["hostels"])
                        content_hostels = content_hostels.replace('[', '')
                        content_hostels = content_hostels.replace(']', '')
                        content_hostels = content_hostels.replace("'", '')
                        text = "HOSTELS: " + content_hostels
                        print_long_string(text)
                        content_blacksmiths = str(zone[which_zone]["content"]["blacksmiths"])
                        content_blacksmiths = content_blacksmiths.replace('[', '')
                        content_blacksmiths = content_blacksmiths.replace(']', '')
                        content_blacksmiths = content_blacksmiths.replace("'", '')
                        text = "BLACKSMITHS: " + content_blacksmiths
                        print_long_string(text)
                    elif zone[which_zone]["type"] == "hostel":
                        current_hostel = zone[which_zone]
                        hostel_point = zone[which_zone]["location"]
                        hostel_coordinates = "(" + COLOR_GREEN + COLOR_STYLE_BRIGHT + str(map["point" + str(hostel_point)]["x"]) + COLOR_RESET_ALL + ", " + COLOR_GREEN + COLOR_STYLE_BRIGHT + str(map["point" + str(hostel_point)]["y"]) + COLOR_RESET_ALL + ")"
                        print("LOCATION: " + hostel_coordinates)
                        print("SLEEP COST: " + COLOR_YELLOW + COLOR_STYLE_BRIGHT + str(current_hostel["sleep gold"]) + COLOR_RESET_ALL)
                        if "None" not in current_hostel["sells"]["drinks"]:
                            print("DRINKS SELLS:")
                            count = 0
                            hostel_drinks = current_hostel["sells"]["drinks"]
                            hostel_drinks_len = len(hostel_drinks)
                            while count < hostel_drinks_len:
                                current_drink = str(current_hostel["sells"]["drinks"][int(count)])
                                print(" -" + current_hostel["sells"]["drinks"][int(count)] + " " + COLOR_YELLOW + COLOR_STYLE_BRIGHT + str(round(drinks[current_drink]["gold"] * current_hostel["cost value"], 2)) + COLOR_RESET_ALL)
                                count += 1
                        if "None" not in current_hostel["sells"]["items"]:
                            print("ITEMS SELLS")
                            count = 0
                            hostel_items = current_hostel["sells"]["items"]
                            hostel_items_len = len(hostel_items)
                            while count < hostel_items_len:
                                current_item = str(current_hostel["sells"]["items"][int(count)])
                                print(" -" + current_hostel["sells"]["items"][int(count)] + " " + COLOR_YELLOW + COLOR_STYLE_BRIGHT + str(round(item[current_item]["gold"] * current_hostel["cost value"], 2)) + COLOR_RESET_ALL)
                                count += 1
                        if "None" not in current_hostel["buys"]["items"]:
                            print("ITEMS BUYS:")
                            count = 0
                            hostel_items = current_hostel["buys"]["items"]
                            hostel_items_len = len(hostel_items)
                            while count < hostel_items_len:
                                current_item = str(current_hostel["buys"]["items"][int(count)])
                                print(" -" + current_hostel["buys"]["items"][int(count)] + " " + COLOR_YELLOW + COLOR_STYLE_BRIGHT + str(round(item[current_item]["gold"] * current_hostel["cost value"], 2)) + COLOR_RESET_ALL)
                                count += 1
                    elif zone[which_zone]["type"] == "stable":
                        current_stable = zone[which_zone]
                        stable_point = zone[which_zone]["location"]
                        stable_coordinates = "(" + COLOR_GREEN + COLOR_STYLE_BRIGHT + str(map["point" + str(stable_point)]["x"]) + COLOR_RESET_ALL + ", " + COLOR_GREEN + COLOR_STYLE_BRIGHT + str(map["point" + str(stable_point)]["y"]) + COLOR_RESET_ALL + ")"
                        print("LOCATION: " + stable_coordinates)
                        print("DEPOSIT COST/DAY: " + COLOR_YELLOW + COLOR_STYLE_BRIGHT + str(current_stable["deposit gold"]) + COLOR_RESET_ALL)
                        print("TRAINING COST/DAY: " + COLOR_YELLOW + COLOR_STYLE_BRIGHT + str(current_stable["training gold"]) + COLOR_RESET_ALL)
                        options = ['Train Mount', '']
                        if "None" not in current_stable["stable"]["sells"]["mounts"]:
                            print("MOUNTS SELLS:")
                            count = 0
                            stable_mounts = current_stable["stable"]["sells"]["mounts"]
                            stable_mounts_len = len(stable_mounts)
                            while count < stable_mounts_len:
                                current_mount = str(current_stable["stable"]["sells"]["mounts"][int(count)])
                                print(" -" + current_stable["stable"]["sells"]["mounts"][int(count)] + " " + COLOR_YELLOW + COLOR_STYLE_BRIGHT + str(round(mounts[current_mount]["gold"] * current_stable["cost value"], 2)) + COLOR_RESET_ALL)
                                count += 1
                        if "None" not in current_stable["stable"]["sells"]["items"]:
                            options += ['Buy Item']
                            print("ITEMS SELLS:")
                            count = 0
                            stable_items = current_stable["stable"]["sells"]["items"]
                            stable_items_len = len(stable_items)
                            while count < stable_items_len:
                                current_mount = str(current_stable["stable"]["sells"]["items"][int(count)])
                                print(" -" + current_stable["stable"]["sells"]["items"][int(count)] + " " + COLOR_YELLOW + COLOR_STYLE_BRIGHT + str(round(item[current_mount]["gold"] * current_stable["cost value"], 2)) + COLOR_RESET_ALL)
                                count += 1
                        deposited_mounts_num = 0
                        count = 0
                        mounts_list_len = len(player["mounts"])
                        deposited_mounts_names = []
                        if "None" not in list(player["mounts"]):
                            while count < mounts_list_len:
                                    selected_mount = list(player["mounts"])[count]
                                    selected_mount = str(selected_mount)
                                    if player["mounts"][selected_mount]["location"] == "point" + str(map_location) and player["mounts"][selected_mount]["is deposited"] == True:
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
                            print("MOUNTS DEPOSITED HERE: " + COLOR_BLUE + COLOR_STYLE_BRIGHT + str(deposited_mounts_num) + COLOR_RESET_ALL)
                        else:
                            print("MOUNTS DEPOSITED HERE: " + COLOR_BLUE + COLOR_STYLE_BRIGHT + str(deposited_mounts_num) + COLOR_RESET_ALL + " " + deposited_mounts_names)
                    elif zone[which_zone]["type"] == "blacksmith":
                        current_black_smith = zone[which_zone]
                        blacksmith_point = zone[which_zone]["location"]
                        black_smith_coordinates = "(" + COLOR_GREEN + COLOR_STYLE_BRIGHT + str(map["point" + str(blacksmith_point)]["x"]) + COLOR_RESET_ALL + ", " + COLOR_GREEN + COLOR_STYLE_BRIGHT + str(map["point" + str(blacksmith_point)]["y"]) + COLOR_RESET_ALL + ")"
                        print("LOCATION: " + black_smith_coordinates)
                        if "None" not in current_black_smith["blacksmith"]["buys"]:
                            print("EQUIPMENT BUYS:")
                            count = 0
                            weapon_buys = current_black_smith["blacksmith"]["buys"]
                            weapon_buys_len = len(weapon_buys)
                            while count < weapon_buys_len:
                                current_weapon = str(current_black_smith["blacksmith"]["buys"][int(count)])
                                print(" -" + current_weapon + " " + COLOR_YELLOW + COLOR_STYLE_BRIGHT + str(round(item[current_weapon]["gold"] * current_black_smith["cost value"], 2)) + COLOR_RESET_ALL)
                                count += 1
                        if "None" not in current_black_smith["blacksmith"]["orders"]:
                            print("WEAPON ORDERS:")
                            count = 0
                            weapon_orders = current_black_smith["blacksmith"]["orders"]
                            weapon_orders_len = len(weapon_orders)
                            while count < weapon_orders_len:
                                current_weapon = str(list(current_black_smith["blacksmith"]["orders"])[int(count)])
                                current_weapon_materials = current_black_smith["blacksmith"]["orders"][current_weapon]["needed materials"]
                                count2 = 0
                                global_current_weapon_materials = []
                                current_weapon_materials_num = len(current_weapon_materials)
                                while count2 < current_weapon_materials_num:
                                    current_material = current_weapon_materials[count2]

                                    global_current_weapon_materials += [current_material]

                                    count2 += 1

                                count2 = 0
                                count3 = 0

                                while count2 < len(global_current_weapon_materials):
                                    current_material = global_current_weapon_materials[count2]
                                    current_material_number = str(global_current_weapon_materials.count(current_material))

                                    if global_current_weapon_materials.count(current_material) > 1:
                                        while count3 < global_current_weapon_materials.count(current_material):
                                            global_current_weapon_materials.remove(current_material)
                                            count3 += 1
                                        global_current_weapon_materials = [sub.replace(current_material, current_material + "X" + current_material_number) for sub in global_current_weapon_materials]

                                    count2 += 1

                                global_current_weapon_materials = str(global_current_weapon_materials)
                                global_current_weapon_materials = global_current_weapon_materials.replace("'", '')
                                global_current_weapon_materials = global_current_weapon_materials.replace("[", '')
                                global_current_weapon_materials = global_current_weapon_materials.replace("]", '')
                                print(" -" + current_weapon + " " + COLOR_YELLOW + COLOR_STYLE_BRIGHT + str(round(item[current_weapon]["gold"] * current_black_smith["cost value"], 2)) + COLOR_RESET_ALL + COLOR_GREEN + COLOR_STYLE_BRIGHT + " (" + COLOR_RESET_ALL + global_current_weapon_materials + COLOR_GREEN + COLOR_STYLE_BRIGHT + ")" + COLOR_RESET_ALL)
                                count += 1
                    elif zone[which_zone]["type"] == "forge":
                        current_forge = zone[which_zone]
                        print(str(current_forge["name"]) + ":")
                        text = current_forge["description"]
                        print_long_string(text)
                        print(" ")
                        if "None" not in current_forge["forge"]["buys"]:
                            print("METAL BUYS:")
                            count = 0
                            metal_buys = current_forge["forge"]["buys"]
                            metal_buys_len = len(metal_buys)
                            while count < metal_buys_len:
                                current_metal = str(metal_buys[count])
                                print(" -" + current_metal + " " + COLOR_YELLOW + COLOR_STYLE_BRIGHT + str(round(item[current_metal]["gold"] * current_forge["cost value"], 2)) + COLOR_RESET_ALL)
                                count += 1
                        if "None" not in current_forge["forge"]["sells"]:
                            print("METAL SELLS:")
                            count = 0
                            metal_sells = current_forge["forge"]["sells"]
                            metal_sells_len = len(metal_sells)
                            while count < metal_sells_len:
                                current_metal = str(metal_sells[count])
                                print(" -" + current_metal + " " + COLOR_YELLOW + COLOR_STYLE_BRIGHT + str(round(item[current_metal]["gold"] * current_forge["cost value"], 2)) + COLOR_RESET_ALL)
                                count += 1
                    text = "DESCRIPTION: " + zone[which_zone]["description"]
                    print_long_string(text)
                    text = '='
                    print_separator(text)
                else:
                    print(" ")
                    print(COLOR_YELLOW + "You don't know about that place" + COLOR_RESET_ALL)
                    logger_sys.log_message(f"INFO: Player has choosen '{which_zone}', which he doesn't know about --> canceling")
                finished = input("")
            elif choice == 'Encountered Monsters':
                print("ENCOUNTERED MONSTERS: ")
                enemies_list = str(player["enemies list"])
                logger_sys.log_message(f"INFO: Printing player known enemies: '{enemies_list}'")
                enemies_list = enemies_list.replace("'None', ", '')
                enemies_list = enemies_list.replace("'", '')
                enemies_list = enemies_list.replace("[", ' -')
                enemies_list = enemies_list.replace("]", '')
                enemies_list = enemies_list.replace(", ", '\n -')
                print(enemies_list)
                text = '='
                print_separator(text)
                which_enemy = input("> ")
                logger_sys.log_message(f"INFO: Player has choosen enemy '{which_enemy}' to display information")
                if which_enemy == "None":
                    print(" ")
                    print(COLOR_YELLOW + "You don't know about that enemy." + COLOR_RESET_ALL)
                    time.sleep(1.5)
                elif which_enemy in player["enemies list"]:
                    logger_sys.log_message(f"INFO: Printing enemy '{which_enemy}' information")

                    text = '='
                    print_separator(text)

                    print_enemy_thumbnail(which_enemy)
                    print(" ")

                    print("NAME: " + which_enemy)

                    print("PLURAL: " + enemy[which_enemy]["plural"])
                    enemy_average_damage = ( enemy[which_enemy]["damage"]["min damage"] + enemy[which_enemy]["damage"]["max damage"] ) / 2
                    enemy_average_health = ( enemy[which_enemy]["health"]["min spawning health"] + enemy[which_enemy]["health"]["max spawning health"] ) / 2
                    print("AVERAGE DAMAGE: " + COLOR_STYLE_BRIGHT + COLOR_CYAN + str(enemy_average_damage) + COLOR_RESET_ALL)
                    print("AVERAGE HEALTH: " + COLOR_STYLE_BRIGHT + COLOR_RED + str(enemy_average_health) + COLOR_RESET_ALL)
                    print("AGILITY: " + COLOR_STYLE_BRIGHT + COLOR_MAGENTA + str(enemy[which_enemy]["agility"]) + COLOR_RESET_ALL)

                    # drops
                    enemy_drops = str(enemy[which_enemy]["inventory"])
                    enemy_drops = enemy_drops.replace('[', '')
                    enemy_drops = enemy_drops.replace(']', '')
                    enemy_drops = enemy_drops.replace("'", '')
                    text = "DROPS: " + str(enemy_drops)
                    print_long_string(text)

                    text = "DESCRIPTION: " + enemy[which_enemy]["description"]
                    print_long_string(text)
                    text = '='
                    print_separator(text)
                    finished = input("")
                else:
                    logger_sys.log_message(f"INFO: Player doesn't know about enemy '{which_enemy}' --> canceling")
                    print(" ")
                    print(COLOR_YELLOW + "You don't know about that enemy." + COLOR_RESET_ALL)
                    time.sleep(1.5)
            elif choice == 'Encountered People':
                print("ENCOUNTERED PEOPLE: ")
                enemies_list = str(player["met npcs names"])
                logger_sys.log_message(f"INFO: Printing player encounter people: '{enemies_list}'")
                enemies_list = enemies_list.replace("'None', ", '')
                enemies_list = enemies_list.replace("'", '')
                enemies_list = enemies_list.replace("[", ' -')
                enemies_list = enemies_list.replace("]", '')
                enemies_list = enemies_list.replace(", ", '\n -')
                print(enemies_list)
                text = '='
                print_separator(text)
                which_npc = input("> ")
                logger_sys.log_message(f"INFO: Player has choosen npc '{which_npc}' to display information about")
                if which_npc == "None":
                    print(" ")
                    print(COLOR_YELLOW + "You don't know about that people." + COLOR_RESET_ALL)
                    time.sleep(1.5)
                elif which_npc in player["met npcs names"]:
                    logger_sys.log_message(f"INFO: Printing npc '{which_npc}' information")

                    text = '='
                    print_separator(text)

                    print_npc_thumbnail(which_npc)
                    print(" ")

                    print("NAME: " + which_npc)


                    print("COST VALUE: " + COLOR_YELLOW + COLOR_STYLE_BRIGHT  + str(npcs[which_npc]["cost value"]) + COLOR_RESET_ALL)
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
                    print(" ")
                    print("SELLS:")
                    text = "DRINKS: " + sells_list_drinks
                    print_long_string(text)
                    text = "ITEMS: " + sells_list_items
                    print_long_string(text)
                    print(" ")
                    print("BUYS:")
                    text = "ITEMS: " + buys_list
                    print_long_string(text)

                    text = "DESCRIPTION: " + npcs[which_npc]["description"]
                    print_long_string(text)
                    text = '='
                    print_separator(text)
                    finished = input("")
                else:
                    print(" ")
                    print(COLOR_YELLOW + "You don't know about that enemy." + COLOR_RESET_ALL)
                    logger_sys.log_message(f"INFO: Player doesn't know about npc '{which_npc}' --> canceling")
                    time.sleep(1.5)
        elif command.lower().startswith('i'):
            text = '='
            print_separator(text)
            logger_sys.log_message(f"INFO: Printing player armor protection, agility and critical hit chance stats")
            print("ARMOR PROTECTION: " + COLOR_GREEN + COLOR_STYLE_BRIGHT + str(player["armor protection"]) + COLOR_RESET_ALL + COLOR_RED + COLOR_STYLE_BRIGHT + " (" + COLOR_RESET_ALL + "More it's higher, the less you'll take damages in fights" + COLOR_RED + COLOR_STYLE_BRIGHT + ")" + COLOR_RESET_ALL)
            print("AGILITY: " + COLOR_MAGENTA + COLOR_STYLE_BRIGHT + str(player["agility"]) + COLOR_RESET_ALL + COLOR_RED + COLOR_STYLE_BRIGHT + " (" + COLOR_RESET_ALL + "More it's higher, the more you'll have a chance to dodge attacks" + COLOR_RED + COLOR_STYLE_BRIGHT + ")" + COLOR_RESET_ALL)
            if player["held item"] != " ":
                print("CRITICAL HIT CHANCE: " + COLOR_CYAN + COLOR_STYLE_BRIGHT + str(item[player["held item"]]["critical hit chance"]) + COLOR_RESET_ALL + COLOR_RED + COLOR_STYLE_BRIGHT + " (" + COLOR_RESET_ALL + "More it's higher, the more you'll have a chance to deal critical attacks" + COLOR_RED + COLOR_STYLE_BRIGHT + ")" + COLOR_RESET_ALL)
            print(" ")
            logger_sys.log_message("INFO: Printing player equipped items")
            # equipment
            if player["held item"] != " ":
                print("HELD WEAPON: " + COLOR_RED + COLOR_STYLE_BRIGHT + player["held item"] + COLOR_RESET_ALL)
            if player["held chestplate"] != " ":
                print("WORN CHESTPLATE: " + COLOR_RED + COLOR_STYLE_BRIGHT + player["held chestplate"] + COLOR_RESET_ALL)
            if player["held leggings"] != " ":
                print("WORN LEGGINGS: " + COLOR_RED + COLOR_STYLE_BRIGHT + player["held leggings"] + COLOR_RESET_ALL)
            if player["held boots"] != " ":
                print("WORN BOOTS: " + COLOR_RED + COLOR_STYLE_BRIGHT + player["held boots"] + COLOR_RESET_ALL)
            if player["held shield"] != " ":
                print("HELD SHIELD: " + COLOR_RED + COLOR_STYLE_BRIGHT + player["held shield"] + COLOR_RESET_ALL)
            player_inventory = str(player["inventory"])
            logger_sys.log_message(f"INFO: Printing player inventory: '{player_inventory}'")
            player_inventory = player_inventory.replace("'", '')
            player_inventory = player_inventory.replace("[", ' -')
            player_inventory = player_inventory.replace("]", '')
            player_inventory = player_inventory.replace(", ", '\n -')
            text = '='
            print_separator(text)
            print("INVENTORY:")
            print(player_inventory)
            text = '='
            print_separator(text)
            which_item = input("> ")
            logger_sys.log_message(f"INFO: Player has choosen item '{which_item}' to display information about")
            if which_item in player["inventory"]:
                text = '='
                print_separator(text)
                logger_sys.log_message(f"INFO: Printing item '{which_item}' information")
                if item[which_item]["type"] == "Weapon":
                    print("NAME: " + item[which_item]["display name"])
                else:
                    print("NAME: " + which_item)
                print("TYPE: " + item[which_item]["type"])
                text = "DESCRIPTION: " + item[which_item]["description"]
                print_long_string(text)
                if item[which_item]["type"] == "Armor Piece: Chestplate" or item[which_item]["type"] == "Armor Piece: Boots" or item[which_item]["type"] == "Armor Piece: Leggings" or item[which_item]["type"] == "Armor Piece: Shield":
                    text = "             Armor pieces can protect you in fights, more the armor protection is higher, the more it protects you."
                    print_long_string(text)
                    item_next_upgrade = detect_weapon_next_upgrade_items(which_item)
                    print("UPGRADE TIER: " + COLOR_GREEN + COLOR_STYLE_BRIGHT + str(item[which_item]["upgrade tier"]) + COLOR_RESET_ALL + "/" + str(check_weapon_max_upgrade(str(which_item))))
                    print("ITEMS FOR NEXT UPGRADE:\n" + str(item_next_upgrade))
                    print("ARMOR PROTECTION: " + COLOR_GREEN + COLOR_STYLE_BRIGHT + str(item[which_item]["armor protection"]) + COLOR_RESET_ALL)
                if item[which_item]["type"] == "Metal":
                    text = "              Metals are items that you buy in village forges that you often use to order weapons in blacksmith."
                if item[which_item]["type"] == "Primary Material":
                    text = "              Primary materials are items that you can find naturally but that you can also buy from many villages shops."
                    print_long_string(text)
                if item[which_item]["type"] == "Weapon":
                    item_next_upgrade = detect_weapon_next_upgrade_items(which_item)
                    print("UPGRADE TIER: " + COLOR_GREEN + COLOR_STYLE_BRIGHT + str(item[which_item]["upgrade tier"]) + COLOR_RESET_ALL + "/" + str(check_weapon_max_upgrade(str(which_item))))
                    print("ITEMS FOR NEXT UPGRADE:\n" + str(item_next_upgrade))
                    print("DAMAGE: " + COLOR_CYAN + COLOR_STYLE_BRIGHT + str(item[which_item]["damage"]) + COLOR_RESET_ALL)
                    print("DEFENSE: " + COLOR_CYAN + COLOR_STYLE_BRIGHT + str(item[which_item]["defend"]) + COLOR_RESET_ALL)
                    print("CRITICAL HIT CHANCE: " + COLOR_MAGENTA + COLOR_STYLE_BRIGHT + str(item[which_item]["critical hit chance"]) + COLOR_RESET_ALL)
                if item[which_item]["type"] == "Consumable" or item[which_item]["type"] == "Food":
                    print("HEALTH BONUS: " + COLOR_STYLE_BRIGHT + COLOR_YELLOW  + str(item[which_item]["max bonus"]) + COLOR_RESET_ALL)
                    print("HEALING: " + COLOR_STYLE_BRIGHT + COLOR_MAGENTA + str(item[which_item]["healing level"]) + COLOR_RESET_ALL)
                text = '='
                print_separator(text)
                if str(item[which_item]["type"]) == 'Armor Piece: Chestplate' or str(item[which_item]["type"]) == 'Weapon' or str(item[which_item]["type"]) == 'Armor Piece: Leggings' or str(item[which_item]["type"]) == 'Armor Piece: Boots' or str(item[which_item]["type"]) == 'Armor Piece: Shield':
                    options = ['Equip', 'Get Rid', 'Exit']
                elif str(item[which_item]["type"]) == 'Consumable' or str(item[which_item]["type"]) == 'Food':
                    options = ['Consume', 'Get Rid', 'Exit']
                else:
                    options = ['Get Rid', 'Exit']
                choice = term_menu.show_menu(options)
                logger_sys.log_message(f"INFO: Player has choosen option '{choice}'")
                if choice == 'Equip':
                    if item[which_item]["type"] == "Weapon":
                        logger_sys.log_message(f"INFO: Equiped item '{which_item}' as a weapon")
                        player["held item"] = which_item
                    elif item[which_item]["type"] == "Armor Piece: Chestplate":
                        logger_sys.log_message(f"INFO: Equiped item '{which_item}' as a chestplate")
                        player["held chestplate"] = which_item
                    elif item[which_item]["type"] == "Armor Piece: Leggings":
                        logger_sys.log_message(f"INFO: Equiped item '{which_item}' as leggings")
                        player["held leggings"] = which_item
                    elif item[which_item]["type"] == "Armor Piece: Boots":
                        logger_sys.log_message(f"INFO: Equiped item '{which_item}' as boots")
                        player["held boots"] = which_item
                    elif item[which_item]["type"] == "Armor Piece: Shield":
                        logger_sys.log_message(f"INFO: Equiped item '{which_item}' as a shield")
                        player["held shield"] = which_item
                    else:
                        logger_sys.log_message(f"INFO: Cannot equip item '{which_item}' --> not an item you can equip")
                elif choice == 'Consume':
                    if item[which_item]["healing level"] == 999:
                        player["health"] = player["max health"]
                        logger_sys.log_message(f"INFO: Consuming item '{which_item}' --> restoring full player health")
                    else:
                        healing_level = item[which_item]["healing level"]
                        health_bonus = item[which_item]["max bonus"]
                        logger_sys.log_message(f"INFO: Consuming item '{which_item}' --> restoring {healing_level} hp and adding {health_bonus} to player max health as a bonus")
                        player["health"] += item[which_item]["healing level"]
                        player["max health"] += item[which_item]["max bonus"]
                    player["inventory"].remove(which_item)
                elif choice == 'Get Rid':
                    text = "You won't be able to get this item back if your throw it away. Are you sure you want to throw away this item"
                    print_long_string(text)
                    ask = input("? (y/n) ")
                    if ask.lower().startswith('y'):
                        logger_sys.log_message(f"INFO: Getting rid of item '{which_item}'")
                        if item[which_item]["type"] == "Bag":
                            if ( player["inventory slots remaining"] - item[which_item]["inventory slots"] ) < 0:
                                text = COLOR_YELLOW + "You cannot throw that item because it would cause your remaining inventory slots to be negative" + COLOR_RESET_ALL
                                print_long_string(text)
                                time.sleep(1.5)
                                print(" ")
                        else:
                            player["inventory"].remove(which_item)
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
                logger_sys.log_message(f"INFO: Canceling item action --> player doesn't own item '{which_item}'")
                print(COLOR_YELLOW + "You do not have that item." + COLOR_RESET_ALL)
                time.sleep(1.5)
        elif command.lower().startswith('z'):
            logger_sys.log_message(f"INFO: Trying to interact with current zone '{map_zone}'")
            if zone[map_zone]["type"] == "hostel":
                logger_sys.log_message(f"INFO: Current map zone '{map_zone}' is an hostel --> can interact")
                text = '='
                print_separator(text)
                logger_sys.log_message(f"INFO: Adding correct interactions options depending on the hostel '{map_zone}' capabilities")
                options = ['Sleep']
                if "None" not in zone[map_zone]["sells"]["drinks"]:
                    options += ['Buy Drink']
                if "None" not in zone[map_zone]["sells"]["items"]:
                    options += ['Buy Item']
                if "None" not in zone[map_zone]["buys"]["items"]:
                    options += ['Sell Item']
                options += ['Exit']
                continue_hostel_actions = True
                logger_sys.log_message("INFO: Starting loop of hostel actions")
                while continue_hostel_actions:
                    choice = term_menu.show_menu(options)
                    logger_sys.log_message(f"INFO: Player has choosen option '{choice}'")
                    if choice == 'Sleep':
                        print("Are you sure you want to spend the night here? It will ")
                        ask = input("cost you " + str(zone[map_zone]["sleep gold"]) + " gold (y/n) ")
                        text = '='
                        print_separator(text)
                        if ask.lower().startswith('y'):
                            logger_sys.log_message("INFO: Starting player sleeping process")
                            if int(player["gold"]) > int(zone[map_zone]["sleep gold"]):
                                sleep_gold = int(zone[map_zone]["sleep gold"])
                                logger_sys.log_message(f"INFO: Removed {sleep_gold} from player --> sleep costs")
                                remove_gold(int(zone[map_zone]["sleep gold"]))
                                loading = 7
                                print(" ")
                                while loading > 0:
                                    print("Sleeping... Zzz", end='\r')
                                    time.sleep(.25)
                                    print("Sleeping... zZz", end='\r')
                                    time.sleep(.25)
                                    print("Sleeping... zzZ", end='\r')
                                    time.sleep(.25)
                                    print("Sleeping... zzz", end='\r')
                                    time.sleep(.25)
                                    print("Sleeping... Zzz", end='\r')
                                    time.sleep(.25)
                                    print("Sleeping... zZz", end='\r')
                                    time.sleep(.25)
                                    print("Sleeping... zzZ", end='\r')
                                    time.sleep(.25)
                                    print("Sleeping... zzz", end='\r')
                                    time.sleep(.25)
                                    player["health"] += random.randint(1, 7)
                                    loading -= 1
                                logger_sys.log_message("INFO: Finished sleeping process")
                                logger_sys.log_message("INFO: Updating correct day time to morning")
                                day_time = float( float(round(player["elapsed time game days"] + 1, 0)) + .25 )
                                player["elapsed time game days"] = float( float(round(player["elapsed time game days"] + 1, 0)) + .25 )
                                continue_hostel_actions = False
                                if player["health"] > player["max health"]:
                                    player["health"] = player["max health"]
                            else:
                                logger_sys.log_message("INFO: Canceling sleeping process --> player doesn't own enough gold")
                                print(COLOR_YELLOW + "You don't own enough gold to sleep here." + COLOR_RESET_ALL)
                    elif choice == 'Buy Drink':
                        which_drink = input("Which drink do you want to buy? ")
                        logger_sys.log_message(f"INFO: Player has choosen drink '{which_drink}' to drink")
                        if which_drink in zone[map_zone]["sells"]["drinks"] and ( drinks[which_drink]["gold"] * zone[map_zone]["cost value"] ) < player["gold"]:
                            drink_cost = str( drinks[which_drink]["gold"] * zone[map_zone]["cost value"] )
                            logger_sys.log_message(f"INFO: Buying drink '{which_drink}' --> removed {drink_cost} gold from player")
                            remove_gold(str( drinks[which_drink]["gold"] * zone[map_zone]["cost value"] ))
                            if drinks[which_drink]["healing level"] == 999:
                                logger_sys.log_message("INFO: Healed player to max health")
                                player["health"] = player["max health"]
                            else:
                                healing_level = drinks[which_drink]["healing level"]
                                logger_sys.log_message(f"INFO: Healed player {healing_level} hp")
                                player["health"] += drinks[which_drink]["healing level"]
                        else:
                            text = COLOR_YELLOW + "You cannot buy that items because it would cause your gold to be negative." + COLOR_RESET_ALL
                            logger_sys.log_message(f"INFO: Canceling buying process of drink '{which_drink}' --> doesn't have enough gold")
                            print_long_string(text)
                    elif choice == 'Buy Item':
                        which_item = input("Which item do you want to buy? ")
                        logger_sys.log_message(f"INFO: Player has choosen item '{which_item}' to buy")
                        if which_item in zone[map_zone]["sells"]["items"] and ( item[which_item]["gold"] * zone[map_zone]["cost value"] ) < player["gold"]:
                            if player["inventory slots remaining"] > 0:
                                player["inventory slots remaining"] -= 1
                                logger_sys.log_message(f"INFO: Adding item '{which_item}' to player inventory")
                                player["inventory"].append(which_item)
                                item_cost = str( item[which_item]["gold"] * zone[map_zone]["cost value"] )
                                logger_sys.log_message(f"INFO: Removing {item_cost} gold from player")
                                remove_gold(str( item[which_item]["gold"] * zone[map_zone]["cost value"] ))
                            else:
                                logger_sys.log_message("INFO: Canceling buying process --> doesn't have enough inventory slots")
                                text = COLOR_YELLOW + "You cannot buy that items because it would cause your inventory slots to be negative." + COLOR_RESET_ALL
                                print_long_string(text)
                        else:
                            logger_sys.log_message("INFO: Canceling buying process --> doesn't have enough gold")
                            text = COLOR_YELLOW + "You cannot buy that items because it would cause your gold to be negative." + COLOR_RESET_ALL
                            print_long_string(text)
                    elif choice == 'Sell Item':
                        which_item = input("Which item do you want to sell? ")
                        logger_sys.log_message(f"INFO: Player has choosen item '{which_item}' to sell")
                        if which_item in zone[map_zone]["buys"]["items"] and ( item[which_item]["gold"] * zone[map_zone]["cost value"] ) < player["gold"] and which_item in player["inventory"]:
                            logger_sys.log_message(f"INFO: Removing item '{which_item}' from player inventory")
                            player["inventory slots remaining"] -= 1
                            logger_sys.log_message(f"INFO: Adding to player {gold} gold")
                            gold = str( item[which_item]["gold"] * zone[map_zone]["cost value"] )
                            add_gold(str( item[which_item]["gold"] * zone[map_zone]["cost value"] ))
                            player["inventory"].remove(which_item)
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
                            logger_sys.log_message(f"INFO: Canceling selling process --> doesn't own item '{which_item}'")
                            text = COLOR_YELLOW + "You cannot sell that items because you don't own any of this item." + COLOR_RESET_ALL
                            print_long_string(text)
                    else:
                        continue_hostel_actions = False
            elif zone[map_zone]["type"] == "stable":
                logger_sys.log_message(f"INFO: Current map zone '{map_zone}' is a stable --> can interact")
                options = ["Train Mount", "Deposit Mount", "Ride Mount"]
                if "None" not in zone[map_zone]["stable"]["sells"]["mounts"]:
                    options += ["Buy Mount"]
                if "None" not in zone[map_zone]["stable"]["sells"]["drinks"]:
                    options += ["Buy Drink"]
                if "None" not in zone[map_zone]["stable"]["sells"]["items"]:
                    options += ["Buy Item"]
                options += ["Exit"]
                active_stable_menu = True
                text = '='
                print_separator(text)
                logger_sys.log_message("INFO: Starting stable interaction loop")
                while active_stable_menu:
                    action = term_menu.show_menu(options)
                    logger_sys.log_message(f"INFO: Player has choosen option '{action}'")
                    if action == 'Buy Item':
                        which_item = input("Which item do you want to buy? ")
                        logger_sys.log_message(f"INFO: Player has choosen item '{which_itm}' to buy")
                        if which_item in zone[map_zone]["stable"]["sells"]["items"] and ( item[which_item]["gold"] * zone[map_zone]["cost value"] ) < player["gold"]:
                            if player["inventory slots remaining"] > 0:
                                logger_sys.log_message(f"INFO: Adding item '{which_item}' from player inventory")
                                player["inventory slots remaining"] -= 1
                                player["inventory"].append(which_item)
                                logger_sys.log_message(f"INFO: Removing {gold} gold from player")
                                gold = str( item[which_item]["gold"] * zone[map_zone]["cost value"] )
                                remove_gold(str( item[which_item]["gold"] * zone[map_zone]["cost value"] ))
                            else:
                                logger_sys.log_message("INFO: Canceling buying process -> doesn't gas enough inventory slots")
                                text = COLOR_YELLOW + "You cannot buy that items because it would cause your inventory slots to be negative." + COLOR_RESET_ALL
                                print_long_string(text)
                        else:
                            logger_sys.log_message("INFO: Canceling buying process --> doesn't has enough gold")
                            text = COLOR_YELLOW + "You cannot buy that items because it would cause your gold to be negative." + COLOR_RESET_ALL
                            print_long_string(text)
                    elif action == 'Buy Drink':
                        which_drink = input("Which drink do you want to buy? ")
                        logger_sys.log_message(f"INFO: Player has choosen drink '{which_drink}' to buy")
                        if which_drink in zone[map_zone]["stable"]["sells"]["drinks"] and ( drinks[which_drink]["gold"] * zone[map_zone]["cost value"] ) < player["gold"]:
                            gold = str( drinks[which_drink]["gold"] * zone[map_zone]["cost value"] )
                            logger_sys.log_message(f"INFO: Removing {gold}  gold from player")
                            remove_gold(str( drinks[which_drink]["gold"] * zone[map_zone]["cost value"] ))
                            if drinks[which_drink]["healing level"] == 999:
                                logger_sys.log_message(f"INFO: Consuming drink '{which_drink}' --> healing player to max health")
                                player["health"] = player["max health"]
                            else:
                                healing_level = drinks[which_drink]["healing level"]
                                logger_sys.log_message(f"INFO: Consuming drink '{which_drink}' --> healing player {healing_level} hp")
                                player["health"] += drinks[which_drink]["healing level"]
                        else:
                            logger_sys.log_message("INFO: Canceling buying process --> doesn't have enough gold")
                            text = COLOR_YELLOW + "You cannot buy that items because it would cause your gold to be negative." + COLOR_RESET_ALL
                            print_long_string(text)
                    elif action == 'Buy Mount':
                        which_mount = input("Which mount do you want to buy? ")
                        logger_sys.log_message(f"INFO: Player has choosen mount '{which_mount}' to buy")
                        if which_mount in zone[map_zone]["stable"]["sells"]["mounts"]:
                            mount_cost = ( mounts[which_mount]["gold"] * zone[map_zone]["cost value"] )
                            if mount_cost < player["gold"]:
                                logger_sys.log_message(f"INFO: Removing player {mount_cost} gold")
                                remove_gold(str(mount_cost))
                                generated_mount_uuid = generate_random_uuid()
                                print("How you mount should be named ?")
                                new_mount_name = input("> ")
                                logger_sys.log_message(f"INFO: Player has choosen name '{new_mount_name}' for its new mount")
                                mounts_names_list = []
                                count = 0
                                if "None" not in list(player["mounts"]):
                                    mounts_list_len = len(player["mounts"])
                                    while count < mounts_list_len:
                                        selected_mount = list(player["mounts"])[count]
                                        selected_mount = str(selected_mount)
                                        mounts_names_list.append(str(player["mounts"][selected_mount]["name"]))
                                        count += 1
                                if new_mount_name in mounts_names_list:
                                    logger_sys.log_message(f"INFO: Canceling buying process --> already has a mount name '{new_mount_name}'")
                                    print(COLOR_YELLOW + "You already have a mount named like that." + COLOR_RESET_ALL)
                                    text = '='
                                    print_separator(text)
                                else:
                                    logger_sys.log_message("INFO: Creating new mount stats")
                                    mount_stats = {
                                        "agility addition": mounts[which_mount]["stats"]["agility addition"],
                                        "resistance addition": mounts[which_mount]["stats"]["resistance addition"]
                                    }
                                    mount_dict = {
                                        "deposited day": round(player["elapsed time game days"], 2),
                                        "is deposited": True,
                                        "level": 0,
                                        "location": "point" + str(map_location),
                                        "mount": str(which_mount),
                                        "name": str(new_mount_name),
                                        "stats": mount_stats
                                    }
                                    logger_sys.log_message(f"INFO: Created new mount stats: '{mount_dict}'")
                                    player["mounts"][generated_mount_uuid] = mount_dict
                                    logger_sys.log_message(f"INFO: Deposited new mount at map zone '{map_zone}'")
                                    text = "Your mount is currently deposited at the " + zone[map_zone]["name"] + "\nYou can ride it whenever you want."
                                    print_speech_text_effect(text)
                                    text = '='
                                    print_separator(text)
                            else:
                                logger_sys.log_message("INFO: Canceling buying process --> doesn't has enough gold")
                                print(COLOR_YELLOW + "You don't own enough gold to buy that mount" + COLOR_RESET_ALL)
                        else:
                            logger_sys.log_message(f"INFO: Canceling buying process --> current stable '{map_zone}' doesn't sell mount '{which_mount}'")
                            print(COLOR_YELLOW + "The current stable do not sell this mount" + COLOR_RESET_ALL)
                    elif action == 'Deposit Mount':
                        if player["current mount"] != " ":
                            current_mount_uuid = str(player["current mount"])
                            mount_data = player["mounts"][current_mount_uuid]
                            current_mount = mount_data["name"]
                            current_mount_type = mount_data["mount"]
                            # check if required stables are in the stable attributes
                            required_mount_stable = str(mounts[str(mount_data["mount"])]["stable"]["required stable"])
                            if required_mount_stable in zone[map_zone]["stable"]["stables"]:
                                ask = input("Do you want to deposit your current mount " + mount_data["name"] + " ? (y/n) ")
                                if ask.lower().startswith('y'):
                                    logger_sys.log_message(f"INFO: Depositing currently player ridden mount '{current_mount}' to map zone '{map_zone}")
                                    player["current mount"] = " "
                                    player["mounts"][current_mount_uuid]["is deposited"] = True
                                    player["mounts"][current_mount_uuid]["deposited day"] = round(player["elapsed time game days"], 1)
                                    player["mounts"][current_mount_uuid]["location"] = str("point" + str(map_location))
                                text = "="
                                print_separator(text)
                            else:
                                logger_sys.log_message(f"INFO: Canceling depositing process --> current stable '{map_zone}' doesn't accept mounts of type '{current_mount_type}'")
                                print(COLOR_YELLOW + "This stable doesn't accept this type of mount." + COLOR_RESET_ALL)
                        else:
                            logger_sys.log_message("INFO: Canceling depositing process --> doesn't ride any mounts by now")
                            print(COLOR_YELLOW + "You don't have any mounts to deposit here." + COLOR_RESET_ALL)
                    elif action == 'Train Mount':
                        if player["current mount"] != ' ':
                            current_mount_uuid = str(player["current mount"])
                            logger_sys.log_message("INFO: Starting mount training of mount '{current_mount_uuid}'")
                            train.training_loop(current_mount_uuid, player, item, mounts, zone[map_zone])
                        else:
                            logger_sys.log_message("INFO: Canceling mount train process --> doesn't ride any mounts by now")
                            text = COLOR_YELLOW + "You're not riding any mounts currently. You need to ride one to train it." + COLOR_RESET_ALL
                            print_long_string(text)
                    elif action == 'Ride Mount':
                        if player["current mount"] == ' ':
                            logger_sys.log_message(f"INFO: Getting player deposited mounts at stable '{map_zone}'")
                            # get player total mounts at this place
                            deposited_mounts_num = 0
                            count = 0
                            mounts_list_len = len(player["mounts"])
                            deposited_mounts_names = []
                            if "None" not in list(player["mounts"]):
                                while count < mounts_list_len:
                                        selected_mount = list(player["mounts"])[count]
                                        selected_mount = str(selected_mount)
                                        if player["mounts"][selected_mount]["location"] == "point" + str(map_location) and player["mounts"][selected_mount]["is deposited"] == True:
                                            deposited_mounts_num += 1
                                            deposited_mounts_names += [str(player["mounts"][selected_mount]["name"])]
                                        count += 1
                            else:
                                deposited_mounts_names = None
                                deposited_mounts_num = 0
                            deposited_mounts_names_list = deposited_mounts_names
                            deposited_mounts_names = str(deposited_mounts_names)
                            deposited_mounts_names = deposited_mounts_names.replace("'", '')
                            deposited_mounts_names = deposited_mounts_names.replace("[", ' -')
                            deposited_mounts_names = deposited_mounts_names.replace("]", '')
                            deposited_mounts_names = deposited_mounts_names.replace(", ", '\n -')
                            print("MOUNTS AT THIS STABLE:")
                            print(deposited_mounts_names)
                            text = '='
                            print_separator(text)
                            which_mount = input("> ")
                            logger_sys.log_message(f"INFO: Player has choosen mount '{which_mount}' to ride")
                            if which_mount in deposited_mounts_names_list:
                                # get what is the uuid of the mount of this name
                                count = 0
                                continue_searching = True
                                which_mount_uuid = ""
                                while count < len(list(player["mounts"])) and continue_searching == True:
                                    selected_mount_uuid = list(player["mounts"])[count]
                                    selected_mount_data = player["mounts"][selected_mount_uuid]
                                    if selected_mount_data["name"] == which_mount:
                                        continue_searching = False
                                        which_mount_uuid = str(selected_mount_uuid)
                                    count += 1
                                mount_take_back_cost = round(( player["elapsed time game days"] - player["mounts"][which_mount_uuid]["deposited day"] ) * zone[map_zone]["deposit gold"], 2)
                                print("If you take back this mount it will cost you " + COLOR_YELLOW + COLOR_STYLE_BRIGHT + str(mount_take_back_cost) + COLOR_RESET_ALL + " gold. ")
                                ask = input("(y/n) ")
                                if player["gold"] > mount_take_back_cost:
                                    if ask.lower().startswith('y'):
                                        logger_sys.log_message(f"INFO: Removing {mount_take_back_cost} gold from player")
                                        remove_gold(mount_take_back_cost)
                                        player["current mount"] = str(which_mount_uuid)
                                        player["mounts"][which_mount_uuid]["is deposited"] = False
                                        player["mounts"][which_mount_uuid]["deposited day"] = 0
                                        player["mounts"][which_mount_uuid]["location"] = "point" + str(map_location)
                                else:
                                    logger_sys.log_message("INFO: Canceling taking back process --> doesn't has enough gold")
                                    print(COLOR_YELLOW + "You don't own enough gold to take back your mount." + COLOR_RESET_ALL)
                            else:
                                logger_sys.log_message("INFO: Canceling taking back process --> doesn't own that mount or the mount isn't deposited at this current location")
                                text = COLOR_YELLOW + "You don't own that mount or the mount isn't deposited at this current location" + COLOR_RESET_ALL
                                print_long_string(text)
                        else:
                            (f"INFO: Canceling taking back process --> already riding mount '{which_mount}'")
                            text = COLOR_YELLOW + "You are currently already riding a mount. You need to deposit your current mount before riding an other one." + COLOR_RESET_ALL
                            print_long_string(text)
                    else:
                        active_stable_menu = False
            elif zone[map_zone]["type"] == "blacksmith":
                logger_sys.log_message(f"INFO: Current map zone '{map_zone}' is a blacksmith --> can interact")
                text = '='
                print_separator(text)

                options = ['Sell Equipment', 'Order Equipment', 'Upgrade Equipment', 'Check Order', 'Exit']
                continue_blacksmith_actions = True
                logger_sys.log_message("INFO: Starting blacksmith interact loop")
                while continue_blacksmith_actions:
                    action = term_menu.show_menu(options)
                    logger_sys.log_message(f"INFO: Player has choosen option '{action}'")
                    if action == 'Sell Equipment':
                        which_weapon = input("Which equipment do you want to sell? ")
                        logger_sys.log_message(f"INFO: Player has choosen item '{which_weapon}' to sell")
                        if which_weapon in zone[map_zone]["blacksmith"]["buys"] and which_weapon in player["inventory"]:
                            gold = str( item[which_weapon]["gold"] * zone[map_zone]["cost value"] )
                            add_gold(str( item[which_weapon]["gold"] * zone[map_zone]["cost value"] ))
                            logger_sys.log_message(f"INFO: Adding to player {gold} gold")
                            player["inventory"].remove(which_weapon)
                            logger_sys.log_message(f"INFO: Removing item '{which_weapon}' from player inventory")
                        else:
                            text = COLOR_YELLOW + "You cannot sell that equipment because you dont own any of that weapon or because the current blacksmith doesn't buy this weapon." + COLOR_RESET_ALL
                            logger_sys.log_message(f"INFO: Canceling selling process --> current blacksmith '{map_zone}' doesn't sell item '{which_weapon}' or player doesn't own item '{which_weapon}'")
                            print_long_string(text)
                    elif action == 'Order Equipment':
                        which_weapon = input("Which equipment do you want to order? ")
                        logger_sys.log_message(f"INFO: Player has choosen item '{which_weapon}' to order")
                        if which_weapon in zone[map_zone]["blacksmith"]["orders"] and player["gold"] > zone[map_zone]["blacksmith"]["orders"][which_weapon]["gold"]:
                            required_items = False
                            count = 0
                            required_items_number = 0
                            fake_player_inventory = player["inventory"]
                            while count < len(fake_player_inventory):
                                selected_item = fake_player_inventory[count]
                                if selected_item in zone[map_zone]["blacksmith"]["orders"][which_weapon]["needed materials"]:
                                    required_items_number += 1
                                count += 1
                            if required_items_number == len(zone[map_zone]["blacksmith"]["orders"][which_weapon]["needed materials"]):
                                required_items = True
                                logger_sys.log_message("INFO: Player has required items --> continuing")
                            if required_items == True:
                                gold = str( item[which_weapon]["gold"] * zone[map_zone]["cost value"] )
                                logger_sys.log_message(f"INFO: Removing from player {gold} gold")
                                remove_gold(str( item[which_weapon]["gold"] * zone[map_zone]["cost value"] ))
                                count = 0
                                remaining_items_to_remove = len(zone[map_zone]["blacksmith"]["orders"][which_weapon]["needed materials"])
                                while count < len(player["inventory"]) and remaining_items_to_remove != 0:
                                    selected_item = zone[map_zone]["blacksmith"]["orders"][which_weapon]["needed materials"][count]
                                    logger_sys.log_message(f"INFO: Removing from player inventory item '{selected_item}'")
                                    player["inventory"].remove(selected_item)
                                    remaining_items_to_remove -= 1
                                    count += 1
                                order_uuid = generate_random_uuid()
                                logger_sys.log_message(f"INFO: Creating order '{order_uuid}' dictionary")
                                order_dict = {
                                    "paid gold": zone[map_zone]["blacksmith"]["orders"][which_weapon]["gold"],
                                    "ordered weapon": which_weapon,
                                    "ordered day": player["elapsed time game days"],
                                    "ordered blacksmith": zone[map_zone]["name"],
                                    "time needed": zone[map_zone]["blacksmith"]["orders"][which_weapon]["time needed"],
                                    "has taken back order": "false"
                                }
                                logger_sys.log_message(f"Created order '{order_uuid}' dictionary: '{order_dict}'")
                                player["orders"][order_uuid] = order_dict
                                text = "You'll be able to get your finished order in " + COLOR_MAGENTA + COLOR_STYLE_BRIGHT + str(zone[map_zone]["blacksmith"]["orders"][which_weapon]["time needed"]) + COLOR_RESET_ALL + " days."
                                print_long_string(text)
                            else:
                                logger_sys.log_message("INFO: Canceling ordering process --> doesn't have necessary items")
                                text = COLOR_YELLOW + "You cannot order that equipment because you dont have the necessary items." + COLOR_RESET_ALL
                                print_long_string(text)
                        else:
                            logger_sys.log_message("INFO: Canceling ordering process --> doesn't has enough gold")
                            text = COLOR_YELLOW + "You cannot order that weapon because you dont own enough gold." + COLOR_RESET_ALL
                            print_long_string(text)
                    elif action == 'Upgrade Equipment':
                        which_weapon = input("Which equipment do you want to upgrade? ")
                        logger_sys.log_message(f"INFO: Player has choosen equipment '{which_weapon}' to upgrade")
                        if which_weapon in player["inventory"]:
                            item_next_upgrade_name = str(check_weapon_next_upgrade_name(which_weapon))
                            if item_next_upgrade_name != 'None':
                                if player["gold"] > item[item_next_upgrade_name]["gold"]:
                                    required_items = False
                                    count = 0
                                    required_items_number = 0
                                    fake_player_inventory = player["inventory"]
                                    while count < len(fake_player_inventory):
                                        selected_item = fake_player_inventory[count]
                                        if selected_item in item[str(item_next_upgrade_name)]["for this upgrade"]:
                                            required_items_number += 1
                                        count += 1
                                    if required_items_number == len(item[str(item_next_upgrade_name)]["for this upgrade"]):
                                        required_items = True
                                        logger_sys.log_message("INFO: Player has required items for --< continuing")
                                    if required_items == True:
                                        gold = str(item[item_next_upgrade_name]["gold"])
                                        logger_sys.log_message(f"INFO: Removing from player {gold} gold")
                                        remove_gold(str(item[item_next_upgrade_name]["gold"]))
                                        player["inventory"].remove(which_weapon)
                                        count = 0
                                        remaining_items_to_remove = len(item[str(item_next_upgrade_name)]["for this upgrade"])
                                        while count < len(player["inventory"]) and remaining_items_to_remove != 0:
                                            selected_item = item[str(item_next_upgrade_name)]["for this upgrade"][count]
                                            player["inventory"].remove(selected_item)
                                            remaining_items_to_remove -= 1
                                            count += 1
                                        order_uuid = generate_random_uuid()
                                        logger_sys.log_message(f"INFO: Creating order '{order_uuid}' dictionary")
                                        order_dict = {
                                            "paid gold": item[str(item_next_upgrade_name)]["gold"],
                                            "ordered weapon": str(item_next_upgrade_name),
                                            "ordered day": player["elapsed time game days"],
                                            "ordered blacksmith": zone[map_zone]["name"],
                                            "time needed": round(random.uniform(.55, 3.55), 2),
                                            "has taken back order": "false"
                                        }
                                        logger_sys.log_message(f"Created order '{order_uuid}' dictionary: '{order_dict}'")
                                        player["orders"][order_uuid] = order_dict
                                        text = "You'll be able to get your finished order in " + COLOR_MAGENTA + COLOR_STYLE_BRIGHT + str(player["orders"][order_uuid]["time needed"]) + COLOR_RESET_ALL + " days."
                                        print_long_string(text)
                                    else:
                                        logger_sys.log_message("INFO: Canceling upgrading process --> doesn't has the necessary items")
                                        print(COLOR_YELLOW + "You don't own the necessary items to upgrade" + COLOR_RESET_ALL)
                                else:
                                    logger_sys.log_message("INFO: Canceling upgrading process --> doesn't has enough gold")
                                    print(COLOR_YELLOW + "You don't have enough gold to upgrade." + COLOR_RESET_ALL)
                            else:
                                logger_sys.log_message(f"INFO: Canceling upgrading process --> cannot upgrade equipment '{which_weapon}' further")
                                print(COLOR_YELLOW + "You cannot upgrade this equipment further." + COLOR_RESET_ALL)
                        else:
                            logger_sys.log_message(f"INFO: Canceling upgrading process --> player doesn't own any '{which_weapon}' in its inventory")
                            print(COLOR_YELLOW + "You don't own that equipment" + COLOR_RESET_ALL)
                    elif action == 'Check Order':
                        player_orders = player["orders"]
                        logger_sys.log_message(f"INFO: Printing player orders: '{player_orders}'")
                        player_orders_numbers = len(list(player_orders))
                        player_orders_to_collect = []
                        player_orders_number = []
                        count = 0
                        while count < player_orders_numbers:
                            skip = False
                            selected_order_name = list(player_orders)[count]
                            if selected_order_name == "None":
                                skip = True
                            if not skip:
                                selected_order = player["orders"][selected_order_name]
                                try:
                                    ordered_blacksmith = selected_order["ordered blacksmith"]
                                    ordered_weapon = selected_order["ordered weapon"]
                                except:
                                    print(ordered_blacksmith, ordered_weapon)
                                if ordered_blacksmith == zone[map_zone]["name"]:
                                    ordered_weapon_syntax = ordered_weapon + " {" + str(count) + "}"
                                    player_orders_to_collect += [ordered_weapon_syntax]
                                    player_orders_number += [str(count)]
                            count += 1
                        player_orders_to_collect = str(player_orders_to_collect)
                        logger_sys.log_message(f"INFO: Printing player orders to collect: '{player_orders_to_collect}'")
                        player_orders_to_collect = player_orders_to_collect.replace("'", '')
                        player_orders_to_collect = player_orders_to_collect.replace("[", ' -')
                        player_orders_to_collect = player_orders_to_collect.replace("]", '')
                        player_orders_to_collect = player_orders_to_collect.replace(", ", '\n -')
                        print("ORDERS:")
                        print(player_orders_to_collect)
                        text = '='
                        print_separator(text)
                        which_order = input("> ")
                        logger_sys.log_message(f"INFO: Player has choosen order '{which_order}'")
                        if which_order in player_orders_number:
                            current_order_uuid = str(list(player["orders"])[int(which_order)])
                            text = '='
                            print_separator(text)

                            time_left = round(player["orders"][current_order_uuid]["ordered day"] + player["orders"][current_order_uuid]["time needed"] - player["elapsed time game days"], 1)
                            if time_left <= 0:
                                time_left = "READY TO COLLECT"
                            logger_sys.log_message(f"INFO: Printing order '{current_order_uuid}' information to GUI")
                            print("ORDERED EQUIPMENT: " + COLOR_RED + str(player["orders"][current_order_uuid]["ordered weapon"]) + COLOR_RESET_ALL)
                            print("PAID GOLD: " + COLOR_YELLOW + COLOR_STYLE_BRIGHT + str(round(player["orders"][current_order_uuid]["paid gold"], 1)) + COLOR_RESET_ALL)
                            print("ORDERED DAY: " + COLOR_MAGENTA + COLOR_STYLE_BRIGHT + str(round(player["orders"][current_order_uuid]["ordered day"], 1)) + COLOR_RESET_ALL)
                            print("TIME LEFT: " + COLOR_CYAN + COLOR_STYLE_BRIGHT + str(time_left) + COLOR_RESET_ALL)

                            text = '='
                            print_separator(text)
                            options_order = ['Cancel Order']
                            if time_left == "READY TO COLLECT":
                                options_order += ['Collect Order']
                            options_order += ['Exit']
                            action = term_menu.show_menu(options_order)
                            logger_sys.log_message(f"INFO: Player has choosen option '{action}'")
                            if action == 'Cancel Order':
                                text = "Are you sure you want to cancel this order? You will receive 75% of the gold you paid and you won't be able"
                                print_long_string(text)
                                ask =input(" to get your given items back. (y/n)")
                                if ask.lower().startswith('y'):
                                    # give player 75% of paid gold
                                    gold = player["orders"][current_order_uuid]["paid gold"]
                                    gold2 = player["orders"][current_order_uuid]["paid gold"] * ( 75 / 100 )
                                    logger_sys.log_message(f"INFO: Giving back player 75% of the paid gold: {gold} * 100 / 75 = {gold2}")
                                    add_gold(player["orders"][current_order_uuid]["paid gold"] * ( 75 / 100 ))
                                    # remove order from player orders
                                    player["orders"].pop(current_order_uuid)
                            if action == 'Collect Order':
                                order = str(player["orders"][current_order_uuid]["ordered weapon"])
                                logger_sys.log_message(f"INFO: Collecting order --> adding to player inventory item '{order}'")
                                player["inventory"].append(str(player["orders"][current_order_uuid]["ordered weapon"]))
                                # remove order from player orders
                                player["orders"].pop(current_order_uuid)
                        else:
                            logger_sys.log_message(f"INFO: Cancelling collecting order process --> player has no order '{which_order}' at map zone '{map_zone}'")
                            print(COLOR_YELLOW + "You don't have this order currently at this place." + COLOR_RESET_ALL)
                    else:
                        continue_blacksmith_actions = False
            elif zone[map_zone]["type"] == "forge":
                logger_sys.log_message(f"INFO: map zone '{map_zone}' is a forge --> can interact")
                current_forge = zone[map_zone]
                text = '='
                print_separator(text)
                options = []
                if "None" not in current_forge["forge"]["buys"]:
                    options += ['Sell Metals']
                if "None" not in current_forge["forge"]["sells"]:
                    options += ['Buy Metals']
                options += ['Exit']
                continue_forge_actions = True
                logger_sys.log_message("INFO: Starting forge interact loop")
                while continue_forge_actions:
                    choice = term_menu.show_menu(options)
                    logger_sys.log_message(f"INFO: Player has choosen option '{choice}'")
                    if choice == 'Sell Metals':
                        which_metal = input("Which metal do you want to sell? ")
                        logger_sys.log_message(f"INFO: Player has choosen metal '{which_metal}' to buy")
                        if which_metal in current_forge["forge"]["buys"]:
                            metal_count = int(input("How many count of this metal you want to sell? "))
                            logger_sys.log_message(f"INFO: Player has choosen to sell '{metal_count}' of the metal '{which_metal}'")
                            if player["inventory"].count(which_metal) >= metal_count:
                                gold = item[which_metal]["gold"] * current_forge["cost value"] * metal_count
                                logger_sys.log_message(f"INFO: Adding {gold} gold to player")
                                add_gold(item[which_metal]["gold"] * current_forge["cost value"] * metal_count)
                                count = 0
                                while count < metal_count:
                                    logger_sys.log_message(f"INFO: Removing from player inventory item '{which_metal}'")
                                    player["inventory"].remove(which_metal)
                                    count += 1
                            else:
                                logger_sys.log_message(f"INFO: Canceling selling process --> doesn't has {metal_count} '{which_metal}' in player's inventory")
                                print(COLOR_YELLOW + "You don't own that many count of this metal" + COLOR_RESET_ALL)
                        else:
                            logger_sys.log_message(f"INFO: Canceling selling process --> current forge '{map_zone}' doesn't sell metal '{which_metal}'")
                            print(COLOR_YELLOW + "The current forge doesn't buys this metal" + COLOR_RESET_ALL)
                    elif choice == 'Buy Metals':
                        which_metal = input("Which metal do you want to buy? ")
                        logger_sys.log_message(f"INFO: Player has choosen item '{which_metal}' to buy")
                        if which_metal in current_forge["forge"]["sells"]:
                            metal_count = int(input("How many count of this metal you want to buy? "))
                            if player["gold"] >= item[which_metal]["gold"] * current_forge["cost value"] * metal_count:
                                gold = item[which_metal]["gold"] * current_forge["cost value"] * metal_count
                                logger_sys.log_message(f"INFO: Removing from player {gold} gold")
                                remove_gold(item[which_metal]["gold"] * current_forge["cost value"] * metal_count)
                                count = 0
                                while count < metal_count:
                                    logger_sys.log_message(f"INFO: Removing from player inventory item '{which_metal}")
                                    player["inventory"].append(which_metal)
                                    count += 1
                            else:
                                logger_sys.log_message(f"INFO: Canceling buying process --> doesn't have enough gold")
                                print(COLOR_YELLOW + "You don't own enough gold to buy that many metal" + COLOR_RESET_ALL)
                        else:
                            logger_sys.log_message(f"INFO: Canceling buying process --> current forge '{map_zone}' doesn't sell item '{which_metal}'")
                            print(COLOR_YELLOW + "The current forge doesn't sells this metal" + COLOR_RESET_ALL)
                    else:
                        continue_forge_actions = False
            else:
                logger_sys.log_message(f"INFO: Map zone '{map_zone}' cannot have interactions")
                print(COLOR_YELLOW + "You cannot find any near hostel, stable, blacksmith, forge or church." + COLOR_RESET_ALL)
                time.sleep(1.5)
        elif command.lower().startswith('y'):
            if "mounts" in player and player["mounts"] != '':
                logger_sys.log_message("INFO: Printing player currently ridden mount")
                text = '='
                print_separator(text)
                if "current mount" in player:
                    current_mount_uuid = str(player["current mount"])
                    if current_mount_uuid != ' ':
                        print("RIDDED MOUNT: " + COLOR_GREEN + COLOR_STYLE_BRIGHT + player["mounts"][current_mount_uuid]["name"] + COLOR_RESET_ALL + " (" + player["mounts"][current_mount_uuid]["mount"] + ")")
                    else:
                        print("RIDDED MOUNT: " + COLOR_RED + COLOR_STYLE_BRIGHT + "NONE" + COLOR_RESET_ALL)
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
                print(" ")
                print("OWNED MOUNTS:")
                print(mounts_names_list_str)
                text = '='
                print_separator(text)
                which_mount = input("> ")
                logger_sys.log_message(f"INFO: Player has choosen option '{which_mount}' to examine")
                if which_mount in mounts_names_list:
                    text = '='
                    print_separator(text)

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
                    print_enemy_thumbnail(str(mounts[which_mount_data["mount"]]["name"]))
                    print(" ")

                    print("GIVEN NAME: " + which_mount_data["name"])
                    print("MOUNT: " + mounts[which_mount_data["mount"]]["name"])
                    print("PLURAL: " + mounts[which_mount_data["mount"]]["plural"])
                    print(" ")

                    which_mount_location = "(" + COLOR_GREEN + COLOR_STYLE_BRIGHT + str(map[which_mount_data["location"]]["x"]) + COLOR_RESET_ALL + ", " + COLOR_GREEN + COLOR_STYLE_BRIGHT + str(map[which_mount_data["location"]]["y"]) + COLOR_RESET_ALL + ")"
                    print("LOCATION: " + which_mount_location)
                    if which_mount_data["is deposited"] == True:
                        print("STABLE: " + str(map[which_mount_data["location"]]["map zone"]))
                        print("DEPOSITED DAY: " + COLOR_MAGENTA + COLOR_STYLE_BRIGHT + str(which_mount_data["deposited day"]) + COLOR_RESET_ALL)
                    print(" ")

                    print("STATS:")
                    print("  LEVEL: " + COLOR_GREEN + COLOR_STYLE_BRIGHT + str(int(round(which_mount_data["level"], 0))) + COLOR_RESET_ALL + "/" + str(int(round(mounts[str(which_mount_data["mount"])]["levels"]["max level"]))))
                    print("  AGILITY ADDITION: " + COLOR_MAGENTA + COLOR_STYLE_BRIGHT + str(which_mount_data["stats"]["agility addition"]) + COLOR_RESET_ALL)
                    print("  RESISTANCE ADDITION: " + COLOR_CYAN + COLOR_STYLE_BRIGHT + str(which_mount_data["stats"]["resistance addition"]) + COLOR_RESET_ALL)
                    print(" ")

                    # get player possible feeding items
                    current_mount_feeds = mounts[which_mount_data["mount"]]["feed"]["food"]
                    player_feeding_items_text = str(current_mount_feeds)
                    player_feeding_items_text = player_feeding_items_text.replace("'", '')
                    player_feeding_items_text = player_feeding_items_text.replace("[", ' -')
                    player_feeding_items_text = player_feeding_items_text.replace("]", '')
                    player_feeding_items_text = player_feeding_items_text.replace(", ", '\n -')
                    print("FEEDING ITEMS:")
                    print(player_feeding_items_text)
                    print("")

                    text = "DESCRIPTION: " + mounts[which_mount_data["mount"]]["description"]
                    print_long_string(text)

                    text = '='
                    print_separator(text)
                    options = ['Abandon', 'Rename', 'Exit']
                    choice = term_menu.show_menu(options)
                    logger_sys.log_message(f"INFO: Player has choosen option '{choice}'")
                    count = 0
                    continue_action = True
                    while count < len(list(player["mounts"])) and continue_action == True:
                        selected_mount_uuid = str(list(player["mounts"])[count])
                        if player["mounts"][selected_mount_uuid]["name"] == str(which_mount):
                            mount_uuid = selected_mount_uuid
                            continue_action = False
                        count += 1
                    if choice == 'Abandon':
                        print("Are you sure you want to abandon this mount? You won't")
                        ask = input(" be able to find him after that. (y/n) ")
                        if ask.lower().startswith('y'):
                            logger_sys.log_message(f"INFO: Player is abandoning mount '{which_mount}'")
                            player["mounts"].pop(mount_uuid)
                            player["current mount"] = " "
                    elif choice == 'Rename':
                        print("Select a new name for your mount")
                        new_name = input("> ")
                        logger_sys.log_message(f"INFO: Player has choosen as a new name for mount '{which_mount}' '{new_name}'")
                        if new_name in mounts_names_list:
                            logger_sys.log_message("INFO: Canceling mount renaming process --> already has a mount name like hat")
                            print(COLOR_YELLOW + "You already have a mount named like that." + COLOR_RESET_ALL)
                            time.sleep(1.5)
                        else:
                            player["mounts"][mount_uuid]["name"] = str(new_name)
                else:
                    logger_sys.log_message(f"INFO: Canceling mount examining process --> doesn't own any mount named '{which_mount}'")
                    print(COLOR_YELLOW + "You don't have any mounts named like that." + COLOR_RESET_ALL)
                    time.sleep(1.5)
            else:
                logger_sys.log_message(f"INFO: Canceling mount examining process --> player doesn't own any mounts")
                print(COLOR_YELLOW + "It seems you don't own any mounts." + COLOR_RESET_ALL)
                time.sleep(1.5)
        elif command.lower().startswith('m'):
            if "Map" in player["inventory"]:
                logger_sys.log_message("INFO: Player is examining map")
                map_item.print_map(player, map, zone)
            else:
                logger_sys.log_message("INFO: Canceling map examining process --> doesn't have 'Map' item")
                print("You do not have a map.")
                print(" ")
            finished = input(" ")
        elif command == "q" or command == "Q":
            logger_sys.log_message("INFO: Closing & Saving game")
            print(separator)
            play = 0
        else:
            logger_sys.log_message(f"INFO: Choosen command '{command}' is not a valid command")
            print("'" + command + "' is not a valid command")
            time.sleep(2)
            print(" ")
        # get end time
        end_time = time.time()
        logger_sys.log_message(f"INFO: Getting end time: '{end_time}'")

        # calculate elapsed time
        elapsed_time = end_time - start_time
        elapsed_time = round(elapsed_time, 2)
        logger_sys.log_message(f"INFO: Getting elapsed time: '{elapsed_time}'")

        game_elapsed_time = .001389 * elapsed_time # 180 seconds irl = .25 days in-game
        game_elapsed_time = round(game_elapsed_time, 2)
        logger_sys.log_message(f"INFO: Getting elapsed time in game days: '{game_elapsed_time}'")

        player["elapsed time seconds"] = float(elapsed_time) + float(player["elapsed time seconds"])
        player["elapsed time game days"] = game_elapsed_time + player["elapsed time game days"]

if play == 1:
    play = run(1)

# finish up and save
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

# deinitialize colorame
deinit()
os.system('clear')

