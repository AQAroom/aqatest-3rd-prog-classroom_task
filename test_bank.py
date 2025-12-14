#!/usr/bin/env python3
"""
Тестовый скрипт для проверки класса BankAccount
Версия для GitHub Classroom с использованием autograding-io-grader

Использование: python test_bank.py
Входные данные через stdin: два числа
- начальный баланс
- сумма операции (положительная - пополнение, отрицательная - снятие)

Пример:
Вход: 1000
      200
Вывод:
Баланс счёта: 1000 единиц
На счет зачислено: 200 единиц
Баланс счёта: 1200 единиц
"""

import sys
import os

def import_bank_account():
    """
    Импортирует класс BankAccount из файла task.py
    с обработкой ошибок
    """
    try:
        # Добавляем текущую директорию в Python path
        sys.path.insert(0, os.getcwd())
        
        # Пытаемся импортировать
        from task import BankAccount
        return BankAccount
        
    except ImportError as e:
        print(f"ОШИБКА: Не удалось импортировать класс BankAccount из файла task.py")
        print(f"Детали ошибки: {e}")
        print("Убедитесь, что:")
        print("1. Файл task.py существует в текущей директории")
        print("2. Файл содержит класс BankAccount")
        print("3. Класс определен корректно")
        sys.exit(1)
        
    except SyntaxError as e:
        print(f"ОШИБКА: Синтаксическая ошибка в файле task.py")
        print(f"Детали: {e}")
        sys.exit(1)
        
    except Exception as e:
        print(f"ОШИБКА: Неожиданная ошибка при импорте: {e}")
        sys.exit(1)


def read_input():
    """
    Читает входные данные из stdin
    Возвращает кортеж (начальный_баланс, операция)
    """
    try:
        # Читаем все данные из stdin
        data = sys.stdin.read().strip()
        
        # Разделяем на строки и убираем пустые
        lines = [line.strip() for line in data.split('\n') if line.strip()]
        
        # Проверяем количество аргументов
        if len(lines) < 2:
            print("ОШИБКА: Недостаточно входных данных")
            print("Ожидается: начальный баланс (целое число)")
            print("           сумма операции (целое число, может быть отрицательным)")
            sys.exit(1)
        
        # Преобразуем в числа
        try:
            initial_balance = int(lines[0])
            operation = int(lines[1])
        except ValueError:
            print("ОШИБКА: Входные данные должны быть целыми числами")
            sys.exit(1)
        
        return initial_balance, operation
        
    except Exception as e:
        print(f"ОШИБКА: Ошибка чтения входных данных: {e}")
        sys.exit(1)


def run_bank_operations(initial_balance, operation):
    """
    Выполняет операции с банковским счетом
    с перехватом вывода в stdout
    """
    try:
        # Импортируем класс
        BankAccount = import_bank_account()
        
        # Создаем счет с заданным балансом
        # Второй аргумент "test" - это номер счета для теста
        account = BankAccount("test", initial_balance)
        
        # Выполняем операцию в зависимости от знака
        if operation >= 0:
            # Положительное число - пополнение
            account.add(operation)
        else:
            # Отрицательное число - снятие (убираем минус)
            account.withdraw(-operation)
        
        # Выводим итоговый баланс
        account.status()
        
    except TypeError as e:
        print(f"ОШИБКА: Неверные аргументы при создании BankAccount: {e}")
        print("Проверьте сигнатуру метода __init__:")
        print("Ожидается: def __init__(self, number, sum)")
        sys.exit(1)
        
    except AttributeError as e:
        print(f"ОШИБКА: У класса BankAccount отсутствует необходимый метод: {e}")
        print("Требуемые методы: add(), withdraw(), status()")
        sys.exit(1)
        
    except Exception as e:
        print(f"ОШИБКА: Неожиданная ошибка при работе с BankAccount: {e}")
        sys.exit(1)


def main():
    """
    Главная функция тестового скрипта
    """
    # Читаем входные данные
    initial_balance, operation = read_input()
    
    # Выполняем операции
    run_bank_operations(initial_balance, operation)


def run_test_cases():
    """
    Функция для локального тестирования
    (не используется в GitHub Actions)
    """
    test_cases = [
        (1000, 200,
         """Баланс счёта: 1000 единиц
На счет зачислено: 200 единиц
Баланс счёта: 1200 единиц"""),
        
        (1000, -300,
         """Баланс счёта: 1000 единиц
Со счета снято: 300 единиц
Баланс счёта: 700 единиц"""),
        
        (1000, -1100,
         """Баланс счёта: 1000 единиц
Недостаточно средств на счете
Баланс счёта: 1000 единиц""")
    ]
    
    for i, (balance, op, expected) in enumerate(test_cases, 1):
        print(f"\n{'='*50}")
        print(f"ТЕСТ {i}: Баланс={balance}, Операция={op}")
        print(f"{'='*50}")
        
        # Сохраняем оригинальный stdin
        import io
        original_stdin = sys.stdin
        
        try:
            # Подменяем stdin для теста
            sys.stdin = io.StringIO(f"{balance}\n{op}")
            
            # Сохраняем stdout
            original_stdout = sys.stdout
            sys.stdout = io.StringIO()
            
            # Запускаем тест
            main()
            
            # Получаем вывод
            output = sys.stdout.getvalue().strip()
            
            # Восстанавливаем stdout
            sys.stdout = original_stdout
            
            # Сравниваем с ожидаемым
            if output.strip() == expected.strip():
                print("✅ ТЕСТ ПРОЙДЕН")
                print(f"Вывод:\n{output}")
            else:
                print("❌ ТЕСТ НЕ ПРОЙДЕН")
                print(f"Ожидалось:\n{expected}")
                print(f"Получено:\n{output}")
                
        except Exception as e:
            # Восстанавливаем stdin/stdout
            sys.stdin = original_stdin
            sys.stdout = original_stdout
            print(f"❌ ОШИБКА В ТЕСТЕ: {e}")
            
        finally:
            # Гарантированно восстанавливаем stdin
            sys.stdin = original_stdin


if __name__ == "__main__":
    # Если скрипт запущен без аргументов - используем stdin
    # Если с аргументом "test" - запускаем тестовые случаи
    if len(sys.argv) > 1 and sys.argv[1] == "test":
        run_test_cases()
    else:
        main()