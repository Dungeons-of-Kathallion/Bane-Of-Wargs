* [battle.py](#battlepy)
* [check_yaml.py](#check_yamlpy)
* [consumable_handling.py](#consumable_handlingpy)
* [data_handling.py](#data_handlingpy)
* [dialog_handling.py](#dialog_handlingpy)
* [dungeon.py](#dungeonpy)
* [enemy_handling.py](#enemy_handlingpy)
* [event_handling.py](#event_handlingpy)
* [item_handling.py](#item_handlingpy)
* [logger_sys.py](#logger_syspy)
* [main.py](#mainpy)
* [mission_handling.py](#mission_handlingpy)
* [npc_handling.py](#npc_handlingpy)

## battle.py

The [`battle.py`](https://github.com/Dungeons-of-Kathallion/Bane-Of-Wargs/blob/master/source/battle.py) class handles all of the game combat UI. Here are all of its functions (_Note that you should use the [enemy_handling.py](#enemy_handlingpy) class to make enemy spawn instead of battle.py_):

| Name                    | Arguments                                                                                                                                                                                                                                                                                                                                                                     | Description                                                                                            |
|-------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------|
| calculate_player_risk() | `player`, `item`, `enemies_remaining`, `chosen_enemy`, `enemy`, `player_damage_coefficient`, `enemies_damage_coefficient`                                                                                                                                                                                                                                                     | Simulate a fight with `enemies_remaining` `enemy` enemies, to return the risk percentage of the player |
| encounter_text_show()   | `player`, `item`, `enemy`, `map`, `map_location`, `enemies_remaining`, `lists`, `defeat_percentage`, `preferences`, `drinks`, `npcs`, `zone`, `mounts`, `mission`, `start_player`, `dialog`, `text_replacements_generic`, `player_damage_coefficient`, `previous_player`, `save_file`, `start_time`, `enemies_damage_coefficient`, `entry_data`, `enemies`, `no_run_away`=False | Display the encountering text of enemy pool list `entry_data`                                          |
| fight()                 | `player`, `item`, `enemy`, `map`, `map_location`, `enemies_remaining`, `lists`, `preferences`, `drinks`, `npcs`, `start_player`, `zone`, `dialog`, `mission`, `mounts`, `player_damage_coefficient`, `start_time`, `text_replacements_generic`,  `previous_player`, `save_file`, `enemies_damage_coefficient`, `defeat_percentage`, `entry_data`, `enemies`                   | Start fight of enemy pool list `entry_data`                                                            |

## check_yaml.py

The [`check_yaml.py`](https://github.com/Dungeons-of-Kathallion/Bane-Of-Wargs/blob/master/source/check_yaml.py) class won't be a class you'll use for custom scripting, as it contains the functions to run tests on the loaded game data. But if you're interested in contributing, you might want to check yourself the class and analyze it.

## colors.py

The [`colors.py`](https://github.com/Dungeons-of-Kathallion/Bane-Of-Wargs/blob/master/source/colors.py) class is a database of color codes, used for colored terminal input. Just check the class if you need a color code you're searching for.

## consumable_handling.py

The [`consumable_handling.py`](https://github.com/Dungeons-of-Kathallion/Bane-Of-Wargs/blob/master/source/consumable_handling.py) class contains a set of function that generates the effect of consumables, or print its effects to the console. There are many small functions, so we're only gonna go over the three main ones you have a chance to ever use:

| Name                       | Arguments                                                                                                                                                                                                                                                                                                               | Description                                                                                                                                                                          |
|----------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| consume_consumable()       | `item_data`, `consumable_name`, `player`, `dialog`, `preferences`, `text_replacements_generic`, `lists`, `map_location`, `enemy`, `item`, `drinks`, `start_player`, `npcs`, `zone`, `mounts`, `mission`, `player_damage_coefficient`, `previous_player`, `save_file`, `map`, `start_time`, `enemies_damage_coefficient` | Consume consumable `consumable_name`                                                                                                                                                 |
| print_consumable_effects() | `current_effect_type`, `current_effect_data`                                                                                                                                                                                                                                                                            | Output to the console the visible effects of effect `current_effect_data` of type `current_effect_type` (display percentages instead of meaning numbers of print_consumable_effects) |
| print_active_effect_info() | `effect_data`, `player`                                                                                                                                                                                                                                                                                                 | Print the effects of a visible effect `effect_data`, on the `player` (display meaning numbers instead of percentages of print_consumable_effects)                                    |

## data_handling.py

The [`data_handling.py`](https://github.com/Dungeons-of-Kathallion/Bane-Of-Wargs/blob/master/source/data_handling.py) class contains functions to load the game data, and to download stuff from online locations, using [fsspec](https://pypi.org/project/fsspec/). Here are all the functions:

| Name                          | Arguments                                                                              | Description                                                                                                                                                                                                                                                                               |
|-------------------------------|----------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| load_game_data()              | `which_type`, `preferences`                                                            | Determine which game data to load and from where, and load it (and analyze it if the preferences 'analyze' option is set to enabled). Return every game data variables: `map`, `item`, `drinks`, `enemy`, `npcs`, `start_player`, `lists`, `zone`, `dialog`, `mission`, `mounts`, `event` |
| update_game_data()            | `preferences`, `latest_game_data_version`                                              | Redownload the game vanilla data at '{bow-folder}/game/', from latest game data version                                                                                                                                                                                                   |
| fsspec_download()             | `github_file`, `destination_point`, `download_branch`, `download_repo`, `download_org` | Download a file from path `github_file` to destination path `destination_point`, from github account `donload_org`, repo `download_repo`, and branch/tag `download_branch`                                                                                                                |
| temporary_git_file_download() | `selected_file`, `url`                                                                 | Download a file from path `selected_file` from github url `url`, in a created temporary folder, and return the data of the file in a string                                                                                                                                               |
| open_file()                   | `file_path`                                                                            | Open file from path `file_path` with default user terminal editor                                                                                                                                                                                                                         |

## dialog_handling.py

The [`dialog_handling.py`](https://github.com/Dungeons-of-Kathallion/Bane-Of-Wargs/blob/master/source/dialog_handling.py) class contains function to load dialog and their conversations. The only function you need to know about is the one to trigger a dialog:

| Name           | Arguments                                                                                                                                                                                                                           | Description                                                                                                                             |
|----------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------|
| print_dialog() | `current_dialog`, `dialog`, `preferences`, `text_replacements_generic`, `player`, `drinks`, `item`, `enemy`, `npcs`, `start_player`, `lists`, `zone`, `mission`, `mounts`, `start_time`, `map`, `save_file`, `player_damage_coefficient`, `enemies_damage_coefficient`, `previous_player`, `mission_offered`=None | Triggers dialog `current_dialog`. Specify a mission id at `mission_offered` if you want conversation actions like 'accept()' to be ran |

## dungeon.py

The [`dungeon.py`](https://github.com/Dungeons-of-Kathallion/Bane-Of-Wargs/blob/master/source/dungeon.py) class handles the dungeon UI. It only contains one function, that starts the dungeon loop:

| Name           | Arguments                                                                                                                                                                                                                                                                                                              | Description                                         |
|----------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-----------------------------------------------------|
| dungeon_loop() | `player`, `current_dungeon`, `lists`, `enemy`, `start_player`, `item`, `start_time`, `preferences`, `npcs`, `drinks`, `zone`, `mounts`, `dialog`, `mission`, `map_location`, `text_replacements_generic`, `player_damage_coefficient`, `enemies_damage_coefficient`, `previous_player`, `save_file`, `map` | Starts dungeon loop of dungeon id `current_dungeon` |

## enemy_handling.py

The [`enemy_handling.py`](https://github.com/Dungeons-of-Kathallion/Bane-Of-Wargs/blob/master/source/enemy_handling.py) class handles enemy spawning actions:

| Name                         | Arguments                                                                                                                                                                                                                                                                                                                    | Description                                                              |
|------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|--------------------------------------------------------------------------|
| generate_enemies_from_list() | `lists`, `list_enemies`, `player`                                                                                                                                                                                                                                                                                            | Randomly generate a list of enemies, with enemy pool list `list_enemies` |
| spawn_enemy()                | `map_location`, `list_enemies`, `enemy`, `item`, `lists`, `start_player`, `map`, `player`, `preferences`, `drinks`, `npcs`, `zone`, `mounts`, `mission`, `dialog`, `player_damage_coefficient`, `text_replacements_generic`, `start_time`, `previous_player`, `save_file`, `enemies_damage_coefficient`, `no_run_away`=False | Summon enemy pool list `list_enemies`                                    |

## event_handling.py

The [`event_handling.py`](https://github.com/Dungeons-of-Kathallion/Bane-Of-Wargs/blob/master/source/event_handling.py) class handles events:

| Name                      | Arguments                                                                                                                                                                                                                                                                                                    | Description                                                                                                        |
|---------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------------------|
| event_triggering_checks() | `event_id`, `event`, `player`, `map`, `zone`                                                                                                                                                                                                                                                                 | Return a boolean value that tells if the event id `event_id` can be triggered at the current player circumstances  |
| trigger_event()           | `event_id`, `event`, `player`, `mission`, `dialog`, `preferences`, `text_replacements_generic`, `drinks`, `item`, `enemy`, `npcs`, `start_player`, `lists`, `zone`, `mounts`, `start_time`, `map`, `save_file`, `map_location`, `player_damage_coefficient`, `previous_player`, `enemies_damage_coefficient` | Trigger event id `event_id` triggers                                                                               |

## item_handling.py

The [`item_handling.py`](https://github.com/Dungeons-of-Kathallion/Bane-Of-Wargs/blob/master/source/item_handling.py) class contains functions to handle item usage:

| Name         | Arguments                                                                                                                                                                                                                                                                                                          | Description                                                                                                                                                            |
|--------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| use_item()   | `which_item`, `item_data`, `player`, `preferences`, `drinks`, `enemy`, `npcs`, `start_player`, `lists`, `zone`, `dialog`, `mission`, `mounts`, `text_replacements_generic`, `item`, `map_location`, `player_damage_coefficient`, `previous_player`, `save_file`, `start_time`, `enemies_damage_coefficient`, `map` | Use item id `which_item` if it can be (if it's a food or consumable, consume it; if it's a weapon or armor piece run equip_item(), if it's an utility, run its script) |
| equip_item() | `item_name`, `player`, `equipment_type`                                                                                                                                                                                                                                                                            | Equip item id `item_name` of type `equipment_type`                                                                                                                     |

## logger_sys.py

The [`logger_sys.py`](https://github.com/Dungeons-of-Kathallion/Bane-Of-Wargs/blob/master/source/logger_sys.py) class handles the logging system of the program:

| Name            | Arguments | Description                                                                                                  |
|-----------------|-----------|--------------------------------------------------------------------------------------------------------------|
| write_message() | `message` | Write string `message` to the game logs                                                                      |
| log_message()   | `message` | Process string `message` to the write it to the program's logs (run level tests with the player preferences) |

## main.py

The [`main.py`](https://github.com/Dungeons-of-Kathallion/Bane-Of-Wargs/blob/master/source/main.py) class doesn't have any function, as it is the game engine's root, that contains the master loop of the game.

## mission_handling.py

The [`mission_handling.py`](https://github.com/Dungeons-of-Kathallion/Bane-Of-Wargs/blob/master/source/mission_handling.py) class contains many functions to handle missions:

| Name                        | Arguments                                                                                                                                                                                                                                                                                              | Description                                                                                                                     |
|-----------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------------------------|
| get_mission_id_from_name()  | `mission_name`, `mission_data`                                                                                                                                                                                                                                                                         | Return the id of a mission named `mission_name`, by going through the mission data file data `mission_data`                     |
| print_description()         | `mission_data`, `map`                                                                                                                                                                                                                                                                                  | Output a mission description (the one in the diary), from its data `mission_data`                                               |
| mission_checks()            | `mission_data`, `player`, `which_key`                                                                                                                                                                                                                                                                  | Return a boolean value, to tell if a mission condition `which_key` is completed, from its data `mission_data`                   |
| execute_triggers()          | `mission_data`, `player`, `which_key`, `dialog`, `preferences`, `text_replacements_generic`, `drinks`, `item`, `enemy`, `npcs`, `start_player`, `lists`, `zone`, `mission`, `mounts`, `start_time`, `map`, `save_file`, `player_damage_coefficient`                                                    | Execute a mission trigger `which_key` from its data `mission_data`                                                              |
| offer_mission()             | `mission_id`, `player`, `missions_data`, `dialog`, `preferences`, `text_replacements_generic`, `drinks`, `item`, `enemy`, `npcs`, `start_player`, `lists`, `zone`, `mission`, `mounts`, `start_time`, `map`, `save_file`, `player_damage_coefficient`, `enemies_damage_coefficient`, `previous_player` | Initiate the mission offering UI of mission id `mission_id`                                                                     |
| mission_completing_checks() | `mission_id`, `missions_data`, `player`, `dialog`, `preferences`, `text_replacements_generic`, `drinks`, `item`, `enemy`, `npcs`, `start_player`, `lists`, `zone`, `mission`, `mounts`, `start_time`, `save_file`, `player_damage_coefficient`                                                         | Check if mission id `mission_id` can be completed. If it can, mark it as completed and run its completing triggers if there are |

## npc_handling.py

The [`npc_handling.py`](https://github.com/Dungeons-of-Kathallion/Bane-Of-Wargs/blob/master/source/npc_handling.py) class handles the interaction between the player and the npcs:

| Name       | Arguments                                                                | Description                                                                                                      |
|------------|--------------------------------------------------------------------------|------------------------------------------------------------------------------------------------------------------|
| init_npc() | `map_location`, `player`, `npcs`, `drinks`, `item`, `preferences`, `map` |  Init the interaction loop between the player and the npc at the player's current map point digit `map_location` |
