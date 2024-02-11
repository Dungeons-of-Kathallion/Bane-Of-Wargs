import random
import text_handling
import colors
from colorama import Fore, Back, Style, init, deinit
from colors import *

# initialize colorama
init()

def dialog_action(player):
    print(" ")
    text_handling.print_separator("=")
    how_many_exp = float(input("How many exp would you like to spend?\n"))
    # Here we consider that the player will enter a correct input`, because this is an example

    # First, check that the player has the experience that he said, then
    # if the player has enough experience, we
    if player["xp"] < how_many_exp:
        print(COLOR_YELLOW + "You don't have enough experience for this action!" + COLOR_RESET_ALL)
    else:
        player["xp"] -= how_many_exp
        health_regeneration = round(how_many_exp / round(random.uniform(2.8, 4.3), 2))
        player["health"] += health_regeneration

    text_handling.print_separator("=")

# Actually run the action, and tells the game which arguments to use
dialog_action(player)

# deinitialize colorama
deinit()
