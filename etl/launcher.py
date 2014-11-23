from SQLiteDriver import SQLiteDriver
from Instance import Instance
from Configuration import Configuration

Configuration.load_filters()

sql = SQLiteDriver()

instances = sql.execute('SELECT DISTINCT config_name FROM '+SQLiteDriver.config_instances_table)

for instance in instances:
        Instance(instance[0]).run()
        
sql.close()