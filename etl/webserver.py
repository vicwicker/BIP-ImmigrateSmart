import sys
sys.path.insert(0, 'webserver/html')
import main

import cgi, cgitb
import traceback

from Configuration import Configuration
from ContentReader import ContentReader

# Do not change this name function... It needs to be webserver:app so
# gunicorn (python webserver) finds it
def app(environ, start_response):
    def parse_req(form):
        def insertETL(form):
            # Get data from fields
            config_name         = form['config_name'][0]
            source_file         = form['source_file'][0]
            source_file_type    = form['source_file_type'][0]
            delimiter_char      = form['delimiter_char'][0] if 'delimiter_char' in form else None
            potential_csv       = form['potential_csv'][0] if 'potential_csv' in form else None
            countries_col       = form['country_name'][0]
            if countries_col == 'multiple':
                countries_col = form['countries_col'][0]
                
            extras = 'NULL'
            if not delimiter_char is None:
                extras = delimiter_char
            elif not potential_csv is None:
                extras = potential_csv
                    
            headers = 'false'
            if 'has_headers' in form:
                headers = 'true'
            
            criterias = []
            for i in range(1, int(form['criteria_count'][0])+1):
                criterias.append({
                    'criteria':form['criteria_'+str(i)][0], 
                    'column':form['col_num'+str(i)][0],
                    'category':form['category_'+str(i)][0]
                })
            
            Configuration.insert(config_name, source_file, source_file_type, extras, headers, countries_col, criterias)
            
        def potentialCsv(form):
            potential_csv_list = ContentReader.html(form['source_file'][0], form['config_name'][0])
            potential_csv_data = '<html><body>'
            number = 0
            for potential_csv_current in potential_csv_list:
                potential_csv_data = potential_csv_data+'<p>Insert '+str(number)+' to use this CSV</p><table border="1">'
                for row, i in zip(potential_csv_current, range(10)):
                    potential_csv_data = potential_csv_data+'<tr>'
                    for value in row:
                        potential_csv_data = potential_csv_data+'<td>'+str(value)+'</td>'
                    potential_csv_data = potential_csv_data+'</tr>'
                potential_csv_data = potential_csv_data+'</table>'
                number = number+1
            potential_csv_data = potential_csv_data+'</body></html>'
            
            return potential_csv_data
            
            
        if not 'potential_csv_submit' in form:
            insertETL(form)
            return None
        else:
            return potentialCsv(form)

    try:
        data = None
        content_length = int(environ.get('CONTENT_LENGTH', 0))
        if content_length > 0:
            form = cgi.parse_qs(environ['wsgi.input'].read(content_length))
            data = parse_req(form)
        
        if data is None:
            data = main.html()
                
        # This is how we play with the HTTP
        status = '200 OK'
        response_headers = [
            ('Content-type','text/html'),
            ('Content-Length', str(len(data)))
        ]
        start_response(status, response_headers)
        
        # This is how we return the HTML code
        return iter([data])
    except Exception, e:
        data = traceback.format_exc()
        status = '200 OK'
        response_headers = [
            ('Content-type','text/plain'),
            ('Content-Length', str(len(data)))
        ]
        start_response(status, response_headers)
        
        # This is how we return the HTML code
        return iter([data])
