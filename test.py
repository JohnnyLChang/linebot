#!/usr/bin/env python
import os
import sys
import json

def get_ngrok_url():
    os.system("curl  http://localhost:4040/api/tunnels > tunnels.json")
    url = ""
    with open('tunnels.json') as data_file:    
        datajson = json.load(data_file)
        
    for i in datajson['tunnels']:
        url = i['public_url'] +'\n'
    print(url)

if __name__ == "__main__":
    get_ngrok_url()
