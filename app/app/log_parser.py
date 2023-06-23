import re
from datetime import datetime

from app.app.utils import Logger, db_connect, read_config

config = read_config()
db = db_connect()
logger = Logger()

def parse_log_line(log_line):
    pattern = config['Database']['re_mask']
    match = re.match(rf'{pattern}', log_line)
    if match:
        ip_address = match.group('ip_address')
        remote_logname = match.group('remote_logname') if match.group('remote_logname') != '-' else None
        remote_user = match.group('remote_user') if match.group('remote_user') != '-' else None
        timestamp = match.group('timestamp')
        request_method = match.group('request_method')
        requested_url = match.group('requested_url')
        status_code = int(match.group('status_code'))
        response_size = int(match.group('response_size')) if match.group('response_size') != '-' else None

        try:
            request_time = datetime.strptime(timestamp, '%d/%b/%Y:%H:%M:%S %z')
            return ip_address, remote_logname, remote_user, request_time, request_method, requested_url, status_code, response_size
        except ValueError:
            return None

    return None

def parse_apache_logs(log_file_path):
    with open(log_file_path, 'r') as file:
        count = 0
        for line in file:
            log_data = parse_log_line(line)
            if log_data:
                logger.message(log_data)
                try:
                    db.create_log_entry(*log_data)
                    count+=1
                except:
                    logger.error('Ошибка при добавлении данных')
        logger.message(f'Добавлено записей: {count}')
        

if __name__ == '__main__':
    # ApacheLog.__table__.create(db.engine, checkfirst=True)
    log_file_path = config['App']['log_dir'] + '/' + config['App']['log_file_mask']
    parse_apache_logs(log_file_path)
  
    
