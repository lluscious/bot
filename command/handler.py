import importlib
import traceback
from util.log import logger
from resources.bot.bot_resources import bot_resources
from resources.commands.commands import commands

class command_handler:
    async def process_command(msg):
        command = msg.content.split(' ')[0].replace('-', '')
        resp = await commands.get_command_info(command)
        if resp == 0:
            logger.warn(f"Command {command} is not found in commands.json")
        else:
            permission = resp["permission"]
            user_permission = await bot_resources.get_user_permissions(msg.author.id)
            for i in user_permission:
                if i in permission:
                    logger.log(f"{msg.author.name}: {msg.content} (Permission Success)")
                    try:
                        wait = await msg.channel.send("I'm thinking...")
                        cmd_module = importlib.import_module(f"command.commands.{resp["module_name"]}")
                        cmd_rsp = await cmd_module.execute(msg)
                        if cmd_rsp == 0:
                            await wait.delete()
                            return await msg.channel.send(resp["usage"])
                        else:
                            logger.log(f"Command {command} executed successfully with return {cmd_rsp}")
                            return await wait.delete()
                    except Exception as e:
                        logger.error(e)
                        logger.error(traceback.format_exc())
                        await wait.delete()
                        return await msg.channel.send(f"Sorry... I encountered an error: `{e}`")
                    break
            else:
                logger.log(user_permission)
                if "permission_blacklist" in user_permission:
                    logger.log(f"{msg.author.name}: {msg.content} (Permission Denied)")
                    return await msg.channel.send("You are blacklisted.")
                else:
                    logger.log(f"{msg.author.name}: {msg.content} (Permission Denied)")
                    return await msg.channel.send("You do not have the permissions to use this command")

