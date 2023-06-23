from datetime import date, datetime


import app.app.utils
from app.app.mydb.models import ApacheLog, Base, User
from sqlalchemy import create_engine, func
from sqlalchemy.exc import DatabaseError
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import create_database, database_exists


class Database:
    def __init__(self, config):
        self.config = config
        self.create_db = eval(self.config['create_db_if_not_exist'])
        self.engine = create_engine(
            f"mysql+mysqlconnector://{self.config['username']}:{self.config['password']}@{self.config['host']}:{self.config['port']}/{self.config['database']}",
            pool_pre_ping=True,
        )
        if self.create_db:
            self.create_database()

        self.Session = sessionmaker(bind=self.engine)
        self.date_format = app.utils.set_date_format(config['dateformat'])
        try:
            Base.metadata.create_all(self.engine, checkfirst=True)
        except DatabaseError as e:
            if str(e).startswith("(mysql.connector.errors.DatabaseError) 2003 (HY000)"):
                print("Ошибка подключения к базе данных. Проверьте данные подключения и работу службы MYSQL")

    def create_database(self):
        if not database_exists(self.engine.url):
            create_database(self.engine.url)
        else:
            self.engine.connect()


    def check_username_existence(self, username):
        session = self.Session()
        query = session.query(User).filter(User.username == username)
        user = query.first()
        session.close()
        return user is not None
   
    def check_credentials(self, username, password):
        session = self.Session()
        query = session.query(User).filter(User.username == username, User.password == password)
        user = query.first()
        session.close()
        return user is not None

    def create_user(self, v_username, v_password):
        session = self.Session()
        user = User(username=v_username, password=v_password)
        session.add(user)
        session.commit()
        session.close()


    def create_log_entry(self, v_ip_address, v_remote_logname, v_remote_user, v_request_time, v_request_method, v_requested_url, v_status_code, v_response_size):
        session = self.Session()
        log_entry = ApacheLog(ip_address=v_ip_address, 
                              remote_logname=v_remote_logname, 
                              remote_user=v_remote_user, 
                              request_dtime=v_request_time, 
                              request_method=v_request_method, 
                              requested_url=v_requested_url,
                              status_code=v_status_code, 
                              response_size=v_response_size)
        session.add(log_entry)
        session.commit()
        session.close()

    def get_log_entries(self):
        session = self.Session()
        query = session.query(ApacheLog)
        log_entries = query.all()
        session.close()
        return [
        {
            'id': log_entry.id,
            'ip_address': log_entry.ip_address,
            'remote_logname': log_entry.remote_logname,
            'remote_user': log_entry.remote_user,
            'request_dtime': log_entry.request_dtime,
            'request_method': log_entry.request_method,
            'requested_url': log_entry.requested_url,
            'response_size': log_entry.response_size,
            'status_code': log_entry.status_code
        }
        for log_entry in log_entries
    ]

    def get_log_entries_by_ip(self):
        session = self.Session()
        query = session.query(ApacheLog.ip_address, func.count(ApacheLog.ip_address)).group_by(ApacheLog.ip_address)
        log_entries = query.all()
        session.close()
        return [
            {
            'ip_address': log_entry[0],
            'count': log_entry[1]
            }
        for log_entry in log_entries
    ]

    def get_log_entries_by_date(self):
        session = self.Session()
        query = session.query(func.date(ApacheLog.request_dtime), func.count(ApacheLog.request_dtime)).group_by(
            func.date(ApacheLog.request_dtime))
        log_entries = query.all()
        session.close()
        return [
            {
            'date': log_entry[0],
            'count': log_entry[1]
            }
        for log_entry in log_entries
    ]

    def get_log_entries_in_date_range(self, start_date:date, end_date:date):
        if not isinstance(start_date, date):  start_date = datetime.strptime(start_date, self.date_format).date()
        if not isinstance(end_date, date): end_date = datetime.strptime(end_date, self.date_format)
        session = self.Session()
        query = session.query(ApacheLog).filter(ApacheLog.request_dtime.between(start_date, end_date))
        log_entries = query.all()
        session.close()
        return [
        {
            'id': log_entry.id,
            'ip_address': log_entry.ip_address,
            'remote_logname': log_entry.remote_logname,
            'remote_user': log_entry.remote_user,
            'request_dtime': log_entry.request_dtime,
            'request_method': log_entry.request_method,
            'requested_url': log_entry.requested_url,
            'response_size': log_entry.response_size,
            'status_code': log_entry.status_code
        }
        for log_entry in log_entries
    ]

