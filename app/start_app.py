from tkinter.messagebox import showerror

import app.gui.config_page
from app.utils import db_connect

if __name__ == '__main__':
    db = db_connect()
    if db:
        import app.gui.auth_page
        app.gui.auth_page.AuthApp()
    else:
        showerror('Ошибка', 'База данных с такими параметрами не существует.\n\nПроверьте достоверность введенных данных в конфигурационном файле.\nПосле редактирования перезапустите программу.')
        app.gui.config_page.ConfigApp()