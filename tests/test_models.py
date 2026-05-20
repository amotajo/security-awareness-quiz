"""Unit tests for the Question class."""

from models import Question


def test_question_stores_text_and_options():
    q = Question('What is 2+2?', ['3', '4', '5', '6'], 'B')
    assert q.text == 'What is 2+2?'
    assert q.options == ['3', '4', '5', '6']


def test_question_stores_answer_as_uppercase():
    q = Question('Pick one', ['a', 'b', 'c', 'd'], 'b')
    assert q.answer == 'B'


def test_question_is_correct_returns_true_for_matching_answer():
    q = Question('Pick one', ['a', 'b', 'c', 'd'], 'C')
    assert q.is_correct('C') is True


def test_question_is_correct_is_case_insensitive():
    q = Question('Pick one', ['a', 'b', 'c', 'd'], 'C')
    assert q.is_correct('c') is True


def test_question_is_correct_returns_false_for_wrong_answer():
    q = Question('Pick one', ['a', 'b', 'c', 'd'], 'C')
    assert q.is_correct('A') is False