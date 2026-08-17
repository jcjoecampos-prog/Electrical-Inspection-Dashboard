import os
from pathlib import Path

import psycopg
from dotenv import load_dotenv

load_dotenv()

SQL_FILE = Path("sql/005_join_analysis.sql")

def run_join_analysis() -> None:
    """Execute join analysis queries against PostgreSQL"""

    sql_text = SQL_FILE.read_text(encoding="utf-8")

    queries = [
        query.strip()
        for query in sql_text.split(";")
        if query.strip()
    ]

    connection = psycopg.connect(
        host = os.getenv("DB_HOST"),
        port = os.getenv("DB_PORT"),
        dbname = os.getenv("DB_NAME"),
        user = os.getenv("DB_USER"),
        password = os.getenv("DB_PASSWORD")
    )

    try:
        with connection.cursor() as cursor:
            for query_number, query in enumerate(
                queries,
                start = 1,
            ):
                print(f"\n--- Query {query_number} ---")

                cursor.execute(query)

                column_names = [
                    column.name
                    for column in cursor.description
                ]

                print(" | ".join(column_names))

                rows = cursor.fetchall()

                for row in rows:
                    print(" | ".join(str(value) for value in row))

                print(f"Rows returned: {len(rows)}")

    finally:
        connection.close()
if __name__ == "__main__":
    run_join_analysis()
