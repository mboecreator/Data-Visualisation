import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path
import sys

# Add parent directory to path to import backend modules
sys.path.append(str(Path(__file__).parent.parent))
from backend.process_data import load_data, process_enrollment_data

def create_enrollment_dashboard(enrollment_data):
    """
    Create a comprehensive enrollment dashboard
    """
    # Create a directory for saving visualizations
    output_dir = Path(__file__).parent.parent / 'data' / 'visualizations'
    output_dir.mkdir(exist_ok=True)
    
    # Create a dashboard layout using Plotly
    fig = go.Figure()
    
    # Add enrollment trends
    term_enrollment = enrollment_data.groupby('term')['enrolled'].sum().reset_index()
    fig.add_trace(
        go.Scatter(
            x=term_enrollment['term'],
            y=term_enrollment['enrolled'],
            mode='lines+markers',
            name='Enrollment Trends'
        )
    )
    
    # Add department-wise enrollment
    dept_enrollment = enrollment_data.groupby('department_name')['enrolled'].sum().reset_index()
    dept_enrollment = dept_enrollment.sort_values('enrolled', ascending=False)
    
    fig.add_trace(
        go.Bar(
            x=dept_enrollment['department_name'],
            y=dept_enrollment['enrolled'],
            name='Department Enrollment'
        )
    )
    
    # Update layout
    fig.update_layout(
        title="University Enrollment Dashboard",
        xaxis_title="Term / Department",
        yaxis_title="Number of Students",
        barmode='group',
        height=800
    )
    
    # Save the dashboard
    fig.write_html(output_dir / 'enrollment_dashboard.html')
    
    # Create a summary report
    summary = {
        'total_enrollments': enrollment_data['enrolled'].sum(),
        'average_class_size': enrollment_data['enrolled'].mean(),
        'enrollment_rate': (enrollment_data['enrolled'].sum() / enrollment_data['capacity'].sum() * 100),
        'top_department': dept_enrollment.iloc[0]['department_name'],
        'top_department_enrollment': dept_enrollment.iloc[0]['enrolled']
    }
    
    # Save summary to a text file
    with open(output_dir / 'enrollment_summary.txt', 'w') as f:
        f.write("Enrollment Summary\n")
        f.write("=================\n\n")
        f.write(f"Total Enrollments: {summary['total_enrollments']:,}\n")
        f.write(f"Average Class Size: {summary['average_class_size']:.1f}\n")
        f.write(f"Overall Enrollment Rate: {summary['enrollment_rate']:.1f}%\n")
        f.write(f"Top Department: {summary['top_department']}\n")
        f.write(f"Top Department Enrollment: {summary['top_department_enrollment']:,}\n")
    
    print(f"Dashboard and summary saved to {output_dir}")

def main():
    """
    Main function to generate the enrollment dashboard
    """
    # Load and process data
    data = load_data()
    enrollment_data = process_enrollment_data(data)
    
    # Create dashboard
    create_enrollment_dashboard(enrollment_data)
    
    print("Enrollment dashboard generated successfully!")

if __name__ == "__main__":
    main() 