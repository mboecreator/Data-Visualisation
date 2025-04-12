import os
from pathlib import Path
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class DatabaseConnection:
    def __init__(self):
        """
        Initialize database connection
        """
        self.connection_string = os.getenv('DATABASE_URL', 'sqlite:///data/university.db')
        self.engine = create_engine(self.connection_string)
    
    def load_data_from_csv(self, csv_path, table_name):
        """
        Load data from CSV file into database
        """
        # Try different encodings and delimiters
        encodings = ['utf-8', 'latin1', 'iso-8859-1', 'cp1252']
        delimiters = [',', '\t', ';', '|']
        
        for encoding in encodings:
            for delimiter in delimiters:
                try:
                    df = pd.read_csv(csv_path, encoding=encoding, delimiter=delimiter)
                    print(f"Successfully loaded {table_name} data with {encoding} encoding and '{delimiter}' delimiter")
                    df.to_sql(table_name, self.engine, if_exists='replace', index=False)
                    print(f"Data loaded into {table_name} successfully!")
                    return
                except (UnicodeDecodeError, pd.errors.ParserError):
                    continue
        
        raise ValueError(f"Could not load {table_name} data with any encoding or delimiter")
    
    def query_data(self, query):
        """
        Execute SQL query and return results as DataFrame
        """
        return pd.read_sql(query, self.engine)
    
    def get_enrollment_data(self):
        """
        Get processed enrollment data
        """
        query = """
        SELECT 
            c.course_name,
            d.department_name,
            i.instructor_name,
            s.enrolled,
            s.capacity,
            s.term
        FROM section s
        JOIN course c ON s.course_id = c.course_id
        JOIN department d ON c.department_id = d.department_id
        JOIN instructor i ON s.instructor_id = i.instructor_id
        """
        return self.query_data(query)

def main():
    """
    Main function to set up database and load initial data
    """
    db = DatabaseConnection()
    
    # Define data directory
    data_dir = Path(__file__).parent.parent / 'data'
    
    # Load initial data
    tables = {
        'course': 'course',
        'section': 'section',
        'instructor': 'instructor',
        'department': 'department'
    }
    
    for table_name, file_name in tables.items():
        file_path = data_dir / file_name
        if file_path.exists():
            db.load_data_from_csv(file_path, table_name)
    
    print("Database setup completed successfully!")

if __name__ == "__main__":
    main() 