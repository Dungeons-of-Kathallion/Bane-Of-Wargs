# Introduction

Even if the game is coded in python which is a very simple and multi-platform compatible language and is made to be played the most easiest way possible; if you've never used programs like this, or if you've never ran programs manually or just don't know how to install python; it can be difficult and scary to run this game/program.

In this document, you'll find very in-depth documentation about installing this game from nothing. You'll find a small summary under this paragraph to find where you should start.

### Summary

* [Get Python Installed (Windows, Linux, MacOS)](#get-python-installed-windows-linux-macos)
* [Getting The Game](#getting-the-game)
* [Getting Required Modules/Libraries Installed & Possibly Fix Issues](#getting-required-moduleslibraries-installed--possibly-fix-issues)
* [Run The Game & Possibly Fix Issues](#run-the-game--possibly-fix-issues)

## Step-By-Step Guide

### Get Python Installed (Windows, Linux, MacOS)

Depending on your operation system or your distribution if you're running a linux computer, the methods are very different. Methods will be separated on 3 cases: Windows, Linux Distributions and MacOS. Note that only Windows 10 and 11 will be covered in this guide.

#### // Windows //

##### 1 // Downloading The Python Installer

1. Go to the official [Python download page for Windows](https://www.python.org/downloads/windows/).
2. Find the latest stable version.
3. Click the appropriate link for your system to download the executable file: **Windows installer (64-bit)** or **Windows installer (32-bit)**.
![python-download-page-windows](https://deved-images.nyc3.cdn.digitaloceanspaces.com/CONTINT-1526%2Fpy_download.png)

##### 2 // Running the Executable Installer

1. After you downloaded the installer, run the `.exe` file to run the Python installer.
2. Select the **Install launcher for all users** checkbox, which enables installation of the python environment for all users of this computer.
3. Select the **Add python.exe to PATH** checkbox, which enables users to access to python at any location in their terminal.
![python-installer-windowds](https://deved-images.nyc3.cdn.digitaloceanspaces.com/CONTINT-1526%2Fpy_download.png)
4. If you’re just getting started with Python and you want to install it with default features as described in the dialog, then click **Install Now**. To install other optional and advanced features, click **Customize installation** and continue.
5. The **Optional Feature** include common tools and resources for Python and you can install all of them, even if you don't plan using them. You'll need to check the `pip` box since this program uses external Python modules/libraries. Other boxes are just optional for this program.
![python-optional-features-windows](https://deved-images.nyc3.cdn.digitaloceanspaces.com/CONTINT-1526%2Fpy-installer-optional.png)
6. Click **Next**.
7. The **Advanced Options** dialog displays.
    ![python-advanced-options-windows](https://deved-images.nyc3.cdn.digitaloceanspaces.com/CONTINT-1526%2Fpy-installer-advanced.png)

* **Install for all users**: recommended if you’re not the only user on this computer.
* **Associate files with Python**: recommended, because this option associates all the Python file types with the launcher or editor.
* **Create shortcuts for installed applications**: recommended to enable shortcuts for Python applications.
* **Add Python to environment variables**: recommended to enable launching Python.
* **Precompile standard library**: not required, it might down the installation.
* **Download debugging symbols and Download debug binaries**: recommended only if you plan to create C or C++ extensions.
This program requires to check the **Add Python to environment variables**. Make note of the Python installation directory in case you need to reference it later.
1. Click **Install** to start the installation
2. After the installation is complete, a **Setup was successful** message displays.
![setup-was-successful-windows](https://deved-images.nyc3.cdn.digitaloceanspaces.com/CONTINT-1526%2Fpy-installer-success.png)

##### 3 // Verify the Python Installation

You can verify whether the Python installation is successful either through the command line or through the Integrated Development Environment (IDLE) application, if you chose to install it.

Go to **Start** and enter cmd in the search bar. Click **Command Prompt**.

Enter the following command in the command prompt:
```
python --version
```
An example of the output is:
```
Output
Python 3.12.2
```

##### 4 // Credits

Since myself, @OcelotWalrus I'm running a Linux computer, this guide for installing Python on windows in completely taken from this website: https://www.digitalocean.com/community/tutorials/install-python-windows-10.

#### // Linux //

If you're using a linux computer, you've probably already used python or at least you're used to the command line. Know that python comes already installed with most Linux Distributions. If you don't know if you have python installed, you can just run the command below:

```
python --version
```

So as I said sooner, most Linux Distributions come with Python installed, so if it's the case for you, skip the 1st step and got directly to the 2nd ste

##### 1 // Installing Python environment

First, before installing, you'll need to have [sudo](https://www.pluralsight.com/resources/blog/cloud/linux-commands-for-beginners-sudo) access on the system.

1. Installing from the package manager

RPM-based distros:
```
sudo dnf install python
# or
sudo yum install python
```
DEB-based distros:
```
sudo apt-get install python
```

2. Verifying Python installation and check if you've already PIP (Python Package Manager) installed
```
python --version
```
To check for Python installation.

##### 2 // Installing PIP (Python Package Manager)

First, you'll need to check if pip is already installed on your system.
```
pip -V
```

If you don't have pip installed then, follow these steps:
1. First, get the installer
```
wget https://bootstrap.pypa.io/get-pip.py
```
2. Next, run the installer
```
python get-pip.py
```

Now, you should have pip installed. To use pip, run `python -m pip`. You can also alternatively install pip from a package manager, which is better because you would just have to run the `pip` command on the terminal, but it will not be covered in this guide.

You can get more information about pip [here](https://www.w3schools.com/python/python_pip.asp).

#### // MacOS //

Installed Python on MacOs is very similar to installing Python on Windows, you'll just have to download the installer and then install it.

##### 1 // Python Installer

1. Go to the [official Python website](https://www.python.org/downloads/macos/) to access the download page for the latest version of Python for MacOS
2. Download the Installer
3. On the Download page, you'll find the MacOS installers packages (.pkg files). Download the latest stable version.
4. Run the installer. Proceed through the installation steps by agreeing to the software license agreement, choosing the installation location (we recommend using the default location), and entering your administrator password when prompted.
Make sure to have pip installed.
![python-installer-macos](https://kinsta.com/wp-content/uploads/2023/04/python-mac-installer.png)
5. Verify the installation by running `python --version`

##### 2 // Credits
Since I'm a linux user and I don't own currently any mac book, i taken all these instructions from this website:
https://kinsta.com/knowledgebase/install-python/#mac

### Getting The Game

To get the game you have two methods: either cloning the github repository from the command or either download the zip folder of the game. It's recommended to get the game by the first method because you will be able to update the game simply by running a simple command, but it requires having [git](https://git-scm.com/) installed. While the second methods doesn't require git, you'll have to re-download the game every time you want to update the game.

#### // Git Cloning //

As I said sooner, you'll need to have [git](https://git-scm.com/) installed to use this method. This guide doesn't cover installing git but here's a good guide for that:
https://github.com/git-guides/install-git

1. Decide if you want to use https or ssh to clone. (https://www.warp.dev/terminus/git-clone-ssh#cloning about the difference between https and ssh)
2. Clone using your favorite method
```
git clone https://github.com/Dungeons-of-Kathallion/Bane-Of-Wargs.git
# or
git clone git@github.com:Dungeons-of-Kathallion/Bane-Of-Wargs.git
# or
gh repo clone Dungeons-of-Kathallion/Bane-Of-Wargs
```

3. Check that the fold Bane-Of-Wargs is on your computer.

#### // Zip Download //

Note that with this method, automatic or semi-automatic update will not work. You'll have to re-download the game.

1. Go to the Bane Of Wargs github repo main page.
https://github.com/Dungeons-of-Kathallion/Bane-Of-Wargs
2. Click on the **`<> Code`** button.
![github-code-button](https://github.com/Dungeons-of-Kathallion/Bane-Of-Wargs/assets/87318892/d6e26d4f-26a3-45d0-a3dc-aae0adc84eb5)
3. Once the pop-up open, click on the **Download Zip** button.
![download-zip-button-github](https://github.com/Dungeons-of-Kathallion/Bane-Of-Wargs/assets/87318892/4cc54250-0979-4a54-90aa-17a6731db104)
The download should start quickly.

### Getting Required Modules/Libraries Installed & Possibly Fix Issues

#### Introduction

Like most python programs, it's very rare that it only requires the default packages coming with the Python environment. This program requires 6 python modules/libraries.
All of these modules/libraries are contained in the [requirements.txt](https://github.com/Dungeons-of-Kathallion/Bane-Of-Wargs/blob/master/requirements.txt) file.

* **[fade](https://pypi.org/project/fade/)** // the modules that makes the game title fade possible.
* **[GitPython](https://pypi.org/project/GitPython/)** // the modules that makes updating the game from the github repository while being in-game possible.
* **[colorama](https://pypi.org/project/colorama/)** // the module that makes displaying colored text in terminal easier.
* **[PyYaml](https://pypi.org/project/PyYAML/)** // the module that makes using yaml files as a data base for the game possible.
* **[yamale](https://pypi.org/project/yamale/)** // the module that makes the verification and debug by the game of every opened yaml files by the program possible.
* **[fsspec](https://filesystem-spec.readthedocs.io/en/latest/index.html)** // the module that makes downloading game data from the github repository and moving them to the game data folder possible.
* **[appdirs](https://pypi.org/project/appdirs/)** // the module that make cross-platform game config and data storing in users directories possible
* **[requests](https://pypi.org/project/requests/)** // the module that makes downloading game data from the github repository and moving them to the game data folder possible.
* **[rich](https://pypi.org/project/rich/)** // the module that make displaying markdown files in terminal possible

#### Installing

To install all these modules you can simply run:
```
pip install -r requirements.txt
# or
python -m pip install -r requirements.txt
```
while being on the root of the game directory.

You can after run `pip freeze` #or `python -m pip freeze` to check if all packages have been installed.

### Run The Game & Possibly Fix Issues

#### Introduction

We're almost done here. In this final step you'll run the game and finally be able to play it and create plugins for it.

#### Running with the Python command
First go to the root of the repository with your terminal by using the **`cd`** command.
Depending on how you installed python, you will run the game differently but it's the same way.

```
python source/main.py
# or
python3 source/main.py
#or
python<x.x> source/main.py #x.x is for example 3.7 for the version 3.7
```

##### Additional: Compiling & Building
If you want to take the game to a next level, you can compile the game by following the instructions of the [`docs/BUILDING.md`](https://github.com/Dungeons-of-Kathallion/Bane-Of-Wargs/blob/master/docs/BUILDING.md) documentation.

#### Fixing Possible Issues

Here are the common issues that can happen and crash the game while trying to run it for the first time:

##### "No such module" //

If you have an error about modules or libraries, it's that you didn't installed correctly the required dependencies. Get back to [Getting Required Modules/Libraries Installed & Possibly Fix Issues](#getting-required-moduleslibraries-installed--possibly-fix-issues).

##### "Could not find save file 'saves/save_ .yaml'" //
If this message displays in red after selecting the **`Use Latest Preset`** in the **`Play Game`** menu, it's because you've never played the game before and because you don't have any save yet.
Instead of choosing **`Use Latest Preset`**, choose **`Play Vanilla`** and create a new save. Next time you'll press the **`Use Latest Preset`**, it should work.

##### "A parsing error in a yaml file has been detected: Error validating data with schema [...]" //
If you encounter this error, it's probably because you're using a plugin or because you modified the game vanilla data locally and made an error. If you did, there should be a debug message to help you understand what's wrong.
If you didn't modified locally the vanilla data, please report the bug by creating a github issue [here](https://github.com/Dungeons-of-Kathallion/Bane-Of-Wargs/issues/new/choose) or by sending me an email at angelo.longo13@outlook.com.
If this error is encountered while using a plugin not made by you, please report the issue to the plugin developer(s).

##### Any other weird errors //

If you have some weird errors, it's probably because you have an outdated version of python. Get the latest stable version of Python or update your current one.
