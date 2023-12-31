import colors
import yaml
import appdirs
from colorama import Fore, Back, Style, deinit, init
from colors import *

# initialize colorama
init()


def print_map(player, map, zone):
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
    for n in range(0, 16383):
        if coord_x == 65:
            coord_x = -64
            coord_y -= 1
            print("║")
        if coord_x == -64:
            print("║", end="")
        if coord_x == player_x and coord_y == player_y:
            print(COLOR_CYAN + COLOR_STYLE_BRIGHT + "¿" + COLOR_RESET_ALL, end="")
        else:
            print_color = COLOR_BLACK + '░'
            get_zone = True
            try:
                current_point = search_point(coord_x, coord_y, map_points_num, map)
            except:
                get_zone = False
            if get_zone and current_point not in current_point_list:
                print_color = get_zone_color(zone[map["point" + str(current_point)]["map zone"]]["type"])
            print(print_color + COLOR_RESET_ALL, end="")
            if get_zone:
                current_point_list += [current_point]
        coord_x += 1
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
                zone_color = COLOR_GREEN + COLOR_STYLE_BRIGHT + '█'
            elif zone_code == 1:
                zone_color = COLOR_GREEN + COLOR_STYLE_BRIGHT + '█'
            elif zone_code == 2:
                zone_color = COLOR_GREEN + '█'
            elif zone_code == 3:
                zone_color = COLOR_GREEN + COLOR_STYLE_DIM + '█'
            elif zone_code == 4:
                zone_color = "\033[1;30;40m" + '█'
            elif zone_code == 5:
                zone_color = "\033[1;30;40m" + COLOR_STYLE_DIM + '█'
            elif zone_code == 6:
                zone_color = "\033[1;30;40m" + COLOR_STYLE_BRIGHT + '█'
            elif zone_code == 7:
                zone_color = "\033[0;30;47m" + COLOR_STYLE_DIM + '█'
            elif zone_code == 8:
                zone_color = "\033[1;33;40m" + '█'
            elif zone_code == 9:
                zone_color = "\033[1;33;40m" + '█'
            elif zone_code == 10:
                zone_color = "\033[1;33;40m" + COLOR_STYLE_DIM + '█'
            elif zone_code == 11:
                zone_color = "\033[33m" + COLOR_STYLE_DIM + '█'
            elif zone_code == 12:
                zone_color = "\033[33m" + COLOR_STYLE_DIM + '█'
            elif zone_code == 13:
                zone_color = "\033[33m" + COLOR_STYLE_DIM + '█'
            elif zone_code == 14:
                zone_color = "\033[33m" + COLOR_STYLE_DIM + '█'
            elif zone_code == 15:
                zone_color = "\033[33m" + COLOR_STYLE_DIM + '█'
            elif zone_code == 16:
                zone_color = "\033[33m" + COLOR_STYLE_DIM + '█'
            elif zone_code == 17:
                zone_color = "\033[33m" + COLOR_STYLE_DIM + '█'
            elif zone_code == 18:
                zone_color = COLOR_MAGENTA + '█'
            elif zone_code == 19:
                zone_color = COLOR_YELLOW + COLOR_STYLE_BRIGHT + '█'
            elif zone_code == 20:
                zone_color = COLOR_GREEN + COLOR_STYLE_DIM + '█'
            elif zone_code == 21:
                zone_color = COLOR_YELLOW + COLOR_STYLE_DIM + '█'
            elif zone_code == 22:
                zone_color = zone_color = "\033[0;30;47m" + COLOR_STYLE_DIM + '█'
            elif zone_code == 23:
                zone_color = "\033[0;30;47m" + COLOR_STYLE_DIM + '█'
            elif zone_code == 24:
                zone_color = COLOR_BLUE + '▓'
            elif zone_code == 25:
                zone_color = COLOR_BLUE + '▒'
            elif zone_code == 26:
                zone_color = COLOR_BLUE + '▒'
            elif zone_code == 27:
                zone_color = COLOR_BLUE + '▒'
            elif zone_code == 28:
                zone_color = COLOR_BLUE + '▒'
            elif zone_code == 28:
                zone_color = COLOR_BLUE + '▒'
    except Exception as error:
        print(COLOR_RED + "ERROR: " + COLOR_STYLE_BRIGHT + f"zone type '{zone_type}' is not a valid zone type." + COLOR_RESET_ALL)
        print(error)
        exit(1)
    return zone_color

# function to search through the map file
def search_point(x, y, map_points_num, map):
    global map_location
    for i in range(0, map_points_num):
        point_i = map["point" + str(i)]
        if point_i["x"] == x and point_i["y"] == y:
            map_location = i
    return map_location
