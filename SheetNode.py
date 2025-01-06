# import gspread
# from google.oauth2.service_account import Credentials

# scopes = ["https://www.googleapis.com/auth/spreadsheets"]
# creds = Credentials.from_service_account_file("credentials-sheets.json", scopes=scopes)
# client = gspread.authorize(creds)

# #unique identification for the sheet connected to the API
# sheet_id = "19GpFb5B8SaVqjgqkBGrytiCzwU6D1PIiqnRrw_Qrmcg"
# workbook = client.open_by_key(sheet_id)

# values_list = workbook.sheet1.row_values(1)

# print(values_list)

# example = [
#     ["Date", "Studio", "Artist Name", "Engineer?", "Engineer Name", "Referral", "Hours", "Price", "Paid?"],
#     ["2024-12-21", "Studio B", "John Doe", "Y", "John", "John", "3", "150", "Y"]
# ]

# values = [
#     ["Name", "Price", "Quantity"],
#     ["Basketball", 29.99, 1],
#     ["Jeans", 39.99, 4],
#     ["Soap", 7.99, 3],
# ]

# worksheet_list = map(lambda x: x.title, workbook.worksheets())
# new_worksheet_name = "Values"

# if new_worksheet_name in worksheet_list:
#     sheet = workbook.worksheet(new_worksheet_name)
# else:
#     sheet = workbook.add_worksheet(new_worksheet_name, rows=10, cols=10)

# sheet.clear()

# sheet.update(f"A1:C{len(values)}", values)

# sheet.update_cell(len(values) + 1, 2, "=sum(B2:B4)")
# sheet.update_cell(len(values) + 1, 3, "=sum(C2:C4)")

# sheet.format("A1:C1", {"textFormat": {"bold": True}})




import os
import json
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from FormatterNode import FormatterNode  # Assuming FormatterNode is implemented.
from CalendarNode import get_calendar_data

# Constants
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
TOKEN_FILE = 'sheet_token.json'
CREDENTIALS_FILE = 'credentials.json'


def get_sheets_service():
    """Authenticate and return a Google Sheets API service instance."""
    creds = None

    # Check if token exists and is valid
    if os.path.exists(TOKEN_FILE):
        if os.stat(TOKEN_FILE).st_size > 0:  # Ensure the token file is non-empty
            try:
                creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)
            except Exception as e:
                print(f"Error loading {TOKEN_FILE}: {e}")
                os.remove(TOKEN_FILE)  # Delete the invalid file
        else:
            print(f"{TOKEN_FILE} is empty. Deleting and re-authenticating.")
            os.remove(TOKEN_FILE)

    # If credentials are not available or invalid, authenticate
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
            creds = flow.run_local_server(port=0)

        # Save the credentials for the next run
        with open(TOKEN_FILE, 'w') as token:
            token.write(creds.to_json())

    return build('sheets', 'v4', credentials=creds)


def create_sheet_if_not_exists(service, spreadsheet_id, title):
    """Create a sheet with the given title if it does not already exist."""
    try:
        # Get existing sheet names
        response = service.spreadsheets().get(spreadsheetId=spreadsheet_id).execute()
        existing_sheets = [sheet['properties']['title'] for sheet in response['sheets']]
        
        if title in existing_sheets:
            print(f"Sheet '{title}' already exists.")
            return True

        # Add new sheet
        body = {
            "requests": [
                {
                    "addSheet": {
                        "properties": {
                            "title": title
                        }
                    }
                }
            ]
        }
        service.spreadsheets().batchUpdate(spreadsheetId=spreadsheet_id, body=body).execute()
        print(f"Sheet '{title}' created successfully.")
        return True
    except HttpError as error:
        print(f"An error occurred: {error}")
        return False

def write_data_to_sheet(service, spreadsheet_id, sheet_name, data):
    """Write data to the specified sheet."""
    try:
        range_name = f"{sheet_name}!A1"
        body = {
            "values": data
        }
        service.spreadsheets().values().update(
            spreadsheetId=spreadsheet_id,
            range=range_name,
            valueInputOption="RAW",
            body=body
        ).execute()
        print(f"Data written successfully to sheet '{sheet_name}'.")
    except HttpError as error:
        print(f"An error occurred: {error}")

def main():

    start_date = input("Enter start date (YYYY-MM-DD): ")
    end_date = input("Enter end date (YYYY-MM-DD) [leave blank for full month]: ")

    print(start_date)
    print(end_date)

    # Example spreadsheet ID and time frame
    spreadsheet_id = "19GpFb5B8SaVqjgqkBGrytiCzwU6D1PIiqnRrw_Qrmcg"
    # time_frame = input("Enter the time frame for the new sheet (e.g., '2024-12'): ")

    formatter = FormatterNode()
    # Mocked FormatterNode output (replace with actual function call)
    formatted_data = formatter.format_data(get_calendar_data(start_date, end_date))
    
    
    [
        # ["Date", "Studio", "Artist Name", "Engineer?", "Engineer Name", "Referral", "Hours", "Price", "Paid?"],
        # ["2024-12-21", "Studio B", "John Doe", "Y", "John", "John", "3", "150", "Y"]
    ]

    # Get Sheets service
    service = get_sheets_service()


    print(formatted_data)
    # Create the sheet if it doesn't exist
    if create_sheet_if_not_exists(service, spreadsheet_id, end_date if end_date.strip() else start_date):
        # Write data to the sheet
        write_data_to_sheet(service, spreadsheet_id, end_date if end_date.strip() else start_date, formatted_data)

if __name__ == '__main__':
    main()
