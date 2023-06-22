from datetime import date, datetime
from get_dformat import set_date_format
from models import ApacheLog, Base
from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker



class Database:
    def __init__(self, config):
        self.config = config
        self.engine = create_engine(
            f"mysql+mysqlconnector://{config['username']}:{config['password']}@{config['host']}:{config['port']}/{config['database']}",
            pool_pre_ping=True,
        )
        self.Session = sessionmaker(bind=self.engine)
        self.date_format = set_date_format(config['dateformat'])

        Base.metadata.create_all(self.engine, checkfirst=True)

    

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