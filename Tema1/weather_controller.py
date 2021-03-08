from responses import * 
from os import getenv
from urllib.parse import urlparse, urljoin, parse_qsl, parse_qs
import requests
from math import trunc

def weather_route(environ, http_methods):

    route_methods = ["GET"]

    if environ["REQUEST_METHOD"] not in http_methods:
        return bad_request(environ["REQUEST_METHOD"], http_methods)

    if environ["REQUEST_METHOD"] not in route_methods:
        return method_not_allowed(environ["REQUEST_METHOD"], environ["REQUEST_URI"], route_methods)

    return weather_middleware(environ)

def weather_middleware(environ):

    api_key = getenv('WEATHER_SERVICE')
    weather_request = get_weather(environ, api_key)

    status = status_codes.get(weather_request.status_code, "100 Continue")
    response_headers = [(header, value) for header, value in weather_request.headers.items()]
    response_body = weather_request.text.encode()

    return status, response_headers, response_body

def get_weather(environ, api_key):

    url_args = parse_qs(environ['QUERY_STRING'])

    lat = url_args.get('lat', 0)[0]
    lon = url_args.get('lon', 0)[0]
    #API-ul celor de la openweather accepta numere rationale cu doar 2 cifre dupa virgula 
    lat = '.'.join([lat.split(".")[0], lat.split(".")[1][0:2]])
    lon = '.'.join([lon.split(".")[0], lon.split(".")[1][0:2]])

    weather_endpoint = f'https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}'
    weather_request = requests.get(weather_endpoint)

    return weather_request