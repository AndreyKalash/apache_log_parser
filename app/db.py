from sqlalchemy import create_engine
from sqlalchemy import func
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import sessionmaker

from models import ApacheLog, Base

class Database:
    def __init__(self, config):
        self.config = config
        self.engine = create_engine(
            f"mysql+mysqlconnector://{config['username']}:{config['password']}@{config['host']}:{config['port']}/{config['database']}",
            pool_pre_ping=True,
        )
        self.Session = sessionmaker(bind=self.engine)

        Base.metadata.create_all(self.engine, checkfirst=True)

    def create_log_entry(self, ip_address, request_time, request, status_code, response_size):
        session = self.Session()
        log_entry = ApacheLog(ip_address=ip_address, request_dtime=request_time, request_method=request,
                              status_code=status_code, response_size=response_size)
        session.add(log_entry)
        session.commit()
        session.close()

    def get_log_entries(self, filters):
        session = self.Session()
        query = session.query(ApacheLog).filter_by(**filters)
        log_entries = query.all()
        session.close()
        return log_entries

    def get_log_entries_by_ip(self):
        session = self.Session()
        query = session.query(ApacheLog.ip_address, func.count(ApacheLog.ip_address)).group_by(ApacheLog.ip_address)
        log_entries = query.all()
        session.close()
        return log_entries

    def get_log_entries_by_date(self):
        session = self.Session()
        query = session.query(func.date(ApacheLog.request_dtime), func.count(ApacheLog.request_dtime)).group_by(
            func.date(ApacheLog.request_dtime))
        log_entries = query.all()
        session.close()
        return log_entries

    def get_log_entries_in_date_range(self, start_date, end_date):
        session = self.Session()
        query = session.query(ApacheLog).filter(ApacheLog.request_dtime.between(start_date, end_date))
        log_entries = query.all()
        session.close()
        return log_entries
