from tkinter import ttk, Tk, Text, Scrollbar, Frame, Button, messagebox
from configparser import ConfigParser, ParsingError


def start_config():
    root = Tk()
    root.title("Агрегатор Apache - Config")
    root.geometry("600x600+700+180")
    # root.minsize(780, 550)

    def save_config():
        config_content = config_text.get(1.0, 'end')
        
        try:
            # Parse the config content to validate it
            ConfigParser().read_string(config_content)
            
            # Save the config to a file (replace 'config.ini' with your desired file name)
            with open('config.ini', 'w') as file:
                file.write(config_content)
            
            messagebox.showinfo('Успех', 'Конфигурационный файл успешно сохранен')
            root.title("Агрегатор Apache - Config. Сохранено")
        except ParsingError as e:
            messagebox.showerror('Ошибка', f"Неверная запись. Конфигурационный файл должен быть типа 'переменная = значение' ")
        except Exception as e:
            messagebox.showerror('Ошибка', f'Неверный конфиг файл {str(e)}')

    def on_closing():
        if config_text.get(1.0, 'end').strip() != config_content.strip():
            result = messagebox.askquestion('Изменения не сохраненны', 'Изменения не сохранены. Хотите сохранить перед выходом?',
                                            icon='warning')
            if result == 'yes':
                save_config()
                root.destroy()
            elif result == 'no':
                root.destroy()
        else:
            root.destroy()
    frame = ttk.Frame(root)
    # frame.pack(fill='both', expand=True)
    frame.place(rely=0.05, relx=0.05, relheight=0.7, relwidth=0.9)

    scrollbar = ttk.Scrollbar(frame)
    scrollbar.pack(side='right', fill='y')

    config_text = Text(frame, wrap='word', yscrollcommand=scrollbar.set)
    config_text.pack(side='left', fill='both', expand=True)
    scrollbar.config(command=config_text.yview)

   
    save_button = ttk.Button(root, text='Сохранить', command=save_config)
    save_button.place(rely=0.8, relx=0.05, relheight=0.1, relwidth=0.3)

    save_button = ttk.Button(root, text='Выход', command=on_closing)
    save_button.place(rely=0.8, relx=0.63, relheight=0.1, relwidth=0.3)

   
    try:
        with open('config.ini', 'r') as file:
            config_content = file.read()
            config_text.insert('end', config_content)
    except FileNotFoundError:
        messagebox.showwarning('Предупреждение', 'Конфигурационный файл не найден')

    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()

if __name__ == '__main__':
    start_config()
