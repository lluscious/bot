import json
import random
import discord
from resources.items.item import item
from resources.data.data import data
from util.log import logger

class gacha:
    
    async def get_all_banner_config():
        with open("resources/gacha/banner_config.json", 'r') as f:
            return json.load(f)

    async def get_all_pool_config():
        with open("resources/gacha/pool_config.json", 'r') as f:
            return json.load(f)
        
    async def get_all_gacha_config():
        with open("resources/gacha/gacha_config.json", 'r') as f:
            return json.load(f)
        
    async def get_banner(id):
        id = str(id)
        banner_config = await gacha.get_all_banner_config()
        if (id in banner_config):
            return banner_config[id]
        else:
            logger.log(f"{id} is not in banner config")
            return 0
        
    async def get_pool(id):
        pool_config = await gacha.get_all_pool_config()
        if (id in pool_config):
            return pool_config[id]
        else:
            logger.log(f"{id} is not in pool config")
            return 0
        
    async def get_gacha(id):
        gacha_config = await gacha.get_all_gacha_config()
        if (id in gacha_config):
            return gacha_config[id]
        else:
            logger.log(f"{id} is not in gacha config")
            return 0
        
    async def wish(banner_id, user):
        user_id = str(user.id)
        user_gacha = await data.get_gacha_banner_data(user, banner_id)
        banner = await gacha.get_banner(banner_id)
        pool_config = await gacha.get_pool(banner["pool_id"])
        gacha_config = await gacha.get_gacha(banner["gacha_id"])
        rarity4_pity = user_gacha["pity_4"]
        rarity5_pity = user_gacha["pity_5"]
        rateup = user_gacha["is_rate_up"]
        soft_4 = gacha_config["rarity_4"]["soft"]
        hard_4 = gacha_config["rarity_4"]["max"]

        soft_5 = gacha_config["rarity_5"]["soft"]
        hard_5 = gacha_config["rarity_5"]["max"]

        chance_4 = 5.1
        chance_5 = 0.6

        if rarity4_pity >= soft_4:
            for i in range(rarity4_pity - soft_4):
                chance_4 += gacha_config["rarity_4"]["add_percent"]+1/100
        else:
            for i in range(soft_4 - rarity4_pity):
                chance_4 += gacha_config["rarity_4"]["buildup_add"]+1/100

        if rarity5_pity >= soft_5:
            for i in range(rarity5_pity - soft_5):
                chance_5 += gacha_config["rarity_5"]["add_percent"]+1/100
        else:
            for i in range(soft_5 - rarity5_pity):
                chance_5 += gacha_config["rarity_5"]["buildup_add"]+1/100

        if rarity4_pity >= hard_4:
            chance_4 = 101
        if rarity5_pity >= hard_5:
            chance_5 = 101

        recv_pity = -1
        chance = random.random() * 100
        drop = "?"
        rarity = 3
        print(chance_4 , chance_5, chance)
        if chance_5 > chance: # omg 5*
            recv_pity = user_gacha["pity_5"]
            user_gacha["pity_5"] = 0
            user_gacha["pity_4"] += 1
            if random.randrange(1, 3) == 1 or user_gacha["is_rate_up"] == True: # omg 5050 winner (or rateup)
                drop = pool_config["featured_5"]
                rarity = 5
                user_gacha["is_rate_up"] = False
            else:
                user_gacha["is_rate_up"] = True
                drop = random.choice(pool_config["off_5"]) # fucking loser
                rarity = 5
        elif chance_4 > chance:
            user_gacha["pity_5"] += 1
            user_gacha["pity_4"] = 0
            if random.randrange(1, 3) == 1: # omg featured 4 star winner
                drop = random.choice(pool_config["featured_4"])
                rarity = 4
            else:
                drop = random.choice(pool_config["off_5"])
                rarity = 4
        else:
            user_gacha["pity_4"] += 1
            user_gacha["pity_5"] += 1
            drop = random.choice(pool_config["3_list"])
            rarity = 3
        await data.add_gacha_data(user, user_gacha, banner_id)
        return drop, str(rarity), recv_pity # for the dictionary...
    
    async def process_wish(user, banner_id, amount):
        from resources.items.item import item
        banner_config = await gacha.get_banner(banner_id)
        cost_item = await item.get_item_config_from_id(banner_config["cost_item_id"])
        owned_amount = await data.get_owned_item_amount(user, cost_item)
        print(owned_amount, amount)
        if owned_amount < amount:
            return "poor"
        amount = int(amount)
        i = 0
        results = {
            "5": [],
            "4": [],
            "3": []
        }
        rarity5_pity_list = []
        # {"40003": 58}
        while i < amount:
            i += 1
            await data.modify_user_inventory_by_config(user, cost_item, -i)
            drop, rarity, pity = await gacha.wish(banner_id, user)
            results[rarity].append(drop)
            if rarity == "5":
                rarity5_pity_list.append({drop: pity})
        return results, rarity5_pity_list
    
    async def make_gacha_banner_embed(config_list):
        embed = discord.Embed(title=f"{config_list["name"]} ({config_list['id']})", color=discord.Color.from_str(config_list["color"]))
        icon_path = discord.File(config_list["icon_path"], filename="icon.png")
        image_path = discord.File(config_list["image_path"], filename="image.png")
        embed.set_thumbnail(url="attachment://icon.png")
        embed.set_image(url="attachment://image.png")
        pool_config = await gacha.get_pool(config_list["pool_id"])
        featured_id = pool_config["featured_5"]
        feature_char = await item.get_item_config_from_id(str(featured_id))
        embed.add_field(name="Featured Character", value=feature_char["name"])
        featured_list = []
        for i in pool_config["featured_4"]:
            item_config = await item.get_item_config_from_id(i)
            featured_list.append(item_config["name"])
        embed.add_field(name="Featured 4* Characters", value='\n'.join(featured_list))
        return icon_path, image_path, embed