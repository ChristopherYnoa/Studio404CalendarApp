import unittest
import sys
import os

# Add the parent directory to the system path
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, parent_dir)

from FormatterNode import FormatterNode  # Import your module


class TestFormatterNode(unittest.TestCase):
    def setUp(self):
        """Set up the FormatterNode instance for testing."""
        self.formatter = FormatterNode()
        self.template = ["Date", "Studio", "Artist Name", "Engineer?", "Engineer Name", "Referral", "Hours", "Price", "Paid?"]

    def test_format_complete_data(self):
        """Test if complete data is formatted correctly."""
        raw_calendar_data = [
            {
                "date": "2024-12-21",
                "studio": "Studio B",
                "artist_name": "John Doe",
                "engineer": "Y",
                "engineer_name": "John",
                "referral": "John",
                "hours": "3",
                "price": "150",
                "paid": "Y",
            }
        ]
        expected_output = [
            self.template,
            ["2024-12-21", "Studio B", "John Doe", "Y", "John", "John", "3", "150", "Y"]
        ]
        self.assertEqual(self.formatter.format_data(raw_calendar_data), expected_output)

    def test_format_incomplete_data(self):
        """Test if incomplete data is formatted correctly with None or blank spaces."""
        raw_calendar_data = [
            {"date": "2024-12-22", "studio": "Studio A", "artist_name": "Jane Smith"}
        ]
        expected_output = [
            self.template,
            ["2024-12-22", "Studio A", "Jane Smith", "", "", "", "", "", ""]
        ]
        self.assertEqual(self.formatter.format_data(raw_calendar_data), expected_output)

    def test_format_empty_data(self):
        """Test if empty data returns only the header row."""
        raw_calendar_data = []
        expected_output = [self.template]
        self.assertEqual(self.formatter.format_data(raw_calendar_data), expected_output)

    def test_format_mixed_data(self):
        """Test if mixed complete and incomplete data is formatted correctly."""
        raw_calendar_data = [
            {
                "date": "2024-12-21",
                "studio": "Studio B",
                "artist_name": "John Doe",
                "engineer": "Y",
                "engineer_name": "John",
                "referral": "John",
                "hours": "3",
                "price": "150",
                "paid": "Y",
            },
            {"date": "2024-12-22", "studio": "Studio A", "artist_name": "Jane Smith"}
        ]
        expected_output = [
            self.template,
            ["2024-12-21", "Studio B", "John Doe", "Y", "John", "John", "3", "150", "Y"],
            ["2024-12-22", "Studio A", "Jane Smith", "", "", "", "", "", ""]
        ]
        self.assertEqual(self.formatter.format_data(raw_calendar_data), expected_output)

if __name__ == "__main__":
    unittest.main()
