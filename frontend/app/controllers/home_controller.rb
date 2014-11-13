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
    @query = Neo4j::Session.query.match('n-[r]->m').pluck('n.name,type(r),m.value')
  end
end
