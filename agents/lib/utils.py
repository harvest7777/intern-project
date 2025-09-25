import json
def getPrettyDump(object):
    return json.dumps(object.dict(), indent=2)