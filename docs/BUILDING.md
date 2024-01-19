# Build instructions

First you need to get the source code of the game (here use your fork's url if you want to compile your fork).

```powershell
> git clone git@github.com:Dungeons-of-Kathallion/Bane-Of-Wargs.git
```

The game root directory, the folder that has been created after cloning the repository will be the start point for building and compiling the game. After running the git clone command, you can run `cd Bane-Of-Wargs` to changed of folder.

Next, you'll have to install a few dependencies in order to be able to make the whole compiling process.

## Installing Build Dependencies

Well of course first, you'll need to have the Python interpreter installed as well as a python package manager PIP. You can check the [`docs/PLAYING.md`](https://github.com/Dungeons-of-Kathallion/Bane-Of-Wargs/blob/master/docs/PLAYING.md#get-python-installed-windows-linux-macos) document if you need help installing the Python interpreter.

Afterwards, you'll also need to get the python packages required for the game to run. Here are the PIP packages:
```
simple_term_menu
fade
GitPython
colorama
PyYaml
Yamale
Fsspec
AppDirs
```

You can also find them in the `requirements.txt` file, located in the root directory. You can also find a guide on how to install these packages in the [`docs/PLAYING.md`](https://github.com/Dungeons-of-Kathallion/Bane-Of-Wargs/blob/master/docs/PLAYING.md#getting-required-moduleslibraries-installed--possibly-fix-issues) document.

And finally, you'll need to install the python package [`PyInstaller`](https://pyinstaller.org/en/stable/), which is used to compile the source code of the game. Install this package the same way you did for the last ones.

*Note: there is no specific version required for these packages but make sure it's the latest version just in case.*

## Building The Game

#### Building From The Command Line

Here's a summary of each command case per case that you'll need to run to compile the program.

```shell
$ mkdir yamale
$ echo `4.0.4` >> yamale/VERSION # for certain reasons, the compiled program needs this file
$ python -m PyInstaller \
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
source/term_menu.py \
source/mission_handling.py \
source/dialog_handling.py \
source/enemy_handling.py \
source/data_handling.py \
source/npc_handling.py \
source/text_handling.py \
--add-data yamale/VERSION:yamale \
--collect-submodules fsspec \
--collect-submodules appdirs \
--hidden-import appdirs \
--hidden-import fsspec \
--exclude-module fcntl \
--log-level DEBUG
# create a single executable name `Bane Of Wargs` with all the source code in it, the required libraries and additional stuff required
```

Alternatively, you can run the bash script `compile.sh` in the root directory **but you're still need the `yamale/VERSION` with `4.0.4` written in for the first time**.
**For windows and macos user, compiling has not been tested yet.**

The compiled executable file will be found in the `dist/` directory, which is located in the root directory.

## Additional: Making A Desktop Shortcut (Linux)

The next step to make the game a real app is to create a desktop shortcut for it. Here I will only cover doing this on linux desktops simply because that's my desktop.

First, open a text editor and create a new document. Name it `Bane-Of-Wargs.desktop`.
In this document, you will enter this code:

```yaml
[Desktop Entry]
Version=1.0
Type=Application
Name=Bane Of Wargs
Comment=Play the Bane Of Wargs game
Keywords=bane;wargs;python;bane of wargs;
Exec=<path to executable>
Icon=<path to icon>
Terminal=true
Categories=Game;
```

- `Version` // version of the program. This totally not required, you can remove it or enter any value.
- `Type` // the type of the desktop shortcut. Here, it's an application.
- `Name` // the name that will displayed under the icon.
- `Comment` // a fast and compact description of the program.
- `Keywords` // the keywords that will make the shortcut appears in the search bar.
- `Exec` // the path to the executable. For example, me I would put '~/Documents/vscode-cloned-repositories/Bane-Of-Wargs/dist/Bane-Of-Wargs'
- `Icon` // the path of the icon that will be displayed on top of the app name. This is not required, you can remove it, if you do, it's the default app icon that will be shown.
- `Terminal` // make so that it will open the terminal when executing the program specified at `Exec`.
- `Categories` // the list of categories of program this program is in.

After finishing the editing of that file, save it at the following location:
`/usr/share/applications/`.
If you've done everything right, the app should be on your desktop shortcuts. If it doesn't work, maybe try to log out.
