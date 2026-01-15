# AI Planner (LLM + Groq + Streamlit)

Aplikacja webowa do planowania dnia.  
Użytkownik wpisuje zadania (tekstowo) oraz ustawia godziny dnia i poziom energii, a następnie **model LLM (Groq / LLaMA 3.3)** generuje harmonogram w formie JSON i wyświetla go w interfejsie Streamlit.

## Uruchomienie

1) Zainstaluj wymagane biblioteki:

pip install streamlit groq

2) Ustaw klucz API Groq (PowerShell):

$env:GROQ_API_KEY="Twój klucz"

3) Uruchom aplikację:

streamlit run main.py

4) Aplikacja otworzy się w przeglądarce pod adresem: http://localhost:8501
