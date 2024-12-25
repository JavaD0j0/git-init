# Project Initialization Helper

> Note: These are instructions for Windows OS

This repo is to help you speed up the process of creating your project repositories with the execution of just one command.
**Instead of ~~6-plus~~ git commands, just run 1 and be done with it!**

By running this script, you will have a project directory in your designated location. A project repo will be added to your GitHub Account with a README.md file and the requirements.txt file added and pushed to the remote repo as the initial commit. Lastly a virtal environment will be created and set project directory to current project location.

- You can create a project locally without the Git repo.

## How to Install

```bash
git clone "https://github.com/JavaD0j0/git-init.git"
cd git-init
pip install -r requirements.txt
```

## Set-Up

- In order to connect to GitHub and have a determined project folder, we need to make some environment additions...

```txt
Under System Variables add the following entries:
1. "PROJECT_DIR" = project directory where you want repos to be saved
2. "GITHUB_TOKEN" = your github token which you can find in your GitHub account
```

- Also, we need to add the PATH of the repo so we can call **create** from anywhere in the command prompt...

```txt
Under System Variables, go to Path and add a new entry with the path of where you cloned the repo in your machine.
1. C:\"pathToDirectoryWhereRepoIsAt\git-init\
Example:
    - C:\%USERPROFILE%\git-init\
```

## How to Use

- Make sure ```<project_name>``` is all one word (i.e. create helloWorld)

```bash
create <project_name>
```

To create project locally:

```bash
create <project_name> -l
```
