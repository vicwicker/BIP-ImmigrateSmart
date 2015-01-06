require 'date'
require 'Neo4jDriver'

class HomeController < ApplicationController
  before_filter :get_country_list
  
  # No-Routed methods
  def get_country_list
    @countryList = Neo4jDriver.getCountryNames
  end
  
  def get_criterias_country(country)
    # Get all the criterias for that country
    criterias = Neo4jDriver.getCriteriaNamesForCountry(country)
    
    # Init dictionary. The default value is N/A in case we do not have such info
    dictionary = Hash.new
    dictionary.default = 'N/A'
    
    # Fill the dictionary
    criterias.each do |crt|
      criteria  = crt[:'criteria']
      attribute  = crt[:'attribute']
      value       = crt[:'value']
      if criteria == attribute
        dictionary[criteria] = value
      else
        if not dictionary.has_key?(criteria)
          dictionary[criteria] = Hash.new
          dictionary[criteria].default = 'N/A'
        end
        dictionary[criteria][attribute] = value
      end
    end
    
    # Return the dictionary
    return dictionary
  end
  
  # Routed methods
  def index
    @comment='This is a test comment for the visa sharing experience.';
    @user='asdf';
    @commenttime = (Time.new).inspect;
    
    @criteriaDict = get_criterias_country(params[:'country'])
  end
  
  
  def getquestionsdata
    country=params[:country];
    q=params[:q].to_i;
    
    if q==1
    chartTitle='Time taken for an appointment';
    chartXaxis={
               categories:['Less than 10','Between 10 and 30','More than 30']
      
    };
    chartYaxis={
            title: {
                text: 'Day(s)'
            }
        };
    elsif q==2
    chartTitle='Documents required apart from application form';
    chartXaxis={
               categories:['1 or 2','Between 3 and 5','More than 5']
      
    };
    chartYaxis={
            title: {
                text: 'Document(s)'
            }
        };
    elsif q==3
      chartTitle='Visits required to get the visa';
      chartXaxis={
               categories:['Less than 5','Between 5 and 10','More than 10']
      
    };
    chartYaxis={
            title: {
                text: 'Visit(s)'
            }
        };
    end
    chartData=[{
                name: 'Student Visa',
                data: [5.0,15.0,25.0],
                dataLabels: {    
                             enabled: true,
                             color: '#8F8F8F'
                             },
                }, {
                  name: 'Work Permit',
                  data: [2.0,35.0,50.0],
                  dataLabels: {    
                               enabled: true,
                               color: '#e5e4e4'
                             }
                  
                },
              
            ];
    
    @data={:country=>country,:chartTitle=>chartTitle,:chartXaxis=>chartXaxis,:chartYaxis=>chartYaxis,:chartData=>chartData };
    render :json => @data;
  end
  
  def sharevisaexperience
    
    country=params[:country];
    username=params[:username];
    visat=params[:visat];
    rating=params[:rating];
    time=params[:time];
    documents=params[:documents];
    visits=params[:visits];
    comment=params[:comment];
    commenttime=Time.new;
    redirect_to({ :action => 'index', :country => country }, :flash => { :shareMsg =>"Your visa experience has been shared!"  });
  end
  
  def comparison2
    #Neo4j::Session.open(:server_db)
    #@countryList = Neo4j::Session.query.match('n-[r:has_criteria]->m').pluck('DISTINCT n.name')
    #@value = Neo4jDriver.getCountryCriteriaValue('Australia', 'crime_rate')
  end
  
  def getcomparisondata
    length = params[:length];
    i = 0;

    chartData = Array.new;
    while i < length.to_i do
      cname = 'country' + i.to_s;
      value = Neo4jDriver.getCountryCriteriaValue(params[cname], params[:criteria])
      chartData[i] = [params[cname], value[0][1].to_f];
      i = i + 1;
    end

    criteria = params[:criteria];
    valuesLabel = '';

    @data = {:length=>length,:chartData=>chartData,:criteria=>criteria,:valuesLabel=>valuesLabel};
    render :json => @data;
  end
  
  def comparison
    @criteriaDict_a = get_criterias_country(params[:'country_a'])
    @criteriaDict_b = get_criterias_country(params[:'country_b'])
  end
  
  def profile
    @name               = session[:'name']
    @gender             = session[:'gender']
    @email              = session[:'current_user_id']
    @maritial_status    = session[:'m_status'] 
    @profession_field   = session[:'profession'] 
    @education_level    = session[:'education']
    @origin_country     = session[:'origin_country']
    @residence_country  = session[:'residence_country']
    @native_language    = session[:'native_language']
    @other_language     = session[:'other_lang']
      
    #LOAD PROFILE FOR THE CURRENT USER
    if session[:'current_user_id'] != nil
          @username = session[:'current_user_id']
    else #LOAD PROFILE OF ANY OTHER USER
      if params[:'user'] != nil
        @username = params[:'user']
      end
    end  
  end
  
  #RESETS THE USER'S SESSION AND REDIRECTS IT TO THE HOMEPAGE
  def logout
    if session[:'current_user_id'] != nil
      reset_session()
      redirect_to({ action: 'home' })
    end
  end
  
  #Confirms user's login credentials from database
  #Initiate a session and sets current_user_id and current_user_password in it.
  def userlogin
    user = Neo4jDriver.validCredentials?(params[:'username'], params[:'password'])
    
    # If the returned hash is empty means user does not exists
    if not user.empty?
      session[:'name']              = user[:'name']
      session[:'gender']            = user[:'gender']
      session[:'current_user_id']   = user[:'email']
      session[:'m_status']          = user[:'m_status']
      session[:'profession']        = user[:'profession']
      session[:'education']         = user[:'education']
      session[:'origin_country']    = user[:'origin_country']
      session[:'residence_country'] = user[:'residence_country']
      session[:'native_language']   = user[:'native_language']
      session[:'other_lang']        = user[:'other_lang']
      
      @username = session[:'current_user_id']
      
      redirect_to({ action: 'home' })
    else
      @loginError="Username and Password combination does not exist!";
      redirect_to({ action: 'login' }, :flash => { :login_error =>"Username and Password combination does not exist!"  })
    end
  end
  
  #Save user's rehistration info in the database
  def registeruser
    exists = Neo4jDriver.existsUser?(params[:email])
    
    if not exists
      Neo4jDriver.createUser(params)
      
      session[:'name']              = params['name']
      session[:'gender']            = params['gender']
      session[:'current_user_id']   = params['email']
      session[:'m_status']          = params['m_status']
      session[:'profession']        = params['profession']
      session[:'education']         = params['education']
      session[:'origin_country']    = params['origin_country']
      session[:'residence_country'] = params['residence_country']
      session[:'native_language']   = params['native_language']
      session[:'other_lang']        = params['other_lang']
      
      redirect_to({ action: 'home' })
    else
      # What to do here?
      redirect_to 'https://support.google.com/a/answer/1071113?hl=en'
    end
  end
  
  def getlanguagesdata
    country = params[:country];
    
    values = Neo4jDriver.getCountryCriteriaValue(country, 'most_widely_spoken_languages')
    chartData = []
    chartXaxis = []
    chartYaxis = []
    values.each do |v|
      val = v[1].gsub(',', '').to_f
      chartData.push([v[0], val])
      chartXaxis.push(v[0])
      chartYaxis.push(val)
    end

    @data={:country=>country,:chartXaxis=>chartXaxis,:chartYaxis=>chartYaxis,:chartData=>chartData };
    render :json => @data;
    
  end
  def getsalariesdata
    country = params[:country];
    
    values = Neo4jDriver.getCountryCriteriaValue(country, 'average_salary_per_profession')
    chartData = []
    chartXaxis = []
    chartYaxis = []
    minSal = 100000000
    maxSal = 0
    min = []
    max = []
    values.each do |v|
      sal = v[1][0, v[1].index(' ')].gsub(',', '').to_i
      chartData.push([v[0], sal])
      chartXaxis.push(v[0])
      chartYaxis.push(sal)
      if (sal < minSal) then
        minSal = sal
        min = [v[0], sal]
      end
      if (sal > maxSal) then
        maxSal = sal
        max = [v[0], sal]
      end
    end

    cxAxis= {
                 type: 'category',
                 labels: {
                     rotation: 90,
                     style: {
                         fontSize: '10px',
                         fontFamily: 'Verdana, sans-serif'
                     }
                 }
             };
    cyAxis={
                 min: 1000,
                 title: {
                     text: 'Average Salary (USD)'
                 }
             };
    @data={:country=>country,:cxAxis=>cxAxis,:cyAxis=>cyAxis,
    :chartData=>chartData,:minSal=>min,:maxSal=>max,
    :chartXaxis=>chartXaxis,:chartYaxis=>chartYaxis };
    render :json => @data;
  end

  def getunemploymentdata
    country = params[:country];
    
    values = Neo4jDriver.getCountryCriteriaValue(country, 'unemployment_rate_per_year')
    chartData = []
    values.each do |v|
      chartData.push([(Date.parse(v[0] + "-01-01").to_time.to_f * 1000).to_i, v[1].gsub(',', '.').to_f])
    end

		@data={:country=>country,:chartData=>chartData};
    render :json => @data;
  end
end
