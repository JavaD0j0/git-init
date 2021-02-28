import os
import sys
# If we don't use PyGithub, we can always use Selenium as well to log in to GitHub
from github import Github, GithubException

def promptEnd():
    response = input("Do you want to open files with VS Code? (Y/N) ")
    if response == 'Y' or response == 'y':
        os.system("code .")


def promptFirst():
    response = input("Do you want this repo to be private? (Y/N) ")
    return True if response == 'Y' or response == 'y' else False
        

def checkForRepo(user, folder_name, type_):
    try:
        return user.create_repo(folder_name, private=type_)
    except GithubException:
        print(f'\t{folder_name} already exists. Use a different name for your project!')
        print('\tMoving you to the project folder...')
        print('-'*45)
        sys.exit(-1) 

def createDir(dir):
    os.mkdir(dir)
    os.chdir(dir)

def callCommands(repo, login, dir_, folder_name):
    commands = [
        f'ECHO # {repo.name} >> README.md',
        'git init',
        f'git remote add origin https://github.com/{login}/{folder_name}.git',
        'git add .',
        'git commit -m "Initial commit"',
        'git push -u origin master'
    ]

    # Create directory and move to it
    createDir(dir_)

    # Execute commands
    for c in commands:
        os.system(c)

    print(f'{folder_name} created successfully...\n')

def createVirtualEnv(folder_name):
    response = input("Do you want to create a virtual environment for your project? (Y/N) ")
    if response == 'Y' or response == 'y':
        commands = [
            f'mkvirtualenv {folder_name}'#,
            # f'workon {folder_name}',
            # 'setprojectdir .',
            # 'pip freeze > requirements.txt'
        ]

        for c in commands:
            os.system(c)

        print(f'\nVirtual Env for {folder_name} is created...')
        #print("We have created requirements.txt with current pip packages...\n")
    else:
        print("Not creating a virtual environment!")


def main():
    # Gather basic info of where to place repository locally
    # print(f"*** len(sys.argv) = {len(sys.argv)} : {sys.argv} ***")
    folder_name = str(sys.argv[1])
    local = ""
    if len(sys.argv) > 2:
        local = str(sys.argv[2])

    path = os.environ.get("projectDir")
    token = os.environ.get("gToken")
    dir_ = path + '/' + folder_name

    if local != "-l":
        # Ask if repo will be private or not
        type_ = promptFirst()

        # Connect to Github account and create repository
        gh = Github(token)
        user = gh.get_user()
        print('-'*45)
        print(f'\tUsername: {user.name}') ##TESTING
        login = user.login

        # Check if repo already exists, if not create it
        repo = checkForRepo(user, folder_name, type_) 
        #repo = user.create_repo(folder_name, private=type_)
        print(f'\t{repo.name} repo created in Github!') ##TESTING
        print('-'*45)

        # Execute Git Commands
        callCommands(repo, login, dir_, folder_name)
    else:
        createDir(dir_)

    # Create virtual enviroment
    createVirtualEnv(folder_name)

    # Ask if files should be open with VS Code
    promptEnd()

if __name__ == "__main__":
    main()