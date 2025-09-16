def is_valid_int(value) -> bool:
  try:
    int(value)
    return True
  except ValueError:
    return False