import discord
from resources.user.user_info_config import user_info_config
from resources.items.item import item
from resources.data.data import data

keys = {
    "sig": "signature",
    "signature": "signature",
    "thumbnail": "thumbnail_url",
    "icon": "thumbnail_url",
    "thumbnail_url": "thumbnail_url",
    "image": "image_url",
    "image_url": "image_url",
    "colour": "color", # fuck the britishians
    "color": "color"
}

async def execute(msg):
    user = msg.author
    args = msg.content.split(' ')
    action = "view"
    if len(args) >= 2:
        action = args[1]
    if action == "view":
        if msg.mentions:
            user = msg.mentions[0]
        user_info = await data.get_user_info(user=user)
        ranking = await user_info_config.get_ranking_config_from_id(user_info["rank"])
        properties = user_info["currency"]
        profile = discord.Embed(title=f"{user.display_name} ({user_info["name"]})", color=discord.Color.from_str(user_info["color"]))
        profile.description = f'"{user_info["signature"]}" - {user.name}'
        if user_info["thumbnail_url"] == "pfp":
            profile.set_thumbnail(url=user.display_avatar.url)
        else:
            profile.set_thumbnail(url=user_info["thumbnail_url"])
        profile.set_image(url=user_info["image_url"])
        level = user_info["lv"]
        level_config = await user_info_config.get_level_config(level["level"])
        profile.add_field(name="Level", value=f"{level["level"]} ({level["exp"]}/{level_config})", inline=True)
        profile.add_field(name="Total Pulls", value=user_info["total_pulls"], inline=True)
        profile.add_field(name="Rank", value=ranking["name"], inline=True)
        for i, u in properties.items():
            d = await item.get_item_config_from_id(i)
            profile.add_field(name=d["name"], value=u)
        await msg.channel.send(embed=profile)
        return 1
    elif action == "edit":
        if not len(args) >= 4: # -profile edit signature hi
            await  msg.channel.send('Usage: -profile edit <property> <new value>\nProperties: signature, thumbnail, image, color')
            return 1
        edit_prop = args[2]
        new_value = " ".join(args[3:])
        if edit_prop in keys:
            edit_prop = keys[edit_prop]
        else:
            await msg.channel.send('Usage: -profile edit <property> <new value>\nProperties: signature, thumbnail, image, color')
            return 1
        rsp = await data.edit_user_info(user, edit_prop, new_value)
        if rsp == 1:
            await msg.channel.send(f"Edited {edit_prop} to `{new_value}`!")
            return 1
        else:
            await msg.channel.send("Something went wrong...")
            return 1
    else:
        return 0