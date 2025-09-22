import tkinter as tk
import argparse
import json
import os

class VFS:
    def __init__(self, json_path=None):
        self.fs = {}
        self.current_dir = "/"

        if json_path and os.path.exists(json_path):
            self.load_from_json(json_path)

    def load_from_json(self, json_path):
        try:
            with open(json_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.fs = data.get('filesystem', {})
                print(f"VFS loaded: {len(self.fs)} items")
        except Exception as e:
            print(f"Error loading VFS: {e}")
            self.fs = {}

    def ls(self, path="."):
        target_path = self._resolve_path(path)
        items = []

        for item_path, item_data in self.fs.items():
            if self._is_in_directory(item_path, target_path):
                rel_path = os.path.relpath(item_path, target_path)
                if rel_path != "." and "/" not in rel_path:
                    items.append((rel_path, item_data))

        return sorted(items, key=lambda x: (x[1]['type'] != 'dir', x[0]))

    def _resolve_path(self, path):
        if path.startswith("/"):
            return os.path.normpath(path)
        return os.path.normpath(os.path.join(self.current_dir, path))

    def _is_in_directory(self, item_path, directory_path):
        return item_path.startswith(directory_path + "/") or item_path == directory_path

def create_vfs_window():
    window = tk.Tk()
    window.title("VFS")
    window.geometry("800x600")
    window.configure(bg='black')
    window.resizable(False, False)
    return window

class TerminalEmulator:
    def __init__(self, window, script_path=None, vfs_json=None):
        self.window = window
        self.command_count = 0
        self.script_path = script_path
        self.vfs = VFS(vfs_json)
        self.script_commands = []
        self.script_index = 0
        self.setup_terminal()
        self.show_commands_info(1)
        if self.script_path:
            self.window.after(100, self.run_startup_script)

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

    def setup_terminal(self):
        self.main_frame = tk.Frame(self.window, bg='black')
        self.main_frame.pack(fill=tk.BOTH, expand=True)

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

    def run_startup_script(self):
        try:
            with open(self.script_path, 'r', encoding='utf-8') as f:
                self.script_commands = [line.strip() for line in f if line.strip() and not line.strip().startswith('#')]

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
        )
        label.grid(row=row, column=0, sticky='w', padx=0, pady=0)

    def create_input_field(self, row):
        input_frame = tk.Frame(self.main_frame, bg='black', highlightthickness=0)
        input_frame.grid(row=row, column=0, sticky='w', padx=0, pady=0)

        prompt_label = tk.Label(
            input_frame,
            text="/>",
            bg='black',
            fg='white',
            font=('Courier New', 12)
        )
        prompt_label.pack(side=tk.LEFT)

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
        input_entry.pack(side=tk.LEFT, padx=(0, 0))
        input_entry.focus_set()
        input_entry.bind('<Return>', lambda e, r=row: self.execute_command(self.current_input_entry.get().strip(), r))
        self.current_input_frame = input_frame
        self.current_input_entry = input_entry

    def execute_command(self, command, row=None, from_script=False):
        if from_script:
            display_row = 8 + self.script_index * 2
            self.script_index += 1
        else:
            display_row = row
        self.display_output(f"/> {command}", display_row)
        command2 = command.split(" ", 1)

        if command2[0] == "ls":
            self.display_output(f"ls {command2[1]}\n", display_row + 1)
        elif command2[0] == "cd":
            self.display_output(f"cd {command2[1]}\n", display_row + 1)
        elif command2[0] == "exit":
            self.window.after(100, self.window.destroy)
        else:
            self.display_output(f"{command} - не является командой!\n", display_row + 1)

        if from_script:
            if self.script_index < len(self.script_commands):
                next_command = self.script_commands[self.script_index]
                self.window.after(500, lambda: self.execute_command(next_command, None, True))
            else:
                final_row = 8 + len(self.script_commands) * 2
                self.create_input_field(final_row)
        else:
            self.current_input_frame.destroy()
            self.create_input_field(display_row + 2)

        self.command_count += 1
        return "break"


def parse_arguments():
    parser = argparse.ArgumentParser(description='VFS Terminal Emulator со стартовым скриптом')
    parser.add_argument('--script', '-s', type=str, help='Путь к стартовому скрипту')
    parser.add_argument('--vfs', '-v', type=str, help='Путь к JSON файлу VFS')
    return parser.parse_args()


def main():
    args = parse_arguments()
    vfs_window = create_vfs_window()
    terminal = TerminalEmulator(vfs_window, args.script, args.vfs)
    vfs_window.mainloop()

if __name__ == "__main__":
    main()