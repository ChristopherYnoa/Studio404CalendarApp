# from datetime import datetime, timedelta
# import calendar
# import datetime as dt
# import os.path

# from google.auth.transport.requests import Request
# from google.oauth2.credentials import Credentials
# from google_auth_oauthlib.flow import InstalledAppFlow
# from googleapiclient.discovery import build
# from googleapiclient.errors import HttpError
# # Constants
# SCOPES = ['https://www.googleapis.com/auth/calendar']

# def get_service():
#     """Authenticate and return a Google Calendar API service instance."""
#     creds = None

#     # Check if token.json exists
#     if os.path.exists('token.json'):
#         creds = Credentials.from_authorized_user_file('token.json', SCOPES)

#     # If token.json is missing or invalid, prompt the user for authorization
#     if not creds or not creds.valid:
#         if creds and creds.expired and creds.refresh_token:
#             creds.refresh(Request())
#         else:
#             flow = InstalledAppFlow.from_client_secrets_file(
#                 'credentials.json', SCOPES
#             )
#             creds = flow.run_local_server(port=0)

#         # Save the credentials for the next run
#         with open('token.json', 'w') as token:
#             token.write(creds.to_json())

#     # Build the Google Calendar API service
#     service = build('calendar', 'v3', credentials=creds)
#     return service

# def parse_date(date_string):
#     """Parses a date string into a datetime object."""
#     return datetime.strptime(date_string, '%Y-%m-%d')

# def calculate_end_date(start_date, end_date=None):
#     """
#     Determines the end date for the date range.
#     If end_date is None, sets it to the last day of the start_date's month.
#     """
#     if not end_date:
#         _, last_day = calendar.monthrange(start_date.year, start_date.month)
#         return datetime(start_date.year, start_date.month, last_day, 23, 59, 59)
#     else:
#         parsed_end_date = parse_date(end_date)
#         return datetime(parsed_end_date.year, parsed_end_date.month, parsed_end_date.day, 23, 59, 59)

# def format_dates_for_api(start_date, end_date):
#     """Formats the start and end dates as ISO 8601 strings for the API."""
#     return start_date.isoformat() + 'Z', end_date.isoformat() + 'Z'

# def fetch_events_from_service(service, time_min, time_max):
#     """
#     Fetches events from the calendar service for the specified time range.
#     Handles API errors gracefully.
#     """
#     try:
#         events_result = service.events().list(
#             calendarId='primary',
#             timeMin=time_min,
#             timeMax=time_max,
#             singleEvents=True,
#             orderBy='startTime'
#         ).execute()
#         return events_result.get('items', [])
#     except HttpError as error:
#         print(f"An error occurred: {error}")
#         return []

# def format_events(events):
#     """Formats the raw event data into a simplified structure."""
#     if not events:
#         print('No events found.')
#         return []
    
#     formatted_events = []
    
#     for event in events:
#         # Extract start and end times
#         start = event['start'].get('dateTime', event['start'].get('date'))
#         end = event['end'].get('dateTime', event['end'].get('date'))  # Added handling for end time
        
#         formatted_event = {
#             'start': start,
#             'end': end,  # Include end time in the formatted event
#             'summary': event.get('summary'),
#             'description': event.get('description', None)
#         }
        
#         formatted_events.append(formatted_event)
    
#     return formatted_events


# def get_calendar_data(start_date, end_date=None):
#     """
#     Retrieves calendar events within the specified date range.
#     If end_date is None, fetches all events for the month of start_date.
#     """
#     # Parse and calculate dates
#     start_date = parse_date(start_date)
#     end_date = calculate_end_date(start_date, end_date)

#     # Format dates for API
#     time_min, time_max = format_dates_for_api(start_date, end_date)

#     # Get calendar service
#     service = get_service()

#     # Fetch events
#     events = fetch_events_from_service(service, time_min, time_max)

#     # Format and return events
#     print("Fetched events:", format_events(events))

#     return format_events(events)





# def main():

 
#     # Example: User inputs
#     start_date = input("Enter start date (YYYY-MM-DD): ")
#     end_date = input("Enter end date (YYYY-MM-DD) [leave blank for full month]: ")

#     # Fetch and display events
#     events = get_calendar_data(start_date, end_date if end_date.strip() else None)





# # Main execution
# if __name__ == '__main__':
#     main()


# # from datetime import datetime, timedelta
# # import calendar
# # import datetime as dt
# # import os.path

# # from google.auth.transport.requests import Request
# # from google.oauth2.credentials import Credentials
# # from google_auth_oauthlib.flow import InstalledAppFlow
# # from googleapiclient.discovery import build
# # from googleapiclient.errors import HttpError

# # # Constants
# # SCOPES = ['https://www.googleapis.com/auth/calendar']

# # def get_service():
# #     """Authenticate and return a Google Calendar API service instance."""
# #     creds = None

# #     # Check if token.json exists
# #     if os.path.exists('token.json'):
# #         creds = Credentials.from_authorized_user_file('token.json', SCOPES)

# #     # If token.json is missing or invalid, prompt the user for authorization
# #     if not creds or not creds.valid:
# #         if creds and creds.expired and creds.refresh_token:
# #             creds.refresh(Request())
# #         else:
# #             flow = InstalledAppFlow.from_client_secrets_file(
# #                 'credentials.json', SCOPES
# #             )
# #             creds = flow.run_local_server(port=0)

# #         # Save the credentials for the next run
# #         with open('token.json', 'w') as token:
# #             token.write(creds.to_json())

# #     # Build the Google Calendar API service
# #     service = build('calendar', 'v3', credentials=creds)
# #     return service

# # def parse_date(date_string):
# #     """Parses a date string into a datetime object."""
# #     return datetime.strptime(date_string, '%Y-%m-%d')

# # def calculate_end_date(start_date, end_date=None):
# #     """
# #     Determines the end date for the date range.
# #     If end_date is None, sets it to the last day of the start_date's month.
# #     """
# #     if not end_date:
# #         _, last_day = calendar.monthrange(start_date.year, start_date.month)
# #         return datetime(start_date.year, start_date.month, last_day, 23, 59, 59)
# #     else:
# #         parsed_end_date = parse_date(end_date)
# #         return datetime(parsed_end_date.year, parsed_end_date.month, parsed_end_date.day, 23, 59, 59)

# # def format_dates_for_api(start_date, end_date):
# #     """Formats the start and end dates as ISO 8601 strings for the API."""
# #     return start_date.isoformat() + 'Z', end_date.isoformat() + 'Z'

# # def fetch_events_from_service(service, calendar_id, time_min, time_max):
# #     """
# #     Fetches events from the calendar service for the specified time range.
# #     Handles API errors gracefully.
# #     """
# #     try:
# #         events_result = service.events().list(
# #             calendarId=calendar_id,
# #             timeMin=time_min,
# #             timeMax=time_max,
# #             singleEvents=True,
# #             orderBy='startTime'
# #         ).execute()
# #         return events_result.get('items', [])
# #     except HttpError as error:
# #         print(f"An error occurred while fetching events from {calendar_id}: {error}")
# #         return []

# # def format_events(events):
# #     """Formats the raw event data into a simplified structure."""
# #     formatted_events = []

# #     for event in events:
# #         # Extract start and end times
# #         start = event['start'].get('dateTime', event['start'].get('date'))
# #         end = event['end'].get('dateTime', event['end'].get('date'))  # Added handling for end time
        
# #         formatted_event = {
# #             'start': start,
# #             'end': end,  # Include end time in the formatted event
# #             'summary': event.get('summary'),
# #             'description': event.get('description', None)
# #         }
        
# #         formatted_events.append(formatted_event)
    
# #     return formatted_events

# # def get_calendar_data(calendar_ids, start_date, end_date=None):
# #     """
# #     Retrieves calendar events from multiple calendars within the specified date range.
# #     If end_date is None, fetches all events for the month of start_date.
    
# #     Args:
# #         calendar_ids (list): List of Google Calendar IDs.
# #         start_date (str): Start date in YYYY-MM-DD format.
# #         end_date (str, optional): End date in YYYY-MM-DD format.
    
# #     Returns:
# #         list: Combined and formatted events from all specified calendars.
# #     """
# #     # Parse and calculate dates
# #     start_date = parse_date(start_date)
# #     end_date = calculate_end_date(start_date, end_date)

# #     # Format dates for API
# #     time_min, time_max = format_dates_for_api(start_date, end_date)

# #     # Get calendar service
# #     service = get_service()

# #     # Fetch and combine events from all calendars
# #     all_events = []
# #     for calendar_id in calendar_ids:
# #         print(f"Fetching events from calendar: {calendar_id}")
# #         events = fetch_events_from_service(service, calendar_id, time_min, time_max)
# #         all_events.extend(events)  # Add fetched events to the combined list

# #     # Format and return combined events
# #     formatted_events = format_events(all_events)
# #     print("Fetched events:", formatted_events)
# #     return formatted_events

# # def main():
# #     # List of Google Calendar IDs (Replace these with actual calendar IDs)
# #     CALENDAR_IDS = [
# #         "your_calendar_id_1@group.calendar.google.com",
# #         "your_calendar_id_2@group.calendar.google.com"
# #     ]

# #     # Example: User inputs
# #     start_date = input("Enter start date (YYYY-MM-DD): ")
# #     end_date = input("Enter end date (YYYY-MM-DD) [leave blank for full month]: ")

# #     # Fetch and display events from both calendars
# #     events = get_calendar_data(CALENDAR_IDS, start_date, end_date if end_date.strip() else None)

# # # Main execution
# # if __name__ == '__main__':
# #     main()

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
# Hard-coded calendar IDs
PRIMARY_CALENDAR_ID = 'primary'
SECOND_CALENDAR_ID = 'fe8846449c91e6dbd1177a8d1d29cd4e57ad901e44d4262f5fc865cc1720c95e@group.calendar.google.com'  # Replace with actual second calendar ID

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

def fetch_events_from_service(service, calendar_id, time_min, time_max):
    """
    Fetches events from the calendar service for the specified time range.
    Handles API errors gracefully.
    """
    try:
        events_result = service.events().list(
            calendarId=calendar_id,
            timeMin=time_min,
            timeMax=time_max,
            singleEvents=True,
            orderBy='startTime'
        ).execute()
        return events_result.get('items', [])
    except HttpError as error:
        print(f"An error occurred while fetching events from {calendar_id}: {error}")
        return []

def format_events(events, calendar_id=None):
    """Formats the raw event data into a simplified structure."""
    if not events:
        print(f'No events found in calendar: {calendar_id if calendar_id else "primary"}')
        return []
    
    formatted_events = []
    
    for event in events:
        # Extract start and end times
        start = event['start'].get('dateTime', event['start'].get('date'))
        end = event['end'].get('dateTime', event['end'].get('date'))
        
        formatted_event = {
            'start': start,
            'end': end,
            'summary': event.get('summary', ''),  # Default to empty string
            'description': event.get('description', ''),  # Default to empty string
            'calendar': calendar_id if calendar_id else 'primary'  # Ensure calendar ID is never None
        }
        
        formatted_events.append(formatted_event)
    
    return formatted_events

def get_calendar_data(start_date, end_date=None):
    """
    Retrieves calendar events within the specified date range from both primary and second calendar.
    If end_date is None, fetches all events for the month of start_date.
    
    Args:
        start_date (str): Start date in YYYY-MM-DD format.
        end_date (str, optional): End date in YYYY-MM-DD format.
    
    Returns:
        list: Combined and formatted events from both calendars.
    """
    # Hard-coded calendar IDs
    calendar_ids = [PRIMARY_CALENDAR_ID, SECOND_CALENDAR_ID]
    
    # Parse and calculate dates
    start_date_obj = parse_date(start_date)
    end_date_obj = calculate_end_date(start_date_obj, end_date)

    # Format dates for API
    time_min, time_max = format_dates_for_api(start_date_obj, end_date_obj)

    # Get calendar service
    service = get_service()

    # Fetch and combine events from both calendars
    all_events = []
    for calendar_id in calendar_ids:
        print(f"Fetching events from calendar: {calendar_id}")
        events = fetch_events_from_service(service, calendar_id, time_min, time_max)
        formatted_events = format_events(events, calendar_id)
        all_events.extend(formatted_events)

    print(f"Total events fetched: {len(all_events)}")
    return all_events

def main():
    # Example: User inputs
    start_date = input("Enter start date (YYYY-MM-DD): ")
    end_date = input("Enter end date (YYYY-MM-DD) [leave blank for full month]: ")
    end_date = end_date if end_date.strip() else None

    # Fetch and display events from both calendars
    events = get_calendar_data(start_date, end_date)

# Main execution
if __name__ == '__main__':
    main()