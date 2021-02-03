#known bugs
#webpage automated deletion doesn't seem to work
#takes a while to update things once a webpage is deleted

import random
import os
import time
import sys

webpageDir = '/srv/http/'
webpageURL = 'http://4tccc.mooo.com/'
webpageUptime = 86400 #seconds
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

    file = open(webpageDir + fileName, 'x')
    
    timeCreated = os.path.getctime(webpageDir + fileName)
    metaTag = '<meta name="timeCreated" content="{0}">\n'.format(timeCreated)
    htmlText = templateHTML[:155] + metaTag + templateHTML[155:227] + header + templateHTML[227:274] + body + templateHTML[274:]

    file.write(htmlText)
    file.close()

    webpages[key] = timeCreated
    
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

#starts apache if it isn't running
def start_apache_process():
    apacheRunning = os.system('systemctl status httpd &> /dev/null')
    if not apacheRunning == 0:
        os.system('systemctl restart httpd')
    

#deletes webpages that have expired then returns the time until the next webpage is to be deleted, returns webpage uptime if there is no webpages
def delete_next_webpage():
    currTime = time.time()
    webpageExpiries = []
    webpageToDelete = []

    for key in webpages:
        timeToDelete = webpageUptime - (time.time() - webpages[key])
        if timeToDelete <= 0:
            os.remove(webpageDir + key + '.html')
            webpageToDelete.append(key)
        else:
            webpageExpiries.append(timeToDelete)

    for key in webpageToDelete:
        del webpages[key]

    if len(webpageExpiries) == 0:
        return(webpageUptime)
    else:
        return(min(webpageExpiries))

#hanldes file removing after thier time is up
async def start_webserver():
    start_apache_process()
    init_existing_files()
