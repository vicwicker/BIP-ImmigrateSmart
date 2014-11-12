import csv, xlrd
import config, sqlite3
import urllib2

from py2neo import neo4j, node, rel

# Convert any object to String
def tostr (val):
    if (isinstance(val, float)):
        return str(round(val, 0))
    
    return val.encode('utf-8')
    
# Retrieve data from an Excel file
def read_excel (file_uri, col_country, cols, filters, delimiter):
    # Read Excel file from URL
    socket = urllib2.urlopen(file_uri)
    xlfile = xlrd.open_workbook(file_contents = socket.read())
    xlsheet = xlfile.sheet_by_index(0)
    
    rows = []
    for rownum in range(xlsheet.nrows):
        rows.append([tostr(val) for val in xlsheet.row_values(rownum)])
    
    filtered = filter(lambda row: row[int(col_country)].lower() in filters, rows)
    result = []
    for row in filtered:
        country = {'country':row[int(col_country)], 'values':{}}
        for c in cols:
            country['values'][str(c['property'])] = row[int(c['id'])] 
        result.append(country)
    return result

# Retrieve data from an Excel file
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

def execute_sample(config_name, file_type):
    connection = sqlite3.connect(config.config_db)
    c = connection.cursor()
    instances = c.execute('SELECT * FROM instances WHERE name_config = \'' + config_name + '\'')
    instance_config = instances.fetchone()
    
    # Load basic instance configuration properties
    name_config = instance_config[0] # Name of this ETL configuration
    column_country = instance_config[1] # Column in the CSV file where the country name is
    file_uri = instance_config[2] # URI of the file to read
    delimiter = instance_config[3] # Delimiter
    header = instance_config[4] # Ignore header if there is
    
    # Read Criteria-Column pairs (must be ordered by index)
    columns = []
    columns_to_read = c.execute('SELECT * FROM columns WHERE name = \'' + config_name + '\'')
    for col in columns_to_read:
        columns.append({'id':col[1], 'property':col[2]})
    
    # Read Filter List (must match country name exactly, might have problems with UAE, USA, UK)
    filter_on = []
    filters = c.execute('SELECT * FROM filters')
    for f in filters:
        filter_on.append(str(f[0]))
    
    criteria_res = []
    if (file_type == 'csv'):
        criteria_res = read_csv(file_uri, column_country, columns, filter_on, delimiter)
    elif (file_type == 'excel'):
        criteria_res = read_excel(file_uri, column_country, columns, filter_on, delimiter)
    
    print '-----------------'
    print config_name
    print '-----------------'

    for row in criteria_res:
        for value in row['values']:
            print row['country']+' --[:'+value+']--> '+row['values'][value]
            
    graph_db = neo4j.GraphDatabaseService('http://localhost:7474/db/data')
    batch = neo4j.WriteBatch(graph_db)
    
    for row in criteria_res:
        country = batch.create(node(name = row['country']))
        for value in row['values']:
            fact = batch.create(node(value = row['values'][value]))
            batch.create(rel(country, value, fact))
    
    batch.submit()

######################
# Main Program Start #
######################

print 'Welcome to ImmigrateSmart Sample Data Flow!'

#CSV Sample
execute_sample('Sample ETL', 'csv')

#Excel Sample
execute_sample('Sample ETL Excel', 'excel')