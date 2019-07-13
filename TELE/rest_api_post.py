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

if __name__ == "__main__":
	print("Adding 5 random temps")

	pomiar = {
	    "name": "Temp TEST",
	    "description": "Pomiar {}",
	    "owner": 1,
	    "raw_value": "{}",
		"eng_value": 0
	}

	for item in range(5):
		temp = randint(0,100)
		pomiar.update({
			"description" : "Pomiar {}".format(item),
			"raw_value": "{}".format(temp),
			"eng_value": temp
		})
		add_fdata(pomiar)
