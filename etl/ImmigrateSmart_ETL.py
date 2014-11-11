import csv
import xlrd

# Function to read specific columns from a CSV file
def read_csv(file_uri, cols, filters):
    file = open(file_uri, 'rb')
    reader = csv.reader(file, delimiter=';')
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
filter_on = []          # List of countries to filter on
#delimiter = ''
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
filter_on.append('Australia')
filter_on.append('Canada')
filter_on.append('Germany')

criteria_res = read_csv(file_uri, criteria_cols.keys(), filter_on)

for key, val in criteria_cols.items():
    print val + '\t\t\t',
print '\n'

for row in criteria_res:
    print '\t\t\t'.join(row)