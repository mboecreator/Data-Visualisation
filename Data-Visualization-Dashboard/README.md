# Data Visualization Dashboard

This project contains a comprehensive data visualization dashboard analyzing university enrollment data and student demographics using Python-based visualization tools.

## Project Structure

```
Data-Visualization-Dashboard/
│
├── data/                           # Directory containing datasets
│   ├── university_enrollment_data.csv
│   ├── student_demographics_data.csv
│   └── other_data_sources.xlsx
│
├── backend/                        # Server-side code and data preprocessing
│   ├── process_data.py            # Python script to clean and preprocess data
│   ├── database_connection.py     # Script for database connections
│   └── check_data.py              # Script to check data files and encodings
│
├── visualizations/                 # Python visualization scripts
│   ├── enrollment_dashboard.py    # Main dashboard visualization script
│   ├── student_demographics.py    # Student demographics visualization
│   └── app.py                     # Web-based dashboard using Streamlit
│
├── run_app.py                     # Script to run the Streamlit app
├── README.md                      # Project documentation
├── .gitignore                     # Git ignore file
└── LICENSE                        # Project license
```

## Data Sources

The project utilizes the following data sources:
- Course enrollment data
- Student demographics
- Department information
- Instructor data
- Section and meeting information

## Setup Instructions

1. Clone the repository
2. Install required dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Check data file encodings and delimiters (if you encounter issues):
   ```
   python backend/check_data.py
   ```
4. Run the data processing scripts:
   ```
   python backend/process_data.py
   python backend/database_connection.py
   ```
5. Launch the visualization dashboard:
   ```
   python run_app.py
   ```
   or directly with Streamlit:
   ```
   streamlit run visualizations/app.py
   ```

## Troubleshooting

### Data Loading Issues

If you encounter errors when loading data, try the following:

1. Run the data check script to diagnose issues:
   ```
   python backend/check_data.py
   ```

2. The data processing scripts have been updated to handle different encodings and delimiters, but if you still encounter issues, you can modify the encoding and delimiter lists in `process_data.py` and `database_connection.py`.

3. Common encodings to try:
   - utf-8
   - latin1
   - iso-8859-1
   - cp1252

4. Common delimiters to try:
   - comma (,)
   - tab (\t)
   - semicolon (;)
   - pipe (|)

### Other Issues

1. Make sure all dependencies are installed correctly
2. Check that the data files are in the correct location
3. Ensure you have sufficient permissions to read/write files

## Features

- Interactive enrollment trends visualization
- Student demographic analysis
- Department-wise enrollment patterns
- Course popularity metrics
- Instructor workload analysis

## Visualization Tools

This project uses the following Python libraries for visualization:
- Matplotlib: For static visualizations
- Seaborn: For statistical visualizations
- Plotly: For interactive visualizations
- Streamlit: For creating web-based dashboards

## Contributing

Please read the LICENSE file for details on our code of conduct and the process for submitting pull requests.

## License

This project is licensed under the MIT License - see the LICENSE file for details. 