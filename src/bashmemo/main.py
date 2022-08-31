import os
from os.path import exists
import pickle
import time
import webbrowser

import click
import requests

from src.bashmemo.config import domain
from src.bashmemo.utils import autodiscover_most_used_commands, create_bookmark

import subprocess

commands = []



@click.command()
@click.option("-b", "--bookmark", help="Bookmark a command")
@click.option("-ad", "--autodiscover", default=0, help="Autodiscover most used commands from your bash history to bookmark")
def run(autodiscover, bookmark):

    if not (str(autodiscover) or bookmark):
        raise click.ClickException('filename argument and option string are mutually exclusive!')

    # Getting back token if existing else displaying link to connect with github
    token_file_path = "/tmp/token.pickle"
    if exists(token_file_path):
        pickle_in = open(token_file_path, "rb")
        token = pickle.load(pickle_in)
    else:
        # try to validate the token via the api
        print(f"Please Log in here: {domain}/accounts/github/login")
        print("Redirecting you to Login page ...")
        time.sleep(3)
        webbrowser.open(f"{domain}/accounts/github/login")
        token = input("Token: ")
        pickle_in = open("/tmp/token.pickle", "wb")
        pickle.dump(token, pickle_in)

    print("Sync local with cloud ...")

    response = requests.get(f"{domain}/api/users/self/", headers={
        'Authorization': f"Bearer {token}"
    })
    if response.status_code != 200:
        print("Invalid token: Please retry")
        os.remove("/tmp/token.pickle")
        exit()

    user_id = response.json()['user']['id']
    commands = response.json()['user']['bookmarks']
    if autodiscover:
        autodiscover_most_used_commands()
    elif bookmark:
        keywords_input = input("Any keywords to find back this command? (separated by empty space): ")
        bookmark_created = create_bookmark(bookmark, keywords_input, user_id, token)
        if not bookmark_created:
            print("Command bookmark has not been created because of an error")
        else:
            print("Command Bookmark saved. Oh yeah!")
    else:
        keywords = input("bm-i-search (keywords separated by space): ")
        keywords = keywords.split(" ")
        commands_selection = []

        for command in commands:
            cond = []
            for keyword in keywords:
                cond.append( keyword in command['command'] or keyword in command['keywords'])

            if all(cond):
                commands_selection.append(command["command"])

        if not commands_selection:
            print("No commands found! :D")
            exit()

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

        # print("\033[A                                          \033[A")

        for _ in commands_selection:
            print("\033[A                             \033[A")

        print("\033[A                             \033[A")

        print(execute_command)

        subprocess.run(command_parts)


if __name__ == '__main__':
    run()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
