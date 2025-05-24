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