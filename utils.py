from datetime import datetime

def is_valid_int(value) -> bool:
  try:
    int(value)
    return True
  except ValueError:
    return False
  

def is_valid_date(value) -> bool:
  try:
    datetime.strptime(value, "%Y-%m-%d")
    return True
  except ValueError:
    return False

def list_expenses(expenses): # Migh not use it, but better just keep it anyway
  
  ID_SPACE = 1
  AMOUNT_SPACE = 1
  CATEGORY_SPACE = 1
  DATE_SPACE = 1

  print(f"\n{'ID':<{ID_SPACE}} - {'Amount':<{AMOUNT_SPACE}} - {'Category':<{CATEGORY_SPACE}} - {'Date':<{DATE_SPACE}} - Description")
  print('-'*100)

  for expense in expenses:
    expense_id, amount, category, date, description = expense
    print(f"{expense_id:<{ID_SPACE}} | {amount:<{AMOUNT_SPACE}} | {category:<{CATEGORY_SPACE}} | {date:<{DATE_SPACE}} | {description}")


  input("Press any button to go back to menu.")