import sys, sqlite3

class SQLiteDriver:
    
    # SQLite configuration DB
    config_db = './config/config_db.db'

    # Configuration instance table
    config_instances_table = 'instances'

    # Configuration read column table
    config_columns_table = 'columns'

    # Filters table (i.e., list of countries)
    config_filters_table = 'filters'
    
    # File from which obtaining the country filter list
    filters_file = './config/filters.list'
    
    def __init__(self):
        self.connection = sqlite3.connect(SQLiteDriver.config_db)
        self.cursor = self.connection.cursor()
        
    # Executes the statement
    def execute(self, statement, commit = False):
        result = self.cursor.execute(statement)
        if commit:
            self.commit()
        return result
        
    # Just in case we puntually need to make a single commit
    def commit(self):
        self.connection.commit()
        
    # Closes the connection no longer needed
    def close(self):
        self.connection.close()
        
    # Predefined functionalities
    def create(self):
        self.execute('''CREATE TABLE '''+SQLiteDriver.config_instances_table+''' (
                            config_name TEXT,
                            country_in TEXT,
                            file_uri TEXT,
                            file_type TEXT,
                            delimiter TEXT)''')
                
        self.execute('''CREATE TABLE '''+SQLiteDriver.config_columns_table+''' (
                            config_name TEXT,
                            criteria TEXT,
                            column TEXT,
                            fact TEXT)''', True)
        
    def drop(self):
        self.execute('DROP TABLE '+SQLiteDriver.config_instances_table)
        self.execute('DROP TABLE '+SQLiteDriver.config_columns_table)
        self.execute('DROP TABLE '+SQLiteDriver.config_filters_table, True)
        
    def filters(self, drop = False):
        if drop:
            self.execute('DROP TABLE '+SQLiteDriver.config_filters_table)
    
        self.execute('''CREATE TABLE '''+SQLiteDriver.config_filters_table+''' (
                            country TEXT)''')
            
        with open(SQLiteDriver.filters_file, 'r') as f:
            lines = f.readlines()
            for line in lines:
                countries = line.split(';')
                for country in countries:
                    # Additional chracter parsing will be needed before insertion
                    self.execute('''INSERT INTO '''+SQLiteDriver.config_filters_table+'''
                        VALUES (\''''+country.strip().lower()+'''\')''')
        
        self.commit()
        
    # NOTE: Only works for unidimensional criteria
    def insertNewInstance(config_name, source_file, source_file_type, delimiter_char, countries_col, criteria_cols):
        sql.execute('''INSERT INTO '''+SQLiteDriver.config_instances_table+''' VALUES (
                        ''' + config_name + ''',
                        ''' + countries_col + ''',
                        ''' + source_file + ''',
                        ''' + source_file_type + ''',
                        ''' + delimiter_char + ''')''')
            
        for k in criteria_cols.keys():
            sql.execute('''INSERT INTO '''+SQLiteDriver.config_columns_table+''' VALUES (
                            ''' + config_name + ''',
                            ''' + criteria_cols[k] + ''',
                            ''' + k + ''',
                            'yes')''')
            
        
# Main program
sql = SQLiteDriver()

def sample():
    sql.execute('DELETE FROM '+SQLiteDriver.config_instances_table)
    sql.execute('DELETE FROM '+SQLiteDriver.config_columns_table)
                   
    # XLS configuration instance sample - Minimum Wage / Paid Annual Leave
    sql.execute('''INSERT INTO '''+SQLiteDriver.config_instances_table+''' VALUES (
                        'doingbusiness',
                        '0',
                        'http://www.doingbusiness.org/~/media/GIAWB/Doing%20Business/Documents/Miscellaneous/LMR-DB15-DB14-service-sector-data-points-and-details.xlsx',
                        'xls',
                        '0')''')
            
    sql.execute('''INSERT INTO '''+SQLiteDriver.config_columns_table+''' VALUES (
                        'doingbusiness',
                        'minimum_wage',
                        '4',
                        'yes')''')
                
    sql.execute('''INSERT INTO '''+SQLiteDriver.config_columns_table+''' VALUES (
                        'doingbusiness',
                        'paid_annual_leave',
                        '16',
                        'yes')''', True)  
                        
    # HTML configuration instance sample - Foreign Worker Salaries
    sql.execute('''INSERT INTO '''+SQLiteDriver.config_instances_table+''' VALUES (
                        'nationmaster',
                        '1',
                        'http://www.nationmaster.com/country-info/stats/People/Migration/Foreign-worker-salaries',
                        'html',
                        NULL)''')
            
    sql.execute('''INSERT INTO '''+SQLiteDriver.config_columns_table+''' VALUES (
                        'nationmaster',
                        'foreign_worker_salaries',
                        '2',
                        'yes')''', True)
                        
    # HTML configuration instance sample - Area
    sql.execute('''INSERT INTO '''+SQLiteDriver.config_instances_table+''' VALUES (
                        'cia-area',
                        '1',
                        'https://www.cia.gov/library/publications/the-world-factbook/rankorder/2147rank.html?countryname=Australia&countrycode=as&regionCode=aus&rank=6#as',
                        'html',
                        NULL)''')
            
    sql.execute('''INSERT INTO '''+SQLiteDriver.config_columns_table+''' VALUES (
                        'cia-area',
                        'area',
                        '2',
                        'yes')''', True)
                        
    # HTML configuration instance sample - Population
    sql.execute('''INSERT INTO '''+SQLiteDriver.config_instances_table+''' VALUES (
                        'cia-population',
                        '1',
                        'https://www.cia.gov/library/publications/the-world-factbook/rankorder/2119rank.html?countryname=Australia&countrycode=as&regionCode=aus&rank=56#as',
                        'html',
                        NULL)''')
            
    sql.execute('''INSERT INTO '''+SQLiteDriver.config_columns_table+''' VALUES (
                        'cia-population',
                        'population',
                        '2',
                        'yes')''', True)
                        
    # HTML configuration instance sample - GDP per capita
    sql.execute('''INSERT INTO '''+SQLiteDriver.config_instances_table+''' VALUES (
                        'cia-gdp-per-capita',
                        '1',
                        'https://www.cia.gov/library/publications/the-world-factbook/rankorder/2004rank.html?countryname=Australia&countrycode=as&regionCode=aus&rank=21#as',
                        'html',
                        NULL)''')
            
    sql.execute('''INSERT INTO '''+SQLiteDriver.config_columns_table+''' VALUES (
                        'cia-gdp-per-capita',
                        'gdp_per_capita',
                        '2',
                        'yes')''', True)
                        
    # HTML configuration instance sample - Cost of Living
    sql.execute('''INSERT INTO '''+SQLiteDriver.config_instances_table+''' VALUES (
                        'numbero-cost-of-living',
                        '0',
                        'http://www.numbeo.com/cost-of-living/rankings_by_country.jsp',
                        'html',
                        NULL)''')
            
    sql.execute('''INSERT INTO '''+SQLiteDriver.config_columns_table+''' VALUES (
                        'numbero-cost-of-living',
                        'cost_of_living',
                        '3',
                        'yes')''', True)
                        
    # HTML configuration instance sample - Crimes Rate
    sql.execute('''INSERT INTO '''+SQLiteDriver.config_instances_table+''' VALUES (
                        'numbero-cime-rate',
                        '0',
                        'http://www.numbeo.com/crime/rankings_by_country.jsp',
                        'html',
                        NULL)''')
            
    sql.execute('''INSERT INTO '''+SQLiteDriver.config_columns_table+''' VALUES (
                        'numbero-cime-rate',
                        'crime_rate',
                        '1',
                        'yes')''', True)
                        
    # HTML configuration instance sample - Quality of Health Care System
    sql.execute('''INSERT INTO '''+SQLiteDriver.config_instances_table+''' VALUES (
                        'numbero-quality-health-care-system',
                        '0',
                        'http://www.numbeo.com/health-care/rankings_by_country.jsp',
                        'html',
                        NULL)''')
            
    sql.execute('''INSERT INTO '''+SQLiteDriver.config_columns_table+''' VALUES (
                        'numbero-quality-health-care-system',
                        'quality_of_health_care_system',
                        '1',
                        'yes')''', True)
                        
    # HTML configuration instance sample - Average Overall Monthly Salary
    sql.execute('''INSERT INTO '''+SQLiteDriver.config_instances_table+''' VALUES (
                        'nationmaster-avg-overall-salary',
                        '1',
                        'http://www.nationmaster.com/country-info/stats/Cost-of-living/Average-monthly-disposable-salary/After-tax',
                        'html',
                        NULL)''')
            
    sql.execute('''INSERT INTO '''+SQLiteDriver.config_columns_table+''' VALUES (
                        'nationmaster-avg-overall-salary',
                        'average_overall_monthly_salary',
                        '2',
                        'yes')''', True)
                        
    # HTML configuration instance sample - Average Income Taxes
    sql.execute('''INSERT INTO '''+SQLiteDriver.config_instances_table+''' VALUES (
                        'kpmg-avg-income-tax',
                        '0',
                        'http://www.kpmg.com/GLOBAL/EN/SERVICES/TAX/TAX-TOOLS-AND-RESOURCES/Pages/individual-income-tax-rates-table.aspx',
                        'html',
                        NULL)''')
            
    sql.execute('''INSERT INTO '''+SQLiteDriver.config_columns_table+''' VALUES (
                        'kpmg-avg-income-tax',
                        'average_income_taxes',
                        '8',
                        'yes')''', True)
                        
    # HTML configuration instance sample - Unemployment Rate
    sql.execute('''INSERT INTO '''+SQLiteDriver.config_instances_table+''' VALUES (
                        'cia-unemployment-rate',
                        '1',
                        'https://www.cia.gov/library/publications/the-world-factbook/rankorder/2129rank.html?countryname=Australia&countrycode=as&regionCode=aus&rank=53#as',
                        'html',
                        NULL)''')
            
    sql.execute('''INSERT INTO '''+SQLiteDriver.config_columns_table+''' VALUES (
                        'cia-unemployment-rate',
                        'unemployment_rate',
                        '2',
                        'yes')''', True)
                        
    # HTML configuration instance sample - Health Care Expenditure
    sql.execute('''INSERT INTO '''+SQLiteDriver.config_instances_table+''' VALUES (
                        'cia-health-care-expenditure',
                        '1',
                        'https://www.cia.gov/library/publications/the-world-factbook/rankorder/2225rank.html?countryname=Cambodia&countrycode=cb&regionCode=eas&rank=118#cb',
                        'html',
                        NULL)''')
            
    sql.execute('''INSERT INTO '''+SQLiteDriver.config_columns_table+''' VALUES (
                        'cia-health-care-expenditure',
                        'health_care_expenditure',
                        '2',
                        'yes')''', True)
                        
    # HTML configuration instance sample - Percentage of English Speakers
    sql.execute('''INSERT INTO '''+SQLiteDriver.config_instances_table+''' VALUES (
                        'wiki-pct-english-speakers',
                        '0',
                        'http://en.wikipedia.org/wiki/List_of_countries_by_English-speaking_population',
                        'html',
                        NULL)''')
            
    sql.execute('''INSERT INTO '''+SQLiteDriver.config_columns_table+''' VALUES (
                        'wiki-pct-english-speakers',
                        'percentage_of_english_speakers',
                        '1',
                        'yes')''', True)
                        
    # HTML configuration instance sample one country - Salary per profession Australia
    sql.execute('''INSERT INTO '''+SQLiteDriver.config_instances_table+''' VALUES (
                        'salary-profession-australia',
                        'Australia',
                        'http://www.salaryexplorer.com/average-salary.php?&loctype=1&loc=13',
                        'html',
                        NULL)''')
            
    sql.execute('''INSERT INTO '''+SQLiteDriver.config_columns_table+''' VALUES (
                        'salary-profession-australia',
                        'average_salary_per_profession',
                        '0',
                        'no')''')
                        
    sql.execute('''INSERT INTO '''+SQLiteDriver.config_columns_table+''' VALUES (
                        'salary-profession-australia',
                        'average_salary_per_profession',
                        '1',
                        'yes')''', True)
                        
    # HTML configuration instance sample one country - Salary per profession Canada
    sql.execute('''INSERT INTO '''+SQLiteDriver.config_instances_table+''' VALUES (
                        'salary-profession-canada',
                        'Canada',
                        'http://www.salaryexplorer.com/average-salary.php?&loctype=1&loc=38',
                        'html',
                        NULL)''')
            
    sql.execute('''INSERT INTO '''+SQLiteDriver.config_columns_table+''' VALUES (
                        'salary-profession-canada',
                        'average_salary_per_profession',
                        '0',
                        'no')''')
                        
    sql.execute('''INSERT INTO '''+SQLiteDriver.config_columns_table+''' VALUES (
                        'salary-profession-canada',
                        'average_salary_per_profession',
                        '1',
                        'yes')''', True)
                        
    # HTML configuration instance sample one country - Salary per profession France
    sql.execute('''INSERT INTO '''+SQLiteDriver.config_instances_table+''' VALUES (
                        'salary-profession-france',
                        'France',
                        'http://www.salaryexplorer.com/average-salary.php?&loctype=1&loc=74',
                        'html',
                        NULL)''')
            
    sql.execute('''INSERT INTO '''+SQLiteDriver.config_columns_table+''' VALUES (
                        'salary-profession-france',
                        'average_salary_per_profession',
                        '0',
                        'no')''')
                        
    sql.execute('''INSERT INTO '''+SQLiteDriver.config_columns_table+''' VALUES (
                        'salary-profession-france',
                        'average_salary_per_profession',
                        '1',
                        'yes')''', True)
                        
    # HTML configuration instance sample one country - Salary per profession Germany
    sql.execute('''INSERT INTO '''+SQLiteDriver.config_instances_table+''' VALUES (
                        'salary-profession-germany',
                        'Germany',
                        'http://www.salaryexplorer.com/average-salary.php?&loctype=1&loc=81',
                        'html',
                        NULL)''')
            
    sql.execute('''INSERT INTO '''+SQLiteDriver.config_columns_table+''' VALUES (
                        'salary-profession-germany',
                        'average_salary_per_profession',
                        '0',
                        'no')''')
                        
    sql.execute('''INSERT INTO '''+SQLiteDriver.config_columns_table+''' VALUES (
                        'salary-profession-germany',
                        'average_salary_per_profession',
                        '1',
                        'yes')''', True)
                        
    # HTML configuration instance sample one country - Salary per profession South Africa
    sql.execute('''INSERT INTO '''+SQLiteDriver.config_instances_table+''' VALUES (
                        'salary-profession-south-africa',
                        'South Africa',
                        'http://www.salaryexplorer.com/average-salary.php?&loctype=1&loc=201',
                        'html',
                        NULL)''')
            
    sql.execute('''INSERT INTO '''+SQLiteDriver.config_columns_table+''' VALUES (
                        'salary-profession-south-africa',
                        'average_salary_per_profession',
                        '0',
                        'no')''')
                        
    sql.execute('''INSERT INTO '''+SQLiteDriver.config_columns_table+''' VALUES (
                        'salary-profession-south-africa',
                        'average_salary_per_profession',
                        '1',
                        'yes')''', True)
                        
    # HTML configuration instance sample one country - Salary per profession UAE
    sql.execute('''INSERT INTO '''+SQLiteDriver.config_instances_table+''' VALUES (
                        'salary-profession-uae',
                        'United Arab Emirates',
                        'http://www.salaryexplorer.com/average-salary.php?&loctype=1&loc=227',
                        'html',
                        NULL)''')
            
    sql.execute('''INSERT INTO '''+SQLiteDriver.config_columns_table+''' VALUES (
                        'salary-profession-uae',
                        'average_salary_per_profession',
                        '0',
                        'no')''')
                        
    sql.execute('''INSERT INTO '''+SQLiteDriver.config_columns_table+''' VALUES (
                        'salary-profession-uae',
                        'average_salary_per_profession',
                        '1',
                        'yes')''', True)
                        
    # HTML configuration instance sample one country - Salary per profession UK
    sql.execute('''INSERT INTO '''+SQLiteDriver.config_instances_table+''' VALUES (
                        'salary-profession-uk',
                        'United Kingdom',
                        'http://www.salaryexplorer.com/average-salary.php?&loctype=1&loc=228',
                        'html',
                        NULL)''')
            
    sql.execute('''INSERT INTO '''+SQLiteDriver.config_columns_table+''' VALUES (
                        'salary-profession-uk',
                        'average_salary_per_profession',
                        '0',
                        'no')''')
                        
    sql.execute('''INSERT INTO '''+SQLiteDriver.config_columns_table+''' VALUES (
                        'salary-profession-uk',
                        'average_salary_per_profession',
                        '1',
                        'yes')''', True)
                        
    # HTML configuration instance sample one country - Salary per profession USA
    sql.execute('''INSERT INTO '''+SQLiteDriver.config_instances_table+''' VALUES (
                        'salary-profession-usa',
                        'United States',
                        'http://www.salaryexplorer.com/average-salary.php?&loctype=1&loc=229',
                        'html',
                        NULL)''')
            
    sql.execute('''INSERT INTO '''+SQLiteDriver.config_columns_table+''' VALUES (
                        'salary-profession-usa',
                        'average_salary_per_profession',
                        '0',
                        'no')''')
                        
    sql.execute('''INSERT INTO '''+SQLiteDriver.config_columns_table+''' VALUES (
                        'salary-profession-usa',
                        'average_salary_per_profession',
                        '1',
                        'yes')''', True)
                        
    # Excel configuration instance sample one country - Unemployment Rate Australia
    sql.execute('''INSERT INTO '''+SQLiteDriver.config_instances_table+''' VALUES (
                        'unemployment-rate-australia',
                        'Australia',
                        'http://www.bls.gov/fls/intl_unemployment_rates_monthly.xls',
                        'xls',
                        '1')''')
            
    sql.execute('''INSERT INTO '''+SQLiteDriver.config_columns_table+''' VALUES (
                        'unemployment-rate-australia',
                        'unemployment_rate_per_year',
                        '0',
                        'no')''')
                        
    sql.execute('''INSERT INTO '''+SQLiteDriver.config_columns_table+''' VALUES (
                        'unemployment-rate-australia',
                        'unemployment_rate_per_year',
                        '6',
                        'yes')''', True)
                        
    # Excel configuration instance sample one country - Unemployment Rate Canada
    sql.execute('''INSERT INTO '''+SQLiteDriver.config_instances_table+''' VALUES (
                        'unemployment-rate-canada',
                        'Canada',
                        'http://www.bls.gov/fls/intl_unemployment_rates_monthly.xls',
                        'xls',
                        '1')''')
            
    sql.execute('''INSERT INTO '''+SQLiteDriver.config_columns_table+''' VALUES (
                        'unemployment-rate-canada',
                        'unemployment_rate_per_year',
                        '0',
                        'no')''')
                        
    sql.execute('''INSERT INTO '''+SQLiteDriver.config_columns_table+''' VALUES (
                        'unemployment-rate-canada',
                        'unemployment_rate_per_year',
                        '4',
                        'yes')''', True)
                        
    # Excel configuration instance sample one country - Unemployment Rate France
    sql.execute('''INSERT INTO '''+SQLiteDriver.config_instances_table+''' VALUES (
                        'unemployment-rate-france',
                        'France',
                        'http://www.bls.gov/fls/intl_unemployment_rates_monthly.xls',
                        'xls',
                        '1')''')
            
    sql.execute('''INSERT INTO '''+SQLiteDriver.config_columns_table+''' VALUES (
                        'unemployment-rate-france',
                        'unemployment_rate_per_year',
                        '0',
                        'no')''')
                        
    sql.execute('''INSERT INTO '''+SQLiteDriver.config_columns_table+''' VALUES (
                        'unemployment-rate-france',
                        'unemployment_rate_per_year',
                        '10',
                        'yes')''', True)
                        
    # Excel configuration instance sample one country - Unemployment Rate Germany
    sql.execute('''INSERT INTO '''+SQLiteDriver.config_instances_table+''' VALUES (
                        'unemployment-rate-germany',
                        'Germany',
                        'http://www.bls.gov/fls/intl_unemployment_rates_monthly.xls',
                        'xls',
                        '1')''')
            
    sql.execute('''INSERT INTO '''+SQLiteDriver.config_columns_table+''' VALUES (
                        'unemployment-rate-germany',
                        'unemployment_rate_per_year',
                        '0',
                        'no')''')
                        
    sql.execute('''INSERT INTO '''+SQLiteDriver.config_columns_table+''' VALUES (
                        'unemployment-rate-germany',
                        'unemployment_rate_per_year',
                        '12',
                        'yes')''', True)
                        
    # Excel configuration instance sample one country - Unemployment Rate UK
    sql.execute('''INSERT INTO '''+SQLiteDriver.config_instances_table+''' VALUES (
                        'unemployment-rate-uk',
                        'United Kingdom',
                        'http://www.bls.gov/fls/intl_unemployment_rates_monthly.xls',
                        'xls',
                        '1')''')
            
    sql.execute('''INSERT INTO '''+SQLiteDriver.config_columns_table+''' VALUES (
                        'unemployment-rate-uk',
                        'unemployment_rate_per_year',
                        '0',
                        'no')''')
                        
    sql.execute('''INSERT INTO '''+SQLiteDriver.config_columns_table+''' VALUES (
                        'unemployment-rate-uk',
                        'unemployment_rate_per_year',
                        '20',
                        'yes')''', True)
                        
    # Excel configuration instance sample one country - Unemployment Rate USA
    sql.execute('''INSERT INTO '''+SQLiteDriver.config_instances_table+''' VALUES (
                        'unemployment-rate-usa',
                        'United States',
                        'http://www.bls.gov/fls/intl_unemployment_rates_monthly.xls',
                        'xls',
                        '1')''')
            
    sql.execute('''INSERT INTO '''+SQLiteDriver.config_columns_table+''' VALUES (
                        'unemployment-rate-usa',
                        'unemployment_rate_per_year',
                        '0',
                        'no')''')
                        
    sql.execute('''INSERT INTO '''+SQLiteDriver.config_columns_table+''' VALUES (
                        'unemployment-rate-usa',
                        'unemployment_rate_per_year',
                        '2',
                        'yes')''', True)
                        
    # CSV configuration instance sample - Health Care System Description
    sql.execute('''INSERT INTO '''+SQLiteDriver.config_instances_table+''' VALUES (
                        'health-care-system-description',
                        '0',
                        'healthCareSystemByCountry.csv',
                        'csv',
                        ';')''')
            
    sql.execute('''INSERT INTO '''+SQLiteDriver.config_columns_table+''' VALUES (
                        'health-care-system-description',
                        'health_care_system',
                        '1',
                        'yes')''', True)

for i in range(1, len(sys.argv)):
    cmd = sys.argv[i]
    if cmd == '-create':
        sql.create()
        sql.filters()
    elif cmd == '-drop':
        sql.drop()
    elif cmd == '-filters':
        sql.filters(True)
    elif cmd == '-sample':
        sample()
    else:
        print cmd+' is not a valid command.'
        
sql.close()