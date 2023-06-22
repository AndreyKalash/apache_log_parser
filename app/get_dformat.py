def set_date_format(strformat):
    formats = {
        'dd.mm.yyyy' : "%d.%m.%Y",
        'dd-mm-yyyy' : "%d-%m-%Y", 
        'dd/mm/yyyy' : "%d/%m/%Y", 
        'mm.dd.yyyy' : "%d.%m.%Y", 
        'mm-dd-yyyy' : "%d-%m-%Y",
        'mm/dd/yyyy' : "%d/%m/%Y",
        'yyyy.mm.dd' : '%Y.%m.%d',
        'yyyy-mm-dd' : '%Y-%m-%d',
        'yyyy/mm/dd' : '%Y/%m/%d'
    }
    return formats.get(strformat, "%d.%m.%Y")