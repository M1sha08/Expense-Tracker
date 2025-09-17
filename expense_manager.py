import database
import utils

database.init_db()

def add_expense():
  valid = False
  print("Enter required information to create an expense.")
  
  while True:
    amount = input("Amount: ").strip()
    try:
      amount_value = float(amount)
      if amount_value > 0:
        category = input("Category: ").strip()
        description = input("Description: ").strip()
        
        if not category:
          category = "Empty"
        
        if not description:
          description = "Empty"

        while True:
          date = input("Date - YYYY-MM-DD: ")
          if utils.is_valid_date(date):
            valid = True
            break
          print("Invalid date!")
        
        if valid == True:
          database.add_expense(amount=amount_value, category=category, date=date, description=description)
          break
      else:
        print("Amount must be positive number!")
    except ValueError:
      print("Amount must be a valid number!")


def edit_expense():
  print("edit")
  
def delete_expense():
  print("delete")

def show_expenses():
  expenses = database.get_expenses()
  
  ID_SPACE = 3
  AMOUNT_SPACE = 5
  CATEGORY_SPACE = 10
  DATE_SPACE = 10

  print(f"\nID - Amount - Date - Description")
  print('-'*100)

  for expense in expenses:
    expense_id, amount, category, date, description = expense
    print(f"{expense_id} - {amount} - {category} - {date} - {description}")


  input("Press any button to go back to menu.")