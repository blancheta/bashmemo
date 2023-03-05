from pathlib import Path

import requests
from rich.console import Console
from rich.table import Table

from src.bashmemo.config import domain


def autodiscover_most_used_commands():

    """
    Sort commands from the bash history by usage
    :return:
    """

    home = str(Path.home())

    commands = {}

    with open(home + "/.zsh_history", "r") as file:
        for command in file.read().splitlines():
            # Could use Counter here
            if command == "":
                continue

            if command in commands:
                commands[command] += 1
            else:
                commands[command] = 1

    commands_list = list(map(list, commands.items()))
    commands_list = sorted(commands_list, key=lambda x: x[1], reverse=True)

    table = Table(title="Command usage leaderboard")

    table.add_column("Command", style="magenta")
    table.add_column("Count", style="cyan")

    for command in commands_list[:20]:
        if command[1] > 1:
            table.add_row(command[0], str(command[1]))

    console = Console()
    console.clear()
    console.print(table)


def create_bookmark(command: str, keywords_input: str, user_id, token) -> bool:
    # create a list of keywords from string containing keywords
    # request the creation of the bookmark

    print(command)
    keywords = keywords_input.split(" ")
    payload = {
        "command": command,
        "keywords": [{"name": keyword} for keyword in keywords],
        "object_id": user_id
    }
    response = requests.post(
        f"{domain}/api/bookmarks/",
        json=payload,
        headers={
            "Content-type": "application/json",
            "Authorization": f"Bearer {token}"
        }
    )

    if response.status_code == 201:
        return True
    else:
        return False
