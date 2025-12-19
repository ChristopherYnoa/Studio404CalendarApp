"""
Configuration settings for the Calendar Processing Tool.
Loads sensitive data from environment variables.
"""
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Project root directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Credentials directory
CREDENTIALS_DIR = BASE_DIR / "credentials"

# Google API Scopes
CALENDAR_SCOPES = ['https://www.googleapis.com/auth/calendar']
SHEET_SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
#SCOPES = ['https://www.googleapis.com/auth/calendar']

# Token files
CALENDAR_TOKEN_FILE = str(BASE_DIR / 'token.json')
SHEETS_TOKEN_FILE = str(BASE_DIR / 'sheet_token.json')
CREDENTIALS_FILE = str(CREDENTIALS_DIR / 'credentials.json')

# Calendar IDs
PRIMARY_CALENDAR_ID = os.getenv('PRIMARY_CALENDAR_ID', 'primary')
SECOND_CALENDAR_ID = os.getenv('SECOND_CALENDAR_ID', '')

# Spreadsheet ID
SPREADSHEET_ID = os.getenv('SPREADSHEET_ID', '')

# Studio mapping
STUDIO_MAP = {
    "primary": os.getenv('STUDIO_A_NAME', 'Studio A'),
    SECOND_CALENDAR_ID: os.getenv('STUDIO_B_NAME', 'Studio B'),
}

# Engineer names for recognition
ENGINEER_NAMES = ['john', 'jaylun', 'aaron', 'chris']

# Validation
def validate_config():
    """Validate that required configuration is present."""
    errors = []
    
    if not SPREADSHEET_ID:
        errors.append("SPREADSHEET_ID not set in .env file")
    
    if not SECOND_CALENDAR_ID:
        errors.append("SECOND_CALENDAR_ID not set in .env file")
    
    if not os.path.exists(CREDENTIALS_FILE):
        errors.append(f"credentials.json not found at {CREDENTIALS_FILE}")
    
    if errors:
        raise ValueError(
            "Configuration errors:\n" + "\n".join(f"  - {e}" for e in errors)
        )

# Validate on import (optional - comment out if you want manual validation)
# validate_config()