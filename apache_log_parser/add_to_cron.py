import os
from app.app.utils import read_config

config = read_config()

script_path = config['Cron']['script_path']
schedule = config['Cron']['cron_schedule']

with open('cron_tasks.txt', 'w') as file:
    file.write(f'{schedule} python {script_path}\n')

os.system('crontab cron_tasks.txt')
os.remove('cron_tasks.txt')
