import csv, xlrd
import config, sqlite3

from py2neo import neo4j, node, rel

# Function to read specific columns from a CSV file
def read_csv(file_uri, col_country, cols, filters, delimiter):
    file = open(file_uri, 'rb')
    reader = csv.reader(file, delimiter = str(delimiter))
    filtered = filter(lambda row: row[int(col_country)].lower() in filters, reader)
    result = []
    for row in filtered:
        country = {'country':row[int(col_country)], 'values':{}}
        for c in cols:
            country['values'][str(c['property'])] = row[int(c['id'])] 
        result.append(country)
    return result


######################
# Main Program Start #
######################

print 'Welcome to ImmigrateSmart Sample Data Flow!'

connection = sqlite3.connect(config.config_db)
    
c = connection.cursor()

instances = c.execute('SELECT * FROM instances WHERE name_config = \'Sample ETL\'')

instance_config = instances.fetchone()

# Load basic instance configuration properties

name_config = instance_config[0] # Name of this ETL configuration

column_country = instance_config[1] # Column in the CSV file where the country name is

file_uri = instance_config[2] # URI of the file to read

delimiter = instance_config[3] # Delimiter

header = instance_config[4] # Ignore header if there is

# Read Criteria-Column pairs (must be ordered by index)

columns = []

columns_to_read = c.execute('SELECT * FROM columns WHERE name = \'Sample ETL\'')

for col in columns_to_read:
    columns.append({'id':col[1], 'property':col[2]})

# Read Filter List (must match country name exactly, might have problems with UAE, USA, UK)

filter_on = []

filters = c.execute('SELECT * FROM filters')

for f in filters:
    filter_on.append(str(f[0]))

criteria_res = read_csv(file_uri, column_country, columns, filter_on, delimiter)

#for row in criteria_res:
#    for value in row['values']:
#        print row['country']+' --[:'+value+']--> '+row['values'][value]
        
graph_db = neo4j.GraphDatabaseService('http://localhost:7474/db/data')
batch = neo4j.WriteBatch(graph_db)

for row in criteria_res:
    country = batch.create(node(name = row['country']))
    for value in row['values']:
        fact = batch.create(node(value = row['values'][value]))
        batch.create(rel(country, value, fact))

batch.submit()