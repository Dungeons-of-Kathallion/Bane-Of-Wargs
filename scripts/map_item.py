import yaml
import appdirs
import time
import text_handling
import terminal_handling
from colors import *
from terminal_handling import cout


def print_map_xs(player, map, zone, start_time):
    map_printing_starting_time = time.time()

    # Get the player near points with a 8x8 range
    player_already_printed = False
    start_point = [player["x"], player["y"]]
    to_print_points = [start_point]
    count = 0
    x_to_remove = -4
    y_to_remove = 4
    cout("╔", end="")
    while count <= 7:
        cout("═", end="")
        count += 1
    cout("╗")
    current_point_list = []
    for i in range(64):
        if x_to_remove == 4:
            x_to_remove = -4
            y_to_remove -= 1
            cout("║")
        if x_to_remove == -4:
            cout("║", end="")
        current_point = search_point(player["x"] + x_to_remove, player["y"] + y_to_remove, len(map), map)
        if current_point is not None:
            current_point_data = map[f"point{current_point}"]
            to_print_points += [[current_point_data["x"], current_point_data["y"]]]
        if not player_already_printed and current_point == search_point(player["x"], player["y"], len(map), map):
            cout(COLOR_CYAN + COLOR_STYLE_BRIGHT + "¶" + COLOR_RESET_ALL, end="")
            player_already_printed = True
        else:
            print_color = COLOR_BLACK + '?'
            try:
                if current_point not in current_point_list:
                    print_color = get_zone_color(zone[map["point" + str(current_point)]["map zone"]]["type"])
            except Exception as error:
                pass
            cout(print_color + COLOR_RESET_ALL, end="")
            current_point_list += [current_point]

        x_to_remove += 1
        count += 1

    cout("║")
    cout("╚", end="")
    count = 0
    while count <= 7:
        cout("═", end="")
        count += 1
    cout("╝")

    map_printing_starting_ending_time = time.time()
    start_time -= map_printing_starting_ending_time - map_printing_starting_time


def print_map_s(player, map, zone, start_time):
    map_printing_starting_time = time.time()

    # Get the player near points with a 16x16 range
    player_already_printed = False
    start_point = [player["x"], player["y"]]
    to_print_points = [start_point]
    count = 0
    x_to_remove = -8
    y_to_remove = 8
    cout("╔", end="")
    while count <= 15:
        cout("═", end="")
        count += 1
    cout("╗")
    current_point_list = []
    for i in range(256):
        if x_to_remove == 8:
            x_to_remove = -8
            y_to_remove -= 1
            cout("║")
        if x_to_remove == -8:
            cout("║", end="")
        current_point = search_point(player["x"] + x_to_remove, player["y"] + y_to_remove, len(map), map)
        if current_point is not None:
            current_point_data = map[f"point{current_point}"]
            to_print_points += [[current_point_data["x"], current_point_data["y"]]]
        if not player_already_printed and current_point == search_point(player["x"], player["y"], len(map), map):
            cout(COLOR_CYAN + COLOR_STYLE_BRIGHT + "¶" + COLOR_RESET_ALL, end="")
            player_already_printed = True
        else:
            print_color = COLOR_BLACK + '?'
            try:
                if current_point not in current_point_list:
                    print_color = get_zone_color(zone[map["point" + str(current_point)]["map zone"]]["type"])
            except Exception as error:
                pass
            cout(print_color + COLOR_RESET_ALL, end="")
            current_point_list += [current_point]

        x_to_remove += 1
        count += 1

    cout("║")
    cout("╚", end="")
    count = 0
    while count <= 15:
        cout("═", end="")
        count += 1
    cout("╝")

    map_printing_starting_ending_time = time.time()
    start_time -= map_printing_starting_ending_time - map_printing_starting_time


def print_map_m(player, map, zone, start_time):
    map_printing_starting_time = time.time()

    # Get the player near points with a 32x32 range
    player_already_printed = False
    start_point = [player["x"], player["y"]]
    to_print_points = [start_point]
    count = 0
    x_to_remove = -16
    y_to_remove = 16
    cout("╔", end="")
    while count <= 31:
        cout("═", end="")
        count += 1
    cout("╗")
    current_point_list = []
    for i in range(1024):
        if x_to_remove == 16:
            x_to_remove = -16
            y_to_remove -= 1
            cout("║")
        if x_to_remove == -16:
            cout("║", end="")
        current_point = search_point(player["x"] + x_to_remove, player["y"] + y_to_remove, len(map), map)
        if current_point is not None:
            current_point_data = map[f"point{current_point}"]
            to_print_points += [[current_point_data["x"], current_point_data["y"]]]
        if not player_already_printed and current_point == search_point(player["x"], player["y"], len(map), map):
            cout(COLOR_CYAN + COLOR_STYLE_BRIGHT + "¶" + COLOR_RESET_ALL, end="")
            player_already_printed = True
        else:
            print_color = COLOR_BLACK + '?'
            try:
                if current_point not in current_point_list:
                    print_color = get_zone_color(zone[map["point" + str(current_point)]["map zone"]]["type"])
            except Exception as error:
                pass
            cout(print_color + COLOR_RESET_ALL, end="")
            current_point_list += [current_point]

        x_to_remove += 1
        count += 1

    cout("║")
    cout("╚", end="")
    count = 0
    while count <= 31:
        cout("═", end="")
        count += 1
    cout("╝")

    map_printing_starting_ending_time = time.time()
    start_time -= map_printing_starting_ending_time - map_printing_starting_time


def print_map_l(player, map, zone, start_time):
    map_printing_starting_time = time.time()

    # Get the player near points with a 64x64 range
    player_already_printed = False
    start_point = [player["x"], player["y"]]
    to_print_points = [start_point]
    count = 0
    x_to_remove = -32
    y_to_remove = 32
    cout("╔", end="")
    while count <= 63:
        cout("═", end="")
        count += 1
    cout("╗")
    current_point_list = []
    for i in range(4096):
        if x_to_remove == 32:
            x_to_remove = -32
            y_to_remove -= 1
            cout("║")
        if x_to_remove == -32:
            cout("║", end="")
        current_point = search_point(player["x"] + x_to_remove, player["y"] + y_to_remove, len(map), map)
        if current_point is not None:
            current_point_data = map[f"point{current_point}"]
            to_print_points += [[current_point_data["x"], current_point_data["y"]]]
        if not player_already_printed and current_point == search_point(player["x"], player["y"], len(map), map):
            cout(COLOR_CYAN + COLOR_STYLE_BRIGHT + "¶" + COLOR_RESET_ALL, end="")
            player_already_printed = True
        else:
            print_color = COLOR_BLACK + '?'
            try:
                if current_point not in current_point_list:
                    print_color = get_zone_color(zone[map["point" + str(current_point)]["map zone"]]["type"])
            except Exception as error:
                pass
            cout(print_color + COLOR_RESET_ALL, end="")
            current_point_list += [current_point]

        x_to_remove += 1
        count += 1

    cout("║")
    cout("╚", end="")
    count = 0
    while count <= 63:
        cout("═", end="")
        count += 1
    cout("╝")

    map_printing_starting_ending_time = time.time()
    start_time -= map_printing_starting_ending_time - map_printing_starting_time


def print_full_map(player, map, zone, start_time):
    map_printing_starting_time = time.time()
    player_already_printed = False
    player_x = player["x"]
    player_y = player["y"]
    map_points = list(map)
    map_points_num = len(map_points)
    count = 0
    cout("╔", end="")
    while count <= 128:
        cout("═", end="")
        count += 1
    cout("╗")
    coord_x = -64
    coord_y = 64
    current_point_list = []
    counting = 0
    while counting < 16383:
        if coord_x > 64:
            coord_x = -64
            coord_y -= 1
            cout("║")
        if coord_x < -63:
            cout("║", end="")
        if not player_already_printed and coord_x == player_x and coord_y == player_y:
            cout(COLOR_CYAN + COLOR_STYLE_BRIGHT + "¶" + COLOR_RESET_ALL, end="")
            player_already_printed = True
        else:
            print_color = COLOR_BLACK + '░'
            get_zone = True
            current_point = search_point(coord_x, coord_y, map_points_num, map)
            if current_point == None:
                get_zone = False
            if get_zone and current_point not in current_point_list:
                print_color = get_zone_color(zone[map["point" + str(current_point)]["map zone"]]["type"])
            cout(print_color + COLOR_RESET_ALL, end="")
            if get_zone:
                current_point_list += [current_point]
        coord_x += 1
        counting += 1
    cout("║")
    cout("╚", end="")
    count = 0
    while count <= 128:
        cout("═", end="")
        count += 1
    cout("╝")
    map_printing_starting_ending_time = time.time()
    start_time -= map_printing_starting_ending_time - map_printing_starting_time


def get_zone_color(zone_type):
    program_dir = str(appdirs.user_config_dir(appname='Bane-Of-Wargs'))
    global zone_color
    zone_color = COLOR_BLACK
    try:
        with open(program_dir + '/game/schemas/zones_colors.yaml', 'r') as f:
            zones_colors = yaml.safe_load(f)
            zone_code = zones_colors[str(zone_type)]
            if zone_code == 0:
                zone_color = COLOR_GREENS_4 + '╬'
            elif zone_code == 1:
                zone_color = COLOR_GREENS_5 + '╬'
            elif zone_code == 2:
                zone_color = COLOR_GREEN + '╬'
            elif zone_code == 3:
                zone_color = COLOR_GREENS_12 + '╬'
            elif zone_code == 4:
                zone_color = COLOR_GREENS_2 + '↟'
            elif zone_code == 5:
                zone_color = COLOR_GREENS_1 + '⇞'
            elif zone_code == 6:
                zone_color = COLOR_GRAY_4 + '▲'
            elif zone_code == 7:
                zone_color = COLOR_GRAY_5 + '▲'
            elif zone_code == 8:
                zone_color = COLOR_GRAY_3 + '▲'
            elif zone_code == 9:
                zone_color = COLOR_GRAY_1 + '▲'
            elif zone_code == 10:
                zone_color = COLOR_YELLOW_6 + '≡'
            elif zone_code == 11:
                zone_color = COLOR_YELLOW_7 + '≡'
            elif zone_code == 12:
                zone_color = COLOR_YELLOW_7 + '≡'
            elif zone_code == 13:
                zone_color = COLOR_ORANGE_5 + '≡'
            elif zone_code == 14:
                zone_color = COLOR_ORANGE_3 + '≡'
            elif zone_code == 15:
                zone_color = COLOR_ORANGE_4 + '≡'
            elif zone_code == 16:
                zone_color = COLOR_ORANGE_4 + '≡'
            elif zone_code == 17:
                zone_color = COLOR_ORANGE_6 + '≡'
            elif zone_code == 18:
                zone_color = COLOR_ORANGE_6 + '≡'
            elif zone_code == 19:
                zone_color = COLOR_ORANGE_7 + '≡'
            elif zone_code == 20:
                zone_color = COLOR_MAGENTA_7 + '#'
            elif zone_code == 21:
                zone_color = COLOR_YELLOW_8 + '≡'
            elif zone_code == 22:
                zone_color = COLOR_GREENS_20 + '«'
            elif zone_code == 23:
                zone_color = COLOR_YELLOW_3 + '«'
            elif zone_code == 24:
                zone_color = COLOR_RED_1 + '«'
            elif zone_code == 25:
                zone_color = COLOR_RED_0 + '«'
            elif zone_code == 26:
                zone_color = COLOR_BLUE_5 + '⌂'
            elif zone_code == 27:
                zone_color = COLOR_BLUE_13 + '⌂'
            elif zone_code == 28:
                zone_color = COLOR_BLUE_13 + '⟰'
            elif zone_code == 29:
                zone_color = COLOR_BLUE_13 + '⟰'
            elif zone_code == 30:
                zone_color = COLOR_BLUE_13 + '⥣'
            elif zone_code == 31:
                zone_color = COLOR_BLUE_13 + '⤊'
            elif zone_code == 32:
                zone_color = COLOR_BLUE_13 + '±'
            elif zone_code == 33:
                zone_color = COLOR_CYAN_3 + '≈'
            elif zone_code == 34:
                zone_color = COLOR_CYAN_1 + '≈'
            elif zone_code == 35:
                zone_color = COLOR_GREENS_0 + '#'
            elif zone_code == 36:
                zone_color = COLOR_BLUE_13 + '⟰'
            elif zone_code == 37:
                zone_color = COLOR_BLUE_14 + '⇭'
    except Exception as error:
        cout(COLOR_RED + "ERROR: " + COLOR_STYLE_BRIGHT + f"zone type '{zone_type}' is not a valid zone type." + COLOR_RESET_ALL)
        cout(error)
        text_handling.exit_game()
    return zone_color


# function to search through the map file
def search_point(x, y, map_points_num, map):
    map_location = None
    counting2 = 0
    found_map_point = False
    while counting2 < map_points_num and not found_map_point:
        point_i = map["point" + str(counting2)]
        if point_i["x"] == x and point_i["y"] == y:
            map_location = str(counting2)
            found_map_point = True
        counting2 += 1
    return map_location


def run(player, map, zone, start_time):
    choices = ['8x8', '16x16', '32x32', '64x64', 'full (128x128)']
    choice = terminal_handling.show_menu(choices, length=19)
    cout("")
    if choice == choices[0]:
        print_map_xs(player, map, zone, start_time)
    if choice == choices[1]:
        print_map_s(player, map, zone, start_time)
    if choice == choices[2]:
        print_map_m(player, map, zone, start_time)
    if choice == choices[3]:
        print_map_l(player, map, zone, start_time)
    if choice == choices[4]:
        print_full_map(player, map, zone, start_time)


# run the script
run(player, map, zone, start_time)
