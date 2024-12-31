# check_yaml.py
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
import text_handling
import yaml_handling
from colors import *
from terminal_handling import cout
# external imports
import yamale
import appdirs
import re

# Create the variable for the program
# to access the program config/data folder
program_dir = str(appdirs.user_config_dir(appname='Bane-Of-Wargs'))


def check_yaml(file_path):
    file_type = 'none'
    with open(file_path, 'r') as f:
        file = yaml_handling.safe_load(f)
    if file_path.endswith('dialog.yaml'):
        file_type = 'dialogs'
    elif file_path.endswith('drinks.yaml'):
        file_type = 'drinks'
    elif file_path.endswith('enemies.yaml'):
        file_type = 'enemies'
    elif file_path.endswith('items.yaml'):
        file_type = 'items'
    elif file_path.endswith('lists.yaml'):
        file_type = 'lists'
    elif file_path.endswith('map.yaml'):
        file_type = 'map'
    elif file_path.endswith('mounts.yaml'):
        file_type = 'mounts'
    elif file_path.endswith('npcs.yaml'):
        file_type = 'npcs'
    elif file_path.endswith('start.yaml'):
        file_type = 'start'
    elif file_path.endswith('mission.yaml'):
        file_type = 'missions'
    elif file_path.endswith('zone.yaml'):
        file_type = 'zones'
    elif file_path.endswith('preferences.yaml'):
        file_type = 'preferences'
    elif file_path.startswith('saves/'):
        file_type = 'saves'
    file_schema = str(f'{program_dir}/game/schemas/{file_type}.yaml')
    long_files_types = [
        'drinks', 'mounts', 'map', 'lists', 'npcs',
        'enemies', 'dialogs', 'missions'
    ]
    if file_type in long_files_types:
        count = 0
        file_len = int(len(list(file)))
        while count < file_len:
            current_object_name = str(list(file)[count])
            current_object_data = file[str(list(file)[count])]

            schema = yamale.make_schema(file_schema)
            data = yamale.make_data(content=str(current_object_data))
            logger_sys.log_message(
                f"INFO: Validating file '{file_path}' data: '{current_object_data}'" +
                f" with schema '{file_schema}'"
            )
            yamale.validate(schema, data)

            count += 1
    elif file_type == 'start':
        schema = yamale.make_schema(file_schema)
        data = yamale.make_data(file_path)
        logger_sys.log_message(f"INFO: Validating file '{file_path}' data: '{data}' with schema '{file_schema}'")
        yamale.validate(schema, data)
    elif file_type == 'zones' or file_type == 'items':
        count = 0
        file_len = int(len(list(file)))
        while count < file_len:
            current_object_name = str(list(file)[count])
            current_object_data = file[str(list(file)[count])]
            if current_object_data["type"].startswith('Armor Piece: Boots'):
                file_schema = str(f'{program_dir}/game/schemas/{file_type}_Armor Piece Boots.yaml')
            elif current_object_data["type"].startswith('Armor Piece: Chestplate'):
                file_schema = str(f'{program_dir}/game/schemas/{file_type}_Armor Piece Chestplate.yaml')
            elif current_object_data["type"].startswith('Armor Piece: Leggings'):
                file_schema = str(f'{program_dir}/game/schemas/{file_type}_Armor Piece Leggings.yaml')
            elif current_object_data["type"].startswith('Armor Piece: Shield'):
                file_schema = str(f'{program_dir}/game/schemas/{file_type}_Armor Piece Shield.yaml')
            else:
                file_schema = str(f"{program_dir}/game/schemas/{file_type}_{current_object_data['type']}.yaml")

            schema = yamale.make_schema(str(file_schema))
            data = yamale.make_data(content=str(current_object_data))
            logger_sys.log_message(
                f"INFO: Validating file '{file_path}' data: '{current_object_data}'" +
                f" with schema '{file_schema}'"
            )
            yamale.validate(schema, data)

            count += 1
    elif file_type == 'preferences' or file_type == 'saves':
        file_schema = f'{program_dir}/game/schemas/{file_type}.yaml'
        schema = yamale.make_schema(file_schema)
        data = yamale.make_data(file_path)
        logger_sys.log_message(f"INFO: Validating file '{file_path}' data: '{data}' with schema '{file_schema}'")
        yamale.validate(schema, data)


def examine(file_path):
    try:
        check_yaml(str(file_path))
    except Exception as error:
        cout(
            COLOR_RED + "ERROR: " + COLOR_RESET_ALL + COLOR_RED + COLOR_STYLE_BRIGHT +
            "A parsing error in a yaml file has been detected:\n" + COLOR_RESET_ALL + str(error)
        )
        logger_sys.log_message(f"ERROR: A parsing error in a yaml file has been detected:\n{error}")
        text_handling.exit_game()


def check_dialog_conversations(dialog_data, dialog_name):
    # Run every checks required to pass
    # for a dialog's conversation to be
    # valid
    logger_sys.log_message(f"INFO: Checking dialog '{dialog_name}' conversation data")

    conversation = dialog_data[dialog_name]["conversation"]

    # Create digits database
    logger_sys.log_message("INFO: Creating digits database from 0 to 120")
    digits = []
    count = 0
    while count <= 120:
        digits += [count]

        count += 1

    count = 0
    while count < len(conversation):
        current_label_name = str(list(conversation[count]))
        current_label_name = current_label_name.replace('[', '')
        current_label_name = current_label_name.replace(']', '')
        current_label_name = current_label_name.replace("'", '')

        # Check if the label name is correct, if not,
        # close the program and output an error message
        # in the UI and in logging
        logger_sys.log_message(
            f"INFO: Checking if dialog '{dialog_name}' conversation label '{current_label_name}' is a valid label name"
        )
        if current_label_name.lower().startswith('label '):
            try:
                if int(current_label_name.split('label ', 1)[1]) not in digits:
                    invalid_label_name_output(dialog_name, current_label_name)
            except Exception as error:
                invalid_label_name_output(dialog_name, current_label_name)
        else:
            invalid_label_name_output(dialog_name, current_label_name)

        # Check if the functions in the label are valid,
        # if not, close the program and output an error
        # message in the UI and in logging
        possible_functions = [
            'print(', 'ask-input(', 'goto(', 'wait(', 'ask-confirmation(', 'if(',
            'choice(', 'create-variable(', 'accept(', 'decline(', 'defer(', 'die(',
            'display-scene('
        ]

        count2 = 0
        while count2 < len(conversation[count][current_label_name]):
            current_function = conversation[count][current_label_name][count2]
            continue_actions = True
            count3 = 0
            while count3 < len(possible_functions) and continue_actions:
                i = possible_functions[count3]
                if str(type(current_function)) != "<class 'str'>":
                    current_function = list(current_function)[0]
                if not current_function.lower().startswith(i):
                    error = True
                else:
                    error = False
                    continue_actions = False

                count3 += 1

            # If the current function is a 'if()' function,
            # then run specific tests to test the functions
            # inside of it
            if current_function.lower().startswith('if('):
                count4 = 0
                while count4 < len(conversation[count][current_label_name][count2]):
                    count5 = 0
                    continue_actions = True
                    while count5 < len(possible_functions) and continue_actions:
                        i = possible_functions[count5]
                        current_sub_function = conversation[count][current_label_name][count2][current_function][count4]
                        if str(type(current_sub_function)) != "<class 'str'>":
                            current_sub_function = list(
                                conversation[count][current_label_name][count2][current_function][count4]
                            )[0]
                        if not current_sub_function.lower().startswith(i):
                            error = True
                        else:
                            error = False
                            continue_actions = False

                        count5 += 1

                    count4 += 1

            count2 += 1

            if error:
                invalid_conversation_functions_output(dialog_name, current_function)
        count += 1


def invalid_label_name_output(dialog_name, label_name):
    # Output in the UI and the logging
    # proper error messages
    cout(
        COLOR_RED + "ERROR: " + COLOR_STYLE_BRIGHT +
        f"dialog '{dialog_name}' conversation label '{label_name}' isn't a valid label name --> closing game" +
        COLOR_RESET_ALL
    )
    logger_sys.log_message(
        f"ERROR: dialog '{dialog_name}' conversation label '{label_name}' isn't a valid label name --> closing game"
    )
    text_handling.exit_game()


def invalid_conversation_functions_output(dialog_name, function_name):
    # Output in the UI and the logging
    # proper error messages
    cout(
        COLOR_RED + "ERROR: " + COLOR_STYLE_BRIGHT +
        f"dialog '{dialog_name}' conversation function '{function_name}' isn't a valid function --> closing game" +
        COLOR_RESET_ALL
    )
    logger_sys.log_message(
        f"ERROR: dialog '{dialog_name}' conversation function '{function_name}' isn't a valid function --> closing game"
    )
    text_handling.exit_game()


def examine_map_point(data):
    try:
        data = yamale.make_data(content=str(data))
        schema = yamale.make_schema(f'{program_dir}/game/schemas/map.yaml')
        yamale.validate(schema, data)
    except Exception as error:
        cout(
            COLOR_RED + "ERROR: " + COLOR_RESET_ALL + COLOR_RED + COLOR_STYLE_BRIGHT +
            "A parsing error in a yaml file has been detected:\n" + COLOR_RESET_ALL + str(error)
        )
        logger_sys.log_message(f"ERROR: A parsing error in a yaml file has been detected:\n{error}")
        text_handling.exit_game()


def examine_item(data):
    try:
        data_type = data["type"]
        data_real = data
        if data_type.startswith("Armor Piece"):
            data_type = data_type.replace(':', '')
        data = yamale.make_data(content=str(data))
        schema = yamale.make_schema(f'{program_dir}/game/schemas/items_{data_type}.yaml')
        yamale.validate(schema, data)
        if data_type == "Consumable":
            examine_consumable(data_real)
    except Exception as error:
        return
    #    cout(
    #        COLOR_RED + "ERROR: " + COLOR_RESET_ALL + COLOR_RED + COLOR_STYLE_BRIGHT +
    #        "A parsing error in a yaml file has been detected:\n" + COLOR_RESET_ALL + str(error)
    #    )
    #    logger_sys.log_message(f"ERROR: A parsing error in a yaml file has been detected:\n{error}")
    #    text_handling.exit_game()


def examine_drink(data):
    try:
        data = yamale.make_data(content=str(data))
        schema = yamale.make_schema(f'{program_dir}/game/schemas/drinks.yaml')
        yamale.validate(schema, data)
    except Exception as error:
        cout(
            COLOR_RED + "ERROR: " + COLOR_RESET_ALL + COLOR_RED + COLOR_STYLE_BRIGHT +
            "A parsing error in a yaml file has been detected:\n" + COLOR_RESET_ALL + str(error)
        )
        logger_sys.log_message(f"ERROR: A parsing error in a yaml file has been detected:\n{error}")
        text_handling.exit_game()


def examine_enemy(data):
    try:
        data = yamale.make_data(content=str(data))
        schema = yamale.make_schema(f'{program_dir}/game/schemas/enemies.yaml')
        yamale.validate(schema, data)
    except Exception as error:
        cout(
            COLOR_RED + "ERROR: " + COLOR_RESET_ALL + COLOR_RED + COLOR_STYLE_BRIGHT +
            "A parsing error in a yaml file has been detected:\n" + COLOR_RESET_ALL + str(error)
        )
        logger_sys.log_message(f"ERROR: A parsing error in a yaml file has been detected:\n{error}")
        text_handling.exit_game()


def examine_npc(data):
    try:
        data = yamale.make_data(content=str(data))
        schema = yamale.make_schema(f'{program_dir}/game/schemas/npcs.yaml')
        yamale.validate(schema, data)
    except Exception as error:
        cout(
            COLOR_RED + "ERROR: " + COLOR_RESET_ALL + COLOR_RED + COLOR_STYLE_BRIGHT +
            "A parsing error in a yaml file has been detected:\n" + COLOR_RESET_ALL + str(error)
        )
        logger_sys.log_message(f"ERROR: A parsing error in a yaml file has been detected:\n{error}")
        text_handling.exit_game()


def examine_list(data):
    try:
        count = 0
        while count < len(list(data)):
            entry = data[list(data)[count]]
            data = yamale.make_data(content=str(entry))
            schema = yamale.make_schema(f'{program_dir}/game/schemas/lists.yaml')
            yamale.validate(schema, data)
            count += 1
    except Exception as error:
        cout(
            COLOR_RED + "ERROR: " + COLOR_RESET_ALL + COLOR_RED + COLOR_STYLE_BRIGHT +
            "A parsing error in a yaml file has been detected:\n" + COLOR_RESET_ALL + str(error)
        )
        logger_sys.log_message(f"ERROR: A parsing error in a yaml file has been detected:\n{error}")
        text_handling.exit_game()


def examine_zone(data):
    try:
        data_type = data["type"]
        data = yamale.make_data(content=str(data))
        schema = yamale.make_schema(f'{program_dir}/game/schemas/zones_{data_type}.yaml')
        yamale.validate(schema, data)
    except Exception as error:
        cout(
            COLOR_RED + "ERROR: " + COLOR_RESET_ALL + COLOR_RED + COLOR_STYLE_BRIGHT +
            "A parsing error in a yaml file has been detected:\n" + COLOR_RESET_ALL + str(error)
        )
        logger_sys.log_message(f"ERROR: A parsing error in a yaml file has been detected:\n{error}")
        text_handling.exit_game()


def examine_dialog(data):
    try:
        data = yamale.make_data(content=str(data))
        schema = yamale.make_schema(f'{program_dir}/game/schemas/dialogs.yaml')
        yamale.validate(schema, data)
    except Exception as error:
        cout(
            COLOR_RED + "ERROR: " + COLOR_RESET_ALL + COLOR_RED + COLOR_STYLE_BRIGHT +
            "A parsing error in a yaml file has been detected:\n" + COLOR_RESET_ALL + str(error)
        )
        logger_sys.log_message(f"ERROR: A parsing error in a yaml file has been detected:\n{error}")
        text_handling.exit_game()


def examine_mission(data):
    try:
        data = yamale.make_data(content=str(data))
        schema = yamale.make_schema(f'{program_dir}/game/schemas/missions.yaml')
        yamale.validate(schema, data)
    except Exception as error:
        cout(
            COLOR_RED + "ERROR: " + COLOR_RESET_ALL + COLOR_RED + COLOR_STYLE_BRIGHT +
            "A parsing error in a yaml file has been detected:\n" + COLOR_RESET_ALL + str(error)
        )
        logger_sys.log_message(f"ERROR: A parsing error in a yaml file has been detected:\n{error}")
        text_handling.exit_game()


def examine_event(data):
    try:
        data = yamale.make_data(content=str(data))
        schema = yamale.make_schema(f'{program_dir}/game/schemas/events.yaml')
        yamale.validate(schema, data)
    except Exception as error:
        cout(
            COLOR_RED + "ERROR: " + COLOR_RESET_ALL + COLOR_RED + COLOR_STYLE_BRIGHT +
            "A parsing error in a yaml file has been detected:\n" + COLOR_RESET_ALL + str(error)
        )
        logger_sys.log_message(f"ERROR: A parsing error in a yaml file has been detected:\n{error}")
        text_handling.exit_game()


def examine_mount(data):
    try:
        data = yamale.make_data(content=str(data))
        schema = yamale.make_schema(f'{program_dir}/game/schemas/mounts.yaml')
        yamale.validate(schema, data)
    except Exception as error:
        cout(
            COLOR_RED + "ERROR: " + COLOR_RESET_ALL + COLOR_RED + COLOR_STYLE_BRIGHT +
            "A parsing error in a yaml file has been detected:\n" + COLOR_RESET_ALL + str(error)
        )
        logger_sys.log_message(f"ERROR: A parsing error in a yaml file has been detected:\n{error}")
        text_handling.exit_game()


def consumable_effect_output_error(message):
    cout(
        COLOR_RED + "ERROR: " + COLOR_RESET_ALL + COLOR_RED + COLOR_STYLE_BRIGHT +
        "A parsing error in a yaml file has been detected:\n" + COLOR_RESET_ALL + str(message)
    )
    logger_sys.log_message(f"ERROR: A parsing error in a yaml file has been detected:\n{message}")
    text_handling.exit_game()


def check_if_is_a_number(variable_to_test):
    is_int = True
    is_float = True
    if type(variable_to_test) is not type(0):
        is_int = False
    elif type(variable_to_test) is not type(.1):
        is_float = False

    if is_int or is_float:
        output = True

    return output


def consumable_run_test(data, effect_type):
    # Firstly, check the effect type and then
    # run specifics tests
    if effect_type == "healing":
        if "effect time" in data:
            if not check_if_is_a_number(data["effect time"]):
                consumable_effect_output_error("effect time should be an integer or floating number")
        if "health change" not in data:
            consumable_effect_output_error("missing required 'health change' dictionary")
        elif data["health change"] is not None:
            if "augmentation" in data["health change"]:
                if not check_if_is_a_number(data["health change"]["augmentation"]):
                    consumable_effect_output_error("'augmentation' key should be an integer or floating number")
            if "diminution" in data["health change"]:
                if not check_if_is_a_number(data["health change"]["diminution"]):
                    consumable_effect_output_error("'diminution' key should be an integer or floating number")
            if "max health" in data["health change"]:
                if "augmentation" in data["health change"]["max health"]:
                    if not check_if_is_a_number(data["health change"]["max health"]["augmentation"]):
                        consumable_effect_output_error("'augmentation' key should be an integer or floating number")
                if "diminution" in data["health change"]["max health"]:
                    if not check_if_is_a_number(data["health change"]["max health"]["diminution"]):
                        consumable_effect_output_error("'diminution' key should be an integer or floating number")
    elif effect_type == "protection":
        if "effect time" in data:
            if not check_if_is_a_number(data["effect time"]):
                consumable_effect_output_error("'effect time' should be an integer or floating number")
        else:
            consumable_effect_output_error("missing required 'effect time' key")
        if "protection change" not in data:
            consumable_effect_output_error("missing required 'protection change' dictionary")
        if data["protection change"] is not None:
            if "coefficient" in data["protection change"]:
                if not check_if_is_a_number(data["protection change"]["coefficient"]):
                    consumable_effect_output_error("'coefficient' key should be an integer or floating number")
    elif effect_type == "strength":
        if "effect time" in data:
            if not check_if_is_a_number(data["effect time"]):
                consumable_effect_output_error("'effect time' should be an integer or floating number")
        else:
            consumable_effect_output_error("missing required 'effect time' key")
        if "strength change" not in data:
            consumable_effect_output_error("missing required 'strength change' dictionary")
        if data["strength change"] is not None:
            if "damage coefficient" in data["strength change"]:
                if not check_if_is_a_number(data["strength change"]["damage coefficient"]):
                    consumable_effect_output_error("'damage coefficient' key should be an integer or floating number")
            if "critical hit chance coefficient" in data["strength change"]:
                if not check_if_is_a_number(data["strength change"]["critical hit chance coefficient"]):
                    consumable_effect_output_error(
                        "'critical hit chance coefficient' key should be an integer or floating number"
                    )
    elif effect_type == "agility":
        if "effect time" in data:
            if not check_if_is_a_number(data["effect time"]):
                consumable_effect_output_error("'effect time' should be an integer or floating number")
        else:
            consumable_effect_output_error("missing required 'effect time' key")
        if "agility change" not in data:
            consumable_effect_output_error("missing required 'agility change' dictionary")
        if data["agility change"] is not None:
            if "coefficient" in data["agility change"]:
                if not check_if_is_a_number(data["agility change"]["coefficient"]):
                    consumable_effect_output_error("'coefficient' key should be an integer or floating number")
    elif effect_type == "time elapsing":
        if "effect time" in data:
            if not check_if_is_a_number(data["effect time"]):
                consumable_effect_output_error("effect time should be an integer or floating number")
        else:
            consumable_effect_output_error("missing required 'effect time' key")
        if "time change" not in data:
            consumable_effect_output_error("missing required 'time change' dictionary")
        if data["time change"] is not None:
            if "coefficient" in data["time change"]:
                if not check_if_is_a_number(data["time change"]["coefficient"]):
                    consumable_effect_output_error("coefficient key should be an integer or floating number")
    elif effect_type == "attributes addition":
        if "attributes addition" not in data:
            consumable_effect_output_error("missing required 'attributes addition' key list")
        else:
            if type(['1']) is not type(data["attributes addition"]):
                consumable_effect_output_error("key 'attributes addition' should be a list")
    elif effect_type == "dialog displaying":
        if "dialog" not in data:
            consumable_effect_output_error("missing required 'dialog' key")
    elif effect_type == "enemy spawning":
        if "enemy list" not in data:
            consumable_effect_output_error("missing required 'enemy list' key")
        if "enemy number" not in data:
            consumable_effect_output_error("missing required 'enemy number' key")
        elif not check_if_is_a_number(data["enemy number"]):
            consumable_effect_output_error("'enemy number' should be an integer or floating number")
    elif effect_type == "exp change":
        if "exp change" not in data:
            consumable_effect_output_error("missing required 'exp change' dictionary")
        if data["exp change"] is not None:
            if "augmentation" in data["exp change"]:
                if not check_if_is_a_number(data["exp change"]["augmentation"]):
                    consumable_effect_output_error("'augmentation' key should be an integer or floating number")
            if "diminution" in data["exp change"]:
                if not check_if_is_a_number(data["exp change"]["diminution"]):
                    consumable_effect_output_error("'diminution' key should be an integer or floating number")
    elif effect_type == "coordinates change":
        if "coordinates change" not in data:
            consumable_effect_output_error("missing required 'coordinates change' dictionary")
        if data["coordinates change"] is not None:
            if "x" in data["coordinates change"]:
                if not check_if_is_a_number(data["coordinates change"]["x"]):
                    consumable_effect_output_error("'x' key should be an integer or floating number")
            if "x" in data["coordinates change"]:
                if not check_if_is_a_number(data["coordinates change"]["x"]):
                    consumable_effect_output_error("'x' key should be an integer or floating number")
    elif effect_type == "inventory change":
        if "inventory change" not in data:
            consumable_effect_output_error("missing required 'inventory change' dictionary")
        if data["inventory change"] is not None:
            if "removals" in data["inventory change"]:
                if type(['1']) is not type(data["inventory change"]["removals"]):
                    consumable_effect_output_error("'removals' key should be a list")
            if "additions" in data["inventory change"]:
                if type(['1']) is not type(data["inventory change"]["additions"]):
                    consumable_effect_output_error("'additions' key should be a list")


def examine_consumable(data):
    # For every effect in that consumable,
    # load it and run every tests, depending
    # on the effect type and dictionary keys
    try:
        count = 0
        for effect in data["effects"]:
            current_effect_data = data["effects"][count]
            current_effect_type = current_effect_data["type"]

            consumable_run_test(current_effect_data, current_effect_type)

            count += 1
    except Exception as error:
        cout(
            COLOR_RED + "ERROR: " + COLOR_RESET_ALL + COLOR_RED + COLOR_STYLE_BRIGHT +
            "An error happened when examining item:\n" + COLOR_RESET_ALL + str(data)
        )
        logger_sys.log_message(f"ERROR: A error happened when examining item:\n{data}")
        text_handling.exit_game()


def verify_data(
    map, item, drinks, enemy, npcs, start_player, lists,
    zone, dialog, mission, mounts, event
):
    # Specific checks for the map dictionary
    # The checks are:
    # - verify the map point id is valid
    # - check if the map point coordinates are unique
    # - check if the map point zone exists
    # - check if the blocked directions are syntactically good
    # - check if all the items on the ground exists
    # - verify the validity of the key entry
    # - check if enemy list spawned exists
    # - check if dialog exists
    # - check if npcs exist
    for map_point_id in list(map):
        map_point = map[map_point_id]
        # Check map point id using pattern
        if not bool(re.fullmatch(r"point[0-9]+", map_point_id)):
            print(
                COLOR_RED + "ERROR: " + COLOR_STYLE_BRIGHT +
                f"Map point id '{map_point_id}' isn't valid --> invalid pattern" +
                COLOR_RESET_ALL
            )
            print(
                COLOR_RED + "ERROR: " + COLOR_STYLE_BRIGHT +
                "The pattern is `point{digits}`" +
                COLOR_RESET_ALL
            )
            text_handling.exit_game()

        # Verify duplicate coordinates
        for i in list(map):
            if (
                map[i]["x"] == map_point["x"] and
                map[i]["y"] == map_point["y"] and
                i != map_point_id
            ):
                print(
                    COLOR_RED + "ERROR: " + COLOR_STYLE_BRIGHT +
                    f"Map point '{map_point_id}' isn't valid --> " +
                    f"duplicate coordinates with map point '{i}'" +
                    COLOR_RESET_ALL
                )
                text_handling.exit_game()

        # Verify map zone
        if map_point["map zone"] not in list(zone):
            print(
                COLOR_RED + "ERROR: " + COLOR_STYLE_BRIGHT +
                f"Map point id '{map_point_id}' isn't valid --> "
                f"map zone '{map_point['map zone']}' doesn't exist" +
                COLOR_RESET_ALL
            )
            text_handling.exit_game()

        # Verify blocked directions syntax
        directions = [
            'North', 'South', 'West', 'East', 'North-East',
            'North-West', 'South-East', 'South-West', 'None'
        ]
        if 'None' in map_point["blocked"] and len(map_point["blocked"]) > 1:
            print(
                COLOR_RED + "ERROR: " + COLOR_STYLE_BRIGHT +
                f"Map point id '{map_point_id}' isn't valid --> "
                f"entry `{direction}` in blocked directions isn't required" +
                COLOR_RESET_ALL
            )
            text_handling.exit_game()
        for direction in directions:
            if map_point["blocked"].count(direction) > 1:
                print(
                    COLOR_RED + "ERROR: " + COLOR_STYLE_BRIGHT +
                    f"Map point id '{map_point_id}' isn't valid --> "
                    f"too many `{direction}` entries in blocked directions" +
                    COLOR_RESET_ALL
                )
                text_handling.exit_game()
        for direction in map_point["blocked"]:
            if direction not in directions:
                print(
                    COLOR_RED + "ERROR: " + COLOR_STYLE_BRIGHT +
                    f"Map point id '{map_point_id}' isn't valid --> "
                    f"entry `{direction}` in blocked directions isn't valid" +
                    COLOR_RESET_ALL
                )
                text_handling.exit_game()

        # Ground items check
        if "item" in map_point:
            if type(map_point["item"]) is not type([]):
                print(
                    COLOR_RED + "ERROR: " + COLOR_STYLE_BRIGHT +
                    f"Map point id '{map_point_id}' isn't valid --> "
                    f"entry `item` isn't a list" +
                    COLOR_RESET_ALL
                )
                text_handling.exit_game()
            for i in map_point["item"]:
                if i not in list(item):
                    print(
                        COLOR_RED + "ERROR: " + COLOR_STYLE_BRIGHT +
                        f"Map point id '{map_point_id}' isn't valid --> "
                        f"item `{i}` in ground items doesn't exist" +
                        COLOR_RESET_ALL
                    )
                    text_handling.exit_game()
                if map_point["item"].count(i) > 1:
                    print(
                        COLOR_RED + "ERROR: " + COLOR_STYLE_BRIGHT +
                        f"Map point id '{map_point_id}' isn't valid --> "
                        f"item `{i}` in ground items is duplicated" +
                        COLOR_RESET_ALL
                    )
                    text_handling.exit_game()

        # Keys checks
        if "key" in map_point:
            if type(map_point["key"]) is not type({}):
                print(
                    COLOR_RED + "ERROR: " + COLOR_STYLE_BRIGHT +
                    f"Map point id '{map_point_id}' isn't valid --> "
                    f"entry `key` isn't a dictionary" +
                    COLOR_RESET_ALL
                )
                text_handling.exit_game()
            if "remove key" not in map_point["key"]:
                print(
                    COLOR_RED + "ERROR: " + COLOR_STYLE_BRIGHT +
                    f"Map point id '{map_point_id}' isn't valid --> "
                    f"missing `remove key` entry in key dictionary" +
                    COLOR_RESET_ALL
                )
                text_handling.exit_game()
            if "required keys" not in map_point["key"]:
                print(
                    COLOR_RED + "ERROR: " + COLOR_STYLE_BRIGHT +
                    f"Map point id '{map_point_id}' isn't valid --> "
                    f"missing `required keys` entry in key dictionary" +
                    COLOR_RESET_ALL
                )
                text_handling.exit_game()

            if type(map_point["key"]["remove key"]) is not type(True):
                print(
                    COLOR_RED + "ERROR: " + COLOR_STYLE_BRIGHT +
                    f"Map point id '{map_point_id}' isn't valid --> "
                    f"key `remove key` isn't a boolean" +
                    COLOR_RESET_ALL
                )
                text_handling.exit_game()
            if type(map_point["key"]["required keys"]) is not type([]):
                print(
                    COLOR_RED + "ERROR: " + COLOR_STYLE_BRIGHT +
                    f"Map point id '{map_point_id}' isn't valid --> "
                    f"entry `required keys` in key dictionary isn't a list" +
                    COLOR_RESET_ALL
                )
                text_handling.exit_game()
            if map_point["key"]["required keys"] == []:
                print(
                    COLOR_RED + "ERROR: " + COLOR_STYLE_BRIGHT +
                    f"Map point id '{map_point_id}' isn't valid --> "
                    f"entry `required keys` in key dictionary is empty" +
                    COLOR_RESET_ALL
                )
                text_handling.exit_game()
            for key in map_point["key"]["required keys"]:
                if key not in list(item):
                    print(
                        COLOR_RED + "ERROR: " + COLOR_STYLE_BRIGHT +
                        f"Map point id '{map_point_id}' isn't valid --> "
                        f"item `{key}` in required keys doesn't exist" +
                        COLOR_RESET_ALL
                    )
                    text_handling.exit_game()
                if map_point["key"]["required keys"].count(key) > 1:
                    print(
                        COLOR_RED + "ERROR: " + COLOR_STYLE_BRIGHT +
                        f"Map point id '{map_point_id}' isn't valid --> "
                        f"key `{ke}` in required keys is duplicated" +
                        COLOR_RESET_ALL
                    )
                    text_handling.exit_game()
        # Enemy, dialog and npcs checks
        if "enemy type" in map_point:
            if type(map_point["enemy type"]) is not type(""):
                print(
                    COLOR_RED + "ERROR: " + COLOR_STYLE_BRIGHT +
                    f"Map point id '{map_point_id}' isn't valid --> "
                    f"entry `enemy type` isn't a string" +
                    COLOR_RESET_ALL
                )
                text_handling.exit_game()
            if map_point["enemy type"] not in list(lists):
                print(
                    COLOR_RED + "ERROR: " + COLOR_STYLE_BRIGHT +
                    f"Map point id '{map_point_id}' isn't valid --> "
                    f"enemy list `{map_point['enemy type']}` doesn't exist" +
                    COLOR_RESET_ALL
                )
                text_handling.exit_game()
        if "dialog" in map_point:
            if type(map_point["dialog"]) is not type(""):
                print(
                    COLOR_RED + "ERROR: " + COLOR_STYLE_BRIGHT +
                    f"Map point id '{map_point_id}' isn't valid --> "
                    f"entry `dialog` isn't a string" +
                    COLOR_RESET_ALL
                )
                text_handling.exit_game()
            if map_point["dialog"] not in list(dialog):
                print(
                    COLOR_RED + "ERROR: " + COLOR_STYLE_BRIGHT +
                    f"Map point id '{map_point_id}' isn't valid --> "
                    f"dialog `{map_point['dialog']}` doesn't exist" +
                    COLOR_RESET_ALL
                )
                text_handling.exit_game()
        if "npcs" in map_point:
            if type(map_point["npc"]) is not type([]):
                print(
                    COLOR_RED + "ERROR: " + COLOR_STYLE_BRIGHT +
                    f"Map point id '{map_point_id}' isn't valid --> "
                    f"entry `nps` isn't a list" +
                    COLOR_RESET_ALL
                )
                text_handling.exit_game()
            for npc in map_point["npc"]:
                if npc not in list(npcs):
                    print(
                        COLOR_RED + "ERROR: " + COLOR_STYLE_BRIGHT +
                        f"Map point id '{map_point_id}' isn't valid --> "
                        f"npc `{npc}` doesn't exist" +
                        COLOR_RESET_ALL
                    )
                    text_handling.exit_game()
                if map_point["npc"].count(npc) > 1:
                    print(
                        COLOR_RED + "ERROR: " + COLOR_STYLE_BRIGHT +
                        f"Map point id '{map_point_id}' isn't valid --> "
                        f"key `{npc}` in npcs is duplicated" +
                        COLOR_RESET_ALL
                    )
                    text_handling.exit_game()

        # Specific checks for the `item` dictionary
        # The checks are:
        # EVERY TYPE
        # - check if every requires keys are valid
        # WEAPONS:
        # - check if there're every keys
        # - check if every key i the right class (bool, str, float...)
        # - check if every item for the upgrade exists
        # ARMOR PIECES:
        # - check if there're every keys
        # - check if every key i the right class (bool, str, float...)
        # - check if every item for the upgrade exists
        # CONSUMABLES:
        # - check if there're every keys
        # - check if every key i the right class (bool, str, float...)
        # UTILITIES:
        # - check if there're every keys
        # - check if every key i the right class (bool, str, float...)
        # - check if every arguments exist
        # BAGS:
        # - checks for the inventory slots keys
        # FOOD:
        # - check if there're every keys
        # - check if every key i the right class (bool, str, float...)
        # MAPS:
        # - checks for the inventory slots keys
        # LURES:
        # - check if the preferred types list contains existing items
        for current in list(item):
            item_data = item[current]

            if "type" not in item_data:
                print(
                    COLOR_RED + "ERROR: " + COLOR_STYLE_BRIGHT +
                    f"item id '{current}' isn't valid --> "
                    f"missing required `type` key" +
                    COLOR_RESET_ALL
                )
                text_handling.exit_game()
            if "gold" not in item_data:
                print(
                    COLOR_RED + "ERROR: " + COLOR_STYLE_BRIGHT +
                    f"item id '{current}' isn't valid --> "
                    f"missing required `gold` key" +
                    COLOR_RESET_ALL
                )
                text_handling.exit_game()
            if "description" not in item_data:
                print(
                    COLOR_RED + "ERROR: " + COLOR_STYLE_BRIGHT +
                    f"item id '{current}' isn't valid --> "
                    f"missing required `description` key" +
                    COLOR_RESET_ALL
                )
                text_handling.exit_game()
            if "thumbnail" not in item_data:
                print(
                    COLOR_RED + "ERROR: " + COLOR_STYLE_BRIGHT +
                    f"item id '{current}' isn't valid --> "
                    f"missing required `thumbnail` key" +
                    COLOR_RESET_ALL
                )
                text_handling.exit_game()

            if type(item_data["type"]) is not type(""):
                print(
                    COLOR_RED + "ERROR: " + COLOR_STYLE_BRIGHT +
                    f"item id '{current}' isn't valid --> "
                    f"entry `type` isn't a string" +
                    COLOR_RESET_ALL
                )
                text_handling.exit_game()
            if (
                type(item_data["gold"]) is not type(.1) and
                type(item_data["gold"]) is not type(1)
            ):
                print(
                    COLOR_RED + "ERROR: " + COLOR_STYLE_BRIGHT +
                    f"item id '{current}' isn't valid --> "
                    f"entry `gold` isn't an integer or floating number" +
                    COLOR_RESET_ALL
                )
                text_handling.exit_game()
            if type(item_data["description"]) is not type(""):
                print(
                    COLOR_RED + "ERROR: " + COLOR_STYLE_BRIGHT +
                    f"item id '{current}' isn't valid --> "
                    f"entry `description` isn't a string" +
                    COLOR_RESET_ALL
                )
                text_handling.exit_game()
            if type(item_data["thumbnail"]) is not type(""):
                print(
                    COLOR_RED + "ERROR: " + COLOR_STYLE_BRIGHT +
                    f"item id '{current}' isn't valid --> "
                    f"entry `thumbnail` isn't a string" +
                    COLOR_RESET_ALL
                )
                text_handling.exit_game()

            if item_data["type"] == 'Weapon':
                if "display name" not in item_data:
                    print(
                        COLOR_RED + "ERROR: " + COLOR_STYLE_BRIGHT +
                        f"item id '{current}' isn't valid --> "
                        f"missing required `display name` key" +
                        COLOR_RESET_ALL
                    )
                    text_handling.exit_game()
                if "upgrade tier" not in item_data:
                    print(
                        COLOR_RED + "ERROR: " + COLOR_STYLE_BRIGHT +
                        f"item id '{current}' isn't valid --> "
                        f"missing required `upgrade tier` key" +
                        COLOR_RESET_ALL
                    )
                    text_handling.exit_game()
                if "damage" not in item_data:
                    print(
                        COLOR_RED + "ERROR: " + COLOR_STYLE_BRIGHT +
                        f"item id '{current}' isn't valid --> "
                        f"missing required `damage` key" +
                        COLOR_RESET_ALL
                    )
                    text_handling.exit_game()
                if "defend" not in item_data:
                    print(
                        COLOR_RED + "ERROR: " + COLOR_STYLE_BRIGHT +
                        f"item id '{current}' isn't valid --> "
                        f"missing required `defend` key" +
                        COLOR_RESET_ALL
                    )
                    text_handling.exit_game()
                if "agility" not in item_data:
                    print(
                        COLOR_RED + "ERROR: " + COLOR_STYLE_BRIGHT +
                        f"item id '{current}' isn't valid --> "
                        f"missing required `agility` key" +
                        COLOR_RESET_ALL
                    )
                    text_handling.exit_game()
                if "critical hit chance" not in item_data:
                    print(
                        COLOR_RED + "ERROR: " + COLOR_STYLE_BRIGHT +
                        f"item id '{current}' isn't valid --> "
                        f"missing required `critical hit chance` key" +
                        COLOR_RESET_ALL
                    )
                    text_handling.exit_game()
                if "for this upgrade" not in item_data and item_data["upgrade tier"] > 0:
                    print(
                        COLOR_RED + "ERROR: " + COLOR_STYLE_BRIGHT +
                        f"item id '{current}' isn't valid --> "
                        f"missing required `for this upgrade` key" +
                        COLOR_RESET_ALL
                    )
                    text_handling.exit_game()

                if type(item_data["display name"]) is not type(""):
                    print(
                        COLOR_RED + "ERROR: " + COLOR_STYLE_BRIGHT +
                        f"item id '{current}' isn't valid --> "
                        f"entry `display name` isn't a string" +
                        COLOR_RESET_ALL
                    )
                    text_handling.exit_game()
                if type(item_data["upgrade tier"]) is not type(1):
                    print(
                        COLOR_RED + "ERROR: " + COLOR_STYLE_BRIGHT +
                        f"item id '{current}' isn't valid --> "
                        f"entry `upgrade tier` isn't an integer" +
                        COLOR_RESET_ALL
                    )
                    text_handling.exit_game()
                if (
                    type(item_data["damage"]) is not type(.1) and
                    type(item_data["damage"]) is not type(1)
                ):
                    print(
                        COLOR_RED + "ERROR: " + COLOR_STYLE_BRIGHT +
                        f"item id '{current}' isn't valid --> "
                        f"entry `damage` isn't an integer of a floating number" +
                        COLOR_RESET_ALL
                    )
                    text_handling.exit_game()
                if (
                    type(item_data["defend"]) is not type(.1) and
                    type(item_data["defend"]) is not type(1)
                ):
                    print(
                        COLOR_RED + "ERROR: " + COLOR_STYLE_BRIGHT +
                        f"item id '{current}' isn't valid --> "
                        f"entry `defend` isn't an integer of a floating number" +
                        COLOR_RESET_ALL
                    )
                    text_handling.exit_game()
                if (
                    type(item_data["agility"]) is not type(.1) and
                    type(item_data["agility"]) is not type(1)
                ):
                    print(
                        COLOR_RED + "ERROR: " + COLOR_STYLE_BRIGHT +
                        f"item id '{current}' isn't valid --> "
                        f"entry `agility` isn't an integer of a floating number" +
                        COLOR_RESET_ALL
                    )
                    text_handling.exit_game()
                if (
                    type(item_data["critical hit chance"]) is not type(.1) and
                    type(item_data["critical hit chance"]) is not type(1)
                ):
                    print(
                        COLOR_RED + "ERROR: " + COLOR_STYLE_BRIGHT +
                        f"item id '{current}' isn't valid --> "
                        f"entry `critical hit chance` isn't an integer of a floating number" +
                        COLOR_RESET_ALL
                    )
                    text_handling.exit_game()
                if (
                    item_data["upgrade tier"] > 0 and
                    type(item_data["for this upgrade"]) is not type([])
                ):
                    print(
                        COLOR_RED + "ERROR: " + COLOR_STYLE_BRIGHT +
                        f"item id '{current}' isn't valid --> "
                        f"entry `for this upgrade` isn't a list" +
                        COLOR_RESET_ALL
                    )
                    text_handling.exit_game()

                if item_data["upgrade tier"] > 0:
                    for metal in item_data["for this upgrade"]:
                        if metal not in list(item):
                            print(
                                COLOR_RED + "ERROR: " + COLOR_STYLE_BRIGHT +
                                f"item id '{current}' isn't valid --> "
                                f"item `{metal}` in `for this upgrade` doesn't exist" +
                                COLOR_RESET_ALL
                            )
                            text_handling.exit_game()

            elif item_data["type"].startswith('Armor Piece: '):
                if "upgrade tier" not in item_data:
                    print(
                        COLOR_RED + "ERROR: " + COLOR_STYLE_BRIGHT +
                        f"item id '{current}' isn't valid --> "
                        f"missing required `upgrade tier` key" +
                        COLOR_RESET_ALL
                    )
                    text_handling.exit_game()
                if "armor protection" not in item_data:
                    print(
                        COLOR_RED + "ERROR: " + COLOR_STYLE_BRIGHT +
                        f"item id '{current}' isn't valid --> "
                        f"missing required `armor protection` key" +
                        COLOR_RESET_ALL
                    )
                    text_handling.exit_game()
                if "agility" not in item_data:
                    print(
                        COLOR_RED + "ERROR: " + COLOR_STYLE_BRIGHT +
                        f"item id '{current}' isn't valid --> "
                        f"missing required `agility` key" +
                        COLOR_RESET_ALL
                    )
                    text_handling.exit_game()
                if "for this upgrade" not in item_data and item_data["upgrade tier"] > 0:
                    print(
                        COLOR_RED + "ERROR: " + COLOR_STYLE_BRIGHT +
                        f"item id '{current}' isn't valid --> "
                        f"missing required `for this upgrade` key" +
                        COLOR_RESET_ALL
                    )
                    text_handling.exit_game()

                if (
                    "display name" in item_data and
                    type(item_data["display name"]) is not type("")
                ):
                    print(
                        COLOR_RED + "ERROR: " + COLOR_STYLE_BRIGHT +
                        f"item id '{current}' isn't valid --> "
                        f"entry `display name` isn't a string" +
                        COLOR_RESET_ALL
                    )
                    text_handling.exit_game()
                if type(item_data["upgrade tier"]) is not type(1):
                    print(
                        COLOR_RED + "ERROR: " + COLOR_STYLE_BRIGHT +
                        f"item id '{current}' isn't valid --> "
                        f"entry `upgrade tier` isn't an integer" +
                        COLOR_RESET_ALL
                    )
                    text_handling.exit_game()
                if (
                    type(item_data["agility"]) is not type(.1) and
                    type(item_data["agility"]) is not type(1)
                ):
                    print(
                        COLOR_RED + "ERROR: " + COLOR_STYLE_BRIGHT +
                        f"item id '{current}' isn't valid --> "
                        f"entry `agility` isn't an integer of a floating number" +
                        COLOR_RESET_ALL
                    )
                    text_handling.exit_game()
                if (
                    type(item_data["armor protection"]) is not type(.1) and
                    type(item_data["armor protection"]) is not type(1)
                ):
                    print(
                        COLOR_RED + "ERROR: " + COLOR_STYLE_BRIGHT +
                        f"item id '{current}' isn't valid --> "
                        f"entry `armor protection` isn't an integer of a floating number" +
                        COLOR_RESET_ALL
                    )
                    text_handling.exit_game()
                if (
                    item_data["upgrade tier"] > 0 and
                    type(item_data["for this upgrade"]) is not type([])
                ):
                    print(
                        COLOR_RED + "ERROR: " + COLOR_STYLE_BRIGHT +
                        f"item id '{current}' isn't valid --> "
                        f"entry `for this upgrade` isn't a list" +
                        COLOR_RESET_ALL
                    )
                    text_handling.exit_game()

                if item_data["upgrade tier"] > 0:
                    for metal in item_data["for this upgrade"]:
                        if metal not in list(item):
                            print(
                                COLOR_RED + "ERROR: " + COLOR_STYLE_BRIGHT +
                                f"item id '{current}' isn't valid --> "
                                f"item `{metal}` in `for this upgrade` doesn't exist" +
                                COLOR_RESET_ALL
                            )
                            text_handling.exit_game()

            elif item_data["type"] == "Consumable":
                if "effects" not in item_data:
                    print(
                        COLOR_RED + "ERROR: " + COLOR_STYLE_BRIGHT +
                        f"item id '{current}' isn't valid --> "
                        f"missing required `effects` key" +
                        COLOR_RESET_ALL
                    )
                    text_handling.exit_game()

                if type(item_data["effects"]) is not type([]):
                    print(
                        COLOR_RED + "ERROR: " + COLOR_STYLE_BRIGHT +
                        f"item id '{current}' isn't valid --> "
                        f"entry `effects` isn't a list of dictionaries" +
                        COLOR_RESET_ALL
                    )
                    text_handling.exit_game()

            elif item_data["type"] == "Utility":
                if "key" not in item_data:
                    print(
                        COLOR_RED + "ERROR: " + COLOR_STYLE_BRIGHT +
                        f"item id '{current}' isn't valid --> "
                        f"missing required `key` key" +
                        COLOR_RESET_ALL
                    )
                    text_handling.exit_game()
                if "script name" not in item_data:
                    print(
                        COLOR_RED + "ERROR: " + COLOR_STYLE_BRIGHT +
                        f"item id '{current}' isn't valid --> "
                        f"missing required `script name` key" +
                        COLOR_RESET_ALL
                    )
                    text_handling.exit_game()

                if type(item_data["key"]) is not type(""):
                    print(
                        COLOR_RED + "ERROR: " + COLOR_STYLE_BRIGHT +
                        f"item id '{current}' isn't valid --> "
                        f"entry `key` isn't a string" +
                        COLOR_RESET_ALL
                    )
                    text_handling.exit_game()
                if type(item_data["script name"]) is not type(""):
                    print(
                        COLOR_RED + "ERROR: " + COLOR_STYLE_BRIGHT +
                        f"item id '{current}' isn't valid --> "
                        f"entry `script name` isn't a string" +
                        COLOR_RESET_ALL
                    )
                    text_handling.exit_game()
                if (
                    "arguments" in item_data and
                    type(item_data["arguments"]) is not type([])
                ):
                    print(
                        COLOR_RED + "ERROR: " + COLOR_STYLE_BRIGHT +
                        f"item id '{current}' isn't valid --> "
                        f"entry `arguments` isn't a list" +
                        COLOR_RESET_ALL
                    )
                    text_handling.exit_game()

                possible_arguments = [
                    "player", "map", "item", "drinks", "enemy", "npcs",
                    "start_player", "lists", "zone", "dialog", "mission",
                    "mounts", "start_time", "generic_text_replacements",
                    "preferences"
                ]
                if "arguments" in item_data:
                    for argument in item_data["arguments"]:
                        if argument not in possible_arguments:
                            print(
                                COLOR_RED + "ERROR: " + COLOR_STYLE_BRIGHT +
                                f"item id '{current}' isn't valid --> "
                                f"argument `{argument}` in arguments key " +
                                "is not a valid one" +
                                COLOR_RESET_ALL
                            )
                            text_handling.exit_game()

            elif item_data["type"] == "Bag":
                if "inventory slots" not in item_data:
                    print(
                        COLOR_RED + "ERROR: " + COLOR_STYLE_BRIGHT +
                        f"item id '{current}' isn't valid --> "
                        f"missing required `inventory slots` key" +
                        COLOR_RESET_ALL
                    )
                    text_handling.exit_game()

                if type(item_data["inventory slots"]) is not type(1):
                    print(
                        COLOR_RED + "ERROR: " + COLOR_STYLE_BRIGHT +
                        f"item id '{current}' isn't valid --> "
                        f"entry `inventory slots` isn't an integer" +
                        COLOR_RESET_ALL
                    )
                    text_handling.exit_game()

            elif item_data["type"] == "Food":
                if "max bonus" not in item_data:
                    print(
                        COLOR_RED + "ERROR: " + COLOR_STYLE_BRIGHT +
                        f"item id '{current}' isn't valid --> "
                        f"missing required `max bonus` key" +
                        COLOR_RESET_ALL
                    )
                    text_handling.exit_game()
                if "healing level" not in item_data:
                    print(
                        COLOR_RED + "ERROR: " + COLOR_STYLE_BRIGHT +
                        f"item id '{current}' isn't valid --> "
                        f"missing required `healing level` key" +
                        COLOR_RESET_ALL
                    )
                    text_handling.exit_game()

                if type(item_data["max bonus"]) is not type(1):
                    print(
                        COLOR_RED + "ERROR: " + COLOR_STYLE_BRIGHT +
                        f"item id '{current}' isn't valid --> "
                        f"entry `max bonus` isn't an integer" +
                        COLOR_RESET_ALL
                    )
                    text_handling.exit_game()
                if type(item_data["healing level"]) is not type(1):
                    print(
                        COLOR_RED + "ERROR: " + COLOR_STYLE_BRIGHT +
                        f"item id '{current}' isn't valid --> "
                        f"entry `healing level` isn't an integer" +
                        COLOR_RESET_ALL
                    )
                    text_handling.exit_game()

                elif item_data["type"] == "Map":
                    if "map" not in item_data:
                        print(
                            COLOR_RED + "ERROR: " + COLOR_STYLE_BRIGHT +
                            f"item id '{current}' isn't valid --> "
                            f"missing required `map` key" +
                            COLOR_RESET_ALL
                        )
                        text_handling.exit_game()

                    if type(item_data["inventory slots"]) is not type(""):
                        print(
                            COLOR_RED + "ERROR: " + COLOR_STYLE_BRIGHT +
                            f"item id '{current}' isn't valid --> "
                            f"entry `map` isn't an string" +
                            COLOR_RESET_ALL
                        )
                        text_handling.exit_game()

                elif item_data["type"] == "Lure":
                    for i in item_data["preferred types"]:
                        if i not in item:
                            print(
                                COLOR_RED + "ERROR: " + COLOR_STYLE_BRIGHT +
                                f"item id '{current}' isn't valid --> "
                                f"entry `{i}` in `preferred types is not an"
                                + "existing item" +
                                COLOR_RESET_ALL
                            )
                            text_handling.exit_game()

            item_types = [
                "Weapon", "Armor Piece: Chestplate", "Armor Piece: Leggings",
                "Armor Piece: Boots", "Consumable", "Utility", "Bag", "Food",
                "Key", "Note", "Map", "Metal", "Primary Material", "Misc",
                "Armor Piece: Shield", "Fishing Rod", "Lure"
            ]

            if item_data["type"] not in item_types:
                print(
                    COLOR_RED + "ERROR: " + COLOR_STYLE_BRIGHT +
                    f"item id '{current}' isn't valid --> "
                    f"item type `{item_data['type']}` doesn't exist" +
                    COLOR_RESET_ALL
                )
                text_handling.exit_game()

            # Verify game main commands
            existing_keys = [
                "n", "e", "w", "s", "sw", "se", "ne", "nw",
                "d", "i", "z", "y", "x", "p", "q", "k", "c", "f",
                "$player$data$", "$game$data$", "$spawn$enemy$",
                "$teleport$zone$", "$find$point$", "$teleport$point$",
                "$help$", "$run$dialog$", "$run$script$"
            ]
            for current in list(item):
                if item[current]["type"] == "Utility":
                    existing_keys += [item[current]["key"].lower()]

            for key in existing_keys:
                if existing_keys.count(key) > 1:
                    print(
                        COLOR_RED + "ERROR: " + COLOR_STYLE_BRIGHT +
                        f"Duplicated game main command `{key}` -->" +
                        " check the utility items" +
                        COLOR_RESET_ALL
                    )
                    text_handling.exit_game()

    # Specific checks for the `drinks` dictionary
    # CHECKS:
    # - check if every keys is there
    # - check if every key is valid
    for current in list(drinks):
        drink_data = drinks[current]

        if "gold" not in drink_data:
            print(
                COLOR_RED + "ERROR: " + COLOR_STYLE_BRIGHT +
                f"drink id '{current}' isn't valid --> "
                f"missing required `gold` key" +
                COLOR_RESET_ALL
            )
            text_handling.exit_game()
        if "healing level" not in drink_data:
            print(
                COLOR_RED + "ERROR: " + COLOR_STYLE_BRIGHT +
                f"drink id '{current}' isn't valid --> "
                f"missing required `healing level` key" +
                COLOR_RESET_ALL
            )
            text_handling.exit_game()
        if "description" not in drink_data:
            print(
                COLOR_RED + "ERROR: " + COLOR_STYLE_BRIGHT +
                f"drink id '{current}' isn't valid --> "
                f"missing required `description` key" +
                COLOR_RESET_ALL
            )
            text_handling.exit_game()

        if (
            type(drink_data["gold"]) is not type(1) and
            type(drink_data["gold"]) is not type(.1)
        ):
            print(
                COLOR_RED + "ERROR: " + COLOR_STYLE_BRIGHT +
                f"drink id '{current}' isn't valid --> "
                f"key `gold` isn't an integer or a floating number" +
                COLOR_RESET_ALL
            )
            text_handling.exit_game()
        if (
            type(drink_data["healing level"]) is not type(1) and
            type(drink_data["healing level"]) is not type(.1)
        ):
            print(
                COLOR_RED + "ERROR: " + COLOR_STYLE_BRIGHT +
                f"drink id '{current}' isn't valid --> "
                f"key `healing level` isn't an integer or a floating number" +
                COLOR_RESET_ALL
            )
            text_handling.exit_game()
        if drink_data["healing level"] > 999:
            print(
                COLOR_RED + "ERROR: " + COLOR_STYLE_BRIGHT +
                f"drink id '{current}' isn't valid --> "
                f"key `healing level` is greater than 999" +
                COLOR_RESET_ALL
            )
            text_handling.exit_game()
        if type(drink_data["description"]) is not type(""):
            print(
                COLOR_RED + "ERROR: " + COLOR_STYLE_BRIGHT +
                f"drink id '{current}' isn't valid --> "
                f"key `description` isn't a string" +
                COLOR_RESET_ALL
            )
            text_handling.exit_game()

    # Specific checks for the `enemy` dictionary
    # CHECKS:
    # - check if its inventory has existing items
    for current in list(enemy):
        enemy_data = enemy[current]

        for i in enemy_data["inventory"]:
            if i not in list(item):
                print(
                    COLOR_RED + "ERROR: " + COLOR_STYLE_BRIGHT +
                    f"enemy id '{current}' isn't valid --> "
                    f"item `{i}` in `inventory` doesn't exist" +
                    COLOR_RESET_ALL
                )
                text_handling.exit_game()

    # Specific checks for the `npcs` dictionary
    # CHECKS:
    # - check if sold drinks exist
    # - check if sold items exist
    # - check if bought items exist
    for current in list(npcs):
        npc_data = npcs[current]

        for i in npc_data["sells"]["drinks"]:
            if (
                npc_data["sells"]["drinks"].count("None") > 0 and
                len(npc_data["sells"]["drinks"]) > 2
            ):
                print(
                    COLOR_RED + "ERROR: " + COLOR_STYLE_BRIGHT +
                    f"npc id '{current}' isn't valid --> " +
                    f"`None` entry is used in sold drinks," +
                    " but other drinks are present" +
                    COLOR_RESET_ALL
                )
                text_handling.exit_game()
            if i != "None" and i not in list(drinks):
                print(
                    COLOR_RED + "ERROR: " + COLOR_STYLE_BRIGHT +
                    f"npc id '{current}' isn't valid --> " +
                    f"drink `{i}` in sold drinks doesn't exist" +
                    COLOR_RESET_ALL
                )
                text_handling.exit_game()
            if npc_data["sells"]["drinks"].count(i) > 1:
                print(
                    COLOR_RED + "ERROR: " + COLOR_STYLE_BRIGHT +
                    f"npc id '{current}' isn't valid --> " +
                    f"drink `{i}` in sold drinks is duplicated" +
                    COLOR_RESET_ALL
                )
                text_handling.exit_game()
        for i in npc_data["sells"]["items"]:
            if (
                npc_data["sells"]["items"].count("None") > 0 and
                len(npc_data["sells"]["items"]) > 2
            ):
                print(
                    COLOR_RED + "ERROR: " + COLOR_STYLE_BRIGHT +
                    f"npc id '{current}' isn't valid --> " +
                    f"`None` entry is used in sold items," +
                    " but other items are present" +
                    COLOR_RESET_ALL
                )
                text_handling.exit_game()
            if i != "None" and i not in list(item):
                print(
                    COLOR_RED + "ERROR: " + COLOR_STYLE_BRIGHT +
                    f"npc id '{current}' isn't valid --> " +
                    f"item `{i}` in sold items doesn't exist" +
                    COLOR_RESET_ALL
                )
                text_handling.exit_game()
            if npc_data["sells"]["items"].count(i) > 1:
                print(
                    COLOR_RED + "ERROR: " + COLOR_STYLE_BRIGHT +
                    f"npc id '{current}' isn't valid --> " +
                    f"item `{i}` in sold items is duplicated" +
                    COLOR_RESET_ALL
                )
                text_handling.exit_game()
        for i in npc_data["buys"]["items"]:
            if (
                npc_data["buys"]["items"].count("None") > 0 and
                len(npc_data["buys"]["items"]) > 2
            ):
                print(
                    COLOR_RED + "ERROR: " + COLOR_STYLE_BRIGHT +
                    f"npc id '{current}' isn't valid --> " +
                    f"`None` entry is used in bought items," +
                    " but other items are present" +
                    COLOR_RESET_ALL
                )
                text_handling.exit_game()
            if i != "None" and i not in list(item):
                print(
                    COLOR_RED + "ERROR: " + COLOR_STYLE_BRIGHT +
                    f"npc id '{current}' isn't valid --> " +
                    f"item `{i}` in bought items doesn't exist" +
                    COLOR_RESET_ALL
                )
                text_handling.exit_game()
            if npc_data["buys"]["items"].count(i) > 1:
                print(
                    COLOR_RED + "ERROR: " + COLOR_STYLE_BRIGHT +
                    f"npc id '{current}' isn't valid --> " +
                    f"item `{i}` in bougt items is duplicated" +
                    COLOR_RESET_ALL
                )
                text_handling.exit_game()

    # Specific checks of `lists` dictionary
    # CHECKS:
    # - for every pool in a list:
    #   * verify if the chance is under or equal to 1
    #   * verify if the chance is over 0
    #   * for every rates:
    #     - check if any min or max amount is over 0
    #     - check if the min is greater than the mount
    #   * check if the spawned enemies exist
    for current in list(lists):
        list_data = lists[current]
        for current2 in list(list_data):
            pool_data = list_data[current2]

            if (
                pool_data["chance"] > 1 or
                pool_data["chance"] < 0
            ):
                print(
                    COLOR_RED + "ERROR: " + COLOR_STYLE_BRIGHT +
                    f"pool '{current2}' in list id '{current}' isn't valid --> " +
                    f"spawning chance {pool_data['chance']} must be over 0 and under 1" +
                    COLOR_RESET_ALL
                )
                text_handling.exit_game()

            for rate in list(pool_data["enemies rate"]):
                rate = pool_data["enemies rate"][rate]
                if rate["min"] <= 0 or rate["max"] <= 0:
                    print(
                        COLOR_RED + "ERROR: " + COLOR_STYLE_BRIGHT +
                        f"pool '{current2}' in list id '{current}' isn't valid --> " +
                        "enemies spawning rate min and max values should be over 0" +
                        COLOR_RESET_ALL
                    )
                    text_handling.exit_game()
                if rate["min"] > rate["max"]:
                    print(
                        COLOR_RED + "ERROR: " + COLOR_STYLE_BRIGHT +
                        f"pool '{current2}' in list id '{current}' isn't valid --> " +
                        "min spawning rate should be under max spawning rate" +
                        COLOR_RESET_ALL
                    )
                    text_handling.exit_game()

            for i in list(pool_data["enemies spawns"]):
                if i not in list(enemy):
                    print(
                        COLOR_RED + "ERROR: " + COLOR_STYLE_BRIGHT +
                        f"pool '{current2}' in list id '{current}' isn't valid --> " +
                        f"enemy `{i}` in enemies spawns doesn't exist" +
                        COLOR_RESET_ALL
                    )
                    text_handling.exit_game()

    # Specific checks of the `zone` dictionary
    # CHECKS:
    # EVERY TYPE:
    # - check if zone type exists
    # - check if enemy spawning pool exist
    # SEAS & LAKES:
    # - check if the items in the fishing drops exists
    # VILLAGES:
    # - check if the put contents exist
    # HOSTELS:
    # - check if sold items and drinks exist
    # - check if bought items exist
    # - checks on discounts:
    #   * check if time space is grater than 0
    #   * check if chance is over or equal to 0 and under or equal to 1
    #   * check if max dropoff is greater or equal than min dropoff
    # FORGES:
    # - check if sold items exist
    # - check if bought items exist
    # - checks on discounts:
    #   * check if time space is grater than 0
    #   * check if chance is over or equal to 0 and under or equal to 1
    #   * check if max dropoff is greater or equal than min dropoff
    # STABLES:
    # - check if the sold mounts exist
    # - check if the sold drinks exist
    # - check if the sold items exist
    # - checks on discounts:
    #   * check if time space is grater than 0
    #   * check if chance is over or equal to 0 and under or equal to 1
    #   * check if max dropoff is greater or equal than min dropoff
    # BLACKSMITHS:
    # - check if bought items exist
    # - checks on orders:
    #   * check if ordered item exist
    #   * check if time needed is greater or equal to 0
    #   * check if needed materials exist
    # - checks on discounts:
    #   * check if time space is grater than 0
    #   * check if chance is over or equal to 0 and under or equal to 1
    #   * check if max dropoff is greater or equal than min dropoff
    # GROCERY STORES:
    # - check if the sold items exist
    # - checks on discounts:
    #   * check if time space is grater than 0
    #   * check if chance is over or equal to 0 and under or equal to 1
    #   * check if max dropoff is greater or equal than min dropoff
    # HARBORS:
    # - checks on destinations:
    #   * check if every keys are there
    #   * check if every keys are the right type
    #   * check if the destination point exists
    # - checks on discounts:
    #   * check if time space is grater than 0
    #   * check if chance is over or equal to 0 and under or equal to 1
    #   * check if max dropoff is greater or equal than min dropoff
    # DUNGEONS:
    # - check if rooms number is equal to the length of the rooms dictionary
    # - check if the reward dialog exists
    # - checks on rooms:
    #   * check if every keys are there
    #   * check if every keys are the right type
    #   * check if type is valid
    #   * check if room digit is in between 0 and the rooms number
    #   * check if the room digit isn't duplicated
    #   * check if required data is there
    #   * check if spawned enemy list exists
    #   * check if reward items exist
    #   * check if script arguments exist
    for current in list(zone):
        current_zone = zone[current]
        existing_types = [
            "fields", "hills", "valleys", "woods", "dark woods", "mountains",
            "low mountains", "high mountains", "black rocky mountains", "desert",
            "desert hills", "desert valleys", "badlands", "badlands canyon",
            "badlands hills", "badland valleys", "badlands plateau", "badlands butte",
            "badlands landforms", "flatlands", "beach", "plains canyon", "desert canyons",
            "rocky canyons", "black rocky canyons", "village", "hostel", "forge", "blacksmith",
            "stable", "church", "lake", "sea", "grocery", "harbor", "dungeon", "swamps"
        ]

        if current_zone["type"] not in existing_types:
            print(
                COLOR_RED + "ERROR: " + COLOR_STYLE_BRIGHT +
                f"map zone id '{current}' isn't valid --> "
                f"zone type `{current_zone['type']}` doesn't exist" +
                COLOR_RESET_ALL
            )
            text_handling.exit_game()
        if (
            "enemy spawning" in current_zone and
            current_zone["enemy spawning"] not in list(lists)
        ):
            print(
                COLOR_RED + "ERROR: " + COLOR_STYLE_BRIGHT +
                f"map zone id '{current}' isn't valid --> "
                f"enemy list `{current_zone['enemy spawning']}` doesn't exist" +
                COLOR_RESET_ALL
            )
            text_handling.exit_game()

        if current_zone["type"] in ["sea", "lake"]:
            for i in current_zone["fishing"]:
                if i not in list(item):
                    print(
                        COLOR_RED + "ERROR: " + COLOR_STYLE_BRIGHT +
                        f"map zone id '{current}' isn't valid --> " +
                        f"item '{i}' in `fishing` doesn't exist" +
                        COLOR_RESET_ALL
                    )
                    exit_game()

        if current_zone["type"] == "village":
            for content_id in list(current_zone["content"]):
                content = current_zone["content"][content_id]
                for i in content:
                    if (
                        content.count("None") > 0 and
                        len(content) > 2
                    ):
                        print(
                            COLOR_RED + "ERROR: " + COLOR_STYLE_BRIGHT +
                            f"map zone id '{current}' isn't valid --> " +
                            f"`None` entry is used in '{content_id}' content," +
                            " but other map zones are present" +
                            COLOR_RESET_ALL
                        )
                        text_handling.exit_game()
                    if i != "None" and i not in list(zone):
                        print(
                            COLOR_RED + "ERROR: " + COLOR_STYLE_BRIGHT +
                            f"map zone id '{current}' isn't valid --> " +
                            f"map zone `{i}` in '{content_id}' content doesn't exist" +
                            COLOR_RESET_ALL
                        )
                        text_handling.exit_game()
                    if content.count(i) > 1:
                        print(
                            COLOR_RED + "ERROR: " + COLOR_STYLE_BRIGHT +
                            f"map zone id '{current}' isn't valid --> " +
                            f"map zone `{i}` in '{content_id}' content is duplicated" +
                            COLOR_RESET_ALL
                        )
                        text_handling.exit_game()

        elif current_zone["type"] == "hostel":
            for i in current_zone["sells"]["drinks"]:
                if (
                    current_zone["sells"]["drinks"].count("None") > 0 and
                    len(current_zone["sells"]["drinks"]) > 2
                ):
                    print(
                        COLOR_RED + "ERROR: " + COLOR_STYLE_BRIGHT +
                        f"map zone id '{current}' isn't valid --> " +
                        f"`None` entry is used in sold drinks," +
                        " but other drinks are present" +
                        COLOR_RESET_ALL
                    )
                    text_handling.exit_game()
                if i != "None" and i not in list(drinks):
                    print(
                        COLOR_RED + "ERROR: " + COLOR_STYLE_BRIGHT +
                        f"map zone id '{current}' isn't valid --> " +
                        f"drink `{i}` in sold drinks doesn't exist" +
                        COLOR_RESET_ALL
                    )
                    text_handling.exit_game()
                if current_zone["sells"]["drinks"].count(i) > 1:
                    print(
                        COLOR_RED + "ERROR: " + COLOR_STYLE_BRIGHT +
                        f"map zone id '{current}' isn't valid --> " +
                        f"drink `{i}` in sold drinks is duplicated" +
                        COLOR_RESET_ALL
                    )
                    text_handling.exit_game()
            for i in current_zone["sells"]["items"]:
                if (
                    current_zone["sells"]["items"].count("None") > 0 and
                    len(current_zone["sells"]["items"]) > 2
                ):
                    print(
                        COLOR_RED + "ERROR: " + COLOR_STYLE_BRIGHT +
                        f"map zone id '{current}' isn't valid --> " +
                        f"`None` entry is used in sold items," +
                        " but other items are present" +
                        COLOR_RESET_ALL
                    )
                    text_handling.exit_game()
                if i != "None" and i not in list(item):
                    print(
                        COLOR_RED + "ERROR: " + COLOR_STYLE_BRIGHT +
                        f"map zone id '{current}' isn't valid --> " +
                        f"item `{i}` in sold items doesn't exist" +
                        COLOR_RESET_ALL
                    )
                    text_handling.exit_game()
                if current_zone["sells"]["items"].count(i) > 1:
                    print(
                        COLOR_RED + "ERROR: " + COLOR_STYLE_BRIGHT +
                        f"map zone id '{current}' isn't valid --> " +
                        f"item `{i}` in sold items is duplicated" +
                        COLOR_RESET_ALL
                    )
                    text_handling.exit_game()
            for i in current_zone["buys"]["items"]:
                if (
                    current_zone["buys"]["items"].count("None") > 0 and
                    len(current_zone["buys"]["items"]) > 2
                ):
                    print(
                        COLOR_RED + "ERROR: " + COLOR_STYLE_BRIGHT +
                        f"map zone id '{current}' isn't valid --> " +
                        "`None` entry is used in bought items," +
                        " but other items are present" +
                        COLOR_RESET_ALL
                    )
                    text_handling.exit_game()
                if i != "None" and i not in list(item):
                    print(
                        COLOR_RED + "ERROR: " + COLOR_STYLE_BRIGHT +
                        f"map zone id '{current}' isn't valid --> " +
                        f"item `{i}` in bought items doesn't exist" +
                        COLOR_RESET_ALL
                    )
                    text_handling.exit_game()
                if current_zone["buys"]["items"].count(i) > 1:
                    print(
                        COLOR_RED + "ERROR: " + COLOR_STYLE_BRIGHT +
                        f"map zone id '{current}' isn't valid --> " +
                        f"item `{i}` in bought items is duplicated" +
                        COLOR_RESET_ALL
                    )
                    text_handling.exit_game()

            if current_zone["discounts"]["time space"] < 0:
                print(
                    COLOR_RED + "ERROR: " + COLOR_STYLE_BRIGHT +
                    f"map zone id '{current}' isn't valid --> " +
                    "discounts time space should be greater or equal to 0" +
                    COLOR_RESET_ALL
                )
                text_handling.exit_game()
            if (
                current_zone["discounts"]["chance"] < 0 or
                current_zone["discounts"]["chance"] > 1
            ):
                print(
                    COLOR_RED + "ERROR: " + COLOR_STYLE_BRIGHT +
                    f"map zone id '{current}' isn't valid --> " +
                    "discounts chance should be greater or equal " +
                    "to 0, and over or equal to 1" +
                    COLOR_RESET_ALL
                )
                text_handling.exit_game()
            if (
                current_zone["discounts"]["discount"]["max dropoff"] <
                current_zone["discounts"]["discount"]["max dropoff"]
            ):
                print(
                    COLOR_RED + "ERROR: " + COLOR_STYLE_BRIGHT +
                    f"map zone id '{current}' isn't valid --> " +
                    "discounts max dropoff should be greater or " +
                    "equal to the min dropoff" +
                    COLOR_RESET_ALL
                )
                text_handling.exit_game()

        elif current_zone["type"] == "forge":
            for i in current_zone["forge"]["buys"]:
                if (
                    current_zone["forge"]["buys"].count("None") > 0 and
                    len(current_zone["forge"]["buys"]) > 2
                ):
                    print(
                        COLOR_RED + "ERROR: " + COLOR_STYLE_BRIGHT +
                        f"map zone id '{current}' isn't valid --> " +
                        "`None` entry is used in bought items," +
                        " but other items are present" +
                        COLOR_RESET_ALL
                    )
                    text_handling.exit_game()
                if i != "None" and i not in list(item):
                    print(
                        COLOR_RED + "ERROR: " + COLOR_STYLE_BRIGHT +
                        f"map zone id '{current}' isn't valid --> " +
                        f"item `{i}` in bought items doesn't exist" +
                        COLOR_RESET_ALL
                    )
                    text_handling.exit_game()
                if current_zone["forge"]["buys"].count(i) > 1:
                    print(
                        COLOR_RED + "ERROR: " + COLOR_STYLE_BRIGHT +
                        f"map zone id '{current}' isn't valid --> " +
                        f"item `{i}` in bought items is duplicated" +
                        COLOR_RESET_ALL
                    )
                    text_handling.exit_game()
            for i in current_zone["forge"]["sells"]:
                if (
                    current_zone["forge"]["sells"].count("None") > 0 and
                    len(current_zone["forge"]["sells"]) > 2
                ):
                    print(
                        COLOR_RED + "ERROR: " + COLOR_STYLE_BRIGHT +
                        f"map zone id '{current}' isn't valid --> " +
                        "`None` entry is used in sold items," +
                        " but other items are present" +
                        COLOR_RESET_ALL
                    )
                    text_handling.exit_game()
                if i != "None" and i not in list(item):
                    print(
                        COLOR_RED + "ERROR: " + COLOR_STYLE_BRIGHT +
                        f"map zone id '{current}' isn't valid --> " +
                        f"item `{i}` in sold items doesn't exist" +
                        COLOR_RESET_ALL
                    )
                    text_handling.exit_game()
                if current_zone["forge"]["sells"].count(i) > 1:
                    print(
                        COLOR_RED + "ERROR: " + COLOR_STYLE_BRIGHT +
                        f"map zone id '{current}' isn't valid --> " +
                        f"item `{i}` in sold items is duplicated" +
                        COLOR_RESET_ALL
                    )
                    text_handling.exit_game()

            if current_zone["discounts"]["time space"] < 0:
                print(
                    COLOR_RED + "ERROR: " + COLOR_STYLE_BRIGHT +
                    f"map zone id '{current}' isn't valid --> " +
                    "discounts time space should be greater or equal to 0" +
                    COLOR_RESET_ALL
                )
                text_handling.exit_game()
            if (
                current_zone["discounts"]["chance"] < 0 or
                current_zone["discounts"]["chance"] > 1
            ):
                print(
                    COLOR_RED + "ERROR: " + COLOR_STYLE_BRIGHT +
                    f"map zone id '{current}' isn't valid --> " +
                    "discounts chance should be greater or equal " +
                    "to 0, and over or equal to 1" +
                    COLOR_RESET_ALL
                )
                text_handling.exit_game()
            if (
                current_zone["discounts"]["discount"]["max dropoff"] <
                current_zone["discounts"]["discount"]["max dropoff"]
            ):
                print(
                    COLOR_RED + "ERROR: " + COLOR_STYLE_BRIGHT +
                    f"map zone id '{current}' isn't valid --> " +
                    "discounts max dropoff should be greater or " +
                    "equal to the min dropoff" +
                    COLOR_RESET_ALL
                )
                text_handling.exit_game()

        elif current_zone["type"] == "stable":
            for i in current_zone["stable"]["sells"]["mounts"]:
                if (
                    current_zone["stable"]["sells"]["mounts"].count("None") > 0 and
                    len(current_zone["stable"]["sells"]["mounts"]) > 2
                ):
                    print(
                        COLOR_RED + "ERROR: " + COLOR_STYLE_BRIGHT +
                        f"map zone id '{current}' isn't valid --> " +
                        "`None` entry is used in sold mounts," +
                        " but other mounts are present" +
                        COLOR_RESET_ALL
                    )
                    text_handling.exit_game()
                if i != "None" and i not in list(mounts):
                    print(
                        COLOR_RED + "ERROR: " + COLOR_STYLE_BRIGHT +
                        f"map zone id '{current}' isn't valid --> " +
                        f"mount `{i}` in sold mounts doesn't exist" +
                        COLOR_RESET_ALL
                    )
                    text_handling.exit_game()
                if current_zone["stable"]["sells"]["mounts"].count(i) > 1:
                    print(
                        COLOR_RED + "ERROR: " + COLOR_STYLE_BRIGHT +
                        f"map zone id '{current}' isn't valid --> " +
                        f"mount `{i}` in sold mounts is duplicated" +
                        COLOR_RESET_ALL
                    )
                    text_handling.exit_game()
            for i in current_zone["stable"]["sells"]["drinks"]:
                if (
                    current_zone["stable"]["sells"]["drinks"].count("None") > 0 and
                    len(current_zone["stable"]["sells"]["drinks"]) > 2
                ):
                    print(
                        COLOR_RED + "ERROR: " + COLOR_STYLE_BRIGHT +
                        f"map zone id '{current}' isn't valid --> " +
                        "`None` entry is used in sold drinks," +
                        " but other drinks are present" +
                        COLOR_RESET_ALL
                    )
                    text_handling.exit_game()
                if i != "None" and i not in list(drinks):
                    print(
                        COLOR_RED + "ERROR: " + COLOR_STYLE_BRIGHT +
                        f"map zone id '{current}' isn't valid --> " +
                        f"drink `{i}` in sold drinks doesn't exist" +
                        COLOR_RESET_ALL
                    )
                    text_handling.exit_game()
                if current_zone["stable"]["sells"]["drinks"].count(i) > 1:
                    print(
                        COLOR_RED + "ERROR: " + COLOR_STYLE_BRIGHT +
                        f"map zone id '{current}' isn't valid --> " +
                        f"drink `{i}` in sold drinks is duplicated" +
                        COLOR_RESET_ALL
                    )
                    text_handling.exit_game()
            for i in current_zone["stable"]["sells"]["items"]:
                if (
                    current_zone["stable"]["sells"]["items"].count("None") > 0 and
                    len(current_zone["stable"]["sells"]["items"]) > 2
                ):
                    print(
                        COLOR_RED + "ERROR: " + COLOR_STYLE_BRIGHT +
                        f"map zone id '{current}' isn't valid --> " +
                        "`None` entry is used in sold items," +
                        " but other items are present" +
                        COLOR_RESET_ALL
                    )
                    text_handling.exit_game()
                if i != "None" and i not in list(item):
                    print(
                        COLOR_RED + "ERROR: " + COLOR_STYLE_BRIGHT +
                        f"map zone id '{current}' isn't valid --> " +
                        f"item `{i}` in sold items doesn't exist" +
                        COLOR_RESET_ALL
                    )
                    text_handling.exit_game()
                if current_zone["stable"]["sells"]["items"].count(i) > 1:
                    print(
                        COLOR_RED + "ERROR: " + COLOR_STYLE_BRIGHT +
                        f"map zone id '{current}' isn't valid --> " +
                        f"item `{i}` in sold items is duplicated" +
                        COLOR_RESET_ALL
                    )
                    text_handling.exit_game()

            if current_zone["discounts"]["time space"] < 0:
                print(
                    COLOR_RED + "ERROR: " + COLOR_STYLE_BRIGHT +
                    f"map zone id '{current}' isn't valid --> " +
                    "discounts time space should be greater or equal to 0" +
                    COLOR_RESET_ALL
                )
                text_handling.exit_game()
            if (
                current_zone["discounts"]["chance"] < 0 or
                current_zone["discounts"]["chance"] > 1
            ):
                print(
                    COLOR_RED + "ERROR: " + COLOR_STYLE_BRIGHT +
                    f"map zone id '{current}' isn't valid --> " +
                    "discounts chance should be greater or equal " +
                    "to 0, and over or equal to 1" +
                    COLOR_RESET_ALL
                )
                text_handling.exit_game()
            if (
                current_zone["discounts"]["discount"]["max dropoff"] <
                current_zone["discounts"]["discount"]["max dropoff"]
            ):
                print(
                    COLOR_RED + "ERROR: " + COLOR_STYLE_BRIGHT +
                    f"map zone id '{current}' isn't valid --> " +
                    "discounts max dropoff should be greater or " +
                    "equal to the min dropoff" +
                    COLOR_RESET_ALL
                )
                text_handling.exit_game()

        elif current_zone["type"] == "blacksmith":
            for i in current_zone["blacksmith"]["buys"]:
                if (
                    current_zone["blacksmith"]["buys"].count("None") > 0 and
                    len(current_zone["blacksmith"]["buys"]) > 2
                ):
                    print(
                        COLOR_RED + "ERROR: " + COLOR_STYLE_BRIGHT +
                        f"map zone id '{current}' isn't valid --> " +
                        "`None` entry is used in bought items," +
                        " but other items are present" +
                        COLOR_RESET_ALL
                    )
                    text_handling.exit_game()
                if i != "None" and i not in list(item):
                    print(
                        COLOR_RED + "ERROR: " + COLOR_STYLE_BRIGHT +
                        f"map zone id '{current}' isn't valid --> " +
                        f"item `{i}` in bought items doesn't exist" +
                        COLOR_RESET_ALL
                    )
                    text_handling.exit_game()
                if current_zone["blacksmith"]["buys"].count(i) > 1:
                    print(
                        COLOR_RED + "ERROR: " + COLOR_STYLE_BRIGHT +
                        f"map zone id '{current}' isn't valid --> " +
                        f"item `{i}` in bought items is duplicated" +
                        COLOR_RESET_ALL
                    )
                    text_handling.exit_game()

            for order_id in list(current_zone["blacksmith"]["orders"]):
                order = current_zone["blacksmith"]["orders"][order_id]

                if order_id not in list(item):
                    print(
                        COLOR_RED + "ERROR: " + COLOR_STYLE_BRIGHT +
                        f"order id '{order_id}' in map zone id '{current}' isn't valid --> " +
                        f"item `{order_id}` in order item doesn't exist" +
                        COLOR_RESET_ALL
                    )
                    text_handling.exit_game()
                if order["time needed"] < 0:
                    print(
                        COLOR_RED + "ERROR: " + COLOR_STYLE_BRIGHT +
                        f"order id '{order_id}' in map zone id '{current}' isn't valid --> " +
                        f"time needed should be over or equal to 0" +
                        COLOR_RESET_ALL
                    )
                    text_handling.exit_game()
                for i in order["needed materials"]:
                    if i not in list(item):
                        print(
                            COLOR_RED + "ERROR: " + COLOR_STYLE_BRIGHT +
                            f"order id '{order_id}' in map zone id '{current}' isn't valid --> " +
                            f"item `{i}` in needed materials doesn't exist" +
                            COLOR_RESET_ALL
                        )
                        text_handling.exit_game()

            if current_zone["discounts"]["time space"] < 0:
                print(
                    COLOR_RED + "ERROR: " + COLOR_STYLE_BRIGHT +
                    f"map zone id '{current}' isn't valid --> " +
                    "discounts time space should be greater or equal to 0" +
                    COLOR_RESET_ALL
                )
                text_handling.exit_game()
            if (
                current_zone["discounts"]["chance"] < 0 or
                current_zone["discounts"]["chance"] > 1
            ):
                print(
                    COLOR_RED + "ERROR: " + COLOR_STYLE_BRIGHT +
                    f"map zone id '{current}' isn't valid --> " +
                    "discounts chance should be greater or equal " +
                    "to 0, and over or equal to 1" +
                    COLOR_RESET_ALL
                )
                text_handling.exit_game()
            if (
                current_zone["discounts"]["discount"]["max dropoff"] <
                current_zone["discounts"]["discount"]["max dropoff"]
            ):
                print(
                    COLOR_RED + "ERROR: " + COLOR_STYLE_BRIGHT +
                    f"map zone id '{current}' isn't valid --> " +
                    "discounts max dropoff should be greater or " +
                    "equal to the min dropoff" +
                    COLOR_RESET_ALL
                )
                text_handling.exit_game()

        elif current_zone["type"] == "grocery":
            for i in current_zone["items sold"]:
                if i not in list(item):
                    print(
                        COLOR_RED + "ERROR: " + COLOR_STYLE_BRIGHT +
                        f"map zone id '{current}' isn't valid --> " +
                        f"item `{i}` in sold items doesn't exist" +
                        COLOR_RESET_ALL
                    )
                    text_handling.exit_game()

            if current_zone["discounts"]["time space"] < 0:
                print(
                    COLOR_RED + "ERROR: " + COLOR_STYLE_BRIGHT +
                    f"map zone id '{current}' isn't valid --> " +
                    "discounts time space should be greater or equal to 0" +
                    COLOR_RESET_ALL
                )
                text_handling.exit_game()
            if (
                current_zone["discounts"]["chance"] < 0 or
                current_zone["discounts"]["chance"] > 1
            ):
                print(
                    COLOR_RED + "ERROR: " + COLOR_STYLE_BRIGHT +
                    f"map zone id '{current}' isn't valid --> " +
                    "discounts chance should be greater or equal " +
                    "to 0, and over or equal to 1" +
                    COLOR_RESET_ALL
                )
                text_handling.exit_game()
            if (
                current_zone["discounts"]["discount"]["max dropoff"] <
                current_zone["discounts"]["discount"]["max dropoff"]
            ):
                print(
                    COLOR_RED + "ERROR: " + COLOR_STYLE_BRIGHT +
                    f"map zone id '{current}' isn't valid --> " +
                    "discounts max dropoff should be greater or " +
                    "equal to the min dropoff" +
                    COLOR_RESET_ALL
                )
                text_handling.exit_game()

        elif current_zone["type"] == "harbor":
            for travel_id in list(current_zone["travels"]):
                travel = current_zone["travels"][travel_id]
                if "destination" not in travel:
                    print(
                        COLOR_RED + "ERROR: " + COLOR_STYLE_BRIGHT +
                        f"travel id '{travel_id}' in map zone id '{current}' isn't valid --> " +
                        "`destination` key isn't specified" +
                        COLOR_RESET_ALL
                    )
                    text_handling.exit_game()
                if "travel time" not in travel:
                    print(
                        COLOR_RED + "ERROR: " + COLOR_STYLE_BRIGHT +
                        f"travel id '{travel_id}' in map zone id '{current}' isn't valid --> " +
                        "`travel time` key isn't specified" +
                        COLOR_RESET_ALL
                    )
                    text_handling.exit_game()
                if "cost" not in travel:
                    print(
                        COLOR_RED + "ERROR: " + COLOR_STYLE_BRIGHT +
                        f"travel id '{travel_id}' in map zone id '{current}' isn't valid --> " +
                        "`cost` key isn't specified" +
                        COLOR_RESET_ALL
                    )
                    text_handling.exit_game()

                if type(travel["destination"]) is not type(1):
                    print(
                        COLOR_RED + "ERROR: " + COLOR_STYLE_BRIGHT +
                        f"travel id '{travel_id}' in map zone id '{current}' isn't valid --> " +
                        "key `destination` should be an integer" +
                        COLOR_RESET_ALL
                    )
                    text_handling.exit_game()
                if (
                    type(travel["travel time"]) is not type(1) and
                    type(travel["travel time"]) is not type(.1)
                ):
                    print(
                        COLOR_RED + "ERROR: " + COLOR_STYLE_BRIGHT +
                        f"travel id '{travel_id}' in map zone id '{current}' isn't valid --> " +
                        "key `travel time` should be an integer or a floating number" +
                        COLOR_RESET_ALL
                    )
                    text_handling.exit_game()
                if (
                    type(travel["cost"]) is not type(1) and
                    type(travel["cost"]) is not type(.1)
                ):
                    print(
                        COLOR_RED + "ERROR: " + COLOR_STYLE_BRIGHT +
                        f"travel id '{travel_id}' in map zone id '{current}' isn't valid --> " +
                        "key `cost` should be an integer or a floating number" +
                        COLOR_RESET_ALL
                    )
                    text_handling.exit_game()

                if f"point{travel['destination']}" not in list(map):
                    print(
                        COLOR_RED + "ERROR: " + COLOR_STYLE_BRIGHT +
                        f"travel id '{travel_id}' in map zone id '{current}' isn't valid --> " +
                        "destination points doesn't exist" +
                        COLOR_RESET_ALL
                    )
                    text_handling.exit_game()

            if current_zone["discounts"]["time space"] < 0:
                print(
                    COLOR_RED + "ERROR: " + COLOR_STYLE_BRIGHT +
                    f"map zone id '{current}' isn't valid --> " +
                    "discounts time space should be greater or equal to 0" +
                    COLOR_RESET_ALL
                )
                text_handling.exit_game()
            if (
                current_zone["discounts"]["chance"] < 0 or
                current_zone["discounts"]["chance"] > 1
            ):
                print(
                    COLOR_RED + "ERROR: " + COLOR_STYLE_BRIGHT +
                    f"map zone id '{current}' isn't valid --> " +
                    "discounts chance should be greater or equal " +
                    "to 0, and over or equal to 1" +
                    COLOR_RESET_ALL
                )
                text_handling.exit_game()
            if (
                current_zone["discounts"]["discount"]["max dropoff"] <
                current_zone["discounts"]["discount"]["max dropoff"]
            ):
                print(
                    COLOR_RED + "ERROR: " + COLOR_STYLE_BRIGHT +
                    f"map zone id '{current}' isn't valid --> " +
                    "discounts max dropoff should be greater or " +
                    "equal to the min dropoff" +
                    COLOR_RESET_ALL
                )
                text_handling.exit_game()

        elif current_zone["type"] == "dungeon":
            dungeon = current_zone["dungeon"]
            if dungeon["rooms number"] > len(list(dungeon["rooms"])):
                print(
                    COLOR_RED + "ERROR: " + COLOR_STYLE_BRIGHT +
                    f"map zone id '{current}' isn't valid --> " +
                    "the specified amount of rooms number is over" +
                    " the length of the defined rooms" +
                    COLOR_RESET_ALL
                )
                text_handling.exit_game()
            if dungeon["rooms number"] < len(list(dungeon["rooms"])):
                print(
                    COLOR_RED + "ERROR: " + COLOR_STYLE_BRIGHT +
                    f"map zone id '{current}' isn't valid --> " +
                    "too many rooms are defined in the rooms dictionary" +
                    COLOR_RESET_ALL
                )
                text_handling.exit_game()

            if dungeon["reward dialog"] not in list(dialog):
                print(
                    COLOR_RED + "ERROR: " + COLOR_STYLE_BRIGHT +
                    f"map zone id '{current}' isn't valid --> " +
                    f"dialog `{dungeon['reward dialog']}` in reward " +
                    "dialog doesn't exist" +
                    COLOR_RESET_ALL
                )
                text_handling.exit_game()

            for room_id in list(dungeon["rooms"]):
                room = dungeon["rooms"][room_id]

                if "room type" not in room:
                    print(
                        COLOR_RED + "ERROR: " + COLOR_STYLE_BRIGHT +
                        f"room id '{room_id}' in map zone id '{current}' isn't valid --> " +
                        "key `room type` isn't specified" +
                        COLOR_RESET_ALL
                    )
                    text_handling.exit_game()
                if "room digit" not in room:
                    print(
                        COLOR_RED + "ERROR: " + COLOR_STYLE_BRIGHT +
                        f"room id '{room_id}' in map zone id '{current}' isn't valid --> " +
                        "key `room digit` isn't specified" +
                        COLOR_RESET_ALL
                    )
                    text_handling.exit_game()

                if type(room["room type"]) is not type(""):
                    print(
                        COLOR_RED + "ERROR: " + COLOR_STYLE_BRIGHT +
                        f"room id '{room_id}' in map zone id '{current}' isn't valid --> " +
                        "key `room type` should be a string" +
                        COLOR_RESET_ALL
                    )
                    text_handling.exit_game()
                if type(room["room digit"]) is not type(1):
                    print(
                        COLOR_RED + "ERROR: " + COLOR_STYLE_BRIGHT +
                        f"room id '{room_id}' in map zone id '{current}' isn't valid --> " +
                        "key `room digit` should be an integer" +
                        COLOR_RESET_ALL
                    )
                    text_handling.exit_game()

                if room["room type"] not in ["fight", "boss-fight", "enigma"]:
                    print(
                        COLOR_RED + "ERROR: " + COLOR_STYLE_BRIGHT +
                        f"room id '{room_id}' in map zone id '{current}' isn't valid --> " +
                        "key `room type` doesn't specify a valid room type" +
                        COLOR_RESET_ALL
                    )
                    text_handling.exit_game()

                if room["room digit"] < 1 or room["room digit"] > dungeon["rooms number"]:
                    print(
                        COLOR_RED + "ERROR: " + COLOR_STYLE_BRIGHT +
                        f"room id '{room_id}' in map zone id '{current}' isn't valid --> " +
                        "key `room digit` should be in greater or equal to 1 " +
                        "and lower than the dungeon rooms number" +
                        COLOR_RESET_ALL
                    )
                    text_handling.exit_game()

                for i in dungeon["rooms"]:
                    ii = dungeon["rooms"][i]
                    if i != room_id and ii["room digit"] == room["room digit"]:
                        print(
                            COLOR_RED + "ERROR: " + COLOR_STYLE_BRIGHT +
                            f"room id '{room_id}' in map zone id '{current}' isn't valid --> " +
                            "room digit is duplicated with an other room" +
                            COLOR_RESET_ALL
                        )
                        text_handling.exit_game()

                if room["room type"] in ["fight", "boss-fight"]:
                    if "room fight data" not in room:
                        print(
                            COLOR_RED + "ERROR: " + COLOR_STYLE_BRIGHT +
                            f"room id '{room_id}' in map zone id '{current}' isn't valid --> " +
                            "dictionary `room fight data` can't be found" +
                            COLOR_RESET_ALL
                        )
                        text_handling.exit_game()

                    if "enemy list spawn" not in room["room fight data"]:
                        print(
                            COLOR_RED + "ERROR: " + COLOR_STYLE_BRIGHT +
                            f"room id '{room_id}' in map zone id '{current}' isn't valid --> " +
                            "key `enemy list spawn` in `room fight data` dictionary can't be found" +
                            COLOR_RESET_ALL
                        )
                        text_handling.exit_game()
                    if "no run away" not in room["room fight data"]:
                        print(
                            COLOR_RED + "ERROR: " + COLOR_STYLE_BRIGHT +
                            f"room id '{room_id}' in map zone id '{current}' isn't valid --> " +
                            "key `no run away` in `room fight data` dictionary can't be found" +
                            COLOR_RESET_ALL
                        )
                        text_handling.exit_game()

                    if type(room["room fight data"]["enemy list spawn"]) is not type(""):
                        print(
                            COLOR_RED + "ERROR: " + COLOR_STYLE_BRIGHT +
                            f"room id '{room_id}' in map zone id '{current}' isn't valid --> " +
                            "key `enemy list spawn` in `room fight data` dictionary should be a string" +
                            COLOR_RESET_ALL
                        )
                        text_handling.exit_game()
                    if type(room["room fight data"]["no run away"]) is not type(True):
                        print(
                            COLOR_RED + "ERROR: " + COLOR_STYLE_BRIGHT +
                            f"room id '{room_id}' in map zone id '{current}' isn't valid --> " +
                            "key `no run away` in `room fight data` dictionary should be a boolean" +
                            COLOR_RESET_ALL
                        )
                        text_handling.exit_game()
                    if (
                        "item reward" in room["room fight data"] and
                        type(room["room fight data"]["item reward"]) is not type([])
                    ):
                        print(
                            COLOR_RED + "ERROR: " + COLOR_STYLE_BRIGHT +
                            f"room id '{room_id}' in map zone id '{current}' isn't valid --> " +
                            "key `item reward` in `room fight data` dictionary should be a list" +
                            COLOR_RESET_ALL
                        )
                        text_handling.exit_game()
                    if (
                        "gold reward" in room["room fight data"] and
                        type(room["room fight data"]["gold reward"]) is not type(1) and
                        type(room["room fight data"]["gold reward"]) is not type(.1)
                    ):
                        print(
                            COLOR_RED + "ERROR: " + COLOR_STYLE_BRIGHT +
                            f"room id '{room_id}' in map zone id '{current}' isn't valid --> " +
                            "key `gold reward` in `room fight data` dictionary " +
                            "should be an integer or a floating number" +
                            COLOR_RESET_ALL
                        )
                        text_handling.exit_game()

                    if room["room fight data"]["enemy list spawn"] not in list(lists):
                        print(
                            COLOR_RED + "ERROR: " + COLOR_STYLE_BRIGHT +
                            f"room id '{room_id}' in map zone id '{current}' isn't valid --> " +
                            "key `enemy list spawn` doesn't specify an existing enemy list" +
                            COLOR_RESET_ALL
                        )
                        text_handling.exit_game()

                    if "item reward" in room["room fight data"]:
                        for i in room["room fight data"]["item reward"]:
                            if i not in list(item):
                                print(
                                    COLOR_RED + "ERROR: " + COLOR_STYLE_BRIGHT +
                                    f"room id '{room_id}' in map zone id '{current}' isn't valid --> " +
                                    f"item '{i}' in `item reward` list doesn't exist" +
                                    COLOR_RESET_ALL
                                )
                                text_handling.exit_game()

                else:
                    if "room enigma data" not in room:
                        print(
                            COLOR_RED + "ERROR: " + COLOR_STYLE_BRIGHT +
                            f"room id '{room_id}' in map zone id '{current}' isn't valid --> " +
                            "dictionary `room enigma data` can't be found" +
                            COLOR_RESET_ALL
                        )
                        text_handling.exit_game()

                    if "script name" not in room["room enigma data"]:
                        print(
                            COLOR_RED + "ERROR: " + COLOR_STYLE_BRIGHT +
                            f"room id '{room_id}' in map zone id '{current}' isn't valid --> " +
                            "key `script name` in `room enigma data` dictionary can't be found" +
                            COLOR_RESET_ALL
                        )
                        text_handling.exit_game()

                    if type(room["room enigma data"]["script name"]) is not type(""):
                        print(
                            COLOR_RED + "ERROR: " + COLOR_STYLE_BRIGHT +
                            f"room id '{room_id}' in map zone id '{current}' isn't valid --> " +
                            "key `script name` in `room enigma data` dictionary should be a string" +
                            COLOR_RESET_ALL
                        )
                        text_handling.exit_game()
                    if (
                        "arguments" in room["room enigma data"] and
                        type(room["room enigma data"]["arguments"]) is not type([])
                    ):
                        print(
                            COLOR_RED + "ERROR: " + COLOR_STYLE_BRIGHT +
                            f"room id '{room_id}' in map zone id '{current}' isn't valid --> " +
                            "key `arguments` in `room enigma data` dictionary should be a list" +
                            COLOR_RESET_ALL
                        )
                        text_handling.exit_game()

                    if "arguments" in room["room enigma data"]:
                        possible_arguments = [
                            "player", "map", "item", "drinks", "enemy", "npcs",
                            "start_player", "lists", "zone", "dialog", "mission",
                            "mounts", "start_time", "generic_text_replacements",
                            "preferences"
                        ]
                        for argument in room["room enigma data"]["arguments"]:
                            if argument not in possible_arguments:
                                print(
                                    COLOR_RED + "ERROR: " + COLOR_STYLE_BRIGHT +
                                    f"room id '{room_id}' in map zone id '{current}' isn't valid --> " +
                                    f"argument `{argument}` in arguments key " +
                                    "is not a valid one" +
                                    COLOR_RESET_ALL
                                )
                                text_handling.exit_game()

    # Specific checks for the `dialog` dictionary
    # CHECKS:
    # - checks on `to display` dictionary:
    #   * check if every key is the right type
    #   * check if locations exist
    #   * check if enemies exist
    #   * check if npcs exist
    # - check if the `actions` dictionary is unneeded
    # - check if the `actions` dictionary isn't specified
    # - check if everything in the `actions` dictionary is of a correct type
    for current_id in list(dialog):
        current = dialog[current_id]

        if "to display" in current:
            for key in [
                "player attributes", "visited locations",
                "known enemies", "known npcs", "has items",
                "has missions active", "has missions offered"
            ]:
                if (
                    key in current["to display"] and
                    type(current["to display"][key]) is not type([])
                ):
                    print(
                        COLOR_RED + "ERROR: " + COLOR_STYLE_BRIGHT +
                        f"dialog id '{current_id}' isn't valid --> " +
                        f"key `{key}` in to `display` dictionary should be a list" +
                        COLOR_RESET_ALL
                    )
                    text_handling.exit_game()

            if "visited locations" in current["to display"]:
                for i in current["to display"]["visited locations"]:
                    if f"point{i}" not in list(map):
                        print(
                            COLOR_RED + "ERROR: " + COLOR_STYLE_BRIGHT +
                            f"dialog id '{current_id}' isn't valid --> " +
                            f"map point '{i}' in `visited locations` key " +
                            "in `to display` dictionary doesn't exist" +
                            COLOR_RESET_ALL
                        )
                        text_handling.exit_game()
            if "known enemies" in current["to display"]:
                for i in current["to display"]["known enemies"]:
                    if i not in list(enemy):
                        print(
                            COLOR_RED + "ERROR: " + COLOR_STYLE_BRIGHT +
                            f"dialog id '{current_id}' isn't valid --> " +
                            f"enemy '{i}' in `known enemies` key " +
                            "in `to display` dictionary doesn't exist" +
                            COLOR_RESET_ALL
                        )
                        text_handling.exit_game()
            if "known npcs" in current["to display"]:
                for i in current["to display"]["known npcs"]:
                    if i not in list(npcs):
                        print(
                            COLOR_RED + "ERROR: " + COLOR_STYLE_BRIGHT +
                            f"dialog id '{current_id}' isn't valid --> " +
                            f"npc '{i}' in `known npcs` key " +
                            "in `to display` dictionary doesn't exist" +
                            COLOR_RESET_ALL
                        )
                        text_handling.exit_game()
            if "has items" in current["to display"]:
                for i in current["to display"]["has items"]:
                    if i not in list(item):
                        print(
                            COLOR_RED + "ERROR: " + COLOR_STYLE_BRIGHT +
                            f"dialog id '{current_id}' isn't valid --> " +
                            f"item '{i}' in `has items` key " +
                            "in `to display` dictionary doesn't exist" +
                            COLOR_RESET_ALL
                        )
                        exit_game()
            if "has missions active" in current["to display"]:
                for i in current["to display"]["has missions active"]:
                    if i not in list(mission):
                        print(
                            COLOR_RED + "ERROR: " + COLOR_STYLE_BRIGHT +
                            f"dialog id '{current_id}' isn't valid --> " +
                            f"mission '{i}' in `has missions active` key " +
                            "in `to display` dictionary doesn't exist" +
                            COLOR_RESET_ALL
                        )
                        exit_game()
            if "has missions offered" in current["to display"]:
                for i in current["to display"]["has missions offered"]:
                    if i not in list(mission):
                        print(
                            COLOR_RED + "ERROR: " + COLOR_STYLE_BRIGHT +
                            f"dialog id '{current_id}' isn't valid --> " +
                            f"mission '{i}' in `has missions offered` key " +
                            "in `to display` dictionary doesn't exist" +
                            COLOR_RESET_ALL
                        )
                        exit_game()
            if (
                "random" in current["to display"] and
                type(current["to display"]["random"]) is not type(.1) and
                type(current["to display"]["random"]) is not type(1)
            ):
                print(
                    COLOR_RED + "ERROR: " + COLOR_STYLE_BRIGHT +
                    f"dialog id '{current_id}' isn't valid --> " +
                    f"key `random` in to `display` dictionary should be a floating number or an integer" +
                    COLOR_RESET_ALL
                )
                exit_game()

        if current["use actions"] and "actions" not in current:
            print(
                COLOR_RED + "ERROR: " + COLOR_STYLE_BRIGHT +
                f"dialog id '{current_id}' isn't valid --> " +
                "key `use actions` is set to True but the `actions`" +
                " dictionary isn't defined" +
                COLOR_RESET_ALL
            )
            text_handling.exit_game()
        if not current["use actions"] and "actions" in current:
            print(
                COLOR_RED + "ERROR: " + COLOR_STYLE_BRIGHT +
                f"dialog id '{current_id}' isn't valid --> " +
                "key `use actions` is set to False but the `actions`" +
                " dictionary is still defined" +
                COLOR_RESET_ALL
            )
            text_handling.exit_game()

        if "actions" in current:
            if (
                "add attributes" in current["actions"] and
                type(current["actions"]["add attributes"]) is not type([])
            ):
                print(
                    COLOR_RED + "ERROR: " + COLOR_STYLE_BRIGHT +
                    f"dialog id '{current_id}' isn't valid --> " +
                    "key `add attributes` in `actions` dictionary should be a list" +
                    COLOR_RESET_ALL
                )
                text_handling.exit_game()

            if "give item" in current["actions"]:
                if type(current["actions"]["give item"]) is not type([]):
                    print(
                        COLOR_RED + "ERROR: " + COLOR_STYLE_BRIGHT +
                        f"dialog id '{current_id}' isn't valid --> " +
                        "key `give item` in `actions` dictionary should be a list" +
                        COLOR_RESET_ALL
                    )
                    text_handling.exit_game()
                for i in current["actions"]["give item"]:
                    if i not in list(item) and (
                        not i.startswith("$")
                    ):
                        print(
                            COLOR_RED + "ERROR: " + COLOR_STYLE_BRIGHT +
                            f"dialog id '{current_id}' isn't valid --> " +
                            f"item '{i}' in `give item` list in `actions` " +
                            "dictionary doesn't exist" +
                            COLOR_RESET_ALL
                        )
                        text_handling.exit_game()
            if "remove item" in current["actions"]:
                if type(current["actions"]["remove item"]) is not type([]):
                    print(
                        COLOR_RED + "ERROR: " + COLOR_STYLE_BRIGHT +
                        f"dialog id '{current_id}' isn't valid --> " +
                        "key `remove item` in `actions` dictionary should be a list" +
                        COLOR_RESET_ALL
                    )
                    text_handling.exit_game()
                for i in current["actions"]["remove item"]:
                    if i not in list(item) and (
                        not i.startswith("$")
                    ):
                        print(
                            COLOR_RED + "ERROR: " + COLOR_STYLE_BRIGHT +
                            f"dialog id '{current_id}' isn't valid --> " +
                            f"item '{i}' in `remove item` list in `actions` " +
                            "dictionary doesn't exist" +
                            COLOR_RESET_ALL
                        )
                        text_handling.exit_game()
            if "use drink" in current["actions"]:
                if type(current["actions"]["use drink"]) is not type([]):
                    print(
                        COLOR_RED + "ERROR: " + COLOR_STYLE_BRIGHT +
                        f"dialog id '{current_id}' isn't valid --> " +
                        "key `use drink` in `actions` dictionary should be a list" +
                        COLOR_RESET_ALL
                    )
                    text_handling.exit_game()
                for i in current["actions"]["use drink"]:
                    if i not in list(drinks) and (
                        not i.startswith("$")
                    ):
                        print(
                            COLOR_RED + "ERROR: " + COLOR_STYLE_BRIGHT +
                            f"dialog id '{current_id}' isn't valid --> " +
                            f"item '{i}' in `use drink` list in `actions` " +
                            "dictionary doesn't exist" +
                            COLOR_RESET_ALL
                        )
                        text_handling.exit_game()

            if "health modification" in current["actions"]:
                if (
                    "diminution" in current["actions"]["health modification"] and
                    type(current["actions"]["health modification"]["diminution"]) is not type(1) and
                    not str(current["actions"]["health modification"]["diminution"]).startswith("$")
                ):
                    print(
                        COLOR_RED + "ERROR: " + COLOR_STYLE_BRIGHT +
                        f"dialog id '{current_id}' isn't valid --> " +
                        "key `diminution` in `health modification` " +
                        "in `actions` dictionary should be an integer" +
                        " or a variable created in the conversation" +
                        COLOR_RESET_ALL
                    )
                    text_handling.exit_game()
                if (
                    "augmentation" in current["actions"]["health modification"] and
                    type(current["actions"]["health modification"]["augmentation"]) is not type(1) and
                    not str(current["actions"]["health modification"]["augmentation"]).startswith("$")
                ):
                    print(
                        COLOR_RED + "ERROR: " + COLOR_STYLE_BRIGHT +
                        f"dialog id '{current_id}' isn't valid --> " +
                        "key `augmentation` in `health modification` " +
                        "in `actions` dictionary should be an integer" +
                        " or a variable created in the conversation" +
                        COLOR_RESET_ALL
                    )
                    text_handling.exit_game()
                if "max health" in current["actions"]["health modification"]:
                    if (
                        "diminution" in current["actions"]["health modification"]["max health"] and
                        type(current["actions"]["health modification"]["max health"]["diminution"]) is not type(1) and
                        not str(current["actions"]["health modification"]["max health"]["diminution"]).startswith("$")
                    ):
                        print(
                            COLOR_RED + "ERROR: " + COLOR_STYLE_BRIGHT +
                            f"dialog id '{current_id}' isn't valid --> " +
                            "key `diminution` in `max health` in `health modification` " +
                            "in `actions` dictionary should be an integer" +
                            " or a variable created in the conversation" +
                            COLOR_RESET_ALL
                        )
                        text_handling.exit_game()
                    if (
                        "augmentation" in current["actions"]["health modification"]["max health"] and
                        type(current["actions"]["health modification"]["max health"]["augmentation"]) is not type(1) and
                        not str(current["actions"]["health modification"]["max health"]["augmentation"]).startswith("$")
                    ):
                        print(
                            COLOR_RED + "ERROR: " + COLOR_STYLE_BRIGHT +
                            f"dialog id '{current_id}' isn't valid --> " +
                            "key `augmentation` in `max health` in `health modification` " +
                            "in `actions` dictionary should be an integer" +
                            " or a variable created in the conversation" +
                            COLOR_RESET_ALL
                        )
                        text_handling.exit_game()

            if "gold modification" in current["actions"]:
                if (
                    "diminution" in current["actions"]["gold modification"] and
                    type(current["actions"]["gold modification"]["diminution"]) is not type(1) and
                    type(current["actions"]["gold modification"]["diminution"]) is not type(.1) and
                    not str(current["actions"]["gold modification"]["diminution"]).startswith("$")
                ):
                    print(
                        COLOR_RED + "ERROR: " + COLOR_STYLE_BRIGHT +
                        f"dialog id '{current_id}' isn't valid --> " +
                        "key `diminution` in `gold modification` " +
                        "in `actions` dictionary should be an integer or a floating number" +
                        " or a variable created in the conversation" +
                        COLOR_RESET_ALL
                    )
                    text_handling.exit_game()
                if (
                    "augmentation" in current["actions"]["gold modification"] and
                    type(current["actions"]["gold modification"]["augmentation"]) is not type(1) and
                    type(current["actions"]["gold modification"]["augmentation"]) is not type(.1) and
                    not str(current["actions"]["gold modification"]["augmentation"]).startswith("$")
                ):
                    print(
                        COLOR_RED + "ERROR: " + COLOR_STYLE_BRIGHT +
                        f"dialog id '{current_id}' isn't valid --> " +
                        "key `augmentation` in `gold modification` " +
                        "in `actions` dictionary should be an integer or a floating number" +
                        " or a variable created in the conversation" +
                        COLOR_RESET_ALL
                    )
                    text_handling.exit_game()

            if "add to diary" in current["actions"]:
                if "known zones" in current["actions"]["add to diary"]:
                    if type(current["actions"]["add to diary"]["known zones"]) is not type([]):
                        print(
                            COLOR_RED + "ERROR: " + COLOR_STYLE_BRIGHT +
                            f"dialog id '{current_id}' isn't valid --> " +
                            "key `known zones` in `add to diary` " +
                            "in `actions` dictionary should be a list" +
                            COLOR_RESET_ALL
                        )
                        text_handling.exit_game()
                    for i in current["actions"]["add to diary"]["known zones"]:
                        if i not in list(zone) and (
                            not i.startswith("$")
                        ):
                            print(
                                COLOR_RED + "ERROR: " + COLOR_STYLE_BRIGHT +
                                f"dialog id '{current_id}' isn't valid --> " +
                                f"zone '{i}' in key `known zones` in `add to diary` " +
                                "in `actions` dictionary doesn't exist" +
                                COLOR_RESET_ALL
                            )
                            text_handling.exit_game()
                if "known enemies" in current["actions"]["add to diary"]:
                    if type(current["actions"]["add to diary"]["known enemies"]) is not type([]):
                        print(
                            COLOR_RED + "ERROR: " + COLOR_STYLE_BRIGHT +
                            f"dialog id '{current_id}' isn't valid --> " +
                            "key `known enemies` in `add to diary` " +
                            "in `actions` dictionary should be a list" +
                            COLOR_RESET_ALL
                        )
                        text_handling.exit_game()
                    for i in current["actions"]["add to diary"]["known enemies"]:
                        if i not in list(enemy) and (
                            not i.startswith("$")
                        ):
                            print(
                                COLOR_RED + "ERROR: " + COLOR_STYLE_BRIGHT +
                                f"dialog id '{current_id}' isn't valid --> " +
                                f"enemy '{i}' in key `known enemies` in `add to diary` " +
                                "in `actions` dictionary doesn't exist" +
                                COLOR_RESET_ALL
                            )
                            text_handling.exit_game()
                if "known npcs" in current["actions"]["add to diary"]:
                    if type(current["actions"]["add to diary"]["known npcs"]) is not type([]):
                        print(
                            COLOR_RED + "ERROR: " + COLOR_STYLE_BRIGHT +
                            f"dialog id '{current_id}' isn't valid --> " +
                            "key `known npcs `in `add to diary` " +
                            "in `actions` dictionary should be a list" +
                            COLOR_RESET_ALL
                        )
                        text_handling.exit_game()
                    for i in current["actions"]["add to diary"]["known npcs"]:
                        if i not in list(npcs) and (
                            not i.startswith("$")
                        ):
                            print(
                                COLOR_RED + "ERROR: " + COLOR_STYLE_BRIGHT +
                                f"dialog id '{current_id}' isn't valid --> " +
                                f"npc '{i}' in key `known npcs` in `add to diary` " +
                                "in `actions` dictionary doesn't exist" +
                                COLOR_RESET_ALL
                            )
                            text_handling.exit_game()
            if "remove to diary" in current["actions"]:
                if "known zones" in current["actions"]["remove to diary"]:
                    if type(current["actions"]["remove to diary"]["known zones"]) is not type([]):
                        print(
                            COLOR_RED + "ERROR: " + COLOR_STYLE_BRIGHT +
                            f"dialog id '{current_id}' isn't valid --> " +
                            "key `known zones` in `remove to diary` " +
                            "in `actions` dictionary should be a list" +
                            COLOR_RESET_ALL
                        )
                        text_handling.exit_game()
                    for i in current["actions"]["remove to diary"]["known zones"]:
                        if i not in list(zone) and (
                            not i.startswith("$")
                        ):
                            print(
                                COLOR_RED + "ERROR: " + COLOR_STYLE_BRIGHT +
                                f"dialog id '{current_id}' isn't valid --> " +
                                f"zone '{i}' in key `known zones` in `remove to diary` " +
                                "in `actions` dictionary doesn't exist" +
                                COLOR_RESET_ALL
                            )
                            text_handling.exit_game()
                if "known enemies" in current["actions"]["remove to diary"]:
                    if type(current["actions"]["remove to diary"]["known enemies"]) is not type([]):
                        print(
                            COLOR_RED + "ERROR: " + COLOR_STYLE_BRIGHT +
                            f"dialog id '{current_id}' isn't valid --> " +
                            "key `known enemies` in `remove to diary` " +
                            "in `actions` dictionary should be a list" +
                            COLOR_RESET_ALL
                        )
                        text_handling.exit_game()
                    for i in current["actions"]["remove to diary"]["known enemies"]:
                        if i not in list(enemy) and (
                            not i.startswith("$")
                        ):
                            print(
                                COLOR_RED + "ERROR: " + COLOR_STYLE_BRIGHT +
                                f"dialog id '{current_id}' isn't valid --> " +
                                f"enemy '{i}' in key `known enemies` in `remove to diary` " +
                                "in `actions` dictionary doesn't exist" +
                                COLOR_RESET_ALL
                            )
                            text_handling.exit_game()
                if "known npcs" in current["actions"]["remove to diary"]:
                    if type(current["actions"]["remove to diary"]["known npcs"]) is not type([]):
                        print(
                            COLOR_RED + "ERROR: " + COLOR_STYLE_BRIGHT +
                            f"dialog id '{current_id}' isn't valid --> " +
                            "key `known npcs `in `remove to diary` " +
                            "in `actions` dictionary should be a list" +
                            COLOR_RESET_ALL
                        )
                        text_handling.exit_game()
                    for i in current["actions"]["remove to diary"]["known npcs"]:
                        if i not in list(npcs) and (
                            not i.startswith("$")
                        ):
                            print(
                                COLOR_RED + "ERROR: " + COLOR_STYLE_BRIGHT +
                                f"dialog id '{current_id}' isn't valid --> " +
                                f"npc '{i}' in key `known npcs` in `remove to diary` " +
                                "in `actions` dictionary doesn't exist" +
                                COLOR_RESET_ALL
                            )
                            text_handling.exit_game()
                # scripts tests TODO (for later maybe)

    # Specific checks of `mission` dictionary
    # CHECKS:
    # - check if source, destination and stopovers exist
    # - checks on conditions:
    #   * check if every keys is the right type
    #   * check if the visited locations exist
    #   * check if the known enemies exist
    #   * check if the known npcs exist
    #   * check if the known zones exist
    #   * check if the required items exist
    #   * check if random i in between 0 and 1
    # - checks on triggers:
    #   * check if every key is the right type
    #   * check if the dialog exists
    # - checks on mission enemies:
    #   * check if every keys are there
    #   * check if every keys are the right type
    #   * check if the spanwed enemy list exist
    #   * check if the enemy's location exist
    #   * check if the death dialog exists
    #   * check for the spawning conditions:
    #      > check if every key is the right type
    #      > check if random is in between 0 and 1
    for current_id in list(mission):
        current = mission[current_id]

        if f"point{current['source']}" not in list(map):
            print(
                COLOR_RED + "ERROR: " + COLOR_STYLE_BRIGHT +
                f"mission id '{current_id}' isn't valid --> " +
                f"map point 'point{current['source']}' in `source`" +
                " key doesn't exist" +
                COLOR_RESET_ALL
            )
            text_handling.exit_game()
        if f"point{current['destination']}" not in list(map):
            print(
                COLOR_RED + "ERROR: " + COLOR_STYLE_BRIGHT +
                f"mission id '{current_id}' isn't valid --> " +
                f"map point 'point{current['destination']}' in `destination`" +
                " key doesn't exist" +
                COLOR_RESET_ALL
            )
            text_handling.exit_game()
        if "stopovers" in current:
            for stopover in current["stopovers"]:
                if f"point{stopover}" not in list(map):
                    print(
                        COLOR_RED + "ERROR: " + COLOR_STYLE_BRIGHT +
                        f"mission id '{current_id}' isn't valid --> " +
                        f"map point 'point{stopover}' in `stopovers`" +
                        " key doesn't exist" +
                        COLOR_RESET_ALL
                    )
                    text_handling.exit_game()

        for condition in ["to offer", "to complete", "to fail"]:
            if condition in current:
                if "player attributes" in current[condition]:
                    if type(current[condition]["player attributes"]) is not type([]):
                        print(
                            COLOR_RED + "ERROR: " + COLOR_STYLE_BRIGHT +
                            f"mission id '{current_id}' isn't valid --> " +
                            f"key `player attributes` in `{condition}`" +
                            " should be a list" +
                            COLOR_RESET_ALL
                        )
                        text_handling.exit_game()
                if "visited locations" in current[condition]:
                    if type(current[condition]["visited locations"]) is not type([]):
                        print(
                            COLOR_RED + "ERROR: " + COLOR_STYLE_BRIGHT +
                            f"mission id '{current_id}' isn't valid --> " +
                            f"key `visited locations` in `{condition}`" +
                            " should be a list" +
                            COLOR_RESET_ALL
                        )
                        text_handling.exit_game()
                    for location in current[condition]["visited locations"]:
                        if f"point{location}" not in list(map):
                            print(
                                COLOR_RED + "ERROR: " + COLOR_STYLE_BRIGHT +
                                f"mission id '{current_id}' isn't valid --> " +
                                f"map point 'point{location}' in `visited locations`" +
                                f" in `{condition}` doesn't exist" +
                                COLOR_RESET_ALL
                            )
                            text_handling.exit_game()
                if "known enemies" in current[condition]:
                    if type(current[condition]["known enemies"]) is not type([]):
                        print(
                            COLOR_RED + "ERROR: " + COLOR_STYLE_BRIGHT +
                            f"mission id '{current_id}' isn't valid --> " +
                            f"key `known enemies` in `{condition}`" +
                            " should be a list" +
                            COLOR_RESET_ALL
                        )
                        text_handling.exit_game()
                    for i in current[condition]["known enemies"]:
                        if i not in list(enemy):
                            print(
                                COLOR_RED + "ERROR: " + COLOR_STYLE_BRIGHT +
                                f"mission id '{current_id}' isn't valid --> " +
                                f"enemy '{i}' in `known enemies`" +
                                f" in `{condition}` doesn't exist" +
                                COLOR_RESET_ALL
                            )
                            text_handling.exit_game()
                if "known zones" in current[condition]:
                    if type(current[condition]["known zones"]) is not type([]):
                        print(
                            COLOR_RED + "ERROR: " + COLOR_STYLE_BRIGHT +
                            f"mission id '{current_id}' isn't valid --> " +
                            f"key `known zones` in `{condition}`" +
                            " should be a list" +
                            COLOR_RESET_ALL
                        )
                        text_handling.exit_game()
                    for i in current[condition]["known zones"]:
                        if i not in list(zone):
                            print(
                                COLOR_RED + "ERROR: " + COLOR_STYLE_BRIGHT +
                                f"mission id '{current_id}' isn't valid --> " +
                                f"zone '{i}' in `known zones`" +
                                f" in `{condition}` doesn't exist" +
                                COLOR_RESET_ALL
                            )
                            text_handling.exit_game()
                if "known npcs" in current[condition]:
                    if type(current[condition]["known npcs"]) is not type([]):
                        print(
                            COLOR_RED + "ERROR: " + COLOR_STYLE_BRIGHT +
                            f"mission id '{current_id}' isn't valid --> " +
                            f"key `known npcs` in `{condition}`" +
                            " should be a list" +
                            COLOR_RESET_ALL
                        )
                        text_handling.exit_game()
                    for i in current[condition]["known npcs"]:
                        if i not in list(npcs):
                            print(
                                COLOR_RED + "ERROR: " + COLOR_STYLE_BRIGHT +
                                f"mission id '{current_id}' isn't valid --> " +
                                f"npc '{i}' in `known npcs`" +
                                f" in `{condition}` doesn't exist" +
                                COLOR_RESET_ALL
                            )
                            text_handling.exit_game()
                if "has missions active" in current[condition]:
                    if type(current[condition]["has missions active"]) is not type([]):
                        print(
                            COLOR_RED + "ERROR: " + COLOR_STYLE_BRIGHT +
                            f"mission id '{current_id}' isn't valid --> " +
                            f"key `has missions active` in `{condition}`" +
                            " should be a list" +
                            COLOR_RESET_ALL
                        )
                        exit_game()
                    for i in current[condition]["has missions active"]:
                        if i not in list(mission):
                            print(
                                COLOR_RED + "ERROR: " + COLOR_STYLE_BRIGHT +
                                f"mission id '{current_id}' isn't valid --> " +
                                f"mission '{i}' in `has missions active`" +
                                f" in `{condition}` doesn't exist" +
                                COLOR_RESET_ALL
                            )
                            exit_game()
                if "has missions offered" in current[condition]:
                    if type(current[condition]["has missions offered"]) is not type([]):
                        print(
                            COLOR_RED + "ERROR: " + COLOR_STYLE_BRIGHT +
                            f"mission id '{current_id}' isn't valid --> " +
                            f"key `has missions offered` in `{condition}`" +
                            " should be a list" +
                            COLOR_RESET_ALL
                        )
                        exit_game()
                    for i in current[condition]["has missions offered"]:
                        if i not in list(mission):
                            print(
                                COLOR_RED + "ERROR: " + COLOR_STYLE_BRIGHT +
                                f"mission id '{current_id}' isn't valid --> " +
                                f"mission '{i}' in `has missions offered`" +
                                f" in `{condition}` doesn't exist" +
                                COLOR_RESET_ALL
                            )
                            exit_game()
                if "has items" in current[condition]:
                    if type(current[condition]["has items"]) is not type([]):
                        print(
                            COLOR_RED + "ERROR: " + COLOR_STYLE_BRIGHT +
                            f"mission id '{current_id}' isn't valid --> " +
                            f"key `has items` in `{condition}`" +
                            " should be a list" +
                            COLOR_RESET_ALL
                        )
                        text_handling.exit_game()
                    for i in current[condition]["has items"]:
                        if i not in list(item):
                            print(
                                COLOR_RED + "ERROR: " + COLOR_STYLE_BRIGHT +
                                f"mission id '{current_id}' isn't valid --> " +
                                f"item '{i}' in `has items`" +
                                f" in `{condition}` doesn't exist" +
                                COLOR_RESET_ALL
                            )
                            text_handling.exit_game()

                if "random" in current[condition]:
                    if (
                        current[condition]["random"] > 1 or
                        current[condition]["random"] < 0
                    ):
                        print(
                            COLOR_RED + "ERROR: " + COLOR_STYLE_BRIGHT +
                            f"mission id '{current_id}' isn't valid --> " +
                            f"key `random` in `{condition}`" +
                            " should be in between 0 and 1" +
                            COLOR_RESET_ALL
                        )
                        text_handling.exit_game()

        for trigger in ["on offer", "on complete", "on fail", "on abort", "on accept"]:
            if trigger in current:
                if "dialog" in current[trigger]:
                    if type(current[trigger]["dialog"]) is not type(""):
                        print(
                            COLOR_RED + "ERROR: " + COLOR_STYLE_BRIGHT +
                            f"mission id '{current_id}' isn't valid --> " +
                            f"key `dialog` in `{trigger}`" +
                            " should be a string" +
                            COLOR_RESET_ALL
                        )
                        text_handling.exit_game()
                    if current[trigger]["dialog"] not in list(dialog):
                        print(
                            COLOR_RED + "ERROR: " + COLOR_STYLE_BRIGHT +
                            f"mission id '{current_id}' isn't valid --> " +
                            f"dialog '{current[trigger]['dialog']}' in `dialog` " +
                            f"in `{trigger}` doesn't exist" +
                            COLOR_RESET_ALL
                        )
                        text_handling.exit_game()
                    if (
                        "payment" in current[trigger] and
                        type(current[trigger]["payment"]) is not type(1) and
                        type(current[trigger]["payment"]) is not type(.1)
                    ):
                        print(
                            COLOR_RED + "ERROR: " + COLOR_STYLE_BRIGHT +
                            f"mission id '{current_id}' isn't valid --> " +
                            f"key `payment` in `{trigger}`" +
                            " should be a floating number or an integer" +
                            COLOR_RESET_ALL
                        )
                        text_handling.exit_game()
                    if (
                        "fine" in current[trigger] and
                        type(current[trigger]["fine"]) is not type(1) and
                        type(current[trigger]["fine"]) is not type(.1)
                    ):
                        print(
                            COLOR_RED + "ERROR: " + COLOR_STYLE_BRIGHT +
                            f"mission id '{current_id}' isn't valid --> " +
                            f"key `fine` in `{trigger}`" +
                            " should be a floating number or an integer" +
                            COLOR_RESET_ALL
                        )
                        text_handling.exit_game()
                    if (
                        "exp addition" in current[trigger] and
                        type(current[trigger]["exp addition"]) is not type(1) and
                        type(current[trigger]["exp addition"]) is not type(.1)
                    ):
                        print(
                            COLOR_RED + "ERROR: " + COLOR_STYLE_BRIGHT +
                            f"mission id '{current_id}' isn't valid --> " +
                            f"key `exp addition` in `{trigger}`" +
                            " should be a floating number or an integer" +
                            COLOR_RESET_ALL
                        )
                        text_handling.exit_game()
                    if (
                        "add attributes" in current[trigger] and
                        type(current[trigger]["add attribute"]) is not type([])
                    ):
                        print(
                            COLOR_RED + "ERROR: " + COLOR_STYLE_BRIGHT +
                            f"mission id '{current_id}' isn't valid --> " +
                            f"key `add attribute` in `{trigger}`" +
                            " should be a list" +
                            COLOR_RESET_ALL
                        )
                        exit_game()
        if "enemies" in current:
            for i in current["enemies"]:
                current_enemy = current["enemies"][i]
                if "enemy category" not in current_enemy:
                    print(
                        COLOR_RED + "ERROR: " + COLOR_STYLE_BRIGHT +
                        f"enemy id '{i}' in mission id '{current_id}' isn't valid --> " +
                        f"key `enemy category` is missing" +
                        COLOR_RESET_ALL
                    )
                    text_handling.exit_game()
                if "location" not in current_enemy:
                    print(
                        COLOR_RED + "ERROR: " + COLOR_STYLE_BRIGHT +
                        f"enemy id '{i}' in mission id '{current_id}' isn't valid --> " +
                        f"key `location` is missing" +
                        COLOR_RESET_ALL
                    )
                    text_handling.exit_game()

                if type(current_enemy["enemy category"]) is not type(""):
                    print(
                        COLOR_RED + "ERROR: " + COLOR_STYLE_BRIGHT +
                        f"enemy id '{i}' in mission id '{current_id}' isn't valid --> " +
                        f"key `enemy category` should be a string" +
                        COLOR_RESET_ALL
                    )
                    text_handling.exit_game()
                if type(current_enemy["location"]) is not type(1):
                    print(
                        COLOR_RED + "ERROR: " + COLOR_STYLE_BRIGHT +
                        f"enemy id '{i}' in mission id '{current_id}' isn't valid --> " +
                        f"key `enemy category` should be an integer" +
                        COLOR_RESET_ALL
                    )
                    text_handling.exit_game()
                if "dialog" in current_enemy:
                    if type(current_enemy["dialog"]) is not type(""):
                        print(
                            COLOR_RED + "ERROR: " + COLOR_STYLE_BRIGHT +
                            f"enemy id '{i}' in mission id '{current_id}' isn't valid --> " +
                            f"key `dialog` should be a string" +
                            COLOR_RESET_ALL
                        )
                        text_handling.exit_game()

                if current_enemy["enemy category"] not in list(lists):
                    print(
                        COLOR_RED + "ERROR: " + COLOR_STYLE_BRIGHT +
                        f"enemy id '{i}' in mission id '{current_id}' isn't valid --> " +
                        f"enemy pool list '{current_enemy['enemy category']}' in key `enemy category`" +
                        "doesn't exist" +
                        COLOR_RESET_ALL
                    )
                    text_handling.exit_game()
                if f"point{current_enemy['location']}" not in list(map):
                    print(
                        COLOR_RED + "ERROR: " + COLOR_STYLE_BRIGHT +
                        f"enemy id '{i}' in mission id '{current_id}' isn't valid --> " +
                        f"map point 'point{current_enemy['location']}' in key `location`" +
                        "doesn't exist" +
                        COLOR_RESET_ALL
                    )
                    text_handling.exit_game()
                if "dialog" in current_enemy:
                    if current_enemy["dialog"] not in list(dialog):
                        print(
                            COLOR_RED + "ERROR: " + COLOR_STYLE_BRIGHT +
                            f"enemy id '{i}' in mission id '{current_id}' isn't valid --> " +
                            f"dialog '{current_enemy['dialog']}' in key `dialog`" +
                            "doesn't exist" +
                            COLOR_RESET_ALL
                        )
                        text_handling.exit_game()

                for condition in ["to spawn", "to despawn"]:
                    if condition in current_enemy:
                        if "player attributes" in current_enemy[condition]:
                            if type(current_enemy[condition]["player attributes"]) is not type([]):
                                print(
                                    COLOR_RED + "ERROR: " + COLOR_STYLE_BRIGHT +
                                    f"enemy id '{i}' mission id '{current_id}' isn't valid --> " +
                                    f"key `player attributes` in `{condition}`" +
                                    " should be a list" +
                                    COLOR_RESET_ALL
                                )
                                text_handling.exit_game()
                        if "visited locations" in current_enemy[condition]:
                            if type(current_enemy[condition]["visited locations"]) is not type([]):
                                print(
                                    COLOR_RED + "ERROR: " + COLOR_STYLE_BRIGHT +
                                    f"enemy id '{i}' mission id '{current_id}' isn't valid --> " +
                                    f"key `visited locations` in `{condition}`" +
                                    " should be a list" +
                                    COLOR_RESET_ALL
                                )
                                text_handling.exit_game()
                            for location in current_enemy[condition]["visited locations"]:
                                if f"point{location}" not in list(map):
                                    print(
                                        COLOR_RED + "ERROR: " + COLOR_STYLE_BRIGHT +
                                        f"enemy id '{i}' mission id '{current_id}' isn't valid --> " +
                                        f"map point 'point{location}' in `visited locations`" +
                                        f" in `{condition}` doesn't exist" +
                                        COLOR_RESET_ALL
                                    )
                                    text_handling.exit_game()
                        if "known enemies" in current_enemy[condition]:
                            if type(current_enemy[condition]["known enemies"]) is not type([]):
                                print(
                                    COLOR_RED + "ERROR: " + COLOR_STYLE_BRIGHT +
                                    f"enemy id '{i}' mission id '{current_id}' isn't valid --> " +
                                    f"key `known enemies` in `{condition}`" +
                                    " should be a list" +
                                    COLOR_RESET_ALL
                                )
                                text_handling.exit_game()
                            for i2 in current_enemy[condition]["known enemies"]:
                                if i2 not in list(enemy):
                                    print(
                                        COLOR_RED + "ERROR: " + COLOR_STYLE_BRIGHT +
                                        f"enemy id '{i}' mission id '{current_id}' isn't valid --> " +
                                        f"enemy '{i2}' in `known enemies`" +
                                        f" in `{condition}` doesn't exist" +
                                        COLOR_RESET_ALL
                                    )
                                    text_handling.exit_game()
                        if "known zones" in current_enemy[condition]:
                            if type(current_enemy[condition]["known zones"]) is not type([]):
                                print(
                                    COLOR_RED + "ERROR: " + COLOR_STYLE_BRIGHT +
                                    f"enemy id '{i}' mission id '{current_id}' isn't valid --> " +
                                    f"key `known zones` in `{condition}`" +
                                    " should be a list" +
                                    COLOR_RESET_ALL
                                )
                                text_handling.exit_game()
                            for i2 in current_enemy[condition]["known zones"]:
                                if i2 not in list(zone):
                                    print(
                                        COLOR_RED + "ERROR: " + COLOR_STYLE_BRIGHT +
                                        f"enemy id '{i}' mission id '{current_id}' isn't valid --> " +
                                        f"zone '{i2}' in `known zones`" +
                                        f" in `{condition}` doesn't exist" +
                                        COLOR_RESET_ALL
                                    )
                                    text_handling.exit_game()
                        if "known npcs" in current_enemy[condition]:
                            if type(current_enemy[condition]["known npcs"]) is not type([]):
                                print(
                                    COLOR_RED + "ERROR: " + COLOR_STYLE_BRIGHT +
                                    f"enemy id '{i}' mission id '{current_id}' isn't valid --> " +
                                    f"key `known npcs` in `{condition}`" +
                                    " should be a list" +
                                    COLOR_RESET_ALL
                                )
                                text_handling.exit_game()
                            for i2 in current_enemy[condition]["known npcs"]:
                                if i2 not in list(npcs):
                                    print(
                                        COLOR_RED + "ERROR: " + COLOR_STYLE_BRIGHT +
                                        f"enemy id '{i}' mission id '{current_id}' isn't valid --> " +
                                        f"npc '{i2}' in `known npcs`" +
                                        f" in `{condition}` doesn't exist" +
                                        COLOR_RESET_ALL
                                    )
                                    text_handling.exit_game()
                        if "has missions offered" in current_enemy[condition]:
                            if type(current_enemy[condition]["has missions offered"]) is not type([]):
                                print(
                                    COLOR_RED + "ERROR: " + COLOR_STYLE_BRIGHT +
                                    f"enemy id '{i}' mission id '{current_id}' isn't valid --> " +
                                    f"key `has missions offered` in `{condition}`" +
                                    " should be a list" +
                                    COLOR_RESET_ALL
                                )
                                exit_game()
                            for i2 in current_enemy[condition]["has missions offered"]:
                                if i2 not in list(mission):
                                    print(
                                        COLOR_RED + "ERROR: " + COLOR_STYLE_BRIGHT +
                                        f"enemy id '{i}' mission id '{current_id}' isn't valid --> " +
                                        f"mission '{i2}' in `has missions offered`" +
                                        f" in `{condition}` doesn't exist" +
                                        COLOR_RESET_ALL
                                    )
                                    exit_game()
                        if "has missions active" in current_enemy[condition]:
                            if type(current_enemy[condition]["has missions active"]) is not type([]):
                                print(
                                    COLOR_RED + "ERROR: " + COLOR_STYLE_BRIGHT +
                                    f"enemy id '{i}' mission id '{current_id}' isn't valid --> " +
                                    f"key `has missions active` in `{condition}`" +
                                    " should be a list" +
                                    COLOR_RESET_ALL
                                )
                                exit_game()
                            for i2 in current_enemy[condition]["has missions active"]:
                                if i2 not in list(mission):
                                    print(
                                        COLOR_RED + "ERROR: " + COLOR_STYLE_BRIGHT +
                                        f"enemy id '{i}' mission id '{current_id}' isn't valid --> " +
                                        f"mission '{i2}' in `has missions active`" +
                                        f" in `{condition}` doesn't exist" +
                                        COLOR_RESET_ALL
                                    )
                                    exit_game()
                        if "has items" in current_enemy[condition]:
                            if type(current_enemy[condition]["has items"]) is not type([]):
                                print(
                                    COLOR_RED + "ERROR: " + COLOR_STYLE_BRIGHT +
                                    f"enemy id '{i}' mission id '{current_id}' isn't valid --> " +
                                    f"key `has items` in `{condition}`" +
                                    " should be a list" +
                                    COLOR_RESET_ALL
                                )
                                text_handling.exit_game()
                            for i2 in current_enemy[condition]["has items"]:
                                if i2 not in list(item):
                                    print(
                                        COLOR_RED + "ERROR: " + COLOR_STYLE_BRIGHT +
                                        f"enemy id '{i}' mission id '{current_id}' isn't valid --> " +
                                        f"item '{i2}' in `has items`" +
                                        f" in `{condition}` doesn't exist" +
                                        COLOR_RESET_ALL
                                    )
                                    text_handling.exit_game()

                        if "random" in current[condition]:
                            if (
                                current_enemy[condition]["random"] > 1 or
                                current_enemy[condition]["random"] < 0
                            ):
                                print(
                                    COLOR_RED + "ERROR: " + COLOR_STYLE_BRIGHT +
                                    f"enemy id '{i}' mission id '{current_id}' isn't valid --> " +
                                    f"key `random` in `{condition}`" +
                                    " should be in between 0 and 1" +
                                    COLOR_RESET_ALL
                                )
                                text_handling.exit_game()

    # Specific checks for the `mounts` dictionary
    # CHECKS:
    # - check if feeding items exist
    for mount_id in list(mounts):
        mount = mounts[mount_id]
        for i in mount["feed"]["food"]:
            if i not in list(item):
                print(
                    COLOR_RED + "ERROR: " + COLOR_STYLE_BRIGHT +
                    f"mount id '{mount_id}' isn't valid --> " +
                    f"item '{i}' in `food` in `feed` doesn't exist" +
                    COLOR_RESET_ALL
                )
                text_handling.exit_game()

    # Specific checks for the `event` dictionary
    # CHECKS:
    # - checks on condition:
    #   * check if map points exist
    #   * check if map zones exist
    #   * check if regions exist
    #   * check if date is correct
    #   * check if items exist
    #   * check if missions exist
    #   * check if random is correct
    # - checks on actions:
    #   * check if failed mission exists
    #   * check if ran dialog exists
    #   * check if given and removed items exist
    #   * check if enemy list spawned exists
    #   * check if drunk drinks exist
    #   * check on added/remove diary stuff
    #      - check if zones exist
    #      - check if npcs exist
    #      - check if enemies exist
    #   * checks on ran scripts:
    #      - check if arguments exist
    for event_id in list(event):
        current = event[event_id]
        regions = {
            "fields": 0,
            "hills": 1,
            "plains": 2,
            "valleys": 3,
            "woods": 4,
            "dark woods": 5,
            "mountains": 6,
            "low mountains": 7,
            "high mountains": 8,
            "black rocky mountains": 9,
            "desert": 10,
            "desert hills": 11,
            "desert valleys": 12,
            "badlands": 13,
            "badlands canyon": 14,
            "badlands hills": 15,
            "badlands valleys": 16,
            "badlands plateaus": 17,
            "badlands butte": 18,
            "badlands landforms": 19,
            "flatlands": 20,
            "beach": 21,
            "plains canyon": 22,
            "desert canyons": 23,
            "rocky canyons": 24,
            "black rocky canyons": 25,
            "village": 26,
            "hostel": 27,
            "forge": 28,
            "blacksmith": 29,
            "stable": 30,
            "church": 31,
            "castle": 32,
            "lake": 33,
            "sea": 34,
            "swamps": 35,
            "grocery": 36,
            "harbor": 37,
            "dungeon": 38
        }

        if "map point" in current["source"]:
            for i in current["source"]["map point"]:
                if f"point{i}" not in list(map):
                    print(
                        COLOR_RED + "ERROR: " + COLOR_STYLE_BRIGHT +
                        f"event id '{event_id}' isn't valid --> " +
                        f"map point '{i}' in `map point` in `source` doesn't exist" +
                        COLOR_RESET_ALL
                    )
                    exit_game()
        if "map zone" in current["source"]:
            for i in current["source"]["map zone"]:
                if i not in list(zone):
                    print(
                        COLOR_RED + "ERROR: " + COLOR_STYLE_BRIGHT +
                        f"event id '{event_id}' isn't valid --> " +
                        f"zone '{i}' in `map zone` in `source` doesn't exist" +
                        COLOR_RESET_ALL
                    )
                    exit_game()
        if "region" in current["source"]:
            for i in current["source"]["region"]:
                if i not in list(regions):
                    print(
                        COLOR_RED + "ERROR: " + COLOR_STYLE_BRIGHT +
                        f"event id '{event_id}' isn't valid --> " +
                        f"region '{i}' in `region` in `source` doesn't exist" +
                        COLOR_RESET_ALL
                    )
                    exit_game()

        if (
            "date" in current["source"] and not
            bool(datetime.strptime(current["source"]["date"], '%m-%d-%Y'))
        ):
            print(
                COLOR_RED + "ERROR: " + COLOR_STYLE_BRIGHT +
                f"event id '{event_id}' isn't valid --> " +
                f"date '{current['source']['date']}' in `date` in `source`" +
                " does not use the required format: <month>-<day>-<year>" +
                COLOR_RESET_ALL
            )
            exit_game()

        if "has items" in current["source"]:
            for i in current["source"]["has items"]:
                if i not in list(item):
                    print(
                        COLOR_RED + "ERROR: " + COLOR_STYLE_BRIGHT +
                        f"event id '{event_id}' isn't valid --> " +
                        f"item '{i}' in `has items` in `source` doesn't exist" +
                        COLOR_RESET_ALL
                    )
                    exit_game()
        if "has missions offered" in current["source"]:
            for i in current["source"]["has missions offered"]:
                if i not in list(mission):
                    print(
                        COLOR_RED + "ERROR: " + COLOR_STYLE_BRIGHT +
                        f"event id '{event_id}' isn't valid --> " +
                        f"missions '{i}' in `has missions offered` in `source` doesn't exist" +
                        COLOR_RESET_ALL
                    )
                    exit_game()
        if "has missions active" in current["source"]:
            for i in current["source"]["has missions active"]:
                if i not in list(mission):
                    print(
                        COLOR_RED + "ERROR: " + COLOR_STYLE_BRIGHT +
                        f"event id '{event_id}' isn't valid --> " +
                        f"missions '{i}' in `has missions offered` in `source` doesn't exist" +
                        COLOR_RESET_ALL
                    )
                    exit_game()

        if "random" in current["source"]:
            if (
                current["source"]["random"] > 1 or
                current["source"]["random"] < 0
            ):
                print(
                    COLOR_RED + "ERROR: " + COLOR_STYLE_BRIGHT +
                    f"mission id '{current_id}' isn't valid --> " +
                    f"key `random` in `source`" +
                    " should be in between 0 and 1" +
                    COLOR_RESET_ALL
                )
                exit_game()

        if "fail mission" in current["actions"]:
            for i in current["actions"]["fail mission"]:
                if i not in list(mission):
                    print(
                        COLOR_RED + "ERROR: " + COLOR_STYLE_BRIGHT +
                        f"event id '{event_id}' isn't valid --> " +
                        f"missions '{i}' in `fail mission` in `actions` doesn't exist" +
                        COLOR_RESET_ALL
                    )
                    exit_game()

        if (
            "run dialog" in current["actions"] and
            current["actions"]["run dialog"] not in list(dialog)
        ):
            print(
                COLOR_RED + "ERROR: " + COLOR_STYLE_BRIGHT +
                f"event id '{event_id}' isn't valid --> " +
                f"dialog '{current['actions']['run dialog']}' in `run dialog` in `actions` doesn't exist" +
                COLOR_RESET_ALL
            )
            exit_game()

        for key in ["give item", "remove item"]:
            if key in current["actions"]:
                for i in current["actions"][key]:
                    if i not in list(item):
                        print(
                            COLOR_RED + "ERROR: " + COLOR_STYLE_BRIGHT +
                            f"event id '{event_id}' isn't valid --> " +
                            f"item '{i}' in `{key}` in `actions` doesn't exist" +
                            COLOR_RESET_ALL
                        )
                        exit_game()

        if (
            "enemy spawn" in current["actions"] and
            current["actions"]["enemy spawn"] not in list(enemy)
        ):
            print(
                COLOR_RED + "ERROR: " + COLOR_STYLE_BRIGHT +
                f"event id '{event_id}' isn't valid --> " +
                f"enemy '{current['actions']['enemy spawn']}' in `enemy spawn` " +
                "in `actions` doesn't exist" +
                COLOR_RESET_ALL
            )
            exit_game()

        if "use drink" in current["actions"]:
            for i in current["actions"]["use drink"]:
                if i not in list(drinks):
                    print(
                        COLOR_RED + "ERROR: " + COLOR_STYLE_BRIGHT +
                        f"event id '{event_id}' isn't valid --> " +
                        f"drink '{i}' in `use drink` in `actions` doesn't exist" +
                        COLOR_RESET_ALL
                    )
                    exit_game()

        for key in ["add to diary", "remove to diary"]:
            if key in current["actions"]:
                count = 0
                for key2 in ["known zones", "known enemies", "known npcs"]:
                    if key2 in current["actions"][key]:
                        for key3 in current["actions"][key][key2]:
                            if count == 0 and key3 not in list(zone):
                                print(
                                    COLOR_RED + "ERROR: " + COLOR_STYLE_BRIGHT +
                                    f"event id '{event_id}' isn't valid --> " +
                                    f"zone '{key3}' in `{key2}` in `{key}`" +
                                    "in `actions` doesn't exist" +
                                    COLOR_RESET_ALL
                                )
                                exit_game()
                            elif count == 1 and key3 not in list(enemy):
                                print(
                                    COLOR_RED + "ERROR: " + COLOR_STYLE_BRIGHT +
                                    f"event id '{event_id}' isn't valid --> " +
                                    f"enemy '{key3}' in `{key2}` in `{key}`" +
                                    "in `actions` doesn't exist" +
                                    COLOR_RESET_ALL
                                )
                                exit_game()
                            elif count == 2 and key3 not in list(npcs):
                                print(
                                    COLOR_RED + "ERROR: " + COLOR_STYLE_BRIGHT +
                                    f"event id '{event_id}' isn't valid --> " +
                                    f"npc '{key3}' in `{key2}` in `{key}`" +
                                    "in `actions` doesn't exist" +
                                    COLOR_RESET_ALL
                                )
                                exit_game()
                    count += 1

        # scripts tests TODO (for later maybe)
