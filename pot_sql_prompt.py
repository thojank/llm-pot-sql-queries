def build_prompt(question: str, table_info: str = ""):
    return f"""
You are an intelligent assistant that generates SQL queries by reasoning step-by-step.

User Question:
"{question}"

Table Information:
{table_info}

Step-by-step reasoning:
1. Identify the key information in the question.
2. Understand what the user wants to know.
3. Write an appropriate SQL query to answer it.
4. Use correct SQL syntax for PostgreSQL.
5. Enclose all table names and column names that contain capital letters in double quotes.
6. Return only the SQL query.

Only output the final SQL query on the last line, nothing else.
"""