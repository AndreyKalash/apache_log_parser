# Агрегатор Apache access logs

Агрегатор Apache access logsg - это приложение, которое собирает данные из логов доступа веб-сервера Apache и сохраняет их в базе данных.
# Функционал
- Сохраненных access логов в базе данных, с возможностью группировки по IP-адресу, дате и выборке по промежутку дат.
- Просмотр данных через графический интерфейс.
- Наличие API для получения данных в формате JSON с возможностью фильтрации и группировки по IP-адресу.
- Конфигурация через файл настроек, включающие необходимые настройки для приложения.
- Опциональная аутентификация пользователей с использованием базы данных.
# Требования
- Python 3.x
- База данных: MySQL
# Установка
1. Склонируйте репозиторий: ```git clone https://github.com/AndreyKalash/apache_log_parser.git```
2. Установите необходимые зависимости, запустив команду ```pip install -r requirements.txt```
3. Откройте ```config.ini``` для [настройки конфигурационного файла](#настройка-конфигурационного-файла).

# Использование
После [настройки конфигурационного файла](#настройка-конфигурационного-файла) запустите:
- ```start_app.py``` - если вам нужно основное приложение с графическим интерфейсом
- ```start_api.py``` - если нужно только запустить api
- ```apache_log_parser\add_to_cron.py``` - для добавления парсера в cron с соответсвующими [настройками](#сron)
- ```apache_log_parser\add_to_win_tskmngr.py``` - для добавления парсера в планировщик задач Windows с соответсвующими [настройками](#сron)

## Документация API
- ```/api/logs``` - Выборка всех данных 
- ```/api/logs/ip``` - Группировка по ip
- ```/api/logs/date``` - Группировка по датам
- ```/api/logs/date_range?start_date={Начальная дата}&end_date={Конечная дата}``` - Выборка всех данных в промежутке выбранных дат
  

# Настройка конфигурационного файла 
### ! - Обязательная настройка
### [App]
- ```log_dir``` = Полный путь для папки с логами !
- ```log_file_mask``` = Имя файла с логами !
### [Database]
- ```host``` = Хост(hostname) базы данных !
- ```port``` = Порт(port) базы данных. По умолчанию - ```3306``` !
- ```database``` = Название базы данных !
- ```username``` = Имя пользователя(username) !
- ```password``` = Пароль !
- ```create_db_if_not_exist``` = ```True```|```False``` (Создает базу данных если ее не существует. По умолчанию - ```False```)
- ```dateformat``` = Формат даты. По умолчанию - ```'dd.mm.yyyy'```
- ```re_mask``` = Regexp маска для логов
### [Cron]
- ```script_path``` = Полный путь до ```log_parser.py``` (```your\path\..\apache_log_parser\app\log_parser.py```) !
- ```cron_schedule``` = [Время автозапуска парсера для cron](https://crontab.guru/). По умолчанию - ```30 10 * * *```
- ```win_schedule``` = Время для автозапуска парсера для планировцика задач windows. По умолчанию - ```10:30```
- ```task_name``` = Название задачи. По умолчаниию - ```apache_parser``` 
- ```script_file``` = Название файла создания задачи для windows. По умолчанию - ```start_pars.ps1```
- ```main_dir_path``` = ```Путь до папки apache_log_parser``` ````your\path\..\apache_log_parser```

  
