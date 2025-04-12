import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import seaborn as sns
import matplotlib.pyplot as plt
from pathlib import Path
import sys

# Add parent directory to path to import backend modules
sys.path.append(str(Path(__file__).parent.parent))
from backend.process_data import load_data, process_enrollment_data, generate_summary_statistics
from backend.database_connection import DatabaseConnection

# Set page config
st.set_page_config(
    page_title="University Enrollment Dashboard",
    page_icon="📊",
    layout="wide"
)

# Title and description
st.title("University Enrollment Dashboard")
st.markdown("""
This dashboard provides insights into university enrollment data, including course popularity,
department-wise enrollment patterns, and instructor workload analysis.
""")

# Load data
@st.cache_data
def load_dashboard_data():
    data = load_data()
    enrollment_data = process_enrollment_data(data)
    summary_stats = generate_summary_statistics(enrollment_data)
    return enrollment_data, summary_stats

enrollment_data, summary_stats = load_dashboard_data()

# Sidebar filters
st.sidebar.header("Filters")
department_filter = st.sidebar.multiselect(
    "Select Departments",
    options=enrollment_data['department_name'].unique(),
    default=enrollment_data['department_name'].unique()
)

term_filter = st.sidebar.multiselect(
    "Select Terms",
    options=enrollment_data['term'].unique(),
    default=enrollment_data['term'].unique()
)

# Filter data based on sidebar selections
filtered_data = enrollment_data[
    (enrollment_data['department_name'].isin(department_filter)) &
    (enrollment_data['term'].isin(term_filter))
]

# Dashboard layout
col1, col2, col3 = st.columns(3)

# Key metrics
with col1:
    st.metric(
        "Total Enrollments",
        f"{filtered_data['enrolled'].sum():,}"
    )

with col2:
    st.metric(
        "Average Class Size",
        f"{filtered_data['enrolled'].mean():.1f}"
    )

with col3:
    st.metric(
        "Enrollment Rate",
        f"{(filtered_data['enrolled'].sum() / filtered_data['capacity'].sum() * 100):.1f}%"
    )

# Enrollment trends
st.subheader("Enrollment Trends")
fig_trends = px.line(
    filtered_data.groupby('term')['enrolled'].sum().reset_index(),
    x='term',
    y='enrolled',
    title="Enrollment Trends by Term"
)
st.plotly_chart(fig_trends, use_container_width=True)

# Department-wise enrollment
col1, col2 = st.columns(2)

with col1:
    st.subheader("Department-wise Enrollment")
    fig_dept = px.bar(
        filtered_data.groupby('department_name')['enrolled'].sum().reset_index(),
        x='department_name',
        y='enrolled',
        title="Enrollment by Department"
    )
    st.plotly_chart(fig_dept, use_container_width=True)

with col2:
    st.subheader("Top Courses by Enrollment")
    top_courses = filtered_data.groupby('course_name')['enrolled'].sum().reset_index()
    top_courses = top_courses.sort_values('enrolled', ascending=False).head(10)
    fig_courses = px.bar(
        top_courses,
        x='course_name',
        y='enrolled',
        title="Top 10 Courses by Enrollment"
    )
    st.plotly_chart(fig_courses, use_container_width=True)

# Instructor workload
st.subheader("Instructor Workload Analysis")
instructor_workload = filtered_data.groupby('instructor_name')['enrolled'].sum().reset_index()
instructor_workload = instructor_workload.sort_values('enrolled', ascending=False).head(15)
fig_instructor = px.bar(
    instructor_workload,
    x='instructor_name',
    y='enrolled',
    title="Top 15 Instructors by Student Count"
)
st.plotly_chart(fig_instructor, use_container_width=True)

# Enrollment rate distribution
st.subheader("Enrollment Rate Distribution")
fig_dist = px.histogram(
    filtered_data,
    x='enrollment_rate',
    title="Distribution of Enrollment Rates",
    nbins=30
)
st.plotly_chart(fig_dist, use_container_width=True)

# Data table
st.subheader("Detailed Enrollment Data")
st.dataframe(filtered_data) 