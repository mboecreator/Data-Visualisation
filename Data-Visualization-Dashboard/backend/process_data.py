import pandas as pd
import numpy as np
from pathlib import Path

def load_data():
    """
    Load and combine all relevant data files
    """
    data_dir = Path(__file__).parent.parent / 'data'
    
    # Try different encodings and delimiters
    encodings = ['utf-8', 'latin1', 'iso-8859-1', 'cp1252']
    delimiters = [',', '\t', ';', '|']
    
    # Load course data
    course_data = None
    for encoding in encodings:
        for delimiter in delimiters:
            try:
                course_data = pd.read_csv(data_dir / 'course', encoding=encoding, delimiter=delimiter)
                print(f"Successfully loaded course data with {encoding} encoding and '{delimiter}' delimiter")
                break
            except (UnicodeDecodeError, pd.errors.ParserError):
                continue
        if course_data is not None:
            break
    
    if course_data is None:
        raise ValueError("Could not load course data with any encoding or delimiter")
    
    # Load enrollment data
    section_data = None
    for encoding in encodings:
        for delimiter in delimiters:
            try:
                section_data = pd.read_csv(data_dir / 'section', encoding=encoding, delimiter=delimiter)
                print(f"Successfully loaded section data with {encoding} encoding and '{delimiter}' delimiter")
                break
            except (UnicodeDecodeError, pd.errors.ParserError):
                continue
        if section_data is not None:
            break
    
    if section_data is None:
        raise ValueError("Could not load section data with any encoding or delimiter")
    
    # Load instructor data
    instructor_data = None
    for encoding in encodings:
        for delimiter in delimiters:
            try:
                instructor_data = pd.read_csv(data_dir / 'instructor', encoding=encoding, delimiter=delimiter)
                print(f"Successfully loaded instructor data with {encoding} encoding and '{delimiter}' delimiter")
                break
            except (UnicodeDecodeError, pd.errors.ParserError):
                continue
        if instructor_data is not None:
            break
    
    if instructor_data is None:
        raise ValueError("Could not load instructor data with any encoding or delimiter")
    
    # Load department data
    department_data = None
    for encoding in encodings:
        for delimiter in delimiters:
            try:
                department_data = pd.read_csv(data_dir / 'department', encoding=encoding, delimiter=delimiter)
                print(f"Successfully loaded department data with {encoding} encoding and '{delimiter}' delimiter")
                break
            except (UnicodeDecodeError, pd.errors.ParserError):
                continue
        if department_data is not None:
            break
    
    if department_data is None:
        raise ValueError("Could not load department data with any encoding or delimiter")
    
    return {
        'course': course_data,
        'section': section_data,
        'instructor': instructor_data,
        'department': department_data
    }

def process_enrollment_data(data):
    """
    Process and clean enrollment data
    """
    # Merge relevant datasets
    enrollment = data['section'].merge(
        data['course'],
        on='course_id',
        how='left'
    ).merge(
        data['instructor'],
        on='instructor_id',
        how='left'
    ).merge(
        data['department'],
        on='department_id',
        how='left'
    )
    
    # Calculate enrollment metrics
    enrollment['enrollment_rate'] = enrollment['enrolled'] / enrollment['capacity']
    
    return enrollment

def generate_summary_statistics(enrollment_data):
    """
    Generate summary statistics for the dashboard
    """
    summary = {
        'total_enrollments': enrollment_data['enrolled'].sum(),
        'average_class_size': enrollment_data['enrolled'].mean(),
        'department_enrollments': enrollment_data.groupby('department_name')['enrolled'].sum(),
        'instructor_workload': enrollment_data.groupby('instructor_name')['enrolled'].sum()
    }
    
    return summary

def main():
    """
    Main function to process all data
    """
    # Load data
    data = load_data()
    
    # Process enrollment data
    enrollment_data = process_enrollment_data(data)
    
    # Generate summary statistics
    summary_stats = generate_summary_statistics(enrollment_data)
    
    # Save processed data
    output_dir = Path(__file__).parent.parent / 'data' / 'processed'
    output_dir.mkdir(exist_ok=True)
    
    enrollment_data.to_csv(output_dir / 'processed_enrollment.csv', index=False)
    
    print("Data processing completed successfully!")

if __name__ == "__main__":
    main() 