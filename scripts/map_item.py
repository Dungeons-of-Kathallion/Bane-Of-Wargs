import colors
import yaml
import appdirs
import text_handling
from colorama import Fore, Back, Style, deinit, init
from colors import *

# initialize colorama
init()


def print_map(player, map, zone):
    player_already_printed = False
    player_x = player["x"]
    player_y = player["y"]
    map_points = list(map)
    map_points_num = len(map_points)
    count = 0
    print("╔", end="")
    while count <= 128:
        print("═", end="")
        count += 1
    print("╗")
    coord_x = -64
    coord_y = 64
    current_point_list = []
    counting = 0
    while counting < 16383:
        if coord_x > 64:
            coord_x = -64
            coord_y -= 1
            print("║")
        if coord_x < -63:
            print("║", end="")
        if not player_already_printed and coord_x == player_x and coord_y == player_y:
            print(COLOR_CYAN + COLOR_STYLE_BRIGHT + "¶" + COLOR_RESET_ALL, end="")
            player_already_printed = True
        else:
            print_color = COLOR_BLACK + '░'
            get_zone = True
            try:
                current_point = search_point(coord_x, coord_y, map_points_num, map)
            except Exception as error:
                get_zone = False
            if get_zone and current_point not in current_point_list:
                print_color = get_zone_color(zone[map["point" + str(current_point)]["map zone"]]["type"])
            print(print_color + COLOR_RESET_ALL, end="")
            if get_zone:
                current_point_list += [current_point]
        coord_x += 1
        counting += 1
    print("║")
    print("╚", end="")
    count = 0
    while count <= 128:
        print("═", end="")
        count += 1
    print("╝")


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
    except Exception as error:
        print(COLOR_RED + "ERROR: " + COLOR_STYLE_BRIGHT + f"zone type '{zone_type}' is not a valid zone type." + COLOR_RESET_ALL)
        print(error)
        text_handling.exit_game()
    return zone_color


# function to search through the map file
def search_point(x, y, map_points_num, map):
    global map_location
    counting2 = 0
    found_map_point = False
    while counting2 < map_points_num and not found_map_point:
        point_i = map["point" + str(counting2)]
        if point_i["x"] == x and point_i["y"] == y:
            map_location = str(counting2)
            found_map_point = True
        counting2 += 1
    return map_location

# run the script
print_map(player, map, zone)
