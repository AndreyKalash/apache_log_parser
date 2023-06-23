from tkinter.messagebox import showerror

import apache_log_parser.app.gui.config_page as cp
from apache_log_parser.app.utils import db_connect

if __name__ == '__main__':
    db = db_connect()
    if db:
        import apache_log_parser.app.gui.auth_page as ap
        ap.AuthApp()
    else:
        showerror('Ошибка', 'База данных с такими параметрами не существует.\n\nПроверьте достоверность введенных данных в конфигурационном файле.\nПосле редактирования перезапустите программу.')
        cp.ConfigApp()