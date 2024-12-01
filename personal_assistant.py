import csv
from datetime import datetime
import json
import os


class Note:
    def __init__(self, id, title, content, timestamp):
        self.id = id
        self.title = title
        self.content = content
        self.timestamp = timestamp

    def json(self):
        return self.__dict__

    def __str__(self):
        return self.title

    def view(self):
        return (f'ID: {self.id}\n'
                f'Заголовок: {self.title}\n'
                f'Контент: \n{self.content}\n'
                f'Дата создания: {self.timestamp}'
                )



class NoteManager:
    def __init__(self, core):
        self.core = core
        self.notes = list()
        self.load_notes()

    def load_notes(self):
        if os.path.isfile('notes.json'):
            with open("notes.json", "r") as file:
                self.notes = list(Note(**item) for item in json.load(file))

    def save_notes(self):
        with open("notes.json", "w") as file:
            json.dump([note.json() for note in self.notes], file)

    def create_note(self):
        title = input('Введите название: ')
        print('Начните вводить заметку, а когда закончите отправьте 0')
        content = list()
        while (content_part := input()) != '0':
            content.append(content_part)
        if self.notes:
            note_id = max(int(item.id) for item in self.notes) + 1
        else:
            note_id = 1

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        note = Note(
            id=note_id,
            title=title,
            content='\n'.join(content),
            timestamp=timestamp
        )
        self.notes.append(note)
        self.save_notes()
        self.menu()

    def show_notes(self):
        if self.notes:
            print('Выберите заметку: ')
            for ind, note in enumerate(self.notes, start=1):
                print(f'{ind}. {str(note)}')
            print()
            note = None
            while True:
                try:
                    ind = int(input('Введите номер заметки: '))
                    note = self.notes[ind - 1]
                    break
                except Exception:
                    print('Это не похоже на номер')
            self.info_note(note)
        else:
            print('Пока нет заметок')
            self.menu()

    def info_note(self, note):
        print('\n' + '-' * 10)
        print(note.view())
        print('-' * 10 + '\n')
        ind = -1
        while True:
            try:
                print('1. Редактировать заметку \n'
                      '2. Удалить заметку \n'
                      '3. Назад')
                ind = int(input('Выберите действие: '))
                assert ind <= 3 and ind >= 1
                break
            except Exception:
                print('Это не похоже на цифру')

        if ind == 1:
            self.edit_note(note)
        elif ind == 2:
            self.delete_note(note)
        else:
            self.menu()

    def edit_note(self, note):
        while True:
            try:
                print('1. Изменить название \n'
                      '2. Изменить содержание')
                ind = int(input('Выберите действие: '))
                assert ind <= 2 and ind >= 1
                break
            except Exception:
                print('Это не похоже на цифру')
        if ind == 1:
            title = input()
            note.title = title
        else:
            print('Начните вводить заметку, а когда закончите отправьте 0')
            content = list()
            while (content_part := input()) != '0':
                content.append(content_part)
            note.content = '\n'.join(content)

        self.save_notes()
        self.menu()

    def delete_note(self, note):
        while True:
            try:
                print('Вы уверены, что хотите удалить? \n'
                      '1. Да \n'
                      '2. Нет ')
                ind = int(input('Выберите действие: '))
                assert ind <= 2 and ind >= 1
                break
            except Exception:
                print('Это не похоже на цифру')

        if ind == 1:
            self.notes.remove(note)
        else:
            self.info_note(note)
        self.save_notes()
        self.menu()

    def import_notes(self):
        while True:
            try:
                filepath = input('Укажите путь до файла: ')
                with open(filepath, 'r') as file:
                    reader = csv.DictReader(file)
                    notes = list()
                    for item in reader:
                        if set(item.keys()) != {'id', 'title', 'content', 'timestamp'}:
                            print('Ошибка входного файла')
                            raise ValueError()
                        else:
                            notes.append(Note(**item))
                self.notes += notes
                print('Заметки успешно импортированы из CSV-файла.')
                break
            except Exception:
                print('Это не похоже на путь до файла')
        self.save_notes()
        self.menu()

    def export_notes(self):
        filepath = input('Введите имя файла: ')
        with open(f'{filepath}.csv', 'a+', newline='', encoding='utf-8') as outfile:
            writer = csv.writer(outfile)
            writer.writerow(['id', 'title', 'content', 'timestamp'])
            for note in self.notes:
                writer.writerow([note.id, note.title, note.content, note.timestamp])
        print('Заметки успешно экспортированы в CSV-файл.')
        self.menu()

    def menu(self):
        while True:
            try:
                print('1. Создать заметку \n'
                      '2. Смотреть заметки \n'
                      '3. Импорт заметок \n'
                      '4. Экспорт заметок \n'
                      '5. Назад')
                ind = int(input('Выберите действие: '))
                assert ind <= 5 and ind >= 1
                break
            except Exception:
                print('Это не похоже на цифру')
        if ind == 1:
            self.create_note()
        elif ind == 2:
            self.show_notes()
        elif ind == 3:
            self.import_notes()
        elif ind == 4:
            self.export_notes()
        else:
            self.core.run()


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
        self.note = NoteManager(self)
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
                    self.note.menu()
                elif number == 2:
                    self.task.menu()
                elif number == 3:
                    self.contact.menu()
                elif number == 4:
                    self.finance.menu()
                elif number == 5:
                    self.calc.menu()
                elif number == 6:
                    print('Выход из программы')
                    exit(0)
                else:
                    print('Неверный выбор, пожалуйста, введите цифру от 1 до 6')
            except ValueError:
                print('Это не похоже на цифру, попробуйте снова')


if __name__ == '__main__':
    main = Main()
    main.run()