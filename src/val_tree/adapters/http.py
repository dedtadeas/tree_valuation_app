#!/usr/bin/env python3

import requests

class HTTPAdapter:
    def __init__(self):
        self.headers = {'Content-Type': 'application/json'}

    def post(self, url, data):
        r = requests.post(url, headers=self.headers, json=data)
        r.raise_for_status()
        return r.json()

def make():
    return HTTPAdapter()

