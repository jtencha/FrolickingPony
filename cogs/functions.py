import discord
from discord.ext import commands
from discord.ext.commands import bot_has_permissions, Bot, BotMissingPermissions, guild_only
from discord import Member
from secret import token
import os
import asyncio
import random

class Functions(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        @bot.command()
        async def guetzali(ctx):
            await ctx.send(random.choice(["Guetzali Guetzali",
            "https://media.discordapp.net/attachments/842447676414361620/843713059033710632/60a1f6f95aa22378467759.gif",
            "https://media.discordapp.net/attachments/404803931227553802/860570669322469377/quetzali.gif",
            "https://media.discordapp.net/attachments/863137688470814741/863936864054149140/makesweet-kxksih.gif",
            "https://media.discordapp.net/attachments/404803931227553802/859942873864994816/697995591921172532-8.gif"
            ]))

        #Bot response time
        @bot.command()
        async def ping(ctx):
            embed = discord.Embed(title = ":ping_pong: Pong!", description = f"{round(bot.latency * 1000)}ms", color = 0x009933)
            await ctx.send(embed = embed)

        #Invite command
        @bot.command()
        async def invite(ctx):
            embed = discord.Embed(title = "Invite RoboticPony", url = "https://discord.com/api/oauth2/authorize?client_id=834799912507277312&permissions=244239027318&scope=bot", description = "Invite the bot with the link above!", color = 0x009933)
            await ctx.send(embed = embed)

        @bot.command()
        @bot_has_permissions(manage_messages = True)
        async def poll(ctx, option_one, option_two, option_three = None, option_four = None):
            embed = discord.Embed(title = "Poll Created by {0}".format(ctx.message.author), description = "\n", color = 0x009933)
            embed.add_field(name = "1️⃣ Option One:", value = "{0}".format(option_one), inline = False)
            embed.add_field(name = "2️⃣ Option Two:", value = "{0}".format(option_two), inline = False)
            if option_three != None:
                embed.add_field(name = "3️⃣ Option Three:", value = "{0}".format(option_three), inline = False)
                if option_four != None:
                    embed.add_field(name = "4️⃣ Option Four:", value = "{0}".format(option_four), inline = False)

            #Inefficient, but it gets the job done. I'll make it prettier and less repetitive later.
            #Deletes the ;poll command typed by the user.
            await ctx.message.delete()
            poll = await ctx.send(embed = embed)
            await poll.add_reaction("1️⃣")
            await poll.add_reaction("2️⃣")
            if option_three != None:
                await poll.add_reaction("3️⃣")
                if option_four != None:
                    await poll.add_reaction("4️⃣")

        #Checking for garbage
        @poll.error
        async def denied(ctx, error):
            if isinstance(error, discord.ext.commands.MissingRequiredArgument):
                await ctx.send("You must include at least two choices!")
            else:
                await ctx.send("`{0}`".format(error))

        #Get information about a user - will return bot stuff if no user is provided
        @bot.command()
        async def about(ctx, member: discord.Member):
            embed = discord.Embed(title = "{0}".format(member), description = "User information:", color = 0x009933)
            embed.add_field(name = "Name:", value = member.name, inline = True)
            embed.add_field(name = "User ID:", value = member.id, inline = True)
            embed.add_field(name = "Highest Role:", value = member.top_role)
            embed.add_field(name = "Created Account:", value = member.created_at)
            embed.add_field(name = "Joined Server:", value = member.joined_at)
            embed.set_thumbnail(url = member.avatar_url)
            await ctx.send(embed = embed)

        @about.error
        async def incorrect(ctx, error):
            if isinstance(error, discord.ext.commands.MissingRequiredArgument):
                embed = discord.Embed(title = "About RoboticPony", description = "Version: 1.4.7.2\nDeveloped by: FamiliarNameMissing and discord.py", color = 0x009933)
                await ctx.send(embed = embed)
            else:
                await ctx.send("`{0}`".format(error))

def setup(bot):
    bot.add_cog(Functions(bot))
