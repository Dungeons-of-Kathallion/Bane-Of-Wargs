import yaml
import random
import os
import sys
import time
import term_menu
import text_handling
from colors import *
from colorama import Fore, Back, Style, init, deinit

# initialize colorama
init()

# battle stats
defend = 0
turn = True
fighting = True


def calculate_player_risk(player, item, enemies_remaining, chosen_enemy, enemy):
    # get all stats
    player_hp = player["health"]
    player_agi = player["agility"]
    player_prot = player["armor protection"]
    player_av_dmg = round(
        (
            (
                item[player["held item"]]["damage"] + 1 + item[player["held item"]]["damage"]
            ) * item[player["held item"]]["critical hit chance"] * 2.3
        ) / 2, 2
    )
    player_def = item[player["held item"]]["defend"]
    player_critic_ch = item[player["held item"]]["critical hit chance"]
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

        if item[selected_item]["type"] == "Food" or item[selected_item]["type"] == "Consumable":
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

    '''
    print("HP DIFF:", hp_diff)
    print("AVERAGE DMG DIFF:", av_dmg_diff)
    print("ENEMY DODGE CHANCE:", enemy_dodge_chance)
    print("PLAYER DODGE CHANCE:", player_dodge_chance)
    '''

    # simulate fight 5 times to get stats
    count = 0
    player_turn = True
    player_fake_health = player_health_cap + player_hp
    player_fake_health_max = player_fake_health
    player_fake_agility = player["agility"]
    player_fake_armor_protection = player["armor protection"]
    player_fake_agility = player["agility"]
    player_critical_hit_chance = item[player["held item"]]["critical hit chance"]
    player_fake_defend = item[player["held item"]]["defend"]
    enemy_fake_critical_hit_chance = enemy_critical_chance
    enemy_fake_health = enemy_health * enemies_number
    enemies_count = enemies_number
    player_deaths = 0
    enemy_deaths = 0
    while count < 5:
        someone_died = False
        # reset enemy health stats
        player_fake_health = player_health_cap + player_hp
        enemy_fake_health = enemy_health * enemies_number
        enemies_count = enemies_number

        while not someone_died:
            # to fix sometimes errors at line 187
            global enemy_dodged
            enemy_dodged = False
            while player_turn:
                # if player health is less than 45% and random formula, defend
                if player_fake_health > player_fake_health * (45 / 100) and round(random.uniform(.20, .60), 2) > .45:
                    defend = 0
                    defend += random.randint(0, int(item[player["held item"]]["defend"])) * player_fake_agility
                    # defend formula
                    player_fake_health += random.randint(0, 3)
                    if player_fake_health > player_fake_health_max:
                        player_fake_health = player_fake_health_max
                # else, the player attack
                else:
                    # attack formula
                    enemy_dodged = False
                    player_critical_hit = False
                    player_critical_hit_chance = round(
                        player_critical_hit_chance / random.uniform(
                            .03, player_critical_hit_chance * 2.8
                        ), 2
                    )
                    if round(random.uniform(.30, enemy_agility), 2) > player_fake_agility / 1.15:
                        enemy_dodged = True
                    if player_critical_hit_chance / random.uniform(.20, .35) < player_critical_hit_chance and not enemy_dodged:
                        player_critical_hit = True
                    if not enemy_dodged:
                        player_damage = random.randint(1, int(item[player["held item"]]["damage"]))
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
                    damage = random.randint(enemy_min_damage, enemy_max_damage) - player_fake_defend * (
                        player_fake_armor_protection * round(
                            random.uniform(.50, .90), 1
                        )
                    )
                    damage = round(damage)
                    defend = 0
                    player_dodged = False
                    enemy_critical_hit = False
                    enemy_critical_hit_chance = round(
                        enemy_fake_critical_hit_chance / random.uniform(
                            .03, enemy_fake_critical_hit_chance * 2.8
                        ), 2
                    )
                    critical_hit_chance_formula = round(
                        enemy_critical_hit_chance / random.uniform(
                            .03, enemy_critical_hit_chance * 2.8
                        ), 2
                    )
                    if enemy_critical_hit_chance / random.uniform(.20, .35) < critical_hit_chance_formula and not enemy_dodged:
                        enemy_critical_hit = True
                    elif round(random.uniform(.30, enemy_agility), 2) > enemy_agility / 1.15:
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

        count += 1

    # compute percentage of defeat chance
    defeat_percentage = round(player_deaths * 100 / 5)

    if defeat_percentage > 100:
        defeat_percentage = 100
    elif defeat_percentage <= 0:
        defeat_percentage = random.randint(5, 15)

    return defeat_percentage


def encounter_text_show(player, item, enemy, map, map_location, enemies_remaining, lists, defeat_percentage):
    # import stats
    global turn, defend, fighting, already_encountered
    global enemy_singular, enemy_plural, enemy_max
    global enemy_health, enemy_max_damage, enemy_min_damage
    global enemy_agility, enemy_damage, chosen_item
    player_agility = player["agility"]
    print(" ")  # do not merge with possible actions text
    # load and create enemies list type

    health_color = COLOR_GREEN
    enemies_number = enemies_remaining

    text = '='
    text_handling.print_separator(text)

    if enemies_number > 1:
        print("You encounter a group of " + str(enemy_plural) + " that won't let you pass.")
    else:
        print("You find a/an " + str(enemy_singular) + " on your way.")

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
        health_color = COLOR_STYLE_BRIGHT + COLOR_RED
    elif risk > .60 * 100:
        health_color = COLOR_RED
    elif risk > .45 * 100:
        health_color = COLOR_YELLOW
    elif risk > .30 * 100:
        health_color = COLOR_GREEN
    else:
        health_color = COLOR_STYLE_BRIGHT + COLOR_GREEN

    sys.stdout.write(f"RISK: {risk}% \n")
    sys.stdout.write(
        f"|{health_color}{
            remaining_risk_bars * remaining_risk_symbol
        }{lost_risk_bars * lost_risk_symbol}{COLOR_RESET_ALL}|\n"
    )
    sys.stdout.flush()

    print("[R]un Away, [F]ight, [U]se Item? ")

    text = '='
    text_handling.print_separator(text)

    print(" ")
    startup_action = input(COLOR_GREEN + COLOR_STYLE_BRIGHT + "> " + COLOR_RESET_ALL)
    print("")

    text = '='
    text_handling.print_separator(text)

    if startup_action.lower().startswith('r'):
        # run away chance
        if player["agility"] / round(random.uniform(1.10, 1.25), 2) > enemy_agility:
            print("You succeeded in running away from your enemy!")
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
        player_inventory = str(player["inventory"])
        player_inventory = player_inventory.replace("'", '')
        player_inventory = player_inventory.replace("[", ' -')
        player_inventory = player_inventory.replace("]", '')
        player_inventory = player_inventory.replace(", ", '\n -')
        print("INVENTORY:")
        print(player_inventory)
        item_input = input(COLOR_GREEN + COLOR_STYLE_BRIGHT + "> " + COLOR_RESET_ALL)
        # use item
        if item_input in player["inventory"]:
            if item[item_input]["type"] == "Consumable" or item[item_input]["type"] == "Food":
                if item[item_input]["healing level"] == 999:
                    player["health"] = player["max health"]
                else:
                    player["health"] += item[item_input]["healing level"]
                player["max health"] += item[item_input]["max bonus"]
                player["inventory"].remove(item_input)
            # hold weapon/armor piece if it is one
            if item_input in player["inventory"] and item[item_input]["type"] == "Weapon":
                player["held item"] = item_input
                print("You are now holding a/an ", player["held item"])
            elif item_input in player["inventory"] and item[item_input]["type"] == "Armor Piece: Chestplate":
                player["held chestplate"] = item_input
                print("You are now wearing a/an ", player["held chestplate"])
            elif item_input in player["inventory"] and item[item_input]["type"] == "Armor Piece: Leggings":
                player["held leggings"] = item_input
                print("You are now wearing a/an ", player["held leggings"])
            elif item_input in player["inventory"] and item[item_input]["type"] == "Armor Piece: Boots":
                player["held boots"] = item_input
                print("You are now wearing a/an ", player["held boots"])
            elif item_input in player["inventory"] and item[item_input]["type"] == "Armor Piece: Shield":
                player["held shield"] = item_input
                print("You are now holding a/an ", player["held shield"])
            text = '='
            text_handling.print_separator(text)
    else:
        print("'" + startup_action + "' is not a valid option")
        fighting = True

    print(" ")


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


def fight(player, item, enemy, map, map_location, enemies_remaining, lists):
    # import stats
    global turn, defend, fighting, already_encountered
    global enemy_singular, enemy_plural, enemy_max
    global enemy_health, enemy_max_damage, enemy_min_damage
    global enemy_agility, enemy_damage, chosen_item
    armor_protection = player["armor protection"]
    player_agility = player["agility"]
    # load and create enemies list type

    enemy_max_health = enemy_health

    critical_hit_chance = item[player["held item"]]["critical hit chance"]

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
            while turn:
                # player stats updates
                player_health = player["health"]
                player_max_health = player["max health"]

                # display
                bars = 20
                remaining_health_symbol = "█"
                lost_health_symbol = "_"

                remaining_health_bars = round(player_health / player_max_health * bars)
                lost_health_bars = bars - remaining_health_bars

                remaining_health_bars_enemy = round(enemy_health / enemy_max_health * bars)
                lost_health_bars_enemy = bars - remaining_health_bars_enemy

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

                sys.stdout.write(f"PLAYER: {player_health} / {player_max_health}\n")
                sys.stdout.write(
                    f"|{health_color}{
                        remaining_health_bars * remaining_health_symbol
                    }{lost_health_bars * lost_health_symbol}{color_default}|\n"
                )
                sys.stdout.write(f"ENEMY: {enemy_health} / {enemy_max_health}\n")
                sys.stdout.write(
                    f"|{health_color_enemy}{
                        remaining_health_bars_enemy * remaining_health_symbol
                    }{lost_health_bars_enemy * lost_health_symbol}{color_default}|"
                )
                sys.stdout.flush()

                action = input("\n[A]ttack, [D]efend, [U]se Item? ")

                # if player attack
                if action.lower().startswith('a'):
                    print(" ")
                    # attack formula
                    global enemy_dodged
                    enemy_dodged = False
                    player_critical_hit = False
                    critical_hit_chance_formula = round(critical_hit_chance / random.uniform(.03, critical_hit_chance * 2.8), 2)
                    if round(random.uniform(.30, enemy_agility), 2) > player_agility / 1.15:
                        enemy_dodged = True
                        print("Your enemy dodged your attack!")
                    if critical_hit_chance / random.uniform(.20, .35) < critical_hit_chance_formula and not enemy_dodged:
                        player_critical_hit = True
                        print("You dealt a critical hit to your opponent!")
                    if not enemy_dodged:
                        player_damage = random.randint(1, int(item[player["held item"]]["damage"]))
                        if player_critical_hit:
                            player_damage = player_damage * 2
                        enemy_health -= player_damage
                        print("You dealt " + str(player_damage) + " damage to your enemy.")
                    turn = False

                # if player defend
                elif action.lower().startswith('d'):
                    print(" ")
                    defend += random.randint(0, int(item[player["held item"]]["defend"])) * player_agility
                    # defend formula
                    player["health"] += random.randint(0, 3)
                    if player["health"] > player["max health"]:
                        player["health"] = player["max health"]
                    turn = False

                # if player use an item
                elif action.lower().startswith('u'):
                    player_inventory = str(player["inventory"])
                    player_inventory = player_inventory.replace("'", '')
                    player_inventory = player_inventory.replace("[", ' -')
                    player_inventory = player_inventory.replace("]", '')
                    player_inventory = player_inventory.replace(", ", '\n -')
                    print(" ")
                    text = '='
                    text_handling.print_separator(text)
                    print("INVENTORY:")
                    print(player_inventory)
                    item_input = input(COLOR_GREEN + COLOR_STYLE_BRIGHT + "> " + COLOR_RESET_ALL)
                    # use item
                    if item_input in player["inventory"]:
                        if item[item_input]["type"] == "Consumable" or item[item_input]["type"] == "Food":
                            if item[item_input]["healing level"] == 999:
                                player["health"] = player["max health"]
                            else:
                                player["health"] += item[item_input]["healing level"]
                            player["max health"] += item[item_input]["max bonus"]
                            player["inventory"].remove(item_input)
                        # hold weapon/armor piece if it is one
                        if item_input in player["inventory"] and item[item_input]["type"] == "Weapon":
                            player["held item"] = item_input
                            print("You are now holding a/an ", player["held item"])
                        elif item_input in player["inventory"] and item[item_input]["type"] == "Armor Piece: Chestplate":
                            player["held chestplate"] = item_input
                            print("You are now wearing a/an ", player["held chestplate"])
                        elif item_input in player["inventory"] and item[item_input]["type"] == "Armor Piece: Leggings":
                            player["held leggings"] = item_input
                            print("You are now wearing a/an ", player["held leggings"])
                        elif item_input in player["inventory"] and item[item_input]["type"] == "Armor Piece: Boots":
                            player["held boots"] = item_input
                            print("You are now wearing a/an ", player["held boots"])
                        elif item_input in player["inventory"] and item[item_input]["type"] == "Armor Piece: Shield":
                            player["held shield"] = item_input
                            print("You are now holding a/an ", player["held shield"])
                        text = '='
                        text_handling.print_separator(text)
                        print(" ")
                else:
                    print("'" + action + "' is not a valid option")
                    print(" ")
            # when it's not player turn
            while not turn:
                # if enemy is still alive
                if enemy_health > 0:
                    damage = random.randint(
                        enemy_min_damage, enemy_max_damage
                    ) - defend * (
                        armor_protection * round(random.uniform(.50, .90), 1)
                    )
                    damage = round(damage)
                    defend = 0
                    player_dodged = False
                    enemy_critical_hit = False
                    critical_hit_chance_formula = round(critical_hit_chance / random.uniform(.03, critical_hit_chance * 2.8), 2)
                    if critical_hit_chance / random.uniform(.20, .35) < critical_hit_chance_formula and not enemy_dodged:
                        enemy_critical_hit = True
                        print("Your enemy dealt a critical hit!")
                    elif round(random.uniform(.30, player_agility), 2) > enemy_agility / 1.15:
                        player_dodged = True
                        print("You dodged your enemy attack!")
                    if damage > 0 and not player_dodged:
                        if enemy_critical_hit:
                            damage = damage * 2
                        player["health"] -= damage
                        print("The enemy dealt ", str(damage), " points of damage.")
                    print(" ")
                    turn = True
                else:
                    print(" ")
                    # check if any health is negative
                    if player["health"] < 0:
                        player["health"] = 0
                    if enemy_health < 0:
                        enemy_health = 0
                    remaining_health_bars = round(player_health / player_max_health * bars)
                    lost_health_bars = bars - remaining_health_bars

                    remaining_health_bars_enemy = round(enemy_health / enemy_max_health * bars)
                    lost_health_bars_enemy = bars - remaining_health_bars_enemy
                    sys.stdout.write(f"PLAYER: {player_health} / {player_max_health}\n")
                    sys.stdout.write(f"|{health_color}{
                        remaining_health_bars * remaining_health_symbol
                    }{
                        lost_health_bars * lost_health_symbol
                    }{color_default}|\n")
                    sys.stdout.write(f"ENEMY: {enemy_health} / {enemy_max_health}\n")
                    sys.stdout.write(f"|{health_color_enemy}{
                        remaining_health_bars_enemy * remaining_health_symbol
                    }{
                        lost_health_bars_enemy * lost_health_symbol
                    }{color_default}|")
                    sys.stdout.flush()
                    print("\n")
                    player["xp"] += enemy_max * enemy_max_damage / 3
                    if player["current mount"] in player["mounts"]:
                        player["mounts"][player["current mount"]]["level"] += round(random.uniform(.05, .20), 3)
                    player["health"] += random.randint(0, 3)
                    enemies_remaining -= 1
                    still_playing = False
                    return
        return

still_playing = True

# deinitialize colorama
deinit()
