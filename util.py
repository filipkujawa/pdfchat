import os
from rich import print


def clear():
    os.system("cls" if os.name == "nt" else "clear")


def printLogo():
    logoList = [
        "  _____  _____  ______    _____ _    _       _______ ",
        " |  __ \|  __ \|  ____|  / ____| |  | |   /\|__   __|",
        " | |__) | |  | | |__    | |    | |__| |  /  \  | |   ",
        " |  ___/| |  | |  __|   | |    |  __  | / /\ \ | |   ",
        " | |    | |__| | |      | |____| |  | |/ ____ \| |   ",
        " |_|    |_____/|_|       \_____|_|  |_/_/    \_\_|   ",
        "                                                     ",
    ]

    for line in logoList:
        print("[bold blue]" + line)


def handleApiKeyInput(console) -> str:
    console.print("\n-- OPEN AI API KEY --", style="bold blue")

    console.print(
        "\nYou can get a API Key from https://platform.openai.com/account/api-keys",
        style="italic white",
        highlight=False,
    )
    console.print("\nEnter API Key: ", style="bold white")

    return input()
