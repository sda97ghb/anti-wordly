import re
from pathlib import Path
from typing import Annotated

from typer import Typer, Argument, BadParameter

from anti_wordly.dictionary import FileDictionary
from anti_wordly.wordly import create_wordly_solver, Try

app = Typer()


def validate_tries_argument(tries: list[str]) -> list[str]:
    format_ = r"[а-я\-]{5},[а-я\-]{5},[а-я\-]{5}"
    for try_ in tries:
        if not re.match(format_, try_):
            raise BadParameter(f"The value {try_!r} doesn't match format {format_!r}")
    return tries


@app.command(name="solve")
def solve(
    tries: Annotated[
        list[str],
        Argument(
            help=(
                "Three groups of 5 characters separated by comma, "
                "representing green, yellow, and gray letters respectively. "
                "Unspecified letters must be represented as '-' (minus). "
                "E.g. '---о-,----н,сал--'"
            ),
            callback=validate_tries_argument,
        ),
    ]
) -> None:
    dictionary = FileDictionary(
        nouns_file_path=Path(__file__).resolve().parent / "russian_nouns.txt",
    )
    solver = create_wordly_solver(dictionary)
    tries = [try_.split(",") for try_ in tries]
    tries = [
        Try(
            green_letters=try_[0],
            yellow_letters=try_[1],
            gray_letters=try_[2],
        )
        for try_ in tries
    ]
    for word in solver.possible_solutions(tries=tries):
        print(word)


if __name__ == "__main__":
    app()
