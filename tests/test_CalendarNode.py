import unittest
import sys
import os

# Add the parent directory to the system path
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, parent_dir)

import CalendarNode  # Import your module
from unittest.mock import patch, MagicMock
from CalendarNode import get_service, get_calendar_data



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

    @patch('CalendarNode.get_service')
    @patch('CalendarNode.build')
    def test_get_calendar_data_with_mock_service(self, mock_build, mock_get_service):
        """
        Test if `get_calendar_data` fetches and formats events correctly.
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
                    'summary': 'All-day event',
                    'description': 'Holiday'
                },
                {
                    'start': {'dateTime': '2024-12-18T10:00:00-05:00'},
                    'summary': 'Meeting',
                    # No description provided
                },
            ]
        }
        mock_service.events().list().execute.return_value = mock_events
        mock_get_service.return_value = mock_service

        # Call the function with mock data
        start_date = '2024-12-16'
        end_date = '2024-12-18'
        events = get_calendar_data(start_date, end_date)

        # Verify the results
        self.assertEqual(len(events), 3)
        self.assertEqual(events[0]['summary'], 'Session w/ Joe')
        self.assertEqual(events[0]['description'], '300')
        self.assertEqual(events[1]['summary'], 'All-day event')
        self.assertEqual(events[1]['description'], 'Holiday')
        self.assertEqual(events[2]['summary'], 'Meeting')
        self.assertIsNone(events[2].get('description'))

    def test_date_parsing(self):
        """
        Test date parsing logic for valid and invalid inputs.
        """
        # Valid date range
        start_date = '2024-12-01'
        end_date = '2024-12-31'

        try:
            events = get_calendar_data(start_date, end_date)
            self.assertTrue(True)  # Pass if no exception is raised
        except ValueError:
            self.fail("get_calendar_data() raised ValueError unexpectedly!")

        # Invalid date format
        start_date = '12-01-2024'
        with self.assertRaises(ValueError):
            get_calendar_data(start_date)

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
