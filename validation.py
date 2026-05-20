"""Pure validation functions for user input.

Every function in this module is pure: given the same input it always
returns the same output and has no side effects. This makes them easy
to unit test in isolation.
"""

import re


def is_present(value):
    """Return True if the value contains at least one non-whitespace character.

    Args:
        value: The string to check.

    Returns:
        bool: True if the value is non-empty after stripping, False otherwise.
    """
    return bool(value.strip())


def is_valid_name(name):
    """Return True if the name contains only letters, spaces, hyphens or apostrophes.

    Accepts names like 'Mary-Jane' or "O'Neil" while rejecting names that
    contain digits or other special characters.

    Args:
        name: The name string to validate.

    Returns:
        bool: True if the name matches the allowed pattern, False otherwise.
    """
    return bool(re.fullmatch(r"[A-Za-z\s'-]+", name.strip()))


def is_answer_selected(answer):
    """Return True if the answer is one of the valid options A, B, C or D.

    Args:
        answer: The selected answer letter.

    Returns:
        bool: True if the answer is in the allowed set, False otherwise.
    """
    return answer in ['A', 'B', 'C', 'D']