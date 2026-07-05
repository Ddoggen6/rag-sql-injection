import PyPDF2

def extraer_texto_pdf(ruta):
    paginas = []
    with open(ruta, 'rb') as archivo:
        lector = PyPDF2.PdfReader(archivo)
        for i, pagina in enumerate(lector.pages):
            texto = pagina.extract_text()
            if texto.strip():
                paginas.append({"pagina": i + 1, "texto": texto})
    return paginas
