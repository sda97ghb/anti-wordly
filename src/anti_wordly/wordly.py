from collections import Counter
from collections.abc import Iterable
from dataclasses import dataclass

from anti_wordly.dictionary import Dictionary
from anti_wordly.utils import first_n


def filter_5_letter_words(words: Iterable[str]) -> Iterable[str]:
    return (word for word in words if len(word) == 5)


def exclude_column(word: str, column: int) -> str:
    return word[:column] + word[column + 1 :]


def check_word_matches_green_letters(word: str, green_letters: str) -> bool:
    for letter_from_word, letter_from_green_letters in zip(word, green_letters):
        if letter_from_green_letters == "-":
            continue
        if letter_from_word != letter_from_green_letters:
            return False
    return True


def exclude_columns_matching_green_letters(word: str, green_letters: str) -> str:
    columns_matching_green_letters = [
        idx for idx, letter in enumerate(green_letters) if letter != "-"
    ]
    for column in reversed(columns_matching_green_letters):
        word = exclude_column(word, column)
    return word


def check_word_matches_yellow_letters(word: str, yellow_letters: str) -> bool:
    if not check_word_contains_yellow_letters(word, yellow_letters):
        return False
    if not check_yellow_letters_are_in_different_columns(word, yellow_letters):
        return False
    return True


def check_word_contains_yellow_letters(word: str, yellow_letters: str) -> bool:
    for letter_from_yellow_letters in yellow_letters:
        if letter_from_yellow_letters == "-":
            continue
        if letter_from_yellow_letters not in word:
            return False
    return True


def check_yellow_letters_are_in_different_columns(
    word: str, yellow_letters: str
) -> bool:
    for letter_from_word, letter_from_yellow_letters in zip(word, yellow_letters):
        if letter_from_yellow_letters == "-":
            continue
        if letter_from_word == letter_from_yellow_letters:
            return False
    return True


def check_word_matches_gray_letters(
    word: str, yellow_letters: str, gray_letters: str
) -> bool:
    word_letter_counts = Counter(word)
    yellow_letter_counts = Counter(yellow_letters)
    for letter in set(gray_letters) - {"-"}:
        count_of_in_word = word_letter_counts[letter]
        count_of_yellow = yellow_letter_counts[letter]
        if count_of_yellow > 0:
            if count_of_in_word != count_of_yellow:
                return False
        if count_of_yellow == 0:
            if letter in word:
                return False
    return True


def matches_try(
    word: str, green_letters: str, yellow_letters: str, gray_letters: str
) -> bool:
    # Check word matches green letters
    if not check_word_matches_green_letters(word, green_letters):
        return False

    # Exclude columns matching green letters
    word = exclude_columns_matching_green_letters(word, green_letters)
    yellow_letters = exclude_columns_matching_green_letters(
        yellow_letters, green_letters
    )
    gray_letters = exclude_columns_matching_green_letters(gray_letters, green_letters)

    # Check word matches yellow letters
    if not check_word_matches_yellow_letters(word, yellow_letters):
        return False

    # Check word matches gray letters
    if not check_word_matches_gray_letters(word, yellow_letters, gray_letters):
        return False

    return True


WORD_LENGTH = 5
UNSPECIFIED_COLUMN_LETTER = "-"


@dataclass
class Try:
    green_letters: str
    yellow_letters: str
    gray_letters: str

    def is_valid(self) -> bool:
        return (
            (len(self.green_letters) == WORD_LENGTH)
            and (len(self.yellow_letters) == WORD_LENGTH)
            and (len(self.gray_letters) == WORD_LENGTH)
            and self._are_fit_together()
        )

    def _are_fit_together(self) -> bool:
        for green_letter, yellow_letter, gray_letter in zip(
            self.green_letters, self.yellow_letters, self.gray_letters
        ):
            if not self._are_letters_fit_together(
                green_letter, yellow_letter, gray_letter
            ):
                return False
        return True

    def _are_letters_fit_together(
        self, green_letter: str, yellow_letter: str, gray_letter: str
    ) -> bool:
        return (
            sum(
                [
                    1 if green_letter != UNSPECIFIED_COLUMN_LETTER else 0,
                    1 if yellow_letter != UNSPECIFIED_COLUMN_LETTER else 0,
                    1 if gray_letter != UNSPECIFIED_COLUMN_LETTER else 0,
                ]
            )
            == 1
        )


class WordlySolver:
    _five_letter_words: list[str]

    def __init__(self, file_letter_words: list[str]) -> None:
        self._five_letter_words = file_letter_words

    def possible_solutions(self, tries: list[Try]) -> list[str]:
        self._check_tries_is_valid(tries)
        matching_words = self._select_matching_words(tries)
        return list(first_n(matching_words, n=10))

    def _check_tries_is_valid(self, tries: list[Try]) -> None:
        for try_ in tries:
            if not try_.is_valid():
                raise ValueError(f"Try is invalid: {try_}")

    def _select_matching_words(self, tries: list[Try]) -> Iterable[str]:
        return (
            word
            for word in self._five_letter_words
            if all(
                matches_try(
                    word,
                    green_letters=try_.green_letters,
                    yellow_letters=try_.yellow_letters,
                    gray_letters=try_.gray_letters,
                )
                for try_ in tries
            )
        )


def create_wordly_solver(dictionary: Dictionary) -> WordlySolver:
    five_letter_words = list(filter_5_letter_words(dictionary.nouns()))
    return WordlySolver(file_letter_words=five_letter_words)
