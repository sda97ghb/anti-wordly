from unittest import TestCase

from anti_wordly.utils import first, first_n


class FirstTests(TestCase):
    def test_ok(self) -> None:
        expected_first_item = "one"
        iterable = [expected_first_item, "two", "three"]
        actual_first_item = first(iterable)
        self.assertEqual(actual_first_item, expected_first_item)


class FirstNTests(TestCase):
    def test_ok(self) -> None:
        iterable = ["one", "two", "three", "four", "five"]
        items = list(first_n(iterable, n=3))
        self.assertEqual(items, ["one", "two", "three"])

    def test_iterable_size_less_than_n(self) -> None:
        iterable = ["one", "two"]
        iterator = first_n(iterable, n=3)
        self.assertEqual(next(iterator), "one")
        self.assertEqual(next(iterator), "two")
        self.assertRaises(StopIteration, next, iterator)
