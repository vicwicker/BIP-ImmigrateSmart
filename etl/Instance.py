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
                return ContentReader.csv(self.config.file_uri, self.config.extras, self.config.headers)
            elif self.config.file_type == 'xls':
                return ContentReader.xls(self.config.file_uri, int(self.config.extras), self.config.headers)
            elif self.config.file_type == 'html':
                return ContentReader.html(self.config.file_uri, self.config.config_name, int(self.config.extras), self.config.headers)
        
        # Transform
        def transform(data):
            transformed = []
            if self.config.is_multi:
                data = filter(lambda row: row[self.config.country_in].lower() in Configuration.filters, data)
            else:
                for row in data:
                    row.append(self.config.country_in)
                self.config.country_in = len(data[0])-1
            for row in data:
                current = {'country':row[self.config.country_in], 'criterias':{}}
                for c in self.config.columns:
                    criteria = utils.to_str(c['criteria'])
                    if not criteria in current['criterias']:
                        current['criterias'][criteria] = [criteria, None, utils.to_str(c['category'])]
                    current['criterias'][criteria][c['fact']] = row[int(c['column'])]
                transformed.append(current)
                
            return transformed

        # Load in Neo4j
        def load(data):
            neo4j = Neo4jDriver()
            batch = neo4j.openBatch()
            for row in data:
                #country = batch.create(node(name = row['country']))
                country = neo4j.get_country(row['country'])
                for criteria in row['criterias']:
                    #print row['country']+' --[:has_criteria]-> '+criteria+' --[:' + row['criterias'][criteria][0] + ']-> '+row['criterias'][criteria][1]
                    criteria_node = batch.create(node(criteria = criteria))
                    fact_node = batch.create(node(value = row['criterias'][criteria][1]))
                    batch.create(rel(country, 'has_criteria', criteria_node))
                    batch.create(rel(criteria_node, 'is_category', neo4j.get_category(row['criterias'][criteria][2])))
                    batch.create(rel(criteria_node, row['criterias'][criteria][0], fact_node))
            
            neo4j.submitBatch()
            
        data = extract()
        data = transform(data)
        load(data)
        
        # Print it out!
        # for row in data:
        #   for criteria in row['criterias']:
        #        print row['country']+' --[:has_criteria]--> ' \
        #            +criteria+' --[:'+row['criterias'][criteria][0]+']--> ' \
        #                +row['criterias'][criteria][1]
