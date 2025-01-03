- [battle.py](#battlepy)
- [camp.py](#camppy)
- [check\_yaml.py](#check_yamlpy)
- [colors.py](#colorspy)
- [consumable\_handling.py](#consumable_handlingpy)
- [data\_handling.py](#data_handlingpy)
- [dialog\_handling.py](#dialog_handlingpy)
- [dungeon.py](#dungeonpy)
- [enemy\_handling.py](#enemy_handlingpy)
- [event\_handling.py](#event_handlingpy)
- [fishing.py](#fishingpy)
- [item\_handling.py](#item_handlingpy)
- [logger\_sys.py](#logger_syspy)
- [main.py](#mainpy)
- [mission\_handling.py](#mission_handlingpy)
- [npc\_handling.py](#npc_handlingpy)
- [player\_handling.py](#player_handlingpy)
- [script\_handling.py](#script_handlingpy)
- [terminal\_handling.py](#terminal_handlingpy)
- [text\_handling.py](#text_handlingpy)
- [time\_handling.py](#time_handlingpy)
- [train.py](#trainpy)
- [uuid\_handling.py](#uuid_handlingpy)
- [weapon\_upgrade\_handling.py](#weapon_upgrade_handlingpy)
- [yaml\_handling.py](#yaml_handlingpy)
- [zone\_handling.py](#zone_handlingpy)

_Note that it's recommended to check each wiki page, before reading this document, as it's advanced in the game engine documentation._
_https://github.com/Dungeons-of-Kathallion/Bane-Of-Wargs/wiki_

## battle.py

The [`battle.py`](https://github.com/Dungeons-of-Kathallion/Bane-Of-Wargs/blob/master/source/battle.py) class handles all of the game combat UI. Here are all of its functions (_Note that you should use the [enemy_handling.py](#enemy_handlingpy) class to make enemy spawn instead of battle.py_):

| Name                    | Arguments                                                                                                                                                                                                                                                                                                                                                                     | Description                                                                                            |
|-------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------|
| calculate_player_risk() | `player`, `item`, `enemies_remaining`, `chosen_enemy`, `enemy`, `player_damage_coefficient`, `enemies_damage_coefficient`                                                                                                                                                                                                                                                     | Simulate a fight with `enemies_remaining` `enemy` enemies, to return the risk percentage of the player |
| encounter_text_show()   | `player`, `item`, `enemy`, `map`, `map_location`, `enemies_remaining`, `lists`, `defeat_percentage`, `preferences`, `drinks`, `npcs`, `zone`, `mounts`, `mission`, `start_player`, `dialog`, `text_replacements_generic`, `player_damage_coefficient`, `previous_player`, `save_file`, `start_time`, `enemies_damage_coefficient`, `entry_data`, `enemies`, `no_run_away`=False | Displays the encountering text of enemy pool list `entry_data`                                          |
| fight()                 | `player`, `item`, `enemy`, `map`, `map_location`, `enemies_remaining`, `lists`, `preferences`, `drinks`, `npcs`, `start_player`, `zone`, `dialog`, `mission`, `mounts`, `player_damage_coefficient`, `start_time`, `text_replacements_generic`,  `previous_player`, `save_file`, `enemies_damage_coefficient`, `defeat_percentage`, `entry_data`, `enemies`                   | Starts fight of enemy pool list `entry_data`                                                            |

## camp.py

The [`camp.py`](https://github.com/Dungeons-of-Kathallion/Bane-Of-Wargs/blob/master/source/camp.py) class handles all of the game camping UI. Here are all of its functions:

| Name                    | Arguments                                                                                                                                                                                                                                                                                                                                                                     | Description                                                                                            |
|-------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------|
| camp_loop() | `player`, `save_file`, `map_zone`, `zone`, `time_elapsing_coefficient` | Ignites the camping loop UI. `map_zone` is the id of the player's current map zone. |

## check_yaml.py

The [`check_yaml.py`](https://github.com/Dungeons-of-Kathallion/Bane-Of-Wargs/blob/master/source/check_yaml.py) class won't be a class you'll use for custom scripting, as it contains the functions to run tests on the loaded game data. But if you're interested in contributing, you might want to check out the class yourself and analyze it.

## colors.py

The [`colors.py`](https://github.com/Dungeons-of-Kathallion/Bane-Of-Wargs/blob/master/source/colors.py) class is a database of color codes; used for colored terminal input. Just check the class if you need a color code you're searching for.

## consumable_handling.py

The [`consumable_handling.py`](https://github.com/Dungeons-of-Kathallion/Bane-Of-Wargs/blob/master/source/consumable_handling.py) class contains a set of function that generates the effect of consumables, or print its effects to the console. There are many small functions, so we're only gonna go over the three main ones you have a chance to ever use:

| Name                       | Arguments                                                                                                                                                                                                                                                                                                               | Description                                                                                                                                                                          |
|----------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| consume_consumable()       | `item_data`, `consumable_name`, `player`, `dialog`, `preferences`, `text_replacements_generic`, `lists`, `map_location`, `enemy`, `item`, `drinks`, `start_player`, `npcs`, `zone`, `mounts`, `mission`, `player_damage_coefficient`, `previous_player`, `save_file`, `map`, `start_time`, `enemies_damage_coefficient` | Consume consumable `consumable_name`                                                                                                                                                 |
| print_consumable_effects() | `current_effect_type`, `current_effect_data`                                                                                                                                                                                                                                                                            | Outputs to the console the visible effects of effect `current_effect_data` of type `current_effect_type` (display percentages instead of meaning numbers of print_consumable_effects) |
| print_active_effect_info() | `effect_data`, `player`                                                                                                                                                                                                                                                                                                 | Prints the effects of a visible effect `effect_data`, on the `player` (display meaning numbers instead of percentages of print_consumable_effects)                                    |

## data_handling.py

The [`data_handling.py`](https://github.com/Dungeons-of-Kathallion/Bane-Of-Wargs/blob/master/source/data_handling.py) class contains functions to load the game data, and to download stuff from online locations, using [fsspec](https://pypi.org/project/fsspec/). Here are all the functions:

| Name                          | Arguments                                                                              | Description                                                                                                                                                                                                                                                                               |
|-------------------------------|----------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| load_game_data()              | `which_type`, `preferences`                                                            | Determines which game data to load and from where, and load it (and analyze it if the preferences 'analyze' option is set to enabled). Returns every game data variables: `map`, `item`, `drinks`, `enemy`, `npcs`, `start_player`, `lists`, `zone`, `dialog`, `mission`, `mounts`, `event` |
| update_game_data()            | `preferences`, `latest_game_data_version`                                              | Redownloads the game vanilla data at '{bow-folder}/game/', from latest game data version                                                                                                                                                                                                   |
| fsspec_download()             | `github_file`, `destination_point`, `download_branch`, `download_repo`, `download_org` | Downloads a file from path `github_file` to destination path `destination_point`, from github account `donload_org`, repo `download_repo`, and branch/tag `download_branch`                                                                                                                |
| temporary_git_file_download() | `selected_file`, `url`                                                                 | Downloads a file from path `selected_file` from github url `url`, in a created temporary folder, and return the data of the file in a string                                                                                                                                               |
| wget_download() | `url`                                                                 | Downloads url `url` contents and returns it in a string                                                                                                                                               |
| open_file()                   | `file_path`                                                                            | Opens file from path `file_path` with default user terminal editor                                                                                                                                                                                                                         |

## dialog_handling.py

The [`dialog_handling.py`](https://github.com/Dungeons-of-Kathallion/Bane-Of-Wargs/blob/master/source/dialog_handling.py) class contains function to load dialog and their conversations. The only function you need to know about is the one to trigger a dialog:

| Name           | Arguments                                                                                                                                                                                                                           | Description                                                                                                                             |
|----------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------|
| print_dialog() | `current_dialog`, `dialog`, `preferences`, `text_replacements_generic`, `player`, `drinks`, `item`, `enemy`, `npcs`, `start_player`, `lists`, `zone`, `mission`, `mounts`, `start_time`, `map`, `save_file`, `player_damage_coefficient`, `enemies_damage_coefficient`, `previous_player`, `mission_offered`=None | Triggers dialog `current_dialog`. Specify a mission id at `mission_offered` if you want conversation actions like 'accept()' to be ran |

## dungeon.py

The [`dungeon.py`](https://github.com/Dungeons-of-Kathallion/Bane-Of-Wargs/blob/master/source/dungeon.py) class handles the dungeon UI. It only contains one function, one that starts the dungeon loop:

| Name           | Arguments                                                                                                                                                                                                                                                                                                              | Description                                         |
|----------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-----------------------------------------------------|
| dungeon_loop() | `player`, `current_dungeon`, `lists`, `enemy`, `start_player`, `item`, `start_time`, `preferences`, `npcs`, `drinks`, `zone`, `mounts`, `dialog`, `mission`, `map_location`, `text_replacements_generic`, `player_damage_coefficient`, `enemies_damage_coefficient`, `previous_player`, `save_file`, `map` | Starts dungeon loop of dungeon id `current_dungeon` |

## enemy_handling.py

The [`enemy_handling.py`](https://github.com/Dungeons-of-Kathallion/Bane-Of-Wargs/blob/master/source/enemy_handling.py) class handles enemy spawning actions:

| Name                         | Arguments                                                                                                                                                                                                                                                                                                                    | Description                                                              |
|------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|--------------------------------------------------------------------------|
| generate_enemies_from_list() | `lists`, `list_enemies`, `player`                                                                                                                                                                                                                                                                                            | Randomly generate a list of enemies, with enemy pool list `list_enemies` |
| spawn_enemy()                | `map_location`, `list_enemies`, `enemy`, `item`, `lists`, `start_player`, `map`, `player`, `preferences`, `drinks`, `npcs`, `zone`, `mounts`, `mission`, `dialog`, `player_damage_coefficient`, `text_replacements_generic`, `start_time`, `previous_player`, `save_file`, `enemies_damage_coefficient`, `no_run_away`=False | Summons enemy pool list `list_enemies`                                    |

## event_handling.py

The [`event_handling.py`](https://github.com/Dungeons-of-Kathallion/Bane-Of-Wargs/blob/master/source/event_handling.py) class handles events:

| Name                      | Arguments                                                                                                                                                                                                                                                                                                    | Description                                                                                                        |
|---------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------------------|
| event_triggering_checks() | `event_id`, `event`, `player`, `map`, `zone`                                                                                                                                                                                                                                                                 | Return a boolean value that tells if the event id `event_id` can be triggered at the current player circumstances  |
| trigger_event()           | `event_id`, `event`, `player`, `mission`, `dialog`, `preferences`, `text_replacements_generic`, `drinks`, `item`, `enemy`, `npcs`, `start_player`, `lists`, `zone`, `mounts`, `start_time`, `map`, `save_file`, `player_damage_coefficient`, `enemies_damage_coefficient`, `previous_player` | Triggers event id `event_id` triggers                                                                               |

## fishing.py

The [`fishing.py`](https://github.com/Dungeons-of-Kathallion/Bane-Of-Wargs/blob/master/source/fishing.py) class handles the fishing UI:

| Name                      | Arguments                                                                                                                                                                                                                                                                                                    | Description                                                                                                        |
|---------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------------------|
| fishing_loop() | `fishing_location`, `player`, `save_file`, `map_zone`, `zone`, `time_elapsing_coefficient`, `item`                                                                                                                                                                                                                                                                 | Starts the fishing loop, where **`fishing_location` is the map zone id of the fishing map zone, and `map_zone` the map zone id the player is on**.  |

## item_handling.py

The [`item_handling.py`](https://github.com/Dungeons-of-Kathallion/Bane-Of-Wargs/blob/master/source/item_handling.py) class contains functions to handle item usage:

| Name         | Arguments                                                                                                                                                                                                                                                                                                          | Description                                                                                                                                                            |
|--------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| use_item()   | `which_item`, `item_data`, `player`, `preferences`, `drinks`, `enemy`, `npcs`, `start_player`, `lists`, `zone`, `dialog`, `mission`, `mounts`, `text_replacements_generic`, `item`, `map_location`, `player_damage_coefficient`, `previous_player`, `save_file`, `start_time`, `enemies_damage_coefficient`, `map` | Uses item id `which_item` if it can be (if it's a food or consumable, consume it; if it's a weapon or armor piece run equip_item(), if it's an utility, run its script) |
| equip_item() | `item_name`, `player`, `equipment_type`                                                                                                                                                                                                                                                                            | Equip item id `item_name` of type `equipment_type`                                                                                                                     |

## logger_sys.py

The [`logger_sys.py`](https://github.com/Dungeons-of-Kathallion/Bane-Of-Wargs/blob/master/source/logger_sys.py) class handles the logging system of the program:

| Name            | Arguments | Description                                                                                                  |
|-----------------|-----------|--------------------------------------------------------------------------------------------------------------|
| write_message() | `message` | Writes string `message` to the game logs                                                                      |
| log_message()   | `message` | Processes string `message` to the write it to the program's logs (run level tests with the player preferences) |

## main.py

The [`main.py`](https://github.com/Dungeons-of-Kathallion/Bane-Of-Wargs/blob/master/source/main.py) class doesn't have any function, as it is the game engine's root containing the master loop of the game.

## mission_handling.py

The [`mission_handling.py`](https://github.com/Dungeons-of-Kathallion/Bane-Of-Wargs/blob/master/source/mission_handling.py) class contains many functions to handle missions:

| Name                        | Arguments                                                                                                                                                                                                                                                                                              | Description                                                                                                                     |
|-----------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------------------------|
| get_mission_id_from_name()  | `mission_name`, `mission_data`                                                                                                                                                                                                                                                                         | Returns the id of a mission named `mission_name`, by going through the mission data file data `mission_data`                     |
| print_description()         | `mission_data`, `map`                                                                                                                                                                                                                                                                                  | Outputs a mission description (the one in the diary), from its data `mission_data`                                               |
| mission_checks()            | `mission_data`, `player`, `which_key`                                                                                                                                                                                                                                                                  | Return a boolean value, to tell if a mission condition `which_key` is completed, from its data `mission_data`                   |
| execute_triggers()          | `mission_data`, `player`, `which_key`, `dialog`, `preferences`, `text_replacements_generic`, `drinks`, `item`, `enemy`, `npcs`, `start_player`, `lists`, `zone`, `mission`, `mounts`, `start_time`, `map`, `save_file`, `player_damage_coefficient`, `enemies_damage_coefficient`, `previous_player`                                                    | Executes a mission trigger `which_key` from its data `mission_data`                                                              |
| offer_mission()             | `mission_id`, `player`, `missions_data`, `dialog`, `preferences`, `text_replacements_generic`, `drinks`, `item`, `enemy`, `npcs`, `start_player`, `lists`, `zone`, `mission`, `mounts`, `start_time`, `map`, `save_file`, `player_damage_coefficient`, `enemies_damage_coefficient`, `previous_player` | Initiates the mission offering UI of mission id `mission_id`                                                                     |
| mission_completing_checks() | `mission_id`, `missions_data`, `player`, `dialog`, `preferences`, `text_replacements_generic`, `drinks`, `item`, `enemy`, `npcs`, `start_player`, `lists`, `zone`, `mission`, `mounts`, `start_time`, `save_file`, `player_damage_coefficient`, `enemies_damage_coefficient`, `previous_player`                                                         | Checks if mission id `mission_id` can be completed. If it can, mark it as completed and run its completing triggers if there are |

## npc_handling.py

The [`npc_handling.py`](https://github.com/Dungeons-of-Kathallion/Bane-Of-Wargs/blob/master/source/npc_handling.py) class handles the interaction between the player and the npcs:

| Name       | Arguments                                                                | Description                                                                                                      |
|------------|--------------------------------------------------------------------------|------------------------------------------------------------------------------------------------------------------|
| init_npc() | `map_location`, `player`, `npcs`, `drinks`, `item`, `preferences`, `map` |  Inits the interaction loop between the player and the npc at the player's current map point digit `map_location` |

## player_handling.py

The [`player_handling.py`](https://github.com/Dungeons-of-Kathallion/Bane-Of-Wargs/blob/master/source/player_handling.py) class handles all major actions that can be done on the player, such as death:

| Name           | Arguments                  | Description                                                       |
|----------------|----------------------------|-------------------------------------------------------------------|
| player_death() | `preferences`, `save_file` | Inits player death process, and reset the save to its older state. |

## script_handling.py

The [`script_handling.py`](https://github.com/Dungeons-of-Kathallion/Bane-Of-Wargs/blob/master/source/script_handling.py) class handles custom scripts runs, and python modules installation:

| Name                  | Arguments                                                                                                                                                                                                                                                                                              | Description                                                                                                                                                               |
|-----------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| load_script()         | `script_data`, `preferences`, `player`, `map`, `item`, `drinks`, `enemy`, `npcs`, `start_player`, `lists`, `zone`, `dialog`, `mission`, `mounts`, `start_time`, `generic_text_replacements`, `save_file`, `player_damage_coefficient`, `enemies_damage_coefficient`, `previous_player`, `plugin`=False | Init a script running process, with its data `script_data` (a dictionary containing '{"script name": "script.py", arguments: []}') (run execute_script() afterwards)      |
| execute_script()      | `script_data`, `file`, `player`, `map`, `item`, `drinks`, `enemy`, `npcs`, `start_player`, `lists`, `zone`, `dialog`, `mission`, `mounts`, `start_time`, `generic_text_replacements`, `preferences`, `save_file`, `player_damage_coefficient`, `enemies_damage_coefficient`, `previous_player`         | Executes a script from file `file` with its data `script_data` (a dictionary containing '{"script name": "script.py", arguments: []}') (use load_script() to run scripts!) |
| install_requirement() | `module`                                                                                                                                                                                                                                                                                               | Try to install python module `module` using either 'python -m pip install `module`' and 'python3 -m pip install `module`'                                                 |

## terminal_handling.py

The [`terminal_handling.py`](https://github.com/Dungeons-of-Kathallion/Bane-Of-Wargs/blob/master/source/terminal_handling.py) class handles the console, with functions for output, input and useful tools:

| Name                      | Arguments                | Description                                                                                                                                    |
|---------------------------|--------------------------|------------------------------------------------------------------------------------------------------------------------------------------------|
| cout()                    | `text`="", `end`="\n"    | Writes to stdout text `text` with at the end `end`, and then flush it to stdout                                                                |
| cinput()                  | `text`=""                | Returns gotten user input, with an optional text `text` before it                                                                              |
| cinput_multi()            | `text`="", `type`="list" | Returns gotten user input through multiple line, until a EOFE break (Ctrl + D), and return                                                     |
| show_menu()               | `options`, `length`=52   | Displays a choice box with list of choices `options`. The `length` argument is deprecated since [v0.23-alpha](https://github.com/Dungeons-of-Kathallion/Bane-Of-Wargs/releases/tag/0.23-alpha), as it's automatically determined. Returns the selected choice as a string |
| format_string_separator() | `text`                   | Formats `text` to add thousands separators to every number present in it, and returns the formatted string                                     |
| format_string_color() | `text`                   | Formats `text` to replace every present ANSI RGB color codes, if needed, by compatible color codes (if the terminal doesn't accept "truecolor" color system)                                     |
| get_color_rgb() | `color_code`                  | Takes in input an RGB ANSI color code (`\033[38;2;<r>;<g>;<b>m`) and returns its RGB values in an integer list                                     |
| get_size() |                   | Returns the terminal size in a tuple (columns, lines)                                     |
| get_terminal_color_system() |                   | Returns the terminal color system (None, "standard", "256", "truecolor", "windows") (check [this page](https://rich.readthedocs.io/en/stable/console.html#color-systems) for information about terminal color systems)                                     |

## text_handling.py

The [`text_handling.py`](https://github.com/Dungeons-of-Kathallion/Bane-Of-Wargs/blob/master/source/text_handling.py) class contains many useful functions to format and/or output text that are often used:

| Name                                    | Arguments                                    | Description                                                                                                                                  |
|-----------------------------------------|----------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------|
| print_speech_text_effect()              | `text`, `preferences`                        | Outputs text `text` using a hand-writing effect (random time space between every character)                                                  |
| clear_prompt()                          |                                              | Clears the console                                                                                                                           |
| exit_game()                             |                                              | Properly exits the game (used when caught errors happen)                                                                                     |
| print_title()                           | `preferences`                                | Outputs the game's title                                                                                                                     |
| select_save()                           | `options`, `length`=52                       | Runs [terminal_handling's show_menu](#terminal_handlingpy) function, but add a choice named 'EXIT', that stops the program                   |
| print_separator()                       | `character`                                  | Outputs the UI separator, using character `character`                                                                                        |
| overstrike_text()                       | `text`                                       | Outputs overstricken string `text`                                                                                                           |
| print_long_string()                     | `text`, `no_output`=False                    | Outputs a string `text`, with line breaks every about 52 characters. (`no_output` argument is deprecated                                     |
| apply_yaml_data_color_code()            | `text`                                       | Returns `text`, with transformed [yaml data color codes](https://github.com/Dungeons-of-Kathallion/Bane-Of-Wargs/wiki/Yaml-Data-Color-Codes) |
| print_zone_map()                        | `zone_name`, `zone`, `player`, `preferences` | Outputs the UI map zone id `zone_name` thumbnail, with some player information on its side                                                   |
| print_zone_map_alone()                  | `zone_name`, `zone`                          | Outputs map zone id `zone_name` thumbnail **alone**                                                                                          |
| print_npc_thumbnail()                   | `npc`, `preferences`                         | Outputs npc id `npc` thumbnail to the console                                                                                                |
| print_enemy_thumbnail()                 | `enemy`, `preferences`                       | Outputs enemy id `enemy` thumbnail to the console                                                                                            |
| a_an_check()                            | `word`                                       | Takes word string `word`, and adds its proper article (a/an), and returns the final result as a string (returns article+word)                |
| print_item_thumbnail()                  | `to_print`                                   | Used function to output item thumbnails (`to_print` is the thumbnail string). Also returns the thumbnail string                              |
| multiple_items_in_list_formatting()     | `list_to_format`                             | Format list `list_to_format`, to replace every different occurrences by 'X{occurrences}{text}. Used from required metals in weapon upgrades  |
| transform_negative_number_to_positive() | `number`                                     | Returns negative integer `number` into a positive integer.                                                                                   |
| print_map_art()                         | `item_data`                                  | Formats map item ASCII art to add proper map colors, and returns it to the console, using its data `item_data`                               |
| print_moving_text()                         | `text`                                  | Outputs string `text` to the console using an ending movie credits (used for the credits.txt file display)                               |

## time_handling.py

The [`time_handling.py`](https://github.com/Dungeons-of-Kathallion/Bane-Of-Wargs/blob/master/source/time_handling.py) class contains functions to calculate date and time related stuff:

| Name                           | Arguments                              | Description                                                                                                                                                                 |
|--------------------------------|----------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| addition_to_date()             | `date`, `addition`                     | Returns date `date` after adding `addition` days to it (date format: '{month}-{day}-{year}'                                                                                 |
| date_prettifier()              | `date`                                 | Prettifies date `date` (transform '{month}-{day}-{year}' to '{day}{ordinal suffix} {month name}, {year}'                                                                       |
| get_day_time()                 | `game_days`                            | Returns the day time of bane of wargs day unit `game_days` (night/morning/day/evening)                                                                                      |
| return_game_day_from_seconds() | `seconds`, `time_elapsing_coefficient` | Transforms `seconds` seconds to bane of wargs day units (`time_elapsing_coefficient` is usually 1, but it gets modified by consumable effects)                              |
| traveling_wait()               | `traveling_coefficient`                | Runs traveling wait actions (check [here](https://github.com/Dungeons-of-Kathallion/Bane-Of-Wargs/wiki/Traveling-Time-Handling) for more info about `traveling_coefficient` |

## train.py

The [`train.py`](https://github.com/Dungeons-of-Kathallion/Bane-Of-Wargs/blob/master/source/train.py) class contains the train UI loop:

| Name            | Arguments                                                                                  | Description                                                                                                              |
|-----------------|--------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------------------------|
| get_cost()      | `cost`, `dropoff`, `round_cost`=True                                                       | Returns gold `cost` with dropoff decimal percentage `dropoff` applied                                                    |
| training_loop() | `mount_uuid`, `player`, `item`, `mounts`, `stable`, `time_elapsing_coefficient`, `dropoff` | Starts the training for player's mount uuid `mount_uuid` (`dropoff` is 1 unless the current stable has a dropoff active) |

## uuid_handling.py

The [`uuid_handling.py`](https://github.com/Dungeons-of-Kathallion/Bane-Of-Wargs/blob/master/source/uuid_handling.py) class contains functions to randomly generate UUIDs ([Universal Unique Identifier](https://www.google.com/search?client=firefox-b-d&q=uuid)):

| Name                   | Arguments | Description                                                                                |
|------------------------|-----------|--------------------------------------------------------------------------------------------|
| generate_random_uuid() |           | Returns a randomly generated UUID using python built-in uuid module and its uuid4() method |

## weapon_upgrade_handling.py

The [`weapon_upgrade_handling.py`](https://github.com/Dungeons-of-Kathallion/Bane-Of-Wargs/blob/master/source/weapon_upgrade_handling.py) class contains a few functions that are useful when doing weapon/armor upgrade related actions:

| Name                               | Arguments           | Description                                                                                  |
|------------------------------------|---------------------|----------------------------------------------------------------------------------------------|
| check_for_item()                   | `item_name`, `item` | Checks if item id `item_name` exists                                                         |
| check_weapon_next_upgrade_name()   | `item_name`, `item` | Returns weapon/armor piece id `item_name` next upgrade id                                    |
| check_weapon_max_upgrade()         | `item_name`, `item` | Returns weapon/armor piece id `item_name` max upgrade id                                     |
| detect_weapon_next_upgrade_items() | `item_name`, `item` | Returns a string that contains every next upgrade items of weapon/armor piece id `item_name` |

## yaml_handling.py

The [`yaml_handling.py`](https://github.com/Dungeons-of-Kathallion/Bane-Of-Wargs/blob/master/source/yaml_handling.py) class contains functions to load and dump yaml data:

| Name        | Arguments            | Description                                                                                                                                                         |
|-------------|----------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| safe_load() | `file`, `crash`=True | Loads yaml content of opened file data `file`, and returns python-converted data (`crash` determines if the program should be stopped if an error gets encountered) |
| dump()      | `data`, `crash`=True | Returns a yaml-parsed string from python data `data` (`crash` determines if the program should be stopped if an error gets encountered)                             |

## zone_handling.py

The [`zone_handling.py`](https://github.com/Dungeons-of-Kathallion/Bane-Of-Wargs/blob/master/source/zone_handling.py) class handles the aspects of interactive map zone and some other useful tool functions:

| Name                                 | Arguments                                                                                                                                                                                                                                                                                           | Description                                                                                                                                                                                                                                                                            |
|--------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| get_cost()                           | `cost`, `dropoff`, `round_cost`=True                                                                                                                                                                                                                                                                | Returns gold `cost` with dropoff decimal percentage `dropoff` applied                                                                                                                                                                                                                  |
| print_zone_news()                    | `zone`, `map_zone`, `player`                                                                                                                                                                                                                                                                        | Prints map zone id `map_zone` news (also displays info about the current dropoff if there's one) (only works if this is an interactive map zone)                                                                                                                                       |
| print_forge_information()            | `map_zone`, `zone`, `item`, `player`                                                                                                                                                                                                                                                                | Displays UI information about map zone forge id `map_zone`                                                                                                                                                                                                                             |
| print_blacksmith_information()       | `map_zone`, `zone`, `item`, `player`                                                                                                                                                                                                                                                                | Displays UI information about map zone blacksmith id `map_zone`                                                                                                                                                                                                                        |
| print_stable_information()           | `map_zone`, `zone`, `mounts`, `item`, `player`, `map_location`                                                                                                                                                                                                                                      | Displays UI information about map zone stable id `map_zone` (`map_location` is the player current map point digit)                                                                                                                                                                     |
| print_hostel_information()           | `map_zone`, `zone`, `item`, `drinks`, `player`                                                                                                                                                                                                                                                      | Displays UI information about map zone hostel id `map_zone`                                                                                                                                                                                                                            |
| print_grocery_information()          | `map_zone`, `zone`, `item`, `player`                                                                                                                                                                                                                                                                | Displays UI information about map zone grocery id `map_zone`                                                                                                                                                                                                                           |
| print_harbor_information()           | `map_zone`, `zone`, `map`, `player`                                                                                                                                                                                                                                                                 | Displays UI information about map zone harbor id `map_zone`                                                                                                                                                                                                                            |
| interaction_hostel()                 | `map_zone`, `zone`, `player`, `drinks`, `item`, `save_file`, `preferences`, `previous_player`                                                                                                                                                                                                       | Starts interaction loop with map zone hostel id `map_zone`                                                                                                                                                                                                                             |
| interaction_stable()                 | `map_zone`, `zone`, `player`, `item`, `drinks`, `mounts`, `map_location`, `preferences`, `time_elapsing_coefficient`                                                                                                                                                                                | Starts interaction loop with map zone stable id `map_zone` (`map_location` is the player current map point digit) (check [this wiki page](https://github.com/Dungeons-of-Kathallion/Bane-Of-Wargs/wiki/Traveling-Time-Handling) to know about the `time_elapsing_coefficent` variable) |
| interaction_blacksmith()             | `map_zone`, `zone`, `item`, `player`                                                                                                                                                                                                                                                                | Starts interaction loop with map zone blacksmith id `map_zone`                                                                                                                                                                                                                         |
| interaction_forge()                  | `map_zone`, `zone`, `player`, `item`                                                                                                                                                                                                                                                                | Starts interaction loop with map zone forge id `map_zone`                                                                                                                                                                                                                              |
| interaction_church()                 | `map_zone`, `zone`, `player`, `save_file`, `preferences`, `previous_player`                                                                                                                                                                                                                         | Starts interaction loop with map zone church id `map_zone`                                                                                                                                                                                                                             |
| interaction_grocery()                | `map_zone`, `zone`, `player`, `item`                                                                                                                                                                                                                                                                | Starts interaction loop with map zone grocery id `map_zone`                                                                                                                                                                                                                            |
| interaction_harbor()                 | `map_zone`, `zone`, `map`, `player`                                                                                                                                                                                                                                                                 | Starts interaction loop with map zone harbor id `map_zone`                                                                                                                                                                                                                             |
| interaction_dungeon()                | `map_zone`, `zone`, `map`, `player`, `dialog`, `item`, `preferences`, `text_replacements_generic`, `drinks`, `enemy`, `npcs`, `start_player`, `lists`, `mission`, `mounts`, `start_time`, `map_location`, `player_damage_coefficient`, `enemies_damage_coefficient`, `previous_player`, `save_file` | Starts interaction loop with map zone dungeon id `map_zone`                                                                                                                                                                                                                            |
| get_map_point_distance_from_player() | `map`, `player`, `current_map_point`                                                                                                                                                                                                                                                                | Returns the distance between the map point id `current_map_point` and the player current location, in a map point/mile unit                                                                                                                                                            |
| get_zone_nearest_point()             | `map`, `player`, `map_zone_name`                                                                                                                                                                                                                                                                    | Returns the closest location from player of map zone id `map_zone_name` map point id                                                                                                                                                                                                   |
| determine_grocery_sales()            | `zone_data`                                                                                                                                                                                                                                                                                         | Returns a randomly generated list of sales from grocery zone's data `zone_data`                                                                                                                                                                                                        |
| get_zone_color()                     | `zone_type`                                                                                                                                                                                                                                                                                         | Returns string of colored ASCII art, corresponding the the map zone type `zone_type`                                                                                                                                                                                                   |
