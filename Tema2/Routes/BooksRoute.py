from responses import *
from Repositories import booksRepository
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

def books_route(environ, http_methods):

    collection = "".join(environ["REQUEST_URI"].split("/")[:-1])

    print(environ["REQUEST_URI"].split("/")[-1])

    if environ["REQUEST_URI"].split("/")[-1] == "books":
        return collection_route(environ)
    else:
        return resource_route(environ)

def collection_route(environ):

    allowed_methods = ["GET", "POST"]
    request_method = environ["REQUEST_METHOD"]

    if request_method not in allowed_methods:
        return method_not_allowed(request_method, environ["REQUEST_URI"], allowed_methods)
    
    elif request_method == "GET":

       result = booksRepository.get()

       status_code_key = 0

       if result is False:
           status_code_key = 404
           return resource_not_found(environ, http_methods)
       else:
           status_code_key = 200
           return resource_response(environ, status_code_key, result, "books")

    elif request_method == "POST":
       
       body = get_req_body(environ)
       result, obj_id = booksRepository.post(body)
       status_code_key = 0

       if result is not False:
           status_code_key = 201
           return resource_post(environ, status_code_key, result, obj_id, "book")
       else:
           return "404 Not Found", [], []
       
def resource_route(environ):
    
    allowed_methods = ["GET", "PUT", "DELETE"]
    request_method = environ["REQUEST_METHOD"]
    book_id = environ["REQUEST_URI"].split("/")[-1]

    query ={"id": book_id}

    if request_method not in allowed_methods:
        return method_not_allowed(request_method, environ["REQUEST_URI"], allowed_methods)
    
    elif request_method == "GET":

       result = booksRepository.get(query)

       status_code_key = 0

       if result is False:
           status_code_key = 404
           return resource_not_found(environ, allowed_methods)
       else:
           status_code_key = 200 
           return resource_response(environ, status_code_key, result, "book")

    elif request_method == "DELETE":
        
        result = booksRepository.delete(query)

        status_code_key = 0

        if result is False:
            status_code_key = 404
            return resource_not_found(environ, allowed_methods)
        else:
            status_code_key = 200
            return deleted_resource(status_code_key, "book")

    
    elif request_method == "PUT":

        body = get_req_body(environ)        

        result = booksRepository.put(book_id, body)
        status_code_key = 0

        if result is False:
            status_code_key = 404
            return resource_not_found(environ, allowed_methods)
        else:
            status_code_key = 201
            del body["_id"]
            return resource_put(environ, status_code_key, body, "book")