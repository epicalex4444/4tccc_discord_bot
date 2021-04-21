import json
import requests
import base64
import zlib
import sqlite3
import time
import random

challengeDataUrl = 'https://static-api.nkstatic.com/appdocs/11/es/challenges/'

websiteUrl = 'https://4tccc.mooo.com/'

hereos4tc = ['Quincy', 'Gwen', 'Striker', 'Obyn', 'Church', 'Ben', 'Ezili', 'Pat', 'Adora', 'Brickell', 'Etienne', 'Sauda']
towers4tc = ['Dart', 'Boomer', 'Bomb', 'Tack', 'Ice', 'Glue', 'Sniper', 'Sub', 'Bucc', 'Ace', 'Heli', 'Mortar', 'Dartling', 'Wizard', 'Super', 'Ninja', 'Alch', 'Druid', 'Spac', 'Village', 'Engineer']
hereosNK = ['Quincy', 'Gwendolin', 'StrikerJones', 'ObynGreenfoot', 'CaptainChurchill', 'Benjamin', 'Ezili', 'PatFusty', 'Adora', 'AdmiralBrickell', 'Etienne', 'Sauda']
towersNK = ['DartMonkey', 'BoomerangMonkey', 'BombShooter', 'TackShooter', 'IceMonkey', 'GlueGunner', 'SniperMonkey', 'MonkeySub', 'MonkeyBuccaneer', 'MonkeyAce', 'HeliPilot', 'MortarMonkey', 'DartlingGunner', 'WizardMonkey', 'SuperMonkey', 'NinjaMonkey', 'Alchemist', 'Druid', 'SpikeFactory', 'MonkeyVillage', 'EngineerMonkey']

towerAliases = [
    ["quincy"],
    ["gwen", "gwendolin"],
    ["striker", "jones", "strikerJones"],
    ["obyn", "obyngreenfoot"],
    ["church", "churchill", "captainchurchill"],
    ["ben", "benjamin"],
    ["ezili"],
    ["pat", "patfusty"],
    ["adora"],
    ["brick", "brickell", "admiralbrickell"],
    ["etienne", "eti"],
    ['sauda'],
    ["dart", "dartmonkey"],
    ["boomer", "boomerang", "boomerangmonkey"],
    ["bomb", "bombshooter"],
    ["tack", "tackshooter"],
    ["ice", "icemonkey"],
    ["glue", "gluegunner"],
    ["sniper", "snipermonkey"],
    ["sub", "monkeysub"],
    ["bucc", "boat", "buccaneer", "monkeybuccaneer"],
    ["ace", "monkeyace"],
    ["heli", "helipilot"],
    ["mortar", "mortarmonkey"],
    ["dartling", "dartlinggunner"],
    ["wizard", "wizardmonkey", "wiz"],
    ["super", "supermonkey"],
    ["ninja", "ninjamonkey"],
    ["alch", "alchemist"],
    ["druid"],
    ["spac", "spikefactory", "spactory"],
    ["village", "monkeyvillage", "vill"],
    ["engi", "engineer", "engineermonkey"]
]

conn = sqlite3.connect('4tccc_data.db')
cursor = conn.cursor() 

#all elements of a are in b, for lists/tuples, if a is empty it return true
def is_subset(a, b):
    for aElement in a:
        notContain = True
        for bElement in b:
            if aElement == bElement:
                notContain = False
                break
        if notContain:
            return False
    return True

#fills the str with spaces at front or back until it reaches length
def space_fill(string, length, back=True):
    if back:
        for _ in range(length - len(string)):
            string += ' '
    else:
        for _ in range(length - len(string)):
            string = ' ' + string
    return string

#formats tower arrays in an easy way to view
def tower_print(towers):
    temp = []
    for i in range(len(towers)):
        temp.append(space_fill(towers[i], 8))
    return '|'.join(temp)

#changes any valid tower in towers to be it's default name
def tower_alias(towers):
    defaultNames = hereos4tc + towers4tc
    for item in range(len(towers)):
        for tower in range(len(towerAliases)):
            if towers[item].lower() in towerAliases[tower]:
                towers[item] = defaultNames[tower]
    return towers

#return the invalid tower in a list
def validate_towers(towers):
    validTowers = towers4tc + hereos4tc
    invalidTowers = []
    for tower in towers:
        if not tower in validTowers:
            invalidTowers.append(tower)
    return invalidTowers

#takes towers list with 0-4, towers can be unordered, returns found 4tc's formatted for easy reading
def find4tc(towers):
    towers = tower_alias(towers)

    invalidTowers = validate_towers(towers)
    if invalidTowers != []:
        return ['Invalid Towers: {0}'.format(', '.join(invalidTowers)), None, None]

    if towers == []:
        header = 'All Remaining Combos'
    else:
        header = '{0} Combos'.format(', '.join(towers))

    cursor.execute('SELECT * FROM remaining_combos')
    remaningCombos = cursor.fetchall()

    displayStr = ''
    matches = 0
    for combo in remaningCombos:
        if is_subset(towers, combo):
            displayStr += tower_print(combo) + '\n'
            matches += 1

    if matches == 1:
        return ['1 combo found', '```{0}```'.format(displayStr[:-1]), header]
    elif matches == 0:
        return ['0 combos found', None, None]
    else:
        return ['{0} combos found'.format(matches), '```{0}```'.format(displayStr[:-1]), header]

#returns leaderboard formatted for easy reading
#if name is provided returns score, if amount is provided it returns a shortened version of the leaderboard
def get_leaderboard(name=None, amount=None):
    if name != None:
        cursor.execute('SELECT score FROM leaderboard WHERE name=?', (name,))
        score = cursor.fetchone()
        if score == None:
            return ["{0} hasn't submitted yet".format(name), None, None]
        return ["{0}'s score is {1}".format(name, score[0]), None, None]

    cursor.execute('SELECT * FROM leaderboard')
    leaderboard = cursor.fetchall()

    displayStr = ''
    header = ''
    if amount == None or int(amount) >= len(leaderboard):
        header = 'Full Leaderboard'
        for score in leaderboard:
            displayStr += '{0}: {1}\n'.format(space_fill(str(score[0]), 4, False), score[1])
    else:
        header = 'Top {0} Leaderboard'.format(amount)
        amount = int(amount)
        for score in leaderboard:
            if amount == 0:
                break
            displayStr += '{0}: {1}\n'.format(space_fill(str(score[0]), 4, False), score[1])
            amount -= 1

    return [None, '```{0}```'.format(displayStr[:-1]), header]

#returns all the submission formatted for easy reading, if a name is provided if returns ony submissions by that person
#if towers is provided it returns who completed the combo, must have 4 towers
def get_submissions(name=None):
    displayStr = 'Code    |Tower1  |Tower2  |Tower3  |Tower4  |Combos  '
    header = ''

    if name == None:
        cursor.execute('SELECT * FROM submissions')
        submissions = cursor.fetchall()

        header = 'All Submissions'
        displayStr += '|Name\n'

        for submission in submissions:
            temp = []
            for i in submission:
                temp.append(str(i or ''))
            displayStr += tower_print(temp) + '\n'
    else:
        cursor.execute('SELECT code, tower1, tower2, tower3, tower4, combos FROM submissions WHERE name=?', (name,))
        submissions = cursor.fetchall()

        if len(submissions) == 0:
            return ["{0} doesn't exist".format(name), None, None]

        header = "{0}'s submissions".format(name)
        displayStr += '\n'

        for submission in submissions:
            temp = []
            for i in submission:
                temp.append(str(i or ''))
            displayStr += tower_print(temp) + '\n'

    return [None, '```{0}```'.format(displayStr[:-1]), header]

#change name in names, submissions and leaderboard
def change_name(old, new):
    submittedNew = False
    submittedOld = False

    cursor.execute('SELECT * FROM leaderboard WHERE name=?', (new,))
    if cursor.fetchone() != None:
        submittedNew = True

    cursor.execute('SELECT * FROM leaderboard WHERE name=?', (old,))
    if cursor.fetchone() != None:
        submittedOld = True

    if submittedNew and submittedOld:
        raise Exception('cannot change name since the name you are changing to exists and you have submitted under your current name, this is to prevent combo theft')

    cursor.execute('UPDATE names SET name=? WHERE name=?', (new, old))
    cursor.execute('UPDATE leaderboard SET name=? WHERE name=?', (new, old))
    cursor.execute('UPDATE submissions SET name=? WHERE name=?', (new, old))
    conn.commit()

#adds new name or changes an existing name
def set_name(discordId, name):
    cursor.execute('SELECT name FROM names WHERE discordId=?', (discordId,))
    oldName = cursor.fetchone()

    if oldName == None:
        displayStr = '{0} has been added as your name'.format(name)
        cursor.execute('INSERT INTO names VALUES (?, ?)', (discordId, name))
        conn.commit()
    else:
        if oldName[0] == name:
            return 'You have previously set that as your name'
        try:
            change_name(oldName[0], name)
        except Exception as e:
            return str(e)
        displayStr = '{0} changed to {1}'.format(oldName[0], name)

    return displayStr

#returns name from discord id
def get_name(discordId):
    cursor.execute('SELECT name FROM names WHERE discordId=?', (discordId,))
    name = cursor.fetchone()
    if name == None:
        raise Exception('Name not provided and you have no name set, you can set your name via the !name command')
    else:
        return name[0]

#returns raw challenge data from challenge code
def get_challenge_data(code):
    try:
        #this url contains challenge data that is encrypted with zlib than base64
        response = requests.get(challengeDataUrl + code, timeout=10)
        response.raise_for_status()
        #decrypts data and turns it into a dictionary
        return json.loads(zlib.decompress(base64.b64decode(response.text)))
    except requests.exceptions.HTTPError:
        raise Exception('Invalid Code')
    except (requests.exceptions.RequestException):
        raise Exception("Couldn't establish a connection with nk servers")

#returns approximate verison, works by checking for challenge data changes over time
def get_version(cD):
    if cD['bloonModifiers'].get('allCamo', 'undefined') == 'undefined':
        return 9 #9.0 - 10.2
    if cD.get('numberOfPlayers', 'undefined') == 'undefined':
        return 11 #11.0 - 11.2
    if cD.get('replaces', 'undefined') == 'undefined':
        return 12 #12.0
    if cD['towers'][9]['tower'] != 'Adora':
        return 12.1 #12.1 - 13.1
    if cD['towers'][0].get('path1NumBlockedTiers', 'undefined') == 'undefined':
        return 14 #14.0 - 15.2
    if cD['towers'][10]['tower'] != 'AdmiralBrickell':
        return 16 #16.0 - 17.1
    if cD.get('displayIncludedPowers', 'undefined') == 'undefined':
        return 18 #18.0 - 18.1
    if cD['towers'][11]['tower'] != 'Etienne':
        return 19 #19.0 - 19.2
    if cD.get('roundSets', 'undefined') == 'undefined':
        return 20 #20.0 - 20.1
    if cD['bloonModifiers'].get('regrowRateMultiplier', 'undefined') == 'undefined':
        return 21 # 21.0 - 21.1
    return 22 #22.0 - current

#checks if the settings of the challenge match a valid 4tc challenge, cD = challengeData
def valid_settings(cD, version):
    errorStr = ''

    if cD['difficulty'] != 'Hard':
        errorStr += 'Not hard difficulty\n'
    if cD['mode'] != 'Clicks':
        errorStr += 'Not Chimps Mode\n'
    if not (cD['startRules']['cash'] == 650 or cD['startRules']['cash'] == -1):
        errorStr += "Starting cash isn't 650\n"
    if not (cD['startRules']['maxLives'] == 1 or cD['startRules']['maxLives'] == -1):
        errorStr += "Max lives isn't 1\n"
    if not (cD['startRules']['round'] == 6 or cD['startRules']['round'] == -1):
        errorStr += "Doesn't start on round 6\n"
    if not (cD['startRules']['endRound'] >= 100 or cD['startRules']['endRound'] == -1):
        errorStr += "Ends before round 100\n"
    if cD['towers'][0]['max'] != 0:
        errorStr += "Selected hero can't be a tower\n"

    towerCount = 0
    towerMaxNot1 = False
    for tower in cD['towers']:
        if tower['max'] != 0:
            if tower['max'] != 1:
                towerMaxNot1 = True
            towerCount += 1

    if towerCount < 2 or towerCount > 4:
        errorStr += 'There are not 2 to 4 towers\n'
    if towerMaxNot1:
        errorStr += 'There is more than one of a tower\n'
    if cD['bloonModifiers']['speedMultiplier'] != 1:
        errorStr += "Bloon speed isn't 100%\n"
    if cD['bloonModifiers']['moabSpeedMultiplier'] != 1:
        errorStr += "MOAB speed isn't 100%\n"
    if cD['bloonModifiers']['healthMultipliers']['bloons'] != 1:
        errorStr += "Bloon health isn't 100%\n"
    if cD['bloonModifiers']['healthMultipliers']['moabs'] != 1:
        errorStr += "MOAB health isn't 100%\n"
    if version >= 22 and cD['bloonModifiers']['regrowRateMultiplier'] != 1:
        errorStr += "Regrow rate isn't 100%\n"
    if not cD['disableSelling']:
        errorStr += 'Selling enabled\n'
    if version >= 11:
        if cD['bloonModifiers']['allCamo']:
            errorStr += 'All camo enabled\n'
        if cD['bloonModifiers']['allRegen']:
            errorStr += 'All regrow enabled\n'

    if errorStr != '':
        raise Exception('```{0}```'.format(errorStr[:-1]))

#gets towers used from challenge data
def get_towers(challengeData):
    towers = []
    for tower in challengeData['towers']:
        if tower['max'] != 0:
            towers.append(tower['tower'])

    namesNK = hereosNK + towersNK
    names4tc = hereos4tc + towers4tc

    for i in range(len(towers)):
        for x in range(len(namesNK)):
            if towers[i] == namesNK[x]:
                towers[i] = names4tc[x]

    return tuple(towers)

#removes combos from remaining combos
def remove4tc(towers):
    cursor.execute('SELECT * FROM remaining_combos')
    remaining_combos = cursor.fetchall()
    
    matches = 0
    combosToRemove = []
    for combo in remaining_combos:
        if is_subset(towers, combo):
            combosToRemove.append(combo)
            matches += 1

    cursor.executemany('DELETE FROM remaining_combos WHERE tower1=? AND tower2=? AND tower3=? AND tower4=?', combosToRemove)

    if matches == 0:
        raise Exception('Already submitted')

    conn.commit()
    return matches

#updates leaderboard with new combos
def update_leaderboard(name, combos):
    cursor.execute('SELECT * FROM leaderboard WHERE name=?', (name,))
    row = cursor.fetchone()
    if row != None:
        cursor.execute('UPDATE leaderboard SET score=? WHERE name=?', (row[0] + combos, name))
    else:
        cursor.execute('INSERT INTO leaderboard VALUES (?, ?)', (combos, name))
    
    #sort leaderboard in descending order, couldn't get ORDER BY sql to work so the sorting is done in python instead
    cursor.execute('SELECT * FROM leaderboard')
    leaderboard = cursor.fetchall()
    leaderboard.sort(reverse=True, key=lambda score: score[0])
    cursor.execute('DELETE FROM leaderboard')
    cursor.executemany('INSERT INTO leaderboard VALUES (?, ?)', leaderboard)

    conn.commit()

#adds a new submission
def add_submission(code, towers, combos, name):
    sqlData = (code,) + towers
    for _ in range(4 - len(towers)):
        sqlData += (None,)
    sqlData += (combos, name)
    cursor.execute('INSERT INTO submissions VALUES (?, ?, ?, ?, ?, ?, ?)', sqlData)
    conn.commit()

#checks if challenge code provided is valid submission and adds it, if it is valid
def submit4tc(code, name=None, discordId=None):
    if name == None:
        try:
            name = get_name(discordId)
        except Exception as e:
            return str(e)

    code = code.upper()

    #parses out invalid codes that are not 7 chars long and/or contain non letters
    #this is for efficiency reasons since requesting is very slow
    if len(code) != 7 or not code.isalpha():
        return 'Invalid Code'

    try:
        challengeData = get_challenge_data(code)
        version = get_version(challengeData)
        valid_settings(challengeData, version)
        towers = get_towers(challengeData)
        combosRemoved = remove4tc(towers)
        update_leaderboard(name, combosRemoved)
        add_submission(code, towers, combosRemoved, name)
        return '```Submission:\nName: {0}\nCode: {1}\nTowers: {2}\nCombos removed: {3}```'.format(name, code, ', '.join(towers), combosRemoved)
    except Exception as e:
        return str(e)

#adds data about the webpage into the database to be used by the webpage cgi
def create_webpage(header, body):
    while True:
        key = ''
        for _ in range(4):
            key += chr(random.randrange(65, 90))
        cursor.execute('SELECT * FROM webpages WHERE key=?', (key,))
        if cursor.fetchone() == None:
            break

    sqlData = (key, int(time.time()), header, body)
    cursor.execute('INSERT INTO webpages VALUES (?, ?, ?, ?)', sqlData)
    conn.commit()

    return websiteUrl + key
