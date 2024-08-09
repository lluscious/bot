import asyncio
import discord
from util.log import logger
from application.client import Client
from resources.bot.bot_resources import bot_resources
from util.cache import cache

class init():
    def start():
        logger.log("Starting...")
        cache.clear_cache()
        token = bot_resources.get_token()
        Client(intents=discord.Intents.all()).run(token, log_handler=None)

init.start()