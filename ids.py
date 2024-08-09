import json
with open("resources/items/item_config.json", 'r') as f:
    data = json.load(f)
    for s, i in data.items():
        id = i["id"]
        name = i["name"]
        type = i["type"]
        with open("ids.txt", "a") as r:
            r.write(f"{id} - {name} ({type})\n")