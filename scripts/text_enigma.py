import random
import time
import text_handling
from colors import *
from terminal_handling import cout, cinput


def run(zone):
    completed = False

    finished_sentence = True
    sentence = zone[
        list(zone)[random.randint(0, len(list(zone)) - 1)]
    ]["description"]
    time_limit = (sentence.count("") - 1)
    sentence_randomzed = sentence.split(" ")
    random.shuffle(sentence_randomzed)
    sentence_randomzed_str = ""
    for word in sentence_randomzed:
        sentence_randomzed_str += word + "; "

    while not completed:
        text_handling.clear_prompt()
        cout("Reconstitute the following phrase:")
        cout(sentence_randomzed_str)
        starting_time = time.time()
        player_sentece = cinput(f"\n> {COLOR_STYLE_DIM}")
        ending_time = time.time()
        cout(COLOR_RESET_ALL)
        
        if player_sentece == sentence and (ending_time - starting_time) <= time_limit:
            cout(COLOR_CYAN + "Good job! You've reconstituted the sentence!" + COLOR_RESET_ALL)
            completed = True
            return completed
        elif (ending_time - starting_time) > time_limit:
            cout(COLOR_YELLOW + "Too slow! Try again!" + COLOR_RESET_ALL)
            time.sleep(2.5)
        else:
            cout(COLOR_YELLOW + "This isn't the right sentence! Try again!" + COLOR_RESET_ALL)
            time.sleep(2.5)


# Actually run the action, and tells the game which arguments to use
run(zone)
