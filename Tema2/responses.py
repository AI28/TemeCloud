import json

status_codes = {
  100: "100 Continue",
  200: "200 OK",
  201: "201 Created",
  400: "400 Bad Request",
  401: "401 Unauthorized",
  404: "404 Not Found",
  405: "405 Method Not Allowed",
  500: "500 Internal Server Error"
}

def resource_response(environ, status_code_key, body, resource_type):

   status_code = status_codes[status_code_key]
   resource_response = {resource_type:body}

   resource_response["interactions"] = {}

   resource_response["interactions"]["delete"] = \
       {"method": "DELETE", "uri": environ["REQUEST_URI"]}

   resource_response_json = json.dumps(resource_response)
   resource_response_json = resource_response_json.encode()
    
   response_headers= [("Content-Type", "application/json"), \
                     ("Content-Length", str(len(resource_response_json)))]
    

   return status_code, response_headers, resource_response_json

def resource_post(environ, status_code_key, body, resource_type):

   status_code = status_codes[status_code_key]
   resource_response = {resource_type:body}
   print(body)
   resource_response["interactions"] = {}

   resource_response["interactions"]["delete"] = \
       {"method": "DELETE", "uri": environ["REQUEST_URI"]}

   
   resource_response_json = json.dumps(resource_response)
   resource_response_json = resource_response_json.encode()

   response_headers= [("Content-Type", "application/json"), \
                     ("Content-Length", str(len(resource_response_json)))]
    
   return status_code, response_headers, resource_response_json


def resource_put(environ, status_code_key, body, resource_type):

   status_code = status_codes[status_code_key]
   resource_response = {resource_type:body}
   print(body)
   print(type(body))
   [print(value) for key, value in body.items()]
   resource_response["interactions"] = {}

   resource_response["interactions"]["delete"] = \
       {"method": "DELETE", "uri": environ["REQUEST_URI"]}

   resource_response_json = json.dumps(resource_response)
   resource_response_json = resource_response_json.encode()

   response_headers= [("Content-Type", "application/json"), \
                     ("Content-Length", str(len(resource_response_json)))]
    
   return status_code, response_headers, resource_response_json


def deleted_resource(status_code_key, resource_type):

    status_code = status_codes[status_code_key]
    resource_response = {"deleted":resource_type}

    return status_code, [], json.dumps(resource_response).encode()


def invalid_route(environ, http_methods):

    status = "404 Not Found"
    response_body = "%s is not a valid route." % environ["REQUEST_URI"]
    response_body = response_body.encode()
    response_headers = [("Content-Type","text/plain"),("Content-Length", str(len(response_body)))]

    return status, response_headers, response_body


def resource_not_found(environ, http_methods):

    status = status_codes[404]
    response_body = "Resource at uri %s not found" % environ["REQUEST_URI"]
    response_body = response_body.encode()

    return status, [], response_body


def bad_request(method, http_methods):

    status = "400 Bad Request"
    response_body = "%s is not a valid HTTP Method. RFC 7231 HTTP Methods are: %s" % (method, http_methods)
    response_body = response_body.encode()
    response_headers = [("Content-Type","text/plain"),("Content-Length", str(len(response_body)))]

    return status, response_headers, response_body


def method_not_allowed(method, route, route_methods):

    status = "405 Method Not Allowed"
    response_body = "%s is not a valid verb for route %s. Use one of the following: %s" % (method, route, " ".join(route_methods))
    response_body = response_body.encode()
    response_headers = [("Content-Type","text/plain"),("Content-Length",str(len(response_body)))]

    return status, response_headers, response_body