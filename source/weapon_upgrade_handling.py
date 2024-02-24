import logger_sys
import text_handling


# Handling functions
def check_for_item(item_name, item):
    logger_sys.log_message(f"INFO: Checking if item '{item_name}' actually exists")
    item_exist = False
    if str(item_name) in list(item):
        item_exist = True
    return item_exist


def check_weapon_next_upgrade_name(item_name, item):
    logger_sys.log_message(f"INFO: Check for equipment '{item_name}' next upgrade")
    weapon_next_upgrade_name = str(item_name)
    check_weapon_max_upgrade_number = check_weapon_max_upgrade(str(weapon_next_upgrade_name), item)
    if item[weapon_next_upgrade_name]["upgrade tier"] == check_weapon_max_upgrade_number:
        weapon_next_upgrade_name = None
        logger_sys.log_message(f"INFO: No next upgrade found for equipment '{item_name}'")
    else:
        item_data = item[item_name]
        further_upgrade = True
        item_data = item[weapon_next_upgrade_name]
        # get logical weapon new upgrade name
        weapon_already_upgraded = False
        if "(" in str(item_name):
            weapon_already_upgraded = True

        if not weapon_already_upgraded:
            weapon_next_upgrade_name = str(item_name) + " (1)"
        else:
            weapon_next_upgrade_name = str(
                weapon_next_upgrade_name[0: weapon_next_upgrade_name.index("(")]
            ) + "(" + str(item_data["upgrade tier"] + 1) + ")"

        # check if the next upgrade actually exist
        item_upgrade_exist = check_for_item(weapon_next_upgrade_name, item)
        if not item_upgrade_exist:
            further_upgrade = False

        weapon_next_upgrade_name = str(weapon_next_upgrade_name)
        logger_sys.log_message(f"INFO: Found next upgrade for equipment '{item_name}': '{weapon_next_upgrade_name}'")

    return weapon_next_upgrade_name


def check_weapon_max_upgrade(item_name, item):
    logger_sys.log_message(f"INFO: Getting equipment '{item_name}' max upgrade")
    weapon_next_upgrade_name = str(item_name)
    item_data = item[item_name]
    further_upgrade = True

    while further_upgrade:
        item_data = item[weapon_next_upgrade_name]
        # get logical weapon new upgrade name
        weapon_already_upgraded = False
        if "(" in str(weapon_next_upgrade_name):
            weapon_already_upgraded = True

        if not weapon_already_upgraded:
            weapon_next_upgrade_name = str(item_name) + " (1)"
        else:
            weapon_next_upgrade_name = str(
                weapon_next_upgrade_name[0: weapon_next_upgrade_name.index("(")]
            ) + "(" + str(item_data["upgrade tier"] + 1) + ")"

        # check if the next upgrade actually exist
        item_upgrade_exist = check_for_item(weapon_next_upgrade_name, item)
        if not item_upgrade_exist:
            further_upgrade = False

    # correct max upgrade count
    weapon_next_upgrade_name_count = weapon_next_upgrade_name
    listOfWords = weapon_next_upgrade_name_count.split("(", 1)
    if len(listOfWords) > 0:
        weapon_next_upgrade_name_count = listOfWords[1]
    weapon_next_upgrade_name_count = int(weapon_next_upgrade_name_count.replace(")", ""))
    weapon_next_upgrade_name_count -= 1

    return weapon_next_upgrade_name_count


def detect_weapon_next_upgrade_items(item_name, item):
    logger_sys.log_message(f"INFO: Getting equipment '{item_name}' next upgrade items")
    weapon_next_upgrade_name = str(item_name)
    item_data = item[item_name]
    weapon_already_upgraded = False

    # get logical weapon new upgrade name
    if "(" in str(item_name):
        weapon_already_upgraded = True

    if not weapon_already_upgraded:
        weapon_next_upgrade_name = str(item_name) + " (1)"
    else:
        weapon_next_upgrade_name = str(
            weapon_next_upgrade_name[0: weapon_next_upgrade_name.index("(")]
        ) + "(" + str(item_data["upgrade tier"] + 1) + ")"

    # check if the next upgrade actually exist
    item_upgrade_exist = check_for_item(weapon_next_upgrade_name, item)
    if not item_upgrade_exist:
        weapon_next_upgrade_name = None

    # get next weapon upgrade needed items
    if weapon_next_upgrade_name is not None:
        weapon_next_upgrade_items = item[str(weapon_next_upgrade_name)]["for this upgrade"]
    else:
        weapon_next_upgrade_items = "None"

    # convert list to string and
    # format the string to look better

    if weapon_next_upgrade_name is not None:
        weapon_next_upgrade_items = text_handling.multiple_items_in_list_formatting(weapon_next_upgrade_items)
    weapon_next_upgrade_items = str(weapon_next_upgrade_items)
    weapon_next_upgrade_items = weapon_next_upgrade_items.replace("'", '')
    weapon_next_upgrade_items = weapon_next_upgrade_items.replace("[", '')
    weapon_next_upgrade_items = weapon_next_upgrade_items.replace("]", '')

    logger_sys.log_message(f"INFO: Found equipment '{item_name}' next upgrade items: '{weapon_next_upgrade_items}'")
    return weapon_next_upgrade_items
