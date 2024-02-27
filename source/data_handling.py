import appdirs
import logger_sys
import check_yaml
import colors
import os
import git
import shutil
import tempfile
import yaml
import time
import text_handling
import fsspec
import time
import sys
import subprocess
from rich.progress import Progress
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

    # Make these variables global
    global map, item, drinks, enemy, npcs, start_player
    global lists, zone, dialog, mission, mounts

    print("")
    # If the inputted which_type is vanilla, then just
    # load the vanilla game data

    if which_type == 'vanilla':
        logger_sys.log_message("INFO: Loading vanilla game data")
        with Progress() as progress:
            task_map = progress.add_task("[cyan]Loading Game Map Data...", total=100)
            task_item = progress.add_task("[cyan]Loading Game Items Data...", total=100)
            task_drink = progress.add_task("[cyan]Loading Game Drinks Data...", total=100)
            task_enemy = progress.add_task("[cyan]Loading Game Enemies Data...", total=100)
            task_npc = progress.add_task("[cyan]Loading Game NPCS Data...", total=100)
            task_start = progress.add_task("[cyan]Loading Game Start Data...", total=3)
            task_lists = progress.add_task("[cyan]Loading Game Lists Data...", total=100)
            task_zone = progress.add_task("[cyan]Loading Game Zones Data...", total=100)
            task_dialog = progress.add_task("[cyan]Loading Game Dialogs Data...", total=100)
            task_mission = progress.add_task("[cyan]Loading Game Missions Data...", total=100)
            task_mount = progress.add_task("[cyan]Loading Game Mounts Data...", total=100)

            with open(program_dir + "/game/data/map.yaml") as f:
                map = yaml.safe_load(f)
            progress.update(task_map, total=len(list(map)))
            for i in list(map):
                check_yaml.examine_map_point(map[i])
                progress.update(task_map, advance=1)

            with open(program_dir + "/game/data/items.yaml") as f:
                item = yaml.safe_load(f)
            progress.update(task_item, total=len(list(item)))
            for i in list(item):
                check_yaml.examine_item(item[i])
                progress.update(task_item, advance=1)

            with open(program_dir + "/game/data/drinks.yaml") as f:
                drinks = yaml.safe_load(f)
            progress.update(task_drink, total=len(list(drinks)))
            for i in list(drinks):
                check_yaml.examine_drink(drinks[i])
                progress.update(task_drink, advance=1)

            with open(program_dir + "/game/data/enemies.yaml") as f:
                enemy = yaml.safe_load(f)
            progress.update(task_enemy, total=len(list(enemy)))
            for i in list(enemy):
                check_yaml.examine_enemy(enemy[i])
                progress.update(task_enemy, advance=1)

            with open(program_dir + "/game/data/npcs.yaml") as f:
                npcs = yaml.safe_load(f)
            progress.update(task_npc, total=len(list(npcs)))
            for i in list(npcs):
                check_yaml.examine_npc(npcs[i])
                progress.update(task_npc, advance=1)

            with open(program_dir + "/game/data/start.yaml") as f:
                progress.update(task_start, advance=1)
                start_player = yaml.safe_load(f)
                progress.update(task_start, advance=1)
                check_yaml.examine(program_dir + "/game/data/start.yaml")
            progress.update(task_start, advance=1)

            with open(program_dir + "/game/data/lists.yaml") as f:
                lists = yaml.safe_load(f)
            progress.update(task_lists, total=len(list(lists)))
            for i in list(lists):
                check_yaml.examine_list(lists[i])
                progress.update(task_lists, advance=1)

            with open(program_dir + "/game/data/zone.yaml") as f:
                zone = yaml.safe_load(f)
            progress.update(task_zone, total=len(list(zone)))
            for i in list(zone):
                check_yaml.examine_zone(zone[i])
                progress.update(task_zone, advance=1)

            with open(program_dir + "/game/data/dialog.yaml") as f:
                dialog = yaml.safe_load(f)
            progress.update(task_dialog, total=len(list(dialog)))
            for i in list(dialog):
                check_yaml.check_dialog_conversations(dialog, i)
                progress.update(task_dialog, advance=.5)
                check_yaml.examine_dialog(dialog[i])
                progress.update(task_dialog, advance=.5)

            with open(program_dir + "/game/data/mission.yaml") as f:
                mission = yaml.safe_load(f)
            progress.update(task_mission, total=len(list(mission)))
            for i in list(mission):
                check_yaml.examine_mission(mission[i])
                progress.update(task_mission, advance=1)

            with open(program_dir + "/game/data/mounts.yaml") as f:
                mounts = yaml.safe_load(f)
            progress.update(task_mount, total=len(list(mounts)))
            for i in list(mounts):
                check_yaml.examine_mount(mounts[i])
                progress.update(task_mount, advance=1)

    else:
        logger_sys.log_message(f"INFO: Loading plugin '{what_plugin}' data")
        check_file = os.path.exists(program_dir + "/plugins/" + what_plugin)
        if not check_file:
            print(COLOR_RED + COLOR_STYLE_BRIGHT + "ERROR: Couldn't find plugin '" + what_plugin + "'" + COLOR_RESET_ALL)
            logger_sys.log_message(f"ERROR: Couldn't find plugin '{what_plugin}'")
            play = 0
            text_handling.exit_game()

        with Progress() as progress:

            task_map = progress.add_task("[cyan]Loading Game Map Data...", total=100)
            task_item = progress.add_task("[cyan]Loading Game Items Data...", total=100)
            task_drink = progress.add_task("[cyan]Loading Game Drinks Data...", total=100)
            task_enemy = progress.add_task("[cyan]Loading Game Enemies Data...", total=100)
            task_npc = progress.add_task("[cyan]Loading Game NPCS Data...", total=100)
            task_start = progress.add_task("[cyan]Loading Game Start Data...", total=3)
            task_lists = progress.add_task("[cyan]Loading Game Lists Data...", total=100)
            task_zone = progress.add_task("[cyan]Loading Game Zones Data...", total=100)
            task_dialog = progress.add_task("[cyan]Loading Game Dialogs Data...", total=100)
            task_mission = progress.add_task("[cyan]Loading Game Missions Data...", total=100)
            task_mount = progress.add_task("[cyan]Loading Game Mounts Data...", total=100)
            task_requirements = progress.add_task("[cyan]Loading Plugin Requirements...", total=100)

            with open(program_dir + "/plugins/" + what_plugin + "/map.yaml") as f:
                map = yaml.safe_load(f)
            progress.update(task_map, total=len(list(map)))
            for i in list(map):
                check_yaml.examine_map_point(map[i])
                progress.update(task_map, advance=1)

            with open(program_dir + "/plugins/" + what_plugin + "/items.yaml") as f:
                item = yaml.safe_load(f)
            progress.update(task_item, total=len(list(item)))
            for i in list(item):
                check_yaml.examine_item(item[i])
                progress.update(task_item, advance=1)

            with open(program_dir + "/plugins/" + what_plugin + "/drinks.yaml") as f:
                drinks = yaml.safe_load(f)
            progress.update(task_drink, total=len(list(drinks)))
            for i in list(drinks):
                check_yaml.examine_drink(drinks[i])
                progress.update(task_drink, advance=1)

            with open(program_dir + "/plugins/" + what_plugin + "/enemies.yaml") as f:
                enemy = yaml.safe_load(f)
            progress.update(task_enemy, total=len(list(enemy)))
            for i in list(enemy):
                check_yaml.examine_enemy(enemy[i])
                progress.update(task_enemy, advance=1)

            with open(program_dir + "/plugins/" + what_plugin + "/npcs.yaml") as f:
                npcs = yaml.safe_load(f)
            progress.update(task_npc, total=len(list(npcs)))
            for i in list(npcs):
                check_yaml.examine_npc(npcs[i])
                progress.update(task_npc, advance=1)

            with open(program_dir + "/plugins/" + what_plugin + "/start.yaml") as f:
                progress.update(task_start, advance=1)
                start_player = yaml.safe_load(f)
                progress.update(task_start, advance=1)
                check_yaml.examine(program_dir + "/plugins/" + what_plugin + "/start.yaml")
            progress.update(task_start, advance=1)

            with open(program_dir + "/plugins/" + what_plugin + "/lists.yaml") as f:
                lists = yaml.safe_load(f)
            progress.update(task_lists, total=len(list(lists)))
            for i in list(lists):
                check_yaml.examine_list(lists[i])
                progress.update(task_lists, advance=1)

            with open(program_dir + "/plugins/" + what_plugin + "/zone.yaml") as f:
                zone = yaml.safe_load(f)
            progress.update(task_zone, total=len(list(zone)))
            for i in list(zone):
                check_yaml.examine_zone(zone[i])
                progress.update(task_zone, advance=1)

            with open(program_dir + "/plugins/" + what_plugin + "/dialog.yaml") as f:
                dialog = yaml.safe_load(f)
            progress.update(task_dialog, total=len(list(dialog)))
            for i in list(dialog):
                check_yaml.check_dialog_conversations(dialog, i)
                progress.update(task_dialog, advance=.5)
                check_yaml.examine_dialog(dialog[i])
                progress.update(task_dialog, advance=.5)

            with open(program_dir + "/plugins/" + what_plugin + "/mission.yaml") as f:
                mission = yaml.safe_load(f)
            progress.update(task_mission, total=len(list(mission)))
            for i in list(mission):
                check_yaml.examine_mission(mission[i])
                progress.update(task_mission, advance=1)

            with open(program_dir + "/plugins/" + what_plugin + "/mounts.yaml") as f:
                mounts = yaml.safe_load(f)
            progress.update(task_mount, total=len(list(mounts)))
            for i in list(mounts):
                check_yaml.examine_mount(mounts[i])
                progress.update(task_mount, advance=1)

            logger_sys.log_message(f"INFO: Loading plugin '{what_plugin}' module requirements")
            requirements_file = program_dir + '/plugins/' + what_plugin + "/requirements.txt"
            # Check which executable to use
            executable = "python"
            try:
                subprocess.check_call(
                    ["python", "-V"],
                    stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT
                )
            except Exception as error:
                executable = "python3"

            # Install the required modules
            try:
                f = open(requirements_file)
                modules = f.readlines()
                progress.update(task_requirements, total=len(modules))
                for line in modules:
                    retcode = subprocess.check_call(
                        [executable, "-m", "pip", "install", line],
                        stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT
                    )
                    progress.update(task_requirements, advance=1)
            except Exception as error:
                logger_sys.log_message(f"WARNING: Couldn't install plugin '{what_plugin}' python requirements.txt")
                logger_sys.log_message(f"DEBUG: '{error}'")
                progress.update(task_requirements, advance=100)
    return map, item, drinks, enemy, npcs, start_player, lists, zone, dialog, mission, mounts


def fsspec_download(github_file, destination_point, download_branch, download_repo, download_org):
    try:
        destination = destination_point
        fs = fsspec.filesystem("github", org=download_org, repo=download_repo, sha=download_branch)
        fs.get(fs.ls(github_file), destination)
    except Exception as error:
        print(
            COLOR_YELLOW + COLOR_STYLE_BRIGHT + "WARNING:" + COLOR_RESET_ALL +
            " an error occurred when trying to download game data to '" +
            destination + "'."
        )
        logger_sys.log_message(f"WARNING: An error occurred when downloading game data to '{destination}'.")
        logger_sys.log_message("DEBUG: " + str(error))
        print(COLOR_YELLOW + str(error) + COLOR_RESET_ALL)
        time.sleep(.5)


def temporary_git_file_download(selected_file):
    global file_text_data
    # Create a temporary directory to after
    # clone the repository and select the chosen
    # file and export its data in a string

    temporary_dir = tempfile.mkdtemp()
    logger_sys.log_message(f"INFO: Creating temporary directory at '{temporary_dir}'")
    git.Repo.clone_from('https://github.com/Dungeons-of-Kathallion/Bane-Of-Wargs.wiki.git', temporary_dir, depth=1)

    with open(temporary_dir + '/' + selected_file, 'r') as f:
        file_text_data = f.read()

    return file_text_data


def open_file(file_path):
    try:
        editor = os.environ['EDITOR']
    except KeyError:
        editor = 'nano'
    logger_sys.log_message(f"INFO: Editing file '{file_path}' with editor '{editor}'")
    subprocess.call([editor, file_path])


# deinitialize colorama
deinit()
