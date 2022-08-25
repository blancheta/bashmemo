import click

from bashmemo.utils import autodiscover_most_used_commands

import subprocess


commands = [
    "aws s3 ls",
    "aws s3 ec2",
    "ls"
]

@click.command()
@click.option("-ad", "--autodiscover", default=0, help="Autodiscover most used commands from your bash history to bookmark")
@click.option("-b", "--bookmark", help="The command to bookmark")
def run(autodiscover, bookmark):

    if not str(autodiscover) or bookmark:
        raise click.ClickException('filename argument and option string are mutually exclusive!')

    if autodiscover:
        autodiscover_most_used_commands()
    else:
        keywords = input("bm-i-search (keywords separated by space): ")
        keywords = keywords.split(" ")

        commands_selection = []

        for command in commands:
            cond = []
            for keyword in keywords:
                cond.append( keyword in command)

            if all(cond):
                commands_selection.append(command)

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
