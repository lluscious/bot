import os
import json

from resources.items.item import item
from util.log import logger
from resources.user.user_info_config import user_info_config

class data:

    # Example start_list
    # {
    #   1: 100 - 100 starter mora
    # }
    async def init_gacha(user):
        from resources.gacha.gacha import gacha
        banners = await gacha.get_all_banner_config()
        data = {}
        for i, e in banners.items():
            struct = {
                "pity_5": 0,
                "pity_4": 0,
                "total_pulls": 0,
                "is_rate_up": False,
            }
            if e["is_release"] == True:
                if e["type"] == "GACHA_WEAPON":
                    struct["chosen_path_id"] = 0
            data[i] = struct
        with open(f"data/{str(user.id)}/gacha.json", 'w') as f:
            json.dump(data, f, indent=4)
    
    async def init_new(user, start_list):
        id = str(user.id)
        os.mkdir(f'data/{id}')
        with open("resources/data/user_info.json", 'r') as r:
            t = json.load(r)
            t["name"] = user.name
            items = await item.get_all_item_config()
            if 4 in start_list:
                t["lv"]["level"] = start_list[4]
            for u, i in items.items():
                if i["type"] == "currency":
                    id_string = str(i["id"])
                    if i["id"] in start_list:
                        t["currency"][id_string] = start_list[i["id"]]
                    else:
                        t["currency"][id_string] = 0
            with open(f"data/{id}/user_info.json", 'w') as e:
                json.dump(t, e, indent=4)
        ignore_files = ["user_info.json", "data.py", "gacha.json"]
        await data.init_gacha(user)
        for i in os.listdir('resources/data'):
            if i not in ignore_files:
                with open(f'resources/data/{i}', "r") as file:
                    r = json.load(file)
                    with open(f"data/{id}/{i}", 'w') as out:
                        json.dump(r, out, indent=4)
        return t
    
    async def get_user_info(user):
        id = str(user.id)
        if not os.path.exists(f"data/{id}"):
            await data.init_new(user, {})
        with open(f"data/{id}/user_info.json", 'r') as r:
            return json.load(r)
    
    async def get_inventory(user):
        id = str(user.id)
        if not os.path.exists(f"data/{id}"):
            await data.init_new(user, {})
        with open(f"data/{id}/inventory.json", 'r') as r:
            return json.load(r)
        
    async def get_characters(user):
        id = str(user.id)
        if not os.path.exists(f"data/{id}"):
            await data.init_new(user, {})
        with open(f"data/{id}/characters.json", 'r') as r:
            return json.load(r)
        
    async def get_currency(user):
        user_info = await data.get_user_info(user)
        return user_info["currency"]
    
    async def get_gacha_info(user):
        id = str(user.id)
        if not os.path.exists(f"data/{id}"):
            await data.init_new(user, {})
        with open(f"data/{id}/gacha.json", 'r') as r:
            return json.load(r)
    
    async def add_gacha_data(user, new_data, banner_id):
        id = str(user.id)
        gacha_data = await data.get_gacha_info(user)
        gacha_data[str(banner_id)] = new_data
        with open(f"data/{id}/gacha.json", 'w') as r:
            json.dump(gacha_data, r, indent=4)
            return gacha_data
        
    async def get_gacha_banner_data(user, banner_id):
        id = str(user.id)
        gacha = await data.get_gacha_info(user)
        if not banner_id in gacha:
            gacha = await data.add_gacha_data(user, {"id": banner_id, "pity_5": 0, "pity_4": 0, "total_pulls": 0, "is_rate_up": False})
        banner_data = gacha[banner_id]
        return banner_data
    
    async def edit_user_info(user, prop, new_value):
        id = str(user.id)
        allowed_props = ["signature", "image_url", "thumbnail_url", "color"]
        if not os.path.exists(f"data/{id}"):
            await data.init_new(user, {})
        user_info = await data.get_user_info(user)
        if prop in user_info and prop in allowed_props:
            user_info[prop] = new_value
            with open(f"data/{id}/user_info.json", 'w') as r:
                json.dump(user_info, r, indent=4)
            return 1
        else:
            logger.warn(f"{prop} was not allowed for edit or was not in user_info!")
            return 0
    
    async def modify_user_currency(user, curr, amount):
        user_info = await data.get_user_info(user)
        id = str(user.id)
        if str(curr) in user_info["currency"]:
            user_info["currency"][str(curr)] += amount
            with open(f"data/{id}/user_info.json", 'w') as r:
                json.dump(user_info, r, indent=4)
            return user_info["currency"][str(curr)] 
        else:
            logger.warn(f"{curr} doesn't exist in user data!")

    async def modify_user_inventory_by_config(user, item_config, amount):
        inventory_data = await data.get_inventory(user)
        item_id = str(item_config["id"])
        rarity = item_config["rarity"]
        category = item_config["category"]
        inv_place = inventory_data[category][rarity]
        if item_id in inv_place:
            inv_place[item_id] += amount
            if inv_place[item_id] <= 0:
                del inv_place[item_id]
        else:
            if amount > 0:
                inv_place[item_id] = amount
        with open(f"data/{str(user.id)}/inventory.json", 'w') as r:
            json.dump(inventory_data, r, indent=4)
        
        return 1

    async def add_user_exp(user, exp):
        user_info = await data.get_user_info(user)
        exp = int(exp)
        cur_level = user_info["lv"]["level"]
        cur_exp = user_info["lv"]["exp"]
        
        while exp > 0:
            level_config = await user_info_config.get_level_config(cur_level)
            needed_exp = level_config - cur_exp
            if exp >= needed_exp:
                exp -= needed_exp
                cur_level += 1
                cur_exp = 0
                ranking_config = await user_info_config.get_ranking_config_from_level(cur_level)
                user_info["rank"] = ranking_config["id"]
            else:
                cur_exp += exp
                exp = 0
            user_info["lv"]["level"] = cur_level
            user_info["lv"]["exp"] = cur_exp

        with open(f"data/{str(user.id)}/user_info.json", 'w') as f:
            json.dump(user_info, f, indent=4)
        return cur_level
    
    async def get_owned_item_amount(user, item_config):
        inv = await data.get_inventory(user)
        id = str(item_config["id"])
        rarity = item_config["rarity"]
        category = item_config["category"]
        if id in inv[category][rarity]:
            return inv[category][rarity][id]
        else:
            return 0
    
    async def add_item(user, id, amount):
        item_config = await item.get_item_config_from_id(id)
        if item_config != 0:
            if item_config["type"] == "character":
                char_data = await data.get_characters(user)

                






        