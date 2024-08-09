import discord
import traceback
from util.log import logger
from command.handler import command_handler
from application.handlers.auto_response import auto_response_handler
from application.handlers.level import level_handler

class Client(discord.Client):
    
    async def on_ready(self):
        logger.log(f'Logged in as {self.user}')
        await self.change_presence(status=discord.Status.idle, activity=discord.Activity(type=discord.ActivityType.watching, name='大理寺'))

    async def on_message(self, message):
        if message.author.bot:
            return
        if message.content.startswith('-'):
            await command_handler.process_command(message)
        else:
            try:
                await auto_response_handler.handle(message)
                await level_handler.handle(message)
            except Exception as e:
                logger.error(e)
                logger.error(traceback.format_exc())

    async def on_reaction_add(self, reaction, user):
        logger.log(f"{user.name} react {reaction}")
        
