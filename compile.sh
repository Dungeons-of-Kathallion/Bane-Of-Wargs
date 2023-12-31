#!/bin/sh

python -m PyInstaller \
--console \
--onefile \
--name Bane-Of-Wargs \
source/main.py \
source/battle.py \
source/check_yaml.py \
source/colors.py \
source/map_item.py \
source/train.py \
source/logger_sys.py \
--add-data yamale/VERSION:yamale \
--collect-submodules fsspec \
--collect-submodules appdirs \
--hidden-import appdirs \
--hidden-import fsspec \
--exclude-module fcntl \
--log-level DEBUG
