import re
from datetime import datetime, timedelta

class FormatterNode:
    """
    FormatterNode processes raw calendar data into the expected format for SheetNode.
    Unknown fields are filled with None or blank spaces.
    Events are sorted chronologically before being formatted.
    """

    def __init__(self):
        self.template = [
            "Date", "Studio", "Artist Name", "Session Type", 
            "Start Time", "End Time", "Hours", "Paid?", 
            "Price", "Engineer Name", "Engineer Payment", 
            "Referral", "Referral Payment"
        ]

    def format_data(self, raw_data):
        formatted_data = [self.template]  # Start with headers
        
        # Sort raw_data chronologically by start time
        sorted_events = self.sort_events_chronologically(raw_data)
        
        for event in sorted_events:
            print(f"DEBUG: Event Data: {event}")

            # Extract fields from event data
            start = event.get("start")
            end = event.get("end")
            summary = event.get("summary")
            description = event.get("description")
            calendar_id = event.get("calendar", "primary")  # Fixed to match CalendarNode output

            # Debugging: Set defaults for missing data
            if not start:
                start = "2025-01-01T00:00:00"  # Example default
            if not end:
                end = start  # Default to start time, or adjust as needed

            # Extract formatted time data
            date, start_time, end_time, hours = self.extract_time_info(start, end)

            # Debugging: Print extracted time values
            print(f"DEBUG: Date: {date}, Start Time: {start_time}, End Time: {end_time}, Hours: {hours}")

            # Other formatting logic
            artist_name = self.format_artist(summary)
            session_type = self.determine_session_type(description)
            
            # Extract engineer info and payment details
            engineer_indicator, engineer_name, engineer_payment = self.format_engineer(description)
            
            # Process comprehensive payment information
            paid, price, eng_name, eng_payment, referral, referral_payment = self.process_payment_info(description)
            
            # If engineer name was found in process_payment_info but not in format_engineer, use it
            if not engineer_name and eng_name:
                engineer_name = eng_name
                engineer_payment = eng_payment
            
            # If no engineer name was found, set to empty
            if not engineer_name:
                engineer_name = "No Engineer"
            
            # Determine studio based on calendar ID
            studio = self.determine_studio(calendar_id)

            # Append formatted row to output
            formatted_data.append([
                date, studio, artist_name, session_type,
                start_time, end_time, hours, paid,
                price, engineer_name, engineer_payment,
                referral, referral_payment
            ])

        return formatted_data

    def sort_events_chronologically(self, events):
        """
        Sorts events chronologically by start time.
        Handles timezone-aware and timezone-naive datetime objects.
        
        Args:
            events (list): List of event dictionaries
            
        Returns:
            list: Sorted list of events
        """
        def convert_to_datetime(date_str):
            """Convert various date string formats to datetime objects, ensuring consistent timezone handling"""
            if not date_str:
                return datetime.min
            
            # Remove 'Z' suffix if present to make all datetimes naive
            if isinstance(date_str, str):
                date_str = date_str.replace('Z', '')
                
                # Handle full-day events (date only)
                if 'T' not in date_str:
                    try:
                        return datetime.fromisoformat(date_str)
                    except ValueError:
                        print(f"Warning: Could not parse date from {date_str}")
                        return datetime.min
                
                # Handle datetime strings with time component
                try:
                    # Parse datetime and remove timezone info to make it naive
                    dt = datetime.fromisoformat(date_str)
                    if dt.tzinfo is not None:
                        # Convert to naive datetime in local time
                        dt = dt.replace(tzinfo=None)
                    return dt
                except ValueError:
                    print(f"Warning: Could not parse datetime from {date_str}")
                    return datetime.min
            
            return datetime.min
        
        def get_sort_key(event):
            """Extract sortable datetime from event"""
            start = event.get("start", "")
            return convert_to_datetime(start)
        
        # Sort events by start time
        return sorted(events, key=get_sort_key)

    def determine_studio(self, calendar_id):
        """
        Determines the studio name based on the calendar ID.
        
        Args:
            calendar_id (str): The calendar ID from which the event was fetched.
            
        Returns:
            str: The studio name or an empty string if undetermined.
        """
        # Map calendar IDs to studio names
        studio_map = {
            "primary": "Studio A",
            "fe8846449c91e6dbd1177a8d1d29cd4e57ad901e44d4262f5fc865cc1720c95e@group.calendar.google.com": "Studio B",  # Added the second calendar ID mapping
            # Add more mappings as needed
        }
        
        # Return the mapped studio name or a default value
        return studio_map.get(calendar_id, calendar_id)

    def extract_time_info(self, start, end=""):
        """
        Extracts date, start time, end time, and calculates session duration.

        Args:
            start (str): ISO 8601 datetime string for event start.
            end (str, optional): ISO 8601 datetime string for event end.

        Returns:
            tuple: (date, start_time, end_time, hours)
        """
        if not start:
            return "", "", "", ""

        try:
            # Handle full-day events (date only, no time component)
            if 'T' not in start:
                start_date = datetime.fromisoformat(start)
                date = start_date.strftime("%Y-%m-%d")
                return date, "00:00", "23:59", "24.0"
            
            # Convert ISO datetime string to datetime object for start
            # Remove the 'Z' suffix if present for fromisoformat compatibility
            start = start.replace('Z', '') if start.endswith('Z') else start
            start_dt = datetime.fromisoformat(start)
            
            # Remove timezone info if present to ensure consistent handling
            if start_dt.tzinfo is not None:
                start_dt = start_dt.replace(tzinfo=None)
                
            date = start_dt.strftime("%Y-%m-%d")
            start_time = start_dt.strftime("%H:%M")  # Format HH:MM

            # If no end time provided, assume it's 1 hour after the start time
            if not end:
                end_dt = start_dt + timedelta(hours=1)  # Default to 1 hour after start
            else:
                # Otherwise, use the provided end time
                end = end.replace('Z', '') if end.endswith('Z') else end
                end_dt = datetime.fromisoformat(end)
                # Remove timezone info if present
                if end_dt.tzinfo is not None:
                    end_dt = end_dt.replace(tzinfo=None)
            
            # Calculate end time and duration
            end_time = end_dt.strftime("%H:%M")  # Format HH:MM
            duration = (end_dt - start_dt).total_seconds() / 3600  # Calculate duration in hours

            # Ensure that duration is non-negative
            if duration < 0:
                duration = 0

            # Return formatted data
            return date, start_time, end_time, f"{duration:.2f}"  # Format duration with 2 decimal places
        except Exception as e:
            print(f"Error processing time: {e}")
            return "", "", "", ""

    def format_artist(self, summary):
        """
        Extracts the artist's name from the event summary.
        
        Args:
            summary (str): The event summary.

        Returns:
            str: The formatted artist name.
        """
        if not summary:
            return ""
        
        # Remove "Session w/" if present
        session_match = re.search(r"session\s+w/\s*(.+)", summary, re.IGNORECASE)
        if session_match:
            return session_match.group(1).strip()
        
        # Check for "Recording session for" pattern
        recording_match = re.search(r"recording\s+session\s+for\s*(.+)", summary, re.IGNORECASE)
        if recording_match:
            return recording_match.group(1).strip()
        
        # Remove everything after a colon
        if ':' in summary:
            return summary.split(':', 1)[0].strip()
        
        return summary.strip()

    def determine_session_type(self, description):
        """
        Determines the session type based on description.
        
        Args:
            description (str): The event description.

        Returns:
            str: Session type based on keyword analysis.
        """
        if not description:
            return "No Engineer"
        
        description_lower = description.lower()
        
        # Look for engineer names
        if any(name in description_lower for name in ["john", "jaylun", "aaron", "chris"]):
            return "Engineer"
        
        # Look for session type keywords
        if "mix" in description_lower or "mixing" in description_lower:
            return "Mixing"
        elif "master" in description_lower or "mastering" in description_lower:
            return "Mastering"
        elif "record" in description_lower or "recording" in description_lower:
            return "Recording"
        
        return "No Engineer"

    def format_engineer(self, description):
        """
        Formats the description by extracting potential engineer for sessions
        
        Args:
            description (str): the event description, which may contain engineer name and pricing

        Returns:
            tuple:
                - engineer (str): "Y" if an engineer is present, otherwise "".
                - engineer_name (str): The name of the engineer if present, otherwise "".
                - price (str): the price of the session if present, otherwise "".
        """
        if not description:
            return "", "", ""  # empty fields for an empty description

        # Enhanced pattern matching to be more flexible with engineer names
        # Match1 first format: "<Name> <Price>"
        match1 = re.search(r'([A-Za-z]+)\s+(\d+)', description)
        if match1:
            engineer_name = match1.group(1)
            price = match1.group(2)
            return "Y", engineer_name, price

        # Match2 second format: "<Price> <Name>"
        match2 = re.search(r'(\d+)\s+([A-Za-z]+)', description)
        if match2:
            price = match2.group(1)
            engineer_name = match2.group(2)
            return "Y", engineer_name, price

        # Match3 third format: "<Name>"
        # Looking for common engineer names
        engineer_names = ["john", "jaylun", "aaron", "chris"]
        for name in engineer_names:
            if re.search(r'\b' + name + r'\b', description.lower()):
                return "Y", name.capitalize(), ""

        return "", "", ""

    def process_payment_info(self, description):
        """
        Extracts payment-related information including price, engineer name, and referral details.
        
        Args:
            description (str): The event description.

        Returns:
            tuple: (paid, price, engineer_name, engineer_payment, referral, referral_payment)
        """
        if not description:
            return "", "", "", "", "", ""

        paid = "N"  # Default to unpaid
        price = ""
        engineer_name = ""
        engineer_payment = ""
        referral = ""
        referral_payment = ""

        # Enhanced pattern matching
        # Look for price patterns: "$150", "150$", "150 USD", etc.
        price_match = re.search(r'(\$\s*\d+|\d+\s*\$|\d+\s*usd|\d+\s*dollars)', description, re.IGNORECASE)
        if price_match:
            # Extract just the numeric part
            price = re.search(r'\d+', price_match.group(1)).group(0)
            paid = "Y"
        else:
            # Simpler number pattern if no currency indicators
            num_match = re.search(r'\b(\d+)\b', description)
            if num_match:
                price = num_match.group(1)
                paid = "Y"

        # Look for referral patterns
        referral_match = re.search(r'ref(?:erral)?[:\s]+([A-Za-z]+)', description, re.IGNORECASE)
        if referral_match:
            referral = referral_match.group(1)
            # If there's a referral and a price, assume referral payment is 10%
            if price:
                referral_payment = str(int(int(price) * 0.1))

        # Look for engineer names if not already found by price patterns
        if not engineer_name:
            eng_match = re.search(r'\b(john|jaylun|aaron|chris)\b', description, re.IGNORECASE)
            if eng_match:
                engineer_name = eng_match.group(1).capitalize()
        
        # Calculate engineer payment if there's a price (assuming 50% split)
        if price and engineer_name:
            engineer_payment = str(int(int(price) * 0.5))

        return paid, price, engineer_name, engineer_payment, referral, referral_payment

