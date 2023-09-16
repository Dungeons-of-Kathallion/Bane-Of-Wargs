import random
import yaml
import battle
import os
import sys
import time
import enquiries
import fade
import subprocess
import git
import readline
from git import Repo
from colorama import Fore, Back, Style, deinit, init
from colors import *

# initialize colorama
init()

os.system('clear')

# get terminal size
terminal_rows, terminal_columns = os.popen('stty size', 'r').read().split()

# says you are not playing.
play = 0

fought_enemy = False

separator = COLOR_STYLE_BRIGHT + "###############################" + COLOR_RESET_ALL

# get terminal size
import fcntl, termios, struct
h, w, hp, wp = struct.unpack('HHHH',
    fcntl.ioctl(0, termios.TIOCGWINSZ,
    struct.pack('HHHH', 0, 0, 0, 0)))
term_width = w

def print_title():
    if preferences["theme"] == "OFF":
        with open('imgs/Title' + str(preferences["title style"]) + '.txt', 'r') as f:
            print(f.read())
    else:
        if preferences["theme"] == "blackwhite":
            with open('imgs/Title' + str(preferences["title style"]) + '.txt', 'r') as f:
                faded_text = fade.blackwhite(f.read())
                print(faded_text)
        elif preferences["theme"] == "purplepink":
            with open('imgs/Title' + str(preferences["title style"]) + '.txt', 'r') as f:
                faded_text = fade.purplepink(f.read())
                print(faded_text)
        elif preferences["theme"] == "greenblue":
            with open('imgs/Title' + str(preferences["title style"]) + '.txt', 'r') as f:
                faded_text = fade.greenblue(f.read())
                print(faded_text)
        elif preferences["theme"] == "water":
            with open('imgs/Title' + str(preferences["title style"]) + '.txt', 'r') as f:
                faded_text = fade.water(f.read())
                print(faded_text)
        elif preferences["theme"] == "fire":
            with open('imgs/Title' + str(preferences["title style"]) + '.txt', 'r') as f:
                faded_text = fade.fire(f.read())
                print(faded_text)
        elif preferences["theme"] == "pinkred":
            with open('imgs/Title' + str(preferences["title style"]) + '.txt', 'r') as f:
                faded_text = fade.pinkred(f.read())
                print(faded_text)
        elif preferences["theme"] == "purpleblue":
            with open('imgs/Title' + str(preferences["title style"]) + '.txt', 'r') as f:
                faded_text = fade.purpleblue(f.read())
                print(faded_text)
        elif preferences["theme"] == "brazil":
            with open('imgs/Title' + str(preferences["title style"]) + '.txt', 'r') as f:
                faded_text = fade.brazil(f.read())
                print(faded_text)
        elif preferences["theme"] == "random":
            with open('imgs/Title' + str(preferences["title style"]) + '.txt', 'r') as f:
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


def exit_game():
    time.sleep(1.5)
    print(COLOR_YELLOW + "Warning: closing game now" + COLOR_RESET_ALL)
    time.sleep(.5)
    os.system('clear')
    exit(1)

menu = True

# main menu start
while menu:
    check_file_preferences = os.path.isfile("preferences.yaml")
    if check_file_preferences == False:
        with open("default preferences.yaml") as f:
            default_preferences = yaml.safe_load(f)
            dumped = yaml.dump(default_preferences)
        with open("preferences.yaml", "w") as f:
            f.write(dumped)
    with open('preferences.yaml', 'r') as f:
        preferences = yaml.safe_load(f)
    # try to update game
    if preferences["auto update"]:
        try:
            repo = Repo('.git')
            assert not repo.bare
            git = repo.git
            git.pull()
        except:
            pass
    else: time.sleep(.5)
    os.system('clear')
    print_title()

    options = ['Play Game', 'Manage Saves', 'Preferences', 'Check Update', 'Quit']
    choice = enquiries.choose('', options)
    os.system('clear')

    print_title()

    if choice == 'Play Game':
        options = ['Use Latest Preset', 'Play Vanilla', 'Play Plugin']
        choice = enquiries.choose('', options)
        using_latest_preset = False

        # load data files
        if choice == 'Use Latest Preset':
            using_latest_preset = True
            if preferences["latest preset"]["type"] == 'vanilla':
                with open("data/map.yaml") as f:
                    map = yaml.safe_load(f)

                with open("data/items.yaml") as f:
                    item = yaml.safe_load(f)

                with open("data/drinks.yaml") as f:
                    drinks = yaml.safe_load(f)

                with open("data/enemies.yaml") as f:
                    enemy = yaml.safe_load(f)

                with open("data/npcs.yaml") as f:
                    npcs = yaml.safe_load(f)

                with open("data/start.yaml") as f:
                    start_player = yaml.safe_load(f)

                with open("data/lists.yaml") as f:
                    lists = yaml.safe_load(f)

                with open("data/zone.yaml") as f:
                    zone = yaml.safe_load(f)

                with open("data/dialog.yaml") as f:
                    dialog = yaml.safe_load(f)

                with open("data/mounts.yaml") as f:
                    mounts = yaml.safe_load(f)
            else:

                what_plugin = preferences["latest preset"]["plugin"]

                check_file = os.path.exists("plugins/" + what_plugin )
                if check_file == False:
                    print(COLOR_RED + COLOR_STYLE_BRIGHT + "ERROR: Couldn't find plugin '" + what_plugin + "'" + COLOR_RESET_ALL)
                    play = 0
                    exit(1)
                with open("plugins/" + what_plugin + "/map.yaml") as f:
                    map = yaml.safe_load(f)

                with open("plugins/" + what_plugin + "/items.yaml") as f:
                    item = yaml.safe_load(f)

                with open("plugins/" + what_plugin + "/drinks.yaml") as f:
                    drinks = yaml.safe_load(f)

                with open("plugins/" + what_plugin + "/enemies.yaml") as f:
                    enemy = yaml.safe_load(f)

                with open("plugins/" + what_plugin + "/npcs.yaml") as f:
                    npcs = yaml.safe_load(f)

                with open("plugins/" + what_plugin + "/start.yaml") as f:
                    start_player = yaml.safe_load(f)

                with open("plugins/" + what_plugin + "/lists.yaml") as f:
                    lists = yaml.safe_load(f)

                with open("plugins/" + what_plugin + "/zone.yaml") as f:
                    zone = yaml.safe_load(f)

                with open("plugins/" + what_plugin + "/dialog.yaml") as f:
                    dialog = yaml.safe_load(f)

                with open("plugins/" + what_plugin + "/mounts.yaml") as f:
                    mounts = yaml.safe_load(f)

            open_save = preferences["latest preset"]["save"]
            save_file = "saves/save_" + open_save + ".yaml"
            check_file = os.path.isfile(save_file)
            if check_file == False:
                print(COLOR_RED + COLOR_STYLE_BRIGHT + "ERROR: Couldn't find save file '" + save_file + "'" + COLOR_RESET_ALL)
                play = 0
                exit(1)
            with open(save_file) as f:
                player = yaml.safe_load(f)
            play = 1
            menu = False

        elif choice == 'Play Plugin':
            text = "Please select a plugin to use"
            print_speech_text_effect(text)
            res = []

            for search_for_saves in os.listdir('plugins/'):
                res.append(search_for_saves)

            res.remove('.gitkeep')

            what_plugin = input(COLOR_STYLE_BRIGHT + "Current plugins: " + COLOR_RESET_ALL + COLOR_GREEN + str(res) + COLOR_RESET_ALL + " ")
            preferences["latest preset"]["type"] = "plugin"
            preferences["latest preset"]["plugin"] = what_plugin

            check_file = os.path.exists("plugins/" + what_plugin )
            if check_file == False:
                print(COLOR_RED + COLOR_STYLE_BRIGHT + "ERROR: Couldn't find plugin '" + what_plugin + "'" + COLOR_RESET_ALL)
                play = 0
                exit(1)
            with open("plugins/" + what_plugin + "/map.yaml") as f:
                map = yaml.safe_load(f)

            with open("plugins/" + what_plugin + "/items.yaml") as f:
                item = yaml.safe_load(f)

            with open("plugins/" + what_plugin + "/drinks.yaml") as f:
                drinks = yaml.safe_load(f)

            with open("plugins/" + what_plugin + "/enemies.yaml") as f:
                enemy = yaml.safe_load(f)

            with open("plugins/" + what_plugin + "/npcs.yaml") as f:
                npcs = yaml.safe_load(f)

            with open("plugins/" + what_plugin + "/start.yaml") as f:
                start_player = yaml.safe_load(f)

            with open("plugins/" + what_plugin + "/lists.yaml") as f:
                lists = yaml.safe_load(f)

            with open("plugins/" + what_plugin + "/zone.yaml") as f:
                zone = yaml.safe_load(f)

            with open("plugins/" + what_plugin + "/dialog.yaml") as f:
                dialog = yaml.safe_load(f)

            with open("plugins/" + what_plugin + "/mounts.yaml") as f:
                mounts = yaml.safe_load(f)
        else:
            preferences["latest preset"]["type"] = "vanilla"
            preferences["latest preset"]["plugin"] == "none"
            with open("data/map.yaml") as f:
                map = yaml.safe_load(f)

            with open("data/items.yaml") as f:
                item = yaml.safe_load(f)

            with open("data/drinks.yaml") as f:
                drinks = yaml.safe_load(f)

            with open("data/enemies.yaml") as f:
                enemy = yaml.safe_load(f)

            with open("data/npcs.yaml") as f:
                npcs = yaml.safe_load(f)

            with open("data/start.yaml") as f:
                start_player = yaml.safe_load(f)

            with open("data/lists.yaml") as f:
                lists = yaml.safe_load(f)

            with open("data/zone.yaml") as f:
                zone = yaml.safe_load(f)

            with open("data/dialog.yaml") as f:
                dialog = yaml.safe_load(f)

            with open("data/mounts.yaml") as f:
                mounts = yaml.safe_load(f)

        if using_latest_preset == False:
            text = "Please select an action:"
            print_speech_text_effect(text)
            options = ['Open Save', 'New Save']
            choice = enquiries.choose('', options)

            if choice == 'Open Save':
                res = []

                for search_for_saves in os.listdir('saves/'):
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
                preferences["latest preset"]["save"] = open_save

                save_file = "saves/save_" + open_save + ".yaml"
                check_file = os.path.isfile(save_file)
                if check_file == False:
                    print(COLOR_RED + COLOR_STYLE_BRIGHT + "ERROR: Couldn't find save file '" + save_file + "'" + COLOR_RESET_ALL)
                    play = 0
                    exit(1)
                with open(save_file) as f:
                    player = yaml.safe_load(f)
                play = 1
                menu = False
            else:
                text = "Please name your save: "
                print_speech_text_effect(text)
                enter_save_name = input('> ')
                player = start_player
                dumped = yaml.dump(player)
                save_name = "saves/save_" + enter_save_name + ".yaml"
                save_name_backup = "saves/~0 save_" + enter_save_name + ".yaml"
                check_file = os.path.isfile(save_name)
                if check_file == True:
                    print(COLOR_RED + COLOR_STYLE_BRIGHT + "ERROR: Save file '" + save_name + "'" + " already exists" + COLOR_RESET_ALL)
                    play = 0
                    exit_game()
                with open(save_name, "w") as f:
                    f.write(dumped)
                with open(save_name_backup, "w") as f:
                    f.write(dumped)
                save_file = save_name
                with open(save_file) as f:
                    player = yaml.safe_load(f)
                play = 1
                menu = False

    elif choice == 'Manage Saves':

        res = []

        for search_for_saves in os.listdir('saves/'):
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
        choice = enquiries.choose('', options)
        if choice == 'Edit Save':
            text = "Please select a save to edit."
            print_speech_text_effect(text)
            open_save = input(COLOR_STYLE_BRIGHT + "Current saves: " + COLOR_RESET_ALL + COLOR_GREEN + str(res) + COLOR_RESET_ALL + " ")
            check_file = os.path.isfile("saves/save_" + open_save + ".yaml")
            if check_file == False:
                print(COLOR_RED + COLOR_STYLE_BRIGHT + "ERROR: Save file '" + "saves/save_" + open_save + ".yaml" + "'" + " does not exists" + COLOR_RESET_ALL)
                play = 0
            text = "Select an action for the selected save."
            print_speech_text_effect(text)
            options = ['Rename Save', 'Manually Edit Save']
            choice = enquiries.choose('', options)
            if choice == 'Rename Save':
                rename_name = input("Select a new name for the save: ")
                os.rename("saves/save_" + open_save + ".yaml", "saves/save_" + rename_name + ".yaml")
            else:
                save_to_open ="saves/save_" + open_save + ".yaml"
                try:
                    editor = os.environ['EDITOR']
                except KeyError:
                    editor = 'nano'
                subprocess.call([editor, save_to_open])
        else:
            text = "Please select a save to delete."
            print_speech_text_effect(text)
            open_save = input(COLOR_STYLE_BRIGHT + "Current saves: " + COLOR_RESET_ALL + COLOR_GREEN + str(res) + COLOR_RESET_ALL + " ")
            check_file = os.path.isfile("saves/save_" + open_save + ".yaml")
            if check_file == False:
                print(COLOR_RED + COLOR_STYLE_BRIGHT + "ERROR: Save file '" + "saves/save_" + open_save + ".yaml" + "'" + " does not exists" + COLOR_RESET_ALL)
                play = 0
            check = input("Are you sure you want to delete the following save (y/n)")
            if check.lower().startswith('y'):
                os.remove("saves/save_" + open_save + ".yaml")
                os.remove("saves/~0 save_" + open_save + ".yaml")
    elif choice == 'Preferences':
        try:
            editor = os.environ['EDITOR']
        except KeyError:
            editor = 'nano'
        subprocess.call([editor, "preferences.yaml"])
    elif choice == 'Check Update':
        text = "Checking for updates..."
        print_speech_text_effect(text)
        try:
            repo = Repo('.git')
            assert not repo.bare
            git = repo.git
            git.pull()
        except:
            print(COLOR_RED + "ERROR: Could not update repo: somthing went wrong when pulling. Please try to pull the repo manually on the command line" + COLOR_RESET_ALL)
            time.sleep(5)
        text = "Finished Updating."
        print_speech_text_effect(text)
    else:
        os.system('clear')
        exit(1)

# funcion to search through the map file
def search(x, y):
    global map_location
    map_point_count = int(len(list(map)))
    for i in range(0, map_point_count):
        point_i = map["point" + str(i)]
        point_x, point_y = point_i["x"], point_i["y"]
        # print(i, point_x, point_y, player)
        if point_x == player["x"] and point_y == player["y"]:
            map_location = i
            return map_location


def add_gold(amount):
    player_gold = player["gold"]
    player_gold += float(amount)
    player["gold"] = round(player_gold, 2)

def remove_gold(amount):
    player_gold = player["gold"]
    player_gold -= float(amount)
    player["gold"] = round(player_gold, 2)

def print_zone_map(zone_name):
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
    if preferences["latest preset"]["type"] == "vanilla":
        with open('imgs/' + npc + ".txt") as f:
            to_print = str(f.read())
    else:
        with open('plugins/' +  str(preferences["latest preset"]["plugin"]) + '/imgs/' + npc + ".txt") as f:
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
    if preferences["latest preset"]["type"] == "vanilla":
        with open('imgs/' + enemy + ".txt") as f:
            to_print = str(f.read())
    else:
        with open('plugins/' +  str(preferences["latest preset"]["plugin"]) + '/imgs/' + enemy + ".txt") as f:
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
    map_point_count = int(len(list(map))) - 1
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

        text = "You need the following key(s) to enter this location, if you decide to use it, you may loose it:"
        print_long_string(text)

        keys_list = str(map["point" + str(future_map_location)]["key"]["required keys"])
        keys_list = keys_list.replace("'", '')
        keys_list = keys_list.replace("[", ' -')
        keys_list = keys_list.replace("]", '')
        keys_list = keys_list.replace(", ", '\n -')

        keys_len = len(map["point" + str(future_map_location)]["key"]["required keys"])

        text = '='
        print_separator(text)

        options = ['Continue', 'Leave']
        choice = enquiries.choose('', options)

        count = 0

        have_necessary_keys = True

        if choice == 'Continue':
            while count < ( keys_len ) and have_necessary_keys == True:

                choosen_key = map["point" + str(future_map_location)]["key"]["required keys"][int(count)]

                if choosen_key not in player["inventory"]:
                    have_necessary_keys = False
                else:
                    if map["point" + str(future_map_location)]["key"]["remove key"] == True:
                        player["inventory"].remove(choosen_key)

                count += 1

            if not have_necessary_keys:
                print(" ")
                text = COLOR_YELLOW + "You don't have the necessary key(s) to enter this locations"
                print_long_string(text)
                time.sleep(1.5)
            if have_necessary_keys:
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

def print_dialog(current_dialog):
    current_dialog = dialog[str(current_dialog)]
    dialog_len = len(current_dialog["phrases"])
    if "scene" in current_dialog:
        if preferences["latest preset"]["type"] == 'vanilla':
            with open('imgs/' + str(current_dialog["scene"]) + '.txt') as f:
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
            with open('plugins/' + str(preferences["latest preset"]["plugin"]) + '/imgs/' + str(current_dialog["scene"]) + '.txt') as f:
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
    while count < dialog_len:
        text = str(current_dialog["phrases"][int(count)])
        print_speech_text_effect(text)
        count += 1
    if current_dialog["use actions"] == True:
        actions = current_dialog["actions"]
        if "give item" in actions:
            given_items = actions["give item"]
            given_items_len = len(given_items)
            count = 0
            while count < given_items_len:
                selected_item = given_items[count]
                player["inventory"].append(selected_item)
                count += 1
        if "add attributes" in actions:
            count = 0
            added_attributes = actions["add attributes"]
            added_attributes_len = len(added_attributes)
            while count < added_attributes_len:
                selected_attribute = added_attributes[count]
                player["attributes"].append(selected_attribute)
                count += 1
        if "health modification" in actions:
            if "diminution" in actions["health modification"]:
                player["health"] -= actions["health modification"]["diminution"]
            if "augmentation" in actions["health modification"]:
                player["health"] += actions["health modification"]["augmentation"]
            if "max health" in actions["health modification"]:
                if "diminution" in actions["health modification"]["max health"]:
                    player["max health"] -= actions["health modification"]["max health"]["diminution"]
                if "augmentation" in actions["health modification"]["max health"]:
                    player["max health"] += actions["health modification"]["max health"]["augmentation"]
        if "gold modification" in actions:
            if "diminution" in actions["gold modification"]:
                player["gold"] -= actions["gold modification"]["diminution"]
            if "augmentation" in actions["gold modification"]:
                player["gold"] += actions["gold modification"]["augmentation"]
        if "remove item" in actions:
            removed_items = actions["remove item"]
            removed_items_len = len(removed_items)
            count = 0
            while count < removed_items_len:
                selected_item = removed_items[count]
                player["inventory"].remove(selected_item)
                count += 1
        if "add to diary" in actions:
            if "known zones" in actions["add to diary"]:
                added_visited_zones = actions["add to diary"]["known zones"]
                added_visited_zones_len = len(added_visited_zones)
                count = 0
                while count < added_visited_zones_len:
                    selected_zone = added_visited_zones[count]
                    player["visited zones"].append(selected_zone)
                    count += 1
            if "known enemies" in actions["add to diary"]:
                added_known_enemies = actions["add to diary"]["known enemies"]
                added_known_enemies_len = len(added_known_enemies)
                count = 0
                while count < added_known_enemies_len:
                    selected_enemy = added_known_enemies[count]
                    player["enemies list"].append(selected_enemy)
                    count += 1
            if "known npcs" in actions["add to diary"]:
                added_known_npcs = actions["add to diary"]["known npcs"]
                added_known_npcs_len = len(added_known_npcs)
                count = 0
                while count < added_known_npcs_len:
                    selected_npc = added_known_npcs[count]
                    player["met npcs name"].append(selected_npc)
                    count += 1
        if "remove to diary" in actions:
            if "known zones" in actions["remove to diary"]:
                removed_visited_zones = actions["remove to diary"]["known zones"]
                removed_visited_zones_len = len(removed_visited_zones)
                count = 0
                while count < removed_visited_zones_len:
                    selected_zone = removed_visited_zones[count]
                    player["visited zones"].remove(selected_zone)
                    count += 1
            if "known enemies" in actions["remove to diary"]:
                removed_known_enemies = actions["remove to diary"]["known enemies"]
                removed_known_enemies_len = len(removed_known_enemies)
                count = 0
                while count < removed_known_enemies_len:
                    selected_enemy = removed_known_npcs[count]
                    player["enemies list"].remove(selected_enemy)
                    count += 1
            if "known npcs" in actions["remove to diary"]:
                removed_known_npcs = actions["remove to diary"]["known npcs"]
                removed_known_npcs_len = len(removed_known_npcs)
                count = 0
                while count < removed_known_npcs_len:
                    selected_npc = removed_known_npcs[count]
                    player["met npcs name"].append(selected_npc)
                    count += 1
        if "use drink" in actions:
            used_drinks = actions["use drink"]
            used_drinks_len = len(used_drinks)
            count = 0
            while count < used_drinks_len:
                selected_drink = used_drinks_len[count]
                if drinks[selected_drink]["healing level"] == "max health":
                    player["health"] = player["max health"]
                else:
                    player["health"] += drinks[selected_drink]["healing level"]

def generate_random_uuid():
    import uuid
    random_uuid = uuid.uuid4()
    random_uuid = str(random_uuid)
    random_uuid = random_uuid.replace('UUID', '')
    random_uuid = random_uuid.replace('(', '')
    random_uuid = random_uuid.replace(')', '')
    random_uuid = random_uuid.replace("'", '')
    return random_uuid

def check_for_item(item_name):
    item_exist = False
    if str(item_name) in list(item):
        item_exist = True
    return item_exist

def check_weapon_next_upgrade_name(item_name):
    weapon_next_upgrade_name = str(item_name)
    check_weapon_max_upgrade_number = check_weapon_max_upgrade(str(weapon_next_upgrade_name))
    if item[weapon_next_upgrade_name]["upgrade tier"] == check_weapon_max_upgrade_number:
        weapon_next_upgrade_name = None
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

    return weapon_next_upgrade_name

def check_weapon_max_upgrade(item_name):
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

    return weapon_next_upgrade_items

# gameplay here:
def run(play):
    if preferences["speed up"] != True:
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

        # get terminal size
        terminal_rows, terminal_columns = os.popen('stty size', 'r').read().split()

        # clear text
        os.system('clear')

        # update player ridded mount location:
        if player["current mount"] in player["mounts"]:
            map_location = search(player["x"], player["y"])
            player["mounts"][player["current mount"]]["location"] = "point" + str(map_location)

        # update player current mount stats following its level
        if player["current mount"] in player["mounts"]:
            current_mount_data = player["mounts"][str(player["current mount"])]
            current_mount_type = str(current_mount_data["mount"])
            if current_mount_data["level"] >= 1:
                player["mounts"][str(player["current mount"])]["stats"]["agility addition"] = round(mounts[current_mount_type]["stats"]["agility addition"] + ( mounts[current_mount_type]["levels"]["level stat additions"]["agility addition"] * ( round(current_mount_data["level"]) - 1 )), 3)
                player["mounts"][str(player["current mount"])]["stats"]["resistance addition"] = round(mounts[current_mount_type]["stats"]["resistance addition"] + ( mounts[current_mount_type]["levels"]["level stat additions"]["resistance addition"] * ( round(current_mount_data["level"]) - 1 )), 3)
                
        # verify if player worn equipment are in his inventory
        if str(player["held item"]) not in player["player inventory"]:
            player["held item"] = " "
        if str(player["held chestplate"]) not in player["player inventory"]:
            player["held chestplate"] = " "
        if str(player["held leggings"]) not in player["player inventory"]:
            player["held leggings"] = " "
        if str(player["held boots"]) not in player["player inventory"]:
            player["held boots"] = " "
        if str(player["held shield"]) not in player["player inventory"]:
            player["held shield"] = " "

        # always round player health to an integer amount
        player["health"] = int(round(player["health"]))

        # update player equipment items
        if player["held item"] not in player["inventory"]:
            player["held item"] == " "
        if player["held chestplate"] not in player["inventory"]:
            player["held chestplate"] == " "
        if player["held boots"] not in player["inventory"]:
            player["held boots"] == " "
        if player["held leggings"] not in player["inventory"]:
            player["held leggings"] == " "
        if player["held shield"] not in player["inventory"]:
            player["held shield"] == " "

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
        # check player map location
        if map_location == None:
            text = COLOR_RED + COLOR_STYLE_BRIGHT + "FATAL ERROR: You are in an undefined location. This could have been the result of using or not using a plugin. Verify you are using the right plugin for this save or manullay modify your player coordinates in the 'Manage Saves' in the main menu. The game will close in 10 secs." + COLOR_RESET_ALL
            print_long_string(text)
            time.sleep(10)
            os.system('clear')
            exit(1)
        map_zone = map["point" + str(map_location)]["map zone"]

        # add current player location and map
        # zone to visited areas in the player
        # save file if there aren't there yet
        if map_location not in player["visited points"]:
            player["visited points"].append(map_location)

        if map_zone not in player["visited zones"]:
            player["visited zones"].append(map_zone)

        # init curses

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

        # player start dialog
        if player["start dialog"]["heard start dialog"] == False:
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
        if zone[map_zone]["type"] == "village" or zone[map_zone]["type"] == "hostel" or zone[map_zone]["type"] == "stable" or zone[map_zone]["type"] == "blacksmith" or zone[map_zone]["type"] == "forge":
            print("NEWS:")
            village_news = zone[map_zone]["news"]
            village_news_len = len(village_news)
            choose_rand_news = random.randint(0, ( village_news_len - 1 ))
            choose_rand_news = village_news[int(choose_rand_news)]
            print_long_string(choose_rand_news)
            text = '='
            print_separator(text)
        if "dialog" in map["point" + str(map_location)] and map_location not in player["heard dialogs"]:
            current_dialog = map["point" + str(map_location)]["dialog"]
            has_required_attributes = True
            if "to display" in dialog[str(current_dialog)]:
                if "player attributes" in dialog[str(current_dialog)]["to display"]:
                    count = 0
                    required_attributes = dialog[str(current_dialog)]["to display"]["player attributes"]
                    required_attributes_len = len(required_attributes)
                    while count < required_attributes_len and has_required_attributes == True:
                        selected_attribute = required_attributes[count]
                        if selected_attribute not in player["attributes"]:
                            has_required_attributes = False
                        count += 1
            if has_required_attributes == True:
                print_dialog(current_dialog)
                player["heard dialogs"].append(map_location)
                text = '='
                print_separator(text)
        if zone[map_zone]["type"] == "village":
            is_in_village = True
        if zone[map_zone]["type"] == "forge":
            is_in_forge = True
            current_forge = zone[map_zone]
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
        if zone[map_zone]["type"] == "blacksmith":
            is_in_blacksmith = True
            current_black_smith = zone[map_zone]
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
        if zone[map_zone]["type"] == "stable":
            is_in_stable = True
            current_stable = zone[map_zone]
            print(str(current_stable["name"]) + ":")
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
        if zone[map_zone]["type"] == "hostel":
            is_in_hostel = True
            current_hostel = zone[map_zone]
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
        if "item" in map["point" + str(map_location)] and map_location not in player["taken items"]:
            map_items = str(map["point" + str(map_location)]["item"])
            map_items = map_items.replace('[', '')
            map_items = map_items.replace(']', '')
            map_items = map_items.replace("'", '')
            take_item = "There are these items on the ground: " + map_items
            print(take_item)
            print("")
        if "npc" in map["point" + str(map_location)] and map_location not in player["met npcs"]:
            current_npc = str(map["point" + str(map_location)]["npc"])
            current_npc = current_npc.replace('[', '')
            current_npc = current_npc.replace(']', '')
            current_npc = current_npc.replace("'", '')
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
            while count < npc_speech_len:
                text = str(npcs[current_npc]["speech"][int(count)])
                print_speech_text_effect(text)
                count += 1
            text = '='
            print_separator(text)
            options = []
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
                choice = enquiries.choose('', options)
                if choice == 'Buy Drink':
                    which_drink = input("Which drink do you want to buy from him? ")
                    if which_drink in npcs[current_npc]["sells"]["drinks"] and ( drinks[which_drink]["gold"] * npcs[current_npc]["cost value"] ) < player["gold"]:
                        remove_gold(str( drinks[which_drink]["gold"] * npcs[current_npc]["cost value"] ))
                        if drinks[which_drink]["healing level"] == "max health":
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
                    if drinks[which_item]["healing level"] == "max health":
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

        if "enemy" in map["point" + str(map_location)] and map_location not in player["defeated enemies"]:
            enemies_remaining = map["point" + str(map_location)]["enemy"]
            already_encountered = False
            while enemies_remaining > 0:
                list_enemies = lists[ map["point" + str(map_location)]["enemy type"]]
                choose_rand_enemy = random.randint(0, len(list_enemies) - 1)
                choose_rand_enemy = list_enemies[choose_rand_enemy]
                choosen_enemy = enemy[choose_rand_enemy]

                enemy_total_inventory = choosen_enemy["inventory"]

                enemy_items_number = len(enemy_total_inventory)
                choosen_item = enemy_total_inventory[random.randint(0, enemy_items_number - 1)]
                defeat_percentage = battle.calculate_player_risk(player, item, enemies_remaining, choosen_enemy, enemy)
                battle.get_enemy_stats(player, item, enemy, map, map_location, lists, choose_rand_enemy, choosen_enemy, choosen_item, enemy_items_number, enemy_total_inventory, enemies_remaining)
                if not already_encountered:
                    battle.encounter_text_show(player, item, enemy, map, map_location, enemies_remaining, lists, defeat_percentage)
                    already_encountered = True
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
                    print("Your enemy dropped a/an " + choosen_item)
                options = ['Grab Item', 'Continue']
                drop = enquiries.choose('', options)
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
                print_long_string(text)
                finished = input()
                player = start_player
                play = 0
                return play

        elif day_time == COLOR_RED + COLOR_STYLE_BRIGHT + "NIGHT" + COLOR_RESET_ALL and round(random.uniform(.20, .80), 3) > .7 and zone[map_zone]["type"] != "hostel" and zone[map_zone]["type"] != "stable" and zone[map_zone]["type"] != "village" and zone[map_zone]["type"] != "blacksmith" and zone[map_zone]["type"] != "forge":
            enemies_remaining = random.randint(1, 4)
            already_encountered = False
            while enemies_remaining > 0:
                list_enemies = lists["generic"]
                choose_rand_enemy = random.randint(0, len(list_enemies) - 1)
                choose_rand_enemy = list_enemies[choose_rand_enemy]
                choosen_enemy = enemy[choose_rand_enemy]

                enemy_total_inventory = choosen_enemy["inventory"]

                enemy_items_number = len(enemy_total_inventory)
                choosen_item = enemy_total_inventory[random.randint(0, enemy_items_number - 1)]
                defeat_percentage = battle.calculate_player_risk(player, item, enemies_remaining, choosen_enemy, enemy)
                battle.get_enemy_stats(player, item, enemy, map, map_location, lists, choose_rand_enemy, choosen_enemy, choosen_item, enemy_items_number, enemy_total_inventory, enemies_remaining)
                if not already_encountered:
                    battle.encounter_text_show(player, item, enemy, map, map_location, enemies_remaining, lists, defeat_percentage)
                    already_encountered = True
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
                    print("Your enemy dropped a/an " + choosen_item)
                options = ['Grab Item', 'Continue']
                drop = enquiries.choose('', options)
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
                print_long_string(text)
                finished = input()
                player = start_player
                play = 0
                return play
        command = input("> ")
        print(" ")
        if "item" in map["point" + str(map_location)] and command in map["point" + str(map_location)]["item"]:
            if command in player["inventory"] and item[command]["type"] == "Utility":
                print(COLOR_YELLOW + "You cannot take that item." + COLOR_RESET_ALL)
                time.sleep(1.5)
            elif player["inventory slots remaining"] == 0:
                print(COLOR_YELLOW + "You cannot take that item because you're out of inventory slots." + COLOR_RESET_ALL)
                time.sleep(1.5)
            else:
                player["inventory"].append(command)
                player["taken items"].append(map_location)
        elif command.lower().startswith('go'):
            print(COLOR_YELLOW + "Rather than saying Go <direction>, simply say <direction>." + COLOR_RESET_ALL)
            time.sleep(1.5)
        elif command.lower().startswith('n'):
            if "North" in map["point" + str(map_location)]["blocked"]:
                print(COLOR_YELLOW + "You cannot go that way." + COLOR_RESET_ALL)
                time.sleep(1)
            elif "key" in map["point" + str(map_location)]:
                check_for_key("north")
            else:
                player["y"] += 1
        elif command.lower().startswith('s'):
            if "South" in map["point" + str(map_location)]["blocked"]:
                print(COLOR_YELLOW + "You cannot go that way." + COLOR_RESET_ALL)
                time.sleep(1)
            elif "key" in map["point" + str(map_location)]:
                check_for_key("south")
            else:
                player["y"] -= 1
        elif command.lower().startswith('e'):
            if "East" in map["point" + str(map_location)]["blocked"]:
                print(COLOR_YELLOW + "You cannot go that way." + COLOR_RESET_ALL)
                time.sleep(1)
            elif "key" in map["point" + str(map_location)]:
                check_for_key("east")
            else:
                player["x"] += 1
        elif command.lower().startswith('w'):
            if "West" in map["point" + str(map_location)]["blocked"]:
                print(COLOR_YELLOW + "You cannot go that way." + COLOR_RESET_ALL)
                time.sleep(1)
            elif "key" in map["point" + str(map_location)]:
                check_for_key("west")
            else:
                player["x"] -= 1
        elif command.lower().startswith('d'):
            text = '='
            print_separator(text)
            print("ADVENTURER NAME: " + str(preferences["latest preset"]["save"]))
            print("ELAPSED DAYS: " + COLOR_STYLE_BRIGHT + COLOR_MAGENTA + str(round(player["elapsed time game days"], 1)) + COLOR_RESET_ALL)
            text = '='
            print_separator(text)
            options = ['Visited Places', 'Encountered Monsters', 'Encountered People']
            choice = enquiries.choose('', options)
            if choice == 'Visited Places':
                print("VISITED PLACES: ")
                zones_list = str(player["visited zones"])
                zones_list = zones_list.replace("'", '')
                zones_list = zones_list.replace("[", ' -')
                zones_list = zones_list.replace("]", '')
                zones_list = zones_list.replace(", ", '\n -')
                print(zones_list)
                text = '='
                print_separator(text)
                which_zone = input("> ")
                if which_zone in player["visited zones"]:
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
                finished = input("")
            elif choice == 'Encountered Monsters':
                print("ENCOUNTERED MONSTERS: ")
                enemies_list = str(player["enemies list"])
                enemies_list = enemies_list.replace("'None', ", '')
                enemies_list = enemies_list.replace("'", '')
                enemies_list = enemies_list.replace("[", ' -')
                enemies_list = enemies_list.replace("]", '')
                enemies_list = enemies_list.replace(", ", '\n -')
                print(enemies_list)
                text = '='
                print_separator(text)
                which_enemy = input("> ")
                if which_enemy == "None":
                    print(" ")
                    print(COLOR_YELLOW + "You don't know about that enemy." + COLOR_RESET_ALL)
                    time.sleep(1.5)
                elif which_enemy in player["enemies list"]:

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
                    print(" ")
                    print(COLOR_YELLOW + "You don't know about that enemy." + COLOR_RESET_ALL)
                    time.sleep(1.5)
            elif choice == 'Encountered People':
                print("ENCOUNTERED PEOPLE: ")
                enemies_list = str(player["met npcs names"])
                enemies_list = enemies_list.replace("'None', ", '')
                enemies_list = enemies_list.replace("'", '')
                enemies_list = enemies_list.replace("[", ' -')
                enemies_list = enemies_list.replace("]", '')
                enemies_list = enemies_list.replace(", ", '\n -')
                print(enemies_list)
                text = '='
                print_separator(text)
                which_npc = input("> ")
                if which_npc == "None":
                    print(" ")
                    print(COLOR_YELLOW + "You don't know about that people." + COLOR_RESET_ALL)
                    time.sleep(1.5)
                elif which_npc in player["met npcs names"]:

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
                    time.sleep(1.5)
        elif command.lower().startswith('i'):
            text = '='
            print_separator(text)
            print("ARMOR PROTECTION: " + COLOR_GREEN + COLOR_STYLE_BRIGHT + str(player["armor protection"]) + COLOR_RESET_ALL + COLOR_RED + COLOR_STYLE_BRIGHT + " (" + COLOR_RESET_ALL + "More it's higher, the less you'll take damages in fights" + COLOR_RED + COLOR_STYLE_BRIGHT + ")" + COLOR_RESET_ALL)
            print("AGILITY: " + COLOR_MAGENTA + COLOR_STYLE_BRIGHT + str(player["agility"]) + COLOR_RESET_ALL + COLOR_RED + COLOR_STYLE_BRIGHT + " (" + COLOR_RESET_ALL + "More it's higher, the more you'll have a chance to dodge attacks" + COLOR_RED + COLOR_STYLE_BRIGHT + ")" + COLOR_RESET_ALL)
            if player["held item"] != " ":
                print("CRITICAL HIT CHANCE: " + COLOR_CYAN + COLOR_STYLE_BRIGHT + str(item[player["held item"]]["critical hit chance"]) + COLOR_RESET_ALL + COLOR_RED + COLOR_STYLE_BRIGHT + " (" + COLOR_RESET_ALL + "More it's higher, the more you'll have a chance to deal critical attacks" + COLOR_RED + COLOR_STYLE_BRIGHT + ")" + COLOR_RESET_ALL)
            print(" ")
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
            if which_item in player["inventory"]:
                text = '='
                print_separator(text)
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
                choice = enquiries.choose('', options)
                if choice == 'Equip':
                    if item[which_item]["type"] == "Weapon":
                        player["held item"] = which_item
                    elif item[which_item]["type"] == "Armor Piece: Chestplate":
                        player["held chestplate"] = which_item
                    elif item[which_item]["type"] == "Armor Piece: Leggings":
                        player["held leggings"] = which_item
                    elif item[which_item]["type"] == "Armor Piece: Boots":
                        player["held boots"] = which_item
                    elif item[which_item]["type"] == "Armor Piece: Shield":
                        player["held shield"] = which_item
                elif choice == 'Consume':
                    if item[which_item]["healing level"] == "max health":
                        player["health"] = player["max health"]
                    else:
                        player["health"] += item[which_item]["healing level"]
                        player["max health"] += item[which_item]["max bonus"]
                    player["inventory"].remove(which_item)
                elif choice == 'Get Rid':
                    text = "You won't be able to get this item back if your throw it away. Are you sure you want to throw away this item"
                    print_long_string(text)
                    ask = input("? (y/n) ")
                    if ask.lower().startswith('y'):
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
                print(COLOR_YELLOW + "You do not have that item." + COLOR_RESET_ALL)
                time.sleep(1.5)
        elif command.lower().startswith('z'):
            if zone[map_zone]["type"] == "hostel":
                text = '='
                print_separator(text)
                options = ['Sleep']
                if "None" not in zone[map_zone]["sells"]["drinks"]:
                    options += ['Buy Drink']
                if "None" not in zone[map_zone]["sells"]["items"]:
                    options += ['Buy Item']
                if "None" not in zone[map_zone]["buys"]["items"]:
                    options += ['Sell Item']
                options += ['Exit']
                continue_hostel_actions = True
                while continue_hostel_actions:
                    choice = enquiries.choose('', options)
                    if choice == 'Sleep':
                        print("Are you sure you want to spend the night here? It will ")
                        ask = input("cost you " + str(zone[map_zone]["sleep gold"]) + " gold (y/n) ")
                        text = '='
                        print_separator(text)
                        if ask.lower().startswith('y'):
                            if int(player["gold"]) > int(zone[map_zone]["sleep gold"]):
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
                                day_time = float( float(round(player["elapsed time game days"] + 1, 0)) + .25 )
                                player["elapsed time game days"] = float( float(round(player["elapsed time game days"] + 1, 0)) + .25 )
                                continue_hostel_actions = False
                                if player["health"] > player["max health"]:
                                    player["health"] = player["max health"]
                            else:
                                print(COLOR_YELLOW + "You don't own enough gold to sleep here." + COLOR_RESET_ALL)
                    elif choice == 'Buy Drink':
                        which_drink = input("Which drink do you want to buy? ")
                        if which_drink in zone[map_zone]["sells"]["drinks"] and ( drinks[which_drink]["gold"] * zone[map_zone]["cost value"] ) < player["gold"]:
                            remove_gold(str( drinks[which_drink]["gold"] * zone[map_zone]["cost value"] ))
                            if drinks[which_drink]["healing level"] == "max health":
                                player["health"] = player["max health"]
                            else:
                                player["health"] += drinks[which_drink]["healing level"]
                        else:
                            text = COLOR_YELLOW + "You cannot buy that items because it would cause your gold to be negative." + COLOR_RESET_ALL
                            print_long_string(text)
                    elif choice == 'Buy Item':
                        which_item = input("Which item do you want to buy? ")
                        if which_item in zone[map_zone]["sells"]["items"] and ( item[which_item]["gold"] * zone[map_zone]["cost value"] ) < player["gold"]:
                            if player["inventory slots remaining"] > 0:
                                player["inventory slots remaining"] -= 1
                                player["inventory"].append(which_item)
                                remove_gold(str( item[which_item]["gold"] * zone[map_zone]["cost value"] ))
                            else:
                                text = COLOR_YELLOW + "You cannot buy that items because it would cause your inventory slots to be negative." + COLOR_RESET_ALL
                                print_long_string(text)
                        else:
                            text = COLOR_YELLOW + "You cannot buy that items because it would cause your gold to be negative." + COLOR_RESET_ALL
                            print_long_string(text)
                    elif choice == 'Sell Item':
                        which_item = input("Which item do you want to sell? ")
                        if which_item in zone[map_zone]["buys"]["items"] and ( item[which_item]["gold"] * zone[map_zone]["cost value"] ) < player["gold"] and which_item in player["inventory"]:
                            player["inventory slots remaining"] -= 1
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
                            text = COLOR_YELLOW + "You cannot buy that items because it would cause your gold to be negative or because you don't own that item." + COLOR_RESET_ALL
                            print_long_string(text)
                    else:
                        continue_hostel_actions = False
            elif zone[map_zone]["type"] == "stable":
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
                while active_stable_menu:
                    action = enquiries.choose('', options)
                    if action == 'Buy Item':
                        which_item = input("Which item do you want to buy? ")
                        if which_item in zone[map_zone]["stable"]["sells"]["items"] and ( item[which_item]["gold"] * zone[map_zone]["cost value"] ) < player["gold"]:
                            if player["inventory slots remaining"] > 0:
                                player["inventory slots remaining"] -= 1
                                player["inventory"].append(which_item)
                                remove_gold(str( item[which_item]["gold"] * zone[map_zone]["cost value"] ))
                            else:
                                text = COLOR_YELLOW + "You cannot buy that items because it would cause your inventory slots to be negative." + COLOR_RESET_ALL
                                print_long_string(text)
                        else:
                            text = COLOR_YELLOW + "You cannot buy that items because it would cause your gold to be negative." + COLOR_RESET_ALL
                            print_long_string(text)
                    elif action == 'Buy Drink':
                        which_drink = input("Which drink do you want to buy? ")
                        if which_drink in zone[map_zone]["stable"]["sells"]["drinks"] and ( drinks[which_drink]["gold"] * zone[map_zone]["cost value"] ) < player["gold"]:
                            remove_gold(str( drinks[which_drink]["gold"] * zone[map_zone]["cost value"] ))
                            if drinks[which_drink]["healing level"] == "max health":
                                player["health"] = player["max health"]
                            else:
                                player["health"] += drinks[which_drink]["healing level"]
                        else:
                            text = COLOR_YELLOW + "You cannot buy that items because it would cause your gold to be negative." + COLOR_RESET_ALL
                            print_long_string(text)
                    elif action == 'Buy Mount':
                        which_mount = input("Which mount do you want to buy? ")
                        if which_mount in zone[map_zone]["stable"]["sells"]["mounts"]:
                            mount_cost = ( mounts[which_mount]["gold"] * zone[map_zone]["cost value"] )
                            if mount_cost < player["gold"]:
                                remove_gold(str(mount_cost))
                                generated_mount_uuid = generate_random_uuid()
                                print("How you mount should be named ?")
                                new_mount_name = input("> ")
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
                                player["mounts"][generated_mount_uuid] = mount_dict
                                text = "Your mount is currently deposited at the " + zone[map_zone]["name"] + "\nYou can ride it whenever you want."
                                print_speech_text_effect(text)
                                text = '='
                                print_separator(text)
                            else:
                                print(COLOR_YELLOW + "You don't own enough money to buy that mount" + COLOR_RESET_ALL)
                        else:
                            print(COLOR_YELLOW + "The current stable do not sell this mount" + COLOR_RESET_ALL)
                    elif action == 'Deposit Mount':
                        if player["current mount"] != " ":
                            current_mount_uuid = str(player["current mount"])
                            mount_data = player["mounts"][current_mount_uuid]
                            # check if required stables are in the stable attributes
                            required_mount_stable = str(mounts[str(mount_data["mount"])]["stable"]["required stable"])
                            if required_mount_stable in zone[map_zone]["stable"]["stables"]:
                                ask = input("Do you want to deposit your current mount " + mount_data["name"] + " ? (y/n) ")
                                if ask.lower().startswith('y'):
                                    player["current mount"] = " "
                                    player["mounts"][current_mount_uuid]["is deposited"] = True
                                    player["mounts"][current_mount_uuid]["deposited day"] = round(player["elapsed time game days"], 1)
                                    player["mounts"][current_mount_uuid]["location"] = str("point" + str(map_location))
                                text = "="
                                print_separator(text)
                            else:
                                print(COLOR_YELLOW + "This stable doesn't accept this type of mount." + COLOR_RESET_ALL)
                        else:
                            print(COLOR_YELLOW + "You don't have any mounts to deposit here." + COLOR_RESET_ALL)
                    elif action == 'Ride Mount':
                        if player["current mount"] == " ":
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
                                        remove_gold(mount_take_back_cost)
                                        player["current mount"] = str(which_mount_uuid)
                                        player["mounts"][which_mount_uuid]["is deposited"] = False
                                        player["mounts"][which_mount_uuid]["deposited day"] = 0
                                        player["mounts"][which_mount_uuid]["location"] = "point" + str(map_location)
                                else:
                                    print(COLOR_YELLOW + "You don't own enough money to take back your mount." + COLOR_RESET_ALL)
                            else:
                                text = COLOR_YELLOW + "You don't own that mount or the mount isn't deposited at this current location" + COLOR_RESET_ALL
                                print_long_string(text)
                        else:
                            text = COLOR_YELLOW + "You are currently already riding a mount. You need to deposit your current mount before riding an other one." + COLOR_RESET_ALL
                            print_long_string(text)
                    else:
                        active_stable_menu = False
            elif zone[map_zone]["type"] == "blacksmith":
                text = '='
                print_separator(text)

                options = ['Sell Equipment', 'Order Equipment', 'Upgrade Equipment', 'Check Order', 'Exit']
                continue_blacksmith_actions = True
                while continue_blacksmith_actions:
                    action = enquiries.choose('', options)
                    if action == 'Sell Equipment':
                        which_weapon = input("Which equipment do you want to sell? ")
                        if which_weapon in zone[map_zone]["blacksmith"]["buys"] and which_weapon in player["inventory"]:
                            add_gold(str( item[which_weapon]["gold"] * zone[map_zone]["cost value"] ))
                            player["inventory"].remove(which_weapon)
                        else:
                            text = COLOR_YELLOW + "You cannot sell that equipment because you dont own any of that weapon." + COLOR_RESET_ALL
                            print_long_string(text)
                    elif action == 'Order Equipment':
                        which_weapon = input("Which equipment do you want to order? ")
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
                            if required_items == True:
                                remove_gold(str( item[which_weapon]["gold"] * zone[map_zone]["cost value"] ))
                                count = 0
                                remaining_items_to_remove = len(zone[map_zone]["blacksmith"]["orders"][which_weapon]["needed materials"])
                                while count < len(player["inventory"]) and remaining_items_to_remove != 0:
                                    selected_item = zone[map_zone]["blacksmith"]["orders"][which_weapon]["needed materials"][count]
                                    player["inventory"].remove(selected_item)
                                    remaining_items_to_remove -= 1
                                    count += 1
                                order_uuid = generate_random_uuid()
                                order_dict = {
                                    "paid gold": zone[map_zone]["blacksmith"]["orders"][which_weapon]["gold"],
                                    "ordered weapon": which_weapon,
                                    "ordered day": player["elapsed time game days"],
                                    "ordered blacksmith": zone[map_zone]["name"],
                                    "time needed": zone[map_zone]["blacksmith"]["orders"][which_weapon]["time needed"],
                                    "has taken back order": "false"
                                }
                                player["orders"][order_uuid] = order_dict
                                text = "You'll be able to get your finished order in " + COLOR_MAGENTA + COLOR_STYLE_BRIGHT + str(zone[map_zone]["blacksmith"]["orders"][which_weapon]["time needed"]) + COLOR_RESET_ALL + " days."
                                print_long_string(text)
                            else:
                                text = COLOR_YELLOW + "You cannot order that equipment because you dont have the necessary items." + COLOR_RESET_ALL
                                print_long_string(text)
                        else:
                            text = COLOR_YELLOW + "You cannot order that weapon because you dont own enough money." + COLOR_RESET_ALL
                            print_long_string(text)
                    elif action == 'Upgrade Equipment':
                        which_weapon = input("Which equipment do you want to upgrade? ")
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
                                    if required_items == True:
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
                                        order_dict = {
                                            "paid gold": item[str(item_next_upgrade_name)]["gold"],
                                            "ordered weapon": str(item_next_upgrade_name),
                                            "ordered day": player["elapsed time game days"],
                                            "ordered blacksmith": zone[map_zone]["name"],
                                            "time needed": round(random.uniform(.55, 3.55), 2),
                                            "has taken back order": "false"
                                        }
                                        player["orders"][order_uuid] = order_dict
                                        text = "You'll be able to get your finished order in " + COLOR_MAGENTA + COLOR_STYLE_BRIGHT + str(player["orders"][order_uuid]["time needed"]) + COLOR_RESET_ALL + " days."
                                        print_long_string(text)
                                    else:
                                        print(COLOR_YELLOW + "You don't own the necessary items to upgrade" + COLOR_RESET_ALL)
                                else:
                                    print(COLOR_YELLOW + "You don't have enough gold to upgrade." + COLOR_RESET_ALL)
                            else:
                                print(COLOR_YELLOW + "You cannot upgrade this equipment further." + COLOR_RESET_ALL)
                        else:
                            print(COLOR_YELLOW + "You don't own that equipment" + COLOR_RESET_ALL)
                    elif action == 'Check Order':
                        player_orders = player["orders"]
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
                        player_orders_to_collect = player_orders_to_collect.replace("'", '')
                        player_orders_to_collect = player_orders_to_collect.replace("[", ' -')
                        player_orders_to_collect = player_orders_to_collect.replace("]", '')
                        player_orders_to_collect = player_orders_to_collect.replace(", ", '\n -')
                        print("ORDERS:")
                        print(player_orders_to_collect)
                        text = '='
                        print_separator(text)
                        which_order = input("> ")
                        if which_order in player_orders_number:
                            current_order_uuid = str(list(player["orders"])[int(which_order)])
                            text = '='
                            print_separator(text)

                            time_left = round(player["orders"][current_order_uuid]["ordered day"] + player["orders"][current_order_uuid]["time needed"] - player["elapsed time game days"], 1)
                            if time_left <= 0:
                                time_left = "READY TO COLLECT"
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
                            action = enquiries.choose('', options_order)
                            if action == 'Cancel Order':
                                text = "Are you sure you want to cancel this order? You will receive 75% of the gold you paid and you won't be able"
                                print_long_string(text)
                                ask =input(" to get your given items back. (y/n)")
                                if ask.lower().startswith('y'):
                                    # give player 75% of paid gold
                                    add_gold(player["orders"][current_order_uuid]["paid gold"] * ( 75 / 100 ))
                                    # remove order from player orders
                                    player["orders"].pop(current_order_uuid)
                            if action == 'Collect Order':
                                player["inventory"].append(str(player["orders"][current_order_uuid]["ordered weapon"]))
                                # remove order from player orders
                                player["orders"].pop(current_order_uuid)
                        else:
                            print(COLOR_YELLOW + "You don't have this order currently at this place." + COLOR_RESET_ALL)
                    else:
                        continue_blacksmith_actions = False
            elif zone[map_zone]["type"] == "forge":
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
                while continue_forge_actions:
                    choice = enquiries.choose('', options)
                    if choice == 'Sell Metals':
                        which_metal = input("Which metal do you want to sell? ")
                        if which_metal in current_forge["forge"]["buys"]:
                            metal_count = int(input("How many count of this metal you want to sell? "))
                            if player["inventory"].count(which_metal) >= metal_count:
                                add_gold(item[which_metal]["gold"] * current_forge["cost value"] * metal_count)
                                count = 0
                                while count < metal_count:
                                    player["inventory"].remove(which_metal)
                                    count += 1
                            else:
                                print(COLOR_YELLOW + "You don't own that many count of this metal" + COLOR_RESET_ALL)
                        else:
                            print(COLOR_YELLOW + "The current forge doesn't buys this metal" + COLOR_RESET_ALL)
                    elif choice == 'Buy Metals':
                        which_metal = input("Which metal do you want to buy? ")
                        if which_metal in current_forge["forge"]["sells"]:
                            metal_count = int(input("How many count of this metal you want to buy? "))
                            if player["gold"] >= item[which_metal]["gold"] * current_forge["cost value"] * metal_count:
                                remove_gold(item[which_metal]["gold"] * current_forge["cost value"] * metal_count)
                                count = 0
                                while count < metal_count:
                                    player["inventory"].append(which_metal)
                                    count += 1
                            else:
                                print(COLOR_YELLOW + "You don't own enough money to buy that many metal" + COLOR_RESET_ALL)
                        else:
                            print(COLOR_YELLOW + "The current forge doesn't sells this metal" + COLOR_RESET_ALL)
                    else:
                        continue_forge_actions = False
            else:
                print(COLOR_YELLOW + "You cannot find any near hostel, stable, blacksmith, forge or church." + COLOR_RESET_ALL)
                time.sleep(1.5)
        elif command.lower().startswith('y'):
            if "mounts" in player and player["mounts"] != '':
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

                    text = "DESCRIPTION: " + mounts[which_mount_data["mount"]]["description"]
                    print_long_string(text)

                    text = '='
                    print_separator(text)

                    finished = input("")
                else:
                    print(COLOR_YELLOW + "You don't have any mounts named like that." + COLOR_RESET_ALL)
                    time.sleep(1.5)
            else:
                print(COLOR_YELLOW + "It seems you don't own any mounts." + COLOR_RESET_ALL)
                time.sleep(1.5)
        elif command.lower().startswith('m'):
            if "Map" in player["inventory"]:
                print("**|**")
                print("*[+]*")
                print("**⊥**")
                print(" ")
            else:
                print("You do not have a map.")
                print(" ")
            finished = input(" ")
        elif command == "q" or command == "Q":
            print(separator)
            play = 0
        else:
            print("'" + command + "' is not a valid command")
            time.sleep(2)
            print(" ")
        # get end time
        end_time = time.time()

        # calculate elapsed time
        elapsed_time = end_time - start_time
        elapsed_time = round(elapsed_time, 2)

        game_elapsed_time = .004167 * elapsed_time # 60 seconds irl = .25 days in-game
        game_elapsed_time = round(game_elapsed_time, 2)

        player["elapsed time seconds"] = elapsed_time + player["elapsed time seconds"]
        player["elapsed time game days"] = game_elapsed_time + player["elapsed time game days"]

if play == 1:
    play = run(1)

# finish up and save
dumped = yaml.dump(player)

save_file_quit = save_file
with open(save_file_quit, "w") as f:
    f.write(dumped)

save_name_backup = save_file.replace('save_', '~0 save_')

with open(save_name_backup, "w") as f:
    f.write(dumped)

dumped = yaml.dump(preferences)

with open('preferences.yaml', 'w') as f:
    f.write(dumped)

# deinitialize colorame
deinit()
os.system('clear')

