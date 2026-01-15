# \# ⚡ AI Planner – Inteligentny plan dnia (LLM + Groq + Streamlit)

# 

# Aplikacja webowa, która generuje harmonogram dnia na podstawie listy zadań i ograniczeń czasowych.

# W projekcie wykorzystano \*\*LLM (Large Language Model)\*\* dostępny przez \*\*Groq API\*\* (model: `llama-3.3-70b-versatile`),

# który pełni rolę \*\*agenta planującego\*\*.

# 

# ---

# 

# \## 🎯 Funkcje aplikacji

# \- ✅ wpisywanie zadań w języku naturalnym (tekstowo)

# \- ✅ ustawienie początku i końca dnia

# \- ✅ wybór poziomu energii (niska/średnia/wysoka)

# \- ✅ generowanie harmonogramu z godzinami `start/end`

# \- ✅ uzasadnienie planu dla każdego zadania (`reason`)

# \- ✅ lista zadań, których nie udało się zaplanować (`unscheduled`)

# \- ✅ interfejs webowy w Streamlit

# 

# ---

# 

# \## 🧠 Jak działa LLM w projekcie?

# 1\. Użytkownik podaje zadania i ograniczenia.

# 2\. Aplikacja buduje \*\*prompt\*\* (opis problemu + zasady planowania).

# 3\. LLM przez Groq API generuje wynik jako \*\*JSON\*\* w strukturze:

# &nbsp;  - `schedule` (zaplanowane zadania),

# &nbsp;  - `unscheduled` (zadania, których nie dało się zmieścić w czasie).

# 4\. Aplikacja parsuje JSON i wyświetla plan w interfejsie.

# 

# ---

# 

# \## 🧾 Format odpowiedzi (JSON)

# Model zwraca wynik w formacie:

# 

# ```json

# {

# &nbsp; "schedule": \[

# &nbsp;   {

# &nbsp;     "task": "Siłownia 1h",

# &nbsp;     "start": "20:00",

# &nbsp;     "end": "21:00",

# &nbsp;     "reason": "Uzasadnienie",

# &nbsp;     "notes": ""

# &nbsp;   }

# &nbsp; ],

# &nbsp; "unscheduled": \[

# &nbsp;   {

# &nbsp;     "task": "Zadanie X",

# &nbsp;     "reason": "Brak miejsca w planie"

# &nbsp;   }

# &nbsp; ]

# }





