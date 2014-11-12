import csv
import xlrd
import urllib2

# Convert any object to String
def tostr (val):
    if (isinstance(val, float)):
        return str(round(val, 0))
    
    return val.encode('utf-8')
    
# Retrieve data from an Excel file
def read_excel (file_uri, cols, filters, delimiter):
    # Read Excel file from URL
    socket = urllib2.urlopen(file_uri)
    xlfile = xlrd.open_workbook(file_contents = socket.read())
    xlsheet = xlfile.sheet_by_index(0)
    
    rows = []
    for rownum in range(xlsheet.nrows):
        rows.append([tostr(val) for val in xlsheet.row_values(rownum)])
    
    filtered = filter(lambda row: row[0] in filters, rows)
    result = []
    for row in filtered:
        result.append([row[i] for i in cols])
    return result

# Retrieve data from a CSV file
def read_csv (file_uri, cols, filters, delimiter):
    csv_file = open(file_uri, 'rb')
    reader = csv.reader(csv_file, delimiter=delimiter)
    filtered = filter(lambda row: row[0] in filters, reader)
    result = []
    for row in filtered:
        result.append([row[i] for i in cols])
    return result


######################
# Main Program Start #
######################

print 'Welcome to ImmigrateSmart Sample Data Flow!'

config_name = ''        # Name of this ETL configuration
file_uri = ''           # URI of the file to read
criteria_cols = {}      # Dictionary of column : criteria pairs (columns are keys)
filters = []          # List of countries to filter on
delimiter = ''
#initial_refresh = 'Y/N'

# Read configuration name
config_name = 'Sample ETL'

# Read File URI
file_uri = 'workingHours.csv'

# Read Criteria-Column pairs (must be ordered by index)
criteria_cols[0] = 'Country'    # Default to first column, should it be flexible?
criteria_cols[2] = 'Maximum Working Days per Week'
criteria_cols[10] = 'Paid Annual Leave'

# Read Filter List (must match country name exactly, might have problems with UAE, USA, UK)
filters.append('Australia')
filters.append('Canada')
filters.append('Germany')

# Read Delimiter
delimiter = ';'

criteria_res = read_csv(file_uri, criteria_cols.keys(), filters, delimiter)

print '-----------------'
print 'Sample CSV File'
print '-----------------'
for key, val in criteria_cols.items():
    print val + '\t\t\t',
print '\n'

for row in criteria_res:
    print '\t\t\t'.join(row)
    
#### Excel File ####
file_uri = 'http://www.doingbusiness.org/~/media/GIAWB/Doing%20Business/Documents/Miscellaneous/LMR-DB15-DB14-service-sector-data-points-and-details.xlsx'

criteria_cols2 = {}
criteria_cols2[0] = 'Country'    # Default to first column, should it be flexible?
criteria_cols2[4] = 'Minimum Wage'
criteria_cols2[16] = 'Paid Annual Leave'

result = read_excel(file_uri, criteria_cols2.keys(), filters, delimiter)

print '-----------------'
print 'Sample Excel File'
print '-----------------'
for key, val in criteria_cols2.items():
    print val + '\t\t\t',
print '\n'

for row in result:
    print '\t\t\t'.join(row)