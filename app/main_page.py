from configparser import ConfigParser
from datetime import datetime
from tkinter import Tk, ttk
from tkinter.messagebox import showerror, showwarning
from config_page import start_config
from start_app import db, config
from get_dformat import set_date_format

config.read('config.ini')
type_date_format = config['Database']['dateformat']
# print(type_date_format)
dformat = set_date_format(type_date_format)
def start_main():
    def start_parser():
        

        pass

    def apply_filter():
        dframe.delete(*dframe.get_children())
        sorts = {'По промежутку дат' : db.get_log_entries_in_date_range, 
                'Все данные' : db.get_log_entries ,
                'По IP' : db.get_log_entries_by_ip,
                'По дате' : db.get_log_entries_by_date}
        
        type_sort = sort_choises.get()
        if type_sort == 'По промежутку дат':
            try:
                data_func = sorts.get(type_sort)
                params = (start_date.get(), end_date.get())
                row_data = data_func(params[0], params[1])
            except ValueError:
                showerror(title='Ошибка', message=f'Введенные данные не соответствет формату {type_date_format}')
        else:
            row_data = sorts.get(type_sort)()
        try:
            columns = list(row_data[0].keys())
            data = [tuple(i.values()) for i in row_data]
        except:
            columns = data = [('Данные_отсутсвуют')]


        # data = [(data.)]
        dframe.configure(columns=columns, show='headings')
        for cl in columns: dframe.heading(cl, text=cl)
        for row in data: dframe.insert('', 'end', values=row)
        # pass

    def edit_config():
        start_config()

    def get_api_logs():
        # Логика редакти
        pass
    def sort_selected(event):
        selection = sort_choises.get()
        if selection == 'По промежутку дат':
            start_date.configure(state='normal')
            end_date.configure(state='normal')
        else:
            start_date.state(['disabled'])
            end_date.state(['disabled'])

    def is_valid_date(newval):
        try:
            datetime.strptime(newval, dformat)
            return True
        except ValueError as ex:
            showwarning(title='Ошибка', message=f'Введенная дата не соответствет формату {type_date_format}')
            return False
    
     
    root = Tk()
    root.title("Агрегатор Apache")
    root.geometry("1000x600+450+180")
    root.minsize(780, 550)

    dframe = ttk.Treeview()
    vscroll = ttk.Scrollbar(orient='vertical', command=dframe.yview)
    gscroll = ttk.Scrollbar(orient='horizontal', command=dframe.xview)
    dframe['yscrollcommand']=vscroll.set
    dframe['xscrollcommand']=gscroll.set


    log_screen = ttk.Treeview()

    sort_grpbx = ttk.Labelframe(root, text='Сортировка')


    choises = ['Все данные', 'По IP', 'По дате', 'По промежутку дат']
    sort_choises = ttk.Combobox(sort_grpbx, values=choises, state='readonly')
    sort_choises.current(0)
    sort_choises.bind('<<ComboboxSelected>>', sort_selected)

    start_btn = ttk.Button(text='Запустить парсер', command=start_parser)
    config_btn = ttk.Button(text='Редактировать конфиг', command=edit_config)
    api_btn = ttk.Button(text='Запустить API', command=get_api_logs)
    sort_btn = ttk.Button(sort_grpbx, text='Применить фильтрацию', command=apply_filter)

    check = (root.register(is_valid_date), '%P')

    start_date = ttk.Entry(sort_grpbx, validate='focusout', validatecommand=check)
    start_date.insert(0, 'Введите начальную дату')
    start_date.bind('<FocusIn>', lambda event: start_date.delete(0, 'end') if start_date.get() == 'Введите начальную дату' else None)
    start_date.bind('<FocusOut>', lambda event: start_date.insert(0, 'Введите начальную дату') if start_date.get() == '' else None)
    start_date.state(['disabled'])

    end_date = ttk.Entry(sort_grpbx, validate='focusout', validatecommand=check)
    end_date.insert(0, 'Введите конечную дату')
    end_date.bind('<FocusIn>', lambda event: end_date.delete(0, 'end') if end_date.get() == 'Введите конечную дату' else None)
    end_date.bind('<FocusOut>', lambda event: end_date.insert(0, 'Введите конечную дату') if end_date.get() == '' else None)
    end_date.state(['disabled'])

    dframe.place(rely=0.05, relx=0.05, relheight=0.45, relwidth=0.9)
    vscroll.place(rely=0.05, relx=0.93, relheight=0.45, relwidth=0.02)
    gscroll.place(rely=0.48, relx=0.05, relheight=0.02, relwidth=0.88)

    log_screen.place(rely=0.52, relx=0.05, relheight=0.2, relwidth=0.9)
    start_btn.place(rely=0.74, relx=0.05, relheight=0.06, relwidth=0.35)
    config_btn.place(rely=0.815, relx=0.05, relheight=0.06, relwidth=0.35)
    api_btn.place(rely=0.89, relx=0.05, relheight=0.06, relwidth=0.35)

    sort_grpbx.place(rely=0.73, relx=0.5, relheight=0.22, relwidth=0.45)

    sort_choises.place(rely=0.05, relx=0.05, relheight=0.25, relwidth=0.425)
    sort_btn.place(rely=0.05, relx=0.525, relheight=0.25, relwidth=0.425)
    start_date.place(rely=0.35, relx=0.525, relheight=0.25, relwidth=0.425)
    end_date.place(rely=0.65, relx=0.525, relheight=0.25, relwidth=0.425)

    root.mainloop()

if __name__ == '__main__':
    start_main()
