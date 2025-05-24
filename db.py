import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

def run_sql_query(sql: str):
    #return False
    conn = psycopg2.connect(os.getenv("DATABASE_URL"))
    try:
        with conn.cursor() as cur:
            cur.execute(sql)
            return cur.fetchall()
    finally:
        conn.close()

def schema_to_str(schema):
    lines = []
    for table in schema:
        lines.append(f"Table: {table['table_name']}")
        for col in table["columns"]:
            line = f"  - {col['name']} ({col['type']})"
            if col.get("is_primary_key"):
                line += " [PK]"
            if col.get("is_foreign_key"):
                line += f" [FK → {col['references']}]"
            lines.append(line)
        lines.append("")  # blank line between tables
    return "\n".join(lines)