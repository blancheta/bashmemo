import click
import requests
from click_option_group import optgroup, RequiredMutuallyExclusiveOptionGroup

from bashmemo.utils import autodiscover_most_used_commands, create_bookmark

import subprocess

commands = []

@click.command()
@optgroup.group('Server configuration',
                help='The configuration of some server connection', cls=RequiredMutuallyExclusiveOptionGroup)
@optgroup.option(
    "--bookmark", help="The command to bookmark",
)
@click.option("-ad", "--autodiscover", default=0, help="Autodiscover most used commands from your bash history to bookmark")
def run(autodiscover, bookmark):
    if not (str(autodiscover) or bookmark):
        raise click.ClickException('filename argument and option string are mutually exclusive!')

    print("Sync local with cloud ...")
    response = requests.get("https://bashmemo.herokuapp.com/api/bookmarks/")
    commands = response.json()

    if autodiscover:
        autodiscover_most_used_commands()
    elif bookmark:
        keywords_input = input("Any keywords to find back this command? (separated by empty space): ")
        bookmark_created = create_bookmark(bookmark, keywords_input)
        if not bookmark_created:
            print("Command bookmark has not been created because of an error")
        else:
            print("New Command Bookmark saved!")
    else:
        keywords = input("bm-i-search (keywords separated by space): ")
        keywords = keywords.split(" ")

        commands_selection = []

        for command in commands:
            cond = []
            for keyword in keywords:
                cond.append( keyword in command['command'])

            if all(cond):
                commands_selection.append(command["command"])

        if len(commands_selection) > 1:
            print("Choose the command to execute")
            for index, command in enumerate(commands_selection):
                print(f"{index} - {command}")
            command_choice = input("Choice: ")
            execute_command = commands_selection[int(command_choice)]
        else:
            execute_command = input(commands_selection[0])
            if execute_command == "":
                execute_command = commands_selection[0]

        command_parts = execute_command.split(' ')

        print("\033[A                             \033[A")

        for _ in commands_selection:
            print("\033[A                             \033[A")

        print("\033[A                             \033[A")

        print(execute_command)

        subprocess.run(command_parts)


if __name__ == '__main__':
    run()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
