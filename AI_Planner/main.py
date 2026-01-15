import streamlit as st
from groq import Groq
import json
from datetime import datetime
import os


# =========================
#  KONFIGURACJA GROQ
# =========================

def get_api_key() -> str:
    if "GROQ_API_KEY" in st.secrets:
        return st.secrets["GROQ_API_KEY"]
    return os.environ.get("GROQ_API_KEY", "")

API_KEY = get_api_key()

if not API_KEY:
    st.error("Brak GROQ_API_KEY. Dodaj do .streamlit/secrets.toml albo ustaw zmienną środowiskową GROQ_API_KEY.")
    st.stop()

client = Groq(api_key=API_KEY)

MODEL_NAME = "llama-3.3-70b-versatile"


# =========================
#  FUNKCJA AGENTA
# =========================
def generate_schedule(tasks_text: str, constraints_text: str) -> dict:
    prompt = f"""
Jesteś ekspertem od zarządzania czasem. Stwórz harmonogram dnia.

ZADANIA (tekst użytkownika):
{tasks_text}

OGRANICZENIA:
{constraints_text}

ZASADY:
1) Zwróć WYŁĄCZNIE poprawny JSON **OBIEKT** (nie lista).
2) JSON ma mieć dokładnie strukturę:
{{
  "schedule": [
    {{"task":"nazwa","start":"HH:MM","end":"HH:MM","reason":"uzasadnienie","notes":""}}
  ],
  "unscheduled": [
    {{"task":"nazwa","reason":"czemu się nie zmieściło"}}
  ]
}}
3) Godziny mają być w formacie HH:MM (24h).
4) Harmonogram ma mieścić się w oknie czasu z ograniczeń.
5) Jeśli nie da się czegoś zaplanować — wrzuć to do unscheduled.
"""

    resp = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {"role": "system", "content": "Zwracasz WYŁĄCZNIE poprawny JSON w odpowiedzi."},
            {"role": "user", "content": prompt},
        ],
        temperature=0.3,
        response_format={"type": "json_object"},
    )

    content = resp.choices[0].message.content
    clean = (content or "").replace("```json", "").replace("```", "").strip()
    return json.loads(clean)


# =========================
#  UI (STREAMLIT)
# =========================
st.set_page_config(page_title="AI Planner (Groq)", layout="centered", page_icon="⚡")
st.title("⚡ AI Planner – Powered by Groq")

with st.sidebar:
    st.header("⚙️ Ustawienia")
    work_start = st.time_input("Początek dnia", datetime.strptime("08:00", "%H:%M"))
    work_end = st.time_input("Koniec dnia", datetime.strptime("22:00", "%H:%M"))
    energy = st.select_slider("Energia", options=["Niska", "Średnia", "Wysoka"])

st.subheader("Wpisz swoje zadania:")
user_input = st.text_area(
    "Np.:\n- trening 60 min\n- praca nad projektem 3h\n- zakupy 45 min\n(ważne: podawaj czasy, żeby plan był stabilny)",
    height=170
)

if st.button("Generuj Plan"):
    if not user_input.strip():
        st.warning("Dodaj jakieś zadania!")
    else:
        with st.spinner("Groq generuje plan..."):
            try:
                constraints = f"Dzień od {work_start.strftime('%H:%M')} do {work_end.strftime('%H:%M')}. Energia: {energy}."
                data = generate_schedule(user_input, constraints)

                schedule = data.get("schedule", [])
                unscheduled = data.get("unscheduled", [])

                if not schedule and not unscheduled:
                    st.error("Model zwrócił pustą odpowiedź. Spróbuj dopisać czasy trwania do zadań i ponowić.")
                    st.stop()

                st.success("Plan gotowy!")

                if schedule:
                    st.subheader("📅 Harmonogram")
                    for item in schedule:
                        start = item.get("start", "?")
                        end = item.get("end", "?")
                        task = item.get("task", "(brak nazwy)")
                        with st.expander(f"**{start} - {end}**: {task}"):
                            st.write(f"**Dlaczego:** {item.get('reason','')}")
                            if item.get("notes"):
                                st.info(item["notes"])

                    st.table(schedule)

                if unscheduled:
                    st.subheader("⚠️ Niezaplanowane")
                    st.table(unscheduled)

            except Exception as e:
                st.error(f"Wystąpił błąd: {e}")
                st.info("Sprawdź: (1) czy masz dobry GROQ_API_KEY, (2) czy model jest dostępny, (3) czy zadania mają czasy.")
