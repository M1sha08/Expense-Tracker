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
    description TEXT,
    date TEXT
  )
  """)

  connection.commit()
  connection.close()


def add_expense(amount, category, date, description):
  connection = get_connection()
  cursor = connection.cursor()
  cursor.execute(
    "INSERT INTO expenses (amount, category, date, description) VALUES (?, ?, ?, ?)",
    (amount, category, date, description)
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