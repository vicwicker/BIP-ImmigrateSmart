import cgi
import traceback

# Do not change this name function... It needs to be webserver:app so
# gunicorn (python webserver) finds it
def app(environ, start_response):
    try:
        param = cgi.parse_qs(environ['QUERY_STRING']).get('param', [''])[0]
        data = """<html>
                    <title>ETL web interface</title>
                    <body>This is just an empty interface that detected you sent """+str(param)+"""!</body>
                </html>"""
                
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