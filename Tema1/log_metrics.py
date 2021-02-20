from time import time
from sys import getsizeof
import json


def logging(route_to_log, environ, http_methods):

    start_time = time()

    status, headers, body = route_to_log(environ, http_methods)

    end_time = time()

    metric_dict = {
        "latency": end_time - start_time,
        "request_route": environ["REQUEST_URI"],
        "client": environ["HTTP_HOST"],
        "user_agent": environ["HTTP_USER_AGENT"],
        "response_content_length": getsizeof(body),
        "resonse_status": status,
        "response_headers": headers,
        "response_body": body
    }

    with open(f"{time()}.json", "w") as metric_serialization:
        metric_json = json.dumps(metric_dict)
        metric_serialization.write(metric_json)
    
    return status, headers, body.encode()