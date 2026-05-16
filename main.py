from storage import load_questions, save_result
from quiz import Quiz
from validation import is_answer_selected, is_present

from app import SecurityQuizApp

if __name__ == '__main__':
    app = SecurityQuizApp()
    app.mainloop()

def main():
    name = ''

    while not is_present(name):
        name = input('Enter your name: ').strip()

        if not is_present(name):
            print('Please enter your name before starting the quiz.')

    questions = load_questions('questions.csv')
    quiz = Quiz(questions)

    while quiz.has_more_questions():
        question = quiz.get_current_question()

        print()
        print(question.text)

        letters = ['A', 'B', 'C', 'D']

        for letter, option in zip(letters, question.options):
            print(f'{letter}. {option}')

        user_answer = ''

        while not is_answer_selected(user_answer):
            user_answer = input('Enter A, B, C, or D: ').strip().upper()

            if not is_answer_selected(user_answer):
                print('Invalid input. Please select A, B, C, or D.')

        quiz.check_answer(user_answer)
        quiz.next_question()

    percentage = quiz.calculate_percentage()

    print()
    print(f'Final score: {quiz.score}/{quiz.total_questions()}')
    print(f'Percentage score: {percentage}%')

    save_result(
        'results.csv',
        name.title(),
        quiz.score,
        quiz.total_questions(),
        percentage
    )

if __name__ == '__main__':
    main()