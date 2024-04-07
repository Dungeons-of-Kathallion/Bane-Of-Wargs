import appdirs
import time
import text_handling
import terminal_handling
from colors import *
from terminal_handling import cout
from zone_handling import get_zone_color


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
