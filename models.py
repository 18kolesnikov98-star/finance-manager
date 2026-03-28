from datetime import datetime
from dataclasses import dataclass, asdict
from typing import List

@dataclass
class Transaction:
    """Класс для хранения информации о транзакции"""
    amount: float          # сумма (положительная - доход, отрицательная - расход)
    category: str          # категория (еда, транспорт, зарплата и т.д.)
    description: str       # описание
    date: str              # дата в формате ГГГГ-ММ-ДД
    type: str              # "income" или "expense"
    
    def to_dict(self) -> dict:
        """Преобразует транзакцию в словарь для сохранения в JSON"""
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Transaction':
        """Создаёт транзакцию из словаря"""
        return cls(**data)


class FinanceManager:
    """Класс для управления финансами"""
    
    def __init__(self):
        self.transactions: List[Transaction] = []
    
    def add_transaction(self, amount: float, category: str, description: str, date: str, type: str)-> None:
        """Добавляет новую транзакцию"""
        transaction = Transaction(amount, category, description, date, type)
        self.transactions.append(transaction)
    
    def get_balance(self) -> float:
        """Возвращает текущий баланс (доходы - расходы)"""
        balance = 0
        for t in self.transactions:
            if t.type == "income":
                balance += t.amount
            else:
                balance -= t.amount
        return balance
    
    def get_income_total(self) -> float:
        """Возвращает сумму всех доходов"""
        return sum(t.amount for t in self.transactions if t.type == "income")
    
    def get_expense_total(self) -> float:
        """Возвращает сумму всех расходов"""
        return sum(t.amount for t in self.transactions if t.type == "expense")
    
    def filter_by_category(self, category: str) -> List[Transaction]:
        """Фильтрует транзакции по категории"""
        return [t for t in self.transactions if t.category.lower() == category.lower()]
    
    def filter_by_date_range(self, start_date: str, end_date: str) -> List[Transaction]:
        """Фильтрует транзакции по диапазону дат"""
        return [t for t in self.transactions if start_date <= t.date <= end_date]
    
    def get_categories(self) -> dict:
        """Возвращает статистику по категориям"""
        stats = {}
        for t in self.transactions:
            if t.category not in stats:
                stats[t.category] = {"income": 0, "expense": 0}
            if t.type == "income":
                stats[t.category]["income"] += t.amount
            else:
                stats[t.category]["expense"] += t.amount
        return stats
