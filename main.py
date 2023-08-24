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
    for character in new_input:
        sys.stdout.write(character)
        sys.stdout.flush()
        time.sleep(.05)


def exit_game():
    time.sleep(1.5)
    print(COLOR_YELLOW + "Warning: closing game now" + COLOR_RESET_ALL)
    time.sleep(.5)
    os.system('clear')
    exit(1)

menu = True

# main menu start
while menu:
    with open('preferences.yaml', 'r') as f:
        preferences = yaml.safe_load(f)
    time.sleep(.5)
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
                play = 1
                time.sleep(.5)
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
        repo = Repo('.git')
        assert not repo.bare
        git = repo.git
        git.pull()
        text = "Finished Updating."
        print_speech_text_effect(text)
    else:
        os.system('clear')
        exit(1)

# funcion to search through the map file
def search(x, y):
    global map_location
    for i in range(0, map["coordinate count"]):
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
            print(line + " INVENTORY: " + COLOR_STYLE_BRIGHT + COLOR_CYAN + str(len(player["inventory"])) + COLOR_RESET_ALL + "/" + COLOR_STYLE_BRIGHT + COLOR_CYAN + str(player["inventory slots"]) + COLOR_RESET_ALL)
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

# gameplay here:
def run(play):
    print(separator)
    print(COLOR_GREEN + COLOR_STYLE_BRIGHT + "Reserved keys:" + COLOR_RESET_ALL)
    print(COLOR_BLUE + COLOR_STYLE_BRIGHT + "N: "+ COLOR_RESET_ALL + "Go north" + COLOR_RESET_ALL)
    print(COLOR_BLUE + COLOR_STYLE_BRIGHT + "S: "+ COLOR_RESET_ALL + "Go south" + COLOR_RESET_ALL)
    print(COLOR_BLUE + COLOR_STYLE_BRIGHT + "E: " + COLOR_RESET_ALL + "Go east" + COLOR_RESET_ALL)
    print(COLOR_BLUE + COLOR_STYLE_BRIGHT + "W: " + COLOR_RESET_ALL + "Go west" + COLOR_RESET_ALL)
    print(COLOR_BLUE + COLOR_STYLE_BRIGHT + "D: " + COLOR_RESET_ALL + "Access to your diary.")
    print(COLOR_BLUE + COLOR_STYLE_BRIGHT + "I: " + COLOR_RESET_ALL + "View items. When in this view, type the name of an item to examine it." + COLOR_RESET_ALL)
    print(COLOR_BLUE + COLOR_STYLE_BRIGHT + "Q: " + COLOR_RESET_ALL + "Quit game")
    print(" ")
    print(COLOR_GREEN + COLOR_STYLE_BRIGHT + "Hints:" + COLOR_RESET_ALL)
    print("If you find an item on the ground, type the name of the item to take it.")
    print("Some items have special triggers, which will often be stated in the description. Others can only be activated in certain situations, like in combat.")
    print(separator)
    print(" ")

    loading = 4
    while loading > 0:
        print("Loading game... ▅▃▁", end='\r')
        time.sleep(.15)
        print("Loading game... ▅▅▃", end='\r')
        time.sleep(.15)
        print("Loading game... ▅▅▅", end='\r')
        time.sleep(.15)
        print("Loading game... ▃▅▅", end='\r')
        time.sleep(.15)
        print("Loading game... ▁▃▅", end='\r')
        time.sleep(.15)
        print("Loading game... ▃▅▅", end='\r')
        time.sleep(.15)
        print("Loading game... ▅▅▃", end='\r')
        time.sleep(.15)
        print("Loading game... ▅▅▁", end='\r')
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

        player["armor protection"] = global_armor_protection

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
        player["agility"] = global_agility

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
            print("You can go East ►" + "     " + COLOR_BLUE + COLOR_STYLE_BRIGHT + "H: " + COLOR_RESET_ALL + "Enter hostel if you're near one")
        else:
            print("                 " + "     " + COLOR_BLUE + COLOR_STYLE_BRIGHT + "H: " + COLOR_RESET_ALL + "Enter hostel if you're near one")
        if "West" not in map["point" + str(map_location)]["blocked"]:
            print("You can go West ◄" + "     " + COLOR_BLUE + COLOR_STYLE_BRIGHT + "Q: " + COLOR_RESET_ALL + "Quit & save")
        else:
            print("                 " + "     " + COLOR_BLUE + COLOR_STYLE_BRIGHT + "Q: " + COLOR_RESET_ALL + "Quit & save")

        text = '='
        print_separator(text)

        is_in_village = False
        is_in_hostel = False
        if zone[map_zone]["type"] == "village" or zone[map_zone]["type"] == "hostel":
            print("NEWS:")
            village_news = zone[map_zone]["news"]
            village_news_len = len(village_news)
            choose_rand_news = random.randint(0, ( village_news_len - 1 ))
            choose_rand_news = village_news[int(choose_rand_news)]
            print(choose_rand_news)
            text = '='
            print_separator(text)
        if zone[map_zone]["type"] == "village":
            is_in_village = True
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
        if "None" not in map["point" + str(map_location)]["item"] and map_location not in player["taken items"]:
            map_items = str(map["point" + str(map_location)]["item"])
            map_items = map_items.replace('[', '')
            map_items = map_items.replace(']', '')
            map_items = map_items.replace("'", '')
            take_item = "There are these items on the ground: " + map_items
            print(take_item)
            print("")
        if "None" not in map["point" + str(map_location)]["npc"] and map_location not in player["met npcs"]:
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
                    else:
                        text = COLOR_YELLOW + "You cannot buy that items because it would cause your gold to be negative." + COLOR_RESET_ALL
                        print_long_string(text)
                    if drinks[which_drink]["healing level"] == "max health":
                        player["health"] = player["max health"]
                    else:
                        player["health"] += drinks[which_drink]["healing level"]
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

        if map["point" + str(map_location)]["enemy"] > 0 and map_location not in player["defeated enemies"]:
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
                battle.get_enemy_stats(player, item, enemy, map, map_location, lists, choose_rand_enemy, choosen_enemy, choosen_item, enemy_items_number, enemy_total_inventory)
                if not already_encountered:
                    battle.encounter_text_show(player, item, enemy, map, map_location, enemies_remaining, lists)
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
                if player["cheat"] < 3:
                    cheatcode = input("What is the not-die code? ")
                    if cheatcode == "43590":
                        player["cheat"] += 1
                        player["health"] = player["max health"]
                    else:
                        player = start_player
                        play = 0
                        return play
                else:
                    print("You've cheated too much! No more lives!")
                    time.sleep(1)
                    player = start_player
                    play = 0
                    return play
        elif day_time == COLOR_RED + COLOR_STYLE_BRIGHT + "NIGHT" + COLOR_RESET_ALL and round(random.uniform(.20, .80), 3) > 0.7 and zone[map_zone]["type"] != "hostel" and zone[map_zone]["type"] != "village":
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
                battle.get_enemy_stats(player, item, enemy, map, map_location, lists, choose_rand_enemy, choosen_enemy, choosen_item, enemy_items_number, enemy_total_inventory)
                if not already_encountered:
                    battle.encounter_text_show(player, item, enemy, map, map_location, enemies_remaining, lists)
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
                if player["cheat"] < 3:
                    cheatcode = input("What is the not-die code? ")
                    if cheatcode == "43590":
                        player["cheat"] += 1
                        player["health"] = player["max health"]
                    else:
                        player = start_player
                        play = 0
                        return play
                else:
                    print("You've cheated too much! No more lives!")
                    time.sleep(1)
                    player = start_player
                    play = 0
                    return play
        command = input("> ")
        print(" ")
        if command.lower().startswith('go'):
            print(COLOR_YELLOW + "Rather than saying Go <direction>, simply say <direction>." + COLOR_RESET_ALL)
            time.sleep(1.5)
        elif command.lower().startswith('n'):
            for i in range(0, map["coordinate count"]):
                point_i = map["point" + str(i)]
                point_x, point_y = point_i["x"], point_i["y"] - 1
                # print(i, point_x, point_y, player)
                if point_x == player["x"] and point_y == player["y"]:
                    future_map_location = i
            if "North" in map["point" + str(map_location)]["blocked"]:
                print(COLOR_YELLOW + "You cannot go that way." + COLOR_RESET_ALL)
                time.sleep(1)
            elif "None" not in map["point" + str(future_map_location)]["key"]["required keys"]:
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
                        player["y"] += 1

                text = '='
                print_separator(text)
            else:
                player["y"] += 1
        elif command.lower().startswith('s'):
            if "South" in map["point" + str(map_location)]["blocked"]:
                print(COLOR_YELLOW + "You cannot go that way." + COLOR_RESET_ALL)
                time.sleep(1)
            else:
                player["y"] -= 1
        elif command.lower().startswith('e'):
            if "East" in map["point" + str(map_location)]["blocked"]:
                print(COLOR_YELLOW + "You cannot go that way." + COLOR_RESET_ALL)
                time.sleep(1)
            else:
                player["x"] += 1
        elif command.lower().startswith('w'):
            if "West" in map["point" + str(map_location)]["blocked"]:
                print(COLOR_YELLOW + "You cannot go that way." + COLOR_RESET_ALL)
                time.sleep(1)
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
                        content_hostels = str(zone[which_zone]["content"]["hostels"])
                        content_hostels = content_hostels.replace('[', '')
                        content_hostels = content_hostels.replace(']', '')
                        content_hostels = content_hostels.replace("'", '')
                        text = "HOSTELS: " + content_hostels
                        print_long_string(text)
                    elif zone[which_zone]["type"] == "hostel":
                        current_hostel = zone[which_zone]
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
                print("NAME: " + which_item)
                print("TYPE: " + item[which_item]["type"])
                text = "DESCRIPTION: " + item[which_item]["description"]
                print_long_string(text)
                if item[which_item]["type"] == "Armor Piece: Chestplate" or item[which_item]["type"] == "Armor Piece: Boots" or item[which_item]["type"] == "Armor Piece: Leggings" or item[which_item]["type"] == "Armor Piece: Shield":
                    print("             Armor pieces can protect you in fights, more the armor protection is higher, the more it protects you.")
                    print("ARMOR PROTECTION: " + COLOR_GREEN + COLOR_STYLE_BRIGHT + str(item[which_item]["armor protection"]) + COLOR_RESET_ALL)
                if item[which_item]["type"] == "Weapon":
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
                else:
                    options = ['Get Rid', 'Exit']
                choice = enquiries.choose('', options)
                if choice == 'Equip':
                    if item[which_item]["type"] == "Weapon":
                        player["held item"] = which_item
                    elif item[which_item]["type"] == "Armor Piece: Chestplate":
                        player["held chestplate"] = which_item
                    elif item[which_item]["type"] == "Armor Piece: Leggins":
                        player["held leggings"] = which_item
                    elif item[which_item]["type"] == "Armor Piece: Boots":
                        player["held boots"] = which_item
                    elif item[which_item]["type"] == "Armor Piece: Shield":
                        player["held shield"] = which_item
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
        elif command.lower().startswith('h'):
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
                                    loading -= 1
                                day_time = float( float(round(player["elapsed time game days"] + 1, 0)) + .25 )
                                player["elapsed time game days"] = float( float(round(player["elapsed time game days"] + 1, 0)) + .25 )
                                continue_hostel_actions = False
                            else:
                                print(COLOR_YELLOW + "You don't own enough gold to sleep here." + COLOR_RESET_ALL)
                    elif choice == 'Buy Drink':
                        which_drink = input("Which drink do you want to buy? ")
                        if which_drink in zone[map_zone]["sells"]["drinks"] and ( drinks[which_drink]["gold"] * zone[map_zone]["cost value"] ) < player["gold"]:
                            remove_gold(str( drinks[which_drink]["gold"] * zone[map_zone]["cost value"] ))
                        else:
                            text = COLOR_YELLOW + "You cannot buy that items because it would cause your gold to be negative." + COLOR_RESET_ALL
                            print_long_string(text)
                        if drinks[which_drink]["healing level"] == "max health":
                            player["health"] = player["max health"]
                        else:
                            player["health"] += drinks[which_drink]["healing level"]
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

            else:
                print(COLOR_YELLOW + "You cannot find any near hostel." + COLOR_RESET_ALL)
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
        elif command in map["point" + str(map_location)]["item"]:
            if command in player["inventory"] and item[command]["type"] == "Utility":
                print(COLOR_YELLOW + "You cannot take that item." + COLOR_RESET_ALL)
                time.sleep(1.5)
            elif player["inventory slots remaining"] == 0:
                print(COLOR_YELLOW + "You cannot take that item because you're out of inventory slots." + COLOR_RESET_ALL)
                time.sleep(1.5)
            else:
                player["inventory"].append(command)
                player["taken items"].append(map_location)
        elif command.lower().startswith('q'):
            print(separator)
            play = 0
            return play
        else:
            print("'" + command + "' is not a valid command")
            time.sleep(2)
            print(" ")
        # get end time
        end_time = time.time()

        # calculate elapsed time
        elapsed_time = end_time - start_time
        elapsed_time = round(elapsed_time, 2)

        game_elapsed_time = 0.004167 * elapsed_time # 60 seconds irl = 0.25 days in-game
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

