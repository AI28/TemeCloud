from time import time
from sys import getsizeof
import json
import os
import os.path


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
        "response_body": body.decode()
    }
    for key, value in metric_dict.items():
        print(f"{key} - {type(value)}")

    if os.path.exists("./metrics") is False:
        os.mkdir("./metrics")

    with open(f"./metrics/{time()}.json", "w") as metric_serialization:
        metric_json = json.dumps(metric_dict)
        metric_serialization.write(metric_json)
    
    return status, headers, body