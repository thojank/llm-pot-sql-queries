def build_prompt(question: str, table_info: str = ""):
    return f"""
You are an intelligent assistant that generates SQL queries by reasoning step-by-step.

User Question:
"{question}"

Table Information:
{table_info}

The tables are related as follows:
- "PersonalData.employee_id" ↔ "Evaluations.employee_id"
- "Evaluations.evaluation_id" ↔ "Signatories.evaluation_id"

Step-by-step reasoning:
1. Identify the key information in the question.
2. Understand what the user wants to know.
3. Determine whether data from multiple tables is needed and what JOINs are appropriate.
4. Write an appropriate SQL query using correct PostgreSQL syntax.
5. Enclose all table and column names in double quotes.
6. Return only the SQL query, nothing else.

Only output the final SQL query on the last line, nothing else.
"""