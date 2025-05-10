"""
Advent of code 2024 template file

Author: Alex Traveylan
Date: 2024-12-01
"""

import time
from collections.abc import Callable
from functools import partial

import requests
from bs4 import BeautifulSoup

from src.settings import Settings

settings = Settings()


def get_input(day: int) -> str:
    """Get the input for a given day

    Parameters
    ----------
    day : int
        The day of the puzzle

    Returns
    -------
    str
        The input as a string
    """
    req = requests.get(
        f"https://adventofcode.com/{settings.year}/day/{day}/input",
        headers={"cookie": "session=" + settings.aoc_cookie},
        timeout=5,
    )
    return req.text


def get_example(day: int, offset=0) -> str:
    """Get the example input for a given day

    Parameters
    ----------
    day : int
        The day of the puzzle
    offset : int, optional
        The offset of the example (default is 0)

    Returns
    -------
    str
        The input as a string
    """
    req = requests.get(
        f"https://adventofcode.com/{settings.year}/day/{day}",
        headers={"cookie": "session=" + settings.aoc_cookie},
        timeout=5,
    )
    blocks = req.text.split("<pre><code>")

    return blocks[offset + 1].split("</code></pre>")[0]


def submit(day: int, level: int, answer: str) -> None:
    """Submit an answer to a puzzle

    Parameters
    ----------
    day : int
        The day of the puzzle
    level : int
        The level of the puzzle
    answer : str
        The answer to submit
    """

    text = "Envoi de la réponse suivante :\n"
    text += f"{'>' * 5} {answer} {'<' * 5}\n"
    text += "Press enter to continue or Ctrl+C to abort."
    input(text)

    data = {"level": str(level), "answer": str(answer)}

    response = requests.post(
        f"https://adventofcode.com/{settings.year}/day/{day}/answer",
        headers={"cookie": "session=" + settings.aoc_cookie},
        data=data,
        timeout=5,
    )
    if "You gave an answer too recently" in response.text:
        print("VERDICT : TOO MANY REQUESTS")
    elif "not the right answer" in response.text:
        if "too low" in response.text:
            print("VERDICT : WRONG (TOO LOW)")
        elif "too high" in response.text:
            print("VERDICT : WRONG (TOO HIGH)")
        else:
            print("VERDICT : WRONG (UNKNOWN)")
    elif "seem to be solving the right level." in response.text:
        print("VERDICT : INVALID LEVEL")
    else:
        print("VERDICT : OK !")


def ints(line: str, sep: str | None = None) -> list[int]:
    """Convert a string of ints to a list of ints

    Parameters
    ----------
    line : str
        The string to convert

    Returns
    -------
    list[int]
        The list of ints
    """
    return list(map(int, line.split(sep)))


def extract_statement(day: int, part: int) -> str:
    """Extrait le contenu HTML de l'énoncé d'un puzzle

    Parameters
    ----------
    day : int
        Le jour du puzzle
    part : int
        La partie du puzzle (1 ou 2)

    Returns
    -------
    str
        Le contenu HTML de l'énoncé
    """
    req = requests.get(
        f"https://adventofcode.com/{settings.year}/day/{day}",
        headers={"cookie": "session=" + settings.aoc_cookie},
        timeout=5,
    )

    soup = BeautifulSoup(req.text, "html.parser")
    main = soup.find("main")
    articles = main.find_all("article")

    return str(articles[part - 1])


def main(day: int, part: int, code: Callable[[str], str | int], *, offset: int = 0):
    exemple_or_real = int(input("Exemple (0) ou Réel (1) ? "))

    if exemple_or_real == 0:
        s = get_example(day, offset).strip()
    else:
        s = get_input(day).strip()

    begin_time = time.perf_counter()

    # Your code here
    ans = partial(code, s)()

    # fin du code
    end_time = time.perf_counter()
    print(f"Temps d'exécution : {end_time - begin_time:.2f} secondes")
    if exemple_or_real == 1:
        submit(day, part, ans)
    else:
        print(ans)
