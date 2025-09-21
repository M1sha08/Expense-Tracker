""" utils.py """

from datetime import datetime

def is_valid_int(value) -> bool:
  try:
    int(value)
    return True
  except ValueError:
    return False

def is_valid_float(value) -> bool:
  try:
    float(value)
    return True
  except ValueError:
    return False

def is_valid_date(value) -> bool:
  try:
    datetime.strptime(value, "%Y-%m-%d")
    return True
  except ValueError:
    return False

def list_expenses(expenses): # Might not use it, but better just to keep it anyway
  
  id_space = 1
  amount_space = 1
  category_space = 1
  date_space = 1

  print(f"\n{'ID':<{id_space}} - {'Amount':<{amount_space}} - {'Category':<{category_space}} - {'Date':<{date_space}} - Description")
  print('-'*100)

  for expense in expenses:
    expense_id, amount, category, date, description = expense
    print(f"{expense_id:<{id_space}} | {amount:<{amount_space}} | {category:<{category_space}} | {date:<{date_space}} | {description}")


  input("Press any button to go back to menu.")