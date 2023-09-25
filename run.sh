# Install dependencies
python3 -m venv env
source env/bin/activate
pip install PyQt5 pyinstaller

# Run the code
python time_progress.py

# Convert the Python file to a standalone executable
pyinstaller --onefile time_progress.py
