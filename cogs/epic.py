import discord
from discord.ext import commands
from discord.ext.commands import bot_has_permissions, Bot, BotMissingPermissions, guild_only
from discord import Member
from secret import token
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
            await ctx.send(random.choice(["Sus", "Sussy", "AMOGUS", "I love amogus", "<:amogusmybeloved:889694808963162113>"]))
            await ctx.send(random.choice(["https://media.discordapp.net/attachments/727291251308757113/864568490626777119/image0-2-1-1-1-1-1-1.gif",
            "https://tenor.com/view/sus-amogus-diary-of-a-wimpy-kid-sussy-twerk-gif-21402922",
            "https://media.discordapp.net/attachments/547864105046769676/886434964479029279/de65d757-bbd8-4e7e-b0c7-7ac35d148b14.gif",
            ]))


def setup(bot):
    bot.add_cog(Epic(bot))
