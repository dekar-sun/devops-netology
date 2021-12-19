#!/usr/bin/env python3
import socket
from time import sleep
import datetime

wait = 5 #pause between verifications in seconds

hosts = {'drive.google.com':'1.1.1.1', 'mail.google.com':'1.1.1.1', 'google.com':'1.1.1.1'}

while 1==1 :

  for x in hosts:
    ip = socket.gethostbyname(x)
    if ip != hosts[x]:
        print(str(datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")) +' [ERROR] ' + str(x) +' IP mismatch: '+ hosts[x]+' '+ip)
        hosts[x]=ip
    else:
      print(str(datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")) + ' ' + str(x) + ' ' +ip)
  sleep(wait)
  print('-------------------------------------------------------------------------------------------------------------')