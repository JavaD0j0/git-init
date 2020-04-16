import sys
import os
from github import Github

def promptEnd():
    response = input("Do you want to open files with VS Code? (Y/N)")
    if response == 'Y' or response == 'y':
        os.system("code .")

def main():
    # Gather basic info of where to place repository locally
    folder_name = str(sys.argv[1])
    path = os.environ.get("projectDir")
    token = os.environ.get("gitToken")
    dir_ = path + '/' + folder_name

    # Connect to Github account and create repository
    gh = Github(token)
    user = gh.get_user()
    login = user.login
    repo = user.create_repo(folder_name)

    commands = [
        f'ECHO "# {repo.name}" >> README.md',
        'git init',
        f'git remote add origin https://github.com/{login}/{folder_name}.git',
        'git add .',
        'git commit -m "Initial commit"',
        'git push -u origin master'
    ]

    # Now we need to call the commands
    os.mkdir(dir_)
    os.chdir(dir_)

    for c in commands:
        os.system(c)

    print(f'{folder_name} created successfully...')
    #os.system("code .")

if __name__ == "__main__":
    main()
    promptEnd()