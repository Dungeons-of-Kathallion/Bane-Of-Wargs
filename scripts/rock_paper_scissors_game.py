import random
import terminal_handling.py
import text_handling
import colors
from colorama import Fore, Back, Style, init, deinit
from colors import *

# initialize colorama
init()

def print_action(action1, action2):

    if action1 == 'rock' and action2 == 'rock':
        print("""
            _______           _______
        ---'   ____)         (____   '---
              (_____)       (_____)
              (_____)       (_____)
              (____)         (____)
        ---.__(___)           (___)__.---
                   Rock VS Rock
        """)
    elif action1 == 'rock' and action2 == 'paper':
        print("""
            _______               _______
        ---'   ____)         ____(____   '----
              (_____)       (______
              (_____)       (_______
              (____)         (_______
        ---.__(___)             (_________.---
                   Rock VS Paper
        """)
    elif action1 == 'rock' and action2 == 'scissors':
        print("""
            _______                _______
        ---'   ____)          ____(____   '---
              (_____)        (______
              (_____)       (__________
              (____)              (____)
        ---.__(___)                (___)__.---
                   Rock VS Scissors
        """)
    elif action1 == 'paper' and action2 == 'rock':
        print("""
             _______                 _______
        ---'    ____)____           (____   '---
                   ______)         (_____)
                  _______)         (_____)
                 _______)           (____)
        ---.__________)              (___)__.---
                        Paper VS Rock
        """)
    elif action1 == 'paper' and action2 == 'paper':
        print("""
             _______                     _______
        ---'    ____)____           ____(____   '----
                   ______)         (______
                  _______)         (_______
                 _______)           (_______
        ---.__________)                (_________.---
                        Paper VS Paper
        """)
    elif action1 == 'paper' and action2 == 'scissors':
        print("""
             _______                      _______
        ---'    ____)____            ____(____   '---
                   ______)          (______
                  _______)         (__________
                 _______)                (____)
        ---.__________)                   (___)__.---
                        Paper VS Scissors
        """)
    elif action1 == 'scissors' and action2 == 'rock':
        print("""
            _______                 _______
        ---'   ____)____           (____   '---
                  ______)         (_____)
               __________)        (_____)
              (____)               (____)
        ---.__(___)                 (___)__.---
                     Scissors vs Rock
        """)
    elif action1 == 'scissors' and action2 == 'paper':
        print("""
            _______                     _______
        ---'   ____)____           ____(____   '----
                  ______)         (______
               __________)        (_______
              (____)               (_______
        ---.__(___)                   (_________.---
                     Scissors vs Paper
        """)
    elif action1 == 'scissors' and action2 == 'scissors':
        print("""
            _______                      _______
        ---'   ____)____            ____(____   '---
                  ______)          (______
               __________)        (__________
              (____)                    (____)
        ---.__(___)                      (___)__.---
                     Scissors vs Scissors
        """)


def rock_paper_scissors():
    print(" ")
    text_handling.print_separator("=")
    print("How many rounds?")
    rounds = [3, 4, 6, 8, 12]
    rounds_number = terminal_handling.py.show_menu(rounds)

    player_wins = 0
    ai_wins = 0
    ties = 0

    for count in range(0, rounds_number):
        actions = ['rock', 'paper', 'scissors']
        action = terminal_handling.py.show_menu(actions)

        ai_action = actions[random.randint(0, 2)]

        print('\033[38;2;244;164;96m')
        print_action(action, ai_action)
        print(COLOR_RESET_ALL)

        if action == ai_action:
            ties += 1
            print(f"{COLOR_STYLE_BRIGHT}Tie !{COLOR_RESET_ALL}")
        elif action == 'rock' and ai_action == 'paper':
            ai_wins += 1
            print(f"{COLOR_STYLE_BRIGHT}AI wins !{COLOR_RESET_ALL}")
        elif action == 'rock' and ai_action == 'scissors':
            player_wins += 1
            print(f"{COLOR_STYLE_BRIGHT}Player wins !{COLOR_RESET_ALL}")
        elif action == 'paper' and ai_action == 'rock':
            player_wins += 1
            print(f"{COLOR_STYLE_BRIGHT}Player wins !{COLOR_RESET_ALL}")
        elif action == 'paper' and ai_action == 'scissors':
            ai_wins += 1
            print(f"{COLOR_STYLE_BRIGHT}AI wins !{COLOR_RESET_ALL}")
        elif action == 'scissors' and ai_action == 'rock':
            ai_wins += 1
            print(f"{COLOR_STYLE_BRIGHT}AI wins !{COLOR_RESET_ALL}")
        elif action == 'scissors' and ai_action == 'paper':
            player_wins += 1
            print(f"{COLOR_STYLE_BRIGHT}Player wins !{COLOR_RESET_ALL}")

    print("")
    if player_wins > ai_wins:
        print(f"{COLOR_GREEN}WINNER: {COLOR_BLUE}Player{COLOR_RESET_ALL}")
    elif ai_wins > player_wins:
        print(f"{COLOR_GREEN}WINNER: {COLOR_RED}AI{COLOR_RESET_ALL}")
    else:
        print(f"{COLOR_GREEN}WINNER: {COLOR_CYAN}Tie Game !{COLOR_RESET_ALL}")
    print("")
    print(f"{COLOR_GREEN}Player Wins: {COLOR_MAGENTA}{player_wins}{COLOR_RESET_ALL}")
    print(f"{COLOR_GREEN}AI Wins: {COLOR_MAGENTA}{ai_wins}{COLOR_RESET_ALL}")
    print(f"{COLOR_CYAN}Ties: {COLOR_MAGENTA}{ties}{COLOR_RESET_ALL}")
    text_handling.print_separator("=")


# Actually run the action, and tells the game which arguments to use
rock_paper_scissors()

# deinitialize colorama
deinit()
