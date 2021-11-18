whitelisted = [750304052184612865, 726978704391143485, 341245605194104833]


def check(ctx):
    if ctx.author.id in whitelisted:
         return True
    else:
        return False