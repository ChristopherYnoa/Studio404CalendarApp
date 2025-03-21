import tkinter as tk
from tkinter import messagebox
from datetime import datetime
from FormatterNode import FormatterNode
from CalendarNode import get_calendar_data
from SheetNode import write_data_to_sheet, get_sheets_service, create_sheet_if_not_exists

def process_pipeline(start_date, end_date):
    """
    Executes the pipeline: fetch, format, and write data.
    
    Args:
        start_date (str): Start date in YYYY-MM-DD format
        end_date (str or None): End date in YYYY-MM-DD format
    """
    try:
        # Fetch calendar data (now using both hard-coded calendars)
        raw_data = get_calendar_data(start_date, end_date)
        
        # Format data
        formatter = FormatterNode()
        formatted_data = formatter.format_data(raw_data)
        
        # Write data to Google Sheets
        service = get_sheets_service()
        spreadsheet_id = "19GpFb5B8SaVqjgqkBGrytiCzwU6D1PIiqnRrw_Qrmcg"  # Replace with your actual spreadsheet ID
        
        # Create sheet name with date range - handle None values properly
        if end_date:
            sheet_name = f"{start_date}_{end_date}_combined"
        else:
            sheet_name = f"{start_date}_EOM_combined"
        
        # Create sheet and write data
        if create_sheet_if_not_exists(service, spreadsheet_id, sheet_name):
            # Debug print statement
            print(f"Formatted data (first 2 entries):\n{formatted_data[:2]}")
            write_data_to_sheet(service, spreadsheet_id, sheet_name, formatted_data)
        
        print("Pipeline executed successfully.")
        messagebox.showinfo("Success", "Data from both calendars processed and written to sheet!")
    except Exception as e:
        print(f"An error occurred: {e}")
        messagebox.showerror("Error", f"An error occurred: {e}")

def run_gui():
    """
    Launches the GUI for date input.
    """
    def on_submit():
        start_date = start_date_entry.get().strip()
        end_date = end_date_entry.get().strip()
        
        # Validate date format
        try:
            datetime.strptime(start_date, "%Y-%m-%d")
            if end_date:
                datetime.strptime(end_date, "%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Invalid Date", "Please enter dates in YYYY-MM-DD format.")
            return
        
        # Set end_date to None if it's empty
        if not end_date:
            end_date = None
        
        # Execute the pipeline
        process_pipeline(start_date, end_date)
    
    # Create the main window
    root = tk.Tk()
    root.title("Calendar Processing Tool")
    
    # Input fields for dates
    tk.Label(root, text="Start Date (YYYY-MM-DD):").grid(row=0, column=0, padx=10, pady=10)
    start_date_entry = tk.Entry(root)
    start_date_entry.grid(row=0, column=1, padx=10, pady=10)
    
    tk.Label(root, text="End Date (YYYY-MM-DD):").grid(row=1, column=0, padx=10, pady=10)
    end_date_entry = tk.Entry(root)
    end_date_entry.grid(row=1, column=1, padx=10, pady=10)
    
    # Add an information label about the calendars
    info_label = tk.Label(root, text="This tool will process events from both your primary\nand secondary calendars automatically.")
    info_label.grid(row=2, column=0, columnspan=2, padx=10, pady=5)
    
    # Submit button
    submit_button = tk.Button(root, text="Process Calendars", command=on_submit, bg="#4CAF50", fg="white")
    submit_button.grid(row=3, column=0, columnspan=2, pady=20)
    
    root.mainloop()

if __name__ == "__main__":
    run_gui()