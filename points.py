import json

FILE = "points.json"

def load():
    try:
        return json.load(open(FILE,"r"))
    except:
        return {}

def save(data):
    json.dump(data, open(FILE,"w"), indent=4)


def add_points(uid, amt):
    data = load()
    uid = str(uid)

    data[uid] = data.get(uid, 0) + amt
    save(data)


def get_points(uid):
    return load().get(str(uid), 0)
