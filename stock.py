import json

FILE = "stock.json"

def load():
    return json.load(open(FILE,"r"))

def save(data):
    json.dump(data, open(FILE,"w"), indent=4)


def get_price(item):
    data = load()
    return data[item]["price"]


def reduce_stock(item, qty):
    data = load()

    if item not in data:
        return False

    if data[item]["stock"] < qty:
        return False

    data[item]["stock"] -= qty
    save(data)
    return True
