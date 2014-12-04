import cgi, cgitb

from SQLiteDriver import SQLiteDriver

form = cgi.FieldStorage() 

# Get data from fields
config_name = form.getvalue('config_name')
source_file  = form.getvalue('source_file')
source_file_type  = form.getvalue('source_file_type')
delimiter_char  = form.getvalue('delimiter_char')
countries_col  = form.getvalue('country_name')
if (countries_col == 'multiple'):
    countries_col = form.getvalue('countries_col')

criteria_count = form.getvalue('criteria_count')
criteria_cols = []
i = 1
for i in range(criteria_count):
    key = form.getvalue('col_num' + i)
    value = form.getvalue('criteria_' + i)
    criteria_cols[key] = value

sql = SQLiteDriver()
sql.insertNewInstance(config_name, source_file, source_file_type, delimiter_char, countries_col, criteria_cols)