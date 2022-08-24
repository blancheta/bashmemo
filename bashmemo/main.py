import click

@click.command()
@click.option("--autodiscover", default=1, help="Autodiscover most used commands from your bash history to bookmark")
@click.option('--bookmark', prompt='command',
              help='The command to bookmark')
def run(autodiscover, bookmark):
    print("Welcome to BashMemo!")

    if None not in (autodiscover, bookmark):
        raise click.ClickException('filename argument and option string are mutually exclusive!')


if __name__ == '__main__':
    run()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
