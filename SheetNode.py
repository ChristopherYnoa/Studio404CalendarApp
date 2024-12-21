import gspread
from google.oauth2.service_account import Credentials

scopes = ["https://www.googleapis.com/auth/spreadsheets"]
creds = Credentials.from_service_account_file("credentials-sheets.json", scopes=scopes)
client = gspread.authorize(creds)

#unique identification for the sheet connected to the API
sheet_id = "19GpFb5B8SaVqjgqkBGrytiCzwU6D1PIiqnRrw_Qrmcg"
workbook = client.open_by_key(sheet_id)

values_list = workbook.sheet1.row_values(1)

print(values_list)

values = [
    ["Name", "Price", "Quantity"],
    ["Basketball", 29.99, 1],
    ["Jeans", 39.99, 4],
    ["Soap", 7.99, 3],
]

worksheet_list = map(lambda x: x.title, workbook.worksheets())
new_worksheet_name = "Values"

if new_worksheet_name in worksheet_list:
    sheet = workbook.worksheet(new_worksheet_name)
else:
    sheet = workbook.add_worksheet(new_worksheet_name, rows=10, cols=10)

sheet.clear()

sheet.update(f"A1:C{len(values)}", values)

sheet.update_cell(len(values) + 1, 2, "=sum(B2:B4)")
sheet.update_cell(len(values) + 1, 3, "=sum(C2:C4)")

sheet.format("A1:C1", {"textFormat": {"bold": True}})