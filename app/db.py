import re
from datetime import datetime

from sqlalchemy import create_engine
from sqlalchemy import func
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import sessionmaker

from app.models import ApacheLog, Base

class Database:
    def __init__(self, config):
        self.config = config
        self.engine = create_engine(
            f"mysql+mysqlconnector://{config['username']}:{config['password']}@{config['host']}:{config['port']}/{config['database']}",
            pool_pre_ping=True,
        )
        self.Session = sessionmaker(bind=self.engine)

    def create_log_entry(self, ip_address, date):
        session = self.Session()
        log_entry = ApacheLog(ip_address=ip_address, request_time=date)
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
        query = session.query(func.date(ApacheLog.request_time), func.count(ApacheLog.request_time)).group_by(func.date(ApacheLog.request_time))
        log_entries = query.all()
        session.close()
        return log_entries

    def get_log_entries_in_date_range(self, start_date, end_date):
        session = self.Session()
        query = session.query(ApacheLog).filter(ApacheLog.request_time.between(start_date, end_date))
        log_entries = query.all()
        session.close()
        return log_entries

    def parse_apache_logs(self, log_file_path):
        with open(log_file_path, 'r') as file:
            for line in file:
                log_data = self.parse_log_line(line)
                if log_data:
                    self.create_log_entry(*log_data)

    def parse_log_line(self, log_line):
        pattern = r'^(?P<ip_address>\S+) \S+ \S+ \[(?P<timestamp>[^\]]+)\] "(?P<request>[^"]+)" (?P<status_code>\d+) (?P<response_size>\d+|-)$'
        match = re.match(pattern, log_line)
        if match:
            ip_address = match.group('ip_address')
            timestamp = match.group('timestamp')
            request = match.group('request')
            status_code = int(match.group('status_code'))
            response_size = int(match.group('response_size')) if match.group('response_size') != '-' else None

            try:
                request_time = datetime.strptime(timestamp, '%d/%b/%Y:%H:%M:%S %z')
                return ip_address, request_time, request, status_code, response_size
            except ValueError:
                return None

        return None