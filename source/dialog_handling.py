# source imports
from colors import *
import logger_sys
import text_handling
import terminal_handling
import script_handling
from terminal_handling import cout, cinput
# external imports
import appdirs
import time


# Get program directory
program_dir = str(appdirs.user_config_dir(appname='Bane-Of-Wargs'))

# Functions to handle dialogs


def print_dialog(
    current_dialog, dialog, preferences, text_replacements_generic, player, drinks,
    item, enemy, npcs, start_player, lists, zone,
    mission, mounts, start_time, map
):
    current_dialog_name = current_dialog
    logger_sys.log_message(f"INFO: Printing dialog '{current_dialog_name}'")
    current_dialog = dialog[str(current_dialog)]
    dialog_len = len(current_dialog["conversation"])
    if "scene" in current_dialog:
        current_dialog_scene = str(current_dialog["scene"])
        logger_sys.log_message(
            f"INFO: Printing dialog '{current_dialog_name}' scene at " +
            f"'{program_dir}/temp/imgs/{current_dialog_scene}.txt'"
        )
        with open(f"{program_dir}/temp/imgs/{current_dialog_scene}.txt") as f:
            cout(text_handling.apply_yaml_data_color_code(f.read()))
    count = 0

    # Conversation loop
    # Here we get all the labels and execute functions
    # one by one in the list
    new_text_replacements = text_replacements_generic
    current_label = current_dialog["conversation"][0]['label 1']
    try:
        load_conversation_label(current_label, preferences, new_text_replacements, current_dialog)
    except Exception as error:
        cout(
            COLOR_RED + "ERROR: " + COLOR_STYLE_BRIGHT +
            f"an error occurred when trying to run dialog '{current_dialog_name}' conversations:\n{error}" +
            COLOR_RESET_ALL
        )
        logger_sys.log_message(
            f"ERROR: an error occurred when trying to run dialog '{current_dialog_name}' " +
            f"conversations:\n{error} --> shutting down game"
        )
        text_handling.exit_game()

    logger_sys.log_message(f"INFO: Printing dialog '{current_dialog_name}' conversation")
    if current_dialog["use actions"]:
        logger_sys.log_message(f"INFO: Executing dialog '{current_dialog_name}' actions on the player")
        actions = current_dialog["actions"]
        if "give item" in actions:
            given_items = actions["give item"]
            given_items_len = len(given_items)
            count = 0
            logger_sys.log_message(f"INFO: Giving to the player items '{given_items}'")
            while count < given_items_len:
                selected_item = given_items[count]
                if str(selected_item).replace('$', '') in list(new_text_replacements):
                    selected_item = new_text_replacements[str(selected_item).replace('$', '')]
                player["inventory"].append(selected_item)
                count += 1
        if "add attributes" in actions:
            count = 0
            added_attributes = actions["add attributes"]
            added_attributes_len = len(added_attributes)
            logger_sys.log_message(f"INFO: Adding attributes '{added_attributes}' to the player")
            while count < added_attributes_len:
                selected_attribute = added_attributes[count]
                if str(selected_attribute).replace('$', '') in list(new_text_replacements):
                    selected_attribute = new_text_replacements[str(selected_attribute).replace('$', '')]
                player["attributes"].append(selected_attribute)
                count += 1
        if "health modification" in actions:
            if "diminution" in actions["health modification"]:
                logger_sys.log_message(
                    "INFO: Removing " + str(actions["health modification"]["diminution"]) +
                    " hp from the player's health"
                )
                diminution = actions["health modification"]["diminution"]
                if str(diminution).replace('$', '') in list(new_text_replacements):
                    diminution = new_text_replacements[str(diminution).replace('$', '')]
                player["health"] -= diminution
            if "augmentation" in actions["health modification"]:
                logger_sys.log_message(
                    "INFO: Adding " + str(actions["health modification"]["augmentation"]) +
                    " hp from the player's health"
                )
                augmentation = actions["health modification"]["augmentation"]
                if str(augmentation).replace('$', '') in list(new_text_replacements):
                    augmentation = new_text_replacements[str(augmentation).replace('$', '')]
                if augmentation >= 999:
                    augmentation = player["max health"]
                player["health"] += augmentation
            if "max health" in actions["health modification"]:
                if "diminution" in actions["health modification"]["max health"]:
                    logger_sys.log_message(
                        "INFO: Removing " + str(actions["health modification"]["max health"]["diminution"]) +
                        " hp from the player's max health"
                        )
                    diminution = actions["health modification"]["max health"]["diminution"]
                    if str(diminution).replace('$', '') in list(new_text_replacements):
                        diminution = new_text_replacements[str(diminution).replace('$', '')]
                    player["max health"] -= diminution
                if "augmentation" in actions["health modification"]["max health"]:
                    logger_sys.log_message(
                        "INFO: Adding " + str(actions["health modification"]["max health"]["augmentation"]) +
                        " hp from the player's max health"
                        )
                    augmentation = actions["health modification"]["max health"]["augmentation"]
                    if str(augmentation).replace('$', '') in list(new_text_replacements):
                        augmentation = new_text_replacements[str(augmentation).replace('$', '')]
                    player["max health"] += augmentation
        if "gold modification" in actions:
            if "diminution" in actions["gold modification"]:
                logger_sys.log_message(
                    "INFO: Removing " + str(actions["gold modification"]["diminution"]) + " gold to the player"
                )
                diminution = actions["gold modification"]["diminution"]
                if str(diminution).replace('$', '') in list(new_text_replacements):
                    diminution = new_text_replacements[str(diminution).replace('$', '')]
                player["gold"] -= diminution
            if "augmentation" in actions["gold modification"]:
                logger_sys.log_message(
                    "INFO: Adding " + str(actions["gold modification"]["augmentation"]) + " gold to the player"
                )
                augmentation = actions["gold modification"]["augmentation"]
                if str(augmentation).replace('$', '') in list(new_text_replacements):
                    augmentation = new_text_replacements[str(augmentation).replace('$', '')]
                player["gold"] += augmentation
        if "remove item" in actions:
            removed_items = actions["remove item"]
            removed_items_len = len(removed_items)
            count = 0
            logger_sys.log_message(f"INFO: Removing items '{removed_items}' from player's inventory")
            while count < removed_items_len:
                selected_item = removed_items[count]
                if str(selected_item).replace('$', '') in list(new_text_replacements):
                    selected_item = new_text_replacements[str(selected_item).replace('$', '')]
                player["inventory"].remove(selected_item)
                count += 1
        if "add to diary" in actions:
            if "known zones" in actions["add to diary"]:
                added_visited_zones = actions["add to diary"]["known zones"]
                added_visited_zones_len = len(added_visited_zones)
                count = 0
                logger_sys.log_message(f"INFO: Adding zones '{added_visited_zones}' to player's visited zones")
                while count < added_visited_zones_len:
                    selected_zone = added_visited_zones[count]
                    if str(selected_zone).replace('$', '') in list(new_text_replacements):
                        selected_zone = new_text_replacements[str(selected_zone).replace('$', '')]
                    player["visited zones"].append(selected_zone)
                    count += 1
            if "known enemies" in actions["add to diary"]:
                added_known_enemies = actions["add to diary"]["known enemies"]
                added_known_enemies_len = len(added_known_enemies)
                count = 0
                logger_sys.log_message(f"INFO: Adding enemies '{added_known_enemies}' to player's known enemies")
                while count < added_known_enemies_len:
                    selected_enemy = added_known_enemies[count]
                    if str(selected_enemy).replace('$', '') in list(new_text_replacements):
                        selected_enemy = new_text_replacements[str(selected_enemy).replace('$', '')]
                    player["enemies list"].append(selected_enemy)
                    count += 1
            if "known npcs" in actions["add to diary"]:
                added_known_npcs = actions["add to diary"]["known npcs"]
                added_known_npcs_len = len(added_known_npcs)
                count = 0
                logger_sys.log_message(f"INFO: Adding npcs '{added_known_npcs}' to player's known npcs")
                while count < added_known_npcs_len:
                    selected_npc = added_known_npcs[count]
                    if str(selected_npc).replace('$', '') in list(new_text_replacements):
                        selected_npc = new_text_replacements[str(selected_npc).replace('$', '')]
                    player["met npcs names"].append(selected_npc)
                    count += 1
        if "remove to diary" in actions:
            if "known zones" in actions["remove to diary"]:
                removed_visited_zones = actions["remove to diary"]["known zones"]
                removed_visited_zones_len = len(removed_visited_zones)
                count = 0
                logger_sys.log_message(f"INFO: Removing zones '{added_visited_zones}' to player's visited zones")
                while count < removed_visited_zones_len:
                    selected_zone = removed_visited_zones[count]
                    if str(selected_zone).replace('$', '') in list(new_text_replacements):
                        selected_zone = new_text_replacements[str(selected_zone).replace('$', '')]
                    player["visited zones"].remove(selected_zone)
                    count += 1
            if "known enemies" in actions["remove to diary"]:
                removed_known_enemies = actions["remove to diary"]["known enemies"]
                removed_known_enemies_len = len(removed_known_enemies)
                count = 0
                logger_sys.log_message(f"INFO: Removing enemies '{added_known_enemies}' to player's known enemies")
                while count < removed_known_enemies_len:
                    selected_enemy = removed_known_npcs[count]
                    if str(selected_enemy).replace('$', '') in list(new_text_replacements):
                        selected_enemy = new_text_replacements[str(selected_enemy).replace('$', '')]
                    player["enemies list"].remove(selected_enemy)
                    count += 1
            if "known npcs" in actions["remove to diary"]:
                removed_known_npcs = actions["remove to diary"]["known npcs"]
                removed_known_npcs_len = len(removed_known_npcs)
                count = 0
                logger_sys.log_message(f"INFO: Removing npcs '{added_known_npcs}' to player's known npcs")
                while count < removed_known_npcs_len:
                    selected_npc = removed_known_npcs[count]
                    if str(selected_npc).replace('$', '') in list(new_text_replacements):
                        selected_npc = new_text_replacements[str(selected_npc).replace('$', '')]
                    player["met npcs names"].append(selected_npc)
                    count += 1
        if "use drink" in actions:
            used_drinks = actions["use drink"]
            used_drinks_len = len(used_drinks)
            count = 0
            logger_sys.log_message(f"INFO: Using drinks '{used_drinks}'")
            while count < used_drinks_len:
                selected_drink = used_drinks[count]
                if str(selected_drink).replace('$', '') in list(new_text_replacements):
                    selected_drink = new_text_replacements[str(selected_drink).replace('$', '')]
                if drinks[selected_drink]["healing level"] == 999:
                    player["health"] = player["max health"]
                else:
                    player["health"] += drinks[selected_drink]["healing level"]

                count += 1
        if "run scripts" in actions:
            plugin = preferences["latest preset"]["type"] == "plugin"
            count = 0
            for script in actions["run scripts"]:
                current_script_data = actions["run scripts"][count]
                script_handling.load_script(
                    current_script_data, preferences,  player, map, item, drinks, enemy, npcs,
                    start_player, lists, zone, dialog, mission, mounts, start_time,
                    text_replacements_generic, plugin
                )
                count += 1


def load_conversation_label(label_data, preferences, new_text_replacements, current_dialog):
    # Load a dialog conversation specific label functions
    # one by one and add required data generated by the player

    count = 0
    while count < len(label_data):
        current_function = label_data[count]
        if list(current_function)[0].lower().startswith('if('):
            current_function = list(current_function)[0]
            current_function_executions = label_data[count][current_function]
        elif list(current_function)[0].lower().startswith('choice()'):
            current_function = list(current_function)[0]
            current_function_choices = label_data[count][current_function]
        if current_function.lower().startswith('print('):
            conversation_print(current_function, preferences, new_text_replacements)
        elif current_function.lower().startswith('create-variable('):
            conversation_create_variable(current_function, new_text_replacements)
        elif current_function.lower().startswith('ask-input('):
            conversation_ask_input(current_function, new_text_replacements)
        elif current_function.lower().startswith('goto('):
            conversation_goto(current_function, preferences, new_text_replacements, current_dialog)
            # Stop the current loop
            count = 1e999
        elif current_function.lower().startswith('wait('):
            wait_time = current_function.replace('wait(', '')
            wait_time = int(wait_time.replace(')', ''))
            time.sleep(wait_time)
        elif current_function.lower().startswith('ask-confirmation('):
            conversation_ask_confirmation(current_function, new_text_replacements)
        elif current_function.lower().startswith('if('):
            conversation_if_statement(
                current_function, current_function_executions, new_text_replacements, preferences, current_dialog
            )
        elif current_function.lower().startswith('choice()'):
            conversation_choice_maker(
                current_function, current_function_choices, new_text_replacements, preferences, current_dialog
            )
        # If a function entered isn't valid, report
        # an error and shut down the program
        else:
            cout(
                COLOR_RED + "ERROR: " + COLOR_STYLE_BRIGHT + f"dialog conversation function '{current_function}' isn't valid" +
                COLOR_RESET_ALL
            )
            logger_sys.log_message(
                f"ERROR: dialog conversation function '{current_function}' isn't valid --> shutting down program"
            )
            time.sleep(5)
            text_handling.exit_game()

        count += 1


# Dialog conversation functions

def conversation_print(conversation_input, preferences, new_text_replacements):
    # Run a print function: print text output in
    # the UI
    conversation_input = conversation_input.replace('print(', '')
    conversation_input = conversation_input.replace(')', '')
    count = 0
    for replacement in list(new_text_replacements):
        conversation_input = conversation_input.replace(
            replacement, str(new_text_replacements[replacement])
        )

    text_handling.print_speech_text_effect(conversation_input, preferences)


def conversation_ask_input(conversation_input, new_text_replacements):
    # Run an ask-input function: ask user for any input
    player_input = cinput()
    output_variable = conversation_input.replace('ask-input(', '')
    output_variable = output_variable.replace(')', '')

    new_text_replacements[f"{output_variable}"] = player_input


def conversation_create_variable(conversation_input, new_text_replacements):
    output_variable = conversation_input.replace('create-variable(', '')
    output_variable = output_variable.replace(')', '')
    output_variable_name = output_variable.split(', ', 1)[0]
    output_variable_value = output_variable.split(', ', 1)[1]

    # If the value is supposed to be an other
    # type than a string, convert it to its
    # intended type
    if output_variable_value == 'True':
        output_variable_value = True
    elif output_variable_value == 'False':
        output_variable_value = False
    elif output_variable_value.isnumeric():
        output_variable_value = float(output_variable_value)

    new_text_replacements[f"{output_variable_name}"] = output_variable_value


def conversation_goto(conversation_input, preferences, new_text_replacements, current_dialog):
    # Run a goto function: load a new label and
    # execute its functions on by one in order
    label_name = conversation_input.replace('goto(', '')
    label_name = label_name.replace(')', '')
    label_name_int = int(label_name.split("label", 1)[1]) - 1
    label_data = current_dialog["conversation"][label_name_int][label_name]

    load_conversation_label(label_data, preferences, new_text_replacements, current_dialog)


def conversation_ask_confirmation(conversation_input, new_text_replacements):
    # Run a ask-confirmation function: ask for player input
    # with either 'Yes' or 'No' as an answer
    choice = ['Yes', 'No']
    confirmation = terminal_handling.show_menu(choice)
    if confirmation == 'Yes':
        confirmation = True
    else:
        confirmation = False
    output_variable = conversation_input.replace('ask-confirmation(', '')
    output_variable = output_variable.replace(')', '')
    new_text_replacements[f"{output_variable}"] = confirmation
    return confirmation


def conversation_if_statement(conversation_input, executions_dict, new_text_replacements, preferences, current_dialog):
    # Run a if statement function: check if the statement return
    # a 'True' boolean value and if yes, execute the function's
    # functions one by one in order
    statement = conversation_input.replace('if(', '')
    statement = statement.replace(')', '')
    statement_1 = new_text_replacements[statement.split(", ", 1)[0]]
    statement_2 = statement.split(", ", 1)[1]

    # If the value is supposed to be an other
    # type than a string, convert it to its
    # intended type
    if statement_2 == 'True':
        statement_2 = True
    elif statement_2 == 'False':
        statement_2 = False
    elif statement_2.isnumeric():
        statement_2 = float(statement_2)

    if statement_1 == statement_2:
        load_conversation_label(executions_dict, preferences, new_text_replacements, current_dialog)


def conversation_choice_maker(conversation_input, choices_dict, new_text_replacements, preferences, current_dialog):
    # Run a choice function: create multiple choices
    # and ask the player to choose one. Also loads
    # the choices output functions and run them
    # if they're triggered
    choices = []
    for current_choice_making in choices_dict:
        choice_name = current_choice_making.split("(", 1)[1]
        choice_name = choice_name.split(",", 1)[0]
        choices += [str(choice_name)]

    player_choice = terminal_handling.show_menu(choices)
    choice_position = choices.index(player_choice)

    choice_action = choices_dict[choice_position]
    choice_action = choice_action.split(", ", 1)[1]
    choice_action = choice_action.split("))", 1)[0] + ")"
    if choice_action.lower().startswith('print('):
        conversation_print(choice_action, preferences, new_text_replacements)
    elif choice_action.lower().startswith('create-variable('):
        conversation_create_variable(choice_action, new_text_replacements)
    elif choice_action.lower().startswith('ask-input('):
        conversation_ask_input(choice_action, new_text_replacements)
    elif choice_action.lower().startswith('goto('):
        conversation_goto(choice_action, preferences, new_text_replacements, current_dialog)
        # Stop the current loop
        count = 1e999
    elif choice_action.lower().startswith('wait('):
        wait_time = choice_action.replace('wait(', '')
        wait_time = int(wait_time.replace(')', ''))
        time.sleep(wait_time)
    elif choice_action.lower().startswith('ask-confirmation('):
        conversation_ask_confirmation(choice_action, new_text_replacements)
