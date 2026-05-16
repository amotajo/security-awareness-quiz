import streamlit as st
from quiz import Quiz
from storage import load_questions
from validation import is_present

# --- Session state ---
if 'quiz_started' not in st.session_state:
    st.session_state.quiz_started = False

if 'quiz' not in st.session_state:
    st.session_state.quiz = None

if 'name' not in st.session_state:
    st.session_state.name = ''

st.set_page_config(
    page_title='Security Awareness Quiz',
    page_icon='🔐'
)

st.title('Security Awareness Quiz')

# --- Homepage ---
if not st.session_state.quiz_started:

    name = st.text_input('Enter your name')

    if st.button('Start Quiz'):

        if not is_present(name):
            st.error('Please enter your name before starting the quiz.')

        else:
            questions = load_questions('questions.csv')

            st.session_state.quiz = Quiz(questions)
            st.session_state.quiz_started = True
            st.session_state.name = name.title()

            st.rerun()

# --- Question screen ---
else:

    quiz = st.session_state.quiz

    if quiz.has_more_questions():

        question = quiz.get_current_question()

        st.subheader(
            f'Question {quiz.current_index + 1} of {quiz.total_questions()}'
        )

        st.write(question.text)