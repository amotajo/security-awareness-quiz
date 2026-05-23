The aim of this project is to develop a Python-based GUI quiz application for internal staff that supports security awareness training through multiple-choice questions, result tracking, and CSV-based data storage.

┌──────────────────────────┐
│  Question                │
├──────────────────────────┤
│  + text: str             │
│  + options: list         │
│  + answer: str           │
├──────────────────────────┤
│  + __init__()            │
│  + is_correct(answer)    │
└──────────────────────────┘

┌────────────────────────────────┐
│  Quiz                          │
├────────────────────────────────┤
│  + questions: list[Question]   │
│  + score: int                  │
│  + current_index: int          │
├────────────────────────────────┤
│  + __init__()                  │
│  + get_current_question()      │
│  + check_answer(answer)        │
│  + next_question()             │
│  + has_more_questions()        │
│  + total_questions()           │
│  + calculate_percentage()      │
└────────────────────────────────┘