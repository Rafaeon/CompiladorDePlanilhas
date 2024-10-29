import os
import pandas as pd

def load_spreadsheet(file_path):
    if file_path.endswith('.xlsx'):
        df = pd.read_excel(file_path)
    elif file_path.endswith('.csv'):
        df = pd.read_csv(file_path)
    else:
        raise ValueError('Unsupported file format')
    return df

def compile_spreadsheets(directory_path, output_path):
    data_frames = []
    for filename in os.listdir(directory_path):
        file_path = os.path.join(directory_path, filename)
        if file_path.endswith('.xlsx') or file_path.endswith('.csv'):
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
    else:
        raise ValueError('Unsupported file format')
    print(f"Data compiled and saved to {output_path}")  # Debug

def main(input_directory, output_file):
    compile_spreadsheets(input_directory, output_file)
