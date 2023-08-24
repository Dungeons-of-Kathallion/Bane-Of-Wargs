import yaml
import random
import os
import sys
import time
import enquiries
from colors import *
from colorama import Fore, Back, Style, init, deinit

# initialize colorama
init()

# battle stats
defend = 0
turn = True
fighting = True

def print_long_string(text):
    new_input = ""
    for i, letter in enumerate(text):
        if i % 54 == 0:
            new_input += '\n'
        new_input += letter

    # this is just because at the beginning too a `\n` character gets added
    new_input = new_input[1:]
    print(str(new_input))

def print_separator(character):
    count = 0

    while count < 55:
        sys.stdout.write(COLOR_STYLE_BRIGHT + character + COLOR_RESET_ALL)
        sys.stdout.flush()
        count += 1
    sys.stdout.write('\n')

def encounter_text_show(player, item, enemy, map, map_location, enemies_remaining, lists):
    # import stats
    global turn, defend, fighting, already_encountered
    global enemy_singular, enemy_plural, enemy_max, enemy_health, enemy_max_damage, enemy_min_damage, enemy_agility, enemy_damage, choosen_item
    player_agility = player["agility"]
    print(" ") # do not merge with possible actions text
    # load and create enemies list type

    enemies_number = enemies_remaining

    text = '='
    print_separator(text)

    if enemies_number > 1:
        print("You encounter a group of " + str(enemy_plural) + " that won't let you pass.")
    else:
        print("You find a/an " + str(enemy_singular) + " on your way.")

    print("[R]un Away, [F]ight, [U]se Item? ")

    text = '='
    print_separator(text)

    print(" ")
    startup_action = input("> ")
    print("")

    text = '='
    print_separator(text)

    if startup_action.lower().startswith('r'):
        # run away chance
        if player["agility"] / round(random.uniform(1.10, 1.25), 2) > enemy_agility:
            print("You succeeded in running away from your enemy!")
            fighting = False
        else:
            text = "You failed in running away from your enemy! You now have to fight him/them!"
            print_long_string(text)
            text = '='
            print_separator(text)
            fighting = True
    elif startup_action.lower().startswith('f'):
            pass
    elif startup_action.lower().startswith('u'):
        player_inventory = str(player["inventory"])
        player_inventory = player_inventory.replace("'", '')
        player_inventory = player_inventory.replace("[", ' -')
        player_inventory = player_inventory.replace("]", '')
        player_inventory = player_inventory.replace(", ", '\n -')
        print("INVENTORY:")
        print(player_inventory)
        item_input = input("> ")
        # use item
        if item_input in player["inventory"]:
            if item[item_input]["type"] == "Consumable" or item[item_input]["type"] == "Food":
                if item[item_input]["healing level"] == "max health":
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
            elif item_input in player["inventory"] and item[item_input]["type"] == "Armor Piece: Sheild":
                player["held shield"] = item_input
                print("You are now holding a/an ", player["held shield"])
            text = '='
            print_separator(text)
    else:
        print("'" + startup_action + "' is not a valid option")


    print(" ")

def get_enemy_stats(player, item, enemy, map, map_location, lists, choose_rand_enemy, choosen_enemy, choosen_item, enemy_items_number, enemy_total_inventory):
    global enemy_singular, enemy_plural, enemy_max, enemy_health, enemy_max_damage, enemy_min_damage, enemy_agility, enemy_damage
    # load enemy stat

    # enemy stats
    enemy_singular = choose_rand_enemy
    enemy_plural = choosen_enemy["plural"]
    enemy_max = choosen_enemy["health"]["max health level"]
    enemy_health = random.randint(choosen_enemy["health"]["min spawning health"], choosen_enemy["health"]["max spawning health"])
    enemy_max_damage = choosen_enemy["damage"]["max damage"]
    enemy_min_damage = choosen_enemy["damage"]["min damage"]
    enemy_damage = 0
    enemy_agility = choosen_enemy["agility"]

    if choose_rand_enemy not in player["enemies list"]:
        player["enemies list"].append(choose_rand_enemy)

def fight(player, item, enemy, map, map_location, enemies_remaining, lists):
    # import stats
    global turn, defend, fighting, already_encountered
    global enemy_singular, enemy_plural, enemy_max, enemy_health, enemy_max_damage, enemy_min_damage, enemy_agility, enemy_damage, choosen_item
    armor_protection = player["armor protection"]
    player_agility = player["agility"]
    # load and create enemies list type

    enemies_number = map["point" + str(map_location)]["enemy"]

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

                if player_health > 0.66 * player_max_health:
                    health_color = color_green
                elif player_health > 0.33 * player_max_health:
                    health_color = color_yellow
                else:
                    health_color = color_red

                if enemy_health > 0.66 * enemy_max_health:
                    health_color_enemy = color_blue
                elif enemy_health > 0.33 * enemy_max_health:
                    health_color_enemy = COLOR_CYAN
                else:
                    health_color_enemy = COLOR_MAGENTA

                sys.stdout.write(f"PLAYER: {player_health} / {player_max_health}\n")
                sys.stdout.write(f"|{health_color}{remaining_health_bars * remaining_health_symbol}{lost_health_bars * lost_health_symbol}{color_default}|\n")
                sys.stdout.write(f"ENEMY: {enemy_health} / {enemy_max_health}\n")
                sys.stdout.write(f"|{health_color_enemy}{remaining_health_bars_enemy * remaining_health_symbol}{lost_health_bars_enemy * lost_health_symbol}{color_default}|")
                sys.stdout.flush()

                action = input("\n[A]ttack, [D]efend, [U]se Item? ")

                # if player attack
                if action.lower().startswith('a'):
                    print(" ")
                    # attack formula
                    enemy_dodged = False
                    player_critical_hit = False
                    enemy_dodge_chance = round(random.uniform(0.10, enemy_agility), 2)
                    critical_hit_chance_formula = round(critical_hit_chance / random.uniform(0.03, critical_hit_chance * 2.8), 2)
                    if enemy_dodge_chance > round(random.uniform(.50, .90), 2):
                        enemy_dodged = True
                        print("Your enemy dodged your attack!")
                    if critical_hit_chance / random.uniform(.20, .35) < critical_hit_chance_formula:
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
                    print_separator(text)
                    print("INVENTORY:")
                    print(player_inventory)
                    item_input = input("> ")
                    # use item
                    if item_input in player["inventory"]:
                        if item[item_input]["type"] == "Consumable" or item[item_input]["type"] == "Food":
                            if item[item_input]["healing level"] == "max health":
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
                        elif item_input in player["inventory"] and item[item_input]["type"] == "Armor Piece: Sheild":
                            player["held shield"] = item_input
                            print("You are now holding a/an ", player["held shield"])
                        text = '='
                        print_separator(text)
                        print(" ")
                else:
                    print("'" + action + "' is not a valid option")
                    print(" ")
            # when it's not player turn
            while not turn:
                # if enemy is still alive
                if enemy_health > 0:
                    damage = random.randint(enemy_min_damage, enemy_max_damage) - defend * ( armor_protection * round(random.uniform(0.50, 0.90), 1) )
                    damage = round(damage)
                    defend = 0
                    player_dodged = False
                    player_dodge_chance = round(random.uniform(0.10, player_agility), 2)
                    if player_dodge_chance > round(random.uniform(.50, .90), 2):
                        player_dodged = True
                        print("You dodged your enemy attack!")
                    if damage > 0 and not player_dodged:
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
                    sys.stdout.write(f"|{health_color}{remaining_health_bars * remaining_health_symbol}{lost_health_bars * lost_health_symbol}{color_default}|\n")
                    sys.stdout.write(f"ENEMY: {enemy_health} / {enemy_max_health}\n")
                    sys.stdout.write(f"|{health_color_enemy}{remaining_health_bars_enemy * remaining_health_symbol}{lost_health_bars_enemy * lost_health_symbol}{color_default}|")
                    sys.stdout.flush()
                    print("\n")
                    player["xp"] += enemy_max * enemy_max_damage / 3
                    player["health"] += random.randint(0, 3)
                    enemies_remaining -= 1
                    still_playing = False
                    return
        return



still_playing = True

# deinitialize colorama
deinit()
