from sentence_transformers import SentenceTransformer

modelo = None

def cargar_modelo():
    global modelo
    if modelo is None:
        modelo = SentenceTransformer('all-MiniLM-L6-v2')
    return modelo

def generar_embedding(texto):
    modelo = cargar_modelo()
    return modelo.encode(texto).tolist()
