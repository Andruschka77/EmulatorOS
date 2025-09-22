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
                print("Корневая директория / существует:", "/" in self.fs)
        except Exception as e:
            print(f"Error loading VFS: {e}")
            self.fs = {}

    def ls(self, path="."):
        target_path = self._resolve_path(path)
        if target_path not in self.fs:
            raise Exception(f"Директория '{target_path}' не существует")
        if self.fs[target_path]['type'] != 'dir':
            raise Exception(f"'{target_path}' не является директорией")

        items = []

        if target_path == "/":
            for item_path, item_data in self.fs.items():
                if item_path == "/":
                    continue
                stripped = item_path.lstrip("/")
                if "/" not in stripped:
                    items.append((stripped, item_data))
        else:
            prefix = target_path.rstrip("/") + "/"
            for item_path, item_data in self.fs.items():
                if item_path == target_path:
                    continue
                if item_path.startswith(prefix):
                    rel_path = item_path[len(prefix):]
                    if "/" not in rel_path:
                        items.append((rel_path, item_data))

        return sorted(items, key=lambda x: (x[1]['type'] != 'dir', x[0]))

    def cd(self, path):
        if not path:
            target_path = "/home/user"
        else:
            target_path = self._resolve_path(path)

        if target_path in self.fs and self.fs[target_path]['type'] == 'dir':
            self.current_dir = target_path
            return True
        return False

    def rev(self, path):
        target_path = self._resolve_path(path)
        if target_path not in self.fs:
            raise Exception(f"Файл '{target_path}' не существует!")
        if self.fs[target_path]['type'] != 'file':
            raise Exception(f"'{target_path}' не является файлом!")
        content = self.fs[target_path].get('content', '')
        return content[::-1]

    def find(self, name):
        if not name:
            return []
        results = []
        for item_path in self.fs:
            if item_path != "/" and name.lower() in os.path.basename(item_path).lower():
                results.append(item_path)
        return sorted(results)

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

    def update_prompt(self):
        if hasattr(self, 'current_input_frame'):
            for widget in self.current_input_frame.winfo_children():
                if isinstance(widget, tk.Label):
                    widget.config(text=f"{self.vfs.current_dir}>")

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
            anchor='w',
            justify='left'
        )
        label.grid(row=row, column=0, sticky='w', padx=0, pady=0)

    def create_input_field(self, row):
        input_frame = tk.Frame(self.main_frame, bg='black', highlightthickness=0)
        input_frame.grid(row=row, column=0, sticky='w', padx=0, pady=0)

        prompt_label = tk.Label(
            input_frame,
            text=f"{self.vfs.current_dir}>",
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
        input_entry.pack(side=tk.LEFT, padx=(5, 0))
        input_entry.focus_set()
        input_entry.bind('<Return>', lambda e: self.execute_command(input_entry.get().strip(), row))
        self.current_input_frame = input_frame
        self.current_input_entry = input_entry

    def execute_command(self, command, row=None, from_script=False):
        if not command:
            return

        if from_script:
            display_row = 8 + self.script_index * 2
            self.script_index += 1
        else:
            display_row = row

        self.display_output(f"{self.vfs.current_dir}> {command}", display_row)

        parts = command.split(" ", 1)
        cmd = parts[0]
        arg = parts[1] if len(parts) > 1 else ""
        output_lines = []

        if cmd == "ls":
            try:
                items = self.vfs.ls(arg)
                if not items:
                    output_lines.append("Директория пуста")
                else:
                    for name, item_data in items:
                        item_type = "d" if item_data['type'] == 'dir' else "f"
                        output_lines.append(f"{item_type} {name}")
                    self.display_output("", display_row + 1 + len(output_lines))
            except Exception as e:
                output_lines.append(f"Ошибка: {str(e)}\n")
        elif cmd == "cd":
            success = self.vfs.cd(arg)
            if success:
                output_lines.append(f"Перешел в директорию: {self.vfs.current_dir}\n")
                self.update_prompt()
            else:
                output_lines.append(f"Ошибка: Директория не существует!\n")
        elif cmd == "rev":
            try:
                text = self.vfs.rev(arg)
                output_lines.append(text)
            except Exception as e:
                output_lines.append(f"Ошибка: {str(e)}\n")
        elif cmd == "find":
            try:
                results = self.vfs.find(arg)
                if results:
                    output_lines.extend(results)
                    self.display_output("", display_row + 1 + len(output_lines))
                else:
                    output_lines.append("Ничего не найдено!\n")
            except Exception as e:
                output_lines.append(f"Ошибка: {str(e)}\n")
        elif cmd == "exit":
            self.window.after(100, self.window.destroy)
            return
        else:
            output_lines.append(f"{cmd} - команда не найдена!\n")

        for i, line in enumerate(output_lines):
            self.display_output(line, display_row + 1 + i)

        if from_script:
            if self.script_index < len(self.script_commands):
                next_command = self.script_commands[self.script_index]
                self.window.after(500, lambda: self.execute_command(next_command, None, True))
            else:
                final_row = display_row + 2 + len(output_lines)
                self.create_input_field(final_row)
        else:
            try:
                self.current_input_frame.destroy()
            except Exception:
                pass
            new_row = display_row + 2 + len(output_lines)
            self.create_input_field(new_row)


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
    args = parse_arguments()
    vfs_window = create_vfs_window()
    terminal = TerminalEmulator(vfs_window, args.script, args.vfs)
    vfs_window.mainloop()

if __name__ == "__main__":
    main()