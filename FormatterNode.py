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
            # Extract fields, use None or blank space for missing fields
            date = event.get("date", None)
            studio = event.get("studio", None)
            artist_name = event.get("artist_name", None)
            engineer = event.get("engineer", None)
            engineer_name = event.get("engineer_name", None)
            referral = event.get("referral", None)
            hours = event.get("hours", None)
            price = event.get("price", None)
            paid = event.get("paid", None)

            # Append row to formatted data
            formatted_data.append([
                date or "", 
                studio or "", 
                artist_name or "", 
                engineer or "", 
                engineer_name or "", 
                referral or "", 
                hours or "", 
                price or "", 
                paid or ""
            ])

        return formatted_data

# Example usage
if __name__ == "__main__":
    formatter = FormatterNode()
    # raw_calendar_data = [
    #     {"date": "2024-12-21", "studio": "Studio B", "artist_name": "John Doe", "engineer": "Y", 
    #      "engineer_name": "John", "referral": "John", "hours": "3", "price": "150", "paid": "Y"},
    #     {"date": "2024-12-22", "studio": "Studio A", "artist_name": "Jane Smith"}  # Missing fields
    # ]
    # formatted_output = formatter.format_data(raw_calendar_data)
    # for row in formatted_output:
    #     print(row)
