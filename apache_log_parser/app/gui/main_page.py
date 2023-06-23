import sys
import threading
from datetime import datetime
from tkinter import END, Menu, Text, Tk, ttk
from tkinter.messagebox import askyesno, showerror, showwarning

import apache_log_parser.app.gui.auth_page as ap
from apache_log_parser.app.api import app
from apache_log_parser.app.gui.config_page import ConfigApp
from apache_log_parser.app.log_parser import parse_apache_logs
from apache_log_parser.app.utils import Logger, db_connect, read_config, set_date_format


class MainApp:
    class TextWrapper:
        text_field: Text

        def __init__(self, text_field: Text):
            self.text_field = text_field
            self.text_field.bind("<KeyPress>", lambda e: "break")

        def write(self, text: str):
            self.text_field.insert(END, text)

        def flush(self):
            self.text_field.update()
            
    def __init__(self, username='User'):
        self.username = username
        self.db = db_connect()
        self.config = read_config()
        self.type_date_format = self.config['Database']['dateformat']
        self.dformat = set_date_format(self.type_date_format)
        self.api_thread = None
        self.parser_thread = None
        self.logger = Logger()
        

        self.root = Tk()
        self.root.title("Агрегатор Apache")
        self.root.geometry("1000x600+450+180")
        self.root.minsize(780, 550)

        self.dframe = ttk.Treeview()
        self.vscroll = ttk.Scrollbar(orient='vertical', command=self.dframe.yview)
        self.gscroll = ttk.Scrollbar(orient='horizontal', command=self.dframe.xview)
        self.dframe['yscrollcommand'] = self.vscroll.set
        self.dframe['xscrollcommand'] = self.gscroll.set

        self.log_screen = Text(wrap='none')
        self.vlscroll = ttk.Scrollbar(orient='vertical', command=self.log_screen.yview)
        self.glscroll = ttk.Scrollbar(orient='horizontal', command=self.log_screen.xview)
        self.log_screen['yscrollcommand'] = self.vlscroll.set
        self.log_screen['xscrollcommand'] = self.glscroll.set


        self.log_output = self.TextWrapper(self.log_screen)
        sys.stdout = self.log_output
        sys.stderr = self.log_output
        self.sort_grpbx = ttk.Labelframe(self.root, text='Сортировка')

        self.choises = ['Все данные', 'По IP', 'По дате', 'По промежутку дат']
        self.sort_choises = ttk.Combobox(self.sort_grpbx, values=self.choises, state='readonly')
        self.sort_choises.current(0)
        self.sort_choises.bind('<<ComboboxSelected>>', self.sort_selected)

        self.start_btn = ttk.Button(text='Запустить парсер', command=self.start_parser)
        self.config_btn = ttk.Button(text='Редактировать конфиг', command=self.edit_config)
        self.api_btn = ttk.Button(text='Запустить API', command=self.start_api)
        self.sort_btn = ttk.Button(self.sort_grpbx, text='Применить фильтрацию', command=self.apply_filter)

        self.check = (self.root.register(self.is_valid_date), '%P')
        self.start_date = ttk.Entry(self.sort_grpbx, validate='focusout', validatecommand=self.check)
        self.start_date.insert(0, 'Введите начальную дату')
        self.start_date.bind('<FocusIn>', lambda event: self.start_date.delete(0, 'end') if self.start_date.get() == 'Введите начальную дату' else None)
        self.start_date.bind('<FocusOut>', lambda event: self.start_date.insert(0, 'Введите начальную дату') if self.start_date.get() == '' else None)
        self.start_date.state(['disabled'])

        self.end_date = ttk.Entry(self.sort_grpbx, validate='focusout', validatecommand=self.check)
        self.end_date.insert(0, 'Введите конечную дату')
        self.end_date.bind('<FocusIn>', lambda event: self.end_date.delete(0, 'end') if self.end_date.get() == 'Введите конечную дату' else None)
        self.end_date.bind('<FocusOut>', lambda event: self.end_date.insert(0, 'Введите конечную дату') if self.end_date.get() == '' else None)
        self.end_date.state(['disabled'])

        self.create_menu()

        self.dframe.place(rely=0.05, relx=0.05, relheight=0.45, relwidth=0.9)
        self.vscroll.place(rely=0.05, relx=0.93, relheight=0.45, relwidth=0.02)
        self.gscroll.place(rely=0.48, relx=0.05, relheight=0.02, relwidth=0.88)

        self.log_screen.place(rely=0.52, relx=0.05, relheight=0.2, relwidth=0.9)
        self.vlscroll.place(rely=0.52, relx=0.93, relheight=0.2, relwidth=0.02)
        self.glscroll.place(rely=0.7, relx=0.05, relheight=0.02, relwidth=0.88)

        self.start_btn.place(rely=0.74, relx=0.05, relheight=0.06, relwidth=0.35)
        self.config_btn.place(rely=0.815, relx=0.05, relheight=0.06, relwidth=0.35)
        self.api_btn.place(rely=0.89, relx=0.05, relheight=0.06, relwidth=0.35)

        self.sort_grpbx.place(rely=0.73, relx=0.5, relheight=0.22, relwidth=0.45)
        self.sort_choises.place(rely=0.05, relx=0.05, relheight=0.25, relwidth=0.425)
        self.sort_btn.place(rely=0.05, relx=0.525, relheight=0.25, relwidth=0.425)
        self.start_date.place(rely=0.35, relx=0.525, relheight=0.25, relwidth=0.425)
        self.end_date.place(rely=0.65, relx=0.525, relheight=0.25, relwidth=0.425)

        self.root.mainloop()

    def create_menu(self):
        menu = Menu(self.root)
        self.root.config(menu=menu)
        user_menu = Menu(menu, tearoff=False)
        menu.add_cascade(label=self.username, menu=user_menu)
        user_menu.add_command(label="Выйти", command=self.logout)

    def scroll_to_bottom(self):
        self.log_screen.see(END)

    def start_parser(self):
        if self.parser_thread and self.parser_thread.is_alive():
            showwarning(title='Предупреждение', message='Парсер уже запущен.')
            return

        self.parser_thread = threading.Thread(target=self.parse_logs)
        self.parser_thread.daemon = True
        self.parser_thread.start()


    def parse_logs(self):
        log_file_path = self.config['App']['log_dir'] + '\\' + self.config['App']['log_file_mask']
        parse_apache_logs(log_file_path)


    def apply_filter(self):
        self.dframe.delete(*self.dframe.get_children())
        sorts = {
            'По промежутку дат': self.db.get_log_entries_in_date_range,
            'Все данные': self.db.get_log_entries,
            'По IP': self.db.get_log_entries_by_ip,
            'По дате': self.db.get_log_entries_by_date
        }

        type_sort = self.sort_choises.get()
        self.logger.message(f'Сортировка: {type_sort}')
        if type_sort == 'По промежутку дат':
            try:
                data_func = sorts.get(type_sort)
                params = (self.start_date.get(), self.end_date.get())
                row_data = data_func(params[0], params[1])
            except ValueError:
                showerror(title='Ошибка', message=f'Введенные данные не соответствуют формату {self.type_date_format}')
                self.logger.error('Ошибка формата даты')
        else:
            row_data = sorts.get(type_sort)()

        try:
            columns = list(row_data[0].keys())
            data = [tuple(i.values()) for i in row_data]
        except:
            columns = data = [('Данные отсутствуют')]
            self.logger.error('Данные для вывода отсутствуют')
        self.dframe.configure(columns=columns, show='headings')
        for cl in columns:
            self.dframe.heading(cl, text=cl)
        for row in data:
            self.dframe.insert('', 'end', values=row)

    def edit_config(self):
        ConfigApp()

    def start_api(self):
        if self.api_thread and self.api_thread.is_alive():
            showwarning(title='Предупреждение', message='Сервер уже запущен.')
            return

        self.api_thread = threading.Thread(target=self.start_flask_app)
        self.api_thread.daemon = True
        self.api_thread.start()

    def start_flask_app(self):
        app.run()

    def sort_selected(self, event):
        selection = self.sort_choises.get()
        if selection == 'По промежутку дат':
            self.start_date.configure(state='normal')
            self.end_date.configure(state='normal')
        else:
            self.start_date.state(['disabled'])
            self.end_date.state(['disabled'])

    def is_valid_date(self, newval):
        try:
            datetime.strptime(newval, self.dformat)
            return True
        except ValueError as ex:
            showwarning(title='Ошибка', message=f'Введенная дата не соответствует формату {self.type_date_format}')
            self.logger.error('Ошибка формата даты')
            return False
    def logout(self):
        if askyesno("Выход", "Вы действительно хотите выйти?"):
            self.root.destroy()
            ap.AuthApp()