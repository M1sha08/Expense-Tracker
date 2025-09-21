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


def create_expense(amount: float, category: str, date: str, description: str):
  connection = get_connection()
  cursor = connection.cursor()
  cursor.execute(
    "INSERT INTO expenses (amount, category, date, description) VALUES (?, ?, ?, ?)",
    (amount, category, date, description)
  )
  connection.commit()
  connection.close()


def update_expense(expense_id: int, new_amount: float, new_category: str, new_description: str):
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
  

def delete_expense(expense_id: int) -> None:
  connection = get_connection()
  cursor = connection.cursor()
  cursor.execute("DELETE FROM expenses WHERE id = ?", (expense_id,))
  connection.commit()
  connection.close()

def get_expenses() -> list:
  connection = get_connection()
  cursor = connection.cursor()
  cursor.execute("SELECT id, amount, category, date, description FROM expenses")
  rows = cursor.fetchall()
  connection.close()
  return rows

def check_expense_exists(expense_id: int) -> bool:
  connection = get_connection()
  cursor = connection.cursor()
  cursor.execute("SELECT 1 FROM expenses WHERE id = ?", (expense_id,))
  exists = cursor.fetchone() is not None
  connection.close()
  return exists 

def get_expense(expense_id: int):
  connection = get_connection()
  cursor = connection.cursor()
  cursor.execute("SELECT id, amount, category, date, description FROM expenses WHERE id = ?", (expense_id,))
  expense = cursor.fetchone()
  connection.close()
  return expense