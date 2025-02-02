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
SCOPES = ['https://www.googleapis.com/auth/calendar']

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

def parse_date(date_string):
    """Parses a date string into a datetime object."""
    return datetime.strptime(date_string, '%Y-%m-%d')

def calculate_end_date(start_date, end_date=None):
    """
    Determines the end date for the date range.
    If end_date is None, sets it to the last day of the start_date's month.
    """
    if not end_date:
        _, last_day = calendar.monthrange(start_date.year, start_date.month)
        return datetime(start_date.year, start_date.month, last_day, 23, 59, 59)
    else:
        parsed_end_date = parse_date(end_date)
        return datetime(parsed_end_date.year, parsed_end_date.month, parsed_end_date.day, 23, 59, 59)

def format_dates_for_api(start_date, end_date):
    """Formats the start and end dates as ISO 8601 strings for the API."""
    return start_date.isoformat() + 'Z', end_date.isoformat() + 'Z'

def fetch_events_from_service(service, time_min, time_max):
    """
    Fetches events from the calendar service for the specified time range.
    Handles API errors gracefully.
    """
    try:
        events_result = service.events().list(
            calendarId='primary',
            timeMin=time_min,
            timeMax=time_max,
            singleEvents=True,
            orderBy='startTime'
        ).execute()
        return events_result.get('items', [])
    except HttpError as error:
        print(f"An error occurred: {error}")
        return []

def format_events(events):
    """Formats the raw event data into a simplified structure."""
    if not events:
        print('No events found.')
        return []
    
    return [
        {
            'start': event['start'].get('dateTime', event['start'].get('date')),
            'summary': event['summary'],
            'description': event.get('description', None)
        }
        for event in events
    ]

def get_calendar_data(start_date, end_date=None):
    """
    Retrieves calendar events within the specified date range.
    If end_date is None, fetches all events for the month of start_date.
    """
    # Parse and calculate dates
    start_date = parse_date(start_date)
    end_date = calculate_end_date(start_date, end_date)

    # Format dates for API
    time_min, time_max = format_dates_for_api(start_date, end_date)

    # Get calendar service
    service = get_service()

    # Fetch events
    events = fetch_events_from_service(service, time_min, time_max)

    # Format and return events
    print("Fetched events:", format_events(events))

    return format_events(events)

def main():
  
    # Example: User inputs
    start_date = input("Enter start date (YYYY-MM-DD): ")
    end_date = input("Enter end date (YYYY-MM-DD) [leave blank for full month]: ")

    # Fetch and display events
    events = get_calendar_data(start_date, end_date if end_date.strip() else None)

# Main execution
if __name__ == '__main__':
    main()
