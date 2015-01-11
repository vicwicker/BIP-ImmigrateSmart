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
            MATCH n-[:has_instance]->m-[:has_criteria]->p-[r]->q, p-[:is_category]->s
            WHERE m.name = \''+country+'\' AND TYPE(r) <> \'is_category\'
            RETURN p.criteria, s.name, TYPE(r), q.value, p.description')
        values = []
        result.each do |e|
            values.push({
                :criteria       => e[:'p.criteria'], 
                :category       => e[:'s.name'],
                :attribute      => e[:'TYPE(r)'],
                :value          => e[:'q.value'],
                :description    => e[:'p.description']
            })
        end
        return values
    end
    
    def self.getCountryCriteriaValue(country, criteria)
        Neo4j::Session.open(:server_db)
        result = Neo4j::Session.query('
            START n = node:node_auto_index(schema = \'country\')
            MATCH n-[:has_instance]->m-[:has_criteria]->p-[r]->q
            WHERE m.name = \'' + country + '\'
              AND p.criteria = \'' + criteria + '\'
              AND TYPE(r) <> \'is_category\'
            RETURN TYPE(r), q.value')
        values = []
        result.each do |e|
            values.push([e[:'TYPE(r)'], e[:'q.value']])
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
    
    def self.getUserByEmail(email)
        Neo4j::Session.open(:server_db)
        result = Neo4j::Session.query('
            START n = node:node_auto_index(schema = \'user\')
            MATCH n-[:has_instance]->m
            WHERE m.email = \''+email+'\'
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
    
    def self.createVisaExperience(attributes)
        Neo4j::Session.open(:server_db)
        Neo4j::Transaction.run do
            country = Neo4j::Session.query('
                START n = node:node_auto_index(schema = \'country\')
                MATCH n-[:has_instance]->m
                WHERE m.name = \'' + attributes[:'country'] + '\'
                RETURN m').first[:'m']

            user = Neo4j::Session.query('
                START n = node:node_auto_index(schema = \'user\')
                MATCH n-[:has_instance]->m
                WHERE m.email = \'' + attributes[:'username'] + '\'
                RETURN m').first[:'m']
            
            visa_experience = Neo4j::Node.create(
              :username    => attributes[:'username'],
              :visa_type    => attributes[:'visa_type'],
              :rating       => attributes[:'rating'],
              :time         => attributes[:'time'],
              :documents    => attributes[:'documents'],
              :visits       => attributes[:'visits'],
              :comment      => attributes[:'comment'],
              :comment_time => Time.new.to_s.gsub(' +0000', ''))
              
            country.create_rel(:has_visa_experience, visa_experience)
            user.create_rel(:shared_experience, visa_experience)
        end
    end
  
    def self.getVisaExperienceQuestions(country, question)
        Neo4j::Session.open(:server_db)
        result = Neo4j::Session.query('
            MATCH n-[:has_visa_experience]->m 
            WHERE n.name = \'' + country + '\' 
            RETURN m.visa_type, m.' + question + ', COUNT(*)
            ORDER BY m.visa_type, m.' + question)
        
        resultHash = Hash.new
        resultHash['student'] = [0, 0, 0]
        resultHash['work'] = [0, 0, 0]
        result.each do |r|
            resultHash[r[0]][r[1].to_i - 1] = r[2].to_i
        end
        
        return resultHash
    end
  
    def self.getVisaExperienceComments(country)
        Neo4j::Session.open(:server_db)
        result = Neo4j::Session.query('
            MATCH n-[:has_visa_experience]->m 
            WHERE n.name = \'' + country + '\' 
            RETURN m.username, m.comment_time, m.comment
            ORDER BY m.comment_time DESC')
        
        comments = Array.new
        result.each do |r|
            comment = Hash.new
            comment['username'] = r[0]
            comment['time'] = r[1]
            comment['text'] = r[2]
            comments.push(comment)
        end
        
        return comments
    end
    
    def self.getVisaExperienceRatings(country)
        Neo4j::Session.open(:server_db)
        result = Neo4j::Session.query('
            MATCH n-[:has_visa_experience]->m
            WHERE n.name = \'' + country + '\'
            RETURN m.visa_type, AVG(toFloat(m.rating))
            ORDER BY m.visa_type')
        
        ratings = Hash.new
        ratings['student'] = 0
        ratings['work'] = 0
        result.each do |r|
            ratings[r[0]] = r[1].to_f
        end
        
        return ratings
    end
    
    def self.getLanguagesList()
        Neo4j::Session.open(:server_db)
        result = Neo4j::Session.query('
            MATCH n-[r]->v 
            WHERE n.criteria = \'most_widely_spoken_languages\'
            RETURN TYPE(r), COUNT(*)
            ORDER BY TYPE(r)')
        
        languages = Array.new
        result.each do |r|
            languages.push(r[0])
        end
        
        return languages
    end
end
