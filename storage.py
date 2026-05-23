"""CSV storage layer for loading questions and saving results.

This module raises descriptive exceptions when files are missing or
malformed, so the UI layer can catch them and show a friendly message.
"""

import csv
import os
from datetime import datetime

from models import Question


class QuestionFileError(Exception):
    """Raised when the questions CSV file cannot be loaded or is malformed."""


class ResultSaveError(Exception):
    """Raised when a quiz result cannot be saved to disk."""


def get_file_path(filename):
    """Return an absolute path for a filename.

    If the filename is already absolute it is returned unchanged.
    Otherwise it is resolved relative to this module's directory.

    Args:
        filename: A file name or absolute path.

    Returns:
        str: The absolute file path.
    """
    if os.path.isabs(filename):
        return filename

    base_dir = os.path.dirname(__file__)
    return os.path.join(base_dir, filename)


def load_questions(filename):
    """Load questions from a CSV file and return them as Question objects.

    Args:
        filename: The CSV file name or absolute path.

    Returns:
        list[Question]: The questions parsed from the file.

    Raises:
        QuestionFileError: If the file is missing, empty, or has the wrong columns.
    """
    filepath = get_file_path(filename)

    # Check the file exists before trying to open it
    if not os.path.exists(filepath):
        raise QuestionFileError(
            f'The questions file could not be found: {filename}'
        )

    questions = []

    try:
        with open(filepath, newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)

            for row in reader:
                text = row['Question']
                options = [
                    row['OptionA'],
                    row['OptionB'],
                    row['OptionC'],
                    row['OptionD'],
                ]
                answer = row['Answer']
                questions.append(Question(text, options, answer))

    except KeyError as error:
        # A column was missing from the CSV header
        raise QuestionFileError(
            f'The questions file is missing a required column: {error}'
        )

    except OSError as error:
        # The file could not be opened or read
        raise QuestionFileError(
            f'The questions file could not be read: {error}'
        )

    except csv.Error as error:
        # The CSV is malformed
        raise QuestionFileError(
            f'The questions file could not be read: {error}'
        )

    # If we got here but no rows were parsed, the file is empty
    if not questions:
        raise QuestionFileError('The questions file is empty.')

    return questions


def save_result(filename, name, score, total, percentage):
    """Append a single quiz result row to the results CSV file.

    Writes a header row first if the file does not yet exist or is empty.

    Args:
        filename: The CSV file name or absolute path.
        name: The participant's name.
        score: The number of correct answers.
        total: The total number of questions.
        percentage: The final percentage score.

    Raises:
        ResultSaveError: If the result cannot be written to disk.
    """
    filepath = get_file_path(filename)
    file_exists = os.path.exists(filepath)

    fieldnames = ['Name', 'Score', 'Total', 'Percentage', 'Timestamp']

    try:
        with open(filepath, mode='a', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)

            # Write the header if this is the first time we are writing
            if not file_exists or os.path.getsize(filepath) == 0:
                writer.writeheader()

            writer.writerow({
                'Name': name,
                'Score': score,
                'Total': total,
                'Percentage': percentage,
                'Timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            })

    except OSError as error:
        raise ResultSaveError(
            f'The result could not be saved: {error}'
        )


def load_results(filename):
    """Load all saved quiz results from the CSV file.

    Args:
        filename: The CSV file name or absolute path.

    Returns:
        list[dict]: One dict per result row. Empty list if the file is missing or empty.
    """
    filepath = get_file_path(filename)

    if not os.path.exists(filepath) or os.path.getsize(filepath) == 0:
        return []

    with open(filepath, newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        return list(reader)