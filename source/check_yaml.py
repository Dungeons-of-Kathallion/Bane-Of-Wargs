import yamale
import yaml
import appdirs
import logger_sys
import text_handling
from colors import *
from colorama import Fore, Back, Style, init, deinit

# initialize colorama
init()

# Create the variable for the program
# to access the program config/data folder
program_dir = str(appdirs.user_config_dir(appname='Bane-Of-Wargs'))


def check_yaml(file_path):
    file_type = 'none'
    with open(file_path, 'r') as f:
        file = yaml.safe_load(f)
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
                f"INFO: Validating file '{
                    file_path
                }' data: '{current_object_data}' with schema '{file_schema}'"
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
                file_schema = str(f'{program_dir}/game/schemas/{file_type}_{current_object_data["type"]}.yaml')

            schema = yamale.make_schema(str(file_schema))
            data = yamale.make_data(content=str(current_object_data))
            logger_sys.log_message(
                f"INFO: Validating file '{
                    file_path
                }' data: '{current_object_data}' with schema '{file_schema}'"
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
        print(
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
        possible_functions = ['print(', 'ask-input(', 'goto(', 'wait(', 'ask-confirmation(', 'if(', 'choice(', 'create-variable(']

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
    print(
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
    print(
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
        logger_sys.log_message(f"INFO: Validating data: '{data}' with schema '{program_dir}/game/schemas/map.yaml'")
        yamale.validate(schema, data)
    except Exception as error:
        print(
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
        logger_sys.log_message(f"INFO: Validating data: '{data}' with schema '{program_dir}/game/schemas/items_{data_type}.yaml'")
        yamale.validate(schema, data)
        if data_type == "Consumable":
            examine_consumable(data_real)
    except Exception as error:
        print(
            COLOR_RED + "ERROR: " + COLOR_RESET_ALL + COLOR_RED + COLOR_STYLE_BRIGHT +
            "A parsing error in a yaml file has been detected:\n" + COLOR_RESET_ALL + str(error)
        )
        logger_sys.log_message(f"ERROR: A parsing error in a yaml file has been detected:\n{error}")
        text_handling.exit_game()


def examine_drink(data):
    try:
        data = yamale.make_data(content=str(data))
        schema = yamale.make_schema(f'{program_dir}/game/schemas/drinks.yaml')
        logger_sys.log_message(f"INFO: Validating data: '{data}' with schema '{program_dir}/game/schemas/drinks.yaml'")
        yamale.validate(schema, data)
    except Exception as error:
        print(
            COLOR_RED + "ERROR: " + COLOR_RESET_ALL + COLOR_RED + COLOR_STYLE_BRIGHT +
            "A parsing error in a yaml file has been detected:\n" + COLOR_RESET_ALL + str(error)
        )
        logger_sys.log_message(f"ERROR: A parsing error in a yaml file has been detected:\n{error}")
        text_handling.exit_game()


def examine_enemy(data):
    try:
        data = yamale.make_data(content=str(data))
        schema = yamale.make_schema(f'{program_dir}/game/schemas/enemies.yaml')
        logger_sys.log_message(f"INFO: Validating data: '{data}' with schema '{program_dir}/game/schemas/enemies.yaml'")
        yamale.validate(schema, data)
    except Exception as error:
        print(
            COLOR_RED + "ERROR: " + COLOR_RESET_ALL + COLOR_RED + COLOR_STYLE_BRIGHT +
            "A parsing error in a yaml file has been detected:\n" + COLOR_RESET_ALL + str(error)
        )
        logger_sys.log_message(f"ERROR: A parsing error in a yaml file has been detected:\n{error}")
        text_handling.exit_game()


def examine_npc(data):
    try:
        data = yamale.make_data(content=str(data))
        schema = yamale.make_schema(f'{program_dir}/game/schemas/npcs.yaml')
        logger_sys.log_message(f"INFO: Validating data: '{data}' with schema '{program_dir}/game/schemas/npcs.yaml'")
        yamale.validate(schema, data)
    except Exception as error:
        print(
            COLOR_RED + "ERROR: " + COLOR_RESET_ALL + COLOR_RED + COLOR_STYLE_BRIGHT +
            "A parsing error in a yaml file has been detected:\n" + COLOR_RESET_ALL + str(error)
        )
        logger_sys.log_message(f"ERROR: A parsing error in a yaml file has been detected:\n{error}")
        text_handling.exit_game()


def examine_list(data):
    try:
        data = yamale.make_data(content=str(data))
        schema = yamale.make_schema(f'{program_dir}/game/schemas/lists.yaml')
        logger_sys.log_message(f"INFO: Validating data: '{data}' with schema '{program_dir}/game/schemas/lists.yaml'")
        yamale.validate(schema, data)
    except Exception as error:
        print(
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
        logger_sys.log_message(f"INFO: Validating data: '{data}' with schema '{program_dir}/game/schemas/zones_{data_type}.yaml'")
        yamale.validate(schema, data)
    except Exception as error:
        print(
            COLOR_RED + "ERROR: " + COLOR_RESET_ALL + COLOR_RED + COLOR_STYLE_BRIGHT +
            "A parsing error in a yaml file has been detected:\n" + COLOR_RESET_ALL + str(error)
        )
        logger_sys.log_message(f"ERROR: A parsing error in a yaml file has been detected:\n{error}")
        text_handling.exit_game()


def examine_dialog(data):
    try:
        data = yamale.make_data(content=str(data))
        schema = yamale.make_schema(f'{program_dir}/game/schemas/dialogs.yaml')
        logger_sys.log_message(f"INFO: Validating data: '{data}' with schema '{program_dir}/game/schemas/dialogs.yaml'")
        yamale.validate(schema, data)
    except Exception as error:
        print(
            COLOR_RED + "ERROR: " + COLOR_RESET_ALL + COLOR_RED + COLOR_STYLE_BRIGHT +
            "A parsing error in a yaml file has been detected:\n" + COLOR_RESET_ALL + str(error)
        )
        logger_sys.log_message(f"ERROR: A parsing error in a yaml file has been detected:\n{error}")
        text_handling.exit_game()


def examine_mission(data):
    try:
        data = yamale.make_data(content=str(data))
        schema = yamale.make_schema(f'{program_dir}/game/schemas/missions.yaml')
        logger_sys.log_message(f"INFO: Validating data: '{data}' with schema '{program_dir}/game/schemas/missions.yaml'")
        yamale.validate(schema, data)
    except Exception as error:
        print(
            COLOR_RED + "ERROR: " + COLOR_RESET_ALL + COLOR_RED + COLOR_STYLE_BRIGHT +
            "A parsing error in a yaml file has been detected:\n" + COLOR_RESET_ALL + str(error)
        )
        logger_sys.log_message(f"ERROR: A parsing error in a yaml file has been detected:\n{error}")
        text_handling.exit_game()


def examine_mount(data):
    try:
        data = yamale.make_data(content=str(data))
        schema = yamale.make_schema(f'{program_dir}/game/schemas/mounts.yaml')
        logger_sys.log_message(f"INFO: Validating data: '{data}' with schema '{program_dir}/game/schemas/mounts.yaml'")
        yamale.validate(schema, data)
    except Exception as error:
        print(
            COLOR_RED + "ERROR: " + COLOR_RESET_ALL + COLOR_RED + COLOR_STYLE_BRIGHT +
            "A parsing error in a yaml file has been detected:\n" + COLOR_RESET_ALL + str(error)
        )
        logger_sys.log_message(f"ERROR: A parsing error in a yaml file has been detected:\n{error}")
        text_handling.exit_game()


def consumable_effect_output_error(message):
    print(
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
                    consumable_effect_output_error("'x' key should be a list")


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
        print(
            COLOR_RED + "ERROR: " + COLOR_RESET_ALL + COLOR_RED + COLOR_STYLE_BRIGHT +
            "An error happened when examining item:\n" + COLOR_RESET_ALL + str(data)
        )
        logger_sys.log_message(f"ERROR: A error happened when examining item:\n{data}")
        text_handling.exit_game()
