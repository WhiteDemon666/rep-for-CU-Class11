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


prioritets = ['Низкий', 'Средний', 'Высокий']


class Task:
    def __init__(self, id, title, description, priority, due_date, done=False):
        self.id = id
        self.title = title
        self.description = description
        self.due_date = due_date
        self.priority = priority
        self.done = done

    def json(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'done': self.done,
            'priority': self.priority,
            'due_date': self.due_date
        }

    def __str__(self):
        return f'{self.title} - {"Выполнена" if self.done else "В работе"} - {prioritets[self.priority]} - {self.due_date}'

    def view(self):
        return (f'ID: {self.id}\n'
                f'Заголовок: {self.title}\n'
                f'Описание: {self.description}\n'
                f'Статус: {"Выполнена" if self.done else "В работе"}\n'
                f'Приоритет: {prioritets[self.priority]}\n'
                f'Срок выполнения: {self.due_date}')

    def __lt__(self, other):
        return self.priority < other.priority


class TaskManager:
    def __init__(self, core):
        self.tasks = []
        self.core = core
        self.load_tasks()

    def load_tasks(self):
        if os.path.isfile('tasks.json'):
            with open("tasks.json", "r") as file:
                self.tasks = list(Task(**item) for item in json.load(file))

    def save_tasks(self):
        with open("tasks.json", "w") as file:
            json.dump([task.json() for task in self.tasks], file)

    def create_task(self):
        title = input('Введите название задачи: ')
        description = input('Введите описание задачи: ')

        while True:
            try:
                due_date = datetime.strptime(input('Введи срок выполнения задачи: '), "%d-%m-%Y")
                break
            except Exception:
                print('Дата введена не в том формате или введено что-то другое')

        while True:
            try:
                priority_str = input('Выберите приоритет (Высокий/Средний/Низкий): ')
                priority = prioritets.index(priority_str)
                break
            except Exception:
                print('Это не похоже на приоритет задачи')

        if self.tasks:
            task_id = max(int(item.id) for item in self.tasks) + 1
        else:
            task_id = 1

        task = Task(
            id=task_id,
            title=title,
            description=description,
            due_date=due_date.strftime('%d-%m-%Y'),
            priority=priority
        )
        self.tasks.append(task)
        self.save_tasks()
        self.menu()

    def list_tasks(self):
        if self.tasks:
            print('Выберите задачу: ')
            for ind, task in enumerate(sorted(self.tasks, reverse=True), start=1):
                print(f'{ind}. {str(task)}')
            print()
            task = None
            while True:
                try:
                    ind = int(input('Введите номер задачи: '))
                    task = self.tasks[ind - 1]
                    break
                except Exception:
                    print('Это не похоже на номер задачи')
            self.info_task(task)

        else:
            print('Пока нет задач')
            self.menu()

    def info_task(self, task):
        print('\n' + '-' * 10)
        print(task.view())
        print('-' * 10 + '\n')
        ind = -1
        while True:
            try:
                print('1. Редактировать задачу \n'
                      '2. Удалить задачу \n'
                      '3. Отметить задачу как выполненную\n'
                      '4. Назад')
                ind = int(input('Выберите действие: '))
                assert ind <= 4 and ind >= 1
                break
            except Exception:
                print('Это не похоже на цифру')

        if ind == 1:
            self.edit_task(task)
        elif ind == 2:
            self.delete_task(task)
        elif ind == 3:
            self.mark_as_completed(task)
        else:
            self.menu()

    def edit_task(self, task):
        while True:
            try:
                print('1. Изменить название\n'
                      '2. Изменить описание\n'
                      '3. Изменить приоритет\n'
                      '4. Изменить дату завершения\n'
                      '5. Изменить статус выполнения')
                ind = int(input('Выберите действие: '))
                assert 1 <= ind <= 5
                break
            except Exception:
                print('Это не похоже на цифру или выбран недопустимый пункт')

        if ind == 1:
            task.title = input('Введите новое название: ')
        elif ind == 2:
            task.description = input('Введите описание: ')
        elif ind == 3:
            while True:
                try:
                    priority = int(input('Введите новый приоритет: '))
                    task.priority = prioritets.index(priority)
                    break
                except ValueError:
                    print('Это не похоже на приоритет')
        elif ind == 4:
            while True:
                try:
                    due_date = datetime.strptime(input('Введи срок выполнения задачи: '), "%d-%m-%Y")
                    task.due_date = due_date.strftime("%d-%m-%Y")
                    break
                except Exception:
                    print('Дата введена не в том формате или введено что-то другое')
        elif ind == 5:
            while True:
                try:
                    status = input('Задача выполнена? (да/нет): ').strip().lower()
                    if status in ['да', 'нет']:
                        task.done = (status == 'да')
                        break
                    else:
                        raise ValueError
                except ValueError:
                    print('Введите "да" или "нет".')

        self.save_tasks()
        self.menu()

    def mark_as_completed(self, task):
        task.done = True
        print('Задача помечена как выполенная')
        self.menu()

    def delete_task(self, task):
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
            self.tasks.remove(task)
        else:
            self.info_task(task)
        self.save_tasks()
        self.menu()

    def import_tasks(self):
        while True:
            try:
                filepath = input('Укажите путь до файла: ')
                with open(filepath, 'r') as file:
                    reader = csv.DictReader(file)
                    tasks = list()
                    for item in reader:
                        if set(item.keys()) != {'id', 'title', 'description', 'priority', 'due_date', 'done'}:
                            print('Ошибка входного файла')
                            raise ValueError()
                        else:
                            tasks.append(Task(**item))
                self.tasks += tasks
                print('Заметки успешно импортированы из CSV-файла.')
                break
            except Exception:
                print('Это не похоже на путь до файла')
        self.save_tasks()
        self.menu()

    def export_tasks(self):
        filepath = input('Укажите название для файла: ')
        with open(f'{filepath}.csv', 'a+', newline='', encoding='utf-8') as outfile:
            writer = csv.writer(outfile)
            writer.writerow(['id', 'title', 'description', 'priority', 'due_date', 'done'])
            for task in self.tasks:
                writer.writerow([task.id, task.title, task.description,
                                 task.priority, task.due_date, task.done])
        print('Заметки успешно экспортированы в CSV-файл.')
        self.menu()

    def menu(self):
        while True:
            try:
                print('1. Создать задачу \n'
                      '2. Смотреть задачи \n'
                      '3. Импорт задач \n'
                      '4. Экспорт задач \n'
                      '5. Назад')
                ind = int(input('Выберите действие: '))
                assert ind <= 5 and ind >= 1
                break
            except Exception:
                print('Это не похоже на цифру')
        if ind == 1:
            self.create_task()
        elif ind == 2:
            self.list_tasks()
        elif ind == 3:
            self.import_tasks()
        elif ind == 4:
            self.export_tasks()
        else:
            self.core.run()


class ContactManager:
    pass


class FinanceManager:
    pass


class Calculator:
    pass


class Main:
    def __init__(self):
        self.note = NoteManager(self)
        self.task = TaskManager(self)
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