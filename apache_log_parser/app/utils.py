import configparser
from datetime import datetime
try:
    from apache_log_parser.app.mydb import database
except:
    try:
        from mydb import database
    except:
        from app.mydb import database


class Logger:        
    def message(self, msg):
        print(f'OK [{datetime.now()}] - {msg}')

    def error(self, msg):
        print(f'ERROR [{datetime.now()}] - {msg}')

def read_config():
    config = configparser.ConfigParser()
    if not config.read('config.ini'):
        raise FileNotFoundError("Configuration file 'config.ini' not found.")
    return config

def db_connect():
    try:
        config = read_config()
        return database.Database(config['Database'])
    except Exception as e:
        print(f"Database connection error: {e}")
        return None

def set_date_format(strformat):
    formats = {
        'dd.mm.yyyy' : "%d.%m.%Y",
        'dd-mm-yyyy' : "%d-%m-%Y", 
        'dd/mm/yyyy' : "%d/%m/%Y", 
        'mm.dd.yyyy' : "%d.%m.%Y", 
        'mm-dd-yyyy' : "%d-%m-%Y",
        'mm/dd/yyyy' : "%d/%m/%Y",
        'yyyy.mm.dd' : '%Y.%m.%d',
        'yyyy-mm-dd' : '%Y-%m-%d',
        'yyyy/mm/dd' : '%Y/%m/%d'
    }
    return formats.get(strformat, "%d.%m.%Y")
