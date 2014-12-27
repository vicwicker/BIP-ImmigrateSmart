require 'neo4j'

class Neo4jDriver
    def self.getCountryNames
        Neo4j::Session.open(:server_db)
        result = Neo4j::Session.query('
            START n = node:node_auto_index(schema = \'country\')
            MATCH n-[:has_instance]->m
            RETURN m.name')
        countries = []
        result.each do |e|
            countries.push(e[:'m.name'])
        end
        return countries
    end
    
    def self.getCriteriaNamesForCountry(country)
        Neo4j::Session.open(:server_db)
        result = Neo4j::Session.query('
            START n = node:node_auto_index(schema = \'country\')
            MATCH n-[:has_instance]->m-[:has_criteria]->p-[r]->q
            WHERE m.name = \''+country+'\'
            RETURN p.criteria, type(r), q.value')
        values = []
        result.each do |e|
            values.push({
                :criteria_1 => e[:'p.criteria'], 
                :criteria_2 => e[:'type(r)'],
                :value      => e[:'q.value'] 
            })
        end
        return values
    end
    
    def self.existsUser?(email)
        Neo4j::Session.open(:server_db)
        result = Neo4j::Session.query('
            START n = node:node_auto_index(schema = \'user\')
            MATCH n-[:has_instance]->m
            WHERE m.email = \''+email+'\'
            RETURN COUNT(*) AS count')
        if result.first[:'count'] > 0
            return true
        end
        
        return false
    end
    
    def self.validCredentials?(email, password)
        Neo4j::Session.open(:server_db)
        result = Neo4j::Session.query('
            START n = node:node_auto_index(schema = \'user\')
            MATCH n-[:has_instance]->m
            WHERE m.email = \''+email+'\' AND m.password = \''+password+'\'
            RETURN m')
        user = Hash.new
        if result.first != nil
            user[:'name']               = result.first[:'m'][:'name']
            user[:'gender']             = result.first[:'m'][:'gender']
            user[:'email']              = result.first[:'m'][:'email']
            user[:'m_status']           = result.first[:'m'][:'m_status']
            user[:'profession']         = result.first[:'m'][:'profession']
            user[:'education']          = result.first[:'m'][:'education']
            user[:'origin_country']     = result.first[:'m'][:'origin_country']
            user[:'residence_country']  = result.first[:'m'][:'residence_country']
            user[:'native_language']    = result.first[:'m'][:'native_language']
            user[:'other_lang']         = result.first[:'m'][:'other_lang']
        end
        
        return user
    end
    
    def self.createUser(attributes)
        Neo4j::Session.open(:server_db)
        schema_user = Neo4j::Session.query('
            START n = node:node_auto_index(schema = \'user\')
            RETURN n').first[:'n']
            
        Neo4j::Transaction.run do
            user = Neo4j::Node.create(
              :name               => attributes[:'name'],
              :gender             => attributes[:'gender'],
              :email              => attributes[:'email'],
              :password           => attributes[:'password'],
              :m_status           => attributes[:'m_status'],
              :profession         => attributes[:'profession'],
              :education          => attributes[:'education'],
              :origin_country     => attributes[:'origin_country'],
              :residence_country  => attributes[:'residence_country'],
              :native_language    => attributes[:'native_language'],
              :other_lang         => attributes[:'other_lang'])
              
            schema_user.create_rel(:has_instance, user)
        end
    end
end
