"""Streamlit GUI for the Security Awareness Quiz."""

import os
import streamlit as st
import matplotlib.pyplot as plt

from quiz import Quiz
from storage import load_questions, save_result, get_file_path
from storage import QuestionFileError, ResultSaveError
from validation import is_present, is_valid_name, is_answer_selected


# --- Set up session state with default values ---
def init_state():
    """Set default values in session state if they are missing."""
    st.session_state.setdefault('screen', 'welcome')
    st.session_state.setdefault('name', '')
    st.session_state.setdefault('quiz', None)
    st.session_state.setdefault('saved', False)


# --- Helper for showing each answer option as 'A. Option text' ---
def format_option(letter, question):
    """Return a label like 'A. Fake emails trying to steal information'."""
    if letter == '-- Select an answer --':
        return letter

    letters = ['A', 'B', 'C', 'D']
    position = letters.index(letter)
    return f'{letter}. {question.options[position]}'


init_state()

st.set_page_config(page_title='Security Awareness Quiz', page_icon='🔐')
st.title('🔐 Security Awareness Quiz')


# --- Welcome screen ---
if st.session_state.screen == 'welcome':

    st.write('👋 Welcome! Test your security awareness knowledge.')

    name = st.text_input('✏️ Enter your name')

    if st.button('🚀 Start Quiz'):

        if not is_present(name):
            st.error('⚠️ Please enter your name before starting the quiz.')

        elif not is_valid_name(name):
            st.error('⚠️ Names may only contain letters, spaces, hyphens and apostrophes.')

        else:
            # Try to load the questions from the CSV file
            try:
                questions = load_questions('questions.csv')

                # If loading worked, set up the quiz and move to the quiz screen
                st.session_state.quiz = Quiz(questions)
                st.session_state.name = name.title()
                st.session_state.screen = 'quiz'
                st.session_state.saved = False
                st.rerun()

            except QuestionFileError as error:
                st.error(f'⚠️ {error}')


# --- Quiz screen ---
elif st.session_state.screen == 'quiz':

    quiz = st.session_state.quiz

    if quiz.has_more_questions():

        question = quiz.get_current_question()

        st.subheader(
            f'📝 Question {quiz.current_index + 1} of {quiz.total_questions()}'
        )

        st.write(question.text)

        # The select-box options. The first item is a placeholder
        # so the user has to actively choose A, B, C or D.
        options = ['-- Select an answer --', 'A', 'B', 'C', 'D']

        # A small helper function so the select-box can show
        # 'A. Fake emails...' next to each letter.
        def label_option(letter):
            return format_option(letter, question)

        selected = st.selectbox(
            '👉 Choose your answer',
            options,
            format_func=label_option
        )

        if st.button('✅ Submit Answer'):

            if not is_answer_selected(selected):
                st.error('⚠️ Please select an answer before continuing.')

            else:
                quiz.check_answer(selected)
                quiz.next_question()

                # If that was the last question, move to the end screen
                if not quiz.has_more_questions():
                    st.session_state.screen = 'end'

                st.rerun()


# --- End screen ---
# --- End screen ---
elif st.session_state.screen == 'end':

    quiz = st.session_state.quiz
    percentage = quiz.calculate_percentage()

    st.success('🎉 Quiz Complete!')
    st.balloons()

    st.metric('🏆 Final Score', f'{quiz.score} / {quiz.total_questions()}')

    # Pie chart showing correct vs incorrect
    figure, axis = plt.subplots()
    figure.patch.set_alpha(0)
    axis.set_facecolor('none')
    axis.pie(
        [quiz.score, quiz.total_questions() - quiz.score],
        labels=['Correct', 'Incorrect'],
        colors=['#4CAF50', '#F44336']
    )
    st.pyplot(figure)    st.pyplot(figure)

    st.metric('📊 Percentage Score', f'{percentage}%')

    # Save the result once per completion (so refreshing the page
    # does not save the same score twice).
    if not st.session_state.saved:
        try:
            save_result(
                'results.csv',
                st.session_state.name,
                quiz.score,
                quiz.total_questions(),
                percentage
            )
            st.session_state.saved = True
            st.info('💾 Your result has been saved.')

        except ResultSaveError as error:
            st.error(f'⚠️ {error}')
    else:
        st.info('💾 Your result has been saved.')

    # Download button: lets staff export the results CSV
    results_path = get_file_path('results.csv')

    if os.path.exists(results_path):
        with open(results_path, 'rb') as file:
            st.download_button(
                '⬇️ Download all results (CSV)',
                data=file,
                file_name='results.csv',
                mime='text/csv'
            )

    if st.button('🔄 Restart Quiz'):
        st.session_state.screen = 'welcome'
        st.session_state.quiz = None
        st.session_state.name = ''
        st.session_state.saved = False
        st.rerun()