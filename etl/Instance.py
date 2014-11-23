import utils

from py2neo import node, rel

from Configuration import Configuration
from Neo4jDriver import Neo4jDriver
from ContentReader import ContentReader

class Instance:
    
    def __init__(self, config_name):
        self.config = Configuration(config_name)
        
    def run(self):
        def read():
            if self.config.file_type == 'csv':
                contents = ContentReader.csv(self.config.file_uri, self.config.delimiter)
            elif self.config.file_type == 'xls':
                contents = ContentReader.xls(self.config.file_uri)
                
            filtering = filter(lambda row: row[self.config.country_in].lower() in Configuration.filters, contents)
            result = []
            for row in filtering:
                country = {'country':row[self.config.country_in], 'values':{}}
                for c in self.config.columns:
                    country['values'][utils.to_str(c['property'])] = row[int(c['id'])] 
                result.append(country)
            return result

        to_import = read()
        # Print it out!
        for row in to_import:
            for value in row['values']:
                print row['country']+' --[:'+value+']--> '+row['values'][value]
                
        # Load it in Neo4j
        neo4j = Neo4jDriver()
        batch = neo4j.openBatch()
        
        for row in to_import:
            country = batch.create(node(name = row['country']))
            for value in row['values']:
                fact = batch.create(node(value = row['values'][value]))
                batch.create(rel(country, value, fact))
        
        neo4j.submitBatch()