import csv
import os

import psycopg2
from psycopg2 import sql

db_confing = {
    "dbname": os.getenv("POSTGRES_DB", "foodgram"),
    "user": os.getenv("POSTGRES_USER", "foodgram"),
    "password": os.getenv("POSTGRES_PASSWORD", ""),
    "host": os.getenv("DB_HOST", ""),
    "port": os.getenv("DB_PORT", 5432),
}

csv_file_path = "ingredients.csv"

table_name = "recipes_ingredients"

try:
    conn = psycopg2.connect(**db_confing)
    cursor = conn.cursor()
    with open(csv_file_path, newline="") as csvfile:
        reader = csv.reader(csvfile)
        next(reader)
        for row in reader:
            query = sql.SQL(
                "INSERT INTO {}(name, measurement_unit) VALUES (%s, %s)"
            ).format(sql.Identifier(table_name))
            cursor.execute(query, row)
    conn.commit()

except Exception as e:
    print(f"Error {e}")
    conn.rollback()

if cursor:
    cursor.close()
if conn:
    conn.close()
