import subprocess


def autodiscover_most_used_commands():

    """
    Sort commands from the bash history by usage
    :return:
    """

    list_files = subprocess.run(["history"])
    print(list_files)