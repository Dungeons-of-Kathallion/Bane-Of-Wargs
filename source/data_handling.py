# data_handling.py
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
import check_yaml
import text_handling
import script_handling
import yaml_handling
from colors import *
from terminal_handling import cout
# external imports
import appdirs
import os
import tempfile
import time
import fsspec
import time
import io
import subprocess
import shutil
from rich.progress import Progress


# Get program add directory
program_dir = str(appdirs.user_config_dir(appname='Bane-Of-Wargs'))

# Handling functions


def load_game_data(which_type, preferences):

    # Check if the which_type variable is valid,
    # so if it is not either 'vanilla' or
    # 'plugin' which is inputted, send error
    # and stop the program immediately
    if which_type != 'vanilla' and which_type != 'plugin':
        logger_sys.log_message(f"ERROR: Yaml data loading inputted key '{which_type}' is not valid --> stopping program")
        cout(
            f"{COLOR_RED}ERROR: {COLOR_STYLE_BRIGHT}Yaml" +
            f"data loading inputted key '{which_type}' is not valid --> stopping program{COLOR_RESET_ALL}"
        )
        time.sleep(5)
        text_handling.exit_game()

    # Make these variables global
    global map, item, drinks, enemy, npcs, start_player
    global lists, zone, dialog, mission, mounts
    global map_plugin, item_plugin, drinks_plugin
    global enemy_plugin, npcs_plugin, start_player_plugin
    global lists_plugin, zone_plugin, dialog_plugin
    global mission_plugin, mounts_plugin, event_plugin

    cout()
    # Create a dir, where all game imgs/ files will
    # be stored. First, we create the directory if
    # he doesn't exist yet. If he already exists, empty
    # it. Same for scripts.
    if not os.path.exists(program_dir + "/temp"):
        os.mkdir(program_dir + "/temp")
    imgs_dir = program_dir + "/temp/imgs/"
    if not os.path.exists(imgs_dir):
        os.mkdir(imgs_dir)
    else:
        for file in os.listdir(imgs_dir):
            file = os.path.join(imgs_dir, file)
            os.remove(file)

    scripts_dir = program_dir + "/temp/scripts/"
    if not os.path.exists(scripts_dir):
        os.mkdir(scripts_dir)
    else:
        for file in os.listdir(scripts_dir):
            file = os.path.join(scripts_dir, file)
            os.remove(file)

    # Load the vanilla game data, and then if the inputted
    # `which_type` variable is equal to 'plugin', also
    # load every data of every plugin in the folder, if
    # this one is activated. Then merge all the different
    # variables created, and return them to the game engine

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
        task_event = progress.add_task("[cyan]Loading Game Events Data...", total=100)
        task_mount = progress.add_task("[cyan]Loading Game Mounts Data...", total=100)

        with open(program_dir + "/game/data/map.yaml") as f:
            map = yaml_handling.safe_load(f)
        progress.update(task_map, total=len(list(map)))
        for i in list(map):
            check_yaml.examine_map_point(map[i])
            progress.update(task_map, advance=1)

        with open(program_dir + "/game/data/items.yaml") as f:
            item = yaml_handling.safe_load(f)
        progress.update(task_item, total=len(list(item)))
        for i in list(item):
            check_yaml.examine_item(item[i])
            progress.update(task_item, advance=1)

        with open(program_dir + "/game/data/drinks.yaml") as f:
            drinks = yaml_handling.safe_load(f)
        progress.update(task_drink, total=len(list(drinks)))
        for i in list(drinks):
            check_yaml.examine_drink(drinks[i])
            progress.update(task_drink, advance=1)

        with open(program_dir + "/game/data/enemies.yaml") as f:
            enemy = yaml_handling.safe_load(f)
        progress.update(task_enemy, total=len(list(enemy)))
        for i in list(enemy):
            check_yaml.examine_enemy(enemy[i])
            progress.update(task_enemy, advance=1)

        with open(program_dir + "/game/data/npcs.yaml") as f:
            npcs = yaml_handling.safe_load(f)
        progress.update(task_npc, total=len(list(npcs)))
        for i in list(npcs):
            check_yaml.examine_npc(npcs[i])
            progress.update(task_npc, advance=1)

        with open(program_dir + "/game/data/start.yaml") as f:
            progress.update(task_start, advance=1)
            start_player = yaml_handling.safe_load(f)
            progress.update(task_start, advance=1)
            check_yaml.examine(program_dir + "/game/data/start.yaml")
        progress.update(task_start, advance=1)

        with open(program_dir + "/game/data/lists.yaml") as f:
            lists = yaml_handling.safe_load(f)
        progress.update(task_lists, total=len(list(lists)))
        for i in list(lists):
            check_yaml.examine_list(lists[i])
            progress.update(task_lists, advance=1)

        with open(program_dir + "/game/data/zone.yaml") as f:
            zone = yaml_handling.safe_load(f)
        progress.update(task_zone, total=len(list(zone)))
        for i in list(zone):
            check_yaml.examine_zone(zone[i])
            progress.update(task_zone, advance=1)

        with open(program_dir + "/game/data/dialog.yaml") as f:
            dialog = yaml_handling.safe_load(f)
        progress.update(task_dialog, total=len(list(dialog)))
        for i in list(dialog):
            check_yaml.check_dialog_conversations(dialog, i)
            progress.update(task_dialog, advance=.5)
            check_yaml.examine_dialog(dialog[i])
            progress.update(task_dialog, advance=.5)

        with open(program_dir + "/game/data/mission.yaml") as f:
            mission = yaml_handling.safe_load(f)
        progress.update(task_mission, total=len(list(mission)))
        for i in list(mission):
            check_yaml.examine_mission(mission[i])
            progress.update(task_mission, advance=1)

        with open(program_dir + "/game/data/events.yaml") as f:
            event = yaml_handling.safe_load(f)
        progress.update(task_event, total=len(list(event)))
        for i in list(event):
            check_yaml.examine_event(event[i])
            progress.update(task_event, advance=1)

        with open(program_dir + "/game/data/mounts.yaml") as f:
            mounts = yaml_handling.safe_load(f)
        progress.update(task_mount, total=len(list(mounts)))
        for i in list(mounts):
            check_yaml.examine_mount(mounts[i])
            progress.update(task_mount, advance=1)

        # Add the images and the scripts to the shared folder
        for image in os.listdir(program_dir + "/game/imgs"):
            image_path = os.path.join(program_dir + "/game/imgs/", image)
            shutil.copy(image_path, imgs_dir + image)
        for script in os.listdir(program_dir + "/game/scripts"):
            script_path = os.path.join(program_dir + "/game/scripts/", script)
            shutil.copy(script_path, scripts_dir + script)

    if which_type == 'plugin':
        for what_plugin in os.listdir(program_dir + "/plugins/"):
            what_plugin_config = program_dir + "/plugins/" + what_plugin + "/.game.BOW"

            if not os.path.isfile(what_plugin_config):
                with open(what_plugin_config, "w") as f:
                    f.write("True")

            with open(what_plugin_config, "r") as f:
                if f.readlines()[0] == "True":

                    logger_sys.log_message(f"INFO: Loading plugin '{what_plugin}' data")

                    with Progress() as progress:
                        task_map = progress.add_task(f"[cyan]Loading Plugin '{what_plugin}' Map Data...", total=100)
                        task_item = progress.add_task(f"[cyan]Loading Plugin '{what_plugin}' Items Data...", total=100)
                        task_drink = progress.add_task(f"[cyan]Loading Plugin '{what_plugin}' Drinks Data...", total=100)
                        task_enemy = progress.add_task(f"[cyan]Loading Plugin '{what_plugin}' Enemies Data...", total=100)
                        task_npc = progress.add_task(f"[cyan]Loading Plugin '{what_plugin}' NPCS Data...", total=100)
                        task_start = progress.add_task(f"[cyan]Loading Plugin '{what_plugin}' Start Data...", total=3)
                        task_lists = progress.add_task(f"[cyan]Loading Plugin '{what_plugin}' Lists Data...", total=100)
                        task_zone = progress.add_task(f"[cyan]Loading Plugin '{what_plugin}' Zones Data...", total=100)
                        task_dialog = progress.add_task(f"[cyan]Loading Plugin '{what_plugin}' Dialogs Data...", total=100)
                        task_mission = progress.add_task(f"[cyan]Loading Plugin '{what_plugin}' Missions Data...", total=100)
                        task_event = progress.add_task(f"[cyan]Loading Plugin '{what_plugin}' Events Data...", total=100)
                        task_mount = progress.add_task(f"[cyan]Loading Plugin '{what_plugin}' Mounts Data...", total=100)
                        task_requirements = progress.add_task(f"[cyan]Loading Plugin '{what_plugin}' Requirements...", total=100)

                        with open(program_dir + "/plugins/" + what_plugin + "/map.yaml") as f:
                            map_plugin = yaml_handling.safe_load(f)
                        progress.update(task_map, total=len(list(map_plugin)))
                        for i in list(map_plugin):
                            check_yaml.examine_map_point(map_plugin[i])
                            progress.update(task_map, advance=1)

                        with open(program_dir + "/plugins/" + what_plugin + "/items.yaml") as f:
                            item_plugin = yaml_handling.safe_load(f)
                        progress.update(task_item, total=len(list(item_plugin)))
                        for i in list(item_plugin):
                            check_yaml.examine_item(item_plugin[i])
                            progress.update(task_item, advance=1)

                        with open(program_dir + "/plugins/" + what_plugin + "/drinks.yaml") as f:
                            drinks_plugin = yaml_handling.safe_load(f)
                        progress.update(task_drink, total=len(list(drinks_plugin)))
                        for i in list(drinks_plugin):
                            check_yaml.examine_drink(drinks_plugin[i])
                            progress.update(task_drink, advance=1)

                        with open(program_dir + "/plugins/" + what_plugin + "/enemies.yaml") as f:
                            enemy_plugin = yaml_handling.safe_load(f)
                        progress.update(task_enemy, total=len(list(enemy_plugin)))
                        for i in list(enemy_plugin):
                            check_yaml.examine_enemy(enemy_plugin[i])
                            progress.update(task_enemy, advance=1)

                        with open(program_dir + "/plugins/" + what_plugin + "/npcs.yaml") as f:
                            npcs_plugin = yaml_handling.safe_load(f)
                        progress.update(task_npc, total=len(list(npcs_plugin)))
                        for i in list(npcs_plugin):
                            check_yaml.examine_npc(npcs_plugin[i])
                            progress.update(task_npc, advance=1)

                        with open(program_dir + "/plugins/" + what_plugin + "/start.yaml") as f:
                            progress.update(task_start, advance=1)
                            start_player_plugin = yaml_handling.safe_load(f)
                            progress.update(task_start, advance=1)
                            check_yaml.examine(program_dir + "/plugins/" + what_plugin + "/start.yaml")
                        progress.update(task_start, advance=1)

                        with open(program_dir + "/plugins/" + what_plugin + "/lists.yaml") as f:
                            lists_plugin = yaml_handling.safe_load(f)
                        progress.update(task_lists, total=len(list(lists_plugin)))
                        for i in list(lists_plugin):
                            check_yaml.examine_list(lists_plugin[i])
                            progress.update(task_lists, advance=1)

                        with open(program_dir + "/plugins/" + what_plugin + "/zone.yaml") as f:
                            zone_plugin = yaml_handling.safe_load(f)
                        progress.update(task_zone, total=len(list(zone_plugin)))
                        for i in list(zone_plugin):
                            check_yaml.examine_zone(zone_plugin[i])
                            progress.update(task_zone, advance=1)

                        with open(program_dir + "/plugins/" + what_plugin + "/dialog.yaml") as f:
                            dialog_plugin = yaml_handling.safe_load(f)
                        progress.update(task_dialog, total=len(list(dialog_plugin)))
                        for i in list(dialog_plugin):
                            check_yaml.check_dialog_conversations(dialog_plugin, i)
                            progress.update(task_dialog, advance=.5)
                            check_yaml.examine_dialog(dialog_plugin[i])
                            progress.update(task_dialog, advance=.5)

                        with open(program_dir + "/plugins/" + what_plugin + "/mission.yaml") as f:
                            mission_plugin = yaml_handling.safe_load(f)
                        progress.update(task_mission, total=len(list(mission_plugin)))
                        for i in list(mission_plugin):
                            check_yaml.examine_mission(mission_plugin[i])
                            progress.update(task_mission, advance=1)

                        with open(program_dir + "/plugins/" + what_plugin + "/events.yaml") as f:
                            event_plugin = yaml_handling.safe_load(f)
                        progress.update(task_event, total=len(list(event_plugin)))
                        for i in list(event_plugin):
                            check_yaml.examine_event(event_plugin[i])
                            progress.update(task_event, advance=1)

                        with open(program_dir + "/plugins/" + what_plugin + "/mounts.yaml") as f:
                            mounts_plugin = yaml_handling.safe_load(f)
                        progress.update(task_mount, total=len(list(mounts_plugin)))
                        for i in list(mounts_plugin):
                            check_yaml.examine_mount(mounts_plugin[i])
                            progress.update(task_mount, advance=1)

                        logger_sys.log_message(f"INFO: Loading plugin '{what_plugin}' python module requirements")
                        requirements_file = program_dir + '/plugins/' + what_plugin + "/requirements.txt"
                        try:
                            f = open(requirements_file)
                            modules = f.readlines()
                            progress.update(task_requirements, total=len(modules))
                            for line in modules:
                                line = str(line).replace('\n', '')
                                logger_sys.log_message(f"INFO: Trying to install python module '{line}'")
                                script_handling.install_requirement(line)
                                progress.update(task_requirements, advance=1)
                        except Exception as error:
                            logger_sys.log_message(f"WARNING: Couldn't install plugin '{what_plugin}' python module requirements")
                            logger_sys.log_message(f"DEBUG: '{error}'")
                            progress.update(task_requirements, advance=100)

                        # Merge the loaded plugin data to the main variables
                        map = map | map_plugin
                        item = item | item_plugin
                        drinks = drinks | drinks_plugin
                        enemy = enemy | enemy_plugin
                        npcs = npcs | npcs_plugin
                        start_player = start_player | start_player_plugin
                        lists = lists | lists_plugin
                        zone = zone | zone_plugin
                        dialog = dialog | dialog_plugin
                        mission = mission | mission_plugin
                        event = event | event_plugin
                        mounts = mounts | mounts_plugin

                        # Add the images and scripts to the shared folder
                        for image in os.listdir(program_dir + "/plugins/" + what_plugin + "/imgs/"):
                            image_path = os.path.join(program_dir + "/plugins/" + what_plugin + "/imgs/", image)
                            shutil.copy(image_path, imgs_dir + image)
                        for script in os.listdir(program_dir + "/plugins/" + what_plugin + "/scripts/"):
                            script_path = os.path.join(program_dir + "/plugins/" + what_plugin + "/scripts/", script)
                            shutil.copy(script_path, scripts_dir + script)

    # Run integration tests
    if preferences["game data analyzing"]:
        with Progress() as progress:
            task_verify = progress.add_task(f"[cyan]Analzing Data...", total=None)
            check_yaml.verify_data(
                map, item, drinks, enemy, npcs, start_player, lists,
                zone, dialog, mission, mounts, event
            )
            progress.update(task_verify, total=1)
            progress.update(task_verify, advance=1)

    return map, item, drinks, enemy, npcs, start_player, lists, zone, dialog, mission, mounts, event


def update_game_data(preferences, latest_game_data_version):
    # Update python modules
    logger_sys.log_message("INFO: Starting game python module requirements install process")
    cout(COLOR_STYLE_BRIGHT + "Installing and updating python module requirements..." + COLOR_RESET_ALL)
    cout(COLOR_STYLE_DIM + "This may take a few seconds, sorry for the waiting" + COLOR_RESET_ALL)
    first_timer = time.time()

    requirements = io.StringIO(temporary_git_file_download(
        'requirements.txt', 'https://github.com/Dungeons-of-Kathallion/Bane-Of-Wargs.git'
    )).readlines()
    requirements_length = len(requirements)
    count = 0
    for module in requirements:
        cout(f"{COLOR_BLUE}{count}{COLOR_RESET_ALL}/{COLOR_GREEN}{requirements_length}{COLOR_RESET_ALL}", end="\r")
        module = module.replace('\n', '')
        logger_sys.log_message(f"INFO: Trying to install python module '{module}'")
        script_handling.install_requirement(module)

        count += 1
    cout(f"{COLOR_GREEN}{requirements_length}{COLOR_RESET_ALL}/{COLOR_GREEN}{requirements_length}{COLOR_RESET_ALL}")

    last_timer = time.time()
    process_time = round(last_timer - first_timer, 4)
    logger_sys.log_message(f"INFO: Process of installing game python module requirements completed in {process_time} seconds")

    # Download game data
    logger_sys.log_message("INFO: Downloading game data to update it")
    cout(COLOR_STYLE_BRIGHT + "Downloading game data..." + COLOR_RESET_ALL)
    cout(COLOR_STYLE_DIM + "This may take a few seconds, sorry for the waiting" + COLOR_RESET_ALL)
    cout(f"{COLOR_BLUE}0{COLOR_RESET_ALL}/{COLOR_GREEN}4{COLOR_RESET_ALL}", end="\r")
    download_branch = str(preferences["game data download"]["branch"])
    download_repo = str(preferences["game data download"]["repository"])
    download_org = str(preferences["game data download"]["org"])

    logger_sys.log_message("INFO: Downloading game yaml schemas files from github")

    first_timer = time.time()
    # Download yaml schema files
    fsspec_download('schemas/', program_dir + '/game/schemas', download_branch, download_repo, download_org)
    cout(f"{COLOR_BLUE}1{COLOR_RESET_ALL}/{COLOR_GREEN}4{COLOR_RESET_ALL}", end="\r")

    logger_sys.log_message("INFO: Downloading game data files from github")
    # Download data files
    fsspec_download('data/', program_dir + '/game/data', download_branch, download_repo, download_org)
    cout(f"{COLOR_BLUE}2{COLOR_RESET_ALL}/{COLOR_GREEN}4{COLOR_RESET_ALL}", end="\r")

    logger_sys.log_message("INFO: Downloading game images .txt files from github")
    # Download images .txt files
    fsspec_download('imgs/', program_dir + '/game/imgs', download_branch, download_repo, download_org)
    cout(f"{COLOR_BLUE}3{COLOR_RESET_ALL}/{COLOR_GREEN}4{COLOR_RESET_ALL}", end="\r")

    logger_sys.log_message("INFO: Downloading game scripts .py files from github")
    # Download scripts .py files
    fsspec_download('scripts/', program_dir + '/game/scripts', download_branch, download_repo, download_org)

    logger_sys.log_message("INFO: Downloading credits.txt file from github")
    # Download scripts .py files
    fsspec_download('credits.txt', program_dir + '/game/docs/credits.txt', download_branch, download_repo, download_org)

    cout(f"{COLOR_GREEN}4{COLOR_RESET_ALL}/{COLOR_GREEN}4{COLOR_RESET_ALL}")
    cout("Done")
    last_timer = time.time()
    process_time = round(last_timer - first_timer, 4)
    logger_sys.log_message(f"INFO: Process of downloading game data to update it completed in {process_time} seconds")

    # Update the 'VERSION.bow' file
    with open(f"{program_dir}/game/VERSION.bow", 'w') as f:
        f.write(str(latest_game_data_version))


def fsspec_download(github_file, destination_point, download_branch, download_repo, download_org):
    try:
        destination = destination_point
        fs = fsspec.filesystem("github", org=download_org, repo=download_repo, sha=download_branch)
        fs.get(fs.ls(github_file), destination)
    except Exception as error:
        cout(
            COLOR_YELLOW + COLOR_STYLE_BRIGHT + "WARNING:" + COLOR_RESET_ALL +
            " an error occurred when trying to download a github file to '" +
            destination + "'"
        )
        cout(COLOR_YELLOW + "Check the log files for more information" + COLOR_RESET_ALL)
        logger_sys.log_message(f"WARNING: An error occurred when downloading github file to '{destination}'")
        logger_sys.log_message(f"DEBUG: target file-->'{github_file}'; destination file-->'{destination_point}'")
        logger_sys.log_message(f"DEBUG: branch/tag: '{download_branch}'; repo: '{download_repo}'; org: '{download_org}'")
        logger_sys.log_message("DEBUG: " + str(error))
        cout(COLOR_YELLOW + str(error) + COLOR_RESET_ALL)
        time.sleep(.5)
        return False
    return True


def temporary_git_file_download(selected_file, url):
    global file_text_data
    # Create a temporary directory to after
    # clone the repository and select the chosen
    # file and export its data into a string

    try:
        temporary_dir = tempfile.mkdtemp()
        logger_sys.log_message(f"INFO: Creating temporary directory at '{temporary_dir}'")

        download_org = url.split('github.com/', 1)[1].split('/', 1)[0]
        download_repo = url.split('github.com/', 1)[1].split('/', 1)[1].replace('.git', '')
        fs = fsspec.filesystem("github", org=download_org, repo=download_repo)
        fs.get(fs.ls(selected_file), temporary_dir)

        with open(
            temporary_dir + '/' + os.path.basename(os.path.normpath(selected_file)), 'r'
        ) as f:
            file_text_data = f.read()
    except Exception as error:
        cout(
            COLOR_YELLOW + COLOR_STYLE_BRIGHT + "WARNING:" + COLOR_RESET_ALL +
            f" an error occurred when trying to download file '{selected_file}' from git" +
            f" url '{url}'"
        )
        logger_sys.log_message(
            f"WARNING: An error occurred when downloading file '{selected_file}' from git url" +
            f" '{url}'"
        )
        logger_sys.log_message("DEBUG: " + str(error))
        time.sleep(3)
        file_text_data = "null"

    return file_text_data


def open_file(file_path):
    try:
        editor = os.environ['EDITOR']
    except KeyError:
        editor = 'nano'
    logger_sys.log_message(f"INFO: Editing file '{file_path}' with editor '{editor}'")
    subprocess.call([editor, file_path])
