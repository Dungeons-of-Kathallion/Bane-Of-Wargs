# text_enigma.py
# Copyright (c) 2024 by @Cromha
#
# Bane Of Wargs is free software: you can redistribute it and/or modify it under the
# terms of the GNU General Public License as published by the Free Software
# Foundation, either version 3 of the License, or (at your option) any later version.
#
# Bane Of Wargs is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
# PARTICULAR PURPOSE. See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with
# this program. If not, see <https://www.gnu.org/licenses/>.

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
    ]["description"].replace('\n', '')
    sentence_randomzed = sentence.split(" ")
    random.shuffle(sentence_randomzed)
    sentence_randomzed_str = ""
    for word in sentence_randomzed:
        sentence_randomzed_str += word + "; "

    while not completed:
        text_handling.clear_prompt()
        cout("Reconstitute the following phrase:")
        cout(sentence_randomzed_str)
        player_sentence = cinput(f"\n> {COLOR_STYLE_DIM}").replace('\n', '')
        cout(COLOR_RESET_ALL)

        if player_sentence == sentence:
            cout(COLOR_CYAN + "Good job! You've reconstituted the sentence!" + COLOR_RESET_ALL)
            completed = True
            return completed
        else:
            cout(COLOR_YELLOW + "This isn't the right sentence! Try again!" + COLOR_RESET_ALL)

            hint_sentence = ""
            count = 0
            for word in sentence:
                if count > len(player_sentence) - 1:
                    hint_sentence += f"{COLOR_STYLE_DIM}_{COLOR_RESET_ALL}"
                elif word == player_sentence[count]:
                    hint_sentence += f"{COLOR_GREEN}{word}{COLOR_RESET_ALL}"
                elif word != player_sentence[count]:
                    hint_sentence += f"{COLOR_RED}{player_sentence[count]}{COLOR_RESET_ALL}"
                else:
                    hint_sentence += f"{COLOR_STYLE_DIM}_{COLOR_RESET_ALL}"
                count += 1
            cout("Hint: " + hint_sentence)
            time.sleep(2.5)


# Actually run the action, and tells the game which arguments to use
run(zone)
