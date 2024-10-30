import os
import pandas as pd
from flask import Flask, request, render_template, redirect, url_for

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def load_spreadsheet(file_path):
    if file_path.endswith('.xlsx'):
        df = pd.read_excel(file_path)
    elif file_path.endswith('.xls'):
        df = pd.read_excel(file_path, engine='xlrd')
    elif file_path.endswith('.csv'):
        df = pd.read_csv(file_path)
    else:
        raise ValueError('Unsupported file format')
    return df

def compile_spreadsheets(directory_path, output_path):
    data_frames = []
    for filename in os.listdir(directory_path):
        file_path = os.path.join(directory_path, filename)
        if file_path.endswith('.xlsx') or file_path.endswith('.xls') or file_path.endswith('.csv'):
            print(f"Loading file: {file_path}")  # Debug
            df = load_spreadsheet(file_path)
            print(f"Loaded dataframe shape: {df.shape}")  # Debug
            data_frames.append(df)
    
    if not data_frames:
        raise ValueError('No spreadsheets loaded')

    compiled_df = pd.concat(data_frames, ignore_index=True)
    print(f"Compiled dataframe shape: {compiled_df.shape}")  # Debug
    
    if output_path.endswith('.xlsx'):
        compiled_df.to_excel(output_path, index=False)
    elif output_path.endswith('.csv'):
        compiled_df.to_csv(output_path, index=False)
    elif output_path.endswith('.xls'):
        compiled_df.to_excel(output_path, index=False)
    else:
        raise ValueError('Unsupported file format')
    print(f"Data compiled and saved to {output_path}")  # Debug

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        files = request.files.getlist('file')
        for file in files:
            if file:
                filename = file.filename
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(file_path)
                print(f"Saved file: {file_path}")  # Debug

        compile_spreadsheets(app.config['UPLOAD_FOLDER'], os.path.join(app.config['UPLOAD_FOLDER'], 'compiled_spreadsheet.xlsx'))
        return redirect(url_for('uploaded_file', filename='compiled_spreadsheet.xlsx'))
    return render_template('upload.html')

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return f"File {filename} uploaded and compiled successfully."

if __name__ == '__main__':
    app.run(debug=True)
