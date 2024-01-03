# Bane Of Wargs

```
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

---

Bane Of Wargs is a python text-game engine with pre-built plot an the ability to create custom pugins/mods that complitely change the game content. The game is very customizable and you will find ton of in-game features: equipment upgrading, items orders, mounts training over time, xp gaining, hp gaining etc... So in overall a very customizable and enjoyable python terminal-text based RPG.

You will have to fight monsters, bossses to get keys to after unlock new places of the map. The map is divised in points, determined by x and y coordinates, letting the possibility to map up to 128x128 wide, and more in the future of the engine development.

See the [Gameplay Guide](https://github.com/Dungeons-of-Kathallion/Bane-Of-Wargs/wiki/Gameplay-Guide) wiki page or check or the [Creating Mod](https://github.com/Dungeons-of-Kathallion/Bane-Of-Wargs/wiki/Creating-Mods) wiki page if you're interested in modding the game.

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

## To Play

```
pip install -r requirements.txt
python main.py
```
**It's highly recommende to use a clean terminal in fullscreen for the best gameplay experience.**

If you have any problems, check the full documentation on how to run the game fron nothing at [`docs/PLAYING.MD`](https://github.com/Dungeons-of-Kathallion/Bane-Of-Wargs/blob/master/docs/PLAYING.md).

## Python Module Requirements

Bane Of Wargs is a minimal game but you will have to install/updated some python modules.\n
All required modules are in the `requirements.txt` file.
[enquiries](https://pypi.org/project/enquiries/), [fade](https://pypi.org/project/fade/), [GitPython](https://pypi.org/project/GitPython/), [colorama](https://pypi.org/project/colorama/), [PyYaml](https://pypi.org/project/PyYAML/), [Yamale](https://pypi.org/project/yamale/), [Fsspec](https://filesystem-spec.readthedocs.io/en/latest/index.html).

---

_If you have previously ran the `pip install -r requirements.txt` command, you won't have to install all of theses modules since you already did._

## Contrbuting

All conributions like PR, issues that can go from bug reporting or feature request are all welcome!\n
Just check the [CONTRIBUTING](https://github.com/Dungeons-of-Kathallion/Bane-Of-Wargs/blob/master/.github/CONTRIBUTING.md) guidelines.

## Progress

Beta is out! Most of the planned engine features are developed!\n
If you're interested by the game progress and development, check the wiki page about the [Goals](https://github.com/Dungeons-of-Kathallion/Bane-Of-Wargs/wiki/Game-Progression) of the game.

## Licensing

Bane Of Wargs is a free, open source game. The source code and every file you will find on this repository is avaible under the GPL v3 license.\n
All its work and artwork is all public domain. Feel free to fork, or copy the game source to make your own version of the engine.
