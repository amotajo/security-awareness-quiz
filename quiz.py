"""Quiz session logic: tracks the current question, score and progress."""


class Quiz:
    """Manages a quiz session: a list of questions, the score and progress.

    Attributes:
        questions (list[Question]): The questions to ask, in order.
        score (int): Number of correct answers so far.
        current_index (int): Index of the next question to ask.
    """

    def __init__(self, questions):
        """Initialise the quiz with a list of Question objects.

        Args:
            questions: A list of Question instances.
        """
        self.questions = questions
        self.score = 0
        self.current_index = 0

    def get_current_question(self):
        """Return the Question at the current index."""
        return self.questions[self.current_index]

    def check_answer(self, user_answer):
        """Check the user's answer and increment the score if correct.

        Args:
            user_answer: The letter the user selected.

        Returns:
            bool: True if the answer was correct, False otherwise.
        """
        if self.get_current_question().is_correct(user_answer):
            self.score += 1
            return True
        return False

    def next_question(self):
        """Advance to the next question."""
        self.current_index += 1

    def has_more_questions(self):
        """Return True if there are still questions left to answer."""
        return self.current_index < len(self.questions)

    def total_questions(self):
        """Return the total number of questions in the quiz."""
        return len(self.questions)

    def calculate_percentage(self):
        """Return the final score as a percentage, rounded to 2 decimal places.

        Returns:
            float: The percentage score, or 0 if there are no questions.
        """
        if self.total_questions() == 0:
            return 0
        return round((self.score / self.total_questions()) * 100, 2)