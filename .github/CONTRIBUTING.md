# Issues
### Opening
If you find an error in the progam or wiki, or if there is a feature you want and cannot program it immediately, please create an issue.
### Closing
Once the error is fixed, or the feature request is added or rejected, your issue should be closed.

# Pull Requests
### Opening
1. Fixing issues

If you know how to address an issue with a pull request, please do. However, I ask you to make sure you do some things: 1) Mention the issue; I will link the issue and pull request together, 2) TEST YOUR CODE! 3) Explain what your change does.

2. Your own idea

If you find a bug in the code and can quickly fix it, please create a pull request. It should be merged shortly, if you fix it correctly. If you have an addition to the code, there is a checklist for you to fill out. 1) TEST YOUR CODE! 2) Explain what your new code does and how it would be useful.

### Merging
Once an admin sees your PR, they may review it. Other people who have no mergine permissions may also review your pull request. If you have requested changes, please address them; either explain why the requested change should not be added to your PR or fix them. Once you address the reviews, the reviewers should either explain why they do not thing the reviews are addressed, submit more requested changes, or approve the PR. Once and admin approves a PR, they may merge it.

### Abandoned Pull Requests
Sometimes something happens and someone cannot continue working on their pull request. They are requested to say that, but if they cannot the pull request will be left for oen month and then closed.

# For Collaborators
### Dealing With Your Own Pull Requests
It is requested that you do not merge your own pull request, unless it has: 1) No requested reviews, 2) At least three approvals, and 3) Have at least five total reviewers.

## Duties
Once you have permissions on this repo or in the organization, you have a role that means you should have more involvement. There are several different roles, however, defined by teams.

### coder
The coder is in charge of developing the game; creating pull requests to expand it. They also give coding suggestions in reviews. They do not merge pull requests.

Permission: Read

### documentation reviewers
The job of documentation reviewers is to keep the wiki up to date. They do not merge pull requests.

Permission: Read

### playtester
A playtester is someone who will test out PRs and check for bugs while playing. They do not merge pull requests.

Permission: Read

### inflow control [placeholder name]
Everyone in inflow control has the power to merge pull requests and assign labels. They will usually be in another team. Their job is to merge pull requests and add/remove labels.

Permission: Write

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
| `tweak`           | if it tweaks anything in the repository                                                        |
| `bugfix`          | if it fixes a bug                                                                              |
| `fix`             | if it fixes anything that is not a bug (do not make crash the program or does something wrong) |
| `refactor`        | if it refactors any word. at the end of the commit description, put "`before`-->`after`"       |
| `documentation`   | if it changes something in the `docs/` folder                                                  |
| `update`          | if it updates anything outdated like documentation etc...                                      |
| `workflow_<name>` | if it changes somethings in the `.github/workflows` folder                                     |
| `unspecified`     | anything not in this list                                                                      |
* Optionaly, you can add "`[major]`" or "`[minor]`" after "`<name>`" if you feel it's needed.
* Please make your commit description the most compact, understandable and changes-related possible.

## Merging Pull Requests
When you merge a pull request, please `Squash Merge`, remove commit listing, use the [naming convention](#naming-conventions), and add extra details if necessary. You do not have to use the name of a PR in the commit name.
