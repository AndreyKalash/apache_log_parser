import tkinter as tk
from configparser import ConfigParser, Error
from tkinter import messagebox, ttk

from apache_log_parser.app.utils import Logger


class ConfigApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Агрегатор Apache - Config")
        self.root.geometry("600x600+700+180")
        self.root.minsize(580, 550)
        self.logger = Logger()

        self.frame = ttk.Frame(self.root)
        self.frame.place(rely=0.05, relx=0.05, relheight=0.7, relwidth=0.9)

        self.scrollbar = ttk.Scrollbar(self.frame)
        self.scrollbar.pack(side='right', fill='y')

        self.config_text = tk.Text(self.frame, wrap='word', yscrollcommand=self.scrollbar.set)
        self.config_text.pack(side='left', fill='both', expand=True)
        self.scrollbar.config(command=self.config_text.yview)

        self.save_button = ttk.Button(self.root, text='Сохранить', command=self.save_config)
        self.save_button.place(rely=0.8, relx=0.05, relheight=0.1, relwidth=0.3)

        self.exit_button = ttk.Button(self.root, text='Выход', command=self.on_closing)
        self.exit_button.place(rely=0.8, relx=0.63, relheight=0.1, relwidth=0.3)

        try:
            with open('config.ini', 'r') as file:
                config_content = file.read()
                self.config_text.insert('end', config_content)
        except FileNotFoundError:
            messagebox.showwarning('Предупреждение', 'Конфигурационный файл не найден')
            self.logger.error('Конфигурационный файл не найден')


        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.mainloop()

    def save_config(self):
        config_content = self.config_text.get(1.0, 'end')
        
        try:
            ConfigParser().read_string(config_content)
            with open('config.ini', 'w') as file:
                file.write(config_content)
            
            messagebox.showinfo('Успех', 'Конфигурационный файл успешно сохранен')
            self.logger.message('Конфигурационный файл успешно сохранен')
            messagebox.showwarning('Изменения.', 'Чтобы изменения вступили в силу, перезагрузите приложение')
            self.root.title("Агрегатор Apache - Config. Сохранено")
        except Error as e:
            messagebox.showerror('Ошибка', f"Неверная запись. Конфигурационный файл должен быть типа 'переменная = значение'")
            self.logger.error('Ошибка при сохранении конфигурационного файла')

        except Exception as e:
            messagebox.showerror('Ошибка', f'Неверный конфиг файл: {str(e)}')
            self.logger.error('Неверный конфиг файл')


    def on_closing(self):
        config_content = self.config_text.get(1.0, 'end').strip()
        current_content = self.get_current_config_content().strip()

        if config_content != current_content:
            result = messagebox.askquestion('Изменения не сохранены', 'Изменения не сохранены. Хотите сохранить перед выходом?',
                                            icon='warning')
            messagebox.showwarning('Изменения.', 'Чтобы изменения вступили в силу, перезагрузите приложение')
            
            
            if result == 'yes':
                self.save_config()
        self.root.destroy()

    def get_current_config_content(self):
        try:
            with open('config.ini', 'r') as file:
                return file.read()
        except FileNotFoundError:
            return ''


if __name__ == '__main__':
    app = ConfigApp()
