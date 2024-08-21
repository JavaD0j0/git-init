import os
import sys
from github import Github, GithubException


def prompt_end():
    """
    Prompts the user to open the project folder with VS Code.

    If the user responds with 'Y' or 'y', the folder is opened in VS Code.
    """
    response = input("Do you want to open files with VS Code? (Y/N) ")
    if response.lower() == 'y':
        os.system("code .")


def prompt_first():
    """
    Prompts the user to decide if the GitHub repository should be private.

    Returns:
        bool: True if the user wants a private repository, False otherwise.
    """
    response = input("Do you want this repo to be private? (Y/N) ")
    return response.lower() == 'y'


def check_for_repo(user, folder_name, private):
    """
    Checks if the repository already exists for the user. If it doesn't, creates a new repository.

    Args:
        user (github.AuthenticatedUser.AuthenticatedUser): Authenticated GitHub user.
        folder_name (str): Name of the repository to be created.
        private (bool): Determines if the repository should be private.

    Returns:
        github.Repository.Repository: The created repository.

    Raises:
        SystemExit: If the repository already exists.
    """
    try:
        return user.create_repo(folder_name, private=private)
    except GithubException:
        print(f'\t{folder_name} already exists. Use a different name for your project!')
        print('\tMoving you to the project folder...')
        print('-' * 45)
        sys.exit(-1)


def create_dir(directory):
    """
    Creates a directory and changes the current working directory to it.

    Args:
        directory (str): The directory path to create.
    """
    os.mkdir(directory)
    os.chdir(directory)


def call_commands(repo, login, dir_, folder_name):
    """
    Executes a series of git commands to initialize a new repository and push the initial commit.

    Args:
        repo (github.Repository.Repository): The GitHub repository object.
        login (str): The GitHub login username.
        dir_ (str): The local directory to initialize the repository in.
        folder_name (str): The name of the repository folder.
    """
    commands = [
        f'ECHO # {repo.name} >> README.md',
        'git init',
        f'git remote add origin https://github.com/{login}/{folder_name}.git',
        'git add .',
        'git commit -m "Initial commit"',
        'git push -u origin master'
    ]

    create_dir(dir_)

    for command in commands:
        os.system(command)

    print(f'{folder_name} created successfully...\n')


def create_virtual_env(folder_name):
    """
    Prompts the user to create a virtual environment for the project and executes the necessary commands if confirmed.

    Args:
        folder_name (str): The name of the project folder.
    """
    response = input("Do you want to create a virtual environment for your project? (Y/N) ")
    if response.lower() == 'y':
        commands = [
            f'mkvirtualenv {folder_name}'
        ]

        for command in commands:
            os.system(command)

        print(f'\nVirtual Env for {folder_name} is created...')
    else:
        print("Not creating a virtual environment!")


def main():
    """
    The main function that orchestrates the creation of a GitHub repository, initializes a local repository,
    and optionally sets up a virtual environment and opens the project in VS Code.
    """
    folder_name = str(sys.argv[1])
    local = ""
    if len(sys.argv) > 2:
        local = str(sys.argv[2])

    path = os.environ.get("projectDir")
    token = os.environ.get("gToken")
    dir_ = os.path.join(path, folder_name)

    if local != "-l":
        private = prompt_first()

        gh = Github(token)
        user = gh.get_user()
        print('-' * 45)
        print(f'\tUsername: {user.name}')
        login = user.login

        repo = check_for_repo(user, folder_name, private)
        print(f'\t{repo.name} repo created in GitHub!')
        print('-' * 45)

        call_commands(repo, login, dir_, folder_name)
    else:
        create_dir(dir_)

    create_virtual_env(folder_name)
    prompt_end()


if __name__ == "__main__":
    main()
