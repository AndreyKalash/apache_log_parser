from flask import Flask, jsonify, request
try:
    from apache_log_parser.app.utils import db_connect
except:
    from utils import db_connect


db = db_connect()
app = Flask(__name__)

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
    
if __name__ == '__main__':
    app.run()