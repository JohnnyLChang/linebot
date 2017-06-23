#!/usr/bin/env python
import json
import os
import sys
import time
import subprocess
import signal

def run_ngrok():
    proc = subprocess.Popen(['ngrok http 8000 > ngrok.log 2>&1'], shell=True)
    time.sleep(10)
    return (proc)

def get_ngrok_url():
    os.system("curl  http://localhost:4040/api/tunnels > tunnels.json")
    url = ""
    with open('tunnels.json') as data_file:    
        datajson = json.load(data_file)
        
    for i in datajson['tunnels']:
        url = i['public_url'] +'\n'
    return (url)

def signal_handler(signal, frame):
    pngrok.terminate()
    print('Terminate process')
    sys.exit(0)

if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "line_echobot.settings")
    pngrok = run_ngrok()
    print(get_ngrok_url())

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
