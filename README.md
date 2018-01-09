# UConn-Taiko-Battlecode
Repository for UConn Taiko (#707) - Battlecode

## Team Members
* Adomous Wright
* Eli Udler
* Rania Chowdhury
* Robert Miller

## Setup

### 1. Download Git

* https://git-scm.com/downloads

* Go to the website linked above and download Git Bash
* During installation, leave the settings to the default configuration

### 2. Fork ADWright2018/UConn-Taiko-Battlecode

* https://github.com/ADWright18/UConn-Taiko-Battlecode

* Navigate the link above and click the "Fork" option in the upper-right hand corner
* (Username)/UConn-Taiko-Battlecode should be created

### 3. Local Repository Configuration

* In the Windows Start Menu, search and open "Git Bash"
* A bash terminal will open
* Make a new directory called "repo" -

```
mkdir repo
```

* Open "repo" and clone your fork of the project

```
cd repo
git clone https://github.com/(Username)/UConn-Taiko-Battlecode.git
```

* Now you should have an up-to-date copy of the master/fork in a local directory
* 'UConn-Taiko-Battlecode' should be in 'repo'

## Change Workflow

* Changes will be initiated by creating/updating branches which can be pulled into the master
* Before making any changes, make sure your fork/local repository is up-to-date with the master branch
* Refer to the link below for "Merging an upstream repository into your fork"

* https://help.github.com/articles/merging-an-upstream-repository-into-your-fork/

### 1. Creating a new branch

* To create a branch, click "Branch: master" and a search bar with a dropdown menu should appear
* Type the name of branch - ex. update-readme or feat-robot, then hit enter
* The branch will be created based on _your_ master branch

### 2. Accessing a new branch

* Fetch the new branch/branches
```
git fetch
```

* Check out and edit the new branch
```
git checkout (branch-name)
```

* Now you should be able to make edits to the branch without affecting the master branch

### 3. Stage changes

* Check the status of the branch repo
```
git status
```

* Stage the files that have been modified
```
git add filename.txt
```
```
git add --all
```
### 4. Commit changes
* Commit the modified files
```
git commit -m "description of change"
```

### 5. Push changes to branch
```
git push
```
