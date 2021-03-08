status_codes = {
  100: "100 Continue",
  200: "200 OK",
  400: "400 Bad Request",
  401: "401 Unauthorized",
  404: "404 Not Found",
  405: "405 Method Not Allowed",
  500: "500 Internal Server Error"
}

def invalid_route(environ, http_methods):

    status = "404 Not Found"
    response_body = "%s is not a valid route." % environ["REQUEST_URI"]
    response_body = response_body.encode()
    response_headers = [("Content-Type","text/plain"),("Content-Length", str(len(response_body)))]

    return status, response_headers, response_body


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