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
        """
        Formats raw calendar data into the expected list of lists structure.
        
        Args:
            raw_data (list): List of dictionaries representing raw calendar events.
        
        Returns:
            list: A list of lists formatted as per the template.
        """
        formatted_data = [self.template]  # Start with headers
        
        for event in raw_data:
            # Extract fields from the raw event data
            start = event.get("start")  # Event start datetime
            summary = event.get("summary")  # Event summary (e.g., "Session w/ Joe")
            description = event.get("description")  # Event description (optional)

            # Format extracted values
            date, start_time, end_time, hours = self.extract_time_info(start)
            artist_name = self.format_artist(summary)
            session_type = self.determine_session_type(description)
            paid, price, engineer_name, engineer_payment, referral, referral_payment = self.process_payment_info(description)

            # Placeholder for studio (adjust as needed)
            studio = ""

            # Append formatted row to the output
            formatted_data.append([
                date, studio, artist_name, session_type, 
                start_time, end_time, hours, paid, 
                price, engineer_name, engineer_payment, 
                referral, referral_payment
            ])

        return formatted_data

    def extract_time_info(self, start):
        """
        Extracts date, start time, and calculates end time and session duration.
        
        Args:
            start (str): The event's start time (ISO 8601 datetime string).
        
        Returns:
            tuple: (date, start_time, end_time, hours)
        """
        if not start:
            return "", "", "", ""
        
        try:
            # Convert ISO datetime string to datetime object
            dt_obj = datetime.fromisoformat(start)
            date = dt_obj.strftime("%Y-%m-%d")
            start_time = dt_obj.strftime("%H:%M")  # Extract HH:MM format

            # Placeholder: Assuming 1-hour sessions if no explicit end time
            end_time = (dt_obj.replace(minute=dt_obj.minute + 60)).strftime("%H:%M")
            hours = "1"  # Default to 1 hour

            return date, start_time, end_time, hours
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
        
        if any(word in description.lower() for word in ["engineer", "mix", "record"]):
            return "Engineer"
        
        return "No Engineer"

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





# import re

# class FormatterNode:
#     """
#     FormatterNode processes raw calendar data into the expected format for SheetNode.
#     Unknown fields are filled with None or blank spaces.
#     """
    
#     def __init__(self):
#         self.template = ["Date", "Studio", "Artist Name", "Engineer?", "Engineer Name", "Referral", "Hours", "Price", "Paid?"]

#     def format_data(self, raw_data):
#         """
#         Formats raw calendar data into the expected list of lists structure.
        
#         Args:
#             raw_data (list): List of dictionaries representing raw calendar events.
        
#         Returns:
#             list: A list of lists formatted as per the template.
#         """
#         formatted_data = [self.template]  # Start with headers
        
#         for event in raw_data:
#             # Extract fields from the raw event data
#             start = event.get("start")  # Event start datetime
#             summary = event.get("summary")  # Event summary (e.g., "Session w/ Joe")
#             description = event.get("description")  # Event description (optional)

#             # Format the artist's name using regex to extract the name after "Session w/"
#             artist_name = self.format_artist_name(summary)
            
#             # Format the date (this will handle the datetime case and provide just the date)
#             date = self.extract_date(start)

#             #Format the engineer-related fields
#             engineer, engineer_name, price = self.format_engineer(description)
            
#             # Add empty values for other fields (e.g., "Studio", "Engineer?") if they're not available
#             studio = "B"  # Example; adjust as needed
#             #engineer = ""  # Example; adjust as needed
#             #engineer_name = ""  # Example; adjust as needed
#             referral = ""
#             hours = ""  # Example; adjust as needed
#             #price = ""  # Example; adjust as needed
#             paid = ""  # Example; adjust as needed

#             # Append the formatted row to the formatted_data
#             formatted_data.append([
#                 date or "", 
#                 studio, 
#                 artist_name, 
#                 engineer, 
#                 engineer_name, 
#                 referral, 
#                 hours, 
#                 price, 
#                 paid
#             ])

#         return formatted_data

#     def extract_date(self, start):
#         """
#         Extracts the date from the event's start field.
        
#         Args:
#             start (str): The event's start time (datetime string).
        
#         Returns:
#             str: The event date in 'YYYY-MM-DD' format.
#         """
#         if isinstance(start, str):
#             # If 'start' is a string, assume it's an ISO 8601 datetime string
#             try:
#                 # Extract just the date part from the datetime string (e.g., '2024-12-15')
#                 return start.split('T')[0]
#             except Exception as e:
#                 print(f"Error parsing start date: {e}")
#                 return ""
#         return ""  # Default return in case of unexpected data format

#     def format_artist_name(self, summary):
#         """
#         Extracts the artist's name from the event summary.
        
#         If the summary starts with 'session w/', it returns the name after 'session w/'.
#         If the summary starts with 'rehearsal w/' it returns the name after 'rehearsal w/'.
#         If the summary contains a colon ':', it returns the part before the colon.
#         Otherwise, it returns the entire summary.
        
#         Args:
#             summary (str): The event summary.

#         Returns:
#             str: The formatted artist name.
#         """
#         if not summary:
#             return ""
        
#         # Check if summary starts with 'session w/' (case-insensitive)
#         session_match = re.match(r"session w/\s*(.+)", summary, re.IGNORECASE)
#         if session_match:
#             return session_match.group(1).strip()

#         #check if summary starts with 'rehearsal w/' (case-insensitive)
#         session_match = re.match(r"rehearsal w/\s*(.+)", summary, re.IGNORECASE)
#         if session_match:
#             return session_match.group(1).strip()
        
#         # Check if summary contains a colon ':'
#         if ':' in summary:
#             return summary.split(':', 1)[0].strip()
        
#         # If none of the above, return the entire summary
#         return summary.strip()


#     def format_engineer(self, description):
#         """
#         Formats the description by extracting potential engineer for sessions
        
#         Args:
#             description (str): the event description, which may contain engineer name and pricing

#         Returns:
#             tuple:
#                 - engineer (str): "Y" if an engineer is present, otherwise "".
#                 - engineer_name (str): The name of the engineer if present, otherwise "".
#                 - price (str): the price of the session if present, otherwise "".
#         """

#         if not description:
#             return "","","" #empty fields for an empty description

#         #match1 first format: "<Name> <Price>"
#         match1 = re.match(r'^([A-Za-z]+)\s+(\d+)$', description)
#         if match1:
#             engineer_name = match1.group(1)
#             price = match1.group(2)
#             return "Y", engineer_name, price

#         #match2 second format: "<Price> <Name>"
#         match2 = re.match(r'^(\d+)\s+([A-Za-z]+)$', description)
#         if match2:
#             price = match2.group(1)
#             engineer_name = match2.group(2)
#             return "Y", engineer_name, price

#         return "", "", ""
