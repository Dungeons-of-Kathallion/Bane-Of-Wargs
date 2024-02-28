# Bane Of Wargs (BETA)

```bash
lolo@fedora ~ $ python main.py
████████████████████████████████████████████████████████████████████▀███████
█▄─▄─▀██▀▄─██▄─▀█▄─▄█▄─▄▄─███─▄▄─█▄─▄▄─███▄─█▀▀▀█─▄██▀▄─██▄─▄▄▀█─▄▄▄▄█─▄▄▄▄█
██─▄─▀██─▀─███─█▄▀─███─▄█▀███─██─██─▄██████─█─█─█─███─▀─███─▄─▄█─██▄─█▄▄▄▄─█
▀▄▄▄▄▀▀▄▄▀▄▄▀▄▄▄▀▀▄▄▀▄▄▄▄▄▀▀▀▄▄▄▄▀▄▄▄▀▀▀▀▀▀▄▄▄▀▄▄▄▀▀▄▄▀▄▄▀▄▄▀▄▄▀▄▄▄▄▄▀▄▄▄▄▄▀

> Play Game
  Manage Saves
  Preferences
  Check Update
  Quit
```
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
![Python Version](https://badgen.net/badge/python/3.12/blue?icon=python)
[![CD](https://github.com/Dungeons-of-Kathallion/Bane-Of-Wargs/actions/workflows/cd.yaml/badge.svg)](https://github.com/Dungeons-of-Kathallion/Bane-Of-Wargs/actions/workflows/cd.yaml)
[![Validate-YAML](https://github.com/Dungeons-of-Kathallion/Bane-Of-Wargs/actions/workflows/yaml_checks.yaml/badge.svg)](https://github.com/Dungeons-of-Kathallion/Bane-Of-Wargs/actions/workflows/yaml_checks.yaml)
[![Spell Checks](https://github.com/Dungeons-of-Kathallion/Bane-Of-Wargs/actions/workflows/spell_checks.yaml/badge.svg)](https://github.com/Dungeons-of-Kathallion/Bane-Of-Wargs/actions/workflows/spell_checks.yaml)
---

Bane Of Wargs is a python text-game engine with pre-built plot an the ability to create custom plugins/mods that completely change the game content. The game is very customizable and you will find ton of in-game features: equipment upgrading, items orders, mounts training over time, xp gaining, hp gaining etc... So in overall a very customizable and enjoyable python terminal-text based RPG.

You will have to fight monsters, bossses to get keys to after unlock new places of the map. The map is divised in points, determined by x and y coordinates, letting the possibility to map up to 128x128 wide (so up to 16,384 places to explore), and more in the future of the engine development.

See the [Gameplay Guide](https://github.com/Dungeons-of-Kathallion/Bane-Of-Wargs/wiki/Gameplay-Guide) wiki page or check or the [Creating Mod](https://github.com/Dungeons-of-Kathallion/Bane-Of-Wargs/wiki/Creating-Mods) wiki page if you're interested in modding the game.

---

Here's the vanilla starting dialog plot:
> “
> You're a lumberjack who lives in a small village in the _Forlindon Woods_, a quiet a calm place to live. You've always wondered what's after this quiet forest; because your little village is a small town that lives apart from the other great cities in the _Stall Island_. You've heard some stories and tales about the rest of the world. Only some words come to your mind when you hear "the world": dragons, gold, elves, dwarves, great mountains, adventure...
> 
> A day like others, you get a message in your mailbox: a dwarf king from the _Goro Mountains Peaks_ has heard from the mayor of the village, who keeps contact with him because they provide the village in stone, that you have great woodcraft skills. This dwarf king requests you to come to his castle in the mountains of the _Goro Peaks_ to participate to a great project...
>
> You decide to accept the deal, because of the great promiced remuneration. You'll travel into many places like the _Californ Woods_, the _Stall Fields_, and many other great places.
> ”

<details>

<summary>Check some gameplay shots:</summary>

![Screenshot from 2023-12-22 10-38-14](https://github.com/Dungeons-of-Kathallion/Bane-Of-Wargs/assets/87318892/5e47a039-fe02-49fa-ba29-1eb71fe5e955)
---
![Screenshot from 2023-12-22 10-37-59](https://github.com/Dungeons-of-Kathallion/Bane-Of-Wargs/assets/87318892/7a14c64f-1b0f-4fed-b4ca-4352a9cc540d)
---
![Screenshot from 2023-12-22 10-37-34](https://github.com/Dungeons-of-Kathallion/Bane-Of-Wargs/assets/87318892/02cdebb0-67f9-4ca0-816f-36ee844a8070)
---
![Screenshot from 2023-12-22 10-37-24](https://github.com/Dungeons-of-Kathallion/Bane-Of-Wargs/assets/87318892/2566d62f-d598-4080-8ecc-4de635dd0a3a)
---
![Screenshot from 2023-12-22 10-36-38](https://github.com/Dungeons-of-Kathallion/Bane-Of-Wargs/assets/87318892/691c3dd8-aa8d-4bda-b23b-1212c2ec9a96)
---
![Screenshot from 2023-12-22 10-33-00](https://github.com/Dungeons-of-Kathallion/Bane-Of-Wargs/assets/87318892/6109440f-bf8f-4394-8d3f-6dcaa1fd59f4)
---
![Screenshot from 2023-12-22 10-32-50](https://github.com/Dungeons-of-Kathallion/Bane-Of-Wargs/assets/87318892/ecde99f1-c451-46d9-9471-af36ed9849ea)
---
![Screenshot from 2023-12-22 10-30-30](https://github.com/Dungeons-of-Kathallion/Bane-Of-Wargs/assets/87318892/27c4d3d5-5908-4f64-96d2-c2c6356e85e6)
---
![Screenshot from 2023-12-22 10-28-05](https://github.com/Dungeons-of-Kathallion/Bane-Of-Wargs/assets/87318892/185860cf-80e3-4780-8932-1c15d9a441cf)
---
![Screenshot from 2023-12-22 10-27-55](https://github.com/Dungeons-of-Kathallion/Bane-Of-Wargs/assets/87318892/5aa608ba-11a2-417c-8a69-883313701ead)
---
![Screenshot from 2023-12-22 10-26-54](https://github.com/Dungeons-of-Kathallion/Bane-Of-Wargs/assets/87318892/7899e6c3-2d93-4f56-9e96-8031228daf50)
---
![Screenshot from 2023-12-22 10-26-31](https://github.com/Dungeons-of-Kathallion/Bane-Of-Wargs/assets/87318892/ac9d3b16-3e50-464e-833b-395e8f89f95f)
---
![Screenshot from 2023-12-22 10-26-00](https://github.com/Dungeons-of-Kathallion/Bane-Of-Wargs/assets/87318892/d7610cd5-87b0-4e40-a100-5b23360a3931)
---
![Screenshot from 2023-12-22 10-25-09](https://github.com/Dungeons-of-Kathallion/Bane-Of-Wargs/assets/87318892/f6edcccb-3fdb-4f8f-a04b-13fbc8c52be1)
---
![Screenshot from 2023-12-22 10-25-00](https://github.com/Dungeons-of-Kathallion/Bane-Of-Wargs/assets/87318892/12e2f30c-4639-404e-aa99-2fb14cd3fea3)
---

</details>

## Installing The Game

```
pip install -r requirements.txt
python source/main.py
```

**It's highly recommende to use a clean terminal in fullscreen for the best gameplay experience.**

_If you have any problems, check the full documentation on how to run the game from nothing at [`docs/PLAYING.MD`](https://github.com/Dungeons-of-Kathallion/Bane-Of-Wargs/blob/master/docs/PLAYING.md)._
_Note that you can also download the pre-built game executable from the [Continuous Build](https://github.com/Dungeons-of-Kathallion/Bane-Of-Wargs/releases/tag/9.9.9-continuous)._

## Building From Source

We recommend to build the game using the [PyInstaller](https://pyinstaller.org/en/stable/) program, but you could use any if you'd like, but we only support PyInstaller.There's a full documentation about building the game using PyInstaller at [`docs/BUILDING.md`](https://github.com/Dungeons-of-Kathallion/Bane-Of-Wargs/blob/master/docs/BUILDING.md).

## System Requirements

Bane Of Wargs is a minimal game but you will have to install/updated some python modules.
All required modules are in the `requirements.txt` file.

| Module    | PyPi Link                                                   | Version        |
|-----------|-------------------------------------------------------------|----------------|
| Fade      | https://pypi.org/project/fade/                              | latest-version |
| GitPython | https://pypi.org/project/GitPython/                         | latest-version |
| Colorama  | https://pypi.org/project/colorama/                          | latest-version |
| PyYaml    | https://pypi.org/project/PyYAML/                            | latest-version |
| Yamale    | https://pypi.org/project/yamale/                            | latest-version |
| Fsspec    | https://filesystem-spec.readthedocs.io/en/latest/index.html | latest-version |
| AppDirs   | https://pypi.org/project/appdirs/                           | latest-version |
| Requests  | https://pypi.org/project/requests/                          | latest-version |
| Rich      | https://pypi.org/project/rich/                              | latest-version |

---

_If you have previously ran the `pip install -r requirements.txt` command, you won't have to install all of theses modules since you already did._

## Contributing

As a free and open source game, the source code is accessible to reading and modifying. You can contribute to the game by creating a github issue [from here](https://github.com/Dungeons-of-Kathallion/Bane-Of-Wargs/issues/new/choose) to request a new feature or report a bug. You can propose your own changes by creating a [new pull request](https://github.com/Dungeons-of-Kathallion/Bane-Of-Wargs/pulls). Those who wish to contribute are recommended to checkout the [wiki](https://github.com/Dungeons-of-Kathallion/Bane-Of-Wargs/wiki) and the [CONTRIBUTING](https://github.com/Dungeons-of-Kathallion/Bane-Of-Wargs/blob/master/.github/CONTRIBUTING.md) guidelines.

## Development Progress

The planned game engine is currently in progress, and for the most of it done. The vanilla gameplay is not ready at all by you could always [create your own mod!](https://github.com/Dungeons-of-Kathallion/Bane-Of-Wargs/wiki/Creating-Mods). If you're interested by the game progress and development, check the wiki page about the [Goals](https://github.com/Dungeons-of-Kathallion/Bane-Of-Wargs/wiki/Game-Progression) of the game.

## Licensing

Bane Of Wargs is a free, open source game. The [source code](https://github.com/Dungeons-of-Kathallion/Bane-Of-Wargs/tree/master/source) and every file you will find on this repository is available under the [GPL v3 license](https://github.com/Dungeons-of-Kathallion/Bane-Of-Wargs?tab=GPL-3.0-1-ov-file#readme).
All its work and artwork is all public domain. Feel free to fork, or copy the game source to make your own version of the engine.
