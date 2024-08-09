import json, os

from util.log import logger
from resources.data.data import data
from resources.items.item import item

class store:

    async def get_all_store_config():
        with open('resources/store/store_config.json', 'r') as e:
            store_config = json.load(e)
            return store_config
        
    async def get_store_config_by_name(name):
        store_config = await store.get_all_store_config()
        if name not in store_config:
            logger.warn(f"{name} not found in store_config.json, returning default store")
            return 0
        else:
            return store_config[name]
        
    async def get_store_config_by_id(id):
        if not isinstance(id, int):
            id = int(id)
        store_config = await store.get_all_store_config()
        for i, u in store_config.items():
            if u["id"] == id:
                return u
        logger.warn(f"{id} not found in store_config.json, returning default store")
        return 0
    
    async def get_cost_item_info(cost):
        cost = str(cost)
        item_config = await item.get_item_config_from_id(cost)
        return item_config

    async def buy_store_item(user, store_id, item_id, amount):
        amount = int(amount)
        store_config = await store.get_store_config_by_id(store_id)
        item_id_str = str(item_id)
        for i, u in store_config["items"].items():
            if i == str(item_id):
                break
        else:
            return f'{store_config["name"]} does not have {item_id}!'
        cost_item_id = store_config["items"][item_id_str]["cost_id"]
        cost_item_config = await store.get_cost_item_info(cost_item_id)
        cost_amount = store_config["items"][item_id_str]["cost"]
        total_cost = amount * cost_amount
        buy_item_config = await item.get_item_config_from_id(item_id)

        if cost_item_config["type"] == "currency":
            currency_data = await data.get_currency(user)
            if total_cost > currency_data[str(cost_item_id)]:
                return f"You don't have enough {cost_item_config["name"]} to buy this!"
            rsp = await data.modify_user_inventory_by_config(user, buy_item_config, amount)
            await data.modify_user_currency(user, cost_item_id, -total_cost)
            if rsp == 1:
                return f"Bought x{amount} of {buy_item_config["name"]} for {total_cost} {cost_item_config["name"]}!"
            return "Something isnt right..."

        


