def build_prompt(question: str, table_info: str = ""):
    return f"""
You are an intelligent assistant that generates SQL queries by reasoning step-by-step.

User Question:
"{question}"

DB Schema:
{table_info}

Instructions:
1. Identify the key information in the question.
2. Understand what the user wants to know.
3. Identify the relevant tables based on the question.
4. Determine relationships between these tables (e.g., via foreign keys).
5. Choose the correct columns to select, filter, and join on.
6. Use valid PostgreSQL syntax.
7. Enclose table and column names in double quotes.
8. Output only the SQL query on the last line, nothing else.

"""