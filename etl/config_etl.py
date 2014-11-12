import sys, sqlite3

config_db = './config/config_db.db'

config_instances_table = 'instances'

config_columns_table = 'columns'

config_filters_table = 'filters'

filters_file = './config/filters.list'

def create():
    connection = sqlite3.connect(config_db)
    
    c = connection.cursor()
    
    c.execute('''CREATE TABLE '''+config_instances_table+''' (
                name_config TEXT,
                column_country TEXT,
                file_uri TEXT,
                delimiter TEXT,
                header TEXT
            )''')
            
                            
                
    c.execute('''CREATE TABLE '''+config_columns_table+''' (
                name TEXT,
                column_value TEXT,
                name_value TEXT
            )''')
            
    connection.commit()
    
    connection.close()
    
def drop():
    connection = sqlite3.connect(config_db)
    
    c = connection.cursor()
    
    c.execute('DROP TABLE '+config_instances_table)
    c.execute('DROP TABLE '+config_columns_table)
    c.execute('DROP TABLE '+config_filters_table)
    
    connection.commit()
    
    connection.close()
    
def filters(drop = False):
    connection = sqlite3.connect(config_db)
    
    c = connection.cursor()
    
    if drop:
        c.execute('DROP TABLE '+config_filters_table)
    
    c.execute('''CREATE TABLE '''+config_filters_table+''' (
                country TEXT
            )''')
            
    with open(filters_file, 'r') as f:
        lines = f.readlines()
        for line in lines:
            countries = line.split(';')
            for country in countries:
                # Additional chracter parsing will be needed before insertion
                c.execute('''INSERT INTO '''+config_filters_table+'''
                    VALUES (\''''+country.strip().lower()+'''\')''')
    
    connection.commit()
    
    connection.close()
    
def sample():
    connection = sqlite3.connect(config_db)
    
    c = connection.cursor()
    
    c.execute('DELETE FROM '+config_instances_table)
    c.execute('DELETE FROM '+config_columns_table)
    c.execute('DELETE FROM '+config_filters_table)
    
    
    c.execute('''INSERT INTO '''+config_instances_table+'''
                VALUES (
                    'Sample ETL',
                    '0',
                    'workingHours.csv',
                    ';',
                    'yes'
                )''')
            
    c.execute('''INSERT INTO '''+config_columns_table+'''
                VALUES (
                    'Sample ETL',
                    '2',
                    'maximum_working_days_per_week'
                )''')
                
    c.execute('''INSERT INTO '''+config_columns_table+'''
                VALUES (
                    'Sample ETL',
                    '10',
                    'paid_annual_leave'
                )''')            
                
    
    connection.commit()
    
    connection.close()
    
for i in range(1, len(sys.argv)):
    cmd = sys.argv[i]
    if cmd == '-create':
        create()
        filters()
    elif cmd == '-drop':
        drop()
    elif cmd == '-filters':
        filters(True)
    elif cmd == '-sample':
        sample()
    else:
        print cmd+' is not a valid command.'