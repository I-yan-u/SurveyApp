import json
import os

path = f'{os.getcwd()}/models/'
filename = f'{path}id.json' 

with open(filename, 'r') as f:
    index = json.load(f)


def getUID():
    intId = index.get('UID') + 1
    strId = str(intId).zfill(6)
    id = 'UID{}'.format(strId)

    index['UID'] = intId
    with open(filename, 'w') as wfile:
        json.dump(index, wfile, indent=2)
    return id


def getSID():
    intId = index.get('SID') + 1
    strId = str(intId).zfill(6)
    id = 'SID{}'.format(strId)

    index['SID'] = intId
    with open(filename, 'w') as wfile:
        json.dump(index, wfile, indent=2)
    return id


def getRID():
    intId = index.get('RID') + 1
    strId = str(intId).zfill(6)
    id = 'RID{}'.format(strId)

    index['RID'] = intId
    with open(filename, 'w') as wfile:
        json.dump(index, wfile, indent=2)
    return id
