import re

def is_present(value):
    return bool(value.strip())

def is_valid_name(name):
    return bool(re.fullmatch(r'[A-Za-z\s\'-]+', name.strip()))

def is_answer_selected(answer):
    return answer in ['A', 'B', 'C', 'D']