from sys import stderr
from colorama import init, Fore, Style

init()


def debug(data):
    print(Fore.YELLOW + '[DEBUG] ' + data + Style.RESET_ALL, file=stderr)


def error(data):
    print(Fore.RED + '[ERROR] ' + data + Style.RESET_ALL, file=stderr)


def message(data):
    print(Fore.GREEN + '[MESSAGE] ' + data + Style.RESET_ALL)
