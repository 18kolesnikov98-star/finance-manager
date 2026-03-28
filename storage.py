import json
import os
from typing import List
from models import Transaction, FinanceManager

DATA_FILE = "data/transactions.json"


def save_data(manager: FinanceManager) -> None:
    """Сохраняет все транзакции в JSON-файл"""
    # Создаём папку data, если её нет
    os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
    
    # Преобразуем транзакции в список словарей
    data = [t.to_dict() for t in manager.transactions]
    
    # Сохраняем в файл
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def load_data(manager: FinanceManager) -> None:
    """Загружает транзакции из JSON-файла"""
    if not os.path.exists(DATA_FILE):
        return
    
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    # Преобразуем словари обратно в объекты Transaction
    manager.transactions = [Transaction.from_dict(item) for item in data]
