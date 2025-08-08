# export_all_json.py
import os, json
import psycopg2
from psycopg2.extras import RealDictCursor
from datetime import datetime, date, time

# Carrega a URL do .env ou defina manualmente
DATABASE_URL = os.getenv(
  "DATABASE_URL",
  "postgresql://nichollas:M4n1ck#212021#@localhost:5432/newlife_local"
)

def convert_datetime_objects(obj):
    """Converte objetos datetime, date e time para strings ISO formatadas"""
    if isinstance(obj, datetime):
        return obj.isoformat()
    elif isinstance(obj, date):
        return obj.isoformat()
    elif isinstance(obj, time):
        return obj.isoformat()
    elif isinstance(obj, dict):
        return {key: convert_datetime_objects(value) for key, value in obj.items()}
    elif isinstance(obj, list):
        return [convert_datetime_objects(item) for item in obj]
    else:
        return obj

conn = psycopg2.connect(DATABASE_URL)
cur = conn.cursor(cursor_factory=RealDictCursor)

# Pega todas as tabelas do schema público
cur.execute("""
  SELECT tablename
    FROM pg_tables
   WHERE schemaname = 'public';
""")
tables = [row["tablename"] for row in cur.fetchall()]

os.makedirs("backup/json", exist_ok=True)
all_data = {}

for table in tables:
    print(f"Exportando {table}...")
    cur.execute(f"SELECT * FROM {table};")
    rows = cur.fetchall()             # cada row é um dict
    # Converte objetos datetime antes de serializar
    rows_converted = convert_datetime_objects(rows)
    all_data[table] = rows_converted
    # opcional: salvar por tabela
    with open(f"backup/json/{table}.json", "w", encoding="utf-8") as f:
        json.dump(rows_converted, f, ensure_ascii=False, indent=2)

# opcional: salvar tudo num único arquivo
with open("backup/json/all_data.json", "w", encoding="utf-8") as f:
    json.dump(all_data, f, ensure_ascii=False, indent=2)

cur.close()
conn.close()
print("Exportação Python concluída!")
