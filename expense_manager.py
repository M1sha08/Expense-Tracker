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
        
        if not category:
          category = "Empty"

        while True:
          date = input("Date - YYYY-MM-DD: ")
          if utils.is_valid_date(date):
            valid = True
            break
          print("Invalid date!")

        description = input("Description: ").strip()

        if not description:
          description = "Empty"

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
                if database.expense_existence_validation(by_id=True, expense_id=chosen_id):
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
  print()
  while True:
    options = [
      {"num": 1, "desc": "View Expenses and Delete (To check Expense's ID)"},
      {"num": 2, "desc": "Delete Expense"},
      {"num": 3, "desc": "Cancel (Go back to menu)"}
    ]

    for option in options:
      print(f"{option['num']}. {option['desc']}")

    users_option = input("Choose an option: ").strip()

    if not utils.is_valid_int(users_option):
      print("Option must be a valid number!")
      continue

    users_option = int(users_option)

    if users_option == 3:
      return  # cancel, exit function

    if users_option in (1, 2):
      if users_option == 1:
        view_expenses()

      chosen_id = input("Choose an ID of the expense you'd like to delete: ").strip()
      if not utils.is_valid_int(chosen_id):
        print("ID must be a valid number!")
        continue

      chosen_id = int(chosen_id)

      if not database.expense_existence_validation(by_id=True, expense_id=chosen_id):
        print(f"Expense with ID {chosen_id} doesn't exist!")
        continue

      # Confirm deletion
      while True:
        y_n = input("Are you sure? (Yes/No): ").strip().lower()
        if y_n == "yes":
          expense_id, *_ = database.get_expense(by_id=True, expense_id=chosen_id)
          database.delete_expense(expense_id=expense_id)
          print(f"Expense with ID {expense_id} deleted successfully.")
          return
        elif y_n == "no":
          return
        else:
          print("Invalid option, type Yes or No.")

    else:
      print("Invalid option!")

def view_expenses(pause=None) -> None:
  expenses = database.get_all_expenses()


  print(f"\nID - Amount - Category - Date - Description")
  print('-'*100)

  for expense in expenses:
    expense_id, amount, category, date, description = expense
    print(f"{expense_id} - {amount} - {category} - {date} - {description}")
    print("-"*100)

  if pause:
    input("Press 'Enter' to go back to the menu: ")


def search_expense() -> None:
  options = [
    {"num": 1, "desc": "Search by ID", "action": search_by_id},
    {"num": 2, "desc": "Search by Date", "action": search_by_date},
    {"num": 3, "desc": "Search by Category", "action": search_by_category},
    {"num": 4, "desc": "Search by Amount", "action": search_by_amount},
    {"num": 5, "desc": "Cancel (Go back to menu)", "action": lambda: None},
  ]

  print()
  for option in options:
    print(f"{option.get('num')}. {option.get('desc')}")

  while True:
    users_option = input("Choose an option: ").strip()

    if utils.is_valid_int(users_option):
      users_option = int(users_option)
      for option in options:
        if users_option == option['num']:
          option['action']()
          break
      break
    else: print("Invalid option: option must be an valid number!")

def search_by_id():
  print("\nSearching by id")

  print("1. Search by exact ID")
  print("2. Search by ID range (e.g. 1 - 5)")

  while True:
    option = input("Choose an option: ").strip()

    if utils.is_valid_int(option):
      option = int(option)
      if option in [1,2]:
        break
      else:
        print("Invalid option")
    else:
      print("Chosen option must be an valid number!")

  if option == 1:
    while True:
      chosen_id = input("Expense ID: ").strip()

      if utils.is_valid_int(chosen_id):
        if database.expense_existence_validation(by_id=True, expense_id=chosen_id):
          expense_id, amount, category, date, description = database.get_expense(by_id=True, expense_id=chosen_id)
          print(f"\nExpense (ID: {expense_id} - Amount: {amount} - Category: {category} - Date: {date} - Description: {description})")
          break
        else: print(f"Expense with ID {chosen_id} doesn't exist!")
      else: print("Invalid ID: Must be an positive number!")

  if option == 2:
    while True:
      min_value = input("From which ID would you like to search (number)? ").strip()
      max_value = input("To which ID would you like to search? (number)? ").strip()

      if utils.is_valid_int(min_value) and utils.is_valid_int(max_value):
        min_value = int(min_value)
        max_value = int(max_value)
        expenses = database.search_expense_by_range(min_value=min_value, max_value=max_value, by_id=True)

        print()
        utils.list_expenses(expenses=expenses)

        break
      else:
        print("Invalid options!")

  input("Press 'Enter' to go back to the menu: ")

def search_by_date():
  print("\nSearching by date")

  print("1. Search by exact Date")
  print("2. Search by Date range (From a to b)")

  while True:
    option = input("Choose an option: ").strip()

    if utils.is_valid_int(option):
      option = int(option)
      if option in [1, 2]:
        break
    print("Invalid option!")

  if option == 1:
    print()
    while True:
      date_value = input("Expense exact Date - YYYY-MM-DD: ").strip()
      if utils.is_valid_date(date_value):
        if database.expense_existence_validation(by_date=True, expense_date=date_value):
          expense = database.get_expense(by_date=True, expense_date=date_value)
          id_value, amount, category, date, desc = expense
          print(f"ID: {id_value} - Amount: {amount} - Category: {category} - Date: {date}")
          break
        else: print(f"Expense with Date: {date_value} doesn't exist!")
      else: print("Incorrect value! Provide date like this - YYYY-MM-DD.")

  if option == 2:
    print()
    while True:
      from_value = input("From which Date would you like to search? (YYYY-MM-DD)? ").strip()
      to_value = input("To which Date? (YYYY-MM-DD)? ").strip()

      if utils.is_valid_date(from_value) and utils.is_valid_date(to_value):
        expenses = database.search_expense_by_range(min_value=from_value, max_value=to_value, by_date=True)

        if not expenses:
          print(f"No expenses found. ({from_value} - {to_value})")
          break

        print()
        utils.list_expenses(expenses=expenses)
        break
      else: print("Try again, both of the provided dates should look like - YYYY-MM-DD.")


def search_by_category():
  print("\nSearching by category")

  category_value = input("Enter a category: ").strip()

  expenses = database.get_all_expenses(by_category=True, category=category_value)
  utils.list_expenses(expenses=expenses)


def search_by_amount():
  print("\nSearching by amount")

  while True:
    from_amount = input("From what amount would you like to search? ").strip()
    to_amount = input("To what amount would you like to search? ").strip()

    if utils.is_valid_float(from_amount) and utils.is_valid_float(to_amount):
      expenses = database.search_expense_by_range(min_value=from_amount, max_value=to_amount, by_amount=True)
      utils.list_expenses(expenses=expenses)
      break
    else:
      print("Invalid value! Amount must be a number.")