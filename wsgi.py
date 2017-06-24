"""
WSGI config for eorder project.
It exposes the WSGI callable as a module-level variable named ``application``.
For more information on this file, see
https://docs.djangoproject.com/en/1.6/howto/deployment/wsgi/
"""
import os
import sys
import subprocess
import time
import subprocess
import signal
import json
from django.core.handlers.wsgi import WSGIHandler

def run_ngrok():
    proc = subprocess.Popen(['ngrok http 8090 > /var/log/django/ngrok.log 2>&1'], shell=True)
    time.sleep(10)
    return (proc)

def get_ngrok_url():
    os.system("curl  http://localhost:4040/api/tunnels > /var/log/django/tunnels.json")
    url = ""
    with open('/var/log/django/tunnels.json') as data_file:
        datajson = json.load(data_file)

    for i in datajson['tunnels']:
        url = i['public_url'] +'\n'
    return (url)

def signal_handler(signal, frame):
    pngrok.terminate()
    print('Terminate process')

root = os.path.dirname(__file__)
sys.path.insert(0, root)
os.environ['SECRET_KEY'] = '89mit^_am5^0v(__ukh1@aafq(nh0xacn(=leo$h(0_$&r6p16))))'
os.environ['LINE_CHANNEL_ACCESS_TOKEN'] = 'PxbSfhsHqORsh9Xv8qdL12it0pFtJLEDWkd1qQ7zQ5/wqZ7gP2SBlwt7U/N7w4qe+Me7Lh5VQIMQVhfOOv+FkbkdUjeZSpB0KA1x5YogamreysXADhhj+o7qYCEUpOCuBUrC69hz1SIGt5Me7LGqIwdB04t89/1O/w1cDnyilFU='
os.environ['LINE_CHANNEL_SECRET'] = '433bccd149d8e4f4c2e48bd3914eadf8'
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mainlinebot.settings")

pngrok = run_ngrok()
print(get_ngrok_url())
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()


