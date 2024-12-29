# palace_of_drought.py
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

import time
import random
import text_handling
import terminal_handling
from colors import *
from terminal_handling import cout, cinput

def run(preferences):
    # NOTE //
    # Hieroglyphs design made by Sanne Jabs under GPL-3+

    # Create a list containing all the dialogs of the scene
    texts = [
        "You decide to take a step to the first room. The entrance has closed upon your entry and it seems there's no issue, other than finishing the dungeon. You start wondering if entering this dungeon was a foolish idea.",
        "Suddenly, you hear the sound of torches lighting up, all by themselves. As light is shedded upon the room, you can see strange hieroglyphs, foreign to you. There is what seems to be a door made out of different rocks out in front. You seek for a way to open it, but no button, lever or handle may be seen. Finally, you find some old book on the ground. You open it, and go through the pages until you see a page where you find the same kind of hieroglyphs that are on the walls of the room.",
        "Why not try understanding the sentence written?",
        """
        ,-----------------------------------------------------------------v
        u           ,-~~\\   <~)_   u\\             /\\    ,-.       ,-.     u
        u  _,===-.,  (   \\   ( v~\\ u u  _,===-.,  \\/   <,- \\_____/  `     <
        u (______,.   u\\. \\   \\_/'  \\u (______,. /__\\    /  ___. \\  -===- u
        >            _a_a`\\\\  /\\     u           \\--/ ,_(__/ ,_(__\\       u
        `-----------------------------------------------------------------y
        """,
        """

        ==============================
         _,===-.,
        (______,.

        ------------------------------
         _ ___  _
        / \\\\  \\//
        | | \\  /
        | | /  \\
        \\_//__/\\

        ___  _
        \\  \\//
         \\  /
         / /
        /_/
        ==============================
        ,-~~\\
         (   \\
          u\\. \\
         _a_a`\\\\

        ------------------------------
         _
        / \\  /|
        | |\\ ||
        | | \\||
        \\_/  \\|

         _
        / \\__/|
        | |\\/||
        | |  ||
        \\_/  \\|
        ==============================
        <~)_
         ( v~\\
          \\_/'
          /\\

        ------------------------------
         ____
        /  _ \\
        | / \\|
        | |-||
        \\_/ \\|
        ==============================
        u\\
        u u
         \\u
          u

        ------------------------------
        ___  _
        \\  \\//
         \\  /
         / /
        /_/

         ____
        /_   \\
         /   /
        /   /_
        \\____/
        ==============================
         /\\
         \\/
        /__\\
        \\--/

        ------------------------------
         _____  ____
        /__ __\\/  _ \\
          / \\  | / \\|
          | |  | \\_/|
          \\_/  \\____/

         _____ ____  ____
        /    //  _ \\/  __\\
        |  __\\| / \\||  \\/|
        | |   | \\_/||    /
        \\_/   \\____/\\_/\\_\\
        ==============================
          ,-.       ,-.
         <,- \\_____/  `
           /  ___. \\
        ,_(__/ ,_(__\\

        ------------------------------
         _____ _     _____
        /  __// \\   /    /
        |  \\  | |   |  __\\
        |  /_ | |_/\\| |
        \\____\\\\____/\\_/

         ____  ____  _      _      _____ ____
        /  _ \\/  _ \\/ \\__/|/ \\  /|/  __//  _ \\
        | | \\|| / \\|| |\\/||| |\\ |||  \\  | | \\|
        | |_/|| |-||| |  ||| | \\|||  /_ | |_/|
        \\____/\\_/ \\|\\_/  \\|\\_/  \\|\\____\\\\____/
        ==============================
        -===-

        ------------------------------
         ____
        / ___\\
        |    \\
        \\___ |
        \\____/
        ==============================
        """,
        "You've now successfully translated the hieroglyphs written over the door on the walls. You say it out loud: 'Ixnay to Elfs?'. You don't have time to wonder what it can mean that the doors start squeaking and opening, all by themselves. It seems that what you translated was the password to the dungeon. You now have nothing else to do but entering room 2 of the dungeon..."
    ]

    # Print the first dialogs, with a timing between them
    text_handling.print_speech_text_effect(texts[0], preferences)
    time.sleep(2)
    text_handling.print_speech_text_effect(texts[1], preferences)
    time.sleep(2)
    text_handling.print_speech_text_effect(texts[2], preferences)
    time.sleep(3)

    # Take the hieroglyphs ASCII art scene and edit it
    # to add colors and line breaks.
    enigma_solved = False
    text = list(texts[3] + "\n" + texts[4] + "\n")
    count = 0
    for character in text:
        if random.randint(0, 100) > 85:
            text[count] = character + "$TAN"
            if random.randint(0, 100) > 50:
                text[count] = character + "$WHITE"
        count += 1
    text_final = ""
    for i in text:
        text_final = text_final + str(i)

    # The loop for the enigma. Ends when it's solved.
    while not enigma_solved:
        text_handling.clear_prompt()

        cout(text_handling.apply_yaml_data_color_code(text_final + COLOR_RESET_ALL))

        translation = cinput("TRANSLATION : ")

        if translation.lower() == "ixnay to elfs":
            cout(COLOR_BLUE + "You successfully translated the hieroglyphs!" + COLOR_RESET_ALL)
            time.sleep(2)
            text_handling.clear_prompt()
            enigma_solved = True
        else:
            cout(COLOR_RED + "You successfully messed up in translating the hieroglyphs!" + COLOR_RESET_ALL)
            time.sleep(2)

    # Now that the player's solved the enigma, continue the dialog
    text_handling.print_speech_text_effect(texts[5], preferences)
    time.sleep(3)

# Actually run the action, and tells the game which arguments to use
run(preferences)
