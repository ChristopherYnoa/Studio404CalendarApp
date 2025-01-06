import unittest
from unittest.mock import patch, MagicMock
import os
import sys

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, parent_dir)

from SheetNode import get_sheets_service, create_sheet_if_not_exists, write_data_to_sheet


class TestSheetNode(unittest.TestCase):
    @patch('SheetNode.build')  # Mock the Google Sheets API client
    def test_get_sheets_service_valid_token(self, mock_build):
        """Test that the Sheets service is returned with valid credentials."""
        mock_creds = MagicMock()
        mock_creds.valid = True
        with patch('SheetNode.Credentials.from_authorized_user_file', return_value=mock_creds):
            service = get_sheets_service()
            self.assertIsNotNone(service)
            mock_build.assert_called_once_with('sheets', 'v4', credentials=mock_creds)

    @patch('SheetNode.build')  # Mock the Google Sheets API client
    @patch('SheetNode.os.path.exists', return_value=False)  # Simulate no token file
    def test_get_sheets_service_no_token(self, mock_exists, mock_build):
        """Test that the user is prompted for authentication if no token exists."""
        with patch('SheetNode.InstalledAppFlow.from_client_secrets_file') as mock_flow:
            mock_flow_instance = MagicMock()
            mock_flow.return_value = mock_flow_instance
            mock_flow_instance.run_local_server.return_value = MagicMock()
            service = get_sheets_service()
            self.assertIsNotNone(service)
            mock_flow.assert_called_once()
            mock_build.assert_called_once()

    @patch('SheetNode.build')  # Mock the Google Sheets API client
    def test_create_sheet_if_not_exists(self, mock_build):
        """Test that a new sheet is created if it doesn't exist."""
        mock_service = MagicMock()
        mock_build.return_value = mock_service

        # Simulate existing sheets
        mock_service.spreadsheets().get().execute.return_value = {
            'sheets': [{'properties': {'title': 'ExistingSheet'}}]
        }

        spreadsheet_id = 'test_spreadsheet_id'
        sheet_title = 'NewSheet'

        # Test sheet creation
        result = create_sheet_if_not_exists(mock_service, spreadsheet_id, sheet_title)
        self.assertTrue(result)
        mock_service.spreadsheets().batchUpdate.assert_called_once_with(
            spreadsheetId=spreadsheet_id,
            body={
                "requests": [{"addSheet": {"properties": {"title": sheet_title}}}]
            }
        )

    @patch('SheetNode.build')  # Mock the Google Sheets API client
    def test_write_data_to_sheet(self, mock_build):
        """Test that data is written to the correct sheet."""
        mock_service = MagicMock()
        mock_build.return_value = mock_service

        spreadsheet_id = 'test_spreadsheet_id'
        sheet_name = 'TestSheet'
        data = [["Header1", "Header2"], ["Value1", "Value2"]]

        write_data_to_sheet(mock_service, spreadsheet_id, sheet_name, data)

        mock_service.spreadsheets().values().update.assert_called_once_with(
            spreadsheetId=spreadsheet_id,
            range=f"{sheet_name}!A1",
            valueInputOption="RAW",
            body={"values": data}
        )
        mock_service.spreadsheets().values().update().execute.assert_called_once()

    @patch('SheetNode.get_sheets_service')  # Mock the service method
    @patch('SheetNode.create_sheet_if_not_exists')  # Mock the sheet creation method
    @patch('SheetNode.write_data_to_sheet')  # Mock the data writing method
    def test_main_workflow(self, mock_write, mock_create, mock_service):
        """Test the main workflow."""
        mock_service.return_value = MagicMock()
        mock_create.return_value = True

        # Mock FormatterNode and get_calendar_data
        with patch('SheetNode.FormatterNode') as MockFormatter:
            mock_formatter = MockFormatter.return_value
            mock_formatter.format_data.return_value = [["Header1", "Header2"], ["Value1", "Value2"]]

            with patch('SheetNode.get_calendar_data', return_value="mock_calendar_data"):
                from SheetNode import main

                # Simulate user input
                with patch('builtins.input', side_effect=['2024-12-01', '2024-12-31']):
                    main()

                mock_create.assert_called_once_with(mock_service.return_value, "19GpFb5B8SaVqjgqkBGrytiCzwU6D1PIiqnRrw_Qrmcg", "2024-12-31")
                mock_write.assert_called_once_with(
                    mock_service.return_value,
                    "19GpFb5B8SaVqjgqkBGrytiCzwU6D1PIiqnRrw_Qrmcg",
                    "2024-12-31",
                    [["Header1", "Header2"], ["Value1", "Value2"]]
                )


if __name__ == '__main__':
    unittest.main()
