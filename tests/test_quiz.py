"""Unit tests for the Quiz class."""

from models import Question
from quiz import Quiz


def make_sample_quiz():
    """Helper to build a small quiz for testing."""
    questions = [
        Question('Q1', ['a', 'b', 'c', 'd'], 'A'),
        Question('Q2', ['a', 'b', 'c', 'd'], 'B'),
    ]
    return Quiz(questions)


def test_quiz_starts_with_zero_score():
    quiz = make_sample_quiz()
    assert quiz.score == 0


def test_quiz_starts_at_first_question():
    quiz = make_sample_quiz()
    assert quiz.current_index == 0


def test_check_answer_increments_score_when_correct():
    quiz = make_sample_quiz()
    quiz.check_answer('A')
    assert quiz.score == 1


def test_check_answer_does_not_increment_when_wrong():
    quiz = make_sample_quiz()
    quiz.check_answer('B')
    assert quiz.score == 0


def test_next_question_advances_index():
    quiz = make_sample_quiz()
    quiz.next_question()
    assert quiz.current_index == 1


def test_has_more_questions_true_at_start():
    quiz = make_sample_quiz()
    assert quiz.has_more_questions() is True


def test_has_more_questions_false_when_finished():
    quiz = make_sample_quiz()
    quiz.next_question()
    quiz.next_question()
    assert quiz.has_more_questions() is False


def test_calculate_percentage_full_marks():
    quiz = make_sample_quiz()
    quiz.check_answer('A')
    quiz.next_question()
    quiz.check_answer('B')
    assert quiz.calculate_percentage() == 100.0


def test_calculate_percentage_with_zero_questions():
    quiz = Quiz([])
    assert quiz.calculate_percentage() == 0