import sqlite3
import os

DB_NAME = os.path.join("Expense Tracker (CLI)", "expenses.db")

def get_connection():
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


def create_expense(amount, category, date, description):
  connection = get_connection()
  cursor = connection.cursor()
  cursor.execute(
    "INSERT INTO expenses (amount, category, date, description) VALUES (?, ?, ?, ?)",
    (amount, category, date, description)
  )
  connection.commit()
  connection.close()


def update_expense(expense_id, new_amount, new_category, new_description):
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
  

def get_expenses() -> list:
  connection = get_connection()
  cursor = connection.cursor()
  cursor.execute("SELECT id, amount, category, date, description FROM expenses")
  rows = cursor.fetchall()
  connection.close()
  return rows

def check_expense_exists(expense_id) -> bool:
  connection = get_connection()
  cursor = connection.cursor()
  cursor.execute("SELECT 1 FROM expenses WHERE id = ?", (expense_id,))
  exists = cursor.fetchone() is not None
  connection.close()
  return exists 

def get_expense(expense_id):
  connection = get_connection()
  cursor = connection.cursor()
  cursor.execute("SELECT id, amount, category, date, description FROM expenses WHERE id = ?", (expense_id,))
  expense = cursor.fetchone()
  connection.close()
  return expense