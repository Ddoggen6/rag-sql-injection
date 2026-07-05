import os
import tempfile
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from werkzeug.utils import secure_filename
from .db import conectar_db, crear_tabla
from .pdf_loader import extraer_texto_pdf
from .chunking import dividir_chunks
from .embeddings import generar_embedding
from .rag_pipeline import responder_con_ia

app = Flask(__name__)
CORS(app)  # Permitir conexiones desde otras máquinas

# Configuración
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50MB max
UPLOAD_FOLDER = tempfile.gettempdir()
ALLOWED_EXTENSIONS = {'pdf'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>RAG System - SQL Injection Knowledge Base</title>
        <style>
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                max-width: 800px;
                margin: 0 auto;
                padding: 20px;
                background: #f5f5f5;
            }
            .container {
                background: white;
                padding: 30px;
                border-radius: 10px;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            }
            h1 {
                color: #333;
                border-bottom: 3px solid #4CAF50;
                padding-bottom: 10px;
            }
            .section {
                margin: 30px 0;
                padding: 20px;
                background: #f9f9f9;
                border-radius: 8px;
            }
            input, textarea {
                width: 100%;
                padding: 10px;
                margin: 10px 0;
                border: 1px solid #ddd;
                border-radius: 4px;
                box-sizing: border-box;
            }
            button {
                background: #4CAF50;
                color: white;
                padding: 10px 20px;
                border: none;
                border-radius: 4px;
                cursor: pointer;
                font-size: 16px;
            }
            button:hover {
                background: #45a049;
            }
            .result {
                background: #e8f5e9;
                padding: 15px;
                border-radius: 5px;
                margin-top: 20px;
                white-space: pre-wrap;
                font-family: monospace;
            }
            .error {
                background: #ffebee;
                color: #c62828;
            }
            .status {
                font-size: 12px;
                color: #666;
                margin-top: 5px;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>📚 RAG System - SQL Injection Knowledge Base</h1>
            <p>Sube PDFs y haz preguntas sobre su contenido.</p>
            
            <div class="section">
                <h2>📄 Subir PDF</h2>
                <form id="uploadForm" enctype="multipart/form-data">
                    <input type="file" id="pdfFile" accept=".pdf" required>
                    <input type="text" id="title" placeholder="Título (opcional)">
                    <button type="submit">Subir y Procesar</button>
                </form>
                <div id="uploadResult" class="status"></div>
            </div>
            
            <div class="section">
                <h2>🤖 Hacer Pregunta</h2>
                <form id="queryForm">
                    <textarea id="question" rows="3" placeholder="Escribe tu pregunta sobre SQL injection..." required></textarea>
                    <button type="submit">Preguntar</button>
                </form>
                <div id="queryResult" class="result"></div>
            </div>
        </div>
        
        <script>
            document.getElementById('uploadForm').onsubmit = async (e) => {
                e.preventDefault();
                const file = document.getElementById('pdfFile').files[0];
                const title = document.getElementById('title').value;
                if (!file) return;
                
                const formData = new FormData();
                formData.append('file', file);
                formData.append('title', title);
                
                const resultDiv = document.getElementById('uploadResult');
                resultDiv.textContent = '⏳ Procesando PDF...';
                resultDiv.style.color = '#666';
                
                try {
                    const res = await fetch('/upload', { method: 'POST', body: formData });
                    const data = await res.json();
                    if (data.success) {
                        resultDiv.innerHTML = '✅ ' + data.message;
                        resultDiv.style.color = '#4CAF50';
                    } else {
                        resultDiv.innerHTML = '❌ ' + data.error;
                        resultDiv.style.color = '#c62828';
                    }
                } catch (err) {
                    resultDiv.innerHTML = '❌ Error de conexión';
                    resultDiv.style.color = '#c62828';
                }
            };
            
            document.getElementById('queryForm').onsubmit = async (e) => {
                e.preventDefault();
                const question = document.getElementById('question').value;
                if (!question) return;
                
                const resultDiv = document.getElementById('queryResult');
                resultDiv.textContent = '⏳ Buscando respuesta...';
                resultDiv.classList.remove('error');
                
                try {
                    const res = await fetch('/ask', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ question })
                    });
                    const data = await res.json();
                    if (data.success) {
                        resultDiv.innerHTML = '<strong>📝 Respuesta:</strong><br>' + data.answer;
                        resultDiv.classList.remove('error');
                    } else {
                        resultDiv.innerHTML = '❌ ' + data.error;
                        resultDiv.classList.add('error');
                    }
                } catch (err) {
                    resultDiv.innerHTML = '❌ Error de conexión';
                    resultDiv.classList.add('error');
                }
            };
        </script>
    </body>
    </html>
    '''

@app.route('/upload', methods=['POST'])
def upload_pdf():
    try:
        if 'file' not in request.files:
            return jsonify({'success': False, 'error': 'No file uploaded'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'success': False, 'error': 'No file selected'}), 400
        
        if not allowed_file(file.filename):
            return jsonify({'success': False, 'error': 'Only PDF files allowed'}), 400
        
        # Guardar temporalmente
        filename = secure_filename(file.filename)
        temp_path = os.path.join(UPLOAD_FOLDER, filename)
        file.save(temp_path)
        
        # Procesar PDF
        titulo = request.form.get('title', filename)
        conn = conectar_db()
        crear_tabla(conn)
        
        paginas = extraer_texto_pdf(temp_path)
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
        conn.close()
        
        # Limpiar archivo temporal
        os.remove(temp_path)
        
        return jsonify({'success': True, 'message': f'{total} chunks guardados de "{titulo}"'})
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/ask', methods=['POST'])
def ask_question():
    try:
        data = request.get_json()
        question = data.get('question', '')
        if not question:
            return jsonify({'success': False, 'error': 'No question provided'}), 400
        
        conn = conectar_db()
        answer = responder_con_ia(conn, question)
        conn.close()
        
        return jsonify({'success': True, 'answer': answer})
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

def main():
    # Obtener IP local
    import socket
    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)
    
    print("=" * 60)
    print("🚀 Servidor RAG iniciado!")
    print("=" * 60)
    print(f"📍 Acceso local: http://localhost:5000")
    print(f"🌐 Comparte con tus amigos: http://{local_ip}:5000")
    print("=" * 60)
    print("⚠️  Asegúrate de que tu firewall permita el puerto 5000")
    print("💡 En Arch: sudo firewall-cmd --add-port=5000/tcp")
    print("=" * 60)
    
    app.run(host='0.0.0.0', port=5000, debug=False)

if __name__ == "__main__":
    main()