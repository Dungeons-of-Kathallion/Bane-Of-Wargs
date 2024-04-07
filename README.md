# Bane Of Wargs (BETA)

```bash

████████████████████████████████████████████████████████████████████▀███████
█▄─▄─▀██▀▄─██▄─▀█▄─▄█▄─▄▄─███─▄▄─█▄─▄▄─███▄─█▀▀▀█─▄██▀▄─██▄─▄▄▀█─▄▄▄▄█─▄▄▄▄█
██─▄─▀██─▀─███─█▄▀─███─▄█▀███─██─██─▄██████─█─█─█─███─▀─███─▄─▄█─██▄─█▄▄▄▄─█
▀▄▄▄▄▀▀▄▄▀▄▄▀▄▄▄▀▀▄▄▀▄▄▄▄▄▀▀▀▄▄▄▄▀▄▄▄▀▀▀▀▀▀▄▄▄▀▄▄▄▀▀▄▄▀▄▄▀▄▄▀▄▄▀▄▄▄▄▄▀▄▄▄▄▄▀

╭────────────────────────────────────────────────────╮
│ 0> Play Game                                       │
│ 1> Manage Saves                                    │
│ 2> Preferences                                     │
│ 3> Gameplay Guide                                  │
│ 4> Check Logs                                      │
│ 5> Credits                                         │
│ 6> Quit                                            │
╰────────────────────────────────────────────────────╯
$ _
```
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
![Python Version](https://badgen.net/badge/python/3.12/blue?icon=python)
[![CD](https://github.com/Dungeons-of-Kathallion/Bane-Of-Wargs/actions/workflows/cd.yaml/badge.svg)](https://github.com/Dungeons-of-Kathallion/Bane-Of-Wargs/actions/workflows/cd.yaml)
[![Validate-YAML](https://github.com/Dungeons-of-Kathallion/Bane-Of-Wargs/actions/workflows/yaml_checks.yaml/badge.svg)](https://github.com/Dungeons-of-Kathallion/Bane-Of-Wargs/actions/workflows/yaml_checks.yaml)
[![Spell Checks](https://github.com/Dungeons-of-Kathallion/Bane-Of-Wargs/actions/workflows/spell_checks.yaml/badge.svg)](https://github.com/Dungeons-of-Kathallion/Bane-Of-Wargs/actions/workflows/spell_checks.yaml)
---

Bane Of Wargs is a python text-game engine with pre-built plots and the ability to create custom plugins/mods that completely change the game content. The game is very customizable and you will find many in-game features: equipment upgrading, items orders, mounts training over time, xp gaining, hp gaining, etc. This provides a very customizable and enjoyable python terminal-text based RPG.

You will have to fight monsters and bossses to get keys to unlock new areas on the map. The map is divided into points, determined by x and y coordinates, allowing maps up to 128x128 wide (so up to 16,384 places to explore), and more will be available as the engine progresses.

See the [Gameplay Guide](https://github.com/Dungeons-of-Kathallion/Bane-Of-Wargs/wiki/Gameplay-Guide) wiki page or check or the [Creating Mod](https://github.com/Dungeons-of-Kathallion/Bane-Of-Wargs/wiki/Creating-Mods) wiki page if you're interested in modding the game.

---

Here's the vanilla starting dialog plot:
> “
> You're a lumberjack who lives in a small village in the _Forlindon Woods_, a quiet a calm place to live. You've always wondered what's after this quiet forest; because your little village is a small town that lives apart from the other great cities in the _Stall Island_, _Kathallion Archipelago_. You've heard some stories and tales about the rest of the world. Only some words come to your mind when you hear "the world": dragons, gold, elves, dwarfs, great mountains, adventure...
>
> A day like others, you get a message in your mailbox: a dwarf king from the _Goro Mountains Peaks_ has heard from the mayor of the village, who keeps contact with him because they provide the village in stone, that you have great woodcraft skills. This dwarf king requests you to come to his castle in the mountains of the _Goro Peaks_ to participate to a great project...
>
> You decide to accept the deal, because of the great promiced remuneration. You'll travel into many places like the _Californ Woods_, the _Stall Fields_, and many other great places.
> ”

<details>

<summary>Check some gameplay shots:</summary>

![Screenshot from 2024-03-15 19-10-58](https://github.com/Dungeons-of-Kathallion/Bane-Of-Wargs/assets/87318892/027e11fe-cf7b-4f08-9e24-9bb165fb089f)
---
![Screenshot from 2024-03-15 19-10-44](https://github.com/Dungeons-of-Kathallion/Bane-Of-Wargs/assets/87318892/4db77509-edcf-4124-945c-b62ecde4b677)
---
![Screenshot from 2024-03-15 19-10-21](https://github.com/Dungeons-of-Kathallion/Bane-Of-Wargs/assets/87318892/22630735-c39a-4d31-aaeb-ecc9dc555440)
---
![Screenshot from 2024-03-15 19-10-10](https://github.com/Dungeons-of-Kathallion/Bane-Of-Wargs/assets/87318892/937e8139-6f6a-4e6f-a9d2-10c2c54b6e0a)
---
![Screenshot from 2024-03-15 19-10-06](https://github.com/Dungeons-of-Kathallion/Bane-Of-Wargs/assets/87318892/a4bd5464-87fa-486b-9e89-f0172532edeb)
---
![Screenshot from 2024-03-15 19-09-58](https://github.com/Dungeons-of-Kathallion/Bane-Of-Wargs/assets/87318892/96e980d1-d085-429e-b056-597194177157)
---
![Screenshot from 2024-03-15 19-09-43](https://github.com/Dungeons-of-Kathallion/Bane-Of-Wargs/assets/87318892/5e134855-46a2-496a-a8db-0326b9561b10)
---
![Screenshot from 2024-03-15 19-09-08](https://github.com/Dungeons-of-Kathallion/Bane-Of-Wargs/assets/87318892/1162ed85-d2b1-4b81-81a1-925f42713b28)
---
![Screenshot from 2024-03-15 19-08-44](https://github.com/Dungeons-of-Kathallion/Bane-Of-Wargs/assets/87318892/ccbeb0db-d5e4-4b27-9f7d-11e561e12dd4)
---
![Screenshot from 2024-03-15 19-08-29](https://github.com/Dungeons-of-Kathallion/Bane-Of-Wargs/assets/87318892/bc6aa333-bcf3-4bf2-b9d2-2c28d1a1f634)
---
![Screenshot from 2024-03-15 19-08-17](https://github.com/Dungeons-of-Kathallion/Bane-Of-Wargs/assets/87318892/e323d2a4-103f-4ecc-9da0-947ab5b03c3e)
---
![Screenshot from 2024-03-15 19-07-40](https://github.com/Dungeons-of-Kathallion/Bane-Of-Wargs/assets/87318892/7d1cea75-ec80-4ca6-b098-5191584e0e29)
---
![Screenshot from 2024-03-15 19-06-56](https://github.com/Dungeons-of-Kathallion/Bane-Of-Wargs/assets/87318892/53a7c07d-15eb-4002-bddc-f40ab4b327e5)
---
![Screenshot from 2024-03-15 19-06-33](https://github.com/Dungeons-of-Kathallion/Bane-Of-Wargs/assets/87318892/85754f0d-fc1b-4cf4-8226-1962a050628d)
---
![Screenshot from 2024-03-15 19-06-23](https://github.com/Dungeons-of-Kathallion/Bane-Of-Wargs/assets/87318892/1b33bfc7-feb3-4404-8267-3a4f8de3f817)
---
![Screenshot from 2024-03-15 19-06-08](https://github.com/Dungeons-of-Kathallion/Bane-Of-Wargs/assets/87318892/e3de6e0e-1b5f-4da2-8e23-333046ac7a16)
---
![Screenshot from 2024-03-15 19-05-39](https://github.com/Dungeons-of-Kathallion/Bane-Of-Wargs/assets/87318892/88144fe6-ae0c-4027-8667-bd52713bb527)
---
![Screenshot from 2024-03-15 19-05-23](https://github.com/Dungeons-of-Kathallion/Bane-Of-Wargs/assets/87318892/4333249c-c50b-42e9-b377-9646e01782a7)
---
![Screenshot from 2024-03-15 19-05-02](https://github.com/Dungeons-of-Kathallion/Bane-Of-Wargs/assets/87318892/f4990255-7f2e-4e76-a0f1-6da970f90070)
---
![Screenshot from 2024-03-15 19-04-47](https://github.com/Dungeons-of-Kathallion/Bane-Of-Wargs/assets/87318892/ab69ab07-d780-4b9d-ba75-de8ff6c3e86f)
---
![Screenshot from 2024-03-15 19-04-18](https://github.com/Dungeons-of-Kathallion/Bane-Of-Wargs/assets/87318892/a464e761-d67a-4fce-b5bf-03650618dd96)
---
![Screenshot from 2024-03-15 19-04-06](https://github.com/Dungeons-of-Kathallion/Bane-Of-Wargs/assets/87318892/bbe57829-d879-42e0-b005-dd00e98b41d6)
---
![Screenshot from 2024-03-15 19-03-45](https://github.com/Dungeons-of-Kathallion/Bane-Of-Wargs/assets/87318892/00271e64-78be-4638-ad34-3726d5eb45b8)
---
![Screenshot from 2024-03-15 19-03-14](https://github.com/Dungeons-of-Kathallion/Bane-Of-Wargs/assets/87318892/f9828aea-e5f1-4908-8ca6-e3716580964b)
---
![Screenshot from 2024-03-15 19-02-57](https://github.com/Dungeons-of-Kathallion/Bane-Of-Wargs/assets/87318892/d28eab41-ab2f-4665-9a2b-36da62219c6c)
---
![Screenshot from 2024-03-15 19-02-14](https://github.com/Dungeons-of-Kathallion/Bane-Of-Wargs/assets/87318892/bbecaf2c-7766-48b5-8a24-eca909450597)
---
![Screenshot from 2024-03-15 19-01-29](https://github.com/Dungeons-of-Kathallion/Bane-Of-Wargs/assets/87318892/311137a4-c213-4968-a1c2-fa9585e562da)
---
![Screenshot from 2024-03-15 19-01-12](https://github.com/Dungeons-of-Kathallion/Bane-Of-Wargs/assets/87318892/f74178db-e9c0-4c08-9abf-df3ddc25cd9c)
---

</details>

## Installing The Game

```
pip install -r requirements.txt
python source/main.py
```

**It's highly recommended to use a clean terminal with the ability to zoom in or out. It is also recommended to use fullscreen with a monospace font for the best gameplay experience.**

_If you have any problems, check the full documentation on how to run the game from nothing at [`docs/PLAYING.MD`](https://github.com/Dungeons-of-Kathallion/Bane-Of-Wargs/blob/master/docs/PLAYING.md)._
_Note that you can also download the pre-built game executable from the [Continuous Build](https://github.com/Dungeons-of-Kathallion/Bane-Of-Wargs/releases/tag/9.9.9-continuous)._

## Building From Source

We recommend to build the game using the [PyInstaller](https://pyinstaller.org/en/stable/) program, but you could use any if you'd like, but we only support PyInstaller.There's a full documentation about building the game using PyInstaller at [`docs/BUILDING.md`](https://github.com/Dungeons-of-Kathallion/Bane-Of-Wargs/blob/master/docs/BUILDING.md).

## System Requirements

Bane Of Wargs is a minimal game (requires a small number of dependencies), but you will have to install/update some python modules.
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

_If you have already run the `pip install -r requirements.txt` command, then you won't have to install these modules as they were installed for you._

## Contributing

As a free and open source game, the source code is accessible to reading and modifying. You can contribute to the game by creating a github issue [from here](https://github.com/Dungeons-of-Kathallion/Bane-Of-Wargs/issues/new/choose) to request a new feature or report a bug. You can propose your own changes by creating a [new pull request](https://github.com/Dungeons-of-Kathallion/Bane-Of-Wargs/pulls). Those who wish to contribute are recommended to checkout the [wiki](https://github.com/Dungeons-of-Kathallion/Bane-Of-Wargs/wiki) and the [CONTRIBUTING](https://github.com/Dungeons-of-Kathallion/Bane-Of-Wargs/blob/master/.github/CONTRIBUTING.md) guidelines.

## Development Progress

The planned game engine is currently in progress, and for the most of it done. The vanilla gameplay is not ready at all by you could always [create your own mod!](https://github.com/Dungeons-of-Kathallion/Bane-Of-Wargs/wiki/Creating-Mods). If you're interested by the game progress and development, check the wiki page about the [Goals](https://github.com/Dungeons-of-Kathallion/Bane-Of-Wargs/wiki/Game-Progression) of the game.

## Licensing

Bane Of Wargs is a free, open source game. The [source code](https://github.com/Dungeons-of-Kathallion/Bane-Of-Wargs/tree/master/source) and every file you will find on this repository is available under the [GPL v3 license](https://github.com/Dungeons-of-Kathallion/Bane-Of-Wargs?tab=GPL-3.0-1-ov-file#readme).
All its work and artwork is all [copyrighted](https://github.com/Dungeons-of-Kathallion/Bane-Of-Wargs/blob/master/copyright) and [credited](https://github.com/Dungeons-of-Kathallion/Bane-Of-Wargs/blob/master/credits.txt). Feel free to fork, or copy the game source to make your own version of the engine.
