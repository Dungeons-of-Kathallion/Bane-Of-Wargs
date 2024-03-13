# source imports
import text_handling
import item_handling
from colors import *
from terminal_handling import cout, cinput
# external imports
import random
import time

# battle stats
defend = 0
turn = True
fighting = True


def calculate_player_risk(
    player, item, enemies_remaining, chosen_enemy, enemy,
    player_damage_coefficient, enemies_damage_coefficient
):
    # get all stats
    player_hp = player["health"]
    player_agi = player["agility"]
    player_prot = player["armor protection"]
    if player["held item"] != " ":
        player_held_item_damage = item[player["held item"]]["damage"]
    else:
        player_held_item_damage = 1
    player_av_dmg = round(
        (
            (
                player_held_item_damage + 1 + player_held_item_damage
            ) * player["critical hit chance"] * 2.3
        ) / 2, 2
    )
    if player["held item"] != " ":
        player_def = item[player["held item"]]["defend"]
    else:
        player_def = 1
    player_critic_ch = player["critical hit chance"]
    player_health_cap = 1   # placeholder
    enemies_number = enemies_remaining
    enemy_health = random.randint(chosen_enemy["health"]["min spawning health"], chosen_enemy["health"]["max spawning health"])
    enemy_agility = chosen_enemy["agility"]
    enemy_max_damage = chosen_enemy["damage"]["max damage"]
    enemy_min_damage = chosen_enemy["damage"]["min damage"]
    enemy_critical_chance = chosen_enemy["damage"]["critical chance"]
    enemy_av_dmg = round((enemy_max_damage + enemy_min_damage + enemy_max_damage * enemy_critical_chance * 1.8) / 2, 2)

    # calculate player health capabilities (how many HP the player can restore)
    count = 0
    player_inventory = player["inventory"]
    player_inventory_len = len(player_inventory) - 1
    current_item_health_restoration = 0
    item_health_bonus = 0
    while count < player_inventory_len:

        selected_item = player_inventory[count]

        if item[selected_item]["type"] == "Food":
            item_health_restoration = item[selected_item]["healing level"]
            item_health_bonus = item[selected_item]["max bonus"]
            if item_health_restoration == 999:
                current_item_health_restoration = player["max health"]
            else:
                current_item_health_restoration = int(item_health_restoration)
            if item_health_bonus != 0:
                item_health_bonus = int(item[selected_item]["max bonus"]) / 2

        player_health_cap += current_item_health_restoration
        player_health_cap += item_health_bonus

        count += 1
    # get differences between player and enemy HP
    hp_diff = ((player_hp + player_health_cap + player_def * 1.5) - (enemy_health * enemies_number))

    # dodge formula is if round(random.uniform(.30, player_agility), 2) > enemy_agility / 1.15:
    # enemy agility / 1.15
    # .6 / 1.15 =  .5 # enemy agility
    # 1.05 - .3 = # 75 true possibilities
    # #enemy agility .5 - .3 = .2 # 20 false possibilities
    # 75/75+20 = 75/95 # 75/95 true possibilities
    # 75*100/95 # 78% dodge chance for player

    # dodge chance calculation

    # player
    real_enemy_agility = enemy_agility / 1.15
    player_true_dodge_possibilities = (player_agi - .3) * 100
    player_false_dodge_possibilities = (real_enemy_agility - .3) * 100
    player_total_possibilities = player_true_dodge_possibilities + player_false_dodge_possibilities

    player_dodge_chance = round((player_true_dodge_possibilities / player_total_possibilities) * 100)

    # enemy
    real_player_agility = player_agi / 1.15
    enemy_true_dodge_possibilities = (enemy_agility - .3) * 100
    enemy_false_dodge_possibilities = (real_player_agility - .3) * 100
    enemy_total_possibilities = enemy_true_dodge_possibilities + enemy_false_dodge_possibilities

    enemy_dodge_chance = round((enemy_true_dodge_possibilities / enemy_total_possibilities) * 100)
    av_dmg_diff = player_av_dmg - enemy_av_dmg

    # simulate fight 5 times to get stats
    count = 0
    player_turn = True
    player_fake_health = player_health_cap + player_hp
    player_fake_health_max = player_fake_health
    player_fake_agility = player["agility"]
    player_fake_armor_protection = player["armor protection"]
    player_fake_agility = player["agility"]
    player_critical_hit_chance = player["critical hit chance"]
    if player["held item"] != " ":
        player_fake_defend = item[player["held item"]]["defend"]
    else:
        player_fake_defend = 1
    enemy_fake_critical_hit_chance = enemy_critical_chance
    enemy_fake_health = enemy_health * enemies_number
    enemies_count = enemies_number
    player_deaths = 0
    enemy_deaths = 0
    while count < 65:
        someone_died = False
        # reset enemy health stats
        player_fake_health = player_health_cap + player_hp
        enemy_fake_health = enemy_health * enemies_number
        enemy_fake_health_duplicate = enemy_fake_health
        enemies_count = enemies_number

        # to fix infinite loops
        times_played = 0
        while not someone_died and times_played <= enemy_fake_health_duplicate * enemy_fake_health_duplicate:
            # to fix sometimes errors at line 187
            global enemy_dodged
            enemy_dodged = False
            while player_turn:
                # if player health is less than 45% and random formula, defend
                if player_fake_health > player_fake_health * (45 / 100) and round(random.uniform(.20, .60), 2) > .45:
                    defend = 0
                    defend += random.randint(int(player_fake_defend / 2), int(player_fake_defend)) * player_fake_agility
                    # defend formula
                    player_fake_health += defend
                    if player_fake_health > player_fake_health_max:
                        player_fake_health = player_fake_health_max
                # else, the player attack
                else:
                    # attack formula
                    enemy_dodged = False
                    player_critical_hit = False
                    if round(random.uniform(.30, enemy_agility), 2) > player_fake_agility / 1.15 and random.uniform(0, 1) > .65:
                        enemy_dodged = True
                    if player_critical_hit_chance > random.randint(0, 100):
                        player_critical_hit = True
                    if not enemy_dodged:
                        player_damage = round(random.uniform(0, int(player_av_dmg)) * player_damage_coefficient)
                        if player_critical_hit:
                            player_damage = player_damage * 2
                        enemy_fake_health -= player_damage

                # if the enemy's dead
                if enemy_fake_health <= 0:
                    if enemies_count <= 0:
                        someone_died = True
                        enemy_deaths += 1
                    else:
                        enemies_count -= 1
                        enemy_fake_health = enemy_health * enemies_number

                player_turn = False
            while not player_turn:
                # if enemy is still alive
                if enemy_health > 0:
                    damage = random.randint(
                        enemy_min_damage, enemy_max_damage
                    ) * enemies_damage_coefficient - player_fake_defend * (
                        player_fake_armor_protection * round(
                            random.uniform(.50, .90), 1
                        )
                    )
                    damage = round(damage)
                    defend = 0
                    player_dodged = False
                    enemy_critical_hit = False
                    enemy_critical_hit_chance = enemy_fake_critical_hit_chance
                    if enemy_critical_hit_chance > random.randint(0, 100):
                        enemy_critical_hit = True
                    elif round(random.uniform(.30, player_fake_agility), 2) > enemy_agility / 1.15 and random.uniform(0, 1) > .65:
                        player_dodged = True
                    if damage > 0 and not player_dodged:
                        if enemy_critical_hit:
                            damage = damage * 2
                        player_fake_health -= damage
                    player_turn = True

                # if the player's dead
                if player_fake_health <= 0:
                    someone_died = True
                    player_deaths += 1
            times_played += 1

        count += 1

    # compute percentage of defeat chance
    defeat_percentage = round(player_deaths * 100 / 65)

    if defeat_percentage >= 100:
        defeat_percentage = random.randint(89, 100)
    elif defeat_percentage <= 0:
        defeat_percentage = random.randint(5, 8)

    return defeat_percentage


def encounter_text_show(
    player, item, enemy, map, map_location, enemies_remaining, lists,
    defeat_percentage, preferences, drinks, npcs, zone, mounts, mission,
    start_player, dialog, text_replacements_generic, player_damage_coefficient,
    previous_player, save_file, start_time, enemies_damage_coefficient
):
    # import stats
    global turn, defend, fighting, already_encountered
    global enemy_singular, enemy_plural, enemy_max
    global enemy_health, enemy_max_damage, enemy_min_damage
    global enemy_agility, enemy_damage, chosen_item
    player_agility = player["agility"]
    cout(" ")  # do not merge with possible actions text
    # load and create enemies list type

    health_color = COLOR_GREEN
    enemies_number = enemies_remaining

    text = '='
    text_handling.print_separator(text)

    if enemies_number > 1:
        cout("You encounter a group of " + str(enemy_plural) + " that won't let you pass.")
    else:
        cout("You find " + text_handling.a_an_check(enemy_singular) + " on your way.")

    # player stats updates
    risk = defeat_percentage

    # display
    bars = 10
    remaining_risk_symbol = "█"
    lost_risk_symbol = "_"

    remaining_risk_bars = round(risk / 100 * bars)
    lost_risk_bars = bars - remaining_risk_bars

    # print HP stats and possible actions for the player

    if risk > .80 * 100:
        health_color = COLOR_RED
    elif risk > .60 * 100:
        health_color = COLOR_ORANGE_4
    elif risk > .45 * 100:
        health_color = COLOR_YELLOW
    elif risk > .30 * 100:
        health_color = COLOR_GREEN
    else:
        health_color = COLOR_STYLE_BRIGHT + COLOR_GREEN

    cout(f"RISK: {risk}%")
    cout(
        f"|{health_color}{remaining_risk_bars * remaining_risk_symbol}" +
        f"{lost_risk_bars * lost_risk_symbol}{COLOR_RESET_ALL}|"
    )

    cout("[R]un Away, [F]ight, [U]se Item? ")

    text = '='
    text_handling.print_separator(text)

    cout(" ")
    startup_action = cinput(COLOR_GREEN + COLOR_STYLE_BRIGHT + "> " + COLOR_RESET_ALL)
    cout("")

    text = '='
    text_handling.print_separator(text)

    if startup_action.lower().startswith('r'):
        # run away chance
        if player["agility"] / round(random.uniform(1.10, 1.25), 2) > enemy_agility:
            cout("You succeeded in running away from your enemy!")
            fighting = False
        else:
            text = "You failed in running away from your enemy! You now have to fight him/them!"
            text_handling.print_long_string(text)
            text = '='
            text_handling.print_separator(text)
            fighting = True
    elif startup_action.lower().startswith('f'):
        fighting = True
    elif startup_action.lower().startswith('u'):
        player_inventory_displayed = []
        count = 0
        for i in player["inventory"]:
            zeros = len(str(len(player["inventory"])))
            removed = len(str(count))
            player_inventory_displayed += [f"{"0" * (zeros - removed)}{count}> {i}"]
            count += 1
        cout("INVENTORY:")
        for line in player_inventory_displayed:
            cout(line)
        text = '='
        text_handling.print_separator(text)
        item_input = cinput(COLOR_GREEN + COLOR_STYLE_BRIGHT + "$ " + COLOR_RESET_ALL)
        error = False
        try:
            which_item_index = int(which_item)
            which_item = player["inventory"][which_item_index]
        except Exception as e:
            error = True
        if not error:  # use item
            item_handling.use_item(
                item_input, item, player, preferences, drinks,
                enemy, npcs, start_player, lists, zone, dialog, mission,
                mounts, text_replacements_generic, item, map_location,
                player_damage_coefficient, previous_player, save_file,
                start_time, enemies_damage_coefficient
            )
            text = '='
            text_handling.print_separator(text)
    else:
        cout("'" + startup_action + "' is not a valid option")
        fighting = True

    cout(" ")


def get_enemy_stats(
    player, item, enemy, map, map_location,
    lists, choose_rand_enemy, chosen_enemy,
    chosen_item, enemy_items_number,
    enemy_total_inventory, enemies_remaining
):
    global enemy_singular, enemy_plural, enemy_max, enemy_health
    global enemy_max_damage, enemy_min_damage, enemy_agility, enemy_damage
    # load enemy stat

    # enemy stats
    enemy_singular = choose_rand_enemy
    enemy_plural = chosen_enemy["plural"]
    enemy_max = chosen_enemy["health"]["max health level"]
    enemy_health = random.randint(chosen_enemy["health"]["min spawning health"], chosen_enemy["health"]["max spawning health"])
    enemy_max_damage = chosen_enemy["damage"]["max damage"]
    enemy_min_damage = chosen_enemy["damage"]["min damage"]
    enemy_critical_chance = chosen_enemy["damage"]["critical chance"]
    enemy_damage = 0
    enemy_agility = chosen_enemy["agility"]

    if choose_rand_enemy not in player["enemies list"]:
        player["enemies list"].append(choose_rand_enemy)


def fight(
    player, item, enemy, map, map_location, enemies_remaining, lists,
    preferences, drinks, npcs, start_player, zone, dialog, mission, mounts,
    player_damage_coefficient, start_time, text_replacements_generic,
    previous_player, save_file, enemies_damage_coefficient, defeat_percentage
):
    # import stats
    global turn, defend, fighting, already_encountered
    global enemy_singular, enemy_plural, enemy_max
    global enemy_health, enemy_max_damage, enemy_min_damage
    global enemy_agility, enemy_damage, chosen_item
    armor_protection = player["armor protection"]
    player_agility = player["agility"]
    # load and create enemies list type

    enemy_max_health = enemy_health

    critical_hit_chance = player["critical hit chance"]

    # while the player is still fighting (for run away)

    while fighting:
        # while player still alive
        # colors
        color_green = "\033[92m"
        color_yellow = "\33[33m"
        color_red = "\033[91m"
        color_blue = "\33[34m"
        color_default = "\033[0m"
        health_color = color_green
        health_color_enemy = color_blue

        while player["health"] > 0:
            # apply effects
            # All the checks for the player active effects
            # are done here
            #
            # If the player has any active effects, load
            # them one by one and update them depending
            # on their dictionary content and type
            player_damage_coefficient = 1
            if player["held item"] != " ":
                player["critical hit chance"] = item[player["held item"]]["critical hit chance"]
            else:
                player["critical hit chance"] = 0
            if player["active effects"] != {}:
                for i in list(player["active effects"]):
                    current_effect = player["active effects"][i]
                    effect_over = False
                    # Run the actions for every effect type
                    if current_effect["type"] == 'healing':
                        # Check if the effect duration's over
                        if (
                            (
                                current_effect["effect duration"] + current_effect["effect starting time"]
                            ) < player["elapsed time game days"]
                        ):
                            # Remove that effect from the player
                            # active effects and set the player
                            # modified stats to before the effect
                            # happened
                            player["active effects"].pop(i)
                            player["health"] = current_effect["before stats"]["health"]
                            player["max health"] = current_effect["before stats"]["max health"]
                            effect_over = True
                        # Check if the effect has already been
                        # applied or not
                        if not current_effect["already applied"] and not effect_over:
                            # Apply that effect changes now
                            if current_effect["effects"]["health changes"] >= 999:
                                player["health"] = player["max health"]
                            else:
                                player["health"] += current_effect["effects"]["health changes"]
                            player["max health"] += current_effect["effects"]["max health changes"]
                            player["active effects"][i]["already applied"] = True
                    elif current_effect["type"] == 'protection':
                        # Check if the effect duration's over
                        if (
                            (
                                current_effect["effect duration"] + current_effect["effect starting time"]
                            ) < player["elapsed time game days"] and current_effect["effect duration"] != 999
                        ):
                            # Remove that effect from the player
                            # active effects
                            player["active effects"].pop(i)
                            effect_over = True
                        # Apply the effect effects if the
                        # effect isn't over
                        if not effect_over:
                            player["armor protection"] = player["armor protection"] * current_effect[
                                "effects"
                            ]["protection coefficient"]
                    elif current_effect["type"] == 'strength':
                        # Check if the effect duration's over
                        if (
                            (
                                current_effect["effect duration"] + current_effect["effect starting time"]
                            ) < player["elapsed time game days"] and current_effect["effect duration"] != 999
                        ):
                            # Remove that effect from the player
                            # active effects
                            player["active effects"].pop(i)
                            effect_over = True
                        # Apply the effect effects if the
                        # effect isn't over
                        if not effect_over:
                            player["critical hit chance"] = player["critical hit chance"] * current_effect["effects"][
                                "critical hit chance coefficient"
                            ]
                            # If the player already has an effect that changes
                            # the damage coefficient and that's greater, don't
                            # apply the current effect coefficient
                            # = keep the greater one
                            if not player_damage_coefficient > current_effect["effects"]["damage coefficient"]:
                                player_damage_coefficient = current_effect["effects"]["damage coefficient"]
                    elif current_effect["type"] == 'agility':
                        # Check if the effect duration's over
                        if (
                            (
                                current_effect["effect duration"] + current_effect["effect starting time"]
                            ) < player["elapsed time game days"] and current_effect["effect duration"] != 999
                        ):
                            # Remove that effect from the player
                            # active effects
                            player["active effects"].pop(i)
                            effect_over = True
                        # Apply the effect effects if the
                        # effect isn't over
                        if not effect_over:
                            player["agility"] = player["agility"] * current_effect[
                                "effects"
                            ]["agility coefficient"]
            # player stats updates
            player_health = player["health"]
            player_max_health = player["max health"]

            text_handling.clear_prompt()
            # ui
            text_handling.print_separator('=')
            if enemies_remaining > 1:
                noun = f"{enemies_remaining} {enemy_plural}"
            else:
                noun = enemy_singular
            cout(f"Defeat the {noun}!")
            text_handling.print_separator('=')
            risk = defeat_percentage

            # display
            bars = 10
            remaining_risk_symbol = "█"
            lost_risk_symbol = "_"

            remaining_risk_bars = round(risk / 100 * bars)
            lost_risk_bars = bars - remaining_risk_bars

            # print HP stats and possible actions for the player

            if risk > .80 * 100:
                health_color = COLOR_RED
            elif risk > .60 * 100:
                health_color = COLOR_ORANGE_4
            elif risk > .45 * 100:
                health_color = COLOR_YELLOW
            elif risk > .30 * 100:
                health_color = COLOR_GREEN
            else:
                health_color = COLOR_STYLE_BRIGHT + COLOR_GREEN

            cout(
                f" BATTLE RISK: {risk}% " +
                f"|{health_color}{remaining_risk_bars * remaining_risk_symbol}" +
                f"{lost_risk_bars * lost_risk_symbol}{COLOR_RESET_ALL}|"
            )
            text_handling.print_separator('=')
            bars = 20
            remaining_health_symbol = "█"
            lost_health_symbol = "_"

            remaining_health_bars = round(player_health / player_max_health * bars)
            lost_health_bars = bars - remaining_health_bars

            if remaining_health_bars > 20:
                remaining_health_bars = 20

            remaining_health_bars_enemy = round(enemy_health / enemy_max_health * bars)
            lost_health_bars_enemy = bars - remaining_health_bars_enemy

            if remaining_health_bars_enemy > 20:
                remaining_health_bars_enemy = 20

            # print HP stats and possible actions for the player

            if player_health > .66 * player_max_health:
                health_color = color_green
            elif player_health > .33 * player_max_health:
                health_color = color_yellow
            else:
                health_color = color_red

            if enemy_health > .66 * enemy_max_health:
                health_color_enemy = color_blue
            elif enemy_health > .33 * enemy_max_health:
                health_color_enemy = COLOR_CYAN
            else:
                health_color_enemy = COLOR_MAGENTA

            cout(f"HEALTH of {enemy_singular}: {enemy_health} / {enemy_max_health}")
            cout(
                f"|{health_color_enemy}{remaining_health_bars_enemy * remaining_health_symbol}" +
                f"{lost_health_bars_enemy * lost_health_symbol}{color_default}|"
            )
            cout(f"HEALTH of {save_file.split('save_', 1)[1].replace('.yaml', '')}: {player_health} / {player_max_health}")
            cout(
                f"|{health_color}{remaining_health_bars * remaining_health_symbol}" +
                f"{lost_health_bars * lost_health_symbol}{color_default}|"
            )
            text_handling.print_separator('=')
            cout("  - [A]ttack")
            cout("  - [D]efend")
            cout("  - [U]se Item")
            text_handling.print_separator('=')
            cout("")
            global skip_attacks
            skip_attacks = False
            while turn:
                # display

                action = cinput(COLOR_GREEN + COLOR_STYLE_BRIGHT + "> " + COLOR_RESET_ALL)

                # if player attack
                if player["held item"] != " ":
                    player_damage = item[player["held item"]]["damage"]
                    player_defend = item[player["held item"]]["defend"]
                else:
                    player_damage = 1
                    player_defend = 1
                if action.lower().startswith('a'):
                    cout(" ")
                    # attack formula
                    global enemy_dodged
                    enemy_dodged = False
                    player_critical_hit = False
                    if round(random.uniform(.30, enemy_agility), 2) > player_agility / 1.15 and random.uniform(0, 1) > .65:
                        enemy_dodged = True
                        cout("Your enemy dodged your attack!")
                    if critical_hit_chance > random.randint(0, 100):
                        player_critical_hit = True
                        cout("You dealt a critical hit to your opponent!")
                    if not enemy_dodged:
                        player_damage = round(random.uniform(0, player_damage) * player_damage_coefficient)
                        if player_critical_hit:
                            player_damage = player_damage * 2
                        enemy_health -= player_damage
                        cout("You dealt " + str(player_damage) + " damage to your enemy.")
                    turn = False

                # if player defend
                elif action.lower().startswith('d'):
                    cout(" ")
                    defend += round(random.uniform(player_defend / 2, player_defend) * player_agility)
                    cout(f"You defended yourself and gained back {defend} health points")
                    # defend formula
                    player["health"] += defend
                    if player["health"] > player["max health"]:
                        player["health"] = player["max health"]
                    turn = False

                # if player use an item
                elif action.lower().startswith('u'):
                    cout("")
                    text_handling.print_separator('=')
                    player_inventory_displayed = []
                    count = 0
                    for i in player["inventory"]:
                        zeros = len(str(len(player["inventory"])))
                        removed = len(str(count))
                        player_inventory_displayed += [f"{"0" * (zeros - removed)}{count}> {i}"]
                        count += 1
                    cout("INVENTORY:")
                    for line in player_inventory_displayed:
                        cout(line)
                    text = '='
                    text_handling.print_separator(text)
                    item_input = cinput(COLOR_GREEN + COLOR_STYLE_BRIGHT + "$ " + COLOR_RESET_ALL)
                    error = False
                    try:
                        which_item_index = int(item_input)
                        which_item = player["inventory"][which_item_index]
                    except Exception as e:
                        error = True
                    if not error:  # use item
                        item_handling.use_item(
                            which_item, item, player, preferences, drinks,
                            enemy, npcs, start_player, lists, zone, dialog, mission,
                            mounts, text_replacements_generic, item, map_location,
                            player_damage_coefficient, previous_player, save_file,
                            start_time, enemies_damage_coefficient
                        )
                        text = '='
                        text_handling.print_separator(text)
                    turn = False
                    skip_attacks = True
                else:
                    cout("'" + action + "' is not a valid option")
                    cout(" ")
            # when it's not player turn
            while not turn:
                # if enemy is still alive
                if enemy_health > 0:
                    if not skip_attacks:
                        damage = random.randint(
                            enemy_min_damage, enemy_max_damage
                        ) * enemies_damage_coefficient - defend * (
                            armor_protection * round(random.uniform(.50, .90), 1)
                        )
                        damage = round(damage)
                        defend = 0
                        player_dodged = False
                        enemy_critical_hit = False
                        if critical_hit_chance > random.randint(0, 100):
                            enemy_critical_hit = True
                            cout("Your enemy dealt a critical hit!")
                        elif round(random.uniform(.30, player_agility), 2) > enemy_agility / 1.15 and random.uniform(0, 1) > .65:
                            player_dodged = True
                            cout("You dodged your enemy attack!")
                        if damage > 0 and not player_dodged:
                            if enemy_critical_hit:
                                damage = enemy_max_damage * 2
                            player["health"] -= damage
                            cout("The enemy dealt " + str(damage) + " points of damage.")
                        cout(" ")
                    turn = True
                else:
                    cout(" ")
                    # check if any health is negative
                    if player["health"] < 0:
                        player["health"] = 0
                    if enemy_health < 0:
                        enemy_health = 0
                    remaining_health_bars = round(player_health / player_max_health * bars)
                    lost_health_bars = bars - remaining_health_bars

                    if remaining_health_bars > 20:
                        remaining_health_bars = 20

                    remaining_health_bars_enemy = round(enemy_health / enemy_max_health * bars)
                    lost_health_bars_enemy = bars - remaining_health_bars_enemy

                    if remaining_health_bars_enemy > 20:
                        remaining_health_bars_enemy = 20

                    player["xp"] += enemy_max * enemy_max_damage / 3
                    if player["current mount"] in player["mounts"]:
                        player["mounts"][player["current mount"]]["level"] += round(random.uniform(.05, .20), 3)
                    player["health"] += random.randint(0, 3)
                    enemies_remaining -= 1
                    cout(f"You killed {text_handling.a_an_check(enemy_singular)}!")
                    time.sleep(2)
                    still_playing = False
                    turn = True
                    return
            time.sleep(2)
        return


still_playing = True
