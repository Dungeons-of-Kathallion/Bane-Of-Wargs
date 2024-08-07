# Build instructions

First you need to get the source code of the game (here use your fork's url if you want to compile your fork).

```powershell
> git clone git@github.com:Dungeons-of-Kathallion/Bane-Of-Wargs.git
```

The game root directory, the folder that has been created after cloning the repository will be the start point for building and compiling the game. After running the git clone command, you can run `cd Bane-Of-Wargs` to changed of folder.

Next, you'll have to install a few dependencies in order to be able to make the whole compiling process.

### Installing Build Dependencies

Well of course first, you'll need to have the Python interpreter installed as well as a python package manager PIP. You can check the [`docs/PLAYING.md`](https://github.com/Dungeons-of-Kathallion/Bane-Of-Wargs/blob/master/docs/PLAYING.md#get-python-installed-windows-linux-macos) document if you need help installing the Python interpreter.

Afterwards, you'll also need to get the python packages required for the game to run. Here are the PIP packages:
```
fade
GitPython
colorama
PyYaml
yamale
fsspec
appdirs
requests
rich
```

You can also find them in the `requirements.txt` file, located in the root directory. You can also find a guide on how to install these packages in the [`docs/PLAYING.md`](https://github.com/Dungeons-of-Kathallion/Bane-Of-Wargs/blob/master/docs/PLAYING.md#getting-required-moduleslibraries-installed--possibly-fix-issues) document.

And finally, you'll need to install the python package [`PyInstaller`](https://pyinstaller.org/en/stable/), which is used to compile the source code of the game. Install this package the same way you did for the last ones.

*Note: there is no specific version required for these packages but make sure it's the latest version just in case.*

## Building The Game

#### Generic Build

Here's a summary of each command case per case that you'll need to run to compile the program.

```shell
$ mkdir yamale
$ echo `4.0.4` >> yamale/VERSION # for certain reasons, the compiled program needs this file
$ python -m PyInstaller Bane-Of-Wargs.spec
# create a single executable name `Bane Of Wargs` with all the source code in it, the required libraries and additional stuff required
```

Alternatively, you can run the bash script `compile.sh` in the root directory **but you'll still need the `yamale/VERSION` with `4.0.4` written in for the first time**.
**For windows and macos user, compiling has not been tested yet.**

The compiled executable file will be found in the `dist/` directory, which is located in the root directory.

---

#### Flatpak Build

Alternatively, you can build the game engine as a [flatpak package](https://docs.flatpak.org/en/latest/introduction.html), even if for now the program isn't published in any public repository, but it shouldn't last long until it does. Note that if you build t as a [flatpak package](https://docs.flatpak.org/en/latest/introduction.html), the game directory won't any longer be in your user config folder, but in the flatpak program config folder, usually at `~/.var/app/com.Cromha.BaneOfWargs/config`. Lucky for you, the Bane Of Wargs github repository has everything you need to build the app in a few commands:

* first, you want to install the required runtime (_valid versions: '5.15-23.08'_):
```bash
flatpak install org.kde.Platform
```
* then, you want to install the tool used for building flatpak apps: [flatpak-builder](https://github.com/flatpak/flatpak-builder), that you can install from dnf, apt or flatpak:
```bash
dnf install flatpak-builder
flatpak install flathub org.flatpak.Builder
```
* you can then compile the program using [flatpak-builder](https://github.com/flatpak/flatpak-builder):
```bash
flatpak-builder --user --install --force-clean build-dir com.Cromha.BaneOfWargs.yaml
```
* and it's done! you can run the game using:
```bash
flatpak run com.Cromha.BaneOfWargs
```

## Additional: Making A Desktop Shortcut (GNU/Linux)

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
- `Exec` // the path to the executable. For example, me I would put '~/Documents/vscode-cloned-repositories/Bane-Of-Wargs/dist/Bane-Of-Wargs'. If you built it using flatpak, put '<flatpak binary> run com.Cromha.BaneOfWargs': for example '/usr/bin/flatpak run com.Cromha.BaneOfWargs'
- `Icon` // the path of the icon that will be displayed on top of the app name. This is not required, you can remove it, if you do, it's the default app icon that will be shown.
- `Terminal` // make so that it will open the terminal when executing the program specified at `Exec`.
- `Categories` // the list of categories of program this program is in.

After finishing the editing of that file, save it at the following location:
`/usr/share/applications/`.
If you've done everything right, the app should be on your desktop shortcuts. If it doesn't work, maybe try to log out.
