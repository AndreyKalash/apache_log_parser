import datetime
import subprocess
import os

from app.utils import read_config

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

    try:
        with open(script_file, 'w') as f:
            f.write(powershell_script)
        path_ps_file = main_dir_path + "\\" + script_file
        subprocess.run(["powershell.exe", "-Command", f"{path_ps_file}"])
        os.remove(path_ps_file)
    except:
        print(path_ps_file, 'Проверьте правильность написания имени, а также наличие и правильность пути, после чего повторите попытку.')
    

    
add_to_taskmngr()