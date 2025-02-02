import re
from datetime import datetime

class FormatterNode:
    """
    FormatterNode processes raw calendar data into the expected format for SheetNode.
    Unknown fields are filled with None or blank spaces.
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
        
        for event in raw_data:
            print(f"DEBUG: Event Data: {event}")

            # Extract fields from event data
            start = event.get("start")
            end = event.get("end")
            summary = event.get("summary")
            description = event.get("description")

            # Debugging: Print raw event data to check the start and end values
            if not start:
                start = "2025-01-01T00:00:00"  # Example default
            if not end:
                end = start  # Default to start time, or adjust as needed

            # Extract formatted time data
            date, start_time, end_time, hours = self.extract_time_info(start, end)

            # Debugging: Print extracted time values
            print(f"DEBUG: Date: {date}, Start Time: {start_time}, End Time: {end_time}, Hours: {hours}")

            # Other formatting logic (Artist Name, Session Type, etc.)
            artist_name = self.format_artist(summary)
            session_type = self.determine_session_type(description)
            
            # Extract engineer info
            engineer_indicator, engineer_name, engineer_payment = self.format_engineer(description)
            
            # If no engineer name was found, set to empty
            if engineer_name == "":
                engineer_name = "No Engineer"
            
            # Process payment-related information
            
            # Placeholder for studio (set to empty string for now)
            studio = ""
            paid = ""
            price = ""
            engineer_payment = ""
            referral = ""
            referral_payment = ""

            # Append formatted row to output
            formatted_data.append([
                date, studio, artist_name, session_type,
                start_time, end_time, hours, paid,
                price, engineer_name, engineer_payment,
                referral, referral_payment
            ])

        return formatted_data




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
            # Convert ISO datetime string to datetime object for start
            start_dt = datetime.fromisoformat(start)
            date = start_dt.strftime("%Y-%m-%d")
            start_time = start_dt.strftime("%H:%M")  # Format HH:MM

            # If no end time provided, assume it's 1 hour after the start time
            if not end:
                end_dt = start_dt + timedelta(hours=1)  # Default to 1 hour after start
            else:
                # Otherwise, use the provided end time
                end_dt = datetime.fromisoformat(end)
            
            # Calculate end time and duration
            end_time = end_dt.strftime("%H:%M")  # Format HH:MM
            duration = (end_dt - start_dt).total_seconds() / 3600  # Calculate duration in hours

            # Ensure that duration is non-negative
            if duration < 0:
                duration = 0

            # Return formatted data
            return date, start_time, end_time, str(round(duration, 2))  # Round duration to 2 decimal places
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
        session_match = re.match(r"session w/\s*(.+)", summary, re.IGNORECASE)
        if session_match:
            return session_match.group(1).strip()
        
        # Remove everything after a colon
        if ':' in summary:
            return summary.split(':', 1)[0].strip()
        
        return summary.strip()

    def determine_session_type(self, description):
        """
        Determines whether the session had an engineer or not.
        
        Args:
            description (str): The event description.

        Returns:
            str: "Engineer" if an engineer was present, otherwise "No Engineer".
        """
        if not description:
            return "No Engineer"
        
        if any(word in description.lower() for word in ["john", "jaylun", "aaron", "chris"]):
            return "Engineer"
        
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
            return "","","" #empty fields for an empty description

        #match1 first format: "<Name> <Price>"
        match1 = re.match(r'^([A-Za-z]+)\s+(\d+)$', description)
        if match1:
            engineer_name = match1.group(1)
            price = match1.group(2)
            return "Y", engineer_name, price

        #match2 second format: "<Price> <Name>"
        match2 = re.match(r'^(\d+)\s+([A-Za-z]+)$', description)
        if match2:
            price = match2.group(1)
            engineer_name = match2.group(2)
            return "Y", engineer_name, price

        #match3 third format: "<Name>"
        match3 = re.match(r'^([A-Za-z]+)$', description)
        if match3:
            engineer_name = match3.group(1)
            return "Y", engineer_name, ""

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

        # Match formats like "John 150" or "150 Aaron"
        match1 = re.match(r'^([A-Za-z]+)\s+(\d+)$', description)
        match2 = re.match(r'^(\d+)\s+([A-Za-z]+)$', description)

        if match1:
            engineer_name = match1.group(1)
            price = match1.group(2)
            paid = "Y"
        elif match2:
            price = match2.group(1)
            engineer_name = match2.group(2)
            paid = "Y"

        # Assuming engineer payment is half of session price
        if price:
            engineer_payment = str(int(price) // 2)

        return paid, price, engineer_name, engineer_payment, referral, referral_payment

