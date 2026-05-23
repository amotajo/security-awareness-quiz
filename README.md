The aim of this project is to develop a Python-based GUI quiz application for internal staff that supports security awareness training through multiple-choice questions, result tracking, and CSV-based data storage.

```mermaid
flowchart TD
    A([Start]) --> B[See welcome screen]
    B --> C[/Enter name/]
    C --> D{Name accepted?}
    D -->|No| E[See error message]
    E --> C
    D -->|Yes| F[See question 1 of 10]
    F --> G[/Select answer A B C or D/]
    G --> H{Answer selected?}
    H -->|No| I[See error message]
    I --> F
    H -->|Yes| J[Submit answer]
    J --> K{More questions?}
    K -->|Yes| L[See next question]
    L --> G
    K -->|No| M[See score, percentage and pie chart]
    M --> N{Download results?}
    N -->|Yes| O[Download results.csv]
    N -->|No| P{Restart?}
    O --> P
    P -->|Yes| B
    P -->|No| Z([End])
```

```mermaid
flowchart TD
    A([app.py starts]) --> B[init_state: set default session state values]
    B --> C{screen == 'welcome'?}
    C -->|Yes| D[Render name input and Start button]
    D --> E{is_present and is_valid_name?}
    E -->|No| F[st.error and rerun]
    F --> D
    E -->|Yes| G[load_questions]
    G --> H{QuestionFileError?}
    H -->|Yes| I[st.error and stop]
    H -->|No| J[Create Quiz instance; set screen = 'quiz']
    J --> K{screen == 'quiz'?}
    K -->|Yes| L[Render current question with radio]
    L --> M{is_answer_selected?}
    M -->|No| N[st.error and rerun]
    N --> L
    M -->|Yes| O[quiz.check_answer; quiz.next_question]
    O --> P{quiz.has_more_questions?}
    P -->|Yes| L
    P -->|No| Q[Set screen = 'end']
    Q --> R{screen == 'end'?}
    R -->|Yes| S[Render score, pie chart, download button]
    S --> T{saved flag set?}
    T -->|No| U[save_result; set saved = True]
    T -->|Yes| V[Skip save to avoid duplicates]
    U --> W{Restart clicked?}
    V --> W
    W -->|Yes| X[Reset session state; screen = 'welcome']
    X --> C
    W -->|No| Y([Wait for input])
```