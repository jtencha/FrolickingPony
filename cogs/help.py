import discord
from discord.ext import commands
from discord.ext.commands import bot_has_permissions, Bot, BotMissingPermissions, guild_only
from discord import Member
from secret import token
import os
import asyncio
import random

class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        #Help list
        #Use numbers to navigate the menus
        #Defaults to ;commands 1 if no number is provided.
        @bot.command()
        async def help(ctx, type = "1"):
            if type == "1":
                embed = discord.Embed(title = "RoboticPony Help Menu", description = "Use help [command] for specific information.", color = 0x009933)
                embed.add_field(name = "Commands: ", value = "`about` `guetzali` `help` `invite` `ping` `poll` `eightball` `embed`", inline = False)
                embed.add_field(name = "Mod Commands:", value = "`mute` `unmute` `kick` `ban` `unban`", inline = False)
                embed.add_field(name = "System:", value = "`sleep` `reset`", inline = False)
                embed.add_field(name = "\n\nList 1 of 1", value = "\nBot Version: Version: 1.4.7.3\nDeveloped by: FamiliarNameMissing and discord.py")
                await ctx.send(embed = embed)
            elif type == "about":
                embed = discord.Embed(title = "about", description = "Get information about a user.", color = 0x009933)
                embed.add_field(name = "Format:", value = "`about [user]`")
                embed.add_field(name = "Permissions Required:", value = "Send messages", inline = True)
                await ctx.send(embed = embed)
            elif type == "guetzali":
                embed = discord.Embed(title = "guetzali", description = "Guetzali Guetzali", color = 0x009933)
                embed.add_field(name = "Format:", value = "`guetzali`")
                embed.add_field(name = "Permissions Required:", value = "Send messages", inline = True)
                await ctx.send(embed = embed)
            elif type == "help":
                embed = discord.Embed(title = "help", description = "Display an overview of commands.", color = 0x009933)
                embed.add_field(name = "Format:", value = "`help (command)`")
                embed.add_field(name = "Permissions Required:", value = "Send messages", inline = True)
                await ctx.send(embed = embed)
            elif type == "invite":
                embed = discord.Embed(title = "invite", description = "Display link to invite the bot.", color = 0x009933)
                embed.add_field(name = "Format:", value = "`invite`")
                embed.add_field(name = "Permissions Required:", value = "Send messages", inline = True)
                await ctx.send(embed = embed)
            elif type == "ping":
                embed = discord.Embed(title = "ping", description = "Get the bot repsonse time.", color = 0x009933)
                embed.add_field(name = "Format:", value = "`ping`")
                embed.add_field(name = "Permissions Required:", value = "Send messages", inline = True)
                await ctx.send(embed = embed)
            elif type == "poll":
                embed = discord.Embed(title = "poll", description = "Create a poll.", color = 0x009933)
                embed.add_field(name = "Format:", value = "`poll [option] [option] (option) (option)`")
                embed.add_field(name = "Permissions Required:", value = "Manage messages, add reactions", inline = True)
                await ctx.send(embed = embed)
            elif type == "mute":
                embed = discord.Embed(title = "mute", description = "Mute a user for a set amount of time.", color = 0x009933)
                embed.add_field(name = "Format:", value = "`mute [user] (time) (reason)`")
                embed.add_field(name = "Permissions Required:", value = "Manage members, manage roles", inline = True)
                await ctx.send(embed = embed)
            elif type == "unmute":
                embed = discord.Embed(title = "unmute", description = "Unmute a user.", color = 0x009933)
                embed.add_field(name = "Format:", value = "`unmute [user] (reason)`")
                embed.add_field(name = "Permissions Required:", value = "Manage members, manage roles", inline = True)
                await ctx.send(embed = embed)
            elif type == "kick":
                embed = discord.Embed(title = "kick", description = "Kick a user.", color = 0x009933)
                embed.add_field(name = "Format:", value = "`kick [user] (reason)`")
                embed.add_field(name = "Permissions Required:", value = "Ban members", inline = True)
                await ctx.send(embed = embed)
            elif type == "ban":
                embed = discord.Embed(title = "ban", description = "Ban a user.", color = 0x009933)
                embed.add_field(name = "Format:", value = "`ban [user] (reason)`")
                embed.add_field(name = "Permissions Required:", value = "Ban members", inline = True)
                await ctx.send(embed = embed)
            elif type == "unban":
                embed = discord.Embed(title = "unban", description = "Unban a user (and return some errors while you're at it)", color = 0x009933)
                embed.add_field(name = "Format:", value = "`unban [user]`")
                embed.add_field(name = "Permissions Required:", value = "Ban members", inline = True)
                await ctx.send(embed = embed)
            elif type == "sleep":
                embed = discord.Embed(title = "sleep", description = "Goodnight, RoboticPony.", color = 0x009933)
                embed.add_field(name = "Format:", value = "`sleep`")
                embed.add_field(name = "Permissions Required:", value = "Send messages", inline = True)
                await ctx.send(embed = embed)
            elif type == "reset":
                embed = discord.Embed(title = "reset", description = "Reset the bot.", color = 0x009933)
                embed.add_field(name = "Format:", value = "`reset`")
                embed.add_field(name = "Permissions Required:", value = "Send messages", inline = True)
                await ctx.send(embed = embed)
            elif type == "eightball":
                embed = discord.Embed(title = "eightball", description = "Virtual eightball", color = 0x009933)
                embed.add_field(name = "Format:", value = "`eightball [question]`")
                embed.add_field(name = "Permissions Required:", value = "Send messages", inline = True)
                await ctx.send(embed = embed)
            elif type == "embed":
                embed = discord.Embed(title = "embed", description = "Epic embed fail", color = 0x009933)
                embed.add_field(name = "Format:", value = "`embed [title] [message]`")
                embed.add_field(name = "Permissions Required:", value = "Send messages", inline = True)
                await ctx.send(embed = embed)
            else:
                await ctx.send("`Invalid command.`")


def setup(bot):
    bot.add_cog(Help(bot))
