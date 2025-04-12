import subprocess
import sys
import os
from pathlib import Path

def run_streamlit_app():
    """
    Run the Streamlit app with proper error handling
    """
    # Get the path to the app.py file
    app_path = Path(__file__).parent / 'visualizations' / 'app.py'
    
    if not app_path.exists():
        print(f"Error: App file not found at {app_path}")
        return
    
    print(f"Running Streamlit app from {app_path}")
    print("If you encounter encoding errors, try running the check_data.py script first:")
    print("python backend/check_data.py")
    
    try:
        # Run the Streamlit app
        subprocess.run(['streamlit', 'run', str(app_path)], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error running Streamlit app: {e}")
        print("\nTroubleshooting tips:")
        print("1. Make sure all dependencies are installed: pip install -r requirements.txt")
        print("2. Check data file encodings: python backend/check_data.py")
        print("3. Try running the data processing script first: python backend/process_data.py")
    except Exception as e:
        print(f"Unexpected error: {e}")

if __name__ == "__main__":
    run_streamlit_app() 