import os
import subprocess
import sys

# Delete token files
if os.path.exists("token.json"):
    os.remove("token.json")
if os.path.exists("sheet_token.json"):
    os.remove("sheet_token.json")

print("Installing required libraries...")
subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])

print("Running main program...")
subprocess.run(["python3", "main.py"])

print("Execution completed.")
