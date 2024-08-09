import discord

from resources.data.data import data
from resources.auto_response.auto_response import auto_response
from resources.items.item import item
from util.log import logger

class auto_response_handler:

    async def handle(msg):
        user = msg.author
        rsp = await auto_response.get_auto_response_from_msg(msg)
        if rsp == 0:
            return
        logger.log(f'Auto response invoke: {msg.content}')
        if rsp["response_type"] == "reply":
            await msg.channel.send(rsp["response"])
            for i, e in rsp["reward_list"].items():
                item_config = await item.get_item_config_from_id(i)
                if item_config["type"] == "currency":
                    await data.modify_user_currency(user, i, e)
                elif item_config["type"] == "level":
                    rsp = await data.add_user_exp(user, e)
                    if rsp != 0:
                        await msg.channel.send(f"{user.name} has advanced to {rsp}!")
                elif item_config["type"] == "item":
                    await data.modify_user_inventory_by_config(user, item_config, e)
        elif rsp["response_type"] == "react":
            await msg.react(rsp["response"])