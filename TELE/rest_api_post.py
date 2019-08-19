#!/usr/bin/env python3
import requests
from random import randint
import argparse
import time


BASE_API_URL = 'http://127.0.0.1:8000/api/v1/'

def add_fdata(measure,user,password):
    global BASE_API_URL
    req = requests.post('{}fdata/'.format(BASE_API_URL), data=measure, auth=(user,password))
    return req

measurement = {
    "sensor": 7,
    "value": 66
}

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("-n", dest="n", required=True, help="number of values to be added")
    parser.add_argument("-id", dest="id", required=True, help="sensor id")
    parser.add_argument("-u", dest="u", required=True, help="username")
    parser.add_argument("-p", dest="p", required=True, help="password")

    args = parser.parse_args()

    if args.n and args.u and args.p and args.id: 
        print("Add {} random values".format(args.n))
        for item in range(int(args.n)):
            random_number = randint(0,100)
            measurement.update({"sensor":args.id,"value": random_number})
            print(" * {}".format(add_fdata(measurement,args.u,args.p).text))
            time.sleep(5)
    else:
        print("Missing parameters")
