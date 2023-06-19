import configparser
import re
from datetime import datetime

from db import Database
from models import ApacheLog

config = configparser.ConfigParser()
config.read('config.ini')
db = Database(config['Database'])

def parse_log_line(log_line):
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

def parse_apache_logs(log_file_path):
    with open(log_file_path, 'r') as file:
        for line in file:
            log_data = parse_log_line(line)
            if log_data:
                db.create_log_entry(*log_data)

if __name__ == '__main__':
    ApacheLog.__table__.create(db.engine, checkfirst=True)
    log_file_path = config['App']['log_dir'] + '/' + config['App']['log_file_mask']
    parse_apache_logs(log_file_path)
