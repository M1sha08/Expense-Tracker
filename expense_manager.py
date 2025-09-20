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
          database.create_expense(amount=amount_value, category=category, date=date, description=description)
          print("Expense successfully added.")
          break
      else:
        print("Amount must be positive number!")
    except ValueError:
      print("Amount must be a valid number!")


def edit_expense():
  while True:

    options = [
      {"num": 1, "desc": "View Expenses (To check Expense's ID)"},
      {"num": 2, "desc": "Edit Expense"},
      {"num": 3, "desc": "Cancel (Go back to menu)"}
    ]
    
    for option in options:
      print(f"{option.get('num')}. {option.get('desc')}")

    users_option = input("Choose an option: ").strip()
    
    if utils.is_valid_int(users_option):
      users_option = int(users_option)

      for option in options:
        if users_option == option.get('num'):

          if users_option == 1 or users_option == 2:
            if users_option == 1:
              view_expenses()
            while True:
              choosen_id = input("Choose an ID of expense you'd like to edit: ").strip()
              if utils.is_valid_int(choosen_id):
                if database.check_expense_exists(choosen_id):
                  expense_id, amount, category, date, description = database.get_expense(choosen_id)

                  print()
                  print("You can edit only the Amount, Category or Description of the choosen Expense.")
                  print(f"Expense (ID: {expense_id} - Amount: {amount} - Category: {category} - Date: {date} - Description: {description})")

                  print()
                  new_amount = input("New Amount (Leave it empty and press 'Enter' to not change anything): ").strip()
                  new_category = input("New Category (Leave it empty and press 'Enter' to not change anything): ").strip()
                  new_description = input("New Description (Leave it empty and press 'Enter' to not change anything): ").strip()
                  
                  if not new_amount:
                    new_amount = amount

                  if not new_category:
                    new_category = category
                  
                  if not new_description:
                    new_description = description
                  
                  database.update_expense(expense_id=expense_id ,new_amount=new_amount, new_category=new_category, new_description=new_description)
                  
                  expense_id, amount, category, date, description = database.get_expense(choosen_id)
                  print(f"\nUpdated Expense (ID: {expense_id} - Amount: {amount} - Category: {category} - Date: {date} - Description: {description})")
                  
                  input("Press anything to go back to the menu: ")
                  break
                else: print("Expense doesn't exists!")
              print(f"{choosen_id} is not valid number!")
          return
        
      print("Invalid option!")
    else: print("Option must be an valid number!")
  
def delete_expense():
  print("delete")

def view_expenses():
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
    print("-"*100)
