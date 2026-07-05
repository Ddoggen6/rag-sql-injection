import os
from .db import conectar_db, crear_tabla
from .pdf_loader import extraer_texto_pdf
from .chunking import dividir_chunks
from .embeddings import generar_embedding
from .rag_pipeline import responder_con_ia

def procesar_pdf(conn, ruta, titulo):
    paginas = extraer_texto_pdf(ruta)
    cur = conn.cursor()
    total = 0

    for pagina in paginas:
        chunks = dividir_chunks(pagina["texto"])
        for i, chunk in enumerate(chunks):
            emb = generar_embedding(chunk)
            cur.execute("""
                INSERT INTO documentos_pdf (titulo, pagina, chunk_id, texto, embedding)
                VALUES (%s, %s, %s, %s, %s)
            """, (titulo, pagina["pagina"], i, chunk, emb))
            total += 1

    conn.commit()
    cur.close()
    print(f"✅ {total} chunks guardados")

def main():
    conn = conectar_db()
    crear_tabla(conn)

    while True:
        print("\n1. Procesar PDF")
        print("2. Preguntar (RAG)")
        print("3. Salir")
        op = input("> ")

        if op == "1":
            ruta = input("Ruta PDF: ")
            if os.path.exists(ruta):
                titulo = input("Título: ") or os.path.basename(ruta)
                procesar_pdf(conn, ruta, titulo)
            else:
                print("❌ No existe")
        elif op == "2":
            pregunta = input("Pregunta: ")
            print(responder_con_ia(conn, pregunta))
        elif op == "3":
            break

    conn.close()

if __name__ == "__main__":
    main()
