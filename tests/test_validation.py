"""Unit tests for pure validation functions.

These functions are pure — same input always returns the same output —
which makes them ideal candidates for unit testing.
"""

from validation import is_present, is_valid_name, is_answer_selected


# --- is_present ---

def test_is_present_returns_true_for_normal_text():
    assert is_present('Abiola') is True


def test_is_present_returns_false_for_empty_string():
    assert is_present('') is False


def test_is_present_returns_false_for_whitespace_only():
    assert is_present('   ') is False


# --- is_valid_name ---

def test_is_valid_name_accepts_letters():
    assert is_valid_name('Abiola') is True


def test_is_valid_name_accepts_hyphenated_name():
    assert is_valid_name("Mary-Jane O'Neil") is True


def test_is_valid_name_rejects_numbers():
    assert is_valid_name('John123') is False


def test_is_valid_name_rejects_empty_string():
    assert is_valid_name('') is False


# --- is_answer_selected ---

def test_is_answer_selected_accepts_valid_letters():
    for letter in ['A', 'B', 'C', 'D']:
        assert is_answer_selected(letter) is True


def test_is_answer_selected_rejects_lowercase():
    assert is_answer_selected('a') is False


def test_is_answer_selected_rejects_invalid_letter():
    assert is_answer_selected('E') is False


def test_is_answer_selected_rejects_empty_string():
    assert is_answer_selected('') is False