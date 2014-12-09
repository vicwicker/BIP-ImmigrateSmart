import csv, xlrd
import re
import sys, os
import urllib2, httplib, HTMLParser

import utils

# Reads file contents from URLs
class ContentReader:
    
     # Read CSV file
    @staticmethod
    def csv(file_uri, delimiter = ','):
        file = open(file_uri, 'r')
        data = []
        for row in csv.reader(file, delimiter = utils.to_str(delimiter)):
            data.append([str(val) for val in row])
        return data
    
    # Read XLS file
    @staticmethod
    def xls(file_uri, sheet = 0):
        socket = urllib2.urlopen(file_uri)
        xlfile = xlrd.open_workbook(file_contents = socket.read())
        xlsheet = xlfile.sheet_by_index(sheet)
        data = []
        for rownum in range(xlsheet.nrows):
            data.append([utils.to_str(val) for val in xlsheet.row_values(rownum)])
        return data
        
    # Read HTML file
    @staticmethod
    def html(file_uri, config_name, which = -1, headers = False):
        class ImmigrateSmartParser(HTMLParser.HTMLParser):
        
        	tags = ['table', 'td', 'tr', 'th']
        	
        	# Valid data
        	valid_data = '^[\w%$][\w\s,.\'\-/%()$]*$'
        
        	class AST:
        		def __init__(self, type, value, parent):
        			self.type = type
        			self.value = value
        			self.children = []
        			self.parent = parent
        			
        		def copy_of(self, ast):
        			self.type = ast.type
        			self.value = ast.value
        			self.children = ast.children
        			self.parent = ast.parent
        			
        		def trim(self):
        		    for child in self.children:
        		        # If child is a tag but with no data on it then 
        		        # it is a missing leave
        		        if len(child.children) == 0 and child.type == 'tag':
        		            child.type = 'data'
        		            child.value = None
        		        else:
        		            child.trim()
        		    # If there is only one node as children we put it up to
        		    # balance potential CSV heights
        		    if len(self.children) == 1:
        		        self.copy_of(self.children[0])
        			
        		def csvize(self):
        		    def csvize_rec(ast, h, potential_csv):
        		        if len(ast.children) > 0:
        		            potential_current = []
        		            for child in ast.children:
        		                csvize_rec(child, h+1, potential_csv)
        		                if child.type == 'data':
        		                    potential_current.append({'h':h, 'value':utils.to_str(child.value)})
        		            if len(potential_current) == len(ast.children):
        		                potential_csv.append([i for i in potential_current])
        		                
        		    # Prepare the tree to identify potential CSVs
        		    self.trim()
        		    
        		    # Prepare the potential CSV list
        		    potential_csv = []
        		    
        		    # CSVize it!
        		    csvize_rec(self, 0, potential_csv)
        		    
        		    # Process the results
        		    results = []
        		    current = []
        		    
        		    for i in range(0, len(potential_csv)):
        		        if i > 0:
        		            if potential_csv[i][0]['h'] != potential_csv[i-1][0]['h'] and \
        		                    len(potential_csv[i][0]) == len(potential_csv[i-1][0]):
        		                results.append(current)
        		                current = []
        		        current.append([p['value'] for p in potential_csv[i]])
        		            
        		    results.append(current)
        		    
        		    # In case of nothing is asked we return everything
        		    if which == -1:
        		        return results
        		    
        		    to_return = results[which]
        		    if headers:
        		        to_return.pop(0)
        		        
        		    return to_return
        	
        	def root(self):
        		self.ast = ImmigrateSmartParser.AST('root', None, None)
        		self.data = ''
        		self.charref = False
        	
        	def handle_starttag(self, tag, attrs):
        		if tag in ImmigrateSmartParser.tags:
        		    child = ImmigrateSmartParser.AST('tag', tag, self.ast)
        		    self.ast.children.append(child)
        		    self.ast = child
        		    self.data = ''
        		
        	def handle_endtag(self, tag):
        		if tag in ImmigrateSmartParser.tags:
        			if self.data != '':
        				child = ImmigrateSmartParser.AST('data', self.data, self.ast)
        				self.ast.children.append(child)
        				
        			self.ast = self.ast.parent
        			self.data = ''
        			self.in_valid_tag = False
        			
        	def handle_data(self, data):
        		if self.data == '' or (self.data != '' and self.charref):
        			data = re.sub('[ ]+', ' ', data.strip())
        			if re.search(ImmigrateSmartParser.valid_data, data):
        			    self.data = self.data+data
        			    self.charref = False
        				
        	def handle_charref(self, name):
        		self.charref = True
        	
        parser = ImmigrateSmartParser()
        
        parser.root()
        
        try:
            socket = urllib2.urlopen(file_uri)
            content = socket.read()
        except httplib.IncompleteRead:
        	os.system('wget -q '+file_uri+' -O /tmp/'+config_name)
        	content = open('/tmp/'+config_name, 'r').read()
        	
        parser.feed(content.decode('utf-8'))
        
        potential_csv = parser.ast.csvize()
        
        return potential_csv
        	