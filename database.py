""" database.py """

import sqlite3

DB_NAME = "expenses.db"

def get_connection() -> sqlite3.Connection:
  return sqlite3.connect(DB_NAME)

def init_db():
  connection = get_connection()
  cursor = connection.cursor()
  cursor.execute("""
  CREATE TABLE IF NOT EXISTS expenses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    amount REAL,
    category TEXT,
    date TEXT,
    description TEXT
  )
  """)

  connection.commit()
  connection.close()


def create_expense(amount, category, date, description) -> None:
  connection = get_connection()
  cursor = connection.cursor()
  cursor.execute(
    "INSERT INTO expenses (amount, category, date, description) VALUES (?, ?, ?, ?)",
    (amount, category, date, description)
  )
  connection.commit()
  connection.close()


def update_expense(expense_id, new_amount, new_category, new_description) -> None:
  connection = get_connection()
  cursor = connection.cursor()
  cursor.execute(
    """ 
    UPDATE expenses
    SET amount = ?, category = ?, description = ?
    WHERE id = ?
    """,
    (new_amount, new_category, new_description, expense_id)
  )
  connection.commit()
  connection.close()
  

def delete_expense(expense_id) -> None:
  connection = get_connection()
  cursor = connection.cursor()
  cursor.execute("DELETE FROM expenses WHERE id = ?", (expense_id,))
  connection.commit()
  connection.close()

def get_all_expenses(by_category=None, category=None) -> list:
  connection = get_connection()
  cursor = connection.cursor()
  if by_category:
    cursor.execute("SELECT * FROM expenses WHERE category = ?", (category,))
  else: cursor.execute("SELECT * FROM expenses")
  rows = cursor.fetchall()
  connection.close()
  return rows

def expense_existence_validation(by_id=None, by_amount=None, by_date=None, by_category=None,
                         expense_id=None, expense_amount=None, expense_date=None, expense_category=None) -> bool:
  vds = [
    {"trigger": by_id, "by_value": 'id', "value": expense_id},
    {"trigger": by_amount, "by_value": 'amount', "value": expense_amount},
    {"trigger": by_date, "by_value": 'date', "value": expense_date},
    {"trigger": by_category, "by_value": 'category', "value": expense_category},
  ]
  by_value = None
  value = None
  for vd in vds:
    if vd['trigger']:
      by_value = vd['by_value']
      value = vd['value']
      break

  if not by_value:
    return False

  connection = get_connection()
  cursor = connection.cursor()
  cursor.execute(f"SELECT 1 FROM expenses WHERE {by_value} = ?", (value,))
  exists = cursor.fetchone() is not None
  connection.close()
  return exists 

def get_expense(by_id=None, by_amount=None, by_date=None, by_category=None,
                expense_id=None, expense_amount=None, expense_date=None, expense_category=None):

  vds = [
    {"trigger": by_id, "by_value": 'id', "value": expense_id},
    {"trigger": by_amount, "by_value": 'amount', "value": expense_amount},
    {"trigger": by_date, "by_value": 'date', "value": expense_date},
    {"trigger": by_category, "by_value": 'category', "value": expense_category},
  ]
  by_value = None
  value = None
  for vd in vds:
    if vd['trigger']:
      by_value = vd['by_value']
      value = vd['value']
      break

  if not by_value:
    return None

  connection = get_connection()
  cursor = connection.cursor()
  query = f"SELECT id, amount, category, date, description FROM expenses WHERE {by_value} = ?"
  cursor.execute(query, (value,))
  expense = cursor.fetchone()
  connection.close()
  return expense

def search_expense_by_range(min_value, max_value, by_id = None, by_amount=None,
                            by_date=None ,by_category=None) -> list:

  vds = [
      {"trigger": by_id, "value": "id"},
      {"trigger": by_amount, "value": "amount"},
      {"trigger": by_date, "value": "date"},
      {"trigger": by_category, "value": "category"},
  ]

  by_value = None
  for vd in vds:
      if vd['trigger']:
          by_value = vd['value']
          break

  if not by_value:
      return []

  connection = get_connection()
  cursor = connection.cursor()

  query = f"SELECT * FROM expenses WHERE {by_value} BETWEEN ? AND ?"
  cursor.execute(query, (min_value, max_value))

  rows = cursor.fetchall()
  connection.close()
  return rows