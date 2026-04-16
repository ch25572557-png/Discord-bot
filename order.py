import json

FILE = "orders.json"

def load():
    return json.load(open(FILE,"r"))

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


def update_status(order_id, status):

    db = load()

    if order_id in db["data"]:
        db["data"][order_id]["status"] = status
        save(db)


def cancel_order(order_id):

    db = load()

    if order_id not in db["data"]:
        return False

    return db["data"][order_id]
