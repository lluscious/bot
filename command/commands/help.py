import discord
from resources.commands.commands import commands

async def execute(msg):
    cmds = await commands.get_all_commands()
    embed = discord.Embed(title="All of my commands", color=discord.Color.from_str("#4287f5"))
    embed.set_thumbnail(url=msg.guild.icon)
    for o, i in cmds.items():
        name = i["name"]
        desc = i["description"]
        usage = i["usage"]
        alias = ", ".join(i["triggers"])
        embed.add_field(name=name, value=f"{desc}\n- usage: {usage}\n- Alias: {alias}", inline=False)
    await msg.channel.send(embed=embed)
    return 1
