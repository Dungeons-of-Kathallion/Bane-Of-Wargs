import yaml
import term_menu
import logger_sys
import os
import dialog_handling
from colorama import Fore, Back, Style, deinit, init
from colors import *

# initialize colorama
init()


# Functions to handle missions
def get_mission_id_from_name(mission_name, mission_data):
    logger_sys.log_message(f"INFO: Getting mission name '{mission_name}' corresponding id")
    global mission_id
    count = 0
    continue_action = True

    while count < len(list(mission_data)) and continue_action == True:
        current_mission_data = mission_data[str(list(mission_data)[count])]
        if current_mission_data["name"] == mission_name:
            continue_action = False
            mission_id = str(list(mission_data)[count])

        count += 1
    logger_sys.log_message(f"INFO: Found corresponding id of mission name '{mission_name}': {mission_id}")
    return mission_id

def print_description(mission_data, map):
    logger_sys.log_message(f"INFO: Printing mission '{mission_data}' description to GUI")

    logger_sys.log_message(f"INFO: Generating mission text replacements")
    # Get text replacements
    # Payment of the mission when completed
    payment_for_mission = None
    if "on complete" in list(mission_data):
        if "payment" in list(mission_data["on complete"]):
            payment_for_mission = mission_data["on complete"]["payment"]
    # Destination of the mission
    destination_point = map["point" + str(mission_data["destination"])]
    destination_for_mission = "[X:" + str(destination_point["x"]) + ", Y:" + str(destination_point["y"]) + "]"
    # Deadline of the mission to be completed
    deadline_for_mission = None
    if "deadline" in list(mission_data):
        deadline_for_mission = mission_data["deadline"]
    # Stopovers of the mission
    stopovers_for_mission = None
    if "stopovers" in list(mission_data):
        stopovers_for_mission = mission_data["stopovers"]
        new_stopovers_for_mission = []
        count = 0
        while count < len(stopovers_for_mission):
            current_map_point_data = map["point" + str(stopovers_for_mission[count])]
            current_map_point_coordinates = "[X:" + str(current_map_point_data["x"]) + ", Y:" + str(current_map_point_data["y"]) + "]"
            new_stopovers_for_mission.append(current_map_point_coordinates)

            count += 1
        new_stopovers_for_mission = str(new_stopovers_for_mission)

    # Load text replacements
    mission_text_replacements = {
        "$name_mission": mission_data["name"],
        "$description": mission_data["description"],
        "$payment": payment_for_mission,
        "$destination": destination_for_mission,
        "$deadline": deadline_for_mission,
        "$stopovers": new_stopovers_for_mission
    }
    logger_sys.log_message(f"INFO: Loading missions text replacements: '{mission_text_replacements}'")


    text = str(mission_data["description"])
    # Replace text replacement in the description by
    # its corresponding value in the mission_text_replacements
    # dictionary defined sooner
    count = 0
    while count < len(list(mission_text_replacements)):
        current_text_replacement = list(mission_text_replacements)[count]
        text = text.replace(current_text_replacement, str(mission_text_replacements[current_text_replacement]))

        count += 1

    # Print the text
    new_input = ""
    for i, letter in enumerate(text):
        if i % 54 == 0:
            new_input += '\n'
        new_input += letter

    # This is just because at the beginning too a `\n` character gets added
    new_input = new_input[1:]
    print(str(new_input))

def offer_mission(mission_id, player, missions_data, dialog, preferences, text_replacements_generic, drinks):
    logger_sys.log_message(f"INFO: Offering mission '{mission_id}' to player")
    data = missions_data[mission_id]

    # Add the mission ID to the player's
    # offered missions list
    player["offered missions"].append(mission_id)

    # Trigger the mission 'on offer'
    # triggers if there are

    logger_sys.log_message(f"INFO: Triggering mission '{mission_id}' 'on offer' triggers")
    if "on offer" in list(data):
        # Only ask for accepting mission if there is a dialog,
        # else, make the player automatically accept it
        if "dialog" in list(data["on offer"]):
            dialog_handling.print_dialog(data["on offer"]["dialog"], dialog, preferences, text_replacements_generic, player, drinks)
            accept = input("Do you want to accept this task? (y/n)")
            print("=======================================================")
            if accept.startswith('y'):
                if player["active missions"] == None:
                    player["active missions"] = []
                player["active missions"].append(mission_id)
        else:
            if player["active missions"] == None:
                player["active missions"] = []
            player["active missions"].append(mission_id)
        if "payment" in list(data["on offer"]):
            player["gold"] += int(data["on offer"]["payment"])
        if "fine" in list(data["on offer"]):
            player["gold"] -= int(data["on offer"]["fine"])
        if "exp addition" in list(data["on offer"]):
            player["exp"] += int(data["on offer"]["exp addition"])
    logger_sys.log_message(f"INFO: Finished triggering mission '{mission_id}' 'on offer' triggers")

# deinitialize colorama
deinit()
