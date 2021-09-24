import discord
from discord.ext import commands
from discord.ext.commands import bot_has_permissions, Bot, BotMissingPermissions, guild_only
from discord import Member
import os
import asyncio
import random

class Epic(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        @bot.command()
        async def guetzali(ctx):
            await ctx.send(random.choice(["Guetzali Guetzali",
            "https://media.discordapp.net/attachments/842447676414361620/843713059033710632/60a1f6f95aa22378467759.gif",
            "https://media.discordapp.net/attachments/404803931227553802/860570669322469377/quetzali.gif",
            "https://media.discordapp.net/attachments/863137688470814741/863936864054149140/makesweet-kxksih.gif",
            "https://media.discordapp.net/attachments/404803931227553802/859942873864994816/697995591921172532-8.gif",
            "https://media.discordapp.net/attachments/842447676414361620/843713059033710632/60a1f6f95aa22378467759.gif",
            ]))

        @bot.command()
        async def amogus(ctx):
            embed = discord.Embed(title = random.choice(["Sus", "Sussy", "AMOGUS", "I love amogus", "{0} is sus".format(ctx.message.author)]), description = "\n", color = 0xff6633)
            embed.set_image(url = random.choice(["https://media.discordapp.net/attachments/727291251308757113/864568490626777119/image0-2-1-1-1-1-1-1.gif",
            "https://c.tenor.com/k_H-Sf-5D8IAAAAd/sus-amogus.gif",
            "https://media.discordapp.net/attachments/547864105046769676/886434964479029279/de65d757-bbd8-4e7e-b0c7-7ac35d148b14.gif",
            "https://c.tenor.com/XhYqu5fu4LgAAAAd/boiled-soundcloud-boiled.gif"]))
            msg = await ctx.send(embed = embed)

        @bot.command()
        async def redpanda(ctx):
            embed = discord.Embed(title = "Red Panda, My Beloved", description = "\n", color = 0xff6633)
            embed.set_image(url = random.choice(["https://cdn.discordapp.com/avatars/825212502978723861/c94bd91c4e02b1c9600418e7f8631157.png",
            "https://cdn.discordapp.com/attachments/866857228833128449/891099004446842880/redpanda.png",
            "https://cdn.discordapp.com/attachments/866857228833128449/891099410040229908/red-panda-3.png",
            "https://media.discordapp.net/attachments/866857228833128449/891099663250362398/OIP.png",
            "https://cdn.discordapp.com/attachments/866857228833128449/891100220560121856/OIP.png",
            "https://cdn.discordapp.com/attachments/866857228833128449/891100315544326144/OIP.png",
            "https://cdn.discordapp.com/attachments/866857228833128449/891100505693093938/OIP.png",
            "https://cdn.discordapp.com/attachments/866857228833128449/891100587259740190/OIP.png",
            "https://cdn.discordapp.com/attachments/866857228833128449/891100785260265502/red-pandas-cincinnati-zoo-3.png",
            "https://cdn.discordapp.com/attachments/866857228833128449/891101059190247444/OIP.png"
            ]))
            await ctx.send(embed = embed)

def setup(bot):
    bot.add_cog(Epic(bot))