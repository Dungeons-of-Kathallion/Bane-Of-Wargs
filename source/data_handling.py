# source imports
import logger_sys
import check_yaml
import text_handling
import script_handling
from colors import *
# external imports
import appdirs
import os
import git
import tempfile
import yaml
import time
import fsspec
import time
import io
import subprocess
from rich.progress import Progress


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

            logger_sys.log_message(f"INFO: Loading plugin '{what_plugin}' python module requirements")
            requirements_file = program_dir + '/plugins/' + what_plugin + "/requirements.txt"
            try:
                f = open(requirements_file)
                modules = f.readlines()
                progress.update(task_requirements, total=len(modules))
                for line in modules:
                    logger_sys.log_message(f"INFO: Trying to install python module '{line}'")
                    script_handling.install_requirement(line)
                    progress.update(task_requirements, advance=1)
            except Exception as error:
                logger_sys.log_message(f"WARNING: Couldn't install plugin '{what_plugin}' python module requirements")
                logger_sys.log_message(f"DEBUG: '{error}'")

            # Install the required modules

                progress.update(task_requirements, advance=100)
    return map, item, drinks, enemy, npcs, start_player, lists, zone, dialog, mission, mounts


def update_game_data(preferences, latest_game_data_version):
    # Update python modules
    logger_sys.log_message("INFO: Starting game python module requirements install process")
    print(COLOR_STYLE_BRIGHT + "Installing and updating python module requirements..." + COLOR_RESET_ALL)
    print(COLOR_STYLE_DIM + "This may take a few seconds, sorry for the waiting" + COLOR_RESET_ALL)
    first_timer = time.time()

    requirements = io.StringIO(temporary_git_file_download(
        'requirements.txt', 'https://github.com/Dungeons-of-Kathallion/Bane-Of-Wargs.git'
    )).readlines()
    requirements_length = len(requirements)
    count = 0
    for module in requirements:
        print(f"{COLOR_BLUE}{count}{COLOR_RESET_ALL}/{COLOR_GREEN}{requirements_length}{COLOR_RESET_ALL}", end="\r")
        module = module.replace('\n', '')
        logger_sys.log_message(f"INFO: Trying to install python module '{module}'")
        script_handling.install_requirement(module)

        count += 1
    print(f"{COLOR_GREEN}{requirements_length}{COLOR_RESET_ALL}/{COLOR_GREEN}{requirements_length}{COLOR_RESET_ALL}")

    last_timer = time.time()
    process_time = round(last_timer - first_timer, 4)
    logger_sys.log_message(f"INFO: Process of installing game python module requirements completed in {process_time} seconds")

    # Download game data
    logger_sys.log_message("INFO: Downloading game data to update it")
    print(COLOR_STYLE_BRIGHT + "Downloading game data..." + COLOR_RESET_ALL)
    print(COLOR_STYLE_DIM + "This may take a few seconds, sorry for the waiting" + COLOR_RESET_ALL)
    print(f"{COLOR_BLUE}0{COLOR_RESET_ALL}/{COLOR_GREEN}4{COLOR_RESET_ALL}", end="\r")
    download_branch = str(preferences["game data download"]["branch"])
    download_repo = str(preferences["game data download"]["repository"])
    download_org = str(preferences["game data download"]["org"])

    logger_sys.log_message("INFO: Downloading game yaml schemas files from github")

    first_timer = time.time()
    # Download yaml schema files
    fsspec_download('schemas/', program_dir + '/game/schemas', download_branch, download_repo, download_org)
    print(f"{COLOR_BLUE}1{COLOR_RESET_ALL}/{COLOR_GREEN}4{COLOR_RESET_ALL}", end="\r")

    logger_sys.log_message("INFO: Downloading game data files from github")
    # Download data files
    fsspec_download('data/', program_dir + '/game/data', download_branch, download_repo, download_org)
    print(f"{COLOR_BLUE}2{COLOR_RESET_ALL}/{COLOR_GREEN}4{COLOR_RESET_ALL}", end="\r")

    logger_sys.log_message("INFO: Downloading game images .txt files from github")
    # Download images .txt files
    fsspec_download('imgs/', program_dir + '/game/imgs', download_branch, download_repo, download_org)
    print(f"{COLOR_BLUE}3{COLOR_RESET_ALL}/{COLOR_GREEN}4{COLOR_RESET_ALL}", end="\r")

    logger_sys.log_message("INFO: Downloading game scripts .py files from github")
    # Download scripts .py files
    fsspec_download('scripts/', program_dir + '/game/scripts', download_branch, download_repo, download_org)

    print(f"{COLOR_GREEN}4{COLOR_RESET_ALL}/{COLOR_GREEN}4{COLOR_RESET_ALL}")
    print("Done")
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
        print(
            COLOR_YELLOW + COLOR_STYLE_BRIGHT + "WARNING:" + COLOR_RESET_ALL +
            " an error occurred when trying to download game data to '" +
            destination + "'."
        )
        logger_sys.log_message(f"WARNING: An error occurred when downloading game data to '{destination}'.")
        logger_sys.log_message("DEBUG: " + str(error))
        print(COLOR_YELLOW + str(error) + COLOR_RESET_ALL)
        time.sleep(.5)


def temporary_git_file_download(selected_file, url):
    global file_text_data
    # Create a temporary directory to after
    # clone the repository and select the chosen
    # file and export its data in a string

    temporary_dir = tempfile.mkdtemp()
    logger_sys.log_message(f"INFO: Creating temporary directory at '{temporary_dir}'")
    git.Repo.clone_from(url, temporary_dir, depth=1)

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
