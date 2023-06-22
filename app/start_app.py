
# import database
import configparser
import re
from datetime import datetime

from flask import Flask, jsonify, request
from db import Database

app = Flask(__name__)
config = configparser.ConfigParser()
config.read('config.ini')
db = Database(config['Database'])


@app.route('/api/logs', methods=['GET'])
def get_logs():
    with app.app_context():
        log_entries = db.get_log_entries()
        logs = [log for log in log_entries]
        return jsonify(logs)

@app.route('/api/logs/ip', methods=['GET'])
def get_logs_by_ip():
    with app.app_context():
        log_entries = db.get_log_entries_by_ip()
        logs = [{'ip_address': str(log[0]), 'count': log[1]} for log in log_entries]
        return jsonify(logs)

@app.route('/api/logs/date', methods=['GET'])
def get_logs_by_date():
    with app.app_context():
        log_entries = db.get_log_entries_by_date()
        logs = [{'date': str(log[0]), 'count': log[1]} for log in log_entries]
        return jsonify(logs)

@app.route('/api/logs/date_range', methods=['GET'])
def get_logs_in_date_range():
    with app.app_context():
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        if start_date is None or end_date is None: return jsonify(error='Both start_date and end_date parameters are required.'), 400

        log_entries = db.get_log_entries_in_date_range(start_date, end_date)
        logs = [log for log in log_entries]
        return jsonify(logs)

def parse_log_line(log_line):
    pattern = config['Database']['re_mask']
    match = re.match(pattern, log_line)
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
        for line in file:
            log_data = parse_log_line(line)
            if log_data:
                db.create_log_entry(*log_data)

if __name__ == '__main__':
    # print(db.get_log_entries_in_date_range(start_date='17.05.2015', end_date='19.05.2015'))
    # print(db.get_log_entries_by_date())
    # ApacheLog.__table__.create(db.engine, checkfirst=True)
    # log_file_path = config['App']['log_dir'] + '/' + config['App']['log_file_mask']
    # parse_apache_logs(log_file_path)
    # pprint(db.get_log_entries_by_date())
    # pprint(get_logs_in_date_range(start_date='17.05.2015', end_date='19.05.2015'))
    app.run()
