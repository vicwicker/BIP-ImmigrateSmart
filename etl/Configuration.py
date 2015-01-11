import sys
import re, distance
import utils

from SQLiteDriver import SQLiteDriver

class Configuration:
    
     # Configuration instance table
    config_instances_table = 'instances'

    # Configuration read column table
    config_columns_table = 'columns'

    # Filters table (i.e., list of countries)
    config_filters_table = 'filters'
    
    # File from which obtaining the country filter list
    filters_file = './config/filters.list'
    
    # File from which obtaining the categories
    categories_file = './config/categories.list'
    
    # Filters will be shared through all instance
    filters = []
    
    @staticmethod
    def filters():
        sql = SQLiteDriver()
        
        with open(Configuration.filters_file, 'r') as f:
            lines = f.readlines()
            for line in lines:
                aux = line.split(';')
                for country in aux:
                    sql.execute('''INSERT INTO '''+Configuration.config_filters_table+'''
                        VALUES (\''''+country.strip().lower()+'''\')''')
        
        sql.commit()
        
        sql.close()
    
    @staticmethod
    def load_filters():
        Configuration.filters = []
        sql = SQLiteDriver()
        
        filters_in_db = sql.execute('SELECT * FROM '+Configuration.config_filters_table)
        for f in filters_in_db:
            Configuration.filters.append(utils.to_str(f[0]))
            
        sql.close()
        
    # NOTE: Only works for unidimensional criteria
    @staticmethod
    def insert(config_name, source_file, source_file_type, extras, headers, countries_col, criterias):
        sql = SQLiteDriver()
        
        sql.execute('''INSERT INTO '''+Configuration.config_instances_table+''' VALUES (
                        \''''+config_name+'''\',
                        \''''+countries_col+'''\',
                        \''''+source_file+'''\',
                        \''''+source_file_type+'''\',
                        \''''+extras+'''\',
                        \''''+headers+'''\')''')
            
        for criteria in criterias:
           sql.execute('''INSERT INTO '''+Configuration.config_columns_table+''' VALUES (
                            \''''+config_name+'''\',
                            \''''+criteria['criteria']+'''\',
                            \''''+criteria['category']+'''\',
                            \''''+criteria['column']+'''\',
                            'yes',
                            'N/A')''')
                            
        sql.commit()
        return Configuration(config_name)
        
    @staticmethod
    def create():
        sql = SQLiteDriver()
        
        sql.execute('''CREATE TABLE '''+Configuration.config_instances_table+''' (
                            config_name TEXT,
                            country_in TEXT,
                            file_uri TEXT,
                            file_type TEXT,
                            extras TEXT,
                            headers TEXT)''')
                
        sql.execute('''CREATE TABLE '''+Configuration.config_columns_table+''' (
                            config_name TEXT,
                            criteria TEXT,
                            category TEXT,
                            column TEXT,
                            fact TEXT,
                            description TEXT)''')
                            
        sql.execute('''CREATE TABLE '''+Configuration.config_filters_table+''' (
                            country TEXT)''', True)
                            
        sql.close()
        
    @staticmethod
    def drop():
        sql = SQLiteDriver()
        
        sql.execute('DROP TABLE '+Configuration.config_instances_table)
        sql.execute('DROP TABLE '+Configuration.config_columns_table)
        sql.execute('DROP TABLE '+Configuration.config_filters_table, True)
        
        sql.close()
            
    # Instance methods
    def __init__(self, config_name):
        self.load(config_name)
        
    def load(self, config_name):
        sql = SQLiteDriver()
        
        config = sql.execute('SELECT * FROM instances WHERE config_name = \'' + config_name + '\'').fetchone()
        
        # Load basic instance configuration properties
        self.config_name = utils.to_str(config[0]) # Name of this ETL configuration
        
        self.country_in  = utils.to_str(config[1]) # Column in the CSV file where the country name is
        if not re.search('^[0-9]+$', self.country_in) is None:
            self.country_in = int(self.country_in)
            self.is_multi = True
        else:
            self.is_multi = False
            
        self.file_uri    = utils.to_str(config[2]) # URI of the file to read
        
        self.file_type   = utils.to_str(config[3]) # File type
        self.extras      = utils.to_str(config[4]) # Delimiter, sheet, CSV number...
        
        self.headers     = utils.to_str(config[5])
        if self.headers != 'yes':
            self.headers = False
        else:
            self.headers = True
        
        # Read Criteria-Column pairs (must be ordered by index)
        self.columns = []
        columns_to_read = sql.execute('SELECT * FROM columns WHERE config_name = \'' + config_name + '\'')
        for col in columns_to_read:
            to_append = {'criteria':col[1], 'category':col[2], 'column':col[3], 'fact':1, 'description':str(col[5])}
            if col[4] != 'yes':
                to_append['fact'] = 0
            self.columns.append(to_append)
            
        sql.close()

# Main program
if __name__ == "__main__":
    def sample():
        sql = SQLiteDriver()
        
        sql.execute('DELETE FROM '+Configuration.config_instances_table)
        sql.execute('DELETE FROM '+Configuration.config_columns_table)
                       
        # XLS configuration instance sample - Minimum Wage / Paid Annual Leave
        sql.execute('''INSERT INTO '''+Configuration.config_instances_table+''' VALUES (
                            'doingbusiness',
                            '0',
                            'http://www.doingbusiness.org/~/media/GIAWB/Doing%20Business/Documents/Miscellaneous/LMR-DB15-DB14-service-sector-data-points-and-details.xlsx',
                            'xls',
                            '0',
                            'yes')''')
                
        sql.execute('''INSERT INTO '''+Configuration.config_columns_table+''' VALUES (
                            'doingbusiness',
                            'minimum_wage',
                            'Economic Incentives',
                            '4',
                            'yes',
                            'N/A')''')
                    
        sql.execute('''INSERT INTO '''+Configuration.config_columns_table+''' VALUES (
                            'doingbusiness',
                            'paid_annual_leave',
                            'Economic Incentives',
                            '16',
                            'yes',
                            'N/A')''', True)  
                            
        # HTML configuration instance sample - Foreign Worker Salaries
        sql.execute('''INSERT INTO '''+Configuration.config_instances_table+''' VALUES (
                            'nationmaster',
                            '1',
                            'http://www.nationmaster.com/country-info/stats/People/Migration/Foreign-worker-salaries',
                            'html',
                            '0',
                            'yes')''')
                
        sql.execute('''INSERT INTO '''+Configuration.config_columns_table+''' VALUES (
                            'nationmaster',
                            'foreign_worker_salaries',
                            'Economic Incentives',
                            '2',
                            'yes',
                            'N/A')''', True)
                            
        # HTML configuration instance sample - Area
        sql.execute('''INSERT INTO '''+Configuration.config_instances_table+''' VALUES (
                            'cia-area',
                            '1',
                            'https://www.cia.gov/library/publications/the-world-factbook/rankorder/2147rank.html?countryname=Australia&countrycode=as&regionCode=aus&rank=6#as',
                            'html',
                            '2',
                            'no')''')
                
        sql.execute('''INSERT INTO '''+Configuration.config_columns_table+''' VALUES (
                            'cia-area',
                            'area',
                            'General',
                            '2',
                            'yes',
                            'N/A')''', True)
                            
        # HTML configuration instance sample - Population
        sql.execute('''INSERT INTO '''+Configuration.config_instances_table+''' VALUES (
                            'cia-population',
                            '1',
                            'https://www.cia.gov/library/publications/the-world-factbook/rankorder/2119rank.html?countryname=Australia&countrycode=as&regionCode=aus&rank=56#as',
                            'html',
                            '2',
                            'no')''')
                
        sql.execute('''INSERT INTO '''+Configuration.config_columns_table+''' VALUES (
                            'cia-population',
                            'population',
                            'General',
                            '2',
                            'yes',
                            'N/A')''', True)
                            
        # HTML configuration instance sample - GDP per capita
        sql.execute('''INSERT INTO '''+Configuration.config_instances_table+''' VALUES (
                            'cia-gdp-per-capita',
                            '1',
                            'https://www.cia.gov/library/publications/the-world-factbook/rankorder/2004rank.html?countryname=Australia&countrycode=as&regionCode=aus&rank=21#as',
                            'html',
                            '2',
                            'no')''')
                
        sql.execute('''INSERT INTO '''+Configuration.config_columns_table+''' VALUES (
                            'cia-gdp-per-capita',
                            'gdp_per_capita',
                            'General',
                            '2',
                            'yes',
                            'N/A')''', True)
                            
        # HTML configuration instance sample - Cost of Living
        sql.execute('''INSERT INTO '''+Configuration.config_instances_table+''' VALUES (
                            'numbero-cost-of-living',
                            '0',
                            'http://www.numbeo.com/cost-of-living/rankings_by_country.jsp',
                            'html',
                            '1',
                            'yes')''')
                
        sql.execute('''INSERT INTO '''+Configuration.config_columns_table+''' VALUES (
                            'numbero-cost-of-living',
                            'cost_of_living',
                            'Economic Incentives',
                            '3',
                            'yes',
                            'This index is a relative indicator of consumer goods price, including groceries, restaurants, transportation, utilities and rent. It is relative to New York City (NYC), which means that for New York City, the index should be 100(%). If a country has a CPI index of 120, it means that it is approximately 20% more expensive than New York.')''', True)
                            
        # HTML configuration instance sample - Crimes Rate
        sql.execute('''INSERT INTO '''+Configuration.config_instances_table+''' VALUES (
                            'numbero-cime-rate',
                            '0',
                            'http://www.numbeo.com/crime/rankings_by_country.jsp',
                            'html',
                            '1',
                            'yes')''')
                
        sql.execute('''INSERT INTO '''+Configuration.config_columns_table+''' VALUES (
                            'numbero-cime-rate',
                            'crime_rate',
                            'Economic Incentives',
                            '1',
                            'yes',
                            'This index is an estimation of overall level of crime in a given country. Crime Levels up to 50 are reasonable, and crime index levels more than 100 are too high.')''', True)
                            
        # HTML configuration instance sample - Quality of Health Care System
        sql.execute('''INSERT INTO '''+Configuration.config_instances_table+''' VALUES (
                            'numbero-quality-health-care-system',
                            '0',
                            'http://www.numbeo.com/health-care/rankings_by_country.jsp',
                            'html',
                            '1',
                            'yes')''')
                
        sql.execute('''INSERT INTO '''+Configuration.config_columns_table+''' VALUES (
                            'numbero-quality-health-care-system',
                            'quality_of_health_care_system',
                            'Medical Care',
                            '1',
                            'yes',
                            'This index is an estimation of the overall quality of the health care system, health care professionals, equipment, staff, doctors, cost, etc. The closer the country''s score is to 100, the better the health care system is in that country.')''', True)
                            
        # HTML configuration instance sample - Average Overall Monthly Salary
        sql.execute('''INSERT INTO '''+Configuration.config_instances_table+''' VALUES (
                            'nationmaster-avg-overall-salary',
                            '1',
                            'http://www.nationmaster.com/country-info/stats/Cost-of-living/Average-monthly-disposable-salary/After-tax',
                            'html',
                            '0',
                            'yes')''')
                
        sql.execute('''INSERT INTO '''+Configuration.config_columns_table+''' VALUES (
                            'nationmaster-avg-overall-salary',
                            'average_overall_monthly_salary',
                            'Economic Incentives',
                            '2',
                            'yes',
                            'N/A')''', True)
                            
        # HTML configuration instance sample - Average Income Taxes
        sql.execute('''INSERT INTO '''+Configuration.config_instances_table+''' VALUES (
                            'kpmg-avg-income-tax',
                            '0',
                            'http://www.kpmg.com/GLOBAL/EN/SERVICES/TAX/TAX-TOOLS-AND-RESOURCES/Pages/individual-income-tax-rates-table.aspx',
                            'html',
                            '1',
                            'yes')''')
                
        sql.execute('''INSERT INTO '''+Configuration.config_columns_table+''' VALUES (
                            'kpmg-avg-income-tax',
                            'average_income_taxes',
                            'Economic Incentives',
                            '8',
                            'yes',
                            'N/A')''', True)
                            
        # HTML configuration instance sample - Unemployment Rate
        sql.execute('''INSERT INTO '''+Configuration.config_instances_table+''' VALUES (
                            'cia-unemployment-rate',
                            '1',
                            'https://www.cia.gov/library/publications/the-world-factbook/rankorder/2129rank.html?countryname=Australia&countrycode=as&regionCode=aus&rank=53#as',
                            'html',
                            '2',
                            'no')''')
                
        sql.execute('''INSERT INTO '''+Configuration.config_columns_table+''' VALUES (
                            'cia-unemployment-rate',
                            'unemployment_rate',
                            'Job Opportunities',
                            '2',
                            'yes',
                            'N/A')''', True)
                            
        # HTML configuration instance sample - Health Care Expenditure
        sql.execute('''INSERT INTO '''+Configuration.config_instances_table+''' VALUES (
                            'cia-health-care-expenditure',
                            '1',
                            'https://www.cia.gov/library/publications/the-world-factbook/rankorder/2225rank.html?countryname=Cambodia&countrycode=cb&regionCode=eas&rank=118#cb',
                            'html',
                            '2',
                            'no')''')
                
        sql.execute('''INSERT INTO '''+Configuration.config_columns_table+''' VALUES (
                            'cia-health-care-expenditure',
                            'health_care_expenditure',
                            'Medical Care',
                            '2',
                            'yes',
                            'N/A')''', True)
                            
        # HTML configuration instance sample - Percentage of English Speakers
        sql.execute('''INSERT INTO '''+Configuration.config_instances_table+''' VALUES (
                            'wiki-pct-english-speakers',
                            '0',
                            'http://en.wikipedia.org/wiki/List_of_countries_by_English-speaking_population',
                            'html',
                            '1',
                            'yes')''')
                
        sql.execute('''INSERT INTO '''+Configuration.config_columns_table+''' VALUES (
                            'wiki-pct-english-speakers',
                            'percentage_of_english_speakers',
                            'Education',
                            '1',
                            'yes',
                            'N/A')''', True)
                            
        # HTML configuration instance sample one country - Salary per profession Australia
        sql.execute('''INSERT INTO '''+Configuration.config_instances_table+''' VALUES (
                            'salary-profession-australia',
                            'Australia',
                            'http://www.salaryexplorer.com/average-salary.php?&loctype=1&loc=13',
                            'html',
                            '0',
                            'yes')''')
                
        sql.execute('''INSERT INTO '''+Configuration.config_columns_table+''' VALUES (
                            'salary-profession-australia',
                            'average_salary_per_profession',
                            'Economic Incentives',
                            '0',
                            'no',
                            'N/A')''')
                            
        sql.execute('''INSERT INTO '''+Configuration.config_columns_table+''' VALUES (
                            'salary-profession-australia',
                            'average_salary_per_profession',
                            'Economic Incentives',
                            '1',
                            'yes',
                            'N/A')''', True)
                            
        # HTML configuration instance sample one country - Salary per profession Canada
        sql.execute('''INSERT INTO '''+Configuration.config_instances_table+''' VALUES (
                            'salary-profession-canada',
                            'Canada',
                            'http://www.salaryexplorer.com/average-salary.php?&loctype=1&loc=38',
                            'html',
                            '0',
                            'yes')''')
                
        sql.execute('''INSERT INTO '''+Configuration.config_columns_table+''' VALUES (
                            'salary-profession-canada',
                            'average_salary_per_profession',
                            'Economic Incentives',
                            '0',
                            'no',
                            'N/A')''')
                            
        sql.execute('''INSERT INTO '''+Configuration.config_columns_table+''' VALUES (
                            'salary-profession-canada',
                            'average_salary_per_profession',
                            'Economic Incentives',
                            '1',
                            'yes',
                            'N/A')''', True)
                            
        # HTML configuration instance sample one country - Salary per profession France
        sql.execute('''INSERT INTO '''+Configuration.config_instances_table+''' VALUES (
                            'salary-profession-france',
                            'France',
                            'http://www.salaryexplorer.com/average-salary.php?&loctype=1&loc=74',
                            'html',
                            '0',
                            'yes')''')
                
        sql.execute('''INSERT INTO '''+Configuration.config_columns_table+''' VALUES (
                            'salary-profession-france',
                            'average_salary_per_profession',
                            'Economic Incentives',
                            '0',
                            'no',
                            'N/A')''')
                            
        sql.execute('''INSERT INTO '''+Configuration.config_columns_table+''' VALUES (
                            'salary-profession-france',
                            'average_salary_per_profession',
                            'Economic Incentives',
                            '1',
                            'yes',
                            'N/A')''', True)
                            
        # HTML configuration instance sample one country - Salary per profession Germany
        sql.execute('''INSERT INTO '''+Configuration.config_instances_table+''' VALUES (
                            'salary-profession-germany',
                            'Germany',
                            'http://www.salaryexplorer.com/average-salary.php?&loctype=1&loc=81',
                            'html',
                            '0',
                            'yes')''')
                
        sql.execute('''INSERT INTO '''+Configuration.config_columns_table+''' VALUES (
                            'salary-profession-germany',
                            'average_salary_per_profession',
                            'Economic Incentives',
                            '0',
                            'no',
                            'N/A')''')
                            
        sql.execute('''INSERT INTO '''+Configuration.config_columns_table+''' VALUES (
                            'salary-profession-germany',
                            'average_salary_per_profession',
                            'Economic Incentives',
                            '1',
                            'yes',
                            'N/A')''', True)
                            
        # HTML configuration instance sample one country - Salary per profession South Africa
        sql.execute('''INSERT INTO '''+Configuration.config_instances_table+''' VALUES (
                            'salary-profession-south-africa',
                            'South Africa',
                            'http://www.salaryexplorer.com/average-salary.php?&loctype=1&loc=201',
                            'html',
                            '0',
                            'yes')''')
                
        sql.execute('''INSERT INTO '''+Configuration.config_columns_table+''' VALUES (
                            'salary-profession-south-africa',
                            'average_salary_per_profession',
                            'Economic Incentives',
                            '0',
                            'no',
                            'N/A')''')
                            
        sql.execute('''INSERT INTO '''+Configuration.config_columns_table+''' VALUES (
                            'salary-profession-south-africa',
                            'average_salary_per_profession',
                            'Economic Incentives',
                            '1',
                            'yes',
                            'N/A')''', True)
                            
        # HTML configuration instance sample one country - Salary per profession UAE
        sql.execute('''INSERT INTO '''+Configuration.config_instances_table+''' VALUES (
                            'salary-profession-uae',
                            'United Arab Emirates',
                            'http://www.salaryexplorer.com/average-salary.php?&loctype=1&loc=227',
                            'html',
                            '0',
                            'yes')''')
                
        sql.execute('''INSERT INTO '''+Configuration.config_columns_table+''' VALUES (
                            'salary-profession-uae',
                            'average_salary_per_profession',
                            'Economic Incentives',
                            '0',
                            'no',
                            'N/A')''')
                            
        sql.execute('''INSERT INTO '''+Configuration.config_columns_table+''' VALUES (
                            'salary-profession-uae',
                            'average_salary_per_profession',
                            'Economic Incentives',
                            '1',
                            'yes',
                            'N/A')''', True)
                            
        # HTML configuration instance sample one country - Salary per profession UK
        sql.execute('''INSERT INTO '''+Configuration.config_instances_table+''' VALUES (
                            'salary-profession-uk',
                            'United Kingdom',
                            'http://www.salaryexplorer.com/average-salary.php?&loctype=1&loc=228',
                            'html',
                            '0',
                            'yes')''')
                
        sql.execute('''INSERT INTO '''+Configuration.config_columns_table+''' VALUES (
                            'salary-profession-uk',
                            'average_salary_per_profession',
                            'Economic Incentives',
                            '0',
                            'no',
                            'N/A')''')
                            
        sql.execute('''INSERT INTO '''+Configuration.config_columns_table+''' VALUES (
                            'salary-profession-uk',
                            'average_salary_per_profession',
                            'Economic Incentives',
                            '1',
                            'yes',
                            'N/A')''', True)
                            
        # HTML configuration instance sample one country - Salary per profession USA
        sql.execute('''INSERT INTO '''+Configuration.config_instances_table+''' VALUES (
                            'salary-profession-usa',
                            'United States',
                            'http://www.salaryexplorer.com/average-salary.php?&loctype=1&loc=229',
                            'html',
                            '0',
                            'yes')''')
                
        sql.execute('''INSERT INTO '''+Configuration.config_columns_table+''' VALUES (
                            'salary-profession-usa',
                            'average_salary_per_profession',
                            'Economic Incentives',
                            '0',
                            'no',
                            'N/A')''')
                            
        sql.execute('''INSERT INTO '''+Configuration.config_columns_table+''' VALUES (
                            'salary-profession-usa',
                            'average_salary_per_profession',
                            'Economic Incentives',
                            '1',
                            'yes',
                            'N/A')''', True)
                            
        # CSV configuration instance sample - Health Care System Description
        sql.execute('''INSERT INTO '''+Configuration.config_instances_table+''' VALUES (
                            'health-care-system-description',
                            '0',
                            'samples_csv/healthCareSystemByCountry.csv',
                            'csv',
                            ';',
                            'no')''')
                
        sql.execute('''INSERT INTO '''+Configuration.config_columns_table+''' VALUES (
                            'health-care-system-description',
                            'health_care_system',
                            'Medical Care',
                            '1',
                            'yes',
                            'N/A')''', True)
                            
        # CSV configuration instance sample one country - Unemployment Rate Australia
        sql.execute('''INSERT INTO '''+Configuration.config_instances_table+''' VALUES (
                            'unemployment-rate-australia',
                            'Australia',
                            'samples_csv/unemploymentRatePerYear.csv',
                            'csv',
                            ';',
                            'yes')''')
                
        sql.execute('''INSERT INTO '''+Configuration.config_columns_table+''' VALUES (
                            'unemployment-rate-australia',
                            'unemployment_rate_per_year',
                            'Job Opportunities',
                            '0',
                            'no',
                            'N/A')''')
                            
        sql.execute('''INSERT INTO '''+Configuration.config_columns_table+''' VALUES (
                            'unemployment-rate-australia',
                            'unemployment_rate_per_year',
                            'Job Opportunities',
                            '3',
                            'yes',
                            'N/A')''', True)
                            
        # CSV configuration instance sample one country - Unemployment Rate Canada
        sql.execute('''INSERT INTO '''+Configuration.config_instances_table+''' VALUES (
                            'unemployment-rate-canada',
                            'Canada',
                            'samples_csv/unemploymentRatePerYear.csv',
                            'csv',
                            ';',
                            'yes')''')
                
        sql.execute('''INSERT INTO '''+Configuration.config_columns_table+''' VALUES (
                            'unemployment-rate-canada',
                            'unemployment_rate_per_year',
                            'Job Opportunities',
                            '0',
                            'no',
                            'N/A')''')
                            
        sql.execute('''INSERT INTO '''+Configuration.config_columns_table+''' VALUES (
                            'unemployment-rate-canada',
                            'unemployment_rate_per_year',
                            'Job Opportunities',
                            '2',
                            'N/A',
                            'yes')''', True)
                            
        # CSV configuration instance sample one country - Unemployment Rate France
        sql.execute('''INSERT INTO '''+Configuration.config_instances_table+''' VALUES (
                            'unemployment-rate-france',
                            'France',
                            'samples_csv/unemploymentRatePerYear.csv',
                            'csv',
                            ';',
                            'yes')''')
                
        sql.execute('''INSERT INTO '''+Configuration.config_columns_table+''' VALUES (
                            'unemployment-rate-france',
                            'unemployment_rate_per_year',
                            'Job Opportunities',
                            '0',
                            'no',
                            'N/A')''')
                            
        sql.execute('''INSERT INTO '''+Configuration.config_columns_table+''' VALUES (
                            'unemployment-rate-france',
                            'unemployment_rate_per_year',
                            'Job Opportunities',
                            '5',
                            'yes',
                            'N/A')''', True)
                            
        # CSV configuration instance sample one country - Unemployment Rate Germany
        sql.execute('''INSERT INTO '''+Configuration.config_instances_table+''' VALUES (
                            'unemployment-rate-germany',
                            'Germany',
                            'samples_csv/unemploymentRatePerYear.csv',
                            'csv',
                            ';',
                            'yes')''')
                
        sql.execute('''INSERT INTO '''+Configuration.config_columns_table+''' VALUES (
                            'unemployment-rate-germany',
                            'unemployment_rate_per_year',
                            'Job Opportunities',
                            '0',
                            'no',
                            'N/A')''')
                            
        sql.execute('''INSERT INTO '''+Configuration.config_columns_table+''' VALUES (
                            'unemployment-rate-germany',
                            'unemployment_rate_per_year',
                            'Job Opportunities',
                            '6',
                            'yes',
                            'N/A')''', True)
                            
        # CSV configuration instance sample one country - Unemployment Rate UK
        sql.execute('''INSERT INTO '''+Configuration.config_instances_table+''' VALUES (
                            'unemployment-rate-uk',
                            'United Kingdom',
                            'samples_csv/unemploymentRatePerYear.csv',
                            'csv',
                            ';',
                            'yes')''')
                
        sql.execute('''INSERT INTO '''+Configuration.config_columns_table+''' VALUES (
                            'unemployment-rate-uk',
                            'unemployment_rate_per_year',
                            'Job Opportunities',
                            '0',
                            'no',
                            'N/A')''')
                            
        sql.execute('''INSERT INTO '''+Configuration.config_columns_table+''' VALUES (
                            'unemployment-rate-uk',
                            'unemployment_rate_per_year',
                            'Job Opportunities',
                            '10',
                            'yes',
                            'N/A')''', True)
                            
        # CSV configuration instance sample one country - Unemployment Rate USA
        sql.execute('''INSERT INTO '''+Configuration.config_instances_table+''' VALUES (
                            'unemployment-rate-usa',
                            'United States',
                            'samples_csv/unemploymentRatePerYear.csv',
                            'csv',
                            ';',
                            'yes')''')
                
        sql.execute('''INSERT INTO '''+Configuration.config_columns_table+''' VALUES (
                            'unemployment-rate-usa',
                            'unemployment_rate_per_year',
                            'Job Opportunities',
                            '0',
                            'no',
                            'N/A')''')
                            
        sql.execute('''INSERT INTO '''+Configuration.config_columns_table+''' VALUES (
                            'unemployment-rate-usa',
                            'unemployment_rate_per_year',
                            'Job Opportunities',
                            '1',
                            'yes',
                            'N/A')''', True)
                            
        # HTML configuration instance sample one country - Languages Australia
        sql.execute('''INSERT INTO '''+Configuration.config_instances_table+''' VALUES (
                            'languages-australia',
                            'Australia',
                            'samples_csv/languages_australia.csv',
                            'csv',
                            ';',
                            'no')''')
                
        sql.execute('''INSERT INTO '''+Configuration.config_columns_table+''' VALUES (
                            'languages-australia',
                            'most_widely_spoken_languages',
                            'Education',
                            '0',
                            'no',
                            'N/A')''')
                            
        sql.execute('''INSERT INTO '''+Configuration.config_columns_table+''' VALUES (
                            'languages-australia',
                            'most_widely_spoken_languages',
                            'Education',
                            '1',
                            'yes',
                            'N/A')''', True)
                            
        # HTML configuration instance sample one country - Languages Canada
        sql.execute('''INSERT INTO '''+Configuration.config_instances_table+''' VALUES (
                            'languages-canada',
                            'Canada',
                            'samples_csv/languages_canada.csv',
                            'csv',
                            ';',
                            'no')''')
                
        sql.execute('''INSERT INTO '''+Configuration.config_columns_table+''' VALUES (
                            'languages-canada',
                            'most_widely_spoken_languages',
                            'Education',
                            '0',
                            'no',
                            'N/A')''')
                            
        sql.execute('''INSERT INTO '''+Configuration.config_columns_table+''' VALUES (
                            'languages-canada',
                            'most_widely_spoken_languages',
                            'Education',
                            '1',
                            'yes',
                            'N/A')''', True)
                            
        # HTML configuration instance sample one country - Languages France
        sql.execute('''INSERT INTO '''+Configuration.config_instances_table+''' VALUES (
                            'languages-france',
                            'France',
                            'samples_csv/languages_france.csv',
                            'csv',
                            ';',
                            'no')''')
                
        sql.execute('''INSERT INTO '''+Configuration.config_columns_table+''' VALUES (
                            'languages-france',
                            'most_widely_spoken_languages',
                            'Education',
                            '0',
                            'no',
                            'N/A')''')
                            
        sql.execute('''INSERT INTO '''+Configuration.config_columns_table+''' VALUES (
                            'languages-france',
                            'most_widely_spoken_languages',
                            'Education',
                            '1',
                            'yes',
                            'N/A')''', True)
                            
        # HTML configuration instance sample one country - Languages Germany
        sql.execute('''INSERT INTO '''+Configuration.config_instances_table+''' VALUES (
                            'languages-germany',
                            'Germany',
                            'samples_csv/languages_germany.csv',
                            'csv',
                            ';',
                            'no')''')
                
        sql.execute('''INSERT INTO '''+Configuration.config_columns_table+''' VALUES (
                            'languages-germany',
                            'most_widely_spoken_languages',
                            'Education',
                            '0',
                            'no',
                            'N/A')''')
                            
        sql.execute('''INSERT INTO '''+Configuration.config_columns_table+''' VALUES (
                            'languages-germany',
                            'most_widely_spoken_languages',
                            'Education',
                            '1',
                            'yes',
                            'N/A')''', True)
                            
        # HTML configuration instance sample one country - Languages South Africa
        sql.execute('''INSERT INTO '''+Configuration.config_instances_table+''' VALUES (
                            'languages-south-africa',
                            'South Africa',
                            'samples_csv/languages_south_africa.csv',
                            'csv',
                            ';',
                            'no')''')
                
        sql.execute('''INSERT INTO '''+Configuration.config_columns_table+''' VALUES (
                            'languages-south-africa',
                            'most_widely_spoken_languages',
                            'Education',
                            '0',
                            'no',
                            'N/A')''')
                            
        sql.execute('''INSERT INTO '''+Configuration.config_columns_table+''' VALUES (
                            'languages-south-africa',
                            'most_widely_spoken_languages',
                            'Education',
                            '1',
                            'yes',
                            'N/A')''', True)
                            
        # HTML configuration instance sample one country - Languages UAE
        sql.execute('''INSERT INTO '''+Configuration.config_instances_table+''' VALUES (
                            'languages-uae',
                            'United Arab Emirates',
                            'samples_csv/languages_uae.csv',
                            'csv',
                            ';',
                            'no')''')
                
        sql.execute('''INSERT INTO '''+Configuration.config_columns_table+''' VALUES (
                            'languages-uae',
                            'most_widely_spoken_languages',
                            'Education',
                            '0',
                            'no',
                            'N/A')''')
                            
        sql.execute('''INSERT INTO '''+Configuration.config_columns_table+''' VALUES (
                            'languages-uae',
                            'most_widely_spoken_languages',
                            'Education',
                            '1',
                            'yes',
                            'N/A')''', True)
                            
        # HTML configuration instance sample one country - Languages UK
        sql.execute('''INSERT INTO '''+Configuration.config_instances_table+''' VALUES (
                            'languages-uk',
                            'United Kingdom',
                            'samples_csv/languages_uk.csv',
                            'csv',
                            ';',
                            'no')''')
                
        sql.execute('''INSERT INTO '''+Configuration.config_columns_table+''' VALUES (
                            'languages-uk',
                            'most_widely_spoken_languages',
                            'Education',
                            '0',
                            'no',
                            'N/A')''')
                            
        sql.execute('''INSERT INTO '''+Configuration.config_columns_table+''' VALUES (
                            'languages-uk',
                            'most_widely_spoken_languages',
                            'Education',
                            '1',
                            'yes',
                            'N/A')''', True)
                            
        # HTML configuration instance sample one country - Languages USA
        sql.execute('''INSERT INTO '''+Configuration.config_instances_table+''' VALUES (
                            'languages-usa',
                            'United States',
                            'samples_csv/languages_usa.csv',
                            'csv',
                            ';',
                            'no')''')
                
        sql.execute('''INSERT INTO '''+Configuration.config_columns_table+''' VALUES (
                            'languages-usa',
                            'most_widely_spoken_languages',
                            'Education',
                            '0',
                            'no',
                            'N/A')''')
                            
        sql.execute('''INSERT INTO '''+Configuration.config_columns_table+''' VALUES (
                            'languages-usa',
                            'most_widely_spoken_languages',
                            'Education',
                            '1',
                            'yes',
                            'N/A')''', True)
                            
        sql.close()
    
    for i in range(1, len(sys.argv)):
        cmd = sys.argv[i]
        if cmd == '-create':
            Configuration.create()
        elif cmd == '-drop':
            Configuration.drop()
        elif cmd == '-filters':
            Configuration.filters()
        elif cmd == '-sample':
            sample()
        else:
            print cmd+' is not a valid command.'
