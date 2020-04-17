import os
import sys
# If we don't use PyGithub, we can always use Selenium as well to log in to GitHub
from github import Github

def promptEnd():
    response = input("Do you want to open files with VS Code? (Y/N) ")
    if response == 'Y' or response == 'y':
        os.system("code .")


def promptFirst():
    response = input("Do you want this repo to be private? (Y/N) ")
    return True if response == 'Y' or response == 'y' else False
        

def callCommands(repo, login, dir_, folder_name):
    commands = [
        f'ECHO # {repo.name} >> README.md',
        'git init',
        f'git remote add origin https://github.com/{login}/{folder_name}.git',
        'git add .',
        'git commit -m "Initial commit"',
        'git push -u origin master'
    ]

    # Move to project directory and create folder
    os.mkdir(dir_)
    os.chdir(dir_)

    # Execute commands
    for c in commands:
        os.system(c)

    print(f'{folder_name} created successfully...\n')


def main():
    # Gather basic info of where to place repository locally
    folder_name = str(sys.argv[1])
    path = os.environ.get("projectDir")
    token = os.environ.get("gToken")
    dir_ = path + '/' + folder_name

    # Ask if repo will be private or not
    type_ = promptFirst()

    # Connect to Github account and create repository
    gh = Github(token)
    user = gh.get_user()
    print(f"Username: {user.name}") ##TESTING
    login = user.login
    repo = user.create_repo(folder_name, private=type_)
    print(f'{repo.name} repo created in Github!\n') ##TESTING

    # Execute Git Commands
    callCommands(repo, login, dir_, folder_name)


if __name__ == "__main__":
    main()
    promptEnd()