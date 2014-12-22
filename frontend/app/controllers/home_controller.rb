require 'date'
class HomeController < ApplicationController
  def index
    Neo4j::Session.open(:server_db)
#    Neo4j::Transaction.run do
#      me   = Neo4j::Node.create(:name => 'Me',   :age => 31)
#      bob  = Neo4j::Node.create(:name => 'Bob',  :age => 29)
#      mark = Neo4j::Node.create(:name => 'Mark', :age => 34)
#      mary = Neo4j::Node.create(:name => 'Mary', :age => 32)
#      john = Neo4j::Node.create(:name => 'John', :age => 33)
#      andy = Neo4j::Node.create(:name => 'Andy', :age => 31)
      
#      me.create_rel(:friends, bob, :value => 3)
#      bob.create_rel(:friends, mark)
#      mark.create_rel(:friends, mary)
#      mary.create_rel(:friends, john)
#      john.create_rel(:friends, andy)
#   end
    # Handle Country Name
    
    
    # Get Coutnry Information
    @countryList = Neo4j::Session.query.match('n-[r:has_criteria]->m').pluck('DISTINCT n.name')
    @criteriaList = Neo4j::Session.query.match('n-[r:has_criteria]->m').pluck('DISTINCT m.criteria')
    @criteriaDict = Hash.new("N/A")
    @criteriaList.each do |crt|
		    @criteriaVal = Neo4j::Session.query.match('n-[r:has_criteria]->m-[r2]->v')
		                      .where('n.name=\'' + params[:country] + '\' AND m.criteria=\'' + crt + '\'')
		                      .pluck('type(r2), v.value')
		    if @criteriaVal.size == 1 then
		      @criteriaDict[crt] = @criteriaVal[0][1]
		    else
		      @criteriaDims = Hash.new("N/A")
		      @criteriaVal.each do |dim|
		        @criteriaDims[dim[0]] = dim[1]
		      @criteriaDict[crt] = @criteriaDims
		      end
		    end
		end
  end
  
  def home
    Neo4j::Session.open(:server_db)
    @countryList = Neo4j::Session.query.match('n-[r:has_criteria]->m').pluck('DISTINCT n.name')
  end
  
  
  def profile
    Neo4j::Session.open(:server_db)
    @countryList = Neo4j::Session.query.match('n-[r:has_criteria]->m').pluck('DISTINCT n.name')
    @name="Sehrish Ijaz";
    @gender="Female";
    @email="sehrish.ansari11@gmail.com";
    @maritial_status="Single";
    @profession_field="Information Technology";
    @education_level="Masters";
    @origin_country="Pakistan";
    @residence_country="Spain";
    @native_language="Urdu";
    @other_language="English";
      
    #LOAD PROFILE FOR THE CURRENT USER
    if(session[:current_user_id]!=nil)
          @username=session[:current_user_id];
    else #LOAD PROFILE OF ANY OTHER USER
      if (params[:user]!=nil)
        @username=params[:user];
      end
    end  
  end
  
  #RESETS THE USER'S SESSION AND REDIRECTS IT TO THE HOMEPAGE
  def logout
    Neo4j::Session.open(:server_db)
    @countryList = Neo4j::Session.query.match('n-[r:has_criteria]->m').pluck('DISTINCT n.name')
    if(session[:current_user_id]!=nil)
      reset_session();
      redirect_to({ action: 'home' })
    end
  end
  
  #Confirms user's login credentials from database
  #Initiate a session and sets current_user_id and current_user_password in it.
  def userlogin
    Neo4j::Session.open(:server_db)
    @countryList = Neo4j::Session.query.match('n-[r:has_criteria]->m').pluck('DISTINCT n.name')
    exists = true;
    #Confirm from database 
    #whether the username and password combination exists or not
    #and then set the session variable.
    if (exists)
      session[:current_user_id] = params['username'];
      session[:current_password] = params['password'];
      @username=params['username'];
      redirect_to({ action: 'home' })
    else
        @loginError="Username and Password combination does not exist!";
        redirect_to({ action: 'login' }, :flash => { :login_error =>"Username and Password combination does not exist!"  })
    end
  end
  
  #Save user's rehistration info in the database
  def registeruser
    Neo4j::Session.open(:server_db)
    @countryList = Neo4j::Session.query.match('n-[r:has_criteria]->m').pluck('DISTINCT n.name')
    
    exists = (Neo4j::Session.query.match('n').where('n.email = \''+params['email']+'\'').pluck('DISTINCT n.email')).size() > 0
    
    if (not exists)
      Neo4j::Transaction.run do
        user = Neo4j::Node.create(
          :name               => params['name'],
          :gender             => params['gender'],
          :email              => params['email'],
          :password           => params['password'],
          :m_status           => params['m_status'],
          :profession         => params['profession'],
          :education          => params['education'],
          :origin_country     => params['origin_country'],
          :residence_country  => params['residence_country'],
          :native_language    => params['native_language'],
          :other_lang         => params['other_lang'])
      end
      
      session[:current_user_id]   = params['email'];
      session[:current_password]  = params['password'];
      
      redirect_to({ action: 'home' });
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
  def login
    Neo4j::Session.open(:server_db)
    @countryList = Neo4j::Session.query.match('n-[r:has_criteria]->m').pluck('DISTINCT n.name')
  end
  
  def register
    Neo4j::Session.open(:server_db)
    @countryList = Neo4j::Session.query.match('n-[r:has_criteria]->m').pluck('DISTINCT n.name')
    
  end
  
  def comparison
    Neo4j::Session.open(:server_db)
#    @criteria = params[:criteria].gsub('_', ' ').split.map(&:capitalize)*' '
#    @country_a = Neo4j::Session.query.match('n-[r:has_criteria]->m-->v')
#                  .where('n.name = \''+params[:a]+'\' AND m.criteria = \''+params[:criteria]+'\'')
#                  .pluck('v.value')[0]
#    @country_b = Neo4j::Session.query.match('n-[r:has_criteria]->m-->v')
#                  .where('n.name = \''+params[:b]+'\' AND m.criteria = \''+params[:criteria]+'\'')
#                  .pluck('v.value')[0]
    @countryList = Neo4j::Session.query.match('n-[r:has_criteria]->m').pluck('DISTINCT n.name')
    
    #Country A Criteria
    @criteriaList_a = Neo4j::Session.query.match('n-[r:has_criteria]->m').pluck('DISTINCT m.criteria')
    @criteriaDict_a = Hash.new("N/A")
    @criteriaList_a.each do |crt|
		    @criteriaVal_a = Neo4j::Session.query.match('n-[r:has_criteria]->m-[r2]->v')
		                      .where('n.name=\'' + params[:country_a] + '\' AND m.criteria=\'' + crt + '\'')
		                      .pluck('type(r2), v.value')
		    if @criteriaVal_a.size == 1 then
		      @criteriaDict_a[crt] = @criteriaVal_a[0][1]
		    else
		      @criteriaDims_a = Hash.new("N/A")
		      @criteriaVal_a.each do |dim|
		        @criteriaDims_a[dim[0]] = dim[1]
		      @criteriaDict_a[crt] = @criteriaDims_a
		      end
		    end
		end 
		
		#Country B Criteria
    @criteriaList_b = Neo4j::Session.query.match('n-[r:has_criteria]->m').pluck('DISTINCT m.criteria')
    @criteriaDict_b = Hash.new("N/A")
    @criteriaList_b.each do |crt|
		    @criteriaVal_b = Neo4j::Session.query.match('n-[r:has_criteria]->m-[r2]->v')
		                      .where('n.name=\'' + params[:country_b] + '\' AND m.criteria=\'' + crt + '\'')
		                      .pluck('type(r2), v.value')
		    if @criteriaVal_b.size == 1 then
		      @criteriaDict_b[crt] = @criteriaVal_b[0][1]
		    else
		      @criteriaDims_b = Hash.new("N/A")
		      @criteriaVal_b.each do |dim|
		        @criteriaDims_b[dim[0]] = dim[1]
		      @criteriaDict_b[crt] = @criteriaDims_b
		      end
		    end
		end
  end
end
