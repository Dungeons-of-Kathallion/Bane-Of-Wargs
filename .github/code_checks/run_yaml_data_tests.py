import yamale
import yaml
from colorama import Fore, Back, Style, init, deinit

# initialize colorama
init()

# Create colors
COLOR_BLACK = Fore.BLACK
COLOR_WHITE = Fore.WHITE
COLOR_RED = Fore.RED
COLOR_GREEN = Fore.GREEN
COLOR_YELLOW = Fore.YELLOW
COLOR_BLUE = Fore.BLUE
COLOR_MAGENTA = Fore.MAGENTA
COLOR_CYAN = Fore.CYAN
COLOR_STYLE_BRIGHT = Style.BRIGHT
COLOR_RESET_ALL = Style.RESET_ALL

# Handling Functions

def exit_game():
    exit(1)

# Examining Functions

def check_dialog_conversations(dialog_data, dialog_name):
    # Run every checks required to pass
    # for a dialog conversation to be
    # valid

    conversation = dialog_data[dialog_name]["conversation"]

    # Create digits database
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
    exit_game()


def invalid_conversation_functions_output(dialog_name, function_name):
    # Output in the UI and the logging
    # proper error messages
    print(
        COLOR_RED + "ERROR: " + COLOR_STYLE_BRIGHT +
        f"dialog '{dialog_name}' conversation function '{function_name}' isn't a valid function --> closing game" +
        COLOR_RESET_ALL
    )
    exit_game()

def examine_start(data):
    try:
        data = yamale.make_data(content=str(data))
        schema = yamale.make_schema(f'schemas/start.yaml')
        yamale.validate(schema, data)
    except Exception as error:
        print(
            COLOR_RED + "ERROR: " + COLOR_RESET_ALL + COLOR_RED + COLOR_STYLE_BRIGHT +
            "A parsing error in a yaml file has been detected:\n" + COLOR_RESET_ALL + str(error)
        )
        exit_game()


def examine_map_point(data):
    try:
        data = yamale.make_data(content=str(data))
        schema = yamale.make_schema(f'schemas/map.yaml')
        yamale.validate(schema, data)
    except Exception as error:
        print(
            COLOR_RED + "ERROR: " + COLOR_RESET_ALL + COLOR_RED + COLOR_STYLE_BRIGHT +
            "A parsing error in a yaml file has been detected:\n" + COLOR_RESET_ALL + str(error)
        )
        exit_game()


def examine_item(data):
    try:
        data_type = data["type"].replace(':', '')
        data_real = data
        data = yamale.make_data(content=str(data))
        schema = yamale.make_schema(f'schemas/items_{data_type}.yaml')
        yamale.validate(schema, data)
        if data_type == "Consumable":
            examine_consumable(data_real)
    except Exception as error:
        print(
            COLOR_RED + "ERROR: " + COLOR_RESET_ALL + COLOR_RED + COLOR_STYLE_BRIGHT +
            "A parsing error in a yaml file has been detected:\n" + COLOR_RESET_ALL + str(error)
        )
        exit_game()


def examine_drink(data):
    try:
        data = yamale.make_data(content=str(data))
        schema = yamale.make_schema(f'schemas/drinks.yaml')
        yamale.validate(schema, data)
    except Exception as error:
        print(
            COLOR_RED + "ERROR: " + COLOR_RESET_ALL + COLOR_RED + COLOR_STYLE_BRIGHT +
            "A parsing error in a yaml file has been detected:\n" + COLOR_RESET_ALL + str(error)
        )
        exit_game()


def examine_enemy(data):
    try:
        data = yamale.make_data(content=str(data))
        schema = yamale.make_schema(f'schemas/enemies.yaml')
        yamale.validate(schema, data)
    except Exception as error:
        print(
            COLOR_RED + "ERROR: " + COLOR_RESET_ALL + COLOR_RED + COLOR_STYLE_BRIGHT +
            "A parsing error in a yaml file has been detected:\n" + COLOR_RESET_ALL + str(error)
        )
        exit_game()


def examine_npc(data):
    try:
        data = yamale.make_data(content=str(data))
        schema = yamale.make_schema(f'schemas/npcs.yaml')
        yamale.validate(schema, data)
    except Exception as error:
        print(
            COLOR_RED + "ERROR: " + COLOR_RESET_ALL + COLOR_RED + COLOR_STYLE_BRIGHT +
            "A parsing error in a yaml file has been detected:\n" + COLOR_RESET_ALL + str(error)
        )
        exit_game()


def examine_list(data):
    try:
        data = yamale.make_data(content=str(data))
        schema = yamale.make_schema(f'schemas/lists.yaml')
        yamale.validate(schema, data)
    except Exception as error:
        print(
            COLOR_RED + "ERROR: " + COLOR_RESET_ALL + COLOR_RED + COLOR_STYLE_BRIGHT +
            "A parsing error in a yaml file has been detected:\n" + COLOR_RESET_ALL + str(error)
        )
        exit_game()


def examine_zone(data):
    try:
        data_type = data["type"]
        data = yamale.make_data(content=str(data))
        schema = yamale.make_schema(f'schemas/zones_{data_type}.yaml')
        yamale.validate(schema, data)
    except Exception as error:
        print(
            COLOR_RED + "ERROR: " + COLOR_RESET_ALL + COLOR_RED + COLOR_STYLE_BRIGHT +
            "A parsing error in a yaml file has been detected:\n" + COLOR_RESET_ALL + str(error)
        )
        exit_game()


def examine_dialog(data):
    try:
        data = yamale.make_data(content=str(data))
        schema = yamale.make_schema(f'schemas/dialogs.yaml')
        yamale.validate(schema, data)
    except Exception as error:
        print(
            COLOR_RED + "ERROR: " + COLOR_RESET_ALL + COLOR_RED + COLOR_STYLE_BRIGHT +
            "A parsing error in a yaml file has been detected:\n" + COLOR_RESET_ALL + str(error)
        )
        exit_game()


def examine_mission(data):
    try:
        data = yamale.make_data(content=str(data))
        schema = yamale.make_schema(f'schemas/missions.yaml')
        yamale.validate(schema, data)
    except Exception as error:
        print(
            COLOR_RED + "ERROR: " + COLOR_RESET_ALL + COLOR_RED + COLOR_STYLE_BRIGHT +
            "A parsing error in a yaml file has been detected:\n" + COLOR_RESET_ALL + str(error)
        )
        exit_game()


def examine_mount(data):
    try:
        data = yamale.make_data(content=str(data))
        schema = yamale.make_schema(f'schemas/mounts.yaml')
        yamale.validate(schema, data)
    except Exception as error:
        print(
            COLOR_RED + "ERROR: " + COLOR_RESET_ALL + COLOR_RED + COLOR_STYLE_BRIGHT +
            "A parsing error in a yaml file has been detected:\n" + COLOR_RESET_ALL + str(error)
        )
        exit_game()
        
        
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
    if type(variable_to_test) != type(0):
        is_int = False
    elif type(variable_to_test) != type(.1):
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
                    consumable_effect_output_error("'critical hit chance coefficient' key should be an integer or floating number")
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
            if type(['1']) != type(data["attributes addition"]):
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
                if type(['1']) != type(data["inventory change"]["removals"]):
                    consumable_effect_output_error("'removals' key should be a list")
            if "additions" in data["inventory change"]:
                if type(['1']) != type(data["inventory change"]["additions"]):
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


# Main Function
def run():
    print("Analyzing map...")
    with open("data/map.yaml") as f:
        map = yaml.safe_load(f)
    for i in list(map):
        examine_map_point(map[i])

    print("Analyzing items...")
    with open("data/items.yaml") as f:
        item = yaml.safe_load(f)
    for i in list(item):
        examine_item(item[i])

    print("Analyzing drinks...")
    with open("data/drinks.yaml") as f:
        drinks = yaml.safe_load(f)
    for i in list(drinks):
        examine_drink(drinks[i])

    print("Analyzing enemies...")
    with open("data/enemies.yaml") as f:
        enemy = yaml.safe_load(f)
    for i in list(enemy):
        examine_enemy(enemy[i])

    print("Analyzing npcs...")
    with open("data/npcs.yaml") as f:
        npcs = yaml.safe_load(f)
    for i in list(npcs):
        examine_npc(npcs[i])

    print("Analyzing start...")
    with open("data/start.yaml") as f:
        start_player = yaml.safe_load(f)
        examine_start(start_player)

    print("Analyzing lists...")
    with open("data/lists.yaml") as f:
        lists = yaml.safe_load(f)
    for i in list(lists):
        examine_list(lists[i])

    print("Analyzing zones...")
    with open("data/zone.yaml") as f:
        zone = yaml.safe_load(f)
    for i in list(zone):
        examine_zone(zone[i])

    print("Analyzing dialogs...")
    with open("data/dialog.yaml") as f:
        dialog = yaml.safe_load(f)
    for i in list(dialog):
        check_dialog_conversations(dialog, i)
        examine_dialog(dialog[i])

    print("Analyzing missions...")
    with open("data/mission.yaml") as f:
        mission = yaml.safe_load(f)
    for i in list(mission):
        examine_mission(mission[i])

    print("Analyzing mounts...")
    with open("data/mounts.yaml") as f:
        mounts = yaml.safe_load(f)
    for i in list(mounts):
        examine_mount(mounts[i])
        
run()

# deinitialize colorama
deinit()
