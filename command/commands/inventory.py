import discord
from resources.user.user_info_config import user_info_config
from resources.items.item import item
from resources.data.data import data

rarity_table = {
    "rarity_5": "5*",
    "rarity_4": "4*",
    "rarity_3": "3*"
}

types = {
    "weapon": "weapons",
    "weapons": "weapons",
    "w": "weapons",
    "material": "material",
    "materials": "material",
    "mats": "material",
    "mat": "material",
    "m": "material",
    "usable": "usable",
    "usables": "usable",
    "precious": "precious"
}

names = {
    "weapons": "Weapons",
    "material": "Materials",
    "usable": "Usables",
    "precious": "Precious items"
}

async def make_inv_embed(user, types, inv):
    embed = discord.Embed(title=f"{user.name}'s Inventory")
    embed.set_thumbnail(url=user.display_avatar.url)
    page = inv[types]
    for rarity, type in page.items():
        items_list = []
        for i, quantity in type.items():
            item_config = await item.get_item_config_from_id(i)
            items_list.append(f"x{quantity} {item_config["name"]}")
        items = "\n".join(items_list)
        embed.add_field(name=f"{rarity_table[rarity]} {names[types]}", value=items or "None", inline=False)
    return embed


async def execute(msg):
    user = msg.author
    author_id = msg.author.id
    if msg.mentions:
        user = msg.mentions[0]
    category = msg.content.split(' ')
    if len(category) != 2:
        return 0
    category = category[1]
    inv = await data.get_inventory(user=user)
    if category in types:
        embed = await make_inv_embed(user, types[category], inv)
    await msg.channel.send(embed=embed)
    return 1