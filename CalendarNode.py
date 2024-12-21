from datetime import datetime, timedelta
import calendar
import datetime as dt
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
# Constants
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

def get_service():
    """Authenticate and return a Google Calendar API service instance."""
    creds = None

    # Check if token.json exists
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)

    # If token.json is missing or invalid, prompt the user for authorization
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES
            )
            creds = flow.run_local_server(port=0)

        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    # Build the Google Calendar API service
    service = build('calendar', 'v3', credentials=creds)
    return service


def get_calendar_data(start_date, end_date=None):
    """
    Retrieves calendar events within the specified date range.
    If end_date is None, fetches all events for the month of start_date.
    """
    # Parse start_date
    start_date = datetime.strptime(start_date, '%Y-%m-%d')
    
    # Determine end_date if not provided
    if not end_date:
        _, last_day = calendar.monthrange(start_date.year, start_date.month)
        end_date = datetime(start_date.year, start_date.month, last_day, 23, 59, 59)
    else:
        end_date = datetime.strptime(end_date, '%Y-%m-%d')
        end_date = datetime(end_date.year, end_date.month, end_date.day, 23, 59, 59)

    # Format dates as ISO 8601 strings
    time_min = start_date.isoformat() + 'Z'
    time_max = end_date.isoformat() + 'Z'

    # Get calendar service
    service = get_service()

    # Retrieve events
    events_result = service.events().list(
        calendarId='primary',
        timeMin=time_min,
        timeMax=time_max,
        singleEvents=True,
        orderBy='startTime'
    ).execute()
    
    events = events_result.get('items', [])
    
    # Return formatted events
    if not events:
        print('No events found.')
        return []
    
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        print(f"{start}: {event['summary']}")
    return events

def main():
  
    # Example: User inputs
    start_date = input("Enter start date (YYYY-MM-DD): ")
    end_date = input("Enter end date (YYYY-MM-DD) [leave blank for full month]: ")

    # Fetch and display events
    events = get_calendar_data(start_date, end_date if end_date.strip() else None)

# Main execution
if __name__ == '__main__':
    main()
