"""Section 5.1 / 7: invalid user input is handled and the user is asked again."""
import contextlib
import io
import unittest
from typing import Callable, TypeVar
from unittest.mock import patch

from inventory_manager import get_non_negative_int, get_positive_float


T = TypeVar("T")


def run_with_inputs(function: Callable[[str], T], inputs: list[str]) -> tuple[T, str]:
    """Feed fake keyboard input to a helper and capture what it prints."""
    output = io.StringIO()
    with patch("builtins.input", side_effect=inputs), contextlib.redirect_stdout(output):
        result = function("Price: ")
    return result, output.getvalue()


class GetPositiveFloatTests(unittest.TestCase):
    def test_abc_then_minus_five_then_valid(self) -> None:
        result, printed = run_with_inputs(get_positive_float, ["abc", "-5", "12.50"])
        self.assertEqual(result, 12.5)
        self.assertEqual(printed.splitlines(),
                         ["Please enter a valid number, e.g. 12.50",
                          "Please enter a number greater than zero."])

    def test_zero_nan_and_inf_are_rejected(self) -> None:
        result, printed = run_with_inputs(get_positive_float, ["0", "nan", "inf", "3"])
        self.assertEqual(result, 3.0)
        self.assertEqual(printed.count("greater than zero"), 3)

    def test_valid_first_time_prints_nothing(self) -> None:
        result, printed = run_with_inputs(get_positive_float, ["7.25"])
        self.assertEqual((result, printed), (7.25, ""))


class GetNonNegativeIntTests(unittest.TestCase):
    def test_text_decimal_and_negative_are_rejected_then_valid(self) -> None:
        result, printed = run_with_inputs(get_non_negative_int, ["ten", "2.5", "-1", "0"])
        self.assertEqual(result, 0)
        self.assertEqual(printed.count("valid whole number"), 2)
        self.assertEqual(printed.count("0 or more"), 1)

    def test_unicode_digit_does_not_crash(self) -> None:
        result, _ = run_with_inputs(get_non_negative_int, ["²", "4"])    # superscript 2
        self.assertEqual(result, 4)


if __name__ == "__main__":
    unittest.main()
