import json

from util.log import logger

class auto_response:

    async def get_all_auto_response():
        with open("resources/auto_response/auto_response_config.json", "r") as r:
            return json.load(r)
        
    async def get_auto_response_from_msg(msg):
        auto_response_config = await auto_response.get_all_auto_response()
        split = msg.content.split(' ')
        for word in split:
            for i, e in auto_response_config.items():
                for trigger in e["trigger"]:
                    if trigger == word.lower():
                        return e
        return 0

    
    async def get_auto_response_config_from_id(id):
        auto_response_config = await auto_response.get_all_auto_response()
        if id not in auto_response_config:
            logger.warn(f"{id} not in auto_response_config.json!")
            return 0
        return auto_response_config[id]