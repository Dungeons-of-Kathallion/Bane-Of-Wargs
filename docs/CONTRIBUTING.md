# Index
- [Index](#index)
- [Issues](#issues)
    - [Opening](#opening)
    - [Closing](#closing)
- [Pull Requests](#pull-requests)
    - [Opening](#opening-1)
    - [Merging](#merging)
    - [Abandoned Pull Requests](#abandoned-pull-requests)
- [For Collaborators](#for-collaborators)
    - [Dealing With Your Own Pull Requests](#dealing-with-your-own-pull-requests)
  - [Duties](#duties)
    - [coder](#coder)
    - [documentation reviewers](#documentation-reviewers)
    - [playtester](#playtester)
    - [inflow control](#inflow-control)
  - [Naming conventions](#naming-conventions)
  - [Code Style](#code-style)
  - [Merging Pull Requests](#merging-pull-requests)

# Issues
### Opening
If you happen to find an error in the program or wiki, or if there's a feature you want and cannot program it immediately, please create an issue.
### Closing
Once the error is fixed, or the feature request is added or rejected, your issue should be closed.

# Pull Requests
### Opening
1. Fixing issues

If you know how to address an issue with a pull request, please do. However, I ask you to make sure you do some things: `1) Mention the issue; I will link the issue and pull request together, 2) TEST YOUR CODE! 3) Explain what your change does.`

2. Your own idea

If you find a bug in the code and can quickly fix it, please create a pull request. It should be merged shortly, if you fix it correctly. If you have an addition to the code, there's a checklist for you to fill out. `1) TEST YOUR CODE! 2) Explain what your new code does and how it would be useful.`

### Merging
Once an admin sees your PR, they may review it. Other people who have no merging permissions may also review your pull request. If you have requested changes, please address them; either explain why the requested change should not be added to your PR or fix them. Once you address the reviews, the reviewers should either explain why they do not thing the reviews are addressed, submit more requested changes, or approve the PR. Once and admin approves a PR, they may merge it.

### Abandoned Pull Requests
Sometimes something happens and someone cannot continue working on their pull request. They are requested to say that, but if they cannot the pull request will be left for one month and then closed.

# For Collaborators
### Dealing With Your Own Pull Requests
It's requested that you do not merge your own pull request, unless it has: `1) No requested reviews, 2) At least one approval from the team, and 3) Have at least two total reviewers, not counting the one approval`

## Duties
Once you have permissions on this repo or in the organization, you have a role that means you should have more involvement. There are several different roles, however, defined by teams.

### coder
The coder is in charge of developing the game; creating pull requests to expand it. They also give coding suggestions in reviews. They do not merge pull requests.

_Permission: Read_

### documentation reviewers
The job of documentation reviewers is to keep the wiki up to date. They do not merge pull requests.

_Permission: Read_

### playtester
A playtester is someone who will test out PRs and check for bugs while playing. They do not merge pull requests.

_Permission: Read_

### inflow control
Everyone in inflow control has the power to merge pull requests and assign labels. They will usually be in another team. Their job is to merge pull requests and add/remove labels.

_Permission: Write_

## Naming conventions
You are requested to name commits in a certain style:
You'll use the following syntax:
```yaml
<name>[<major | minor>] - <commit compact description>
```

* `<name>` // Should be replaced by one of the name in this table:

| Name            | Use case                                                                                       |
|-----------------|------------------------------------------------------------------------------------------------|
| `progress`        | if it has something to do with game data and game vanilla plot progression                     |
| `content/feature` | if it adds new content/features to the game that aren't planned in the game engine/vanilla plot progression
| `tweak`           | if it tweaks anything in the repository                                                        |
| `bugfix`          | if it fixes a bug                                                                              |
| `fix`             | if it fixes anything that is not a bug (do not make crash the program or does something wrong) |
| `refactor`        | if it refactors any word. at the end of the commit description, put "`before`-->`after`"       |
| `documentation`   | if it changes something in the `docs/` folder                                                  |
| `update`          | if it updates anything outdated like documentation etc...                                      |
| `workflow_<name>` | if it changes somethings in the `.github/workflows` folder                                     |
| `unspecified`     | anything not in this list                                                                      |
* Optionally, you can add "`[major]`" or "`[minor]`" after "`<name>`" if you feel it's needed.
* Please make your commit description the most compact, understandable and changes-related possible.

## Code Style
In order to make the code clean, optimized and themed, so that everyone can understand it better, we have a code style convention. Apart from keeping the code clean, optimized and themed, it keeps the code organized. We have different github actions that check the code style and syntax for you automatically when you create a pull request to the master branch of the Bane-Of-Wargs repo. Theses checks are required to be passing for the pull request to be merged by an inflow control or an admin. These checks verify the yaml data present in the `data/` directory (the actual yaml syntax and if the data is correct for it to work in the game engin), the spelling across most files, if the program compiles right, and finally, the actual python code style & syntax. The spelling should be american and not any other (british etc...). If every game engine class gets added/removed/updated, make sure the game engine documentation ([`ENGINE_FUNCTIONS.md`](https://github.com/Dungeons-of-Kathallion/Bane-Of-Wargs/blob/master/docs/ENGINE_FUNCTIONS.md)) gets updated.

Every python script or data file should have a copyright header:

```html
# python_script.py //only if it's a script
# Copyright (c) 2024 by <creator>
#
# Bane Of Wargs is free software: you can redistribute it and/or modify it under the
# terms of the GNU General Public License as published by the Free Software
# Foundation, either version 3 of the License, or (at your option) any later version.
#
# Bane Of Wargs is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
# PARTICULAR PURPOSE. See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with
# this program. If not, see <https://www.gnu.org/licenses/>.
```

Here are the main code style conventions:

- **For yaml files**:
  - braces and brackets have a maximum space inside of 1 (level: warning)
  - non-logical placement of colons and commas (level: warning)
  - document start is disabled (you don't need to start a document with a `---`)
  - empty lines (level: warning)
  - hyphens (level: warning)
  - indentation should be 2 spaces
  - maximum line length of 200 characters and allow non-breakable inline mappings (level: warning)
- **For python files (in the `source/` directory)**:
  - We use default python [pycodestyle](https://pypi.org/project/pycodestyle/) module checks with a maximum line length of 130 characters
  - You shouldn't worry about that checks too much

## Merging Pull Requests
When you merge a pull request, please `Squash Merge`, remove commit listing, use the [naming convention](#naming-conventions), and add extra details if necessary. You do not have to use the name of a PR in the commit name. Note that before merging, every github action checks must be passing. If the PR you're merging updates the `GAME_SOURCE_CODE_VERSION` and `GAME_DATA_VERSION` constants in the `main.py` class, please specify it in the commit description.
