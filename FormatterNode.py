class FormatterNode:
    """
    FormatterNode processes raw calendar data into the expected format for SheetNode.
    Unknown fields are filled with None or blank spaces.
    """
    
    def __init__(self):
        self.template = ["Date", "Studio", "Artist Name", "Engineer?", "Engineer Name", "Referral", "Hours", "Price", "Paid?"]

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

            # Format the date (this will handle the datetime case and provide just the date)
            date = self.extract_date(start)
            
            # Map summary and description to the columns as needed
            # Here you could make assumptions about which fields these correspond to.
            # Adjust according to your logic.

            # For simplicity, I am putting the 'summary' as the "Artist Name" and 'description' as the "Referral"
            # You can modify these mappings to match your actual requirements.
            artist_name = summary or ""
            referral = description or ""
            
            # Add empty values for other fields (e.g., "Studio", "Engineer?") if they're not available
            studio = "B"  # Example; adjust as needed
            engineer = ""  # Example; adjust as needed
            engineer_name = ""  # Example; adjust as needed
            hours = ""  # Example; adjust as needed
            price = ""  # Example; adjust as needed
            paid = ""  # Example; adjust as needed

            # Append the formatted row to the formatted_data
            formatted_data.append([
                date or "", 
                studio, 
                artist_name, 
                engineer, 
                engineer_name, 
                referral, 
                hours, 
                price, 
                paid
            ])

        return formatted_data

    def extract_date(self, start):
        """
        Extracts the date from the event's start field.
        
        Args:
            start (str): The event's start time (datetime string).
        
        Returns:
            str: The event date in 'YYYY-MM-DD' format.
        """
        if isinstance(start, str):
            # If 'start' is a string, assume it's an ISO 8601 datetime string
            try:
                # Extract just the date part from the datetime string (e.g., '2024-12-15')
                return start.split('T')[0]
            except Exception as e:
                print(f"Error parsing start date: {e}")
                return ""
        return ""  # Default return in case of unexpected data format


