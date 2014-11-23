from py2neo import neo4j, node, rel

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