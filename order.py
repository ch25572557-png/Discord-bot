import json

FILE = "orders.json"

def load():
    try:
        return json.load(open(FILE,"r"))
    except:
        return {"counter":0,"data":{}}

def save(data):
    json.dump(data, open(FILE,"w"), indent=4)


def create_order(user_id, item, qty, total):

    db = load()

    db["counter"] += 1
    oid = str(db["counter"])

    db["data"][oid] = {
        "user_id": user_id,
        "item": item,
        "qty": qty,
        "total": total,
        "status": "📥 รับออเดอร์"
    }

    save(db)
    return oid
