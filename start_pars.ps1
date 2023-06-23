
$scriptPath = "C:\Users\lolis\python projects\apache_log_parser\apache_log_parser\app\app\log_parser.py"
$taskName = "apache_parser"
$action = New-ScheduledTaskAction -Execute "python.exe" -Argument $scriptPath
$trigger = New-ScheduledTaskTrigger -Daily -At "10:30"
$settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries
Register-ScheduledTask -TaskName $taskName -Action $action -Trigger $trigger -Settings $settings
    