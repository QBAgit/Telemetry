#!/usr/bin/env python3

import requests
import json
import sys
from random import randint

BASE_API_URL = 'http://127.0.0.1:8000/api/v1/'

def add_fdata(measure):
    global BASE_API_URL
    req = requests.post('{}fdata/'.format(BASE_API_URL), measure)
    return req

pomiar = {
    "name": "TESTY",
    "description": "Pomiar",
    "owner": 1,
    "value": 0
}

if __name__ == "__main__":
	print("Adding 5 random temps")



    #for item in range(5):
    #    temp = randint(0,100)
    #    pomiar.update({
    #        "description" : "Pomiar {}".format(item+1),
    #        "raw_value": "{}".format(temp),
    #        "value": temp
    #    })
    #    add_fdata(pomiar)
