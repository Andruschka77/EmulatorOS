import tkinter as tk
import argparse

def create_vfs_window():
    window = tk.Tk()
    window.title("VFS")
    window.geometry("800x600")
    window.configure(bg='black')
    window.resizable(False, False)
    return window

class TerminalEmulator:
    def __init__(self, window, script_path=None):
        self.window = window
        self.command_count = 0
        self.script_path = script_path
        self.setup_terminal()

        if self.script_path:
            self.window.after(100, self.run_startup_script)

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
        self.create_input_field(1)

    def run_startup_script(self):
        try:
            with open(self.script_path, 'r', encoding='utf-8') as f:
                commands = [line.strip() for line in f if line.strip() and not line.strip().startswith('#')]

            for i, cmd in enumerate(commands):
                self.window.after(500 * i, lambda c=cmd: self.execute_command(c, from_script=True))

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
            display_row = self.command_count * 2 + 1
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

        if not from_script:
            self.current_input_frame.destroy()
            self.create_input_field(display_row + 2)

        self.command_count += 1
        return "break"


def parse_arguments():
    parser = argparse.ArgumentParser(description='VFS Terminal Emulator со стартовым скриптом')
    parser.add_argument('--script', '-s', type=str, help='Путь к стартовому скрипту')
    return parser.parse_args()


def main():
    args = parse_arguments()
    vfs_window = create_vfs_window()
    terminal = TerminalEmulator(vfs_window, args.script)
    vfs_window.mainloop()

if __name__ == "__main__":
    main()