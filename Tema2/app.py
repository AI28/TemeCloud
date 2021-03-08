# from weather_controller import *
# from metrics_controller import *
# from location_controller import *
# from price_controller import *
# from log_metrics import *

'''
Micro-micro-framework workflow = register your routes by adding them in the routes dictionary.(before-hand, import the apropriate modules.)
'''


import re
from Routes.BooksRoute import *
from Routes.AuthorsRoute import *
from metrics_controller import metrics_route
from log_metrics import logging

def application (environ, start_response):

    http_methods = ["GET", "HEAD", "POST", "PUT", "DELETE", "CONNECT", "OPTIONS", "TRACE", "PATCH"]
    status, response_headers, response_body = router(environ, http_methods)
    start_response(status, response_headers)

    return [response_body]

def router(environ, http_methods):

    routes = {"/api/v1/metrics": metrics_route, "/api/v1/books": books_route, "/api/v1/authors": authors_route}

    request_uri = environ["REQUEST_URI"].split("?")[0]

    url_re = re.compile("^\/(\w)+\/(\w)+\/(\w)+")
    url_prefix = url_re.match(request_uri).group(0)
    
    route_controller =  routes.get(url_prefix, invalid_route) 

    return route_controller(environ, http_methods)

#mod_wsgi-express start-server main.py