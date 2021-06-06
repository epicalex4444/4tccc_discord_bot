#!/usr/bin/env python3

import sqlite3
import os

conn = sqlite3.connect('../4tccc_data.db')
cursor = conn.cursor()
cursor.execute('SELECT epoche, header, body FROM webpages WHERE key=?', (os.environ['REQUEST_URI'][1:],))
webpageData = cursor.fetchone()
conn.close()

print('''Content-type:text/html

<!DOCTYPE html>
<html lang="en">
<head>
<title>4TCCC</title>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="timeCreated" content="{0}">
<link rel="stylesheet" href="base.css">
</head>
<body>
<div id="header">{1}</div>
<div id="numbers"></div>
<div id="main">{2}</div>
<div id="side">
<img src="4TCCC.png" alt="4TCCC logo" width="200" height="200"></img>
<div id="timer">time till webpage expires:
24h, 0m</div>
<div>webpage made for 4TCCC by epicalex4444</div>
</div>
<script src="base.js"></script>
</body>
</html>'''.format(webpageData[0], webpageData[1], webpageData[2]))
