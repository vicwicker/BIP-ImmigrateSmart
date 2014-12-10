class User
  attr_accessor :name, :email, :password, :gender, :age, 
  :origin_country, :interest_country,:native_language,:other_language,
  :profession, :education,:maritial_status

  def initialize(attributes = {})
    @name  = attributes[:name]
    @email = attributes[:email]
    @password  = attributes[:password]
    @gender = attributes[:gender]
    @age  = attributes[:age]
    @origin_country = attributes[:origin_country]
    @interest_country  = attributes[:interest_country]
    @native_language = attributes[:native_language]
    @other_language  = attributes[:other_language]
    @education = attributes[:education]
    @profession  = attributes[:profession]
    @maritial_status = attributes[:maritial_status]
  end

  def formatted_email
    "#{@name} <#{@email}>"
  end
end