import gspread
from google.oauth2.service_account import Credentials

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT =gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('love_sandwiches')

def get_sales_data():
    """
    Get sales figures input from user
    """

    while True:

        print("Please enter your sales data from the last market")
        print("Data should be 6 numbers seperated by a comma")
        print("Example: 10,20,30,40,50,60\n")

        data_str = input("Enter your data here:\n")

        sales_data = data_str.split(",")
        

        if validate_data(sales_data):
            print('Data is valid')
            break

    return sales_data

def validate_data(values):
    """
    Inside the try, converts all string values to integers. Raises ValueError if string cannot be converted into int, or if there aren't exatly 6 values
    """

    try:
        [int(value) for value in values]
        if len(values) !=6:
            raise ValueError(
                f"Exactly 6 values required, you provided {len(values)}"
            )
    except ValueError as e:
        print(f"Invalid data: {e}, please try again.\n")
        return False

    return True

def update_worksheet(data, worksheet):
    """
    Receives a list of integers to be inserted into a worksheet
    Update the relevant worksheet with the data to be provided
    """
    print(f"Updating {worksheet} worksheet...\n")
    worksheet_to_update = SHEET.worksheet(worksheet)
    worksheet_to_update.append_row(data)
    print(f"{worksheet} worksheet updated succesfully\n")

def calculate_surplus_data(sales_row):
    """
    Compare sales with stock and calculate the surplus for each item type
    """
    print('Calculating surplus data...\n')
    stock =SHEET.worksheet('stock').get_all_values()
    # pprint(stock) prints out the entire stock sheet in a nice view
    stock_row = stock[-1]
    # print(f"stock row: {stock_row}")
    # print(f"Sales row: {sales_row}")
    surplus_data = []
    for stock, sales in zip(stock_row, sales_row):
        surplus = int(stock) - sales
        surplus_data.append(surplus)
    
    return surplus_data


def main():
    """
    Run all program functions
    """
    data = get_sales_data() 
    sales_data = [int(num) for num in data]
    update_worksheet(sales_data, "sales")
    new_surplus_data = calculate_surplus_data(sales_data)
    print(new_surplus_data)
    update_worksheet(new_surplus_data, "surplus")

print('Welcome to love sandwiches data automation')
main()


# sales = SHEET.worksheet('sales')
# data = sales.get_all_values()
# print(data)
# Use tabulate to format the data into a table
# table = tabulate(data, headers="firstrow", tablefmt="grid")
# print(table)