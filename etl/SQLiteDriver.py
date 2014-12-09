import sqlite3

class SQLiteDriver:
    
    # SQLite configuration DB
    config_db = './config/config_db.db'
    
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
