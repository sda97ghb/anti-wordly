from abc import ABC, abstractmethod
from collections.abc import Iterable
from pathlib import Path


class Dictionary(ABC):
    @abstractmethod
    def nouns(self) -> Iterable[str]:
        raise NotImplementedError()


class FileDictionary(Dictionary):
    _nouns_file_path: Path
    _nouns_file_encoding: str

    def __init__(self, nouns_file_path: Path, nouns_file_encoding: str = "utf-8"):
        self._nouns_file_path = nouns_file_path
        self._nouns_file_encoding = nouns_file_encoding

    def nouns(self) -> Iterable[str]:
        with open(self._nouns_file_path, encoding=self._nouns_file_encoding) as file:
            for word in file:
                yield self._clear(word)

    def _clear(self, word: str) -> str:
        return word.strip()
