from pathlib import Path
from typing import Any, Annotated

from fastapi import FastAPI, Body, HTTPException
from pydantic import BaseModel
from starlette.status import HTTP_400_BAD_REQUEST

from anti_wordly.dictionary import FileDictionary
from anti_wordly.wordly import create_wordly_solver, Try as WordlyTry

app = FastAPI(
    title="AntiWordly",
    summary="Service for solving Wordly puzzles",
    description="It can find possible solutions based on previous tries.",
)


class Try(BaseModel):
    green_letters: str
    yellow_letters: str
    gray_letters: str


class SolveResponse(BaseModel):
    possible_solutions: list[str]

    class Config:
        schema_extra = {
            "examples": [{"possible_solutions": ["венок", "гонор", "донор", "рынок"]}]
        }


@app.post(
    "/solve",
    response_model=SolveResponse,
    tags=["Solver"],
    summary="Find possible solutions",
    description="Find possible solutions based on previous tries",
)
def solve(
    tries: Annotated[
        list[Try],
        Body(
            example=[
                Try(
                    green_letters="---о-", yellow_letters="----н", gray_letters="сал--"
                ),
                Try(
                    green_letters="--но-", yellow_letters="-----", gray_letters="би--м"
                ),
            ],
        ),
    ],
) -> Any:
    dictionary = FileDictionary(
        nouns_file_path=Path(__file__).resolve().parent.parent.parent
        / "russian_nouns.txt",
    )
    solver = create_wordly_solver(dictionary)
    tries = [
        WordlyTry(
            green_letters=try_.green_letters,
            yellow_letters=try_.yellow_letters,
            gray_letters=try_.gray_letters,
        )
        for try_ in tries
    ]
    try:
        possible_solutions = solver.possible_solutions(tries=tries)
    except ValueError as err:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=str(err)) from err
    return {"possible_solutions": possible_solutions}
