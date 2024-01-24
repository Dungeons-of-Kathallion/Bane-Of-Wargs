#!/bin/sh

python -m PyInstaller \
--console \
--onefile \
--name Bane-Of-Wargs \
source/main.py \
source/battle.py \
source/check_yaml.py \
source/colors.py \
source/train.py \
source/logger_sys.py \
source/term_menu.py \
source/mission_handling.py \
source/dialog_handling.py \
source/enemy_handling.py \
source/data_handling.py \
source/npc_handling.py \
source/text_handling.py \
source/zone_handling.py \
source/uuid_handling.py \
source/weapon_upgrade_handling.py \
--add-data yamale/VERSION:yamale \
--collect-submodules fsspec \
--collect-submodules appdirs \
--hidden-import appdirs \
--hidden-import fsspec \
--exclude-module fcntl \
--log-level DEBUG

sudo mv dist/Bane-Of-Wargs /usr/bin/
