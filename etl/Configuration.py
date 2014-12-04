import re
import utils

from SQLiteDriver import SQLiteDriver

class Configuration:
    
    # Filters will be shared through all instance
    filters = []
    
    @staticmethod
    def load_filters():
        sql = SQLiteDriver()
        filters_in_db = sql.execute('SELECT * FROM filters')
        for f in filters_in_db:
            Configuration.filters.append(utils.to_str(f[0]))
            
        sql.close()
            
    # Instance methods
    def __init__(self, config_name):
        self.load(config_name)
        
    def load(self, config_name):
        sql = SQLiteDriver()
        
        config = sql.execute('SELECT * FROM instances WHERE config_name = \'' + config_name + '\'').fetchone()
        
        # Load basic instance configuration properties
        self.config_name = utils.to_str(config[0]) # Name of this ETL configuration
        self.country_in  = str(config[1])          # Column in the CSV file where the country name is
        self.file_uri    = utils.to_str(config[2]) # URI of the file to read
        self.file_type   = utils.to_str(config[3]) # File type
        self.delimiter   = None                    # Delimiter
        if not config[4] is None:
            self.delimiter = utils.to_str(config[4])
        if not re.search('^[0-9]+$', self.country_in) is None:
            self.country_in = int(self.country_in)
            self.is_multi = True
        else:
            self.is_multi = False
        
        # Read Criteria-Column pairs (must be ordered by index)
        self.columns = []
        columns_to_read = sql.execute('SELECT * FROM columns WHERE config_name = \'' + config_name + '\'')
        for col in columns_to_read:
            to_append = {'criteria':col[1], 'column':col[2], 'fact':1}
            if col[3] != 'yes':
                to_append['fact'] = 0
            self.columns.append(to_append)
            
        sql.close()