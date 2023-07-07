from pathlib import Path
from unittest import TestCase
from tempfile import TemporaryDirectory

from anti_wordly.dictionary import FileDictionary


class FileDictionaryTests(TestCase):
    def setUp(self) -> None:
        self.nouns = ["apple", "banana", "carrot"]

    def _create_test_nouns_file(self, directory: Path) -> Path:
        file_path = directory / "nouns.txt"
        with open(file_path, mode="w", encoding="utf-8") as file:
            for noun in self.nouns:
                print(noun, file=file)
        return file_path

    def test_nouns(self) -> None:
        with TemporaryDirectory(suffix="dictionary_tests") as directory:
            nouns_file_path = self._create_test_nouns_file(Path(directory))
            dictionary = FileDictionary(nouns_file_path=nouns_file_path)
            nouns = list(dictionary.nouns())
            self.assertEqual(nouns, self.nouns)
