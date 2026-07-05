from langchain_text_splitters import RecursiveCharacterTextSplitter

def dividir_chunks(texto):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50,
        separators=["\n\n", "\n", ".", " ", ""]
    )
    return splitter.split_text(texto)
