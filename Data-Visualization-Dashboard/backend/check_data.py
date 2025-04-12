import os
from pathlib import Path
import pandas as pd
import chardet

def detect_file_encoding(file_path):
    """
    Detect the encoding of a file
    """
    with open(file_path, 'rb') as file:
        raw_data = file.read()
        result = chardet.detect(raw_data)
        return result['encoding']

def check_data_files():
    """
    Check all data files and their encodings
    """
    data_dir = Path(__file__).parent.parent / 'data'
    
    if not data_dir.exists():
        print(f"Data directory not found: {data_dir}")
        return
    
    print(f"Checking data files in: {data_dir}")
    print("-" * 50)
    
    for file_path in data_dir.glob('*'):
        if file_path.is_file():
            print(f"File: {file_path.name}")
            
            # Detect encoding
            try:
                encoding = detect_file_encoding(file_path)
                print(f"  Detected encoding: {encoding}")
            except Exception as e:
                print(f"  Error detecting encoding: {e}")
            
            # Try to read with different encodings and delimiters
            encodings = ['utf-8', 'latin1', 'iso-8859-1', 'cp1252']
            delimiters = [',', '\t', ';', '|']
            
            for encoding in encodings:
                for delimiter in delimiters:
                    try:
                        df = pd.read_csv(file_path, encoding=encoding, delimiter=delimiter)
                        print(f"  Successfully read with {encoding} encoding and '{delimiter}' delimiter")
                        print(f"  Shape: {df.shape}")
                        print(f"  Columns: {df.columns.tolist()}")
                        print(f"  First few rows:")
                        print(df.head(2))
                        print("-" * 50)
                        break
                    except (UnicodeDecodeError, pd.errors.ParserError):
                        print(f"  Failed to read with {encoding} encoding and '{delimiter}' delimiter")
                    except Exception as e:
                        print(f"  Error reading with {encoding} encoding and '{delimiter}' delimiter: {e}")
                else:
                    continue
                break

if __name__ == "__main__":
    check_data_files() 