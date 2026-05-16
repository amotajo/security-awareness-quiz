class Question:class answer):
        self.text = text
        self.options = options
        self.answer = answer.upper()

    def is_correct(self, user_answer):
        return user_answer.upper() == self.answer