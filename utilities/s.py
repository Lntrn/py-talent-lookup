import random

async def randomColour():
    colours = [0x4dff58, 0x9740dd, 0x3455f9, 0xec7a22, 0x5dfdf3, 0xff0000, 0x3a2848, 0x3f798d, 0x86a15e, 0xabff66, 0xfbff14, 0x9fa073, 0x235333, 0x010698, 0xff00d4, 0x8c184c, 0x000000, 0x5865F2, 0x2f3136]
    return random.choice(colours)