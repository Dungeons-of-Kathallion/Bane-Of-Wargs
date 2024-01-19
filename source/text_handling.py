import logger_sys
import colors
import sys
import time
import os
import random
import appdirs
from colorama import Fore, Back, Style, init, deinit
from colors import *

# initialize colorama
init()


# Handling functions
program_dir = str(appdirs.user_config_dir(appname='Bane-Of-Wargs'))

def print_speech_text_effect(text, preferences):
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
    logger_sys.log_message("WARNING: closing game now")
    time.sleep(.5)
    os.system('clear')
    exit(1)

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

def print_zone_map(zone_name, zone, player, preferences):
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

def print_zone_map_alone(zone_name, zone):
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

def print_npc_thumbnail(npc, preferences):
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

def print_enemy_thumbnail(enemy, preferences):
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


# deinitialize colorama
deinit()
