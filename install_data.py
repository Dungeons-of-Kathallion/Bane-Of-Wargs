import appdirs
import shutil
import os

program_dir = str(appdirs.user_config_dir(appname='Bane-Of-Wargs'))

try:
    print("$PROGRAM_DIR = " + program_dir)
    print("Installing vanilla data files...")
    data_files = os.listdir("data")
    for f in data_files:
        shutil.copy2(os.path.join("data",f), program_dir + "/game/data")
    print("Installing vanilla txt images files...")
    data_files = os.listdir("imgs")
    for f in data_files:
        shutil.copy2(os.path.join("imgs",f), program_dir + "/game/imgs")
    print("Installing vanilla schemas files...")
    data_files = os.listdir("schemas")
    for f in data_files:
        shutil.copy2(os.path.join("schemas",f), program_dir + "/game/schemas")
    print("Installing vanilla scripts files...")
    data_files = os.listdir("scripts")
    for f in data_files:
        shutil.copy2(os.path.join("scripts",f), program_dir + "/game/scripts")
except Exception as e:
    print(e)
