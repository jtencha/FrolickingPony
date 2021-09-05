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
        #Ping
        @bot.command()
        async def ping(ctx):
            embed = discord.Embed(title = ":ping_pong: Pong!", description = f"{round(bot.latency * 1000)}ms", color = 0x009933)
            await ctx.send(embed = embed)

        #Invite command
        @bot.command()
        async def invite(ctx):
            embed = discord.Embed(title = "Invite RoboticPony", url = "https://discord.com/oauth2/authorize?bot_id=834799912507277312&permissions=243165293686&scope=bot", description = "Invite the bot with the link above!", color = 0x009933)
            await ctx.send(embed = embed)

        #Help list
        #Use numbers to navigate the menus
        #Defaults to ;commands 1 if no number is provided.
        @bot.command()
        async def help(ctx, type = "1"):
            if type == "1":
                embed = discord.Embed(title = "Avalible Commands:", description = "Commands marked with an * require permissions.\n\n", color = 0x009933)
                embed.add_field(name = "about [user]", value = "Get info about a user", inline = False)
                embed.add_field(name = "guetzali", value = "Guetzali moment", inline = False)
                embed.add_field(name = "help", value = "General overview of commands", inline = False)
                embed.add_field(name = "invite", value = "Invite RoboticPony", inline = False)
                embed.add_field(name = "ping", value = "Bot response time.", inline = False)
                embed.add_field(name = "poll [option] [option] [option] [option]", value = "Create a poll", inline = False)
                embed.add_field(name = "mute [user] [time] [reason]*", value = "Mute a user for a set time", inline = False)
                embed.add_field(name = "unmute [user] [reason]*", value = "Unmute a user", inline = False)
                embed.add_field(name = "kick [user] [reason]*", value = "Kicks a member.", inline = False)
                embed.add_field(name = "ban [user] [reason]*", value = "Bans a member.", inline = False)
                embed.add_field(name = "unban [user]*", value = "Unbans a member.", inline = False)
                embed.add_field(name = "Secret Command*", value = "Puts the bot to sleep.", inline = False)
                embed.add_field(name = "\n\nList 1 of 1", value = "\n\nAdministrator permissions are recommended for moderation.")
                await ctx.send(embed = embed)
            else:
                await ctx.send("`Invalid command.`")

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
                embed = discord.Embed(title = "About RoboticPony", description = "Version: 1.4.6.1\nDeveloped by: FamiliarNameMissing and discord.py", color = 0x009933)
                await ctx.send(embed = embed)

        #Function mute
        #Mutes a member forever and DMs them.


        @bot.event
        async def on_command_error(ctx, error):
            if isinstance(error, discord.ext.commands.MissingRequiredArgument):
                await ctx.send("`You did not include a user!`")
            elif isinstance(error, BotMissingPermissions):
                await ctx.send("`{0}`".format(error))
            else:
                await ctx.send("`{0}`".format(error))

        def setup(bot):
            bot.add_cog(Funcions(bot))

def setup(bot):
    bot.add_cog(Functions(bot))
