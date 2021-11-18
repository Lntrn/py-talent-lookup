# Import everything from the utilities folder. Defined in __init__.py of the relevant folder
from utilities import *

import pprint # https://docs.python.org/3.6/library/pprint.html

import random
import discord
import json

from utilities import config


async def talentsBetween(ctx, bot, args):

    talentsJson = open("./priorities/talents.json")
    talents = json.load(talentsJson)


    await ctx.send("searching, please wait.")

    argsStr = " ".join(args)
    splitArgs = argsStr.split(",")

    epicArr = ["epic", "e", "4"]
    urArr = ["ultra rare", "ur", "3"]
    rareArr = ["rare", "r", "2"]
    ucArr = ["uncommon", "uc", "1"]
    commonArr = ["common", "c", "0"]

    desRank = None
    desiredTalents = []

    if len(splitArgs) > 3:
        return await ctx.send("too many args, try again with a max of 3")

    for arg in splitArgs:

        arg = arg.strip()

        if "defy" in arg.lower() and "defying" not in arg.lower():
            arg = arg.replace("defy", "defying")
        if "armour" in arg.lower():
            arg = arg.replace("armour", "armor")

        if "-" in arg:
            arg = arg.replace("-", " ")
        if "." in arg:
            arg = arg.replace(".", "")
        if "'" in arg:
            arg = arg.replace("'", "")
    
        if arg.lower() in epicArr:
            desRank = "Epic"
        elif arg.lower() in urArr:
            desRank = "Ultra Rare"
        elif arg.lower() in rareArr:
            desRank = "Rare"
        elif arg.lower() in ucArr:
            desRank = "Uncommon"
        elif arg.lower() in commonArr:
            desRank = "Common"
        else:

            if arg.isdigit():
                desiredTalents.append(talents[int(arg)]["name"].lower().replace("-", " "))
            elif arg == "top":
                desiredTalents.append(talents[0]["name"].lower().replace("-", " "))
            elif arg == "bottom":
                desiredTalents.append(talents[-1]["name"].lower().replace("-", " "))
            else:
                desiredTalents.append(arg.lower())

    print(desRank)
    print(desiredTalents)

    arr = []

    for talent in talents:

        name = talent["name"]

        if "-" in name:
            name = name.replace("-", " ")

        if "'" in name:
            name = name.replace("'", "")
        if "." in name:
            name = name.replace(".", "")

        if name.lower() in desiredTalents:
            tal = {
                "name": name,
                "rank": talent["rank"],
                "url": talent["url"],
                "valid_url": talent["valid_url"],
                "locked": talent["locked"],
                "priority": talents.index(talent)
            }

            arr.append(tal)

            
    print(arr[0]["priority"])
    print(arr[1])

    if arr[0]["priority"] > arr[1]["priority"]:
        _max = arr[0]
        _min = arr[1]
    else:
        _max = arr[1]
        _min = arr[0]

    print(f"Min: {_min['priority']}")
    print(f"Max: {_max['priority']}")

    foundTalents = []

    for talent in talents[_min['priority']+1:_max['priority']]:

        name = talent["name"]

        if "-" in name:
            name = name.replace("-", " ")

        if "'" in name:
            name = name.replace("'", "")
        if "." in name:
            name = name.replace(".", "")

        tal = {
            "name": name,
            "rank": talent["rank"],
            "url": talent["url"],
            "valid_url": talent["valid_url"],
            "locked": talent["locked"],
            "priority": talents.index(talent)
        }

        if desRank != None:
            if talent['rank'] == desRank:
                foundTalents.append(tal)

        else:
            foundTalents.append(tal)

            

    foundTalents = sorted(foundTalents, key = lambda x : x["priority"])


    anotherArr = []

    if desRank != None:
        await ctx.send(f"Only returning `{desRank}` talents.")

    for talent in foundTalents:

        name = talent["name"]
        

        #print(len(str(priority)))


        priority = talent["priority"]

        if len(str(priority)) == 1:
            priority = f"00{priority}"

        elif len(str(priority)) == 2:
            priority = f"0{priority}"

        rank = talent["rank"]
        
        if rank == "Common":
            rank = "C "
        elif rank == "Uncommon":
            rank = "UC"
        elif rank == "Rare":
            rank = "R "
        elif rank == "Ultra Rare":
            rank = "UR"
        elif rank == "Epic":
            rank = "E "

        unlocked = ""

        unlockables = ["finder", "hunter", "scout", "farmer", "trained", "track r treater", "elemental retriever", "hatch catcher"]

        for u in unlockables:
            if u in name.lower():
                #print("match!!!")
                if talent["locked"] == True:
                    #print("true!")
                    unlocked = " | Locked"
                elif talent["locked"] == False:
                    #print("false!")
                    unlocked = " | Unlocked"
                else:
                    print("this shouldnt happen ever")


        talentMsg = f"> `{priority}` | `{rank}` | {name}{unlocked}"

        anotherArr.append(talentMsg)



    minRank = _min['rank']

    if minRank == "Common":
        minRank = "C "
    elif minRank == "Uncommon":
        minRank = "UC"
    elif minRank == "Rare":
        minRank = "R "
    elif minRank == "Ultra Rare":
        minRank = "UR"
    elif minRank == "Epic":
        minRank = "E "

    maxRank = _max['rank']

    if maxRank == "Common":
        maxRank = "C "
    elif maxRank == "Uncommon":
        maxRank = "UC"
    elif maxRank == "Rare":
        maxRank = "R "
    elif maxRank == "Ultra Rare":
        maxRank = "UR"
    elif maxRank == "Epic":
        maxRank = "E "

    minPrio = _min['priority']
    if len(str(minPrio)) == 1:
        minPrio = f"00{minPrio}"
    elif len(str(minPrio)) == 2:
        minPrio = f"0{minPrio}"

    maxPrio = _max['priority']
    if len(str(maxPrio)) == 1:
        maxPrio = f"00{maxPrio}"
    elif len(str(maxPrio)) == 2:
        maxPrio = f"0{maxPrio}"


    minMsg = f"`{minPrio}` | `{minRank}` | {_min['name']}"
    maxMsg = f"`{maxPrio}` | `{maxRank}` | {_max['name']}"

    anotherArr.insert(0, minMsg)
    anotherArr.append(maxMsg)

    print(len(anotherArr))

    chunks = []
    while anotherArr:
        chunks.append(anotherArr[:20])
        anotherArr = anotherArr[20:]

    for chunk in chunks:

        #print(chunk)

        try:
            await ctx.author.send("\n".join(chunk))
        except:
            await ctx.send("could not dm you the results, make sure you have dms enabled for this server.")
            break

    await ctx.send("task completed!")



async def search(ctx, bot, args):
    
    talentsJson = open("./priorities/talents.json")
    talents = json.load(talentsJson)

    # Preprare args for use.
    argsStr = " ".join(args)

    splitArgs = argsStr.split(",")
    desiredTalents = []
    desPriorities = []

    for arg in splitArgs:

        arg = arg.strip()

        arg = arg.lower()

        if "defy" in arg and "defying" not in arg:
            arg = arg.replace("defy", "defying")
        if "armour" in arg:
            arg = arg.replace("armour", "armor")

        if "'" in arg:
            arg = arg.replace("'", "")
        if "." in arg:
            arg = arg.replace(".", "")

        if "-" in arg:
            arg = arg.replace("-", " ")

        if arg.isdigit():
            desPriorities.append(int(arg))
        elif arg.lower() == "top":
            desPriorities.append(0)
        elif arg.lower() == "bottom":
            desPriorities.append(len(talents)-1)

        desiredTalents.append(arg)

    print(f"Args:\n{desiredTalents}")

    foundTalents = []

    for num in desPriorities:

        name = talents[num]["name"]

        if "-" in name:
            name = name.replace("-", " ")

        if "'" in name:
            name = name.replace("'", "")
        if "." in name:
            name = name.replace(".", "")

        tal = {
                "name": name,
                "rank": talents[num]["rank"],
                "url": talents[num]["url"],
                "valid_url": talents[num]["valid_url"],
                "locked": talents[num]["locked"],
                "priority": talents.index(talents[num])
            }

        foundTalents.append(tal)

    for talent in talents:

        name = talent["name"]

        if "-" in name:
            name = name.replace("-", " ")

        if "'" in name:
            name = name.replace("'", "")
        if "." in name:
            name = name.replace(".", "")

        #print(name.lower())

        if [d for d in desiredTalents if d in name.lower()]:

            #print(f"matched\n{talent}")

            tal = {
                "name": name,
                "rank": talent["rank"],
                "url": talent["url"],
                "valid_url": talent["valid_url"],
                "locked": talent["locked"],
                "priority": talents.index(talent)
            }

            foundTalents.append(tal)

    #print(foundTalents)

    # Order the array by priority
    foundTalents = sorted(foundTalents, key = lambda x : x["priority"])
    amnt = len(foundTalents)
    chunks = []
    while foundTalents:
        chunks.append(foundTalents[:10])
        foundTalents = foundTalents[10:]

    print(len(chunks))
    if len(chunks) < 10:

        colour = await s.randomColour()

        embed = discord.Embed(
            title = f"{ctx.author}",
            color = colour
        ).set_thumbnail(
            url = ctx.author.avatar_url
        ).set_footer(
            text = f"Returned {amnt} talents."
        )

        for chunk in chunks:

            talentsArray = ["Priority | Rank | Name | Locked/Unlocked Position"]

            
            for talent in chunk:

                name = talent["name"]
                url = talent["url"]
                urlCheck = talent["valid_url"]

                if urlCheck == True:
                    name = f"[{name}]({url})"
        

                #print(len(str(priority)))


                priority = talent["priority"]

                if len(str(priority)) == 1:
                    priority = f"00{priority}"

                elif len(str(priority)) == 2:
                    priority = f"0{priority}"


                rank = talent["rank"]
        
                if rank == "Common":
                    rank = "C "

                elif rank == "Uncommon":
                    rank = "UC"

                elif rank == "Rare":
                    rank = "R "

                elif rank == "Ultra Rare":
                    rank = "UR"

                elif rank == "Epic":
                    rank = "E "

                talentMsg = ""



                #if talent["name"].lower() 

                unlocked = ""

                unlockables = ["finder", "hunter", "scout", "farmer", "trained", "track r treater", "elemental retriever", "hatch catcher"]

                for u in unlockables:
                    #print(u)
                    #print(name.lower())
                    if u in name.lower():
                        #print("match!!!")

                        if talent["locked"] == True:
                            #print("true!")
                            unlocked = " | Locked"
                        elif talent["locked"] == False:
                            #print("false!")
                            unlocked = " | Unlocked"
                        else:
                            print("this shouldnt happen ever")
                    #else:
                    #    unlocked = "NA"

                talentMsg = f"`{priority}` | `{rank}` | {name}{unlocked}"
                talentsArray.append(talentMsg)

            embed.add_field(
                name = f"Chunk {chunks.index(chunk)}",
                value = "\n".join(talentsArray),
                inline = False
            )


        await ctx.send(embed = embed)

    else:

        for chunk in chunks:

            talentsArray = ["Priority | Rank | Name | Locked/Unlocked Position"]


            for talent in chunk:

                name = talent["name"]
        

                #print(len(str(priority)))


                priority = talent["priority"]

                if len(str(priority)) == 1:
                    priority = f"00{priority}"

                elif len(str(priority)) == 2:
                    priority = f"0{priority}"


                rank = talent["rank"]
        
                if rank == "Common":
                    rank = "C "

                elif rank == "Uncommon":
                    rank = "UC"

                elif rank == "Rare":
                    rank = "R "

                elif rank == "Ultra Rare":
                    rank = "UR"

                elif rank == "Epic":
                    rank = "E "

                talentMsg = ""



                #if talent["name"].lower() 

                unlocked = ""

                unlockables = ["finder", "hunter", "scout", "farmer", "trained", "track r treater", "elemental retriever", "hatch catcher"]

                for u in unlockables:
                    #print(u)
                    #print(name.lower())
                    if u in name.lower():
                        #print("match!!!")

                        if talent["locked"] == True:
                            #print("true!")
                            unlocked = " | Locked"
                        elif talent["locked"] == False:
                            #print("false!")
                            unlocked = " | Unlocked"
                        else:
                            print("this shouldnt happen ever")
                    #else:
                    #    unlocked = "NA"

                talentMsg = f"`{priority}` | `{rank}` | {name}{unlocked}"
                talentsArray.append(talentMsg)
        
        
            await ctx.author.send("\n".join(talentsArray))
            await ctx.send("task completed!")
































async def sendInvalidURLS(bot, ctx):

    talentsJson = open("./priorities/talents.json")
    talents = json.load(talentsJson)

    invalidURLS = []

    for talent in talents:
        #if talent["valid_url"] != True:
        #print(talent["name"])
        if talent["name"].lower() == "death giver":

            check = False

            for tal in invalidURLS:

                if (tal["name"]).lower() == talent["name"].lower():
                    print(talent["name"].lower())
                    print(tal["name"].lower())
                    print("match!")
                    check = True
            
            if check == False:
                #print("adding %s to array}"%talent["name"])
                invalidURLS.append(talent)

    name = ""
    rank = ""

    pprint.pprint(invalidURLS)

    for talent in invalidURLS:

        name = talent["name"]
        rank = talent["rank"]
        colour = await s.randomColour()

        embed = discord.Embed(
            title = name,
            description = f"rank: %s"%rank,
            color = colour
        ).set_footer(
            text = str(colour)
        )


        await bot.get_channel(791218472700739655).send(embed = embed)



        


async def stats(ctx):

    talentsJson = open("./priorities/talents.json")
    talents = json.load(talentsJson)

    listLength = len(talents)

    commons = 0
    uncommons = 0
    rares = 0
    ultra_rares = 0
    epics = 0

    invalidURLS = []

    for talent in talents:

        if talent["valid_url"] != True:
            invalidURLS.append(talent)


        #print(talent["rank"].lower())

        if talent["rank"].lower() == "common":
            commons += 1

        elif talent["rank"].lower() == "uncommon":
            uncommons += 1

        elif talent["rank"].lower() == "rare":
            rares += 1

        elif talent["rank"].lower() == "ultra rare":
            ultra_rares += 1

        elif talent["rank"].lower() == "epic":
            epics += 1

    sendThis = f"Commons: {commons}\nUncommons: {uncommons}\nRares: {rares}\nUltra Rares: {ultra_rares}\nEpics: {epics}"
    colour = await s.randomColour()

    embed = discord.Embed(
        #title = f"{ctx.author}",
        #url = "",
        #description = f"{listLength}",
        color = colour
    #).set_author(
        #name = ctx.author,
        #url = "",
        #icon_url = ctx.author.avatar_url
    ).set_thumbnail(
        url = "https://cdn.discordapp.com/attachments/807513553431035924/895894619932475423/802528771026190366.png"
    ).add_field(
        name = f"Total Talents: {listLength}",
        value = sendThis,
        inline = False
    ).add_field(
        name = f"Talents with invalid URLS: {len(invalidURLS)}",
        value = len(invalidURLS),
        inline = False
    #).set_footer(
    #    text = f"Returned {len(foundTalents)} talents.",
    #    icon_url = ctx.author.avatar_url
    )

    pprint.pprint(invalidURLS)
    await ctx.send(embed = embed)




async def prepArgs(ctx, args):

    talentsJson = open("./priorities/talents.json")
    talents = json.load(talentsJson)
    
    argsStr = " ".join(args)
    argsFixed = argsStr.split(",")


    foundTalents = []

    for a in argsFixed:
        a = a.strip()


        x = 0

        for talent in talents:

            name = talent["name"]
            if "-" in name:
                name = name.replace("-", " ")


            if a.lower() in name.lower():

                #print(talent["name"])

                tal = {
                    "name": name,
                    "rank": talent["rank"],
                    "url": talent["url"],
                    "valid_url": talent["valid_url"],
                    "locked": talent["locked"],
                    "priority": talents.index(talent)
                }


                foundTalents.append(tal)



            #print(talent["name"].lower())

            #talent[name] = s.lower(talent[name])

            #if talent.name == a.lower():
            #    await ctx.send(talent.name)

    unlockables = ["finder", "hunter", "scout", "farmer", "trained", "track r treater", "elemental retriever", "hatch catcher"]

    embed = discord.Embed(
        name = ctx.author
    ).set_thumbnail(
        url = ctx.author.avatar_url
    ).set_footer(
        text = f"Returned {len(foundTalents)} talents.",
        icon_url = ctx.author.avatar_url
    )

    # Order the array by priority
    foundTalents = sorted(foundTalents, key=lambda x:x["priority"])

    chunks = []
    while foundTalents:
        chunks.append(foundTalents[:10])
        foundTalents = foundTalents[10:]

    #pprint.pprint(chunks)
    
    for chunk in chunks:

        sendThis = "Priority | Rank | Name | Locked/Unlocked Position"
        talentsArray = []

        for talent in chunk:
        #print(talent)

            name = talent["name"]
            url = talent["url"]
            urlCheck = talent["valid_url"]

            if urlCheck == True:
                name = f"[{name}]({url})"
        

            #print(len(str(priority)))


            priority = talent["priority"]

            if len(str(priority)) == 1:
                priority = f"00{priority}"

            elif len(str(priority)) == 2:
                priority = f"0{priority}"


            rank = talent["rank"]
        
            if rank == "Common":
                rank = "C "

            elif rank == "Uncommon":
                rank = "UC"

            elif rank == "Rare":
                rank = "R "

            elif rank == "Ultra Rare":
                rank = "UR"

            elif rank == "Epic":
                rank = "E "

            talentMsg = ""



            #if talent["name"].lower() 

            unlocked = ""

            for u in unlockables:
                #print(u)
                #print(name.lower())
                if u in name.lower():
                    #print("match!!!")

                    if talent["locked"] == True:
                        #print("true!")
                        unlocked = " | Locked"
                    elif talent["locked"] == False:
                        #print("false!")
                        unlocked = " | Unlocked"
                    else:
                        print("this shouldnt happen ever")
                #else:
                #    unlocked = "NA"

            talentMsg = f"`{priority}` | `{rank}` | {name}{unlocked}"
            talentsArray.append(talentMsg)
    
        embed.add_field(
            name = "Priority | Rank | Name | Locked/Unlocked Position",
            value = "\n".join(talentsArray),
            inline = False
        )
    
    await ctx.send(embed = embed)

    return
    """
    chunks = []
    while talentsArray:
        chunks.append(talentsArray[:8])
        talentsArray = talentsArray[8:]
    """
    #print(chunks)
    #await ctx.send("done")

    count = 0
    for c in chunks:
        pprint.pprint(c)
        embed.add_field(
            name = f"Page {count}",
            value = c,
            inline = False
        )    
        count += 1

    await ctx.send(embed = embed)