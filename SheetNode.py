import os
import json
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from datetime import datetime

# Constants
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
TOKEN_FILE = 'sheet_token.json'
CREDENTIALS_FILE = 'credentials.json'

def get_sheets_service():
    """
    Authenticate and return a Google Sheets API service instance.
    """
    creds = None
    
    # Check if token.json exists
    if os.path.exists(TOKEN_FILE):
        creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)
    
    # If token.json is missing or invalid, prompt the user for authorization
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                CREDENTIALS_FILE, SCOPES
            )
            creds = flow.run_local_server(port=0)
        
        # Save the credentials for the next run
        with open(TOKEN_FILE, 'w') as token:
            token.write(creds.to_json())
   
    # Build the Google Sheets API service
    service = build('sheets', 'v4', credentials=creds)
    return service

def create_sheet_if_not_exists(service, spreadsheet_id, sheet_name):
    """
    Check if a sheet with the given name exists in the spreadsheet.
    If not, create it.
    
    Args:
        service: Google Sheets API service instance
        spreadsheet_id (str): ID of the spreadsheet
        sheet_name (str): Name of the sheet to check/create
        
    Returns:
        bool: True if sheet exists or was created successfully, False otherwise
    """
    try:
        # Ensure sheet_name is not None
        if sheet_name is None:
            sheet_name = "Sheet_" + datetime.now().strftime("%Y%m%d%H%M%S")
        
        # Get spreadsheet metadata
        sheets_metadata = service.spreadsheets().get(spreadsheetId=spreadsheet_id).execute()
        sheets = sheets_metadata.get('sheets', '')
        
        # Check if sheet exists
        sheet_exists = False
        for sheet in sheets:
            if sheet['properties']['title'] == sheet_name:
                sheet_exists = True
                break
        
        # Create sheet if it doesn't exist
        if not sheet_exists:
            request_body = {
                'requests': [{
                    'addSheet': {
                        'properties': {
                            'title': sheet_name
                        }
                    }
                }]
            }
            service.spreadsheets().batchUpdate(
                spreadsheetId=spreadsheet_id,
                body=request_body
            ).execute()
            print(f"Sheet '{sheet_name}' created.")
        else:
            print(f"Sheet '{sheet_name}' already exists.")
        
        return True
    except HttpError as error:
        print(f"An error occurred: {error}")
        return False

def write_data_to_sheet(service, spreadsheet_id, sheet_name, data):
    """
    Write data to a Google Sheet.
    
    Args:
        service: Google Sheets API service instance
        spreadsheet_id (str): ID of the spreadsheet
        sheet_name (str): Name of the sheet to write to
        data (list): List of lists containing the formatted data with headers
        
    Returns:
        bool: True if write was successful, False otherwise
    """
    try:
        # Ensure sheet_name is not None
        if sheet_name is None:
            sheet_name = "Sheet_" + datetime.now().strftime("%Y%m%d%H%M%S")
        
        # Clear existing data in the sheet
        clear_range = f"{sheet_name}!A1:Z1000"
        service.spreadsheets().values().clear(
            spreadsheetId=spreadsheet_id,
            range=clear_range,
            body={}
        ).execute()
        
        # Write new data - assuming data is already in the correct format from FormatterNode
        range_name = f"{sheet_name}!A1"
        body = {
            'values': data
        }
        
        # Debug output
        print(f"Writing data to sheet: {sheet_name}")
        print(f"Data sample (first row): {data[0] if data else 'No data'}")
        
        result = service.spreadsheets().values().update(
            spreadsheetId=spreadsheet_id,
            range=range_name,
            valueInputOption='RAW',
            body=body
        ).execute()
        
        print(f"Data written to sheet '{sheet_name}'. Updated {result.get('updatedCells')} cells.")
        return True
    except HttpError as error:
        print(f"An error occurred: {error}")
        return False

def main():
    from FormatterNode import FormatterNode
    from CalendarNode import get_calendar_data
    
    start_date = input("Enter start date (YYYY-MM-DD): ")
    end_date = input("Enter end date (YYYY-MM-DD) [leave blank for full month]: ")
    end_date = end_date if end_date.strip() else None
    
    print(f"Fetching data from: {start_date} to {end_date if end_date else 'end of month'}")
    
    # Example spreadsheet ID
    spreadsheet_id = "19GpFb5B8SaVqjgqkBGrytiCzwU6D1PIiqnRrw_Qrmcg"
    
    # Get raw data
    raw_data = get_calendar_data(start_date, end_date)
    
    # Format data
    formatter = FormatterNode()
    formatted_data = formatter.format_data(raw_data)
    
    # Get Sheets service
    service = get_sheets_service()
    
    # Generate sheet name
    sheet_name = f"{start_date}_{end_date}_combined" if end_date else f"{start_date}_EOM_combined"
    
    # Create the sheet if it doesn't exist
    if create_sheet_if_not_exists(service, spreadsheet_id, sheet_name):
        # Write data to the sheet
        write_data_to_sheet(service, spreadsheet_id, sheet_name, formatted_data)

if __name__ == '__main__':
    main()

