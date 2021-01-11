import json
import requests
import base64
import zlib
from simplejson.errors import JSONDecodeError

aliasAddress = './aliases.json'
lbAddress = './leaderboard.json'
remainingAddress = './remaining_combos.json'
submittedAddress = './submitted_combos.json'
towerAliasAddress = './tower_aliases.json'

hastebinUrl = 'https://hastebin.com/'
challengeDataUrl = 'https://static-api.nkstatic.com/appdocs/11/es/challenges/'

hereos4tc = ['Quincy', 'Gwen', 'Striker', 'Obyn', 'Church', 'Ben', 'Ezili', 'Pat', 'Adora', 'Brickell', 'Etienne']
towers4tc = ['Dart', 'Boomer', 'Bomb', 'Tack', 'Ice', 'Glue', 'Sniper', 'Sub', 'Bucc', 'Ace', 'Heli', 'Mortar', 'Dartling', 'Wizard', 'Super', 'Ninja', 'Alch', 'Druid', 'Spac', 'Village', 'Engi']
hereosNK = ['Quincy', 'Gwendolin', 'StrikerJones', 'ObynGreenfoot', 'CaptainChurchill', 'Benjamin', 'Ezili', 'PatFusty', 'Adora', 'AdmiralBrickell', 'Etienne']
towersNK = ['DartMonkey', 'BoomerangMonkey', 'BombShooter', 'TackShooter', 'IceMonkey', 'GlueGunner', 'SniperMonkey', 'MonkeySub', 'MonkeyBuccaneer', 'MonkeyAce', 'HeliPilot', 'MortarMonkey', 'DartlingGunner', 'WizardMonkey', 'SuperMonkey', 'NinjaMonkey', 'Alchemist', 'Druid', 'SpikeFactory', 'MonkeyVillage', 'EngineerMonkey']

file = open(towerAliasAddress)
towerAliases = json.load(file) #used for find4tc function so people can input many different names
file.close()

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
    for i in range(len(towers)):
        towers[i] = space_fill(towers[i], 8)
    return '|'.join(towers)

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
        return 'Invalid Towers: {0}'.format(', '.join(invalidTowers))

    file = open(remainingAddress)
    remaningCombos = json.load(file)
    file.close()

    displayStr = ''
    matches = 0
    for combo in remaningCombos:
        if is_subset(towers, combo):
            displayStr += tower_print(combo) + '\n'
            matches += 1

    if matches == 1:
        return '```1 combo found\n{0}```'.format(displayStr[:-1])
    else:
        return '```{0} combos found\n{1}'.format(matches, displayStr)[:-1] + '```'

#returns leaderboard formatted for easy reading
#if name is provided returns score, if amount is provided it returns a shortened version of the leaderboard
def get_leaderboard(name=None, amount=None):
    file = open(lbAddress)
    leaderboard = json.load(file)
    file.close()

    if name != None:
        for score in leaderboard:
            if score[0] == name:
                return "{0}'s score is {1}".format(name, score[1])
        return "{0} hasn't submitted yet".format(name)

    displayStr = ''
    if amount == None or int(amount) >= len(leaderboard):
        for score in leaderboard:
            displayStr += '{0}: {1}\n'.format(space_fill(str(score[1]), 4, False), score[0])
    else:
        amount = int(amount)
        for score in leaderboard:
            if amount == 0:
                break
            displayStr += '{0}: {1}\n'.format(space_fill(str(score[1]), 4, False), score[0])
            amount -= 1

    return '```{0}```'.format(displayStr[:-1])

#returns all the submission formatted for easy reading, if a name is provided if returns ony submissions by that person
#if towers is provided it returns who completed the combo, must have 4 towers
def get_submissions(name=None):
    file = open(submittedAddress)
    submittedCombos = json.load(file)
    file.close()

    displayStr = ''
    if name == None:
        for submission in submittedCombos:
            displayStr += tower_print(submission[2]) + '\n'
    else:
        for submission in submittedCombos:
            if submission[0] == name:
                displayStr += tower_print(submission[2]) + '\n'

        if displayStr == '':
            return "{0} doesn't exist".format(name)

        displayStr = "{0}'s submissions:\n{1}".format(name, displayStr)

    return '```' + displayStr[:-1] + '```'

#change name in submissions and leaderboard
def change_name(old, new):
    file = open(lbAddress)
    leaderboard = json.load(file)
    file.close()

    submittedNew = False
    submittedOld = False

    for score in leaderboard:
        if score[0] == new:
            submittedNew = True
        if score[0] == old:
            submittedOld = True

    if submittedNew and submittedOld:
        raise Exception('cannot change name since the name you are changing to exists and you have submitted under your current alias, this is to prevent combo theft')

    for score in leaderboard:
        if score[0] == old:
            score[0] = new

    file = open(lbAddress, 'w')
    json.dump(leaderboard, file, indent=4)
    file.close()

    file = open(submittedAddress)
    submittedCombos = json.load(file)
    file.close()

    for submission in submittedCombos:
        if submission[0] == old:
            submission[0] = new

    file = open(submittedAddress, 'w')
    json.dump(submittedCombos, file, indent=4)
    file.close()

#adds new alias or changes an existing alias
def set_alias(discordId, name):
    file = open(aliasAddress)
    aliases = json.load(file)
    file.close()

    alias = aliases.get(discordId, None)
    if alias == None:
        displayStr = '{0} has been added as your alias'.format(name)
    else:
        if alias == name:
            return 'Name already added as your alias'
        try:
            change_name(alias, name)
        except Exception as e:
            return str(e)
        displayStr = '{0} changed to {1}'.format(alias, name)

    aliases[discordId] = name

    file = open(aliasAddress, 'w')
    json.dump(aliases, file, indent=4)
    file.close()
    return displayStr

#returns name from discord id
def get_alias(discordId):
    discordId = str(discordId)
    file = open(aliasAddress)
    aliases = json.load(file)
    file.close()
    name = aliases.get(discordId, None)
    if name == None:
        raise Exception('Name not provided and you have no alias set')
    else:
        return name

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

    return towers

#removes combos from remaining combos
def remove4tc(towers):
    file = open(remainingAddress)
    remainingCombos = json.load(file)
    file.close()

    matches = 0
    for i in range(len(remainingCombos) -1, 0, -1):
        if is_subset(towers, remainingCombos[i]):
            del remainingCombos[i]
            matches += 1

    if matches == 0:
        file.close()
        raise Exception('Already submitted')

    file = open(remainingAddress, 'w')
    json.dump(remainingCombos, file, indent=4)
    file.close()
    return matches

#updates leaderboard with new combos
def update_leaderboard(name, combos):
    file = open(lbAddress)
    leaderboard = json.load(file)
    file.close()

    nameNotExist = True
    for score in leaderboard:
        if score[0] == name:
            score[1] += combos
            nameNotExist = False
            break

    if nameNotExist:
        leaderboard.append([name, combos])

    #sort leaderboard in descending order of combos completed
    leaderboard.sort(reverse=True, key=lambda score: score[1])

    file = open(lbAddress, 'w')
    json.dump(leaderboard, file, indent=4)
    file.close()

#adds a new submission
def add_submission(name, code, towers):
    file = open(submittedAddress)
    submittedCombos = json.load(file)
    file.close()
    submittedCombos.append([name, code, towers])
    file = open(submittedAddress, 'w')
    json.dump(submittedCombos, file, indent=4)
    file.close

#checks if challenge code provided is valid submission and adds it, if it is valid
def submit4tc(code, name=None, discordId=None):
    if name == None:
        try:
            name = get_alias(discordId)
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
        add_submission(name, code, towers)
        return '```Submission:\nName: {0}\nCode: {1}\nTowers: {2}\nCombos removed: {3}```'.format(name, code, ', '.join(towers), combosRemoved)
    except Exception as e:
        return str(e)

#creates a hastebin page conataining message and returns the url to it
def create_hastebin_link(message):
    try:
        response = requests.post(hastebinUrl + 'documents', message.encode('utf-8'), timeout=10)
        response.raise_for_status()
        return hastebinUrl + response.json()['key']
    except (requests.exceptions.RequestException, JSONDecodeError, KeyError):
        return "Couldn't create hastebin link, I am working on fixing this issue"
