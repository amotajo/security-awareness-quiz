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
            try:
                questions = load_questions('questions.csv')

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

        # Radio buttons. index=None means nothing is pre-selected,
        # so the user must actively choose an option.
        selected = st.radio(
            '👉 Choose your answer',
            ['A', 'B', 'C', 'D'],
            index=None,
            format_func=lambda letter: format_option(letter, question)
        )

        if st.button('✅ Submit Answer'):

            if selected is None or not is_answer_selected(selected):
                st.error('⚠️ Please select an answer before continuing.')

            else:
                quiz.check_answer(selected)
                quiz.next_question()

                if not quiz.has_more_questions():
                    st.session_state.screen = 'end'

                st.rerun()


# --- End screen ---
elif st.session_state.screen == 'end':

    quiz = st.session_state.quiz
    percentage = quiz.calculate_percentage()

    st.success('🎉 Quiz Complete!')
    st.balloons()

    st.metric('🏆 Final Score', f'{quiz.score} / {quiz.total_questions()}')

    # Pie chart showing correct vs incorrect
    correct = quiz.score
    incorrect = quiz.total_questions() - quiz.score

    figure, axis = plt.subplots()
    axis.pie(
        [correct, incorrect],
        labels=['Correct', 'Incorrect'],
        colors=['#4CAF50', '#F44336'],
        autopct='%1.1f%%'
    )
    st.pyplot(figure)

    st.metric('📊 Percentage Score', f'{percentage}%')

    # Save the result once per completion
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

    # Download button for staff to export results
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