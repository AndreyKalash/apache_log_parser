import datetime
import subprocess
import os

from app.app.utils import read_config

def add_to_taskmngr():
    config = read_config()

    script_path = config['Cron']['script_path']
    main_dir_path = config['Cron']['main_dir_path']
    time = config['Cron']['win_schedule']
    task_name = config['Cron']['task_name']
    script_file = config['Cron']['script_file']


    powershell_script = f'''
$scriptPath = "{script_path}"
$taskName = "{task_name}"
$action = New-ScheduledTaskAction -Execute "python.exe" -Argument $scriptPath
$trigger = New-ScheduledTaskTrigger -Daily -At "{time}"
$settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries
Register-ScheduledTask -TaskName $taskName -Action $action -Trigger $trigger -Settings $settings
    '''
    with open(script_file, 'w') as f:
        f.write(powershell_script)

    subprocess.run(["powershell.exe", "-Command", f"{main_dir_path + '/' + script_file}"])

    
add_to_taskmngr()