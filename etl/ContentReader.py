import csv, xlrd, urllib2

import utils

# Reads file contents from URLs
class ContentReader:
    
    # Read XLS file
    @staticmethod
    def xls(file_uri, sheet = 0):
        socket = urllib2.urlopen(file_uri)
        xlfile = xlrd.open_workbook(file_contents = socket.read())
        xlsheet = xlfile.sheet_by_index(sheet)
        rows = []
        for rownum in range(xlsheet.nrows):
            rows.append([utils.to_str(val) for val in xlsheet.row_values(rownum)])
        return rows
        
    # Read CSV file
    @staticmethod
    def csv(file_uri, delimiter = ','):
        file = open(file_uri, 'r')
        reader = csv.reader(file, delimiter = utils.to_str(delimiter))
        return reader