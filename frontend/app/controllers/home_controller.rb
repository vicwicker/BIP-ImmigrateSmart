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
