# Import ?
import os
import json
import pprint

import asyncio

# python3 -m pip install requests
import requests

# python3 -m pip install beautifulsoup4
from bs4 import BeautifulSoup


# py -3 -m pip install -U discord.py    
import discord

from discord.ext import commands
from discord.ext.commands.core import before_invoke

# Import all files defined in __init__.py from the utilities folder
from utilities import *

# Import all files defined in __init__.py from the commands folder
from commands import *

# pip install python-dotenv
from dotenv import load_dotenv

from utilities import config
# Load the .env file
load_dotenv()
# Get a variable by it's name
token = os.getenv("TOKEN")


# Playing -> activity = discord.Game(name="!help")
# Streaming -> activity = discord.Streaming(name="!help", url="twitch_url_here")
# Listening -> activity = discord.Activity(type=discord.ActivityType.listening, name="!help")
# Watching -> activity = discord.Activity(type=discord.ActivityType.watching, name="!help")
activity = discord.Game(
    name = f"{config.prefixes[0]}help"
)

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(
    command_prefix = config.prefixes,
    activity = activity, 
    status = discord.Status.dnd,
    intents = intents#,help_command = None
)

#bot.remove_command('help')


async def logCmd(ctx, bot, args):

    log = 798411134877040671
    argsStr = " ".join(args)

    embed = discord.Embed(
        color = 0x2AF4C8,
        title = f"Command Used",
        description = f"**Command Used**: `{ctx.command}`\n**Args**:\n> {argsStr}\n**User**: <@{ctx.author.id}>\n**Guild Name**: {ctx.guild}\n**Guild ID**: {ctx.guild.id}\n**Channel**: <#{ctx.channel.id}>"
    )

    await bot.get_channel(log).send(embed = embed)


async def cmdFail(ctx, bot, args):

    log = 798411134877040671
    argsStr = " ".join(args)

    embed = discord.Embed(
        color = 0xFF0000,
        title = f"Command Failed!",
        description = f"Command Used**: `{ctx.command}`\nArgs:\n> {argsStr}\nUser: <@{ctx.author.id}>\nServer: {ctx.guild}\nChannel: <#{ctx.channel.id}>\nReason for failuren> Coming soon.."
    )

    await bot.get_channel(log).send(embed = embed)




#Initiate the bot
@bot.event
async def on_ready():
    print(f"{bot.user} has connected to Discord!")

    await bot.get_channel(791216444548579339).send("bot online")


@bot.event
async def on_message(message):

    # Reject other bots
    if message.author.bot == True:
        return


    # turn the message to lowercase before being processed as a command
    message.content = message.content.lower()

    # Process the message as a command, you must run this if ou want to use @bot.commands with the on messae event
    await bot.process_commands(message)



@bot.command(
    enabled = True,
    hidden = False,
    name = "wait",
    aliases = ["w"],
    brief = "waits a time in minutes",
    usage = f"{config.prefixes[0]}wait <time in minutes> <note>",
    help = f"Example:\n> {config.prefixes[0]}wait 45 beastmoon match ends"
)
async def _wait(ctx, *args):

    if args[0].isdigit():

        note = " ".join(args[1:])
        waitfor = (int(args[0]) - 5) * 60
        await ctx.send(f"I will remind you in {int(args[0]) - 5} minutes\nNote:\n> {note}")
        await asyncio.sleep(waitfor)

        await ctx.send(f"<@{ctx.author.id}> 5 minute warning\nNote:\n> {note}")

        await asyncio.sleep(180)

        await ctx.send(f"<@{ctx.author.id}> 2 minute warning\nNote:\n> {note}")

        await asyncio.sleep(120)
        
        await ctx.send(f"<@{ctx.author.id}> now\nNote:\n> {note}")

    else:
        await ctx.send(f"{args[0]} is not a digit")

@bot.command(
    name = "ping"
)
async def _ping(ctx, *args):

    await ctx.send(f"Pong! {round(bot.latency * 1000)}ms")


@bot.command(
    enabled = True,
    hidden = False,
    name = "newhelp",
    aliases = ["nh"],
    brief = "new help cmd"
)
async def _newHelp(ctx, *args):

    prefixes = ", ".join(config.prefixes)

    print(len(args))

    if len(args) == 0:

        embed = discord.Embed(
            title = ctx.author,
            color = await s.randomColour(),
            description = f"Bot Prefixes:\n> {prefixes.strip()}"
        )

        for cmd in bot.commands:

            if cmd.hidden == False:
                aliases = "`, `".join(cmd.aliases)
                embed.add_field(
                    name = f"`{cmd}`",
                    value = f"> {cmd.brief}\n> **Aliases**: `{aliases}`\n> Ex. {cmd.usage}\nEnabled: {cmd.enabled}",
                    inline = False
                )
    
        await ctx.send(embed = embed)

    else:
        joint = " ".join(args)

        print(joint)
        for cmd in bot.commands:
            print(cmd.hidden)

            if cmd.name.lower() == joint.lower() and cmd.hidden == False:

                aliases = "`, `".join(cmd.aliases)

                embed = discord.Embed(
                    title = f"Help page for {cmd.name}",
                    color = await s.randomColour(),
                    description = f"> {cmd.brief}\n> **Aliases**: `{aliases}`\n> Ex. {cmd.usage}"
                )

                await ctx.send(embed = embed)
            # have to reformat this so that the embed isn't send in the loop. Have the loop return talents, if the found array or something len() is 0, then send couldnt find msg
           # else:
            #    await ctx.send(f"Could not find command called: `{joint}`")
        

@bot.command(
    enabled = True,
    hidden = False,
    name = "firstgen",
    aliases = ["fg"],
    usage = "<body name>",
    brief = "returns the first gen stats of a specific pet body",
    help = f"."
)
async def _firstGen(ctx, *args):

    jsonFile = open("./utilities/bodydata.json")
    bodies = json.load(jsonFile)
    bodiesArr = bodies["pets"]

    talentsJson = open("./priorities/talents.json")
    talentsDB = json.load(talentsJson)

    joint = " ".join(args)

    joint = joint.strip()

    if "'" in joint:
        joint = joint.replace("'", "")

    found = []

    for body in bodiesArr:

        if joint.lower() in body['name'].replace("'", "").lower():
            found.append(body)

    if len(found) == 0:
        return await ctx.send(f"Found no matches from `{joint}`")
    else:
        c = 1
        for body in found:

            # Find the talent info for the pet
            poolArr = []
            for talent in body['talents']:

                if "'" in talent:
                    talent = talent.replace("'", "")
                if "-" in talent:
                    talent = talent.replace("-", " ")
                if "." in talent:
                    talent = talent.replace(".", "")

                for talDB in talentsDB:

                    if "-" in talDB['name']:
                        talDB['name'] = talDB['name'].replace("-", " ")
                    if "." in talDB['name']:
                        talDB['name'] = talDB['name'].replace(".", "")

                    if talDB['name'].replace("'", "").lower() == talent.lower():

                        tal = {
                            "name": talDB['name'],
                            "rank": talDB["rank"],
                            "url": talDB["url"],
                            "valid_url": talDB["valid_url"],
                            "locked": talDB["locked"],
                            "priority": talentsDB.index(talDB)
                        }

                        poolArr.append(tal)

            # Process the talents in to a message
            talentsArray = []
            for talent in poolArr:

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

            pool = "\n> ".join(talentsArray)

            print(body['max_stats']['strength'])

            statsMsg = f"**Stats**:\n> {body['max_stats']['strength']} <:Icon_Strength:802528770296250378>\n> {body['max_stats']['intellect']} <:Icon_Intellect:799225493626683472>\n> {body['max_stats']['agility']} <:Icon_Agility:802528770166620192>\n> {body['max_stats']['will']} <:Icon_Will:802528770358771732>\n> {body['max_stats']['power']} <:Icon_Power:802528770492858378>"
            
            wikiUrl = f'http://www.wizard101central.com/wiki/Pet:{body["name"].replace(" ", "_")}'

            page = requests.get(wikiUrl)

            soup = BeautifulSoup(page.content, "html.parser")

            #results = soup.find(id="mw-content-text")

            print(soup)



            embed = discord.Embed(
                title = f"First Gen {body['name']} Info",
                description = f"{statsMsg}\n\n**Pool**:\n> {pool}",
                color = await s.randomColour(),
                url = wikiUrl
            ).set_footer(
                text = f"Requested by {ctx.author} | Item {c} of {len(found)}."
            )
            c += 1
            await ctx.send(embed = embed)


@bot.command(
    enabled = True,
    hidden = False,
    name = "findbodybyname",
    aliases = ["fbn"],
    usage = "<body name>, <body name>, etc",
    brief = "seperate each body name with a comma",
    help = f"searches for information on specific bodies by name.\n**Example**:\n> {config.prefixes[0]}fbn marshfellow, hamster\nWill return information on the Marshfellow body and any body with \"hamster\" in their name."
)
async def _findBodyByName(ctx, *args):

    try:
        await body.byName(ctx, bot, args)
    except:
        await cmdFail(ctx, bot, args)
    else:
        await logCmd(ctx, bot, args)


@bot.command(
    enabled = True,
    hidden = True,
    name = "compare",
    aliases = ["comp"],
    usage = "<body name>, <body name>, etc",
    brief = "seperate each body name with a comma",
    help = f"searches for information on specific bodies by name.\n**Example**:\n> {config.prefixes[0]}fbn marshfellow, hamster\nWill return information on the Marshfellow body and any body with \"hamster\" in their name."
)
async def _compare(ctx, *args):

    try:
        await body.compare(ctx, bot, args)
    except:
        await cmdFail(ctx, bot, args)
    else:
        await logCmd(ctx, bot, args)


@bot.command(
    enabled = True,
    hidden = False,
    name = "talentsearch",
    aliases = ["ts", "talents"],
    usage = "<talent name>, <talent name>, etc",
    brief = "seperate each talent name with a comma",
    help = f"searches for data on one or more specific talents. Seperate each talent name with a comma.\n**Example**:\n> {config.prefixes[0]}search death dealer, spell-defying, giver\nWill return Death Dealer, Spell Defying, and all talents with the word \"giver\" in their name."
)
async def _search(ctx, *args):

    try:
        await findTalent.search(ctx, bot, args)
    except:
        await cmdFail(ctx, bot, args)
    else:
        await logCmd(ctx, bot, args)
 

@bot.command(
    enabled = True,
    hidden = False,
    name = "talentsbetween",
    aliases = ["tb", "between"],
    usage = "<talent 1>, <talent 2>, <rank>",
    brief = "searches for talents between two talents, rank is optional",
    help = "Searches for talents between two pre determined talents. Rank is optional.\n **Example**:\n> ts!tb "
)
async def _talentsbetween(ctx, *args):

    try:
        await findTalent.talentsBetween(ctx, bot, args)
    except:
        await cmdFail(ctx, bot, args)
    else:
        await logCmd(ctx, bot, args)



# Start the bot
bot.run(token)