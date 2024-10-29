from flask import Flask, request, render_template, send_file
import os
from werkzeug.utils import secure_filename
from src.main import main as compile_spreadsheets

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/'

# Crie a pasta de uploads se não existir
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_files():
    uploaded_files = request.files.getlist('files[]')
    print(f"Uploaded files: {[file.filename for file in uploaded_files]}")  # Debug

    if not uploaded_files:
        return "No files uploaded.", 400

    # Salvar os arquivos enviados
    for file in uploaded_files:
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        print(f"Saved file: {file_path}")  # Debug

    input_directory = app.config['UPLOAD_FOLDER']
    output_file = 'compiled_spreadsheet.xlsx'

    try:
        # Aqui estamos chamando a função main corretamente
        compile_spreadsheets(input_directory, output_file)
    except Exception as e:
        return str(e), 500

    # Limpar arquivos carregados
    for file in os.listdir(app.config['UPLOAD_FOLDER']):
        os.remove(os.path.join(app.config['UPLOAD_FOLDER'], file))

    return send_file(output_file, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)
