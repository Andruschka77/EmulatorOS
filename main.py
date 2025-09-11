import tkinter as tk

def create_vfs_window():
    window = tk.Tk()
    window.title("VFS")
    window.geometry("800x600")
    window.configure(bg='black')
    window.resizable(False, False)
    return window

class TerminalEmulator:
    def __init__(self, window):
        self.window = window
        self.command_count = 0
        self.setup_terminal()

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
        input_entry.bind('<Return>', lambda e, r=row: self.execute_command(r))
        self.current_input_frame = input_frame
        self.current_input_entry = input_entry

    def parse_arguments(self, command):
        quote_start = -1
        for i, char in enumerate(command):
            if char in ['"', "'"]:
                quote_start = i
                break
        if quote_start == -1:
            return ""

        quote_char = command[quote_start]
        for i in range(quote_start + 1, len(command)):
            if command[i] == quote_char:
                return command[quote_start + 1:i]
        return ""

    def execute_command(self, current_row):
        command = self.current_input_entry.get().strip()
        command2 = command.split(" ", 1)

        if command:
            command_label = tk.Label(
                self.main_frame,
                text=f"/> {command}",
                bg='black',
                fg='white',
                font=('Courier New', 12),
            )
            command_label.grid(row=current_row, column=0, sticky='w', padx=0, pady=0)

            if command2[0] == "ls":
                output_label = tk.Label(
                    self.main_frame,
                    text=f"ls {command2[1]}",
                    bg='black',
                    fg='white',
                    font=('Courier New', 12),
                )
                output_label.grid(row=current_row + 1, column=0, sticky='w', padx=0, pady=0)
            elif command2[0] == "cd":
                output_label = tk.Label(
                    self.main_frame,
                    text=f"cd {command2[1]}",
                    bg='black',
                    fg='white',
                    font=('Courier New', 12),
                )
                output_label.grid(row=current_row + 1, column=0, sticky='w', padx=0, pady=0)
            elif command2[0] == "exit":
                self.window.after(100, self.window.destroy) # Закрытие окна программы

            self.current_input_frame.destroy() # Очистка старого поля ввода
            self.create_input_field(current_row + 2) # Создание нового поля ввода в правильной позиции
            self.command_count += 1 # Учет выполненных команд

        return "break"

def main():
    vfs_window = create_vfs_window()
    terminal = TerminalEmulator(vfs_window)
    vfs_window.mainloop()

if __name__ == "__main__":
    main()