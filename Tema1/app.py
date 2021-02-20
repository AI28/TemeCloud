from weather_controller import *
from metrics_controller import *
from location_controller import *
from price_controller import *
from log_metrics import *



def application (environ, start_response):

    http_methods = ["GET", "HEAD", "POST", "PUT", "DELETE", "CONNECT", "OPTIONS", "TRACE", "PATCH"]
    status, response_headers, response_body = router(environ, http_methods)
    start_response(status, response_headers)

    return [response_body]

def router(environ, http_methods):

    routes = {"/api/v1/metrics": metrics_route, "/api/v1/prices": prices_route, "/api/v1/weather": weather_route, "/api/v1/location": location_route}

    request_uri = environ["REQUEST_URI"].split("?")[0]
    route_controller =  routes.get(request_uri, invalid_route) 

    return logging(route_controller, environ, http_methods)

#mod_wsgi-express start-server main.py