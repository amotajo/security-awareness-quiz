"""Domain model for a single quiz question."""


class Question:
    """Represents one multiple-choice quiz question.

    Attributes:
        text (str): The question text shown to the user.
        options (list[str]): The four answer choices (A, B, C, D).
        answer (str): The correct answer letter, stored uppercase.
    """

    def __init__(self, text, options, answer):
        """Initialise a Question.

        Args:
            text: The question text.
            options: A list of four answer choices.
            answer: The correct answer letter (case-insensitive).
        """
        self.text = text
        self.options = options
        self.answer = answer.upper()

    def is_correct(self, user_answer):
        """Check whether a user's answer matches the correct answer.

        The comparison is case-insensitive.

        Args:
            user_answer: The letter the user selected.

        Returns:
            bool: True if the user answered correctly, False otherwise.
        """
        return user_answer.upper() == self.answer