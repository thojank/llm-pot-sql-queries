import streamlit as st
import pandas as pd
import google.generativeai as genai
from dotenv import load_dotenv
import os
import psycopg2
from pot_sql_prompt import build_prompt
from db import run_sql_query

load_dotenv()

# Set up Gemini
API_KEY = os.getenv("GOOGLE_CLOUD_API_KEY")
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel("models/gemini-1.5-flash-latest")

# Set up database
DB_URL = os.getenv("DATABASE_URL")
conn = psycopg2.connect(DB_URL)

st.set_page_config(page_title="Program-of-Thought SQL Generator", layout="wide")
st.title("🧠 Program-of-Thought SQL Generator")
st.caption("Powered by Gemini 2.5 + Streamlit + PostgreSQL")

st.markdown("""
Diese App erzeugt automatisch SQL-Abfragen aus deiner Eingabe und führt sie direkt aus. 
Bitte gib eine **natürlichsprachliche Frage** ein, z.B.:

- *Wie viele Urlaubstage hat Max Mustermann noch?*
- *Gibt es eine Person namens Thorsten Jankowski?*
- *Zeige alle Mitarbeitenden mit weniger als 5 Tagen Urlaub.*
""")

question = st.text_input("Deine Frage an die Datenbank:")

# Tabellenbeschreibung (fixiert)
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
    '), '
    '"Evaluations"('
    'evaluation_id INT, '
    'employee_id INT, '
    'evaluation_date DATE, '
    'evaluator_name TEXT, '
    'evaluation_type TEXT, '
    'aspect TEXT, '
    'rating TEXT, '
    'comment TEXT, '
    'job_description_text TEXT, '
    'language TEXT, '
    'rating_score FLOAT, '
    'used_in_reference BOOLEAN, '
    'created_at TIMESTAMP, '
    'updated_at TIMESTAMP, '
    'zielerreichung_percent INT, '
    'softskills TEXT, '
    'competency_cluster TEXT, '
    'projektbezug TEXT, '
    'created_by_hr TEXT, '
    'module_type TEXT, '
    'finalized BOOLEAN, '
    'approval_status TEXT'
    '), '
    '"Signatories"('
    'signatory_id INT, '
    'evaluation_id INT, '
    'employee_id INT, '
    'signatory_name TEXT, '
    'signed_at TIMESTAMP, '
    'comment TEXT'
    ')'
)

# Helper: run sql query
def run_sql(conn, query):
    try:
        df = pd.read_sql_query(query, conn)
        return df
    except Exception as e:
        st.error(f"Fehler bei der SQL-Ausführung: {e}")
        return pd.DataFrame()

# Helper: call Gemini and clean output
def generate_sql(prompt):
    chat = model.start_chat(history=[])
    response = chat.send_message(prompt)
    return (
        response.text
        .replace("```sql", "")
        .replace("```", "")
        .strip()
    )

if question:
    prompt = build_prompt(question, table_info)
    st.markdown("### Prompt")
    st.code(prompt)

    with st.spinner("Frage wird analysiert..."):
        sql = generate_sql(prompt)
        st.markdown("### Generiertes SQL")
        st.code(sql)

        result_df = run_sql(conn, sql)
        st.markdown("### Ergebnis")
        st.dataframe(result_df)