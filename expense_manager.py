""" expenses_manager.py """

import database
import utils

database.init_db()

def add_expense() -> None:
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
        
        if valid:
          database.create_expense(amount=amount_value, category=category, date=date, description=description)
          print("Expense successfully added.")
          break
      else:
        print("Amount must be positive number!")

    except ValueError:
      print("Amount must be a valid number!")

def edit_expense() -> None:
  while True:

    options = [
      {"num": 1, "desc": "View Expenses and Edit (To check Expense's ID)"},
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
              chosen_id = input("Choose an ID of the expense you'd like to edit: ").strip()
              if utils.is_valid_int(chosen_id):
                if database.check_expense_exists(chosen_id):
                  expense_id, amount, category, date, description = database.get_expense(chosen_id)

                  print()
                  print("You can edit only the Amount, Category or Description of the chosen Expense.")
                  print(f"Expense (ID: {expense_id} - Amount: {amount} - Category: {category} - Date: {date} - Description: {description})")

                  while True:
                    print()
                    new_amount = input("New Amount (Leave it empty and press 'Enter' to not change anything): ").strip()
                    if not new_amount:
                      new_amount = amount
                      break
                    else:
                      if utils.is_valid_float(new_amount):
                        break
                      else:
                        print("Invalid amount! Please try again.")
                        continue

                  new_category = input("New Category (Leave it empty and press 'Enter' to not change anything): ").strip()
                  new_description = input("New Description (Leave it empty and press 'Enter' to not change anything): ").strip()


                  if not new_category:
                    new_category = category
                  
                  if not new_description:
                    new_description = description
                  
                  database.update_expense(expense_id=expense_id ,new_amount=new_amount, new_category=new_category, new_description=new_description)
                  
                  expense_id, amount, category, date, description = database.get_expense(chosen_id)
                  print(f"\nUpdated Expense (ID: {expense_id} - Amount: {amount} - Category: {category} - Date: {date} - Description: {description})")
                  
                  input("Press anything to go back to the menu: ")
                  break
                else: print(f"Expense with ID {chosen_id} doesn't exist!")
              else: print(f"{chosen_id} is not valid number!")
          return
        
      print("Invalid option!")
    else: print("Option must be an valid number!")
  
def delete_expense() -> None:
  while True:
    options = [
      {"num": 1, "desc": "View Expenses and Delete (To check Expense's ID)"},
      {"num": 2, "desc": "Delete Expense"},
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
              chosen_id = input("Choose an ID of the expense you'd like to delete: ").strip()
              if utils.is_valid_int(chosen_id):
                if database.check_expense_exists(chosen_id):
                  expense_id, *_ = database.get_expense(chosen_id)
                  database.delete_expense(expense_id=expense_id)
                  print(f"Expense with ID {expense_id} deleted successfully.")
                  break
                else: print(f"Expense with ID {chosen_id} doesn't exist!")
              else: print("ID must be a valid number!")
          return
      print("Invalid option!")
    else: print("Option must be an valid number!")


def view_expenses() -> None:
  expenses = database.get_expenses()


  print(f"\nID - Amount - Date - Description")
  print('-'*100)

  for expense in expenses:
    expense_id, amount, category, date, description = expense
    print(f"{expense_id} - {amount} - {category} - {date} - {description}")
    print("-"*100)
