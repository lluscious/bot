import json

from util.log import logger

class item:
    async def get_all_item_config():
        with open('resources/items/item_config.json', 'r') as r:
            return json.load(r)
        
    async def get_item_config_from_id(id):
        id = str(id)
        search = f"item_{id}"
        items = await item.get_all_item_config()
        if search not in items:
            logger.warn(f"{search} not in item_config.json")
            return items["item_default"]
        r = items[search]
        return r
