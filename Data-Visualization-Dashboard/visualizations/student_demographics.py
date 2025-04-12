import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import seaborn as sns
import matplotlib.pyplot as plt
from pathlib import Path
import sys

# Add parent directory to path to import backend modules
sys.path.append(str(Path(__file__).parent.parent))
from backend.process_data import load_data, process_enrollment_data

def create_demographics_visualizations(enrollment_data):
    """
    Create various visualizations for student demographics
    """
    # Create a directory for saving visualizations
    output_dir = Path(__file__).parent.parent / 'data' / 'visualizations'
    output_dir.mkdir(exist_ok=True)
    
    # 1. Enrollment by Term (Line Chart)
    term_enrollment = enrollment_data.groupby('term')['enrolled'].sum().reset_index()
    fig_term = px.line(
        term_enrollment,
        x='term',
        y='enrolled',
        title="Enrollment Trends by Term"
    )
    fig_term.write_html(output_dir / 'term_enrollment.html')
    
    # 2. Department-wise Enrollment (Bar Chart)
    dept_enrollment = enrollment_data.groupby('department_name')['enrolled'].sum().reset_index()
    dept_enrollment = dept_enrollment.sort_values('enrolled', ascending=False)
    fig_dept = px.bar(
        dept_enrollment,
        x='department_name',
        y='enrolled',
        title="Enrollment by Department"
    )
    fig_dept.write_html(output_dir / 'department_enrollment.html')
    
    # 3. Top Courses (Bar Chart)
    top_courses = enrollment_data.groupby('course_name')['enrolled'].sum().reset_index()
    top_courses = top_courses.sort_values('enrolled', ascending=False).head(10)
    fig_courses = px.bar(
        top_courses,
        x='course_name',
        y='enrolled',
        title="Top 10 Courses by Enrollment"
    )
    fig_courses.write_html(output_dir / 'top_courses.html')
    
    # 4. Instructor Workload (Bar Chart)
    instructor_workload = enrollment_data.groupby('instructor_name')['enrolled'].sum().reset_index()
    instructor_workload = instructor_workload.sort_values('enrolled', ascending=False).head(15)
    fig_instructor = px.bar(
        instructor_workload,
        x='instructor_name',
        y='enrolled',
        title="Top 15 Instructors by Student Count"
    )
    fig_instructor.write_html(output_dir / 'instructor_workload.html')
    
    # 5. Enrollment Rate Distribution (Histogram)
    fig_dist = px.histogram(
        enrollment_data,
        x='enrollment_rate',
        title="Distribution of Enrollment Rates",
        nbins=30
    )
    fig_dist.write_html(output_dir / 'enrollment_rate_distribution.html')
    
    # 6. Enrollment Rate by Department (Box Plot)
    fig_box = px.box(
        enrollment_data,
        x='department_name',
        y='enrollment_rate',
        title="Enrollment Rate Distribution by Department"
    )
    fig_box.write_html(output_dir / 'enrollment_rate_by_department.html')
    
    print(f"Visualizations saved to {output_dir}")

def main():
    """
    Main function to generate all visualizations
    """
    # Load and process data
    data = load_data()
    enrollment_data = process_enrollment_data(data)
    
    # Create visualizations
    create_demographics_visualizations(enrollment_data)
    
    print("All visualizations generated successfully!")

if __name__ == "__main__":
    main() 