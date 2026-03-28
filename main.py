import os
from models import FinanceManager
from storage import save_data, load_data
from utils import validate_date, get_date_input, get_float_input


def clear_screen():
    """Очищает экран консоли"""
    os.system('cls' if os.name == 'nt' else 'clear')


def print_menu():
    """Печатает главное меню"""
    print("\n" + "=" * 50)
    print("         МЕНЕДЖЕР ЛИЧНЫХ ФИНАНСОВ")
    print("=" * 50)
    print("1. Добавить доход")
    print("2. Добавить расход")
    print("3. Показать баланс")
    print("4. Показать все транзакции")
    print("5. Показать статистику по категориям")
    print("6. Фильтр по категории")
    print("7. Фильтр по диапазону дат")
    print("0. Выход и сохранение")
    print("-" * 50)


def add_income(manager: FinanceManager):
    """Добавляет доход"""
    print("\n📈 Добавление дохода")
    amount = get_float_input("Сумма: ")
    category = input("Категория (например, зарплата, подарок): ")
    description = input("Описание: ")
    date = get_date_input("Дата (ГГГГ-ММ-ДД): ")
    
    manager.add_transaction(amount, category, description, date, "income")
    print("✅ Доход добавлен!")


def add_expense(manager: FinanceManager):
    """Добавляет расход"""
    print("\n📉 Добавление расхода")
    amount = get_float_input("Сумма: ")
    category = input("Категория (например, еда, транспорт, интернет): ")
    description = input("Описание: ")
    date = get_date_input("Дата (ГГГГ-ММ-ДД): ")
    
    manager.add_transaction(amount, category, description, date, "expense")
    print("✅ Расход добавлен!")


def show_balance(manager: FinanceManager):
    """Показывает текущий баланс"""
    print("\n💰 БАЛАНС")
    print("-" * 30)
    print(f"📈 Всего доходов:   {manager.get_income_total():,.2f} ₽")
    print(f"📉 Всего расходов:  {manager.get_expense_total():,.2f} ₽")
    print(f"💵 Итоговый баланс: {manager.get_balance():,.2f} ₽")


def show_all_transactions(manager: FinanceManager):
    """Показывает все транзакции"""
    if not manager.transactions:
        print("\n📭 Нет транзакций. Добавьте доход или расход.")
        return
    
    print("\n📋 ВСЕ ТРАНЗАКЦИИ")
    print("-" * 70)
    print(f"{'Дата':<12} {'Тип':<8} {'Категория':<15} {'Сумма':>12} {'Описание'}")
    print("-" * 70)
    
    for t in manager.transactions:
        type_icon = "📈 ДОХОД" if t.type == "income" else "📉 РАСХОД"
        amount_str = f"+{t.amount:,.2f}" if t.type == "income" else f"-{t.amount:,.2f}"
        print(f"{t.date:<12} {type_icon:<8} {t.category:<15} {amount_str:>12} {t.description}")


def show_category_stats(manager: FinanceManager):
    """Показывает статистику по категориям"""
    stats = manager.get_categories()
    
    if not stats:
        print("\n📭 Нет данных для статистики.")
        return
    
    print("\n📊 СТАТИСТИКА ПО КАТЕГОРИЯМ")
    print("-" * 50)
    print(f"{'Категория':<15} {'Доходы':>12} {'Расходы':>12} {'Разница':>12}")
    print("-" * 50)
    
    for category, amounts in stats.items():
        income = amounts["income"]
        expense = amounts["expense"]
        diff = income - expense
        print(f"{category:<15} {income:>12,.2f} {expense:>12,.2f} {diff:>12,.2f}")


def filter_by_category(manager: FinanceManager):
    """Фильтрует транзакции по категории"""
    category = input("Введите категорию: ")
    filtered = manager.filter_by_category(category)
    
    if not filtered:
        print(f"\n📭 Нет транзакций в категории '{category}'.")
        return
    
    print(f"\n🔍 Транзакции в категории '{category}':")
    print("-" * 60)
    for t in filtered:
        icon = "📈" if t.type == "income" else "📉"
        print(f"  {icon} {t.date} | {t.description} | {t.amount:,.2f} ₽")


def filter_by_date(manager: FinanceManager):
    """Фильтрует транзакции по диапазону дат"""
    print("\nВведите диапазон дат:")
    start = get_date_input("Начальная дата (ГГГГ-ММ-ДД): ")
    end = get_date_input("Конечная дата (ГГГГ-ММ-ДД): ")
    
    filtered = manager.filter_by_date_range(start, end)
    
    if not filtered:
        print(f"\n📭 Нет транзакций с {start} по {end}.")
        return
    
    print(f"\n🔍 Транзакции с {start} по {end}:")
    print("-" * 60)
    total_income = 0
    total_expense = 0
    
    for t in filtered:
        icon = "📈" if t.type == "income" else "📉"
        print(f"  {icon} {t.date} | {t.category} | {t.description} | {t.amount:,.2f} ₽")
        if t.type == "income":
            total_income += t.amount
        else:
            total_expense += t.amount
    
    print("-" * 60)
    print(f"📈 Доходы за период: {total_income:,.2f} ₽")
    print(f"📉 Расходы за период: {total_expense:,.2f} ₽")
    print(f"💵 Разница: {total_income - total_expense:,.2f} ₽")


def main():
    """Главная функция программы"""
    manager = FinanceManager()
    load_data(manager)
    
    while True:
        clear_screen()
        print_menu()
        
        choice = input("\nВыберите действие: ")
        
        if choice == "1":
            add_income(manager)
            input("\nНажмите Enter для продолжения...")
        
        elif choice == "2":
            add_expense(manager)
            input("\nНажмите Enter для продолжения...")
        
        elif choice == "3":
            show_balance(manager)
            input("\nНажмите Enter для продолжения...")
        
        elif choice == "4":
            show_all_transactions(manager)
            input("\nНажмите Enter для продолжения...")
        
        elif choice == "5":
            show_category_stats(manager)
            input("\nНажмите Enter для продолжения...")
        
        elif choice == "6":
            filter_by_category(manager)
            input("\nНажмите Enter для продолжения...")
        
        elif choice == "7":
            filter_by_date(manager)
            input("\nНажмите Enter для продолжения...")
        
        elif choice == "0":
            save_data(manager)
            print("\n💾 Данные сохранены. До свидания!")
            break
        
        else:
            print("❌ Неверный выбор. Попробуйте снова.")
            input("\nНажмите Enter для продолжения...")


if __name__ == "__main__":
    main()
