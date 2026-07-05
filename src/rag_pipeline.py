from .search import buscar

def responder_sin_ia(conn, pregunta):
    resultados = buscar(conn, pregunta)
    if not resultados:
        return "No se encontró información relevante."
    
    fragmentos = []
    for titulo, pagina, chunk_id, texto, similitud in resultados[:3]:
        fragmentos.append(f"[Fragmento {chunk_id} - Pág. {pagina}]\n{texto}")
    
    return "\n\n---\n\n".join(fragmentos)

# Alias para mantener compatibilidad
responder_con_ia = responder_sin_ia
