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
                            fact_column TEXT,
                            fact_name TEXT)''', True)
        
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
                   
    # XLS configuration instance sample - Minimum Wage / Paid Annual Leave
    sql.execute('''INSERT INTO '''+SQLiteDriver.config_instances_table+''' VALUES (
                        'doingbusiness',
                        '0',
                        'http://www.doingbusiness.org/~/media/GIAWB/Doing%20Business/Documents/Miscellaneous/LMR-DB15-DB14-service-sector-data-points-and-details.xlsx',
                        'xls',
                        ';')''')
            
    sql.execute('''INSERT INTO '''+SQLiteDriver.config_columns_table+''' VALUES (
                        'doingbusiness',
                        '4',
                        'minimum_wage')''')
                
    sql.execute('''INSERT INTO '''+SQLiteDriver.config_columns_table+''' VALUES (
                        'doingbusiness',
                        '16',
                        'paid_annual_leave')''', True)  
                        
    # HTML configuration instance sample 1 - Foreign Worker Salaries
    sql.execute('''INSERT INTO '''+SQLiteDriver.config_instances_table+''' VALUES (
                        'nationmaster',
                        '1',
                        'http://www.nationmaster.com/country-info/stats/People/Migration/Foreign-worker-salaries',
                        'html',
                        NULL)''')
            
    sql.execute('''INSERT INTO '''+SQLiteDriver.config_columns_table+''' VALUES (
                        'nationmaster',
                        '2',
                        'foreign_worker_salaries')''', True)
                        
    # HTML configuration instance sample - Area
    sql.execute('''INSERT INTO '''+SQLiteDriver.config_instances_table+''' VALUES (
                        'cia-area',
                        '1',
                        'https://www.cia.gov/library/publications/the-world-factbook/rankorder/2147rank.html?countryname=Australia&countrycode=as&regionCode=aus&rank=6#as',
                        'html',
                        NULL)''')
            
    sql.execute('''INSERT INTO '''+SQLiteDriver.config_columns_table+''' VALUES (
                        'cia-area',
                        '2',
                        'area')''', True)
                        
    # HTML configuration instance sample - Population
    sql.execute('''INSERT INTO '''+SQLiteDriver.config_instances_table+''' VALUES (
                        'cia-population',
                        '1',
                        'https://www.cia.gov/library/publications/the-world-factbook/rankorder/2119rank.html?countryname=Australia&countrycode=as&regionCode=aus&rank=56#as',
                        'html',
                        NULL)''')
            
    sql.execute('''INSERT INTO '''+SQLiteDriver.config_columns_table+''' VALUES (
                        'cia-population',
                        '2',
                        'population')''', True)
                        
    # HTML configuration instance sample - GDP per capita
    sql.execute('''INSERT INTO '''+SQLiteDriver.config_instances_table+''' VALUES (
                        'cia-gdp-per-capita',
                        '1',
                        'https://www.cia.gov/library/publications/the-world-factbook/rankorder/2004rank.html?countryname=Australia&countrycode=as&regionCode=aus&rank=21#as',
                        'html',
                        NULL)''')
            
    sql.execute('''INSERT INTO '''+SQLiteDriver.config_columns_table+''' VALUES (
                        'cia-gdp-per-capita',
                        '2',
                        'gdp-per-capita')''', True)

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