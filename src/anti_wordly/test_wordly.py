from unittest import TestCase

from anti_wordly.wordly import (
    filter_5_letter_words,
    check_word_contains_yellow_letters,
    check_word_matches_gray_letters,
    check_yellow_letters_are_in_different_columns,
    exclude_column,
    check_word_matches_green_letters,
    exclude_columns_matching_green_letters,
    Try,
)


class Filter5LetterWordsTests(TestCase):
    def test_ok(self) -> None:
        words = ["apple", "banana", "carrot", "grape", "peach", "strawberry"]
        five_letter_words = list(filter_5_letter_words(words))
        self.assertEqual(five_letter_words, ["apple", "grape", "peach"])


class ExcludeColumnTests(TestCase):
    def test_first_column(self) -> None:
        self.assertEqual(exclude_column(word="grape", column=0), "rape")

    def test_inner_column(self) -> None:
        self.assertEqual(exclude_column(word="grape", column=2), "grpe")

    def test_last_column(self) -> None:
        self.assertEqual(exclude_column(word="grape", column=4), "grap")


class CheckWordMatchesGreenLettersTests(TestCase):
    def test_matches(self) -> None:
        self.assertTrue(check_word_matches_green_letters("abcde", "ab--e"))

    def test_not_matches(self) -> None:
        self.assertFalse(check_word_matches_green_letters("abcde", "q----"))


class ExcludeColumnsMatchingGreenLettersTests(TestCase):
    def test_ok(self) -> None:
        self.assertEqual(exclude_columns_matching_green_letters("abcde", "ab--e"), "cd")


class CheckWordContainsYellowLettersTests(TestCase):
    def test_contains(self) -> None:
        self.assertTrue(check_word_contains_yellow_letters("abcde", "c-e--"))

    def test_not_contains(self) -> None:
        self.assertFalse(check_word_contains_yellow_letters("abcde", "q-w--"))


class CheckYellowLettersAreInDifferentColumnsTests(TestCase):
    def test_in_different_columns(self) -> None:
        self.assertTrue(check_yellow_letters_are_in_different_columns("abcde", "c-e--"))

    def test_in_same_column(self) -> None:
        self.assertFalse(
            check_yellow_letters_are_in_different_columns("abcde", "ab---")
        )


class CheckWordMatchesGrayLettersTests(TestCase):
    def test_1(self) -> None:
        self.assertFalse(
            check_word_matches_gray_letters(
                "bca", yellow_letters="-bc", gray_letters="a--"
            )
        )

    def test_2(self) -> None:
        self.assertTrue(
            check_word_matches_gray_letters(
                "ваа", yellow_letters="в-а", gray_letters="-в-"
            )
        )

    def test_3(self) -> None:
        self.assertFalse(
            check_word_matches_gray_letters(
                "вва", yellow_letters="в-а", gray_letters="-в-"
            )
        )

    def test_4(self) -> None:
        self.assertTrue(
            check_word_matches_gray_letters(
                "bcaa", yellow_letters="aa-b", gray_letters="--a-"
            )
        )

    def test_5(self) -> None:
        self.assertFalse(
            check_word_matches_gray_letters(
                "bcda", yellow_letters="aa-b", gray_letters="--a-"
            )
        )

    def test_6(self) -> None:
        self.assertFalse(
            check_word_matches_gray_letters(
                "bcaaa", yellow_letters="aa-bc", gray_letters="--a--"
            )
        )


class TryTests(TestCase):
    def test_is_valid(self) -> None:
        try_ = Try(green_letters="---p-", yellow_letters="----e", gray_letters="gra--")
        self.assertTrue(try_.is_valid())

    def test_is_valid_green_letters_wrong_length(self) -> None:
        try_ = Try(green_letters="---p", yellow_letters="----e", gray_letters="gra--")
        self.assertFalse(try_.is_valid())

    def test_is_valid_yellow_letters_wrong_length(self) -> None:
        try_ = Try(green_letters="---p-", yellow_letters="----", gray_letters="gra--")
        self.assertFalse(try_.is_valid())

    def test_is_valid_gray_letters_wrong_length(self) -> None:
        try_ = Try(green_letters="---p-", yellow_letters="----e", gray_letters="gra-")
        self.assertFalse(try_.is_valid())

    def test_is_valid_doesnt_fit_together(self) -> None:
        try_ = Try(green_letters="---pe", yellow_letters="----e", gray_letters="-ra--")
        self.assertFalse(try_.is_valid())
