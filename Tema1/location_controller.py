from responses import * 
from os import getenv
from urllib.parse import urlparse, urljoin, parse_qsl, parse_qs
import requests
from math import trunc


def location_route(environ, http_methods):

    route_methods = ["GET"]

    if environ["REQUEST_METHOD"] not in http_methods:
        return bad_request(environ["REQUEST_METHOD"], http_methods)

    if environ["REQUEST_METHOD"] not in route_methods:
        return method_not_allowed(environ["REQUEST_METHOD"], environ["REQUEST_URI"], route_methods)

    return location_middleware(environ)

def location_middleware(environ):

    location_response = get_my_location()

    status = status_codes.get(location_response.status_code, "100 Continue")
    response_headers = [(header, value) for header, value in location_response.headers.items()]
    response_body = location_response.text.encode()

    return status, response_headers, response_body

def get_my_location():

    location_api_key = getenv('LOCATION_SERVICE')
    location_endpoint = f'https://api.ipdata.co?api-key={location_api_key}'
    location_request = requests.get(location_endpoint)

    return location_request
