from responses import *

from urllib.parse import urlparse, urljoin, parse_qsl, parse_qs
import os
import json
from sys import getsizeof

def metrics_route(environ, http_methods):
    
    
    allowed_methods = ["GET"]

    if os.path.exists("./metrics") is False:
        status = "404 Not Found"
        response_headers = []
        response_body = "404 NOT FOUND. There are two possible causes: no metrics have been collected yet or they have been collected in an unusual place.".encode()

        return status, response_headers, response_body

    metric_logs = os.listdir("./metrics")

    url_args = parse_qs(environ['QUERY_STRING'])
     
    last_x = url_args.get('last_x', ["50"])[0]
    latency_avg = url_args.get('latency_avg', ["0"])[0]
    
    print(f"{last_x} {type(last_x)}   {latency_avg} {type(latency_avg)}")

    if latency_avg not in ["0", "1"]:
        status = "400 Bad Request"
        response_headers = []
        response_body = "400 Bad Request. The url arg latency_avg should be either 0 or 1.".encode()

        return status, response_headers, response_body

    else:
        if last_x.isnumeric() is False or int(last_x) < 0:

            status = "400 Bad Request"
            response_headers = []
            response_body = "400 Bad Rqeust. The last_x should be a positive integer.".encode()

            return status, response_headers, response_body

        else:

            last_x = int(last_x)
            latency_avg = bool(int(latency_avg))
        
     
    status = "200 OK"
    response_headers = [("Content-Type","application/json")]
    response_body = None

    if latency_avg is True:
        response_body = []
    else:
        response_body = {"logs":[]}

    for log in metric_logs:

        with open("./metrics/" + log, "r") as log_file:
            temp_dict = json.loads(log_file.read())
            if latency_avg is True:
                response_body.append(temp_dict["latency"])
            else:
                response_body["logs"].append(temp_dict)

        last_x = last_x - 1

        if last_x == 0:
            break

    if latency_avg is True:
        response_body = {"avg_latency": sum(response_body)/len(response_body)}

    response_body = json.dumps(response_body)

    status = "200 OK"
    response_headers = [("Content-Type","application/json")]


    return status, response_headers, response_body.encode()