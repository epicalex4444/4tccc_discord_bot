import json
import sqlite3

conn = sqlite3.connect('4tccc_data.db')
cursor = conn.cursor()

cursor.execute('SELECT name, code, tower1, tower2, tower3, tower4 FROM submissions')
oldSubmissions = cursor.fetchall()

submissions = []
leaderboard = []
remainingCombos = []

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

#removes combos from remaining combos
def remove4tc(towers):
    global remainingCombos
    matches = 0
    temp = []
    for combo in remainingCombos:
        if is_subset(towers, combo):
            matches += 1
        else:
            temp.append(combo)
    remainingCombos = temp
    return matches

#updates leaderboard with new combos
def update_leaderboard(name, combos):
    global leaderboard
    nameNotFound = True
    for i, score in enumerate(leaderboard):
        if score[1] == name:
            leaderboard[i] = (score[0] + combos, score[1])
            nameNotFound = False
    if nameNotFound:
        leaderboard.append((combos, name))

#adds a new submission
def add_submission(code, towers, combos, name):
    global submissions
    submission = (code,) + towers
    for _ in range(4 - len(towers)):
        submission += (None,)
    submission += (combos, name)
    submissions.append(submission)

#returns whether combo is mathematically possible meaning whether it can damage all bloons
#by the time they come out, even if the method to do so obviosely won't work in practise
def mathematically_possible(towers):
    canBeat6 = False
    canBeat24 = False
    canBeat45 = False

    for tower in towers:
        if (not canBeat6) and tower in ['Quincy', 'Ezili', 'Sauda', 'Dart', 'Boomer', 'Bomb', 'Tack', 'Ice', 'Sniper', 'Sub', 'Bucc', 'Wizard', 'Ninja', 'Alch', 'Druid', 'Engineer']:
            canBeat6 = True
        if (not canBeat24) and tower in ['Quincy', 'Gwen', 'Obyn', 'Ezili', 'Etienne', 'Sauda', 'Psi', 'Dart', 'Sniper', 'Sub', 'Bucc', 'Ace', 'Heli', 'Mortar', 'Dartling', 'Wizard', 'Ninja', 'Spac', 'Engineer']:
            canBeat24 = True
        if (not canBeat45) and tower in ['Quincy', 'Obyn', 'Church', 'Brickell', 'Etienne', 'Sauda', 'Dart', 'Ice', 'Glue', 'Sniper', 'Sub', 'Bucc', 'Ace', 'Heli', 'Mortar', 'Dartling', 'Wizard', 'Super', 'Ninja', 'Spac', 'Village', 'Engineer']:
            canBeat45 = True

    #ice can start but there is no way for it to reach village on it's own because of whites
    #yet ice + striker and ice + brickell are cheap enough to be able to afford village
    if (not canBeat24) and 'Village' in towers:
        if 'Boomer' in towers or 'Tack' in towers or 'Druid' in towers or 'Alch' in towers or 'Bomb' in towers:
            canBeat24 = True
        elif 'Ice' in towers and ('Striker' in towers or 'Brickell' in towers):
            canBeat24 = True

    return canBeat6 and canBeat24 and canBeat45

#generates all the 4tc's and removes mathematically impossible ones 
def reset_remaining_combos():
    global remainingCombos

    file = open('towerNames.json', 'r')
    towerNames = json.load(file)
    file.close()

    heroes4tc = []
    towers4tc = []

    for _, hero in towerNames['heroes'].items():
        heroes4tc.append(hero['4tc_name'])

    for _, tower in towerNames['towers'].items():
        towers4tc.append(tower['4tc_name'])

    heroAmount = len(heroes4tc)
    towerAmount = len(towers4tc)
    
    pos1 = 0
    pos2 = 1
    pos3 = 2
    pos4 = 3

    #generates all the non hero combos
    while True:
        remainingCombos.append((towers4tc[pos1], towers4tc[pos2], towers4tc[pos3], towers4tc[pos4]))
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
        remainingCombos.append((heroes4tc[pos1], towers4tc[pos2], towers4tc[pos3], towers4tc[pos4]))
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
    
    remainingCombos = [combo for combo in remainingCombos if mathematically_possible(combo)]

#clears out old data
def reset_database():
    cursor.execute('CREATE TABLE IF NOT EXISTS remaining_combos (tower1 TEXT, tower2 TEXT, tower3 TEXT, tower4 TEXT)')
    cursor.execute('CREATE TABLE IF NOT EXISTS submissions (code TEXT, tower1 TEXT, tower2 TEXT, tower3 TEXT, tower4 TEXT, combos INTEGER, name TEXT)')
    cursor.execute('CREATE TABLE IF NOT EXISTS leaderboard (score INT, name TEXT)')
    cursor.execute('DELETE FROM remaining_combos')
    cursor.execute('DELETE FROM submissions')
    cursor.execute('DELETE FROM leaderboard')

reset_remaining_combos()
reset_database()

#loops over all the old submissions updating the leaderboard, remainingCombos and submissions
for submission in oldSubmissions:
    towers = [submission[2], submission[3], submission[4], submission[5]]
    towers = tuple([tower for tower in towers if tower is not None])
    combosRemoved = remove4tc(towers)
    update_leaderboard(submission[0], combosRemoved)
    add_submission(submission[1], towers, combosRemoved, submission[0])

#sort leaderboard
leaderboard.sort(reverse=True, key=lambda score: score[0])

#add into database
cursor.executemany('INSERT INTO remaining_combos values (?, ?, ?, ?)', remainingCombos)
cursor.executemany('INSERT INTO submissions values (?, ?, ?, ?, ?, ?, ?)', submissions)
cursor.executemany('INSERT INTO leaderboard values (?, ?)', leaderboard)

conn.commit()
conn.close()
