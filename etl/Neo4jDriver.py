import sys

from py2neo import neo4j, node, rel

from Configuration import Configuration

class Neo4jDriver:
    
    # Neo4j Graph location
    neo4j_location = 'http://localhost:7474/db/data'
    
    # Creates an instance with an already serving connection
    def __init__(self):
        self.graph_db = neo4j.GraphDatabaseService(Neo4jDriver.neo4j_location)
        
    # Return a batch object into what bulk the data to import
    def openBatch(self):
        self.batch = neo4j.WriteBatch(self.graph_db)
        return self.batch
        
    # Apply batch object changes
    def submitBatch(self):
        self.batch.submit()
        
    # Run Default Cypher queries
    def get_country(self, name):
        country = neo4j.CypherQuery(self.graph_db, '''
            START n = node:node_auto_index(schema = \'country\') 
            MATCH n-[:has_instance]->m WHERE m.name = \''''+name+'''\' 
            RETURN m''').execute()
            
        if len(country) > 0:
            return country[0][0]
            
        return None
        
    def get_category(self, name):
        category = neo4j.CypherQuery(self.graph_db, '''
            START n = node:node_auto_index(schema = \'category\') 
            MATCH n-[:has_instance]->m WHERE m.name = \''''+name+'''\' 
            RETURN m''').execute()
            
        if len(category) > 0:
            return category[0][0]
            
        return None
        
    # Get list of countries
    def get_country_list(self):
        countries = neo4j.CypherQuery(self.graph_db, '''
            START n = node:node_auto_index(schema = \'country\')
            MATCH n-[:has_instance]->m
            RETURN m.name
            ORDER BY m.name''').execute()
            
        result = []
        for country in countries:
            result.append(country[0])
        return result
        
    # Get list of categories
    def get_category_list(self):
        categories = neo4j.CypherQuery(self.graph_db, '''
            START n = node:node_auto_index(schema = \'category\')
            MATCH n-[:has_instance]->m
            RETURN m.name
            ORDER BY m.name''').execute()
            
        result = []
        for category in categories:
            result.append(category[0])
        return result
        
# Main program
if __name__ == "__main__":
    def setup():
        neo4j = Neo4jDriver()
        
        batch = neo4j.openBatch()
        
        # Create schema level
        schema_country = batch.create(node(schema = 'country'))
        batch.create(node(schema = 'user'))
        schema_category = batch.create(node(schema = 'category'))
        
        with open(Configuration.filters_file, 'r') as f:
            lines = f.readlines()
            for line in lines:
                names = line.split(';')
                country = batch.create(node(name = names[0].strip()))
                batch.create(rel(schema_country, 'has_instance', country))
                for name in names:
                    country_1 = batch.create(node(name = name.strip()))
                    batch.create(rel(country, 'has_name', country_1))
                    
        with open(Configuration.categories_file, 'r') as f:
            lines = f.readlines()
            for line in lines:
                category = batch.create(node(name = line.strip()))
                batch.create(rel(schema_category, 'has_instance', category))
                    
        neo4j.submitBatch()
        
    for i in range(1, len(sys.argv)):
        cmd = sys.argv[i]
        if cmd == '-setup':
            setup()
        elif cmd == '-print':
            driver = Neo4jDriver()
            for country in driver.get_country_list():
                print country
            for category in driver.get_category_list():
                print category
        else:
            print cmd+' is not a valid command.'