This is an automated build triggered by commit ${{ github.sha }} (@${{ github.actor }}). It may be unstable or even crash, corrupt your save or eat your kitten. Use with caution!
This release was made to be compatible with the **3.12 python version** and the **latest release of the required python module**.

_Certain features will not work with earlier version of python._

### To Use

#### Using Pre-Built Executable
Download one of the possible executables, depending on your OS, the download the requirements:
```bash
pip install fade GitPython colorama PyYaml yamale fsspec appdirs requests rich
```
Then run the executable.

#### Using Source Code
```bash
git clone https://github.com/Dungeons-of-Kathallion/Bane-Of-Wargs.git
cd Bane-Of-Wargs
pip install -r requirements.txt
python source/main.py
```
_If you have an issues trying to install the game, please refer to the [`docs/PLAYING.md`](https://github.com/Dungeons-of-Kathallion/Bane-Of-Wargs/blob/master/docs/PLAYING.md) guide._
_Find a guide to build the game yourself at the [`docs/BUILDING.md`](https://github.com/Dungeons-of-Kathallion/Bane-Of-Wargs/blob/master/docs/BUILDING.md) document._
