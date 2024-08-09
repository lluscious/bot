import json
import os

from util.log import logger

class user_info_config:

    async def get_all_data(file):
        if not os.path.exists(f"resources/user/{file}.json"):
            logger.warn(f"{file} doesn't exist in resources/users")
            return 0
        with open(f"resources/user/{file}.json", 'r') as e:
            return json.load(e)
        
    async def get_ranking_config_from_level(level):
        ranking_config = await user_info_config.get_all_data("ranking_config")
        level = int(level)
        for r, s in ranking_config.items():
            min_lv = s["min_level"]
            max_lv = s["max_level"]
            if min_lv <= level <= max_lv:
                return s
        else:
            logger.warn("something isnt right..")

    async def get_ranking_config_from_id(rank):
        ranking_config = await user_info_config.get_all_data("ranking_config")
        if not rank in ranking_config:
            logger.warn(f"{rank} is not found in ranking_config.json")
            return 0
        else:
            return ranking_config[rank]
        
    async def get_level_config(level):
        level_config = await user_info_config.get_all_data("level_config")
        level = str(level)
        if level in level_config:
            return level_config[level]
        else:
            logger.warn(f"{level} not in level_config.json")
            return 0
        
    