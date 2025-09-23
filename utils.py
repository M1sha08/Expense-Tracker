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

def list_expenses(expenses):

  print(f"ID - Amount - Category - Date - Description")
  print('-'*100)

  for expense in expenses:
    expense_id, amount, category, date, description = expense
    print(f"{expense_id} - {amount} - {category:} - {date} - {description}")
    print('-'*100)
