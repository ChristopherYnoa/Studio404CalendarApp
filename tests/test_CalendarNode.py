import unittest
from unittest.mock import patch, MagicMock
from datetime import datetime
import CalendarNode
from CalendarNode import (
    get_service,
    parse_date,
    calculate_end_date,
    format_dates_for_api,
    fetch_events_from_service,
    format_events,
    get_calendar_data
)

class TestCalendarNode(unittest.TestCase):

    @patch('CalendarNode.build')
    def test_get_service(self, mock_build):
        """
        Test if `get_service` correctly initializes the Google Calendar service.
        """
        # Mock the service instance
        mock_service = MagicMock()
        mock_build.return_value = mock_service

        service = get_service()

        # Assert that the service is built correctly
        mock_build.assert_called_once_with('calendar', 'v3', credentials=unittest.mock.ANY)
        self.assertIsNotNone(service)

    def test_parse_date(self):
        """
        Test the `parse_date` function for valid and invalid date strings.
        """
        valid_date = "2024-12-01"
        parsed_date = parse_date(valid_date)
        self.assertEqual(parsed_date, datetime(2024, 12, 1))

        invalid_date = "12-01-2024"
        with self.assertRaises(ValueError):
            parse_date(invalid_date)

    def test_calculate_end_date(self):
        """
        Test the `calculate_end_date` function for both provided and default end dates.
        """
        start_date = datetime(2024, 12, 1)
        # Test default end date (end of the month)
        calculated_end_date = calculate_end_date(start_date)
        self.assertEqual(calculated_end_date, datetime(2024, 12, 31, 23, 59, 59))

        # Test provided end date
        provided_end_date = "2024-12-15"
        calculated_end_date = calculate_end_date(start_date, provided_end_date)
        self.assertEqual(calculated_end_date, datetime(2024, 12, 15, 23, 59, 59))

    def test_format_dates_for_api(self):
        """
        Test the `format_dates_for_api` function to ensure correct ISO 8601 formatting.
        """
        start_date = datetime(2024, 12, 1)
        end_date = datetime(2024, 12, 31, 23, 59, 59)
        time_min, time_max = format_dates_for_api(start_date, end_date)

        self.assertEqual(time_min, "2024-12-01T00:00:00Z")
        self.assertEqual(time_max, "2024-12-31T23:59:59Z")

    @patch('CalendarNode.get_service')
    def test_fetch_events_from_service(self, mock_get_service):
        """
        Test the `fetch_events_from_service` function for both successful and error scenarios.
        """
        # Mock the service and events response
        mock_service = MagicMock()
        mock_events = {'items': [{'summary': 'Test Event'}]}
        mock_service.events().list().execute.return_value = mock_events
        mock_get_service.return_value = mock_service

        # Successful fetch
        events = fetch_events_from_service(mock_service, "2024-12-01T00:00:00Z", "2024-12-31T23:59:59Z")
        self.assertEqual(events, [{'summary': 'Test Event'}])

        # Simulate an error
        mock_service.events().list().execute.side_effect = Exception("API Error")
        events = fetch_events_from_service(mock_service, "2024-12-01T00:00:00Z", "2024-12-31T23:59:59Z")
        self.assertEqual(events, [])

    def test_format_events(self):
        """
        Test the `format_events` function to ensure correct formatting of event data.
        """
        raw_events = [
            {
                'start': {'dateTime': '2024-12-16T19:30:00-05:00'},
                'summary': 'Session w/ Joe',
                'description': '300'
            },
            {
                'start': {'date': '2024-12-17'},
                'summary': 'Session w/ {Null}',
                'description': 'Holiday'
            },
            {
                'start': {'dateTime': '2024-12-18T10:00:00-05:00'},
                'summary': 'Meeting'
                # No description
            }
        ]

        formatted = format_events(raw_events)
        self.assertEqual(len(formatted), 3)
        self.assertEqual(formatted[0]['summary'], 'Session w/ Joe')
        self.assertEqual(formatted[0]['description'], '300')
        self.assertEqual(formatted[1]['summary'], 'Session w/ {Null}')
        self.assertEqual(formatted[1]['description'], 'Holiday')
        self.assertIsNone(formatted[2].get('description'))

    @patch('CalendarNode.get_service')
    def test_get_calendar_data_with_mock_service(self, mock_get_service):
        """
        Test the `get_calendar_data` function for fetching and formatting events.
        """
        # Mock calendar events response
        mock_service = MagicMock()
        mock_events = {
            'items': [
                {
                    'start': {'dateTime': '2024-12-16T19:30:00-05:00'},
                    'summary': 'Session w/ Joe',
                    'description': '300'
                },
                {
                    'start': {'date': '2024-12-17'},
                    'summary': 'Session w/ {Null}',
                    'description': 'Holiday'
                }
            ]
        }
        mock_service.events().list().execute.return_value = mock_events
        mock_get_service.return_value = mock_service

        events = get_calendar_data('2024-12-16', '2024-12-17')

        self.assertEqual(len(events), 2)
        self.assertEqual(events[0]['summary'], 'Session w/ Joe')
        self.assertEqual(events[1]['summary'], 'Session w/ {Null}')

    @patch('CalendarNode.get_service')
    def test_no_events(self, mock_get_service):
        """
        Test behavior when no events are returned by the API.
        """
        # Mock an empty response
        mock_service = MagicMock()
        mock_service.events().list().execute.return_value = {'items': []}
        mock_get_service.return_value = mock_service

        events = get_calendar_data('2024-12-01', '2024-12-31')
        self.assertEqual(events, [])

if __name__ == "__main__":
    unittest.main()

# import unittest
# import sys
# import os

# # Add the parent directory to the system path
# parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
# sys.path.insert(0, parent_dir)

# import CalendarNode  # Import your module
# from unittest.mock import patch, MagicMock
# from CalendarNode import get_service, get_calendar_data



# class TestCalendarNode(unittest.TestCase):

#     @patch('CalendarNode.build')
#     def test_get_service(self, mock_build):
#         """
#         Test if `get_service` correctly initializes the Google Calendar service.
#         """
#         # Mock the service instance
#         mock_service = MagicMock()
#         mock_build.return_value = mock_service

#         service = get_service()

#         # Assert that the service is built correctly
#         mock_build.assert_called_once_with('calendar', 'v3', credentials=unittest.mock.ANY)
#         self.assertIsNotNone(service)

#     @patch('CalendarNode.get_service')
#     @patch('CalendarNode.build')
#     def test_get_calendar_data_with_mock_service(self, mock_build, mock_get_service):
#         """
#         Test if `get_calendar_data` fetches and formats events correctly.
#         """
#         # Mock calendar events response
#         mock_service = MagicMock()
#         mock_events = {
#             'items': [
#                 {
#                     'start': {'dateTime': '2024-12-16T19:30:00-05:00'},
#                     'summary': 'Session w/ Joe',
#                     'description': '300'
#                 },
#                 {
#                     'start': {'date': '2024-12-17'},
#                     'summary': 'Session w/ {Null}',
#                     'description': 'Holiday'
#                 },
#                 {
#                     'start': {'dateTime': '2024-12-18T10:00:00-05:00'},
#                     'summary': 'Meeting',
#                     # No description provided
#                 },
#             ]
#         }
#         mock_service.events().list().execute.return_value = mock_events
#         mock_get_service.return_value = mock_service

#         # Call the function with mock data
#         start_date = '2024-12-16'
#         end_date = '2024-12-18'
#         events = get_calendar_data(start_date, end_date)

#         # Verify the results
#         self.assertEqual(len(events), 3)
#         self.assertEqual(events[0]['summary'], 'Session w/ Joe')
#         self.assertEqual(events[0]['description'], '300')
#         self.assertEqual(events[1]['summary'], 'Session w/ {Null}')
#         self.assertEqual(events[1]['description'], 'Holiday')
#         self.assertEqual(events[2]['summary'], 'Meeting')
#         self.assertIsNone(events[2].get('description'))

#         #printing the events line by line
#         for event in events:
#             print(event)

#     def test_date_parsing(self):
#         """
#         Test date parsing logic for valid and invalid inputs.
#         """
#         # Valid date range
#         start_date = '2024-12-01'
#         end_date = '2024-12-31'

#         try:
#             events = get_calendar_data(start_date, end_date)
#             self.assertTrue(True)  # Pass if no exception is raised
#         except ValueError:
#             self.fail("get_calendar_data() raised ValueError unexpectedly!")

#         # Invalid date format
#         start_date = '12-01-2024'
#         with self.assertRaises(ValueError):
#             get_calendar_data(start_date)

#     @patch('CalendarNode.get_service')
#     def test_no_events(self, mock_get_service):
#         """
#         Test behavior when no events are returned by the API.
#         """
#         # Mock an empty response
#         mock_service = MagicMock()
#         mock_service.events().list().execute.return_value = {'items': []}
#         mock_get_service.return_value = mock_service

#         events = get_calendar_data('2024-12-01', '2024-12-31')

#         self.assertEqual(events, [])
