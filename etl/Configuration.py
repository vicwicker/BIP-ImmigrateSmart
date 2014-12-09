import re, distance
import utils


from SPARQLWrapper import SPARQLWrapper, JSON

from SQLiteDriver import SQLiteDriver

class Configuration:
    
    # File from which obtaining the country filter list
    filters_file = './config/filters.list'
    
    # Filters will be shared through all instance
    filters = []
    
    @staticmethod
    def update_filters():
        def potential_names(country, subject):
            def clean(start, length = 1):
                name = cleaner.sub('', words[start])
                for i in range(1, length-1):
                    name = name+' '+cleaner.sub('', words[start+i])
                # If what we are cleaning is a concatenation of words that finishes
                # with an exception we do not include such exception
                if length > 1 and not words[start+length-1] in exceptions:
                    name = name+' '+cleaner.sub('', words[start+length-1])
                return name.strip()
                
            sparql = SPARQLWrapper("http://dbpedia.org/sparql")
            sparql.setQuery('''
                SELECT ?abstract
                WHERE {
                    <'''+subject+'''> dbpedia-owl:abstract ?abstract .
                    FILTER (lang(?abstract) = 'en')
                }
            ''')
            
            sparql.setReturnFormat(JSON)
            results = sparql.query().convert()
            
            # Tags about pronunciation (e.g., UK: this, US: this)
            tag_removal = re.compile('[A-Za-z]+:')
            cleaner = re.compile('\W+')
            
            words = tag_removal.sub('', results['results']['bindings'][0]['abstract']['value'].split('.')[0]).split()
            
            exceptions = ['of', 'and', 'de']
            
            start = 0
            length = 0
            current = 0
            
            names = []
            
            for word in words:
                word = word.strip('"') # To avoid emphasis, but this is too hard-coded
                if word.isupper(): # If acronym
                    if length > 0: # If something was already being built then flush it
                        names.append({'name':clean(start, length), 'score':0.0})
                        length = 0
                    names.append({'name':clean(current), 'score':0.0})
                elif word[0].isupper(): # If current word starts with uppercase then it 
                                        # must be considered as part of a potential name
                    if length == 0:
                        start = current
                    length = length+1
                elif word in exceptions and length > 0: # If current word is an exception
                                                        # word but there is something
                                                        # already being built, we include it
                    length = length+1
                elif length > 0:    # If current word is not valid but something has been
                                    # built then it is time to flush it
                    names.append({'name':clean(start, length), 'score':0.0})
                    length = 0
                    
                current = current+1
            
            country = country.replace('_', ' ')
            
            for name in names:
                if name['name'].isupper():
                    name['score'] = 0.0
                else:
                    terms = name['name'].split(' ')
                    min_distance = 10L
                    for t in terms:
                        current_distance = distance.levenshtein(t, country)/float(len(country))
                        if current_distance < min_distance:
                            name['score'] = current_distance
            
            avg = 0    
            
            for name in names:
                avg = avg+name['score']
                
            avg = avg/float(len(names))
            
            result = []
            
            for name in names:
                if (name['score'] <= avg or name['score'] <= 0.9) and name['name'] != country:
                    result.append(name['name'])
            
            print result
            return result
            
        sql = SQLiteDriver()
        sql.filters(True)
        with open(Configuration.filters_file, 'r') as f:
            lines = f.readlines()
            for line in lines:
                aux = line.split(';')
                country = aux[0].strip()
                subject = aux[1].strip()
                names = [country]+potential_names(country, subject)
                for country in names:
                    sql.execute('''INSERT INTO '''+SQLiteDriver.config_filters_table+'''
                        VALUES (\''''+country.strip().lower()+'''\')''')
        
        sql.commit()
    
    @staticmethod
    def load_filters():
        sql = SQLiteDriver()
        filters_in_db = sql.execute('SELECT * FROM filters')
        for f in filters_in_db:
            Configuration.filters.append(utils.to_str(f[0]))
            
        sql.close()
        
    # NOTE: Only works for unidimensional criteria
    @staticmethod
    def insert(config_name, source_file, source_file_type, extras, countries_col, criteria_cols):
        sql = SQLiteDriver()
        
        sql.execute('''INSERT INTO '''+SQLiteDriver.config_instances_table+''' VALUES (
                        \''''+config_name+'''\',
                        \''''+countries_col+'''\',
                        \''''+source_file+'''\',
                        \''''+source_file_type+'''\',
                        \''''+extras+'''\')''')
            
        for k in criteria_cols:
           sql.execute('''INSERT INTO '''+SQLiteDriver.config_columns_table+''' VALUES (
                            \''''+config_name+'''\',
                            \''''+criteria_cols[k]+'''\',
                            \''''+k+'''\',
                            'yes')''')
                            
        sql.commit()
        return Configuration(config_name)
            
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
        self.extras   = None                    # Delimiter
        if not config[4] is None:
            self.extras = utils.to_str(config[4])
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

# Main program
if __name__ == "__main__":
    Configuration.update_filters()