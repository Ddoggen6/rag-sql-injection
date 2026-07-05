from .embeddings import generar_embedding

def buscar(conn, consulta, limite=5):
    cur = conn.cursor()
    emb = generar_embedding(consulta)
    cur.execute("""
        SELECT titulo, pagina, chunk_id, texto,
               1 - (embedding <=> %s::vector) AS similitud
        FROM documentos_pdf
        ORDER BY embedding <=> %s::vector
        LIMIT %s;
    """, (emb, emb, limite))
    resultados = cur.fetchall()
    cur.close()
    return resultados
