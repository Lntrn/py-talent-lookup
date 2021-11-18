import json
from os import replace
import discord

# Import all files defined in __init__.py from the utilities folder
from utilities import *

async def processArgs(args):

    joint = " ".join(args)

    split = joint.split(",")

    data = []

    for x in split:
        
        d = {
            "content": x.strip(),
            "exact": False
        }

        data.append(d)


    return data

async def compare(ctx, bot, args):
    desired = await processArgs(args)
    jsonFile = open("./utilities/bodydata.json")
    bodies = json.load(jsonFile)
    bodiesArr = bodies["pets"]
    found = []
    exact = None

    print(len(desired))

    for des in desired:

        print(des)

        clone = des['content'].strip()

        split = clone.split(" ")

        exactArr = ["-e", "exact"]

        for x in split:

            print(x)

            if x in exactArr:

                index = desired.index(des)

                desired[index]['exact'] = True

                desired[index]['content'] = desired[index]['content'].replace(x, "")


        """
        for x in split:
            
            if x in exactArr:

                index = desired.index(des)

                desired[index]['exact'] = True

                print(index)

                desired[index]['content'] = desired[index]['content'].replace(x, "")

            else:
                 desired[index]['exact'] = False
            """

    for body in bodiesArr:

        for des in desired:
            content = des['content'].strip()

            if "'" in des:
                content = content.replace("'", "")

            if des['exact'] != True:

                if content.lower().strip() in body['name'].replace("'", "").lower():
                    found.append(body)

            else:

                if content.lower().strip() == body['name'].replace("'", "").lower():
                    found.append(body)

    rarityOrder = ["Common", "Uncommon", "Rare", "Ultra-Rare", "Epic"]

    #foundTalents = sorted(found, key = lambda x : x["priority"])
    found = sorted(found, key = lambda x : x["wow_factor"], reverse = True)
    found = sorted(found, key = lambda v: rarityOrder.index(v['rarity']), reverse = True)

    returned = len(found)
    chunks = []
    
    while found:
        chunks.append(found[:10])
        found = found[10:]

    if len(chunks) < 25:
        await ctx.send(f"Found {returned} matches, please wait.")

        colour = await s.randomColour()

        embed = discord.Embed(
            title = ctx.author,
            color = colour
        ).set_footer(
            text = f"Returned {returned} bodies"
        )

        for chunk in chunks:

            msgArr = []

            for body in chunk:

                if body['rarity'] == "Common":
                    rarity = "`C `"
                elif body['rarity'] == "Uncommon":
                    rarity = "`UC`"
                elif body['rarity'] == "Rare":
                    rarity = "`R `"
                elif body['rarity'] == "Ultra-Rare":
                    rarity = "`UR`"
                elif body['rarity'] == "Epic":
                    rarity = "`E `"

                if body['wow_factor'] == 1:
                    wow = "` 1`"
                elif body['wow_factor'] == 2:
                    wow = "` 2`"
                elif body['wow_factor'] == 3:
                    wow = "` 3`"
                elif body['wow_factor'] == 4:
                    wow = "` 4`"
                elif body['wow_factor'] == 5:
                    wow = "` 5`"
                elif body['wow_factor'] == 6:
                    wow = "` 6`"
                elif body['wow_factor'] == 7:
                    wow = "` 7`"
                elif body['wow_factor'] == 8:
                    wow = "` 8`"
                elif body['wow_factor'] == 9:
                    wow = "` 9`"
                elif body['wow_factor'] == 10:
                    wow = "`10`"
                
                msgArr.append(f"> {rarity} | {wow} | {body['name']} ")


            embed.add_field(
                name = "chunk",
                value = "\n".join(msgArr),
                inline = False
            )

        await ctx.send(embed = embed)

    else: 

        await ctx.author.send(f"Found {returned} matches, please wait.")

        for chunk in chunks:


            msgArr = []
            for body in chunk:

                if body['rarity'] == "Common":
                    rarity = "`C `"
                elif body['rarity'] == "Uncommon":
                    rarity = "`UC`"
                elif body['rarity'] == "Rare":
                    rarity = "`R `"
                elif body['rarity'] == "Ultra-Rare":
                    rarity = "`UR`"
                elif body['rarity'] == "Epic":
                    rarity = "`E `"

                if body['wow_factor'] == 1:
                    wow = "` 1`"
                elif body['wow_factor'] == 2:
                    wow = "` 2`"
                elif body['wow_factor'] == 3:
                    wow = "` 3`"
                elif body['wow_factor'] == 4:
                    wow = "` 4`"
                elif body['wow_factor'] == 5:
                    wow = "` 5`"
                elif body['wow_factor'] == 6:
                    wow = "` 6`"
                elif body['wow_factor'] == 7:
                    wow = "` 7`"
                elif body['wow_factor'] == 8:
                    wow = "` 8`"
                elif body['wow_factor'] == 9:
                    wow = "` 9`"
                elif body['wow_factor'] == 10:
                    wow = "`10`"
                
                msgArr.append(f"> {rarity} | {wow} | {body['name']} ")

            try:
                await ctx.author.send("\n".join(msgArr))
            except:
                await ctx.send("cannot dm you, make sure they are enabled in a server we have in common")

        await ctx.send(f"task completed. check your dms.")






async def byName(ctx, bot, args):

    desired = await processArgs(args)

    jsonFile = open("./utilities/bodydata.json")
    bodies = json.load(jsonFile)
    bodiesArr = bodies["pets"]

    for des in desired:

        print(des)

        clone = des['content'].strip()

        split = clone.split(" ")

        exactArr = ["-e", "exact"]

        for x in split:

            print(x)

            if x in exactArr:

                index = desired.index(des)

                desired[index]['exact'] = True

                desired[index]['content'] = desired[index]['content'].replace(x, "")



    found = []

    for body in bodiesArr:

        for des in desired:
            content = des['content'].strip()

            if "'" in des:
                content = content.replace("'", "")

            if des['exact'] != True:

                if content.lower().strip() in body['name'].replace("'", "").lower():
                    found.append(body)

            else:

                if content.lower().strip() == body['name'].replace("'", "").lower():
                    found.append(body)
    
    """

    name = body["name"]
    rarity = body["rarity"]
    wow = body["wow_factor"]
    adj = body["adjectives"]
    race = body["race"]
    eggType = body["egg_name"]
    exclusive = body["exclusive"]
    school = body["school"]

    adjStr = "\n> ".join(adj)

    embed.add_field(
        name = name,
        value = f"**Body Rarity**: {rarity}\n**Wow Factor**: {wow}\n**Race**: {race}\n**School**: {school}\n**Exclusive?**: {exclusive}\n**Egg Type**: {eggType}\n\n**Adjectives**:\n> {adjStr}"
    )


    """

    if len(found) <= 15:

        await ctx.send(f"Found {len(found)} matches, please wait.")

        colour = await s.randomColour()

        embed = discord.Embed(
            title = ctx.author,
            color = colour,
            description = f"Possible Rarities:\n> Common, Uncommon, Rare, Ultra Rare, Epic"
        ).set_footer(
            text = f"Returned {len(found)} bodies"
        )

        for body in found:

            favouritesnacks = "\n> ".join(body['favorite_snacks'])
            adj = "\n> ".join(body['adjectives'])

            msg = f"**Body Rarity**: {body['rarity']}\n**Wow Factor**: {body['wow_factor']}\n\n**Egg Name**: {body['egg_name']}\n**Exclusive?**: {body['exclusive']}\n**Race**: {body['race']}\n**School**: {body['school']}\n\n**Favourite Snack Types**:\n> {favouritesnacks}\n\n**Adjectives**:\n> {adj}"

            if body['item_set']:

                msg += f"\n\n**Item Set**: {body['item_set']}"

            embed.add_field(
                name = f"__{body['name']}__",
                value = msg
            )

        await ctx.send(embed = embed)

    else:

        await ctx.send(f"Found {len(found)} matches, please wait.\n\nPossible Rarities:\n> Common, Uncommon, Rare, Ultra Rare, Epic")

        for body in found:

            favouritesnacks = "\n> ".join(body['favorite_snacks'])
            adj = "\n> ".join(body['adjectives'])

            msg = f"**Body Rarity**: {body['rarity']}\n**Wow Factor**: {body['wow_factor']}\n\n**Egg Name**: {body['egg_name']}\n**Exclusive?**: {body['exclusive']}\n**Race**: {body['race']}\n**School**: {body['school']}\n\n**Favourite Snack Types**:\n> {favouritesnacks}\n\n**Adjectives**:\n> {adj}"

            colour = await s.randomColour()

            embed = discord.Embed(
                color = colour
            ).add_field(
                name = f"__{body['name']}__",
                value = msg
            ).set_footer(
                text = f"{found.index(body)} of {len(found)}"
            )


            try:
                await ctx.author.send(embed = embed)
            except:
                await ctx.send("cannot dm you, make sure they are enabled in a server we have in common")

        await ctx.send(f"task completed. check your dms.")
