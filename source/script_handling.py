import logger_sys
import appdirs


# Load program directory
program_dir = str(appdirs.user_config_dir(appname='Bane-Of-Wargs'))


# Handling Functions

def load_script(
    current_utility, preferences, player, map, item, drinks, enemy, npcs,
    start_player, lists, zone, dialog, mission, mounts, start_time, plugin=False
):
    logger_sys.log_message(f"INFO: Player is using utility item '{current_utility}'")
    if plugin:
        with open(
            program_dir + '/plugins/' + preferences["latest preset"]["plugin"] +
            '/scripts/' + item[current_utility]["script name"]
        ) as f:
            execute_script(
                f, current_utility, player, map, item, drinks, enemy, npcs,
                start_player, lists, zone, dialog, mission, mounts, start_time
            )
    else:
        with open(
            program_dir + '/game/scripts/' + item[current_utility]["script name"]
        ) as f:
            execute_script(
                f, current_utility, player, map, item, drinks, enemy, npcs,
                start_player, lists, zone, dialog, mission, mounts, start_time
            )


def execute_script(
    f, current_utility, player, map, item, drinks, enemy, npcs,
    start_player, lists, zone, dialog, mission, mounts, start_time
):
    global_arguments = {}
    if "arguments" in item[current_utility]:
        arguments = item[current_utility]['arguments']
        if "player" in arguments:
            global_arguments["player"] = player
        if "map" in arguments:
            global_arguments["map"] = map
        if "item" in arguments:
            global_arguments["item"] = item
        if "drinks" in arguments:
            global_arguments["drinks"] = drinks
        if "enemy" in arguments:
            global_arguments["enemy"] = enemy
        if "npcs" in arguments:
            global_arguments["npcs"] = npcs
        if "start_player" in arguments:
            global_arguments["start_player"] = start_player
        if "lists" in arguments:
            global_arguments["lists"] = lists
        if "zone" in arguments:
            global_arguments["zone"] = zone
        if "dialog" in arguments:
            global_arguments["dialog"] = dialog
        if "mission" in arguments:
            global_arguments["mission"] = mission
        if "mounts" in arguments:
            global_arguments["mounts"] = mounts
        if "start_time" in arguments:
            global_arguments["start_time"] = start_time
    exec(f.read(), global_arguments)
