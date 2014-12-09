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
                            extras TEXT)''')
                
        self.execute('''CREATE TABLE '''+SQLiteDriver.config_columns_table+''' (
                            config_name TEXT,
                            criteria TEXT,
                            column TEXT,
                            fact TEXT)''')
                            
        self.execute('''CREATE TABLE '''+SQLiteDriver.config_filters_table+''' (
                            country TEXT)''', True)
        
    def drop(self):
        self.execute('DROP TABLE '+SQLiteDriver.config_instances_table)
        self.execute('DROP TABLE '+SQLiteDriver.config_columns_table)
        self.execute('DROP TABLE '+SQLiteDriver.config_filters_table, True)
        
    def filters(self, reset = False):
        if reset:
            self.execute('DROP TABLE '+SQLiteDriver.config_filters_table)
            self.execute('''CREATE TABLE '''+SQLiteDriver.config_filters_table+''' (
                            country TEXT)''', True)
        
# Main program
if __name__ == "__main__":
    sql = SQLiteDriver()
    
    for i in range(1, len(sys.argv)):
        cmd = sys.argv[i]
        if cmd == '-create':
            sql.create()
        elif cmd == '-drop':
            sql.drop()
        elif cmd == '-sample':
            sample()
        else:
            print cmd+' is not a valid command.'
            
    sql.close()