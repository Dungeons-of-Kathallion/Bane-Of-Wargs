# source imports
import logger_sys
import time_handling
import terminal_handling
from colors import *
from terminal_handling import cout, cinput
# external imports
import time
import random
import appdirs
import fade
from sys import exit


# Handling functions
program_dir = str(appdirs.user_config_dir(appname='Bane-Of-Wargs'))


def print_speech_text_effect(text, preferences):
    text += "\n"
    new_input = print_long_string(text, no_output=True)
    if not preferences["speed up"]:
        wait = random.uniform(.05, .1)
    else:
        wait = .02
    for character in new_input:
        cout(character, end="")
        time.sleep(wait)


def clear_prompt():
    from os import system, name
    # for windows
    if name == 'nt':
        _ = system('cls')

    # for mac and linux(here, os.name is 'posix')
    else:
        _ = system('clear')


def exit_game():
    time.sleep(1.5)
    cout(COLOR_YELLOW + "Warning: closing game now" + COLOR_RESET_ALL)
    logger_sys.log_message("WARNING: closing game now")
    time.sleep(.5)
    clear_prompt()
    logger_sys.log_message(f"INFO: PROGRAM RUN END")
    exit(1)


def print_title(preferences):
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


def select_save(options, length=52):
    options += ['EXIT']
    choice = terminal_handling.show_menu(options, length)
    if choice == 'EXIT':
        clear_prompt()
        logger_sys.log_message(f"INFO: PROGRAM RUN END")
        exit(0)
        return
    return choice


def print_separator(character):
    cout(COLOR_STYLE_BRIGHT + (character * 55) + COLOR_RESET_ALL)


def overstrike_text(text):
    result = ""
    for character in text:
        result += character + '\u0336'
    cout(str(result))


def print_long_string(text, no_output=False):
    new_input = ""
    dont = False
    count = 0
    letters = []
    for i, letter in enumerate(text):
        letters += [letter]
        if letter == '@':
            if not dont:
                dont = True
            elif dont:
                dont = False

        if count % 55 == 0:
            new_input += '\n'

        if letter != '@':
            new_input += letter

        if not dont:
            count += 1

    # this is just because at the beginning too, a `\n` character gets added
    new_input = new_input[1:]
    new_input_list = new_input.split(' ')
    count = 0
    for word in new_input_list:
        if "\n" in word and not word.startswith('\n') and not word.endswith('\n'):
            new_input_list[count] = "\n" + word.replace('\n', '')
        count += 1
    new_input = ""
    for word in new_input_list:
        new_input += word + " "
    # other formatting stuff
    new_input = new_input.replace('\n ', '\n')
    new_input_list = list(new_input)
    if new_input.endswith('\n'):
        new_input_list = list(new_input)[:len(list(new_input)) - 3]
    new_input = ""
    for letter in new_input_list:
        new_input += letter

    if no_output:
        return new_input
    else:
        cout(str(new_input))


def apply_yaml_data_color_code(to_print):
    # Convert it to a proper string in case
    to_print = str(to_print)
    to_print = to_print.replace('$RED', '\033[0;31m')
    to_print = to_print.replace('$DARK_RED', '\033[38;2;139;0;0m')
    to_print = to_print.replace('$GREEN', '\033[0;32m')
    to_print = to_print.replace('$DARK_GREEN', '\033[38;2;0;51;25m')
    to_print = to_print.replace('$YELLOW', '\033[38;2;255;255;0m')
    to_print = to_print.replace('$ORANGE', '\033[38;2;255;128;0m')
    to_print = to_print.replace('$BLUE', '\033[0;34m')
    to_print = to_print.replace('$DARK_BLUE', '\033[38;2;0;0;128m')
    to_print = to_print.replace('$LIGHT_BLUE', '\033[38;2;30;144;255m')
    to_print = to_print.replace('$PURPLE', '\033[0;34m')
    to_print = to_print.replace('$PINK', '\033[38;2;255;0;127m')
    to_print = to_print.replace('$CYAN', '\033[0;36m')
    to_print = to_print.replace('$WHITE', COLOR_RESET_ALL)
    to_print = to_print.replace('$BLACK', '\033[0;30m')
    to_print = to_print.replace('$LIGHT_BLACK', '\033[38;2;46;46;46')
    to_print = to_print.replace('$BROWN', '\033[38;2;244;164;96m')
    to_print = to_print.replace('$TAN', '\033[38;2;210;180;140m')
    to_print = to_print.replace('$DARK_BROWN', '\033[38;2;139;69;19m')
    to_print = to_print.replace('$GRAY', '\033[1;30m')
    to_print = to_print.replace('$LIGHT_GRAY', '\033[38;2;192;192;192m')
    to_print = to_print.replace('$KHAKI', '\033[38;2;240;230;140m')

    return to_print


def print_zone_map(zone_name, zone, player, preferences):
    logger_sys.log_message(f"INFO: Printing zone map '{zone_name}' ascii art")
    to_print = zone[zone_name]["map"]["map full"]
    to_print = apply_yaml_data_color_code(to_print)

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
            cout(line + " NAME: " + preferences["latest preset"]["save"])
        if count == 1:
            cout(
                line + " HEALTH: " + COLOR_STYLE_BRIGHT + COLOR_BLUE +
                str(player["health"]) + COLOR_RESET_ALL + "/" + COLOR_STYLE_BRIGHT +
                COLOR_BLUE + str(player["max health"]) + COLOR_RESET_ALL
            )
        if count == 2:
            cout(
                line + " INVENTORY: " + COLOR_STYLE_BRIGHT + COLOR_CYAN +
                str(len(player["inventory"]) + 1) + COLOR_RESET_ALL + "/" +
                COLOR_STYLE_BRIGHT + COLOR_CYAN + str(player["inventory slots"]) + COLOR_RESET_ALL
            )
        if count == 3:
            date = time_handling.date_prettifier(
                time_handling.addition_to_date(player["starting date"], int(player["elapsed time game days"]))
            )
            cout(
                line + " DATE: " + COLOR_STYLE_BRIGHT + COLOR_MAGENTA +
                str(date) + COLOR_RESET_ALL
            )
        if count == 4:
            cout(line + " EXP: " + COLOR_STYLE_BRIGHT + COLOR_GREEN + str(round(player["xp"], 2)) + COLOR_RESET_ALL)
        if count == 5:
            cout(line + " GOLD: " + COLOR_STYLE_BRIGHT + COLOR_YELLOW + str(round(player["gold"], 2)) + COLOR_RESET_ALL)
        count += 1


def print_zone_map_alone(zone_name, zone):
    logger_sys.log_message(f"INFO: Printing zone map '{zone_name}' ascii art")
    to_print = zone[zone_name]["map"]["map full"]
    to_print = apply_yaml_data_color_code(to_print)

    count = 0
    for line in to_print.splitlines():
        cout(line)
        count += 1


def print_npc_thumbnail(npc, preferences):
    logger_sys.log_message(f"INFO: Printing NPC '{npc}' thumbnail")
    if preferences["latest preset"]["type"] == "vanilla":
        with open(program_dir + '/game/imgs/' + npc + ".txt") as f:
            to_print = str(f.read())
    else:
        with open(
            program_dir + '/plugins/' + str(preferences["latest preset"]["plugin"]) +
            '/imgs/' + npc + ".txt"
        ) as f:
            to_print = str(f.read())
    to_print = apply_yaml_data_color_code(to_print)

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
        with open(
            program_dir + '/plugins/' + str(preferences["latest preset"]["plugin"]) +
            '/imgs/' + enemy + ".txt"
        ) as f:
            to_print = str(f.read())
    to_print = apply_yaml_data_color_code(to_print)

    count = 0
    for line in to_print.splitlines():
        print(line)
        count += 1


def a_an_check(word):
    logger_sys.log_message(f"INFO: Checking correct grammar of 'a' in front of '{word}'")
    global to_return
    vowels = ['a', 'e', 'i', 'o', 'u']
    if str(word.lower()[0]) in vowels:
        to_return = "an " + word
    elif str(word.lower()[0]) == 'h':
        if str(word.lower()[1]) in vowels:
            to_return = "an " + word
    else:
        to_return = "a " + word
    logger_sys.log_message(f"INFO: Checked correct grammar of 'a' in front of '{word}': '{to_return}'")
    return to_return


def print_item_thumbnail(to_print):
    to_print = apply_yaml_data_color_code(to_print)

    print(to_print)
    return to_print


def multiple_items_in_list_formatting(list_to_format):
    output_list = []
    different_items = []

    # Get different items in the list and then
    # count how many times these items appear
    # in the list, to after add the formatted
    # output in the formatted list
    for i in list_to_format:
        if i not in different_items:
            different_items += [i]

    for i in different_items:
        number_of_items = list_to_format.count(i)
        if number_of_items > 1:
            output_list += [f"{i}X{number_of_items}"]
        else:
            output_list += [f"{i}"]

    return output_list


def transform_negative_number_to_positive(number):
    if str(number).startswith("-"):
        number = int(str(number).replace("-", ""))

    return number


def print_map_art(item_data, plugin_name=False):
    # Get the path of the file, following the map
    # name and if the player's using a plugin or
    # vanilla data.
    # Then, each lines of the file one by one and
    # prettify them, to after print the final result
    # to the player's UI
    if plugin_name is not False:
        path = f"{program_dir}/plugins/{plugin_name}/imgs/{item_data["map"]}.txt"
    else:
        path = f"{program_dir}/game/imgs/{item_data["map"]}.txt"
    with open(path, 'r') as f:
        art = f.readlines()

    human_civilizations = ['⌂', '⟰', '⤊', '±', '⇭']
    for line in art:
        line = line.replace('\n', '')
        line = line.replace('≈', '\033[38;2;250;223;199m' + "≈" + '\033[38;2;255;208;166m')
        for character in human_civilizations:
            line = line.replace(character, '\033[38;2;255;195;141m' + character + '\033[38;2;255;208;166m')
        print("║" + '\033[38;2;255;208;166m' + line.replace('\n', '') + COLOR_RESET_ALL + "║")
    return art
