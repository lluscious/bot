import discord
from resources.store.store import store
from resources.items.item import item

async def convert_int(is_view, id):
    try:
        int(id)
        return id
    except ValueError:
        if id == "all" and is_view == True:
            return id
        else:
            return 0

async def get_store_embed(config):
    store_id = config["id"]
    name = config["name"]
    color = config["color"]
    desc = config["desc"]
    image = config["image"]
    side = config["side_image"]
    items = config["items"]
    embed = discord.Embed(title=name, color=discord.Color.from_str(color), description=desc)
    embed.set_image(url=image)
    embed.set_thumbnail(url=side)
    for i, u in items.items():
        item_info = await item.get_item_config_from_id(i)
        name = item_info["name"]
        cost = u["cost"]
        cost_info = await store.get_cost_item_info(u["cost_id"])
        cost_item = cost_info["name"]
        embed.add_field(name=name, value=f"Id: {i}\nPrice: x{cost} {cost_item}")
    embed.set_footer(text=f"store_id: {store_id}")
    return embed

async def execute(msg):
    user = msg.author
    args = msg.content.split(' ')
    if not len(args) >= 2:
        return 0
    action = args[1]
    if action == "view":
        store_id = 60001
        rsp = "The store you mentioned was not found, So i displayed the default store instead."
        if len(args) == 3:
            store_id = await convert_int(True, args[2])
            if store_id == 0:
                await msg.channel.send("Store id must be a number!")
                return 1
            rsp = ""
        if store_id == "all":
            config = await store.get_all_store_config()
            for i, u in config.items():
                config = await store.get_store_config_by_name(i)
                embed = await get_store_embed(config)
            await msg.channel.send(embed=embed)
            return 1
        else:
            config = await store.get_store_config_by_id(store_id)
            if config == 0:
                config = await store.get_store_config_by_id(60001)
                rsp = "The store you mentioned was not found, So i displayed the default store instead."
            embed = await get_store_embed(config)
            await msg.channel.send(content=rsp, embed=embed)
            return 1
    elif action == "buy":
        if not len(args) == 5:
            return 0
        store_id = await convert_int(False, args[2])
        item_id = await convert_int(False, args[3])
        amount = await convert_int(False, args[4])
        if amount == 0 or item_id == 0 or store_id == 0:
            await msg.channel.send("One or more args were invalid!")
            return 1
        rsp = await store.buy_store_item(user, store_id, item_id, amount)
        await msg.channel.send(rsp)
        return 1
    else:
        return 0
        

