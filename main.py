import streamlit as st
from pot_sql_prompt import build_prompt
from db import run_sql_query, schema_to_str
import google.generativeai as genai
from dotenv import load_dotenv
import os
import json

with open("db_schema.json") as f:
    schema_dict = json.load(f)

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
question = st.text_input("Deine Frage:", placeholder="z. B. Gib mir alle verfügbare Informationen über Max Müller?")

# Wenn Frage gestellt wird
if st.button("Frage stellen") and question:

    table_info = schema_to_str(schema_dict)

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