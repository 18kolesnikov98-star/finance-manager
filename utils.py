import re
from datetime import datetime


def validate_date(date_str: str) -> bool:
    """Проверяет, что строка имеет формат ГГГГ-ММ-ДД и является корректной датой"""
    pattern = r"^\d{4}-\d{2}-\d{2}$"
    if not re.match(pattern, date_str):
        return False
    
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
        return True
    except ValueError:
        return False


def get_date_input(prompt: str) -> str:
    """Запрашивает дату у пользователя до тех пор, пока она не станет корректной"""
    while True:
        date_str = input(prompt)
        if validate_date(date_str):
            return date_str
        print("❌ Неверный формат даты. Используйте ГГГГ-ММ-ДД (например, 2024-12-31)")


def get_float_input(prompt: str) -> float:
    """Запрашивает число с плавающей точкой"""
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print(" Введите число (например, 1500.50)")
