from random import randint, uniform
import grequests
from requests import get
from sys import argv
from time import sleep


if len(argv) == 4:


    number_of_requests = int(argv[1])
    batch_size = int(argv[2])

    #request_payload = {"lat": coordinates[0], "lon": coordinates[1], "from":start_date, "until":end_date}
    #request.open("POST","http://172.17.4.60:8000/api/v1/prices"); 

    no_of_batches = int(number_of_requests) // int(batch_size)

    for i in range(0, no_of_batches):

        requests = []

        for j in range(0, batch_size):

            from_day = randint(1,28)
            until_day = randint(from_day,28)
            from_month = randint(3,12)
            until_month = randint(from_month,12)

            from_date = "/".join([str(from_day), str(from_month), "2021"])
            until_date = "/".join([str(until_day), str(until_month), "2021"])

            req_payload = {"lat": uniform(-180, 180), "lon": uniform(-180,180), "from":from_date, "until":until_date}
            requests.append(grequests.request('POST', argv[3], data=req_payload))

        grequests.map(requests)

        get_average_latency = get('http://172.17.4.60:8000/api/v1/metrics?last_x=50&latency_avg=1')
        print(f"Batch {i} average latency {get_average_latency.text}")

        sleep(4)
