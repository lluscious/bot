import random

from resources.data.data import data
from resources.auto_response.auto_response import auto_response
from resources.items.item import item
from util.log import logger

class level_handler:

    async def handle(msg):
        user = msg.author
        if random.randrange(1, 50) == 1:
            rsp = await data.add_user_exp(user, 500)
            if rsp != 0:
                await msg.channel.send(f"{user.name} has advanced to {rsp}!")