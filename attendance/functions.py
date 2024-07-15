import gspread
from datetime import date
from google.oauth2.service_account import Credentials

SHEET_ID = "1v6oAU41-x2fEhgHfIVva7Dzcm3pqMiH9ed47XMWX3OM"
API_KEY = "AIzaSyB3MA7LIcORdNPONzKtSRy6rxYMyqBt7C4"

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets"
]

def index_to_letter(index):
    letter = ""
    while index:
        mod = index % 26
        letter += chr(mod + 65 - 1)
        index = index // 26
    return letter

def authenticate_sheet():
    return Credentials.from_service_account_file("credentials.json", scopes=SCOPES)

def authorize_sheet():
    creds = authenticate_sheet()
    return gspread.authorize(creds)

def open_workbook():
    client = authorize_sheet()
    return client.open_by_key(SHEET_ID)

def open_sheet(name=None):
    workbook = open_workbook()
    if not name:
        return workbook.sheet1
    return workbook.worksheet(name)

def get_names(sheet_name):
    sheet = open_sheet(sheet_name)
    return sheet.col_values(1)[1:]

def get_worksheets_names():
    workbook = open_workbook()
    return [worksheet.title for worksheet in workbook.worksheets()]

def find_date_col(sheet, date):
    value = sheet.find(date)
    if value:
        return index_to_letter(value.col)
    return value

def find_next_col(sheet):
    col_index = len(sheet.get_all_values()[0]) + 1
    return index_to_letter(col_index)

def find_next_row(sheet):
    row_index = len(sheet.get_all_values()) + 1
    return row_index

def build_name_batch(sheet, col, names):
    batch = []
    for name in names :
        try :
            row_index = sheet.find(name).row
            row = col + str(row_index)
            data = {
                "range" : f"{row}",
                "values" : [["+"]]
            }
            batch.append(data)
        except :
            print(f"Error with name : {name}")
    return batch

def update_sheet(sheet, records):
    try :
        sheet.batch_update(records)
    except Exception as e:
        print(e)
        raise Exception("Something went wrong!")

def create_worksheet(sheet_name: str):
    workbook = open_workbook()
    sheet = workbook.add_worksheet(sheet_name, 1000, 26)
    record = [
        {
            "range" : "A1",
            "values" : [["Name"]]
        }
    ]
    try :
        update_sheet(sheet, record)
    except Exception as e:
        print(e)
        raise e
    return "New Class is added successfully!"

def save_attendence(names: list, attendance_day: str, sheet_name: str):
    if not (names and attendance_day):
        raise Exception("Missing Data!")

    sheet = open_sheet(sheet_name)
    col = find_date_col(sheet, attendance_day)
    if not col:
        col = find_next_col(sheet) # B

    records = [
        {
            "range" : f"{col}1",
            "values" : [[attendance_day]]
        },
        *build_name_batch(sheet, col, names)
    ]

    try :
        update_sheet(sheet, records)
    except Exception as e:
        raise e
    
    return "Attendance is saved successfully"

def add_name(name: str, sheet_name: str):
    if not name:
        raise Exception("Missing Data!")
    
    names = get_names(sheet_name)
    if name in names:
        raise Exception("Name exists already")

    sheet = open_sheet(sheet_name)
    row = find_next_row(sheet)
    
    records = [
        {
            "range" : f"A{row}",
            "values" : [[name]]
        }
    ]

    try :
        update_sheet(sheet, records)
    except Exception as e:
        print(e)
        raise e
    
    return "Name is added successfully"