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

        def help_template(command_name, desc, format, perms_req):
            embed = discord.Embed(title = command_name, description = desc, color = 0x009933)
            embed.add_field(name = "Format:", value = format)
            embed.add_field(name = "Permissions Required:", value = perms_req, inline = True)
            return embed
        #Help list
        #Use numbers to navigate the menus
        #Defaults to ;commands 1 if no number is provided.
        @bot.command()
        async def help(ctx, type = "1"):
            if type == "1":
                embed = discord.Embed(title = "RoboticPony Help Menu", description = "Use help [command] for specific information.", color = 0x009933)
                embed.add_field(name = "Commands: ", value = "`about` `guetzali` `help` `invite` `ping` `poll` `eightball` `embed`", inline = False)
                embed.add_field(name = "Mod Commands:", value = "`mute` `unmute` `kick` `ban` `unban` `nick`", inline = False)
                embed.add_field(name = "System:", value = "`sleep` `reset` `pack` `unpack`", inline = False)
                embed.add_field(name = "\n\nList 1 of 1", value = "\nBot Version: Version: 1.4.7.3\nDeveloped by: FamiliarNameMissing and discord.py")
                await ctx.send(embed = embed)
            elif type == "about":
                #embed = discord.Embed(title = "about", description = "Get information about a user.", color = 0x009933)
                #embed.add_field(name = "Format:", value = "`about [user]`")
                #embed.add_field(name = "Permissions Required:", value = "Send messages", inline = True)
                await ctx.send(embed = help_template("about", "Get information about a user.", "`about [user]`", "Send messages"))
            elif type == "guetzali":
                await ctx.send(embed = help_template("guetzali", "Guetzali Guetzali", "`guetzali`", "Send messages"))
            elif type == "help":
                await ctx.send(embed = help_template("help", "Display an overview of commands.", "`help (command)`", "Send messages"))
            elif type == "invite":
                await ctx.send(embed = help_template("invite", "Display a link to invite the bot.", "`invite`", "Send messages"))
            elif type == "ping":
                await ctx.send(embed = help_template("ping", "Bot repsonse time", "`ping`", "Send messages"))
            elif type == "poll":
                await ctx.send(embed = help_template("poll", "Create a poll.", "`poll [option] [option] (option) (option)`", "Manage messages, add reactions"))
            elif type == "mute":
                await ctx.send(embed = help_template("mute", "Mute a user for a set time.", "`mute [user] (time) (reason)`", "Manage members, manage roles"))
            elif type == "unmute":
                await ctx.send(embed = help_template("unmute", "Unmute a user", "`unmute [user] (reason)`", "Manage members, manage roles"))
            elif type == "kick":
                await ctx.send(embed = help_template("kick", "Kick a user", "`kick [user] (reason)`", "Kick members"))
            elif type == "ban":
                await ctx.send(embed = help_template("ban", "Ban a user", "`ban [user] (reason)`", "Ban members"))
            elif type == "unban":
                await ctx.send(embed = help_template("unban", "Unban a user (and return some errors while you're at it)", "`unban [user]`", "Ban members"))
            elif type == "sleep":
                await ctx.send(embed = help_template("sleep", "Sleep well, RoboticPony", "`sleep`", "Send messages (owner only)"))
            elif type == "reset":
                await ctx.send(embed = help_template("reset", "Reset the bot.", "`reset`", "Send messages (owner only)"))
            elif type == "eightball":
                await ctx.send(embed = help_template("eightball", "Virtual eightball", "`eightball`", "Send messages"))
            elif type == "embed":
                await ctx.send(embed = help_template("embed", "Epic embed fail", "`embed [title] [message]`", "Send messages"))
            elif type == "unpack":
                await ctx.send(embed = help_template("unpack", "Manually unpack cogs", "`unpack`", "Send messages (owner only)"))
            elif type == "pack":
                await ctx.send(embed = help_template("pack", "Manually pack away all cogs", "`pack`", "Send messages (owner only)"))
            elif type == "nick":
                await ctx.send(embed = help_template("nick", "Change a user's nickname - leave blank to reset.", "`nickname [user] (nickname)", "Manage nicknames"))
            else:
                await ctx.send("`Invalid command.`")


def setup(bot):
    bot.add_cog(Help(bot))
