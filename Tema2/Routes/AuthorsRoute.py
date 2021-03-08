from responses import *
from Repositories import authorsRepository
from urllib.parse import urlparse, urljoin, parse_qsl, parse_qs

import os
import json

def get_req_body(environ):

    request_body_size = 0
    try:
        request_body_size = int(environ.get('CONTENT_LENGTH', 0))
    except (ValueError):
        request_body_size = 0

    body = environ["wsgi.input"].read(request_body_size)

    return json.loads(body.decode())

def authors_route(environ, http_methods):

    collection = "".join(environ["REQUEST_URI"].split("/")[:-1])

    print(environ["REQUEST_URI"].split("/")[-1])

    if environ["REQUEST_URI"].split("/")[-1] == "authors":
        return collection_route(environ)
    else:
        return resource_route(environ)

def collection_route(environ):

    allowed_methods = ["GET", "POST"]
    request_method = environ["REQUEST_METHOD"]

    if request_method not in allowed_methods:
        return method_not_allowed(request_method, environ["REQUEST_URI"], allowed_methods)
    
    elif request_method == "GET":

       result = authorsRepository.get()

       status_code_key = 0

       if result is False:
           status_code_key = 404
           return resource_not_found(environ, http_methods)
       else:
           status_code_key = 200
           return resource_response(environ, status_code_key, result, "authors")

    elif request_method == "POST":
       
       body = get_req_body(environ)
       result, obj_id = authorsRepository.post(body)
       print(result)
       status_code_key = 0

       if result is not False:
           status_code_key = 201
           return resource_post(environ, status_code_key, result, obj_id,"author")
       else:
           return "404 Not Found", [], []
       
def resource_route(environ):
    
    allowed_methods = ["GET", "PUT", "DELETE"]
    request_method = environ["REQUEST_METHOD"]
    author_id = environ["REQUEST_URI"].split("/")[-1]

    query ={"id": author_id}

    if request_method not in allowed_methods:
        return method_not_allowed(request_method, environ["REQUEST_URI"], allowed_methods)
    
    elif request_method == "GET":

       result = authorsRepository.get(query)

       status_code_key = 0

       if result is False:
           status_code_key = 404
       else:
           status_code_key = 200 

       return resource_response(environ, status_code_key, result, "author")

    elif request_method == "DELETE":
        
        result = authorsRepository.delete(query)

        status_code_key = 0

        if result is False:
            status_code_key = 404
            return resource_not_found(environ, allowed_methods)
        else:
            status_code_key = 200
            return deleted_resource(status_code_key, "author")

    
    elif request_method == "PUT":

        body = get_req_body(environ)        

        result = authorsRepository.put(author_id, body)
        status_code_key = 0

        if result is False:
            status_code_key = 404
            return resource_not_found(environ, allowed_methods)
        else:
            status_code_key = 201
            del body["_id"]
            return resource_put(environ, status_code_key, body, "author")