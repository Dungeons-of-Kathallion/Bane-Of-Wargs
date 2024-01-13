import yaml
import term_menu
import logger_sys
import os
from colorama import Fore, Back, Style, deinit, init
from colors import *

# initialize colorama
init()


# Functions to handle missions
def get_mission_id_from_name(mission_name, mission_data):
    global mission_id
    count = 0
    continue_action = True

    while count < len(list(mission_data)) and continue_action == True:
        current_mission_data = mission_data[str(list(mission_data)[count])]
        if current_mission_data["name"] == mission_name:
            continue_action = False
            mission_id = str(list(mission_data)[count])

        count += 1
    return mission_id

def print_description(mission_data, map):

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

# deinitialize colorama
deinit()
