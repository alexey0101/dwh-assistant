import pandas as pd
import psycopg2
from psycopg2.extras import RealDictCursor
from config import Config


def get_connection():
    conn_string = (
        f"host={Config.PG_HOST} port={Config.PG_PORT} dbname={Config.PG_DBNAME} "
        f"user={Config.PG_USER} password={Config.PG_PASSWORD}"
    )
    return psycopg2.connect(conn_string)

def execute_sql_query(sql_query):
    """
    Выполняет SQL-запрос в базе данных PostgreSQL и возвращает результаты.
    """
    answer = {"result": None, "error": None}
    try:
        with get_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute(sql_query)
                if sql_query.strip().lower().startswith("select"):
                    records = cursor.fetchall()
                    df = pd.DataFrame(records)
                    answer["result"] = df
                else:
                    raise ValueError("Только SELECT запросы разрешены.")
    except Exception as e:
        print(f"Ошибка выполнения SQL-запроса: {e}")
        answer["error"] = str(e)
    return answer
