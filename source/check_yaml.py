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
        data = yamale.make_data(content=str(data))
        schema = yamale.make_schema(f'{program_dir}/game/schemas/items_{data_type}.yaml')
        logger_sys.log_message(f"INFO: Validating data: '{data}' with schema '{program_dir}/game/schemas/items_{data_type}.yaml'")
        yamale.validate(schema, data)
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
