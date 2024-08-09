import json

class commands:

    async def get_all_commands():
        with open('resources/commands/commands.json', 'r') as r:
            return json.load(r)
        
    async def get_command_info(command):
        commandData = await commands.get_all_commands()
        if f'cmd_{command.lower()}' in commandData:
            return commandData[f'cmd_{command.lower()}']
        else:
            for i, e in commandData.items():
                if command.lower() in e["triggers"]:
                    return e
            return 0