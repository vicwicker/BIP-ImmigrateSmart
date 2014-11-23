import sys, sqlite3

class SQLiteDriver:
    
    # SQLite configuration DB
    config_db = './config/config_db.db'

    # Configuration instance table
    config_instances_table = 'instances'

    # Configuration read column table
    config_columns_table = 'columns'

    # Filters table (i.e., list of countries)
    config_filters_table = 'filters'
    
    # File from which obtaining the country filter list
    filters_file = './config/filters.list'
    
    def __init__(self):
        self.connection = sqlite3.connect(SQLiteDriver.config_db)
        self.cursor = self.connection.cursor()
        
    # Executes the statement
    def execute(self, statement, commit = False):
        result = self.cursor.execute(statement)
        if commit:
            self.commit()
        return result
        
    # Just in case we puntually need to make a single commit
    def commit(self):
        self.connection.commit()
        
    # Closes the connection no longer needed
    def close(self):
        self.connection.close()
        
    # Predefined functionalities
    def create(self):
        self.execute('''CREATE TABLE '''+SQLiteDriver.config_instances_table+''' (
                            config_name TEXT,
                            country_in TEXT,
                            file_uri TEXT,
                            file_type TEXT,
                            delimiter TEXT)''')
                
        self.execute('''CREATE TABLE '''+SQLiteDriver.config_columns_table+''' (
                            config_name TEXT,
                            fact_name TEXT,
                            fact_column TEXT)''', True)
        
    def drop(self):
        self.execute('DROP TABLE '+SQLiteDriver.config_instances_table)
        self.execute('DROP TABLE '+SQLiteDriver.config_columns_table)
        self.execute('DROP TABLE '+SQLiteDriver.config_filters_table, True)
        
    def filters(self, drop = False):
        if drop:
            self.execute('DROP TABLE '+SQLiteDriver.config_filters_table)
    
        self.execute('''CREATE TABLE '''+SQLiteDriver.config_filters_table+''' (
                            country TEXT)''')
            
        with open(SQLiteDriver.filters_file, 'r') as f:
            lines = f.readlines()
            for line in lines:
                countries = line.split(';')
                for country in countries:
                    # Additional chracter parsing will be needed before insertion
                    self.execute('''INSERT INTO '''+SQLiteDriver.config_filters_table+'''
                        VALUES (\''''+country.strip().lower()+'''\')''')
        
        self.commit()
            
        
# Main program
sql = SQLiteDriver()

def sample():
    sql.execute('DELETE FROM '+SQLiteDriver.config_instances_table)
    sql.execute('DELETE FROM '+SQLiteDriver.config_columns_table)
    
    # CSV configuration instance sample
    sql.execute('''INSERT INTO '''+SQLiteDriver.config_instances_table+''' VALUES (
                        'Sample ETL',
                        '0',
                        'workingHours.csv',
                        'csv',
                        ';')''')
            
    sql.execute('''INSERT INTO '''+SQLiteDriver.config_columns_table+''' VALUES (
                        'Sample ETL',
                        '2',
                        'maximum_working_days_per_week')''')
                
    sql.execute('''INSERT INTO '''+SQLiteDriver.config_columns_table+''' VALUES (
                        'Sample ETL',
                        '10',
                        'paid_annual_leave')''')     
                   
    # XLS configuration instance sample 
    sql.execute('''INSERT INTO '''+SQLiteDriver.config_instances_table+''' VALUES (
                        'Sample ETL Excel',
                        '0',
                        'http://www.doingbusiness.org/~/media/GIAWB/Doing%20Business/Documents/Miscellaneous/LMR-DB15-DB14-service-sector-data-points-and-details.xlsx',
                        'xls',
                        ';')''')
            
    sql.execute('''INSERT INTO '''+SQLiteDriver.config_columns_table+''' VALUES (
                        'Sample ETL Excel',
                        '4',
                        'minimum_wage')''')
                
    sql.execute('''INSERT INTO '''+SQLiteDriver.config_columns_table+''' VALUES (
                        'Sample ETL Excel',
                        '16',
                        'paid_annual_leave')''', True)  

for i in range(1, len(sys.argv)):
    cmd = sys.argv[i]
    if cmd == '-create':
        sql.create()
        sql.filters()
    elif cmd == '-drop':
        sql.drop()
    elif cmd == '-filters':
        sql.filters(True)
    elif cmd == '-sample':
        sample()
    else:
        print cmd+' is not a valid command.'
        
sql.close()