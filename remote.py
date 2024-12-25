"""
This script creates a new GitHub repository, initializes a local repository,
and optionally sets up a virtual environment and opens the project in VS Code.
"""
import os
import sys
from github import Github, GithubException
from rich.console import Console
from rich.prompt import Prompt, Confirm

console = Console()

def prompt_user(prompt_message, options=None):
    """
    Prompts the user with a given message and returns the response.

    Args:
        prompt_message (str): The message to prompt the user with.
        options (list, optional): A list of valid options to enforce.

    Returns:
        str: The user's validated response.
    """
    while True:
        response = Prompt.ask(f"[bold cyan]{prompt_message}[/bold cyan]", choices=options).strip().lower()
        if options and response not in options:
            console.print(f"[bold red]Invalid input. Please choose from {options}.[/bold red]")
        else:
            return response

def prompt_end():
    """
    Prompts the user to open the project folder with VS Code.

    If the user responds with 'Y' or 'y', the folder is opened in VS Code.
    """
    if Confirm.ask("[bold green]Would you like to open the project in VS Code?[/bold green]", default=False):
        os.system("code .")

def prompt_first():
    """
    Prompts the user to decide if the GitHub repository should be private.

    Returns:
        bool: True if the user wants a private repository, False otherwise.
    """
    return Confirm.ask("[bold green]Should the GitHub repository be private?[/bold green]", default=True)

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
        console.print(f"[bold red]The repository \"{folder_name}\" already exists. Please choose a different name for your project.[/bold red]")
        console.rule()
        sys.exit(-1)

def create_dir(directory):
    """
    Creates a directory and changes the current working directory to it.

    Args:
        directory (str): The directory path to create.
    """
    os.makedirs(directory, exist_ok=True)
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
        f"ECHO # {repo.name} >> README.md",
        "ECHO .venv/ >> .gitignore",
        "ECHO .vscode/ >> .gitignore",
        "ECHO __pycache__/ >> .gitignore",
        "git init",
        f"git remote add origin https://github.com/{login}/{folder_name}.git",
        "git add .",
        "git commit -m \"Initial commit\"",
        "git push -u origin master"
    ]

    create_dir(dir_)
    for command in commands:
        console.print(f"[bold magenta]Running:[/bold magenta] {command}")
        os.system(command)

    console.print(f"[bold green]The repository \"{folder_name}\" has been successfully created and pushed to GitHub.[/bold green]\n")

def create_virtual_env():
    """
    Prompts the user to create a virtual environment for the project and executes the necessary commands if confirmed.
    """
    if Confirm.ask("[bold green]Would you like to create a virtual environment for your project?[/bold green]", default=True):
        os.system("python -m venv .venv")
        console.print("[bold green]Virtual environment has been created.[/bold green]")
    else:
        console.print("[bold yellow]Virtual environment creation skipped.[/bold yellow]")

def main():
    """
    The main function that orchestrates the creation of a GitHub repository, initializes a local repository,
    and optionally sets up a virtual environment and opens the project in VS Code.
    """
    folder_name = str(sys.argv[1])
    local = str(sys.argv[2]) if len(sys.argv) > 2 else ""

    path = os.environ.get("PROJECT_DIR")
    token = os.environ.get("GITHUB_TOKEN")
    console.print(f"[bold cyan]Creating repository \"{folder_name}\" in {path}...[/bold cyan]")
    dir_ = os.path.join(path, folder_name)

    if local != "-l":
        private = prompt_first()

        gh = Github(token)
        user = gh.get_user()
        console.rule("GitHub User Details")
        console.print(f"[bold yellow]Username:[/bold yellow] {user.name}")
        login = user.login

        repo = check_for_repo(user, folder_name, private)
        console.print(f"[bold green]The repository \"{repo.name}\" has been created on GitHub.[/bold green]")
        console.rule()

        call_commands(repo, login, dir_, folder_name)
    else:
        create_dir(dir_)

    create_virtual_env()
    prompt_end()

if __name__ == "__main__":
    main()
