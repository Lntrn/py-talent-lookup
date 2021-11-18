import discord
from discord.utils import get

whitelisted = [75030405218461865, 726978704391143485]


async def agentCheck(ctx, bot):

    tta = bot.get_guild(803061275865120778)
    print(tta)

    role = discord.utils.find(lambda r: r.id == 810654581574991872, tta.roles)

    user = tta.get_member(ctx.author.id)

    print(user)

    if user:
        if role in user.roles:
            return True
        else:
            return False
    else:
        return False