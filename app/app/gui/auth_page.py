import re
import tkinter as tk
from tkinter import messagebox, ttk

from app.app.gui.main_page import MainApp
from app.app.utils import db_connect


class AuthApp:
    def __init__(self):
        self.db = db_connect()
        self.root = tk.Tk()
        self.root.title("Агрегатор Apache - Вход")
        self.root.geometry("600x600+700+180")
        self.root.maxsize(700, 700)
        self.root.minsize(500, 590)

        self.login = ttk.Labelframe(self.root, text='Вход в систему')
        self.username_info = ttk.Label(self.login, text='Имя пользователя должно содержать:\n- Латинские буквы\n- Не меньше 6 символов',
                                       font=('Arial', 9))
        self.password_info = ttk.Label(self.login, text='Пароль должен быть:\n- Не меньше 8 символов',
                                       font=('Arial', 9))

        self.username_entry = ttk.Entry(self.login)
        self.username_entry.insert(0, 'Введите имя пользователя')
        self.username_entry.bind('<FocusIn>',
                                 lambda event: self.username_entry.delete(0, 'end')
                                 if self.username_entry.get() == 'Введите имя пользователя' else None)
        self.username_entry.bind('<FocusOut>',
                                  lambda event: self.username_entry.insert(0, 'Введите имя пользователя')
                                  if self.username_entry.get() == '' else None)

        self.password_entry = ttk.Entry(self.login)
        self.password_entry.insert(0, 'Введите пароль')
        self.password_entry.bind('<FocusIn>',
                                 lambda event: self.password_entry.delete(0, 'end')
                                 if self.password_entry.get() == 'Введите пароль' else None)
        self.password_entry.bind('<FocusOut>',
                                  lambda event: self.password_entry.insert(0, 'Введите пароль')
                                  if self.password_entry.get() == '' else None)

        self.login_btn = ttk.Button(self.login, text='Войти', command=self.login_btn_click)
        self.register = ttk.Label(self.login, text='Зарегистрироваться', foreground='#582de3')
        self.register.bind('<ButtonPress>', self.change_mod)

        self.login.place(rely=0.05, relx=0.1, relheight=0.8, relwidth=0.8)
        self.username_info.place(rely=0.05, relx=0.1, relheight=0.1, relwidth=0.8)
        self.password_info.place(rely=0.15, relx=0.1, relheight=0.1, relwidth=0.8)
        self.username_entry.place(rely=0.325, relx=0.1, relheight=0.1, relwidth=0.8)
        self.password_entry.place(rely=0.45, relx=0.1, relheight=0.1, relwidth=0.8)
        self.login_btn.place(rely=0.7, relx=0.1, relheight=0.1, relwidth=0.8)
        self.register.place(rely=0.8, relx=0.38, relheight=0.1, relwidth=0.6)

        self.root.mainloop()

    def change_mod(self, event):
        if self.register['text'] == 'Зарегистрироваться':
            self.root.title("Агрегатор Apache - Регистрация")
            self.login['text'] = 'Регистрация'
            self.login_btn['text'] = 'Зарегистрироваться'
            self.register['text'] = 'Войти'
            self.register.place(rely=0.8, relx=0.46, relheight=0.1, relwidth=0.6)
        else:
            self.root.title("Агрегатор Apache - Вход")
            self.login['text'] = 'Вход в систему'
            self.login_btn['text'] = 'Войти'
            self.register['text'] = 'Зарегистрироваться'
            self.register.place(rely=0.8, relx=0.38, relheight=0.1, relwidth=0.6)

    def login_btn_click(self):
        if self.username_entry.get() == 'Введите имя пользователя' or self.password_entry.get() == 'Введите пароль':
            messagebox.showinfo('Внимание', 'Вы не заполнили данные')
        else:
            if self.login_btn['text'] == 'Войти':
                if self.validate_credentials(self.username_entry.get(), self.password_entry.get()):
                    if not self.db.check_credentials(username=self.username_entry.get(), password=self.password_entry.get()):
                        messagebox.showerror('Ошибка данных', 'Неверное имя пользователя или пароль')
                    else:
                        username = self.username_entry.get()
                        self.root.destroy()
                        MainApp(username)
            else:
                self.register_user(self.username_entry.get(), self.password_entry.get())

    def validate_credentials(self, username, password):
        if not self.validate_username(username):
            messagebox.showwarning('Ошибка', 'Имя пользователя должно быть больше 5 символов и состоять только из латинских букв')
            return False
        elif not self.validate_password(password):
            messagebox.showwarning('Ошибка', 'Пароль должен быть больше 7 символов')
            return False
        return True

    def register_user(self, username, password):
        if self.validate_credentials(username, password):
            if not self.validate_username(username):
                messagebox.showwarning('Ошибка', 'Недопустимое имя пользователя')
            elif not self.validate_password(password):
                messagebox.showwarning('Ошибка', 'Недопустимый пароль')
            elif self.db.check_username_existence(username):
                messagebox.showwarning('Ошибка', 'Пользователь с таким именем пользователя уже существует')
            else:
                self.db.create_user(username, password)
                messagebox.showinfo('Вы зарегистрировались', 'Регистрация прошла успешно')

    def validate_username(self, username):
        if len(username) < 6:
            return False
        if not re.match(r'^[a-zA-Z]+$', username):
            return False
        return True

    def validate_password(self, password):
        if len(password) < 8:
            return False
        return True

