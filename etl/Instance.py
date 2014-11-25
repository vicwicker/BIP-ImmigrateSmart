import utils

from py2neo import node, rel

from Configuration import Configuration
from Neo4jDriver import Neo4jDriver
from ContentReader import ContentReader

class Instance:
    
    def __init__(self, config_name):
        self.config = Configuration(config_name)
        
    def run(self):
        # Extract
        def extract():
            if self.config.file_type == 'csv':
                return ContentReader.csv(self.config.file_uri, self.config.delimiter)
            elif self.config.file_type == 'xls':
                return ContentReader.xls(self.config.file_uri)
            elif self.config.file_type == 'html':
                return ContentReader.html(self.config.file_uri, self.config.config_name)
        
        # Transform
        def transform(data):
            transformed = []
            filtered = filter(lambda row: row[self.config.country_in].lower() in Configuration.filters, data)
            for row in filtered:
                current = {'country':row[self.config.country_in], 'values':{}}
                for c in self.config.columns:
                    current['values'][utils.to_str(c['property'])] = row[int(c['id'])] 
                transformed.append(current)
            return transformed

        # Load in Neo4j
        def load(data):
            neo4j = Neo4jDriver()
            batch = neo4j.openBatch()
            
            for row in data:
                country = batch.create(node(name = row['country']))
                for value in row['values']:
                    criteria = batch.create(node(criteria = value))
                    fact = batch.create(node(value = row['values'][value]))
                    batch.create(rel(country, 'has_criteria', criteria))
                    batch.create(rel(criteria, 'has_value', fact))
            
            neo4j.submitBatch()
            
        data = extract()
        data = transform(data)
        load(data)
        
        # Print it out!
        #for row in data:
        #    for value in row['values']:
        #        print row['country']+' --[:'+value+']--> '+row['values'][value]