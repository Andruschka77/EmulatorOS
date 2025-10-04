import tkinter as tk
import argparse
import json
import os
import shlex
import base64

class VFS:

    # Создает JSON файл с данными по умолчанию
    def create_default_json(self, json_path):
        try:
            default_data = {
                "filesystem": {
                    "/": {"type": "dir"},
                    "/home": {"type": "dir"},
                    "/home/user": {"type": "dir"},
                    "/home/user/documents": {"type": "dir"},
                    "/home/user/documents/work": {"type": "dir"},
                    "/home/user/documents/work/projects": {"type": "dir"},
                    "/home/user/documents/work/projects/python": {"type": "dir"},
                    "/home/user/documents/work/projects/python/main.py": {
                        "type": "file",
                        "content": "print(\"Hello Python Project!\")"
                    },
                    "/home/user/documents/work/projects/javascript": {"type": "dir"},
                    "/home/user/documents/work/projects/javascript/app.js": {
                        "type": "file",
                        "content": "console.log(\"Hello JavaScript!\");"
                    },
                    "/home/user/documents/personal": {"type": "dir"},
                    "/home/user/documents/personal/notes.txt": {
                        "type": "file",
                        "content": "Личные заметки:\n- Купить молоко\n- Позвонить маме"
                    },
                    "/home/user/downloads": {"type": "dir"},
                    "/home/user/downloads/temp": {"type": "dir"},
                    "/home/user/music": {"type": "dir"},
                    "/home/user/music/rock": {"type": "dir"},
                    "/home/user/music/classical": {"type": "dir"},
                    "/home/user/pictures": {"type": "dir"},
                    "/home/user/pictures/vacation": {"type": "dir"},
                    "/home/user/pictures/vacation/beach.jpg": {
                        "type": "file",
                        "content": "[BINARY DATA: beach photo]"
                    },
                    "/etc": {"type": "dir"},
                    "/etc/config": {"type": "dir"},
                    "/etc/config/system": {"type": "dir"},
                    "/etc/config/system/settings.json": {
                        "type": "file",
                        "content": "{\n  \"theme\": \"dark\",\n  \"language\": \"ru\",\n  \"autostart\": true\n}"
                    },
                    "/etc/config/network": {"type": "dir"},
                    "/etc/config/network/wifi.conf": {
                        "type": "file",
                        "content": "SSID=MyWiFi\nPassword=secret123"
                    },
                    "/etc/passwd": {
                        "type": "file",
                        "content": "root:x:0:0:root:/root:/bin/bash\nuser:x:1000:1000:User:/home/user:/bin/bash"
                    },
                    "/var": {"type": "dir"},
                    "/var/log": {"type": "dir"},
                    "/var/log/system.log": {
                        "type": "file",
                        "content": "2024-01-15 10:30:15 - System started\n2024-01-15 10:31:22 - User logged in"
                    },
                    "/var/log/app.log": {
                        "type": "file",
                        "content": "INFO: Application initialized\nDEBUG: Loading configuration"
                    },
                    "/var/tmp": {"type": "dir"},
                    "/var/tmp/cache": {"type": "dir"},
                    "/usr": {"type": "dir"},
                    "/usr/bin": {"type": "dir"},
                    "/usr/bin/python": {
                        "type": "file",
                        "content": "#!/usr/bin/env python3\nprint(\"Python interpreter\")"
                    },
                    "/usr/bin/bash": {
                        "type": "file",
                        "content": "#!/bin/bash\necho \"Bash shell\""
                    },
                    "/usr/lib": {"type": "dir"},
                    "/usr/lib/python3.10": {"type": "dir"},
                    "/usr/lib/python3.10/os.py": {
                        "type": "file",
                        "content": "# OS module implementation"
                    },
                    "/tmp": {"type": "dir"},
                    "/tmp/test_file.tmp": {
                        "type": "file",
                        "content": "Временный файл\nМожно удалить"
                    },
                    "/root": {"type": "dir"},
                    "/root/.bashrc": {
                        "type": "file",
                        "content": "export PATH=$PATH:/usr/local/bin\nalias ll='ls -la'"
                    },
                    "/opt": {"type": "dir"},
                    "/opt/applications": {"type": "dir"},
                    "/opt/applications/myapp": {"type": "dir"},
                    "/opt/applications/myapp/config.ini": {
                        "type": "file",
                        "content": "[database]\nhost=localhost\nport=5432\nname=myapp_db"
                    },
                    "/mnt": {"type": "dir"},
                    "/mnt/usb": {"type": "dir"},
                    "/mnt/cdrom": {"type": "dir"},
                    "/dev": {"type": "dir"},
                    "/dev/null": {
                        "type": "file",
                        "content": "null device"
                    },
                    "/dev/random": {
                        "type": "file",
                        "content": "random data source"
                    }
                }
            }

            os.makedirs(os.path.dirname(json_path), exist_ok=True) # Создаем директорию если она не существует
            json_str = json.dumps(default_data, indent=2, ensure_ascii=False) # Конвертируем данные в JSON строку
            encoded_data = base64.b64encode(json_str.encode('utf-8')).decode('ascii') # Кодируем в base64

            with open(json_path, 'w', encoding='utf-8') as f: # Сохраняем данные в JSON файл
                f.write(encoded_data)

            print(f"Создан новый VFS файл: {json_path}")

        except Exception as e:
            print(f"Ошибка создания VFS файла: {e}")

    def __init__(self, json_path=None):
        self.fs = {}
        self.current_dir = "/" # Текущая рабочая директория
        self.json_path = json_path  # Сохраняем путь к JSON файлу

        # Создаем JSON файл если он не существует
        if json_path and not os.path.exists(json_path):
            self.create_default_json(json_path)

        if json_path and os.path.exists(json_path):
            self.load_from_json(json_path)

    # Загружает VFS из JSON файла
    def load_from_json(self, json_path):
        try:
            with open(json_path, 'r', encoding='utf-8') as f:
                encoded_data = f.read()

            # Декодируем из base64
            json_str = base64.b64decode(encoded_data.encode('ascii')).decode('utf-8')

            # Парсим JSON
            data = json.loads(json_str)
            self.fs = data.get('filesystem', {})
        except Exception as e:
            print(f"Error loading VFS: {e}")
            self.fs = {}

    def ls(self, path="."):
        target_path = self._resolve_path(path)
        if target_path not in self.fs: # Проверяем, существует ли целевой путь в файловой системе
            raise Exception(f"Директория '{target_path}' не существует")
        if self.fs[target_path]['type'] != 'dir': # Проверяем, что это действительно директория, а не файл
            raise Exception(f"'{target_path}' не является директорией")

        items = [] # Создаем пустой список для хранения найденных элементов

        # Если целевой путь - корневая директория "/"
        if target_path == "/":
            for item_path, item_data in self.fs.items(): # Перебираем все пути в файловой системе
                if item_path == "/": # Пропускаем саму корневую директорию
                    continue
                stripped = item_path.lstrip("/") # Убираем начальный слеш из пути
                if "/" not in stripped: # Проверяем, что это прямой потомок корня
                    items.append((stripped, item_data)) # Добавляем в список (имя, данные)
        else:
            prefix = target_path.rstrip("/") + "/" # Создаем префикс для поиска потомков
            for item_path, item_data in self.fs.items(): # Перебираем все пути в файловой системе
                if item_path == target_path:  # Пропускаем саму целевую директорию
                    continue
                if item_path.startswith(prefix): # Проверяем, что путь начинается с нашего префикса
                    rel_path = item_path[len(prefix):] # Вычисляем относительный путь, убираем префикс
                    if "/" not in rel_path: # Проверяем, что это прямой потомок
                        items.append((rel_path, item_data)) # Добавляем в список (имя, данные)

        return sorted(items, key=lambda x: (x[1]['type'] != 'dir', x[0]))

    def cd(self, path):
        if not path: # Если путь пустой, то используем домашнюю директорию по умолчанию
            target_path = "/home/user"
        else:
            target_path = self._resolve_path(path) # Преобразуем относительный путь в абсолютный

        # Проверяем существует ли путь и является он директорией
        if target_path in self.fs and self.fs[target_path]['type'] == 'dir':
            self.current_dir = target_path # Устанавливаем новую текущую директорию
            return True
        return False

    def rev(self, path):
        target_path = self._resolve_path(path) # Преобразуем относительный путь в абсолютный
        if target_path not in self.fs: # Проверяем, что файл существует
            raise Exception(f"Файл '{target_path}' не существует!")
        if self.fs[target_path]['type'] != 'file': # Проверяем, что это файл, а не директория
            raise Exception(f"'{target_path}' не является файлом!")
        content = self.fs[target_path].get('content', '') # Получаем содержимое файла
        return content[::-1] # Возвращаем содержимое в обратном порядке

    def find(self, name):
        if not name: # Если имя пустое - возвращаем пустой список
            return []
        results = [] # Создаем пустой список для результатов
        for item_path in self.fs: # Перебираем все пути в файловой системе
            # Пропускаем корневую директорию "/" и ищем вхождение подстроки
            if item_path != "/" and name.lower() in os.path.basename(item_path).lower():
                results.append(item_path) # Добавляем полный путь в результаты
        return sorted(results)

    def touch(self, path):
        target_path = self._resolve_path(path) # Преобразуем относительный путь в абсолютный

        parent_dir = os.path.dirname(target_path) # Получаем родительскую директорию
        if not parent_dir: # Если родительская директория пустая - устанавливаем "/"
            parent_dir = "/"

        # Проверяем, что родительская директория существует и является директорией
        if parent_dir not in self.fs or self.fs[parent_dir]['type'] != 'dir':
            raise Exception(f"Родительская директория '{parent_dir}' не существует!")

        if target_path in self.fs: # Проверяем, не существует ли уже такой путь
            # Если путь существует и это файл - ничего не делаем
            if self.fs[target_path]['type'] == 'file':
                return
            else: # Если это не файл (директория) - ошибка
                raise Exception(f"Путь '{target_path}' уже существует и это не файл!")

        self.fs[target_path] = { # Создаем новый файл в файловой системе
            "type": "file", # Тип - файл
            "content": "" # Пустое содержимое
        }

    # Преобразует относительный путь в абсолютный с обработкой . и ..
    def _resolve_path(self, path):
        if not path or path == ".":
            current = self.current_dir
        elif path.startswith("/"):
            current = path
        else:
            if self.current_dir == "/":
                current = "/" + path.strip("/")
            else:
                current = self.current_dir.rstrip("/") + "/" + path.strip("/")

        parts = []
        for part in current.split("/"):
            if part == "" or part == ".":
                continue
            if part == "..":
                if parts:
                    parts.pop()
                continue
            parts.append(part)

        result = "/" + "/".join(parts) if parts else "/"
        return result

    # Удаляет файл vfs.json
    def cleanup(self):
        if self.json_path and os.path.exists(self.json_path):
            try:
                os.remove(self.json_path)
            except Exception as e:
                print(f"Ошибка при удалении файла {self.json_path}: {e}")

# Создает и настраивает главное окно приложения
def create_vfs_window():
    window = tk.Tk()
    window.title("VFS")
    window.geometry("800x600")
    window.configure(bg='black')
    window.resizable(True, True)
    return window

class TerminalEmulator:
    # Инициализация терминала
    def __init__(self, window, script_path=None, vfs_json=None):
        self.window = window # Главное окно
        self.command_count = 0 # Счетчик команд
        self.script_path = script_path # Путь к скрипту
        self.vfs = VFS(vfs_json) # Создание VFS
        self.script_commands = [] # Команды из скрипта
        self.script_index = 0 # Текущая позиция в скрипте
        self.setup_terminal() # Настройка интерфейса
        self.show_commands_info(1) # Вывод информации о командах
        self.auto_scroll_enabled = True
        self.window.protocol("WM_DELETE_WINDOW", self.on_close) # Обработка закрытия окна
        if self.script_path: # Если указан скрипт, то запускаем его
            self.window.after(100, self.run_startup_script)

    # Обработчик закрытия окна
    def on_close(self):
        self.cleanup()
        self.window.destroy()

    # Удаляет файл vfs.json
    def cleanup(self):
        if hasattr(self, 'vfs'):
            self.vfs.cleanup()

    # Парсит команду с поддержкой кавычек
    def parse_command(self, command):
        try:
            # Используем shlex для корректного парсинга команд с кавычками
            parts = shlex.split(command)
            if not parts:
                return "", ""
            cmd = parts[0]
            args = parts[1:] if len(parts) > 1 else []
            return cmd, args
        except Exception as e:
            # В случае ошибки парсинга, возвращаем команду как есть
            parts = command.split(" ", 1)
            cmd = parts[0]
            arg = parts[1] if len(parts) > 1 else ""
            return cmd, [arg] if arg else []

    # Справка по командам
    def show_commands_info(self, row):
        commands_list = [
            "Доступные команды:",
            "ls [path] - список файлов и папок в директории",
            "cd [path] - сменить текущую директорию",
            "rev <file> - вывести содержимое файла в обратном порядке",
            "find <name> - найти файлы и папки по имени",
            "touch <file> - создать пустой файл",
            "exit - выйти из терминала\n",
        ]

        for i, line in enumerate(commands_list):
            self.display_output(line, row + i)

    # Создает основные элементы интерфейса терминала
    def setup_terminal(self):
        # Создаем Canvas и Scrollbar
        self.canvas = tk.Canvas(self.window, bg='black', highlightthickness=0)
        self.scrollbar = tk.Scrollbar(self.window, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        # Размещаем Canvas и Scrollbar
        self.scrollbar.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)

        # Создаем Frame внутри Canvas для содержимого
        self.main_frame = tk.Frame(self.canvas, bg='black')
        self.canvas_frame = self.canvas.create_window((0, 0), window=self.main_frame, anchor="nw")

        # Обновляем область прокрутки при изменении содержимого
        def update_scrollregion(event):
            self.canvas.configure(scrollregion=self.canvas.bbox("all"))
            # Автоматическая прокрутка вниз при изменении содержимого
            if self.auto_scroll_enabled:
                self.canvas.yview_moveto(1.0)

        self.main_frame.bind("<Configure>", update_scrollregion)

        # Настройка прокрутки колесом мыши
        def on_mouse_wheel(event):
            self.auto_scroll_enabled = False
            self.canvas.yview_scroll(-1 * (event.delta // 120), "units")

        self.canvas.bind_all("<MouseWheel>", on_mouse_wheel)

        welcome_label = tk.Label(
            self.main_frame,
            text="Добро пожаловать в VFS Terminal!",
            bg='black',
            fg='white',
            font=('Courier New', 12),
        )
        welcome_label.grid(row=0, column=0, sticky='w', pady=0, padx=0)

        if not self.script_path:
            self.create_input_field(8)

    # Обновляет приглашение ввода после смены директории
    def update_prompt(self):
        if hasattr(self, 'current_input_frame'):
            for widget in self.current_input_frame.winfo_children():
                if isinstance(widget, tk.Label):
                    widget.config(text=f"{self.vfs.current_dir}>")

    # Выполняет стартовый скрипт при запуске эмулятора
    def run_startup_script(self):
        try:
            # Чтение скрипта из файла
            with open(self.script_path, 'r', encoding='utf-8') as f:
                self.script_commands = [line.strip() for line in f if line.strip() and not line.strip().startswith('#')]

            # Если есть команды - запускаем первую
            if self.script_commands:
                self.execute_command(self.script_commands[0], 8, from_script=True)

        except Exception as e:
            self.display_output(f"Ошибка чтения скрипта: {str(e)}", 1)

    def display_output(self, text, row):
        label = tk.Label(
            self.main_frame,
            text=text,
            bg='black',
            fg='white',
            font=('Courier New', 12),
            anchor='w',
            justify='left'
        )
        label.grid(row=row, column=0, sticky='w', padx=0, pady=0)

    # Создает строку ввода с приглашением
    def create_input_field(self, row):
        input_frame = tk.Frame(self.main_frame, bg='black', highlightthickness=0)
        input_frame.grid(row=row, column=0, sticky='w', padx=0, pady=0)

        # Приглашение с текущим путем
        prompt_label = tk.Label(
            input_frame,
            text=f"{self.vfs.current_dir}>",
            bg='black',
            fg='white',
            font=('Courier New', 12)
        )
        prompt_label.pack(side=tk.LEFT)

        # Поле ввода команды
        input_entry = tk.Entry(
            input_frame,
            bg='black',
            fg='white',
            font=('Courier New', 12),
            insertbackground='white',
            width=50,
            highlightthickness=0,
            borderwidth=0,
            relief='flat'
        )
        input_entry.pack(side=tk.LEFT, padx=(5, 0))
        input_entry.focus_set() # Устанавливаем фокус ввода
        # Обработка нажатия Enter
        input_entry.bind('<Return>', lambda e: self.execute_command(input_entry.get().strip(), row))
        self.current_input_frame = input_frame
        self.current_input_entry = input_entry
        self.auto_scroll_enabled = True

    # Основной метод выполнения команд
    def execute_command(self, command, row=None, from_script=False):
        if not command: # Проверка на пустоту команды
            return

        if from_script: # Если команда из скрипта
            display_row = 8 + self.script_index * 2 # 8 - базовая строка, +2 за каждую команду
            self.script_index += 1 # Увеличиваем счетчик команд скрипта
        else:
            display_row = row # Используем переданную строку

        self.display_output(f"{self.vfs.current_dir}> {command}", display_row) # Отображаем введенную команда на экране

        cmd, args = self.parse_command(command)
        output_lines = [] # Список для вывода команды

        if cmd == "ls":
            try:
                path_arg = args[0] if args else "."
                items = self.vfs.ls(path_arg) # Вызываем метод ls из VFS с переданным аргументом
                if not items: # Если директория пустая
                    output_lines.append("Директория пуста")
                else:
                    # форматируем вывод: "d имя" для директорий, "f имя" для файлов
                    for name, item_data in items:
                        item_type = "d" if item_data['type'] == 'dir' else "f"
                        output_lines.append(f"{item_type} {name}")
                    self.display_output("", display_row + 1 + len(output_lines))
            except Exception as e:
                output_lines.append(f"Ошибка: {str(e)}\n")
        elif cmd == "cd":
            path_arg = args[0] if args else ""
            success = self.vfs.cd(path_arg) # Смена директории вызовом метода cd из VFS
            if success: # Если успех
                output_lines.append(f"Перешел в директорию: {self.vfs.current_dir}\n")
                self.update_prompt() # Обновляем приглашение ввода
            else:
                output_lines.append(f"Ошибка: Директория не существует!\n")
        elif cmd == "rev":
            try:
                text = self.vfs.rev(args[0]) # Получаем содержимое файла в обратном порядке методом rev
                output_lines.append(text)
            except Exception as e:
                output_lines.append(f"Ошибка: {str(e)}\n")
        elif cmd == "find":
            try:
                results = self.vfs.find(args[0]) # Ищем файлы/папки по имени
                if results:
                    output_lines.extend(results)
                    self.display_output("", display_row + 1 + len(output_lines))
                else:
                    output_lines.append("Ничего не найдено!\n")
            except Exception as e:
                output_lines.append(f"Ошибка: {str(e)}\n")
        elif cmd == "touch":
            try:
                if not args: # Проверяем, что указано имя файла
                    output_lines.append("Ошибка: укажите имя файла!\n")
                else:
                    self.vfs.touch(args[0]) # Создаем пустой файл
                    output_lines.append(f"Создан пустой файл: {self.vfs._resolve_path(args[0])}\n")
            except Exception as e:
                output_lines.append(f"Ошибка: {str(e)}\n")
        elif cmd == "exit":
            self.cleanup() # Удаляем файл vfs.json
            self.window.after(100, self.window.destroy) # Закрытие окна через 100 мс
            return
        else:
            output_lines.append(f"{cmd} - команда не найдена!\n")

        # Отображаем вывод команды из списка
        for i, line in enumerate(output_lines):
            self.display_output(line, display_row + 1 + i) # Вычисляем строку для каждой линии вывода

        # Логика для скрипта
        if from_script:
            if self.script_index < len(self.script_commands): # Проверяем есть ли еще команды в скрипте
                # Запускаем следующую команду с задержкой
                next_command = self.script_commands[self.script_index]
                # Запускаем следующую команду через 500 мс
                self.window.after(500, lambda: self.execute_command(next_command, None, True))
            else:
                # Скрипт завершен - показываем поле ввода
                final_row = display_row + 2 + len(output_lines)
                self.create_input_field(final_row) # Поле для ручного ввода
        else:
            try:
                self.current_input_frame.destroy() # Удаляем фрейм с полем ввода
            except Exception:
                pass
            new_row = display_row + 2 + len(output_lines) # Вычисляем позицию для нового поля ввода
            self.create_input_field(new_row) # Создаем новое поле ввода для некст команды

# Парсит аргументы командной строки
def parse_arguments():
    parser = argparse.ArgumentParser(description='VFS Terminal Emulator')
    parser.add_argument('--script', '-s', type=str, help='Путь к стартовому скрипту')
    parser.add_argument(
        '--vfs', '-v',
        type=str,
        default=os.path.join(os.path.dirname(__file__), "vfs.json"),
        help='Путь к JSON файлу VFS'
    )
    return parser.parse_args()

def main():
    args = parse_arguments() # Читаем аргументы
    vfs_window = create_vfs_window() # Создаем окно
    terminal = TerminalEmulator(vfs_window, args.script, args.vfs) # Создаем эмулятор
    vfs_window.mainloop() # Запускаем главный цикл

if __name__ == "__main__":
    main()