from fastapi import FastAPI
from pydantic import BaseModel
from pot_sql_prompt import build_prompt
from db import run_sql_query
import google.generativeai as genai
from dotenv import load_dotenv
import os

load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_CLOUD_API_KEY"))
model = genai.GenerativeModel("gemini-2.5-flash-preview-05-20")

app = FastAPI()

table_info = (
    '"PersonalData"('
    'employee_id INT, first_name TEXT, last_name TEXT, email TEXT, '
    'start_date DATE, end_date DATE, job_title TEXT, department TEXT, '
    'manager_name TEXT, manager_title TEXT, status TEXT, date_of_birth DATE, '
    'employment_type TEXT, location TEXT, net_salary TEXT, tax_paid_2024 TEXT, '
    'leave_days_total INT, leave_days_used INT, skills TEXT, languages TEXT, certifications TEXT'
    '), '
    '"Evaluations"('
    'evaluation_id INT, employee_id INT, evaluation_date DATE, evaluator_name TEXT, '
    'evaluation_type TEXT, aspect TEXT, rating TEXT, comment TEXT, '
    'job_description_text TEXT, language TEXT, rating_score FLOAT, used_in_reference BOOLEAN, '
    'created_at TIMESTAMP, updated_at TIMESTAMP, zielerreichung_percent INT, softskills TEXT, '
    'competency_cluster TEXT, projektbezug TEXT, created_by_hr TEXT, module_type TEXT, '
    'finalized BOOLEAN, approval_status TEXT'
    '), '
    '"Signatories"('
    'signatory_id INT, evaluation_id INT, employee_id INT, signatory_name TEXT, '
    'signed_at TIMESTAMP, comment TEXT'
    ')'
)

class QuestionRequest(BaseModel):
    question: str

@app.post("/execute")
async def generate_and_execute(request: dict):
    try:
        # Fallback für verschiedene LLMs: question, input, query
        question = request.get("question") or request.get("input") or request.get("query")
        if not question:
            return {"error": "Missing 'question', 'input' or 'query' field."}

        prompt = build_prompt(question, table_info)
        response = model.generate_content(prompt)

        generated_sql = (
            response.text
            .replace("```sql", "")
            .replace("```", "")
            .strip()
        )

        if generated_sql.startswith("'") and generated_sql.endswith("'"):
            generated_sql = generated_sql[1:-1].strip()

        print("Generated SQL:\n", generated_sql)

        if generated_sql.lower().strip().startswith("select"):
            result = run_sql_query(generated_sql)
            return {"sql": generated_sql, "result": result}
        else:
            return {
                "error": "Kein gültiges SQL erkannt.",
                "llm_output": generated_sql,
                "hinweis": "Das LLM hat kein SQL erzeugt. Eventuell war die Frage zu unklar."
            }

    except Exception as e:
        return {
            "error": "Fehler bei Ausführung",
            "details": str(e),
            "generated_sql": generated_sql if 'generated_sql' in locals() else "N/A"
        }