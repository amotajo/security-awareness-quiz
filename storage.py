import csv
import os
from datetime import datetime

from models import Question

def get_file_path(filename):
    if os.path.isabs(filename):
        return filename

    base_dir = os.path.dirname(__file__)
    return os.path.join(base_dir, filename)

def load_questions(filename):
    filepath = get_file_path(filename)
    questions = []

    with open(filepath, newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)

        for row in reader:
            text = row['Question']
            options = [
                row['OptionA'],
                row['OptionB'],
                row['OptionC'],
                row['OptionD']
            ]
            answer = row['Answer']

            questions.append(Question(text, options, answer))

    return questions

def save_result(filename, name, score, total, percentage):
    filepath = get_file_path(filename)
    file_exists = os.path.exists(filepath)

    fieldnames = [
        'Name',
        'Score',
        'Total',
        'Percentage',
        'Timestamp'
    ]

    with open(filepath, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)

        if not file_exists or os.path.getsize(filepath) == 0:
            writer.writeheader()

        writer.writerow({
            'Name': name,
            'Score': score,
            'Total': total,
            'Percentage': percentage,
            'Timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        })

def load_results(filename):
    filepath = get_file_path(filename)

    if not os.path.exists(filepath) or os.path.getsize(filepath) == 0:
        return []

    with open(filepath, newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        return list(reader)