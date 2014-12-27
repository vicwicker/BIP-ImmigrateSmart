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
        
# Main program
if __name__ == "__main__":
    def setup():
        neo4j = Neo4jDriver()
        
        batch = neo4j.openBatch()
        
        # Create schema level
        schema_country = batch.create(node(schema = 'country'))
        batch.create(node(schema = 'user'))
        
        with open(Configuration.filters_file, 'r') as f:
            lines = f.readlines()
            for line in lines:
                names = line.split(';')
                country = batch.create(node(name = names[0].strip()))
                batch.create(rel(schema_country, 'has_instance', country))
                for name in names:
                    country_1 = batch.create(node(name = name.strip()))
                    batch.create(rel(country, 'has_name', country_1))
                    
        neo4j.submitBatch()
        
    for i in range(1, len(sys.argv)):
        cmd = sys.argv[i]
        if cmd == '-setup':
            setup()
        else:
            print cmd+' is not a valid command.'