import random
import os
import time
import sys
import subprocess

#start_webpage and delete_next_webpage should use threading/coroutines instead of janky waiting

webpageDir = 'C:/Apache24/htdocs/'
httpdExeDir = 'C:/Apache24/bin/httpd.exe'
webpageURL = 'http://4TCCC.mooo.com/'
webpageUptime = 3600 #seconds
webpages = dict()

file = open('./template.html')
templateHTML = file.read()
file.close

#generates random key with 4 upercase chars, makes sure the name doesn't exist
def key_generator():  
    while True:
        key = ''
        for _ in range(4):
            key += chr(random.randrange(65, 90))
        if webpages.get(key) == None:
            return key

#creates a custom webpage from the template.html, adding a meta tag with time created, header and body text
def create_webpage(header, body):
    key = key_generator()
    fileName = key + '.html'

    timeCreated = time.time()
    metaTag = '<meta name="timeCreated" content="{0}">\n'.format(timeCreated)
    htmlText = templateHTML[:173] + metaTag + templateHTML[173:373] + header + templateHTML[373:417] + body + templateHTML[417:]

    file = open(webpageDir + fileName, 'x')
    file.write(htmlText)
    file.close()

    webpages[key] = os.path.getctime(webpageDir + fileName)
    
    return webpageURL + fileName

#used on startup, deletes files that are too old and adds all other files to the webpage dict 
def init_existing_files():
    addresses = os.listdir(webpageDir)
    currTime = time.time()
    for address in addresses:
        if address.endswith('.html'):
            path = webpageDir + address
            deleteTime = os.path.getctime(path) + webpageUptime
            if currTime >= deleteTime:
                os.remove(path)
            else:
                webpages[address[:4]] = os.path.getctime(path)

def process_running(processName):
    call = 'TASKLIST', '/FI', 'imagename eq %s' % processName
    output = subprocess.check_output(call).decode()
    last_line = output.strip().split('\r\n')[-1]
    return last_line.lower().startswith(processName.lower())

#starts apache if it isn't running
def start_apache():
    #couldn't start apache2.4 service because of permission errors, so I reverted to directely running the httpd.exe

    if not process_running('httpd.exe'):
        subprocess.Popen(httpdExeDir)

#finds the webpage that is to be deleted next and waits until deleting it
#if there are no webpages it waits an hour, to prevent an extremely inefficient busy waiting loop, still unoptimal though
async def webpage_handler():
    while True:
        minTime = float('inf')
        minKey = ''

        for key in webpages:
            if webpages[key] < minTime:
                minTime = webpages[key]
                minKey = key

        if minKey != '':
            timeToDelete = max(0, webpageUptime - (time.time() - webpages[minKey]))
            time.sleep(timeToDelete)
            os.remove(webpageDir + minKey + '.html')
            del webpages[minKey]
        else:
            #this is still busy waiting but it is much more efficent then not having this wait
            time.sleep(3600)

#hanldes file removing after thier time is up
async def start_webserver():
    start_apache()
    init_existing_files()
