import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

def conectar_db():
    return psycopg2.connect(
        dbname=os.getenv("DB_NAME", "rag_db"),
        user=os.getenv("DB_USER", "postgres"),
        password=os.getenv("DB_PASSWORD", ""),
        host=os.getenv("DB_HOST", "localhost"),
        port=os.getenv("DB_PORT", "5432")
    )

def crear_tabla(conn):
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS documentos_pdf (
            id SERIAL PRIMARY KEY,
            titulo TEXT,
            pagina INTEGER,
            chunk_id INTEGER,
            texto TEXT,
            embedding vector(384)
        );
    """)
    conn.commit()
    cur.close()
