from weather_controller import *
from metrics_controller import *
from pandemic_controller import *
from reccomendation_controller import *



def application (environ, start_response):

    http_methods = ["GET", "HEAD", "POST", "PUT", "DELETE", "CONNECT", "OPTIONS", "TRACE", "PATCH"]
    status, response_headers, response_body = router(environ, http_methods)
    start_response(status, response_headers)

    return [response_body]

def router(environ, http_methods):

    routes = {"/api/v1/metrics": metrics_route, "/api/v1/getReccomendation": reccomendation_route, "/api/v1/weather": weather_route}

    request_uri = environ["REQUEST_URI"].split("?")[0]
    route_controller =  routes.get(request_uri, invalid_route) 

    return route_controller(environ, http_methods)
