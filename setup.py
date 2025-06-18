import subprocess
import os
import sys

def setup_project():
    """
    Set up the MedAssist project by installing dependencies and creating necessary files.
    """
    print("Setting up MedAssist project...")
    
    # Check if Python is installed
    try:
        python_version = subprocess.check_output([sys.executable, "--version"]).decode().strip()
        print(f"Using {python_version}")
    except Exception as e:
        print(f"Error checking Python version: {e}")
        return
    
    # Install dependencies
    print("\nInstalling dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("Dependencies installed successfully!")
    except Exception as e:
        print(f"Error installing dependencies: {e}")
        return
    
    # Create .env file if it doesn't exist
    if not os.path.exists(".env"):
        print("\nCreating .env file...")
        try:
            with open(".env.example", "r") as example_file:
                example_content = example_file.read()
            
            with open(".env", "w") as env_file:
                env_file.write(example_content)
            
            print(".env file created. You can add your HuggingFace API token for higher rate limits, but it's optional.")
        except Exception as e:
            print(f"Error creating .env file: {e}")
    
    # Create data directory if it doesn't exist
    data_dir = os.path.join(os.path.dirname(__file__), "data")
    if not os.path.exists(data_dir):
        print("\nCreating data directory...")
        try:
            os.makedirs(data_dir)
            print("Data directory created.")
        except Exception as e:
            print(f"Error creating data directory: {e}")
    
    print("\nSetup complete! You can now run the application with:")
    print("streamlit run app.py")

if __name__ == "__main__":
    setup_project()