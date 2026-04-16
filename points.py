import json

FILE = "points.json"

def load():
    try:
        return json.load(open(FILE,"r"))
    except:
        return {}

def save(data):
    json.dump(data, open(FILE,"w"), indent=4)


def add_points(user_id, amt=1):
    data = load()
    uid = str(user_id)

    data[uid] = data.get(uid,0) + amt
    save(data)


def get_points(user_id):
    return load().get(str(user_id),0)


def remove_points(user_id, amt):
    data = load()
    uid = str(user_id)

    data[uid] = max(0, data.get(uid,0)-amt)
    save(data)
