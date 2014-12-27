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
      criteria_1  = crt[:'criteria_1']
      criteria_2  = crt[:'criteria_2']
      value       = crt[:'value']
      if criteria_1 == criteria_2
        dictionary[criteria_1] = value
      else
        if not dictionary.has_key?(criteria_1)
          dictionary[criteria_1] = Hash.new
          dictionary[criteria_1].default = 'N/A'
        end
        dictionary[criteria_1][criteria_2] = value
      end
    end
    
    # Return the dictionary
    return dictionary
  end
  
  # Routed methods
  def index
    @criteriaDict = get_criterias_country(params[:'country'])
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
    country=params[:country];
    chartYaxis=[76.8,1.6,1.4,1.1,1.3,1.2,1.2,5,10.4];
    chartXaxis=['English','Mandarin','Italian','Vietnamese','Arabic','Greek','Cantonese','Unspecified','Others'];
    chartData=[

                ['English',       76.8],
                ['Mandarin',   1.6],
                ['Italian',    1.4],
                ['Vietnamese',     1.1],
                ['Arabic',     1.3],
                ['Greek',     1.2],
                ['Cantonese',     1.2],
                {
                    name: 'Unspecified',
                    y: 5,
                    sliced: true,
                    selected: true
                },
                ['Others',   10.4]
            ];
    
    @data={:country=>country,:chartXaxis=>chartXaxis,:chartYaxis=>chartYaxis,:chartData=>chartData };
    render :json => @data;
    
  end
  def getsalariesdata
    country=params[:country];
    
    min=['Recreation and Sports',2583];
    max=['Executive and Management',11794];
    chartXaxis=[
                  'Recreation and Sports',
                   'Fashion and Apparel',
                   'Gardening / Farming / Fishing',
                   'Media / Broadcasting / Arts / Entertainment',
                   'Care Giving and Child Care',
                   'Food /Hospitality / Tourism / Catering',
                   'Administration / Reception / Secretarial',
                   'Counseling',
                   'Automotive',
                   'Photography',
                   'Customer Service and Call Center',
                   'Real Estate',
                   'Import and Export',
                   'Law Enforcement / Security / Fire',
                   'Electrical and Electronics Trades',
                   'Insurance',
                   'Courier / Delivery / Transport / Drivers',
                   'Sales Retail and Wholesale',
                   'Advertising / Grapic Design / Event Management',
                   'Purchasing and Inventory',
                   'Science and Technical Services',
                   'Architecture',
                   'Teaching / Education',
                   'Factory and Manufacturing',
                   'Environmental',
                   'Health and Medical',
                   'Accounting and Finance',
                   'Business Planning',
                   'Banking',
                   'Telecommunication',
                   'Construction / Building / Installation',
                   'Publishing and Printing',
                   'Pharmaceutical and Biotechnology',
                   'Airlines / Aviation / Aerospace / Defense',
                   'Quality Control and Compliance',
                   'Government and Defence',
                   'Marketing',
                   'Human Resources',
                   'Information Technology',
                   'Legal',
                   'Engineering',
                   
                   'Facilities / Maintenance / Repair',
                   'Oil / Gas / Energy / Mining',
                   'Cleaning and Housekeeping',
                   'Executive and Management']

      chartYaxis=[2583,3625,3776,4043,4106,4247,4298,4333,4471,4479,
                  4638,4685,4792,4830,5296,5750,5813,5866,6127,6186,6382,
                  6390,6411,6557,6567,6595,6679,6835,6990,7023,7069,7107,
                  7150,7305,7313,7472,7529,7589,7849,7897,7942,8169,9514,
                  10542,11794
                  ];

    chartData=[
                ['Recreation and Sports',2583],
                ['Fashion and Apparel',3625],
                ['Gardening / Farming / Fishing',3776],
                ['Media / Broadcasting / Arts / Entertainment',4043],
                ['Care Giving and Child Care',4106],
                ['Food /Hospitality / Tourism / Catering',4247],
                ['Administration / Reception / Secretarial',4298],
                ['Counseling',4333],
                ['Automotive',4471],
                ['Photography',4479],
                ['Customer Service and Call Center',4638],
                ['Real Estate',4685],
                ['Import and Export',4792],
                ['Law Enforcement / Security / Fire',4830],
                ['Electrical and Electronics Trades',5296],
                ['Insurance',5750],
                ['Courier / Delivery / Transport / Drivers',5813],
                ['Sales Retail and Wholesale',5866],
                ['Advertising / Grapic Design / Event Management',6127],
                ['Purchasing and Inventory',6186],
                ['Science and Technical Services',6382],
                ['Architecture',6390],
                ['Teaching / Education',6411],
                ['Factory and Manufacturing',6557],
                ['Environmental',6567],
                ['Health and Medical',6595],
                ['Accounting and Finance',6679],
                ['Business Planning',6835],
                ['Banking',6990],
                ['Telecommunication',7023],
                ['Construction / Building / Installation',7069],
                ['Publishing and Printing',7107],
                ['Pharmaceutical and Biotechnology',7150],
                ['Airlines / Aviation / Aerospace / Defense',7305],
                ['Quality Control and Compliance',7313],
                ['Government and Defence',7472],
                ['Marketing',7529],
                ['Human Resources',7589],
                ['Information Technology',7849],
                ['Legal',7897],
                ['Engineering',7942],
                ['Facilities / Maintenance / Repair',8169],
                ['Oil / Gas / Energy / Mining',9514],
                ['Cleaning and Housekeeping',10542],
                ['Executive and Management',11794]
                ];  
                
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
                     text: 'Average Salary (Australian Dollars)'
                 }
             };
    @data={:country=>country,:cxAxis=>cxAxis,:cyAxis=>cyAxis,
    :chartData=>chartData,:minSal=>min,:maxSal=>max,
    :chartXaxis=>chartXaxis,:chartYaxis=>chartYaxis };
    render :json => @data;
    
  end
  def getunemploymentdata
    country=params[:country];
    chartData=[ #2007
						[(Date.parse('2007-01-01').to_time.to_f * 1000).to_i, 4.5],
						[(Date.parse('2007-01-02').to_time.to_f * 1000).to_i, 4.6],
						[(Date.parse('2007-01-03').to_time.to_f * 1000).to_i, 4.4],
						[(Date.parse('2007-01-04').to_time.to_f * 1000).to_i, 4.4],
						[(Date.parse('2007-01-05').to_time.to_f * 1000).to_i, 4.3],
						[(Date.parse('2007-01-06').to_time.to_f * 1000).to_i, 4.3],
						[(Date.parse('2007-01-07').to_time.to_f * 1000).to_i, 4.3],
						[(Date.parse('2007-01-08').to_time.to_f * 1000).to_i, 4.3],
						[(Date.parse('2007-01-09').to_time.to_f * 1000).to_i, 4.2],
						[(Date.parse('2007-01-12').to_time.to_f * 1000).to_i, 4.3],

						#2008
						[(Date.parse('2008-01-01').to_time.to_f * 1000).to_i, 4.2],
						[(Date.parse('2008-01-02').to_time.to_f * 1000).to_i, 4.0],
						[(Date.parse('2008-01-03').to_time.to_f * 1000).to_i, 4.1],
						[(Date.parse('2008-01-04').to_time.to_f * 1000).to_i, 4.3],
						[(Date.parse('2008-01-05').to_time.to_f * 1000).to_i, 4.3],
						[(Date.parse('2008-01-06').to_time.to_f * 1000).to_i, 4.3],
						[(Date.parse('2008-01-07').to_time.to_f * 1000).to_i, 4.3],
						[(Date.parse('2008-01-08').to_time.to_f * 1000).to_i, 4.1],
						[(Date.parse('2008-01-09').to_time.to_f * 1000).to_i, 4.3],
						[(Date.parse('2008-01-10').to_time.to_f * 1000).to_i, 4.3],
						[(Date.parse('2008-01-11').to_time.to_f * 1000).to_i, 4.5],
						[(Date.parse('2008-01-12').to_time.to_f * 1000).to_i, 4.6],
						 #2009
						[(Date.parse('2009-01-01').to_time.to_f * 1000).to_i, 4.9],
						[(Date.parse('2009-01-02').to_time.to_f * 1000).to_i, 5.3],
						[(Date.parse('2009-01-03').to_time.to_f * 1000).to_i, 5.7],
						[(Date.parse('2009-01-04').to_time.to_f * 1000).to_i,5.5],
						[(Date.parse('2009-01-05').to_time.to_f * 1000).to_i, 5.8],
						[(Date.parse('2009-01-06').to_time.to_f * 1000).to_i, 5.9],
						[(Date.parse('2009-01-07').to_time.to_f * 1000).to_i, 5.8],
						[(Date.parse('2009-01-08').to_time.to_f * 1000).to_i, 5.8],
						[(Date.parse('2009-01-09').to_time.to_f * 1000).to_i, 5.7],
						[(Date.parse('2009-01-10').to_time.to_f * 1000).to_i, 5.6],
						[(Date.parse('2009-01-11').to_time.to_f * 1000).to_i,5.6],
						[(Date.parse('2009-01-12').to_time.to_f * 1000).to_i, 5.5],

						#2010
						[(Date.parse('2010-01-01').to_time.to_f * 1000).to_i, 5.3],
						[(Date.parse('2010-01-02').to_time.to_f * 1000).to_i, 5.3],
						[(Date.parse('2010-01-03').to_time.to_f * 1000).to_i, 5.4],
						[(Date.parse('2010-01-04').to_time.to_f * 1000).to_i, 5.5],
						[(Date.parse('2010-01-05').to_time.to_f * 1000).to_i, 5.2],
						[(Date.parse('2010-01-06').to_time.to_f * 1000).to_i, 5.2],
						[(Date.parse('2010-01-07').to_time.to_f * 1000).to_i, 5.3],
						[(Date.parse('2010-01-08').to_time.to_f * 1000).to_i, 5.1],
						[(Date.parse('2010-01-09').to_time.to_f * 1000).to_i, 5.1],
						[(Date.parse('2010-01-10').to_time.to_f * 1000).to_i, 5.3],
						[(Date.parse('2010-01-11').to_time.to_f * 1000).to_i, 5.1],
						[(Date.parse('2010-01-12').to_time.to_f * 1000).to_i, 5.9],
						#2011
						[(Date.parse('2011-01-01').to_time.to_f * 1000).to_i, 5.1],
						[(Date.parse('2011-01-02').to_time.to_f * 1000).to_i, 5.0],
						[(Date.parse('2011-01-03').to_time.to_f * 1000).to_i, 4.9],
						[(Date.parse('2011-01-04').to_time.to_f * 1000).to_i,4.9],
						[(Date.parse('2011-01-05').to_time.to_f * 1000).to_i, 5.0],
						[(Date.parse('2011-01-06').to_time.to_f * 1000).to_i, 5.0],
						[(Date.parse('2011-01-07').to_time.to_f * 1000).to_i, 5.1],
						[(Date.parse('2011-01-08').to_time.to_f * 1000).to_i, 5.3],
						[(Date.parse('2011-01-09').to_time.to_f * 1000).to_i, 5.2],
						[(Date.parse('2011-01-10').to_time.to_f * 1000).to_i, 5.2],
						[(Date.parse('2011-01-11').to_time.to_f * 1000).to_i, 5.2],
						[(Date.parse('2011-01-12').to_time.to_f * 1000).to_i, 5.2],

						#2012
						[(Date.parse('2012-01-01').to_time.to_f * 1000).to_i, 5.1],
						[(Date.parse('2012-01-02').to_time.to_f * 1000).to_i, 5.2],
						[(Date.parse('2012-01-03').to_time.to_f * 1000).to_i, 5.2],
						[(Date.parse('2012-01-04').to_time.to_f * 1000).to_i, 5.0],
						[(Date.parse('2012-01-05').to_time.to_f * 1000).to_i, 5.2],
						[(Date.parse('2012-01-06').to_time.to_f * 1000).to_i, 5.2],
						[(Date.parse('2012-01-07').to_time.to_f * 1000).to_i, 5.2],
						[(Date.parse('2012-01-08').to_time.to_f * 1000).to_i, 5.1],
						[(Date.parse('2012-01-09').to_time.to_f * 1000).to_i, 5.5],
						[(Date.parse('2012-01-10').to_time.to_f * 1000).to_i, 5.4],
						[(Date.parse('2012-01-11').to_time.to_f * 1000).to_i, 5.3],
						[(Date.parse('2012-01-12').to_time.to_f * 1000).to_i, 5.4],
						#2013
						[(Date.parse('2013-01-01').to_time.to_f * 1000).to_i, 5.4],
						[(Date.parse('2013-01-02').to_time.to_f * 1000).to_i, 5.4],
						[(Date.parse('2013-01-03').to_time.to_f * 1000).to_i, 5.6],
						[(Date.parse('2013-01-04').to_time.to_f * 1000).to_i, 5.6],
						[(Date.parse('2013-01-05').to_time.to_f * 1000).to_i, 5.6],
						[(Date.parse('2013-01-06').to_time.to_f * 1000).to_i, 5.7]
					
						
					];
					 
					
		@data={:country=>country,:chartData=>chartData};
    render :json => @data;
    

  end
end
