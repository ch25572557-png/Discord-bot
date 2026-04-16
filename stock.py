import json

FILE = "stock.json"

def load():
    try:
        return json.load(open(FILE,"r"))
    except:
        return {}

def save(data):
    json.dump(data, open(FILE,"w"), indent=4)


def get_price(item):
    return load().get(item, {}).get("price", 0)


def add_stock(item, qty):
    data = load()
    data.setdefault(item, {"stock": 0, "price": 0})
    data[item]["stock"] += qty
    save(data)


def reduce_stock(item, qty):
    data = load()

    if item not in data or data[item]["stock"] < qty:
        return False

    data[item]["stock"] -= qty
    save(data)
    return True
