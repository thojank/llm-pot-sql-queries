import streamlit as st
from pot_sql_prompt import build_prompt
from db import run_sql_query
import google.generativeai as genai
from dotenv import load_dotenv
import os

# Lade Umgebungsvariablen aus .env-Datei
load_dotenv()

# Konfiguration mit API-Key
genai.configure(api_key=os.getenv("GOOGLE_CLOUD_API_KEY"))

# Modellinitialisierung
model = genai.GenerativeModel("gemini-2.5-flash-preview-05-20")

# UI
st.title("🧠 Program-of-Thought SQL Generator (Gemini via GenerativeAI)")
st.write("Stelle eine Frage, und Gemini generiert dir automatisch eine passende SQL-Query.")

# Nutzerfrage eingeben
question = st.text_input("Deine Frage:", placeholder="z. B. Gibt es einen User namens Max Müller?")

# Wenn Frage gestellt wird
if st.button("Frage stellen") and question:

    # Tabellenbeschreibung für Gemini
    table_info = (
        '"PersonalData"('
        'employee_id INT, '
        'first_name TEXT, '
        'last_name TEXT, '
        'email TEXT, '
        'start_date DATE, '
        'end_date DATE, '
        'job_title TEXT, '
        'department TEXT, '
        'manager_name TEXT, '
        'manager_title TEXT, '
        'status TEXT, '
        'date_of_birth DATE, '
        'employment_type TEXT, '
        'location TEXT, '
        'net_salary TEXT, '
        'tax_paid_2024 TEXT, '
        'leave_days_total INT, '
        'leave_days_used INT, '
        'skills TEXT, '
        'languages TEXT, '
        'certifications TEXT'
        ')'
    )

    # Prompt generieren
    prompt = build_prompt(question, table_info)

    # Prompt anzeigen
    st.text("🧾 Generierter Prompt:")
    st.code(prompt)

    try:
        # Aufruf bei Gemini
        response = model.generate_content(prompt)
        generated_sql = response.text.strip().replace("```", "").replace("sql\n", "")

        # SQL anzeigen
        st.text("💡 Generierte SQL-Abfrage:")
        st.code(generated_sql, language="sql")

        # Ausführen
        results = run_sql_query(generated_sql)

        if not results:
            st.warning("Kein Ergebnis gefunden.")
        else:
            st.success(f"✅ {len(results)} Ergebnis(se) gefunden:")
            st.dataframe(results)

    except Exception as e:
        st.error(f"❌ Fehler: {str(e)}")