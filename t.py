import subprocess

# Команда для просмотра задачи в планировщике задач Windows
command = 'schtasks /query /tn "Log Parser"'

# Запуск команды через subprocess и получение вывода
result = subprocess.run(command, shell=True, capture_output=True, text=True, encoding='utf-8')

# Вывод результатов
print(result.stdout)
