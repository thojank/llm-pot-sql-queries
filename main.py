import streamlit as st
from pot_sql_prompt import build_prompt
from db import run_sql_query
from google import genai
from google.genai import types
import os
from dotenv import load_dotenv

load_dotenv()

# Set up Gemini client
client = genai.Client(
    vertexai=True,
    api_key=os.environ.get("GOOGLE_CLOUD_API_KEY")
)

st.title("🧠 Program-of-Thought SQL Generator (Gemini Flash, VertexAI Client)")
st.write("Ask a question and let the AI generate and run SQL for you using Google's PoT + Gemini Flash.")

question = st.text_input("Enter your question", placeholder="e.g. Is Max Müller a valid user?")

if st.button("Ask") and question:
    table_info = "users(first_name TEXT, last_name TEXT)"
    prompt = build_prompt(question, table_info)

    # Create structured content
    contents = [
        types.Content(
            role="user",
            parts=[types.Part(text=prompt),
                   ]
        )
    ]

    # Define generation config
    generate_content_config = types.GenerateContentConfig(
        temperature=1.0,
        max_output_tokens=8192,
        response_modalities=["TEXT"],
        system_instruction=[
            "You are an intelligent assistant that generates SQL queries by reasoning step-by-step."
        ],
        safety_settings=[
            types.SafetySetting(category="HARM_CATEGORY_HATE_SPEECH", threshold="OFF"),
            types.SafetySetting(category="HARM_CATEGORY_DANGEROUS_CONTENT", threshold="OFF"),
            types.SafetySetting(category="HARM_CATEGORY_SEXUALLY_EXPLICIT", threshold="OFF"),
            types.SafetySetting(category="HARM_CATEGORY_HARASSMENT", threshold="OFF"),
        ]
    )

    model = "gemini-2.5-flash-preview-05-20"

    with st.spinner("Thinking with Gemini Flash..."):
        try:
            sql_lines = []
            for chunk in client.models.generate_content_stream(
                model=model,
                contents=contents,
                config=generate_content_config
            ):
                if chunk.text:
                    sql_lines.append(chunk.text)

            st.text("A complete prompt:")
            st.code(prompt)

            st.text("Model used:")
            st.code(model)
            
            full_response = "".join(sql_lines).strip().replace("```", "").replace("sql\n","")
            st.code(full_response, language="sql")

            results = run_sql_query(full_response)

            if not results:
                st.warning("No results found.")
            else:
                st.success(f"✅ Found {len(results)} matching record(s).")
                st.dataframe(results)

        except Exception as e:
            st.error(f"❌ Error: {str(e)}")
