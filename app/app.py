from db import Database
from models import ApacheLog
import configparser
import re
from datetime import datetime
from sqlalchemy.exc import OperationalError
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import text



config = configparser.ConfigParser()
config.read('config.ini')
db = Database(config['Database'])

ApacheLog.__table__.create(db.engine, checkfirst=True)

session = db.Session()
log_file_path = config['App']['log_dir'] + '/' + config['App']['log_file_mask']
with open(log_file_path, 'r') as file:
    logs = file.readlines()

log_pattern = re.compile(
    r'^(?P<ip_address>[^\s]+) - - \[(?P<request_dtime>[^\]]+)\] "(?P<request_method>[^\s]+) '
    r'(?P<requested_url>[^\s]+) [^\"]+" (?P<status_code>\d+) (?P<response_size>\d+)')

for line in logs:
    match = log_pattern.match(line)
    if match:
        log_data = match.groupdict()
        log_data['request_dtime'] = datetime.strptime(log_data['request_dtime'], '%d/%b/%Y:%H:%M:%S %z')
        log_entry = ApacheLog(**log_data)
        session.add(log_entry)

session.commit()
session.close()