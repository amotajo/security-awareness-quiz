'''Tkinter graphical user interface for the Security Awareness Quiz.'''

import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from quiz import Quiz
from storage import load_questions, load_results, save_result
from validation import is_answer_selected, is_present, is_valid_name


class SecurityQuizApp(tk.Tk):
    '''Main graphical user interface for the Security Awareness Quiz.'''

    def __init__(self):
        '''Initialise the main window and application variables.'''
        super().__init__()

        self.geometry('750x550')
        self.title('Security Awareness Quiz')
        self.config(bg='#61009e')

        self.quiz = None
        self.user_name = ''
        self.answer_var = tk.StringVar(value='')
        self.name_entry = None

        self.show_homepage()

    def clear_window(self):
        '''Remove all widgets from the current screen.'''
        for widget in self.winfo_children():
            widget.destroy()

    def show_homepage(self):
        '''Display the homepage where the user enters their name.'''
        self.clear_window()
        self.config(bg='#61009e')

        tk.Label(
            self,
            text='Security Awareness Quiz',
            font=('Arial', 26, 'bold'),
            bg='#61009e',
            fg='white'
        ).pack(pady=40)

        tk.Label(
            self,
            text='Enter Name',
            font=('Arial', 16),
            bg='#61009e',
            fg='white'
        ).pack(pady=10)

        self.name_entry = tk.Entry(
            self,
            font=('Arial', 16),
            bg='light yellow'
        )
        self.name_entry.pack(pady=10, padx=40, fill='x')

        tk.Button(
            self,
            text='Start Quiz',
            command=self.start_quiz,
            font=('Arial', 16),
            bg='white',
            fg='#61009e'
        ).pack(pady=20)

        tk.Button(
            self,
            text='View Previous Results',
            command=self.show_previous_results,
            font=('Arial', 13),
            bg='white',
            fg='#61009e'
        ).pack(pady=10)

    def start_quiz(self):
        '''Validate the user's name, load questions and start the quiz.'''
        name = self.name_entry.get().strip()

        if not is_present(name):
            messagebox.showerror(
                'Input Error',
                'Please enter your name before starting the quiz.'
            )
            return

        if not is_valid_name(name):
            messagebox.showerror(
                'Input Error',
                'Name should only contain letters, spaces, hyphens and apostrophes.'
            )
            return

        try:
            questions = load_questions('questions.csv')
        except FileNotFoundError:
            messagebox.showerror(
                'File Error',
                'The questions.csv file could not be found.'
            )
            return
        except KeyError:
            messagebox.showerror(
                'File Error',
                'The questions.csv file has missing or incorrect headings.'
            )
            return

        if not questions:
            messagebox.showerror(
                'File Error',
                'No questions were found in the questions.csv file.'
            )
            return

        self.user_name = name.title()
        self.quiz = Quiz(questions)
        self.show_question()

    def show_question(self):
        '''Display the current question and answer options.'''
        self.clear_window()
        self.config(bg='#f4f4f4')
        self.answer_var.set('')

        question = self.quiz.get_current_question()
        question_number = self.quiz.current_index + 1
        total_questions = self.quiz.total_questions()

        tk.Label(
            self,
            text=f'Question {question_number} of {total_questions}',
            font=('Arial', 16, 'bold'),
            bg='#f4f4f4',
            fg='black'
        ).pack(pady=20)

        tk.Label(
            self,
            text=question.text,
            font=('Arial', 18),
            bg='#f4f4f4',
            fg='black',
            wraplength=650
        ).pack(pady=20)

        answer_frame = tk.Frame(self, bg='#f4f4f4')
        answer_frame.pack(pady=10, padx=40, fill='x')

        letters = ['A', 'B', 'C', 'D']

        for index, (letter, option) in enumerate(zip(letters, question.options)):
            tk.Radiobutton(
                answer_frame,
                text=f'{letter}. {option}',
                value=letter,
                variable=self.answer_var,
                font=('Arial', 14),
                bg='#f4f4f4',
                fg='black',
                anchor='w'
            ).grid(row=index, column=0, sticky='w', padx=20, pady=8)

        tk.Button(
            self,
            text='Submit Answer',
            command=self.submit_answer,
            font=('Arial', 16),
            bg='#61009e',
            fg='white'
        ).pack(pady=25)

    def submit_answer(self):
        '''Validate and submit the selected answer.'''
        selected_answer = self.answer_var.get()

        if not is_answer_selected(selected_answer):
            messagebox.showerror(
                'Input Error',
                'Please select an answer before continuing.'
            )
            return

        self.quiz.check_answer(selected_answer)
        self.quiz.next_question()

        if self.quiz.has_more_questions():
            self.show_question()
        else:
            self.show_results()

    def show_results(self):
        '''Display the final score, percentage chart and save the result to CSV.'''
        self.clear_window()
        self.config(bg='#61009e')

        score = self.quiz.score
        total = self.quiz.total_questions()
        percentage = self.quiz.calculate_percentage()

        try:
            save_result(
                'results.csv',
                self.user_name,
                score,
                total,
                percentage
            )
            save_message = 'Your result has been saved.'
        except OSError:
            save_message = 'Your score was calculated, but the result could not be saved.'

        tk.Label(
            self,
            text='Quiz Complete',
            font=('Arial', 24, 'bold'),
            bg='#61009e',
            fg='white'
        ).pack(pady=12)

        tk.Label(
            self,
            text=f'Percentage Score: {percentage}%',
            font=('Arial', 17),
            bg='#61009e',
            fg='white'
        ).pack(pady=4)

        tk.Label(
            self,
            text=f'You scored: {score}/{total}',
            font=('Arial', 17),
            bg='#61009e',
            fg='white'
        ).pack(pady=4)

        self.create_percentage_chart(score, total)

        tk.Label(
            self,
            text=save_message,
            font=('Arial', 12),
            bg='#61009e',
            fg='white'
        ).pack(pady=4)

        tk.Button(
            self,
            text='View Previous Results',
            command=self.show_previous_results,
            font=('Arial', 12),
            bg='white',
            fg='#61009e'
        ).pack(pady=3)

        tk.Button(
            self,
            text='Restart Quiz',
            command=self.restart_quiz,
            font=('Arial', 12),
            bg='white',
            fg='#61009e'
        ).pack(pady=3)

        tk.Button(
            self,
            text='Exit',
            command=self.destroy,
            font=('Arial', 12),
            bg='white',
            fg='#61009e'
        ).pack(pady=3)

    def create_percentage_chart(self, score, total):
        '''Create a pie chart on the results page.'''
        incorrect = total - score

        labels = ['Correct', 'Incorrect']
        sizes = [score, incorrect]
        colours = ['#ffffff', '#c9a3e6']

        figure = Figure(figsize=(3, 2.4), dpi=100)
        chart = figure.add_subplot(111)

        chart.pie(
            sizes,
            labels=labels,
            autopct='%1.1f%%',
            startangle=140,
            colors=colours,
            textprops={'fontsize': 8}
        )

        chart.set_title('Result Breakdown', fontsize=10)
        chart.axis('equal')
        figure.patch.set_facecolor('#61009e')

        canvas = FigureCanvasTkAgg(figure, master=self)
        canvas.draw()
        canvas.get_tk_widget().pack(pady=3)

    def show_previous_results(self):
        '''Display saved quiz results in a table.'''
        self.clear_window()
        self.config(bg='#f4f4f4')

        tk.Label(
            self,
            text='Previous Results',
            font=('Arial', 24, 'bold'),
            bg='#f4f4f4',
            fg='black'
        ).pack(pady=20)

        columns = (
            'Name',
            'Score',
            'Total',
            'Percentage',
            'Timestamp'
        )

        results_table = ttk.Treeview(
            self,
            columns=columns,
            show='headings',
            height=10
        )

        for column in columns:
            results_table.heading(column, text=column)
            results_table.column(column, width=130)

        results_table.pack(pady=10)

        try:
            results = load_results('results.csv')
        except OSError:
            messagebox.showerror(
                'File Error',
                'The results file could not be loaded.'
            )
            results = []

        for result in results:
            results_table.insert(
                '',
                tk.END,
                values=(
                    result.get('Name', ''),
                    result.get('Score', ''),
                    result.get('Total', ''),
                    result.get('Percentage', ''),
                    result.get('Timestamp', '')
                )
            )

        if not results:
            tk.Label(
                self,
                text='No saved results are available yet.',
                font=('Arial', 13),
                bg='#f4f4f4',
                fg='black'
            ).pack(pady=10)

        tk.Button(
            self,
            text='Back to Home',
            command=self.restart_quiz,
            font=('Arial', 13),
            bg='#61009e',
            fg='white'
        ).pack(pady=10)

        tk.Button(
            self,
            text='Exit',
            command=self.destroy,
            font=('Arial', 13),
            bg='#61009e',
            fg='white'
        ).pack(pady=5)

    def restart_quiz(self):
        '''Reset the quiz and return to the homepage.'''
        self.quiz = None
        self.user_name = ''
        self.answer_var.set('')
        self.show_homepage()


if __name__ == '__main__':
    app = SecurityQuizApp()
    app.mainloop()