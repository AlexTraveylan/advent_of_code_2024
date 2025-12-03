"""
Advent of code 2024 template file

Author: Alex Traveylan
Date: 2024-12-01
"""

import time
from collections.abc import Callable
from enum import StrEnum
from functools import partial

import requests
from bs4 import BeautifulSoup

from src.settings import Settings

settings = Settings()


class ResponseStatus(StrEnum):
    OK = "OK"
    WRONG = "WRONG"
    TOO_LOW = "TOO_LOW"
    TOO_HIGH = "TOO_HIGH"
    INVALID_LEVEL = "INVALID_LEVEL"
    TOO_MANY_REQUESTS = "TOO_MANY_REQUESTS"


class ExampleOrReal(StrEnum):
    EXAMPLE = "EXAMPLE"
    REAL = "REAL"


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


def submit(day: int, level: int, answer: str) -> ResponseStatus:
    """Submit an answer to a puzzle

    Parameters
    ----------
    day : int
        The day of the puzzle
    level : int
        The level of the puzzle
    answer : str
        The answer to submit

    Returns
    -------
    ResponseStatus
        The status of the submission
    """
    data = {"level": str(level), "answer": str(answer)}

    response = requests.post(
        f"https://adventofcode.com/{settings.year}/day/{day}/answer",
        headers={"cookie": "session=" + settings.aoc_cookie},
        data=data,
        timeout=5,
    )
    if "You gave an answer too recently" in response.text:
        return ResponseStatus.TOO_MANY_REQUESTS
    elif "not the right answer" in response.text:
        if "too low" in response.text:
            return ResponseStatus.TOO_LOW
        elif "too high" in response.text:
            return ResponseStatus.TOO_HIGH
        else:
            return ResponseStatus.WRONG
    elif "seem to be solving the right level." in response.text:
        return ResponseStatus.INVALID_LEVEL
    else:
        return ResponseStatus.OK


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


def main(
    day: int,
    part: int,
    code: Callable[[str], str | int],
    *,
    example_or_real: ExampleOrReal = ExampleOrReal.REAL,
    offset: int = 0,
) -> None:
    if example_or_real == ExampleOrReal.EXAMPLE:
        s = get_example(day, offset).strip()
    else:
        s = get_input(day).strip()

    begin_time = time.perf_counter()

    # Your code here
    ans = partial(code, s)()
    print(f"Answer: {ans}")

    # fin du code
    end_time = time.perf_counter()
    print(f"Temps d'exécution : {end_time - begin_time:.2f} secondes")

    if example_or_real == ExampleOrReal.REAL:
        response_status = submit(day, part, ans)
        print(response_status)
