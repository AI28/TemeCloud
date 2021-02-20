from responses import * 
from location_controller import *
from os import getenv
import json
from urllib.parse import urlparse, urljoin, parse_qsl, parse_qs
import requests
from math import trunc

def prices_route(environ, http_methods):

    route_methods = ["POST"]

    if environ["REQUEST_METHOD"] not in http_methods:
        return bad_request(environ["REQUEST_METHOD"], http_methods)

    if environ["REQUEST_METHOD"] not in route_methods:
        return method_not_allowed(environ["REQUEST_METHOD"], environ["REQUEST_URI"], route_methods)

    request_body_size = 0

    try:
        request_body_size = int(environ.get('CONTENT_LENGTH', 0))
        print(request_body_size)
        print(environ['CONTENT_LENGTH'])

    except (ValueError):
        request_body_size = 0

    request_body = environ['wsgi.input'].read(request_body_size).decode()
    d = json.loads(request_body)

    return prices_middleware(environ, d)

def prices_middleware(environ, d):

    status, headers, body = location_middleware(environ)
    body = json.loads(body)

    api_key = getenv('PRICES_SERVICE')
    prices_request = get_prices(environ, api_key, body, d)
 
    status = status_codes.get(prices_request.status_code, "100 Continue")
    response_headers = [(header, value) for header, value in prices_request.headers.items() \
                        if header not in ["Access-Control-Allow-Credentials", "Access-Control-Allow-Origin", "Transfer-Encoding", "Content-Encoding"]]

    response_headers.append(("Access-Control-Allow-Origin", "*"))
    response_body = prices_request.text.encode()

    response_dict = json.loads(response_body)
    if len(response_dict["data"]) > 0:
        response_dict = {i:j for i, j in response_dict["data"][0].items() if i in ["cityFrom","cityTo","price","fly_duration"]}
    else:
        response_dict = {"message": "No flights found."}

    response_body = json.dumps(response_dict)

    return status, response_headers, response_body


def get_location(lat, lon):

    location_endpoint = f'https://api.skypicker.com/locations?type=radius&lat={lat}&lon={lon}&location_types=airport'
    location_request = requests.get(location_endpoint)

    return location_request

def get_prices(environ, api_key, body, d):

    my_location_request =  get_location(body['latitude'], body['longitude'])
    my_destination_request = get_location(d['lat'], d['lon'])

    my_location = my_location_request.text
    my_destination = my_destination_request.text

    my_location_dict = json.loads(my_location)
    my_destination_dict = json.loads(my_destination)

    prices_endpoint = f'https://api.skypicker.com/flights?date_from={d["from"]}&date_to={d["from"]}&return_from={d["until"]}&return_to={d["until"]}&fly_from={my_location_dict["locations"][0]["id"]}&fly_to={my_destination_dict["locations"][0]["id"]}&partner=picky'
    print(prices_endpoint)
    prices_request = requests.get(prices_endpoint)


    return prices_request