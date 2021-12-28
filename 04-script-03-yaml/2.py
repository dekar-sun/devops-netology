#!/usr/bin/env python3
import socket
from time import sleep
import datetime
import json
import yaml

wait = 5  # pause between verifications in seconds

hosts = {'drive.google.com': '1.1.1.1', 'mail.google.com': '1.1.1.1', 'google.com': '1.1.1.1'}

services_error_pool = []

while True:

    for x in hosts:
        ip = socket.gethostbyname(x)
        if ip != hosts[x]:
            print(str(datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")) + ' [ERROR] ' + str(x) + ' IP mismatch: ' +
                  hosts[x] + ' ' + ip)
            hosts[x] = ip
            # json
            with open('./' + x + '.json', 'w') as json_file:
                json_data = json.dumps({x: ip})
                json_file.write(json_data)
            # yaml
            with open('./' + x + '.yml', 'w') as yml_file:
                yml_data = yaml.dump([{x: ip}])
                yml_file.write(yml_data)
            # Create one file for all services in Json and yaml
            services_error_pool.append({x: ip})
            with open('./' + 'services.json', 'w') as json_file:
                json_data = json.dumps(services_error_pool)
                json_file.write(json_data)
            with open('./' + 'services.yml', 'w') as yml_file:
                yml_data = yaml.dump(services_error_pool)
                yml_file.write(yml_data)
        else:
            print(str(datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")) + ' ' + str(x) + ' ' + ip)
    sleep(wait)
    print('-----------------------------------------------------------------------------------------------------------')
