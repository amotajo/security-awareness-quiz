class Quiz:

    def __init__(self, questions):
        self.questions = questions
        self.score = 0
        self.current_index = 0

    def get_current_question(self):
        return self.questions[self.current_index]

    def check_answer(self, user_answer):
        if self.get_current_question().is_correct(user_answer):
            self.score += 1
            return True

        return False

    def next_question(self):
        self.current_index += 1

    def has_more_questions(self):
        return self.current_index < len(self.questions)

    def total_questions(self):
        return len(self.questions)

    def calculate_percentage(self):
        if self.total_questions() == 0:
            return 0

        return round((self.score / self.total_questions()) * 100, 2)