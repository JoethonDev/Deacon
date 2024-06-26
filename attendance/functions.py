import gspread
from datetime import date
from google.oauth2.service_account import Credentials

SHEET_ID = "1v6oAU41-x2fEhgHfIVva7Dzcm3pqMiH9ed47XMWX3OM"
API_KEY = "AIzaSyB3MA7LIcORdNPONzKtSRy6rxYMyqBt7C4"

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets"
]

def index_to_column_letter(index):
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

def open_sheet():
    client = authorize_sheet()
    workbook = client.open_by_key(SHEET_ID)
    return workbook.sheet1

def get_names():
    sheet = open_sheet()
    return sheet.col_values(1)[1:]

def find_next_col(sheet):
    col_index = len(sheet.get_all_values()[0]) + 1
    return index_to_column_letter(col_index)

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


def save_attendence(names: list, attendance_day: str):
    if not (names and attendance_day):
        raise Exception("Missing Data!")

    sheet = open_sheet()
    col = find_next_col(sheet) # B

    records = [
        {
            "range" : f"{col}1",
            "values" : [[attendance_day]]
        },
        *build_name_batch(sheet, col, names)
    ]

    try :
        sheet.batch_update(records)
    except :
        raise Exception("Something went wrong!")
    
    return "Attendance is saved successfully"

# names = [
#     "جورج عادل",
#     "كاراس ثروت",
#     "بيشوي جرجس",
#     "مينا زكي",
#     "كيرلس حارس",
#     "توماس حارس",
#     'جيلانيا مجدي',
#     'مارلي سمير',
#     'ميرولا وجدي',
#     'ساندي عماد',
#     'مريم مدحت',
#     'كيفين مدحت',
#     'كيفن هاني',
#     'دانيال يوحنا'

# ]
# current = date.today().strftime("%d/%m/%Y")
# records = save_attendence(names, current)
# print(records)