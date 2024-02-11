import time
import text_handling

def teleportation_action(player, map):
    print(" ")
    text_handling.print_separator("=")
    which_coordinates_x = int(input("Where would you like to be at x?\n"))
    which_coordinates_y = int(input("Where would you like to be at y?\n"))
    # Here we consider that the player will enter a correct input`, because this is an example

    # Check if a map point exists at player wish coordinates
    point_exists = False
    for i in list(map):
        if map[i]["x"] == which_coordinates_x and map[i]["y"] == which_coordinates_y:
            point_exists = True

    # Run the teleportation action
    if point_exists:
        print("Teleporting...")
        time.sleep(5)
        player["x"], player["y"] = which_coordinates_x, which_coordinates_y
        print("Teleported!")
    else:
        print(f"Where you want to go does not exists...")
    text_handling.print_separator("=")

player = None

# Actually run the action, and tells the game which arguments to use
teleportation_action(player, map)
