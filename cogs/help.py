import discord
from discord.ext import commands
from discord.ext.commands import bot_has_permissions, Bot, BotMissingPermissions, guild_only
from discord import Member
import os
import asyncio
import random

class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        def help_template(command_name, desc, format, perms_req):
            embed = discord.Embed(title = command_name, description = desc, color = 0xff6633)
            embed.add_field(name = "Format:", value = format)
            embed.add_field(name = "Permissions Required:", value = perms_req, inline = True)
            return embed

        #provide specific info for a given command
        #plug and chug into the function above
        @bot.command(aliases = ["h"])
        async def help(ctx, type = "1"):
            if type == "1":
                embed = discord.Embed(title = "Help Menu", description = "Use help [command] for specific information. Time suffixes are h, m, and d.", color = 0xff6633)
                embed.add_field(name = "Commands: ", value = "`about` | `amogus` | `avatar` | `eightball` | `embed` | `guetzali` | `help` | `invite` | `ping` | `poll` | `redpanda` | `sourcecode` | `stats` | `suggest`", inline = False)
                embed.add_field(name = "Mod Commands:", value = "`mute` | `unmute` | `kick` | `ban` | `tempban` | `unban` | `nick` | `setnick` | `blacklist` | `unblacklist`", inline = False)
                embed.add_field(name = "System:", value = "`sleep` | `reload` | `pack` | `unpack`", inline = False)
                embed.add_field(name = "\n\nList 1 of 1", value = "\nBot Version: Version: 1.6.5\nDeveloped by: PrancingPony#2112 and discord.py", inline = False)
                await ctx.send(embed = embed)
            elif type == "about":
                await ctx.send(embed = help_template("about", "Get information about a user. Defaults to your own info.", "`about [user]`", "Send messages"))
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
                await ctx.send(embed = help_template("unban", "Unban a user", "`unban [user]`", "Ban members"))
            elif type == "sleep":
                await ctx.send(embed = help_template("sleep", "Sleep well, RoboticPony", "`sleep`", "Send messages (owner only)"))
            elif type == "reset":
                await ctx.send(embed = help_template("reload", "Reload the bot.", "`reload`", "Send messages (owner only)"))
            elif type == "eightball":
                await ctx.send(embed = help_template("eightball", "Virtual eightball", "`eightball`", "Send messages"))
            elif type == "embed":
                await ctx.send(embed = help_template("embed", "Epic embed fail", "`embed [title] (text)`", "Send messages"))
            elif type == "unpack":
                await ctx.send(embed = help_template("unpack", "Manually unpack cogs", "`unpack`", "Send messages (owner only)"))
            elif type == "pack":
                await ctx.send(embed = help_template("pack", "Manually pack away all cogs", "`pack`", "Send messages (owner only)"))
            elif type == "nick":
                await ctx.send(embed = help_template("nick", "Change a user's nickname - leave blank to reset", "`nickname [user] (nickname)`", "Manage nicknames"))
            elif type == "setnick":
                await ctx.send(embed = help_template("setnick", "Change a user's nickname for a set time and stop them from changing it.", "`setnick [user] [time] [nickname]`", "Manage nicknames, manage roles"))
            elif type == "amogus":
                await ctx.send(embed = help_template("amogus", "Sussy command", "`amogus`", "Send Messages"))
            elif type == "sourcecode":
                await ctx.send(embed = help_template("sourcecode", "Provides a link to the source code for this bot.", "`sourcecode`", "Send Messages"))
            elif type == "suggest":
                await ctx.send(embed = help_template("suggest", "Suggest feedback to bot developers.", "`suggest [message]`", "Send messages"))
            elif type == "tempban":
                await ctx.send(embed = help_template("tempban", "Temporarily ban a member.", "`tempban [member] [time] (reason)`", "Ban Messages"))
            elif type == "avatar":
                await ctx.send(embed = help_template("avatar", "Display a member's avatar. Defaults to your own avatar.", "`avatar [member]`", "Send messages"))
            elif type == "redpanda":
                await ctx.send(embed = help_template("redpanda", "Redpanda <:pandaqop:891098560387510272>", "`redpanda`", "Send messages, upload images"))
            elif type == "stats":
                await ctx.send(embed = help_template("stats", "Server stats", "`stats`", "Send messages"))
            elif type == "blacklist":
                await ctx.send(embed = help_template("blacklist", "Ban a user from using the bot.", "`blacklist [member]`", "Send messages (owner only)"))
            elif type == "unblacklist":
                await ctx.send(embed = help_template("unblacklist", "Allow a banned user to use the bot.", "`unblacklist [member]`", "Send messages (owner only)"))
            else:
                await ctx.send("{0} is not a vaild command!.".format(type))

def setup(bot):
    bot.add_cog(Help(bot))
