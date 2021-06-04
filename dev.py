import json
import requests
import base64
import zlib
import sqlite3
import os

challengeDataUrl = 'https://static-api.nkstatic.com/appdocs/11/es/challenges/'

hereos4tc = ['Quincy', 'Gwen', 'Striker', 'Obyn', 'Church', 'Ben', 'Ezili', 'Pat', 'Adora', 'Brickell', 'Etienne', 'Sauda', 'Psi']
towers4tc = ['Dart', 'Boomer', 'Bomb', 'Tack', 'Ice', 'Glue', 'Sniper', 'Sub', 'Bucc', 'Ace', 'Heli', 'Mortar', 'Dartling', 'Wizard', 'Super', 'Ninja', 'Alch', 'Druid', 'Spac', 'Village', 'Engineer']
hereosNK = ['Quincy', 'Gwendolin', 'StrikerJones', 'ObynGreenfoot', 'CaptainChurchill', 'Benjamin', 'Ezili', 'PatFusty', 'Adora', 'AdmiralBrickell', 'Etienne', 'Sauda', 'Psi']
towersNK = ['DartMonkey', 'BoomerangMonkey', 'BombShooter', 'TackShooter', 'IceMonkey', 'GlueGunner', 'SniperMonkey', 'MonkeySub', 'MonkeyBuccaneer', 'MonkeyAce', 'HeliPilot', 'MortarMonkey', 'DartlingGunner', 'WizardMonkey', 'SuperMonkey', 'NinjaMonkey', 'Alchemist', 'Druid', 'SpikeFactory', 'MonkeyVillage', 'EngineerMonkey']

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
    except requests.exceptions.RequestException:
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

    return matches

#updates leaderboard with new combos
def update_leaderboard(name, combos):
    cursor.execute('SELECT * FROM leaderboard WHERE name=?', (name,))
    row = cursor.fetchone()
    if row != None:
        cursor.execute('UPDATE leaderboard SET score=? WHERE name=?', (row[0] + combos, name))
    else:
        cursor.execute('INSERT INTO leaderboard VALUES (?, ?)', (combos, name))

#adds a new submission
def add_submission(code, towers, combos, name):
    for _ in range(4 - len(towers)):
        towers += (None,)

    sqlData = (code,) + towers + (combos, name)
    cursor.execute('INSERT INTO submissions VALUES (?, ?, ?, ?, ?, ?, ?)', sqlData)

#checks if challenge code provided is valid submission and adds it, if it is valid
def submit4tc(code, name):
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

#generates all unique combinations of 4 towers, in the standard 4tc order
def generate_all_4tcs():
    heroAmount = len(hereos4tc)
    towerAmount = len(towers4tc)
    
    pos1 = 0
    pos2 = 1
    pos3 = 2
    pos4 = 3

    #generates all the non hero combos
    while True:
        cursor.execute('INSERT INTO remaining_combos VALUES (?, ?, ?, ?)', (towers4tc[pos1], towers4tc[pos2], towers4tc[pos3], towers4tc[pos4]))
        if pos4 != towerAmount - 1:
            pos4 += 1
        elif pos3 != towerAmount - 2:
            pos3 += 1
            pos4 = pos3 + 1
        elif pos2 != towerAmount - 3:
            pos2 += 1
            pos3 = pos2 + 1
            pos4 = pos3 + 1
        elif pos1 != towerAmount - 4:
            pos1 += 1
            pos2 = pos1 + 1
            pos3 = pos2 + 1
            pos4 = pos3 + 1
        else:
            break

    pos1 = 0
    pos2 = 0
    pos3 = 1
    pos4 = 2

    #generates all the hero combos
    while True:
        cursor.execute('INSERT INTO remaining_combos VALUES (?, ?, ?, ?)', (hereos4tc[pos1], towers4tc[pos2], towers4tc[pos3], towers4tc[pos4]))
        if pos4 != towerAmount - 1:
            pos4 += 1
        elif pos3 != towerAmount - 2:
            pos3 += 1
            pos4 = pos3 + 1
        elif pos2 != towerAmount - 3:
            pos2 += 1
            pos3 = pos2 + 1
            pos4 = pos3 + 1
        elif pos1 != heroAmount - 1:
            pos1 += 1
            pos2 = 0
            pos3 = 1
            pos4 = 2
        else:
            break

#returns whether the towers are mathematically possible to be a 4tc
#some other starts are also removed because they are very obviously impossible
def mathematically_possible(towers):
    canBeat6 = False
    canBeat24 = False

    for tower in towers:
        if tower in ['Quincy', 'Ezili', 'Sauda', 'Dart', 'Boomer', 'Bomb', 'Tack', 'Ice', 'Sniper', 'Sub', 'Bucc', 'Wizard', 'Ninja', 'Alch', 'Druid', 'Engineer']:
            canBeat6 = True

    for tower in towers:
        if tower in ['Quincy', 'Gwen', 'Obyn', 'Etienne', 'Ezili', 'Sauda', 'Dart', 'Sniper', 'Sub', 'Bucc', 'Ace', 'Heli', 'Mortar', 'Dartling', 'Wizard', 'Ninja', 'Spac', 'Engineer', 'Psi']:
            canBeat24 = True

    #Village is expensive so bomb, ice and alch -> village doesn't work although some variants of those starts are not mathatically impossible
    if 'Village' in towers:
        if 'Boomer' in towers or 'Tack' in towers or 'Druid' in towers or 'Alch' in towers or 'Bomb' in towers:
            canBeat24 = True
        elif 'Ice' in towers and ('Striker' in towers or 'Brickell' in towers):
            canBeat24 = True

    #all 4tc combos can mathematically beat all the other threats such as 28 and 25
    return canBeat6 and canBeat24

#removes mathematically impossible combos from the remainingCombos
def remove_impossible_combos():
    cursor.execute('SELECT * FROM remaining_combos')
    remainingCombos = cursor.fetchall()

    for combo in remainingCombos:
        if not mathematically_possible(combo):
            cursor.execute('DELETE FROM remaining_combos WHERE tower1=? AND tower2=? AND tower3=? AND tower4=?', combo)

def sort_leaderboard():
    cursor.execute('SELECT * FROM leaderboard')
    leaderboard = cursor.fetchall()
    leaderboard.sort(reverse=True, key=lambda score: score[0])
    cursor.execute('DELETE FROM leaderboard')
    cursor.executemany('INSERT INTO leaderboard VALUES (?, ?)', leaderboard)

def init_database():
    cursor.execute('CREATE TABLE IF NOT EXISTS remaining_combos (tower1 TEXT, tower2 TEXT, tower3 TEXT, tower4 TEXT)')
    cursor.execute('CREATE TABLE IF NOT EXISTS submissions (code TEXT, tower1 TEXT, tower2 TEXT, tower3 TEXT, tower4 TEXT, combos INTEGER, name TEXT)')
    cursor.execute('CREATE TABLE IF NOT EXISTS leaderboard (score INT, name TEXT)')
    cursor.execute('DELETE FROM remaining_combos')
    cursor.execute('DELETE FROM submissions')
    cursor.execute('DELETE FROM leaderboard')

#creates 4tccc_data.db from submitted_combos.json, sql database contains leaderboard, remaining_combos and submissions
#progress metre doesn't work with some ide's
def clean_submissions():
    print('Verifying Submissions')

    if os.path.exists('invalid_combos.json'):
        os.remove('invalid_combos.json')

    cursor.execute('SELECT name, code FROM submissions')
    submissions = cursor.fetchall()

    init_database()
    generate_all_4tcs()

    invalidCombos = []
    totalCombos = combosRemaining = len(submissions)
    for combo in submissions:
        combosRemaining -= 1
        print('\rCombos Remaining: {0}/{1} '.format(combosRemaining, totalCombos), end='') #progress metre
        response = submit4tc(combo[1], combo[0])
        if not response.startswith('```Submission:'): #weird i know, didn't make the submit4tc function with this in mind
            invalidCombos.append([combo[0], combo[1], response])

    print() #adds newline since progress metre doesn't end with a newline

    if len(invalidCombos) != 0:
        file = open('invalid_combos.json', 'x')
        json.dump(invalidCombos, file, indent=4)
        file.close()

    sort_leaderboard()
    remove_impossible_combos()
    conn.commit()

clean_submissions()

conn.close()
