import csv
from datetime import datetime
import json
import os


class NoteManager:
    pass


class TaskManager:
    pass


class ContactManager:
    pass


class FinanceManager:
    pass


class Calculator:
    pass


class Main:
    def __init__(self):
        self.note = NoteManager()
        self.task = TaskManager()
        self.contact = ContactManager()
        self.finance = FinanceManager()
        self.calc = Calculator()

    def run(self):
        while True:
            print('Добро пожаловать в Персональный помощник!'
                  '\nВыберите действие:'
                  '\n1. Управление заметками'
                  '\n2. Управление задачами'
                  '\n3. Управление контактами'
                  '\n4. Управление финансовыми записями'
                  '\n5. Калькулятор'
                  '\n6. Выход')

            try:
                number = int(input('Введите номер действия: '))
                if number == 1:
                    self.note.run()
                elif number == 2:
                    self.task.run()
                elif number == 3:
                    self.contact.run()
                elif number == 4:
                    self.finance.run()
                elif number == 5:
                    self.calc.run()
                elif number == 6:
                    print('Выход из программы')
                    break
                else:
                    print('Неверный выбор, пожалуйста, введите цифру от 1 до 6')
            except ValueError:
                print('Это не похоже на цифру, попробуйте снова')


if __name__ == '__main__':
    main = Main()
    main.run()