import json
from util.log import logger

class character:

    async def get_all_character_config():
        with open("resources/character/character_config.json", 'r') as f:
            return json.load(f)

    async def get_character_config(id):
        id = str(id)
        character_config = await character.get_all_character_config()
        if not character_config[id]:
            logger.warn(f"{id} does not exist!")
            return {}
        return character_config[id]
