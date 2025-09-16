import expense_manager
import utils


def show_menu() -> None:
  print(f"{'Menu':_^18}")

  print("1. Add Expense\n" \
  "2. Edit Expense\n" \
  "3. Delete Expense\n" \
  "4. View Expenses\n" \
  "5. Quit Program")


def check_option(option) -> bool:
  if not utils.is_valid_int(option):
    return False
  option = int(option)

  if 1 <= option <= 5:
    return True
  
  return False
  

def execute_command(option) -> None:
  commands = [
    {"number": 1, "action": expense_manager.add_expense},
    {"number": 2, "action": expense_manager.edit_expense},
    {"number": 3, "action": expense_manager.delete_expense},
    {"number": 4, "action": expense_manager.show_expenses},
  ]

  option = int(option)
  for command in commands:
    if int(option) == command.get('number'):
      command['action']()


def main() -> None:
  running = True
  while running:
    show_menu()

    users_option = input('Choose an option (Enter number): ').strip()
    if check_option(users_option):
      if int(users_option) == 5:
        running = False
      execute_command(users_option)
    else:
      print("Invalid option!")


if __name__ == "__main__":
  main()