import discord
from resources.items.item import item
from resources.data.data import data
from resources.gacha.gacha import gacha

keywords = ["wish", "pull", "w"]

async def convert_int(val):
    try:
        val = int(val)
        return val
    except ValueError:
        return 0
    
async def make_results(user, banner_id, drops, rarity5_list):
    user_gacha = await data.get_gacha_banner_data(user, banner_id)
    embed = discord.Embed(title=f"{user.name}'s Wish", color=user.color)
    result_5 = []
    result_4 = []
    result_3 = []
    for i in drops["5"]:
        for t in rarity5_list:
            for s, e in t.items():
                if s == i:
                    result_5.append(f"{i} ({e})")
                    break
                break
            break
        break
    for i in drops["4"]:
        config = await item.get_item_config_from_id(i)
        result_4.append(config["name"])
    for i in drops["3"]:
        config = await item.get_item_config_from_id(i)
        result_3.append(config["name"])
    embed.set_thumbnail(url=user.display_avatar.url)
    embed.add_field(name=f"5* drops", value=", ".join(result_5), inline=False)
    embed.add_field(name=f"4* drops", value=", ".join(result_4), inline=False)
    embed.add_field(name=f"3* drops", value=", ".join(result_3), inline=False)
    embed.set_footer(text=f"Pity: {user_gacha["pity_5"]} // Rateup: {user_gacha["is_rate_up"]}")
    return embed

async def execute(msg):
    user = msg.author
    args = msg.content.split(' ')
    if len(args) < 3:
        return 0
    action = args[1]
    if action == "view": 
        banner_config = await gacha.get_all_banner_config()
        if args[2] == "all":
            for s, i in banner_config.items():
                icon_path, image_path, banner_embed = await gacha.make_gacha_banner_embed(i)
                await msg.channel.send(files=[icon_path, image_path], embed=banner_embed)
        else:
            banner = await gacha.get_banner(args[2])
            if banner == 0: await msg.channel.send(f"{args[2]} does not exist in my banner data..."); return 1
            icon_path, image_path, banner_embed = await gacha.make_gacha_banner_embed(banner)
            await msg.channel.send(files=[icon_path, image_path], embed=banner_embed)
        return 1
    elif action in keywords:
        # -gacha wish 10001 10
        banner_id = args[2]
        amount = await convert_int(args[3])
        if amount == 0:
            return 0
        if amount > 30:
            amount = 30
        banner = await gacha.get_banner(banner_id)
        if banner == 0: await msg.channel.send(f"{banner_id} does not exist in my banner data..."); return 1
        results, rarity5_pity_list = await gacha.process_wish(user, banner_id, amount)
        embed = await make_results(user, banner_id, results, rarity5_pity_list)
        await msg.channel.send(embed=embed)
        return 1
    return 0