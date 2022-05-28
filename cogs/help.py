import discord
from discord.ext import commands
from discord.ext.commands import bot_has_permissions, Bot, BotMissingPermissions, guild_only
from discord import Member
import os
import asyncio
import random
from bot import isBanned

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
        @bot_has_permissions(manage_webhooks = True)
        async def help(ctx, type = "1"):
            if isBanned(str(ctx.message.author.id), 1) != False:
                await ctx.send(embed = isBanned(str(ctx.message.author.id)))
                return

            if type == "1":
                embed = discord.Embed(title = "Help Menu", description = "Use help [command] for specific information. Time suffixes are h, m, and d.", color = 0xff6633)
                embed.add_field(name = "Commands: ", value = "`about` | `amogus` | `avatar` | `block` | `contact` | `eightball` | `embed` | `guetzali` | `help` | `impersonate` | `invite` | `ping` | `poll` | `redpanda` | `sourcecode` | `stats` | `support` ", inline = False)
                embed.add_field(name = "Economy: ", value = "`work` | `balance` | `addmoney` | `removemoney` | `leaderboard` | `dice` | `daily`")
                embed.add_field(name = "Mod Commands:", value = "`clear` | `mute` | `unmute` | `kick` | `ban` | `tempban` | `unban` | `nick` | `blacklist` | `unblacklist` | `listblacklist`", inline = False)
                embed.add_field(name = "System:", value = "`sleep` | `reload` | `pack` | `unpack`| `uptime` | `printcontents` | `settings` | `changestatus` ", inline = False)
                embed.add_field(name = "\n\nList 1 of 1", value = "\nBot Version: Version: 1.9\nDeveloped by: PrancingPony#2112 and discord.py", inline = False)
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
            elif type == "amogus":
                await ctx.send(embed = help_template("amogus", "Sussy command", "`amogus`", "Send Messages"))
            elif type == "sourcecode":
                await ctx.send(embed = help_template("sourcecode", "Provides a link to the source code for this bot.", "`sourcecode`", "Send Messages"))
            elif type == "contact":
                await ctx.send(embed = help_template("contact", "Contact the bot developers.", "`contact [message]`", "Send messages"))
            elif type == "tempban":
                await ctx.send(embed = help_template("tempban", "Temporarily ban a member.", "`tempban [member] [time] (reason)`", "Ban Messages"))
            elif type == "avatar":
                await ctx.send(embed = help_template("avatar", "Display a member's avatar. Defaults to your own avatar.", "`avatar [member]`", "Send messages"))
            elif type == "redpanda":
                await ctx.send(embed = help_template("redpanda", "Redpanda <:pandaqop:942169694717239307>", "`redpanda`", "Send messages, upload images"))
            elif type == "stats":
                await ctx.send(embed = help_template("stats", "Server stats", "`stats`", "Send messages"))
            elif type == "blacklist":
                await ctx.send(embed = help_template("blacklist", "Ban a user from using the bot.", "`blacklist [member]`", "Send messages (owner only)"))
            elif type == "unblacklist":
                await ctx.send(embed = help_template("unblacklist", "Allow a banned user to use the bot.", "`unblacklist [member]`", "Send messages (owner only)"))
            elif type == "gibamdib":
                await ctx.send(embed = help_template("gibamdib", "Gib amdib role wo", "`gibamdib (remove)`", "Manage roles, send messages"))
            elif type == "listblacklist":
                await ctx.send(embed = help_template("listblacklist", "List all blacklisted users.", "`listblacklist`", "Send messages (owner only)"))
            elif type == "impersonate":
                await ctx.send(embed = help_template("impersonate", "Impersonate a user of your choosing", "`impersonate [user] [message]`", "Manage webhooks, send messages"))
            elif type == "clear":
                await ctx.send(embed = help_template("clear", "Clear x messages in a channel or clear messages from a certain user in the last x messages.", "`clear [number] (user)`", "Manage messages"))
            elif type == "block":
                await ctx.send(embed = help_template("block", "Block users from impersonating you.", "`block`", "Send messages"))
            elif type == "uptime":
                await ctx.send(embed = help_template("uptime", "Display uptime of the bot.", "`uptime`", "Send messages"))
            elif type == "work":
                await ctx.send(embed = help_template("work", "Work for digital currency", "`work`", "Send messages"))
            elif type == "balance":
                await ctx.send(embed = help_template("balance", "View your balance for a server", "`balance`", "Send messages"))
            elif type == "addmoney":
                await ctx.send(embed = help_template("addmoney", "Add money to a user's bank account", "`addmoney [user] [amount]`", "Administrator"))
            elif type == "removemoney":
                await ctx.send(embed = help_template("removemoney", "Remove money from a user's bank account", "`removemoney [user] [amount]`", "Administrator"))
            elif type == "leaderboard":
                await ctx.send(embed = help_template("leaderboard", "Shows the economic leaderboard of the server", "`leaderboard`", "Send messages"))
            elif type == "printcontents":
                await ctx.send(embed = help_template("printcontents", "Print the contents of a specific file", "`printcontents`", "Send messages (owner only)"))
            elif type == "dice":
                await ctx.send(embed = help_template("dice", "Gamble your life savings away", "`dice [amount]`", "Send messages"))
            elif type == "daily":
                await ctx.send(embed = help_template("daily", "Claim money daily", "`daily`", "Send messages"))
            elif type == "support":
                await ctx.send(embed = help_template("support", "Invite link to the FrolickingPony support server", "`support`", "Send messages"))
            elif type == "settings":
                await ctx.send(embed = help_template("settings", "Access server-based settings. Customize by adding the two fields.", "`settings (setting) (enable/disable)`", "Administrator"))
            elif type == "changestatus":
                await ctx.send(embed = help_template("changestatus", "Change the status of the bot.", "`changestatus [status]`", "Owner"))
            else:
                await ctx.send("{0} is not a recognized command.".format(type))

        @help.error
        async def lol(ctx, error):
            if isinstance(error, BotMissingPermissions):
                await ctx.send("I don't have permission to run this command! Required {0}".format(join(error.missing_perms)))
            else:
                embed = discord.Embed(title = ":x: Error", description = "{0}".format(error), color = 0xff0000)
                await ctx.send(embed = embed)

def setup(bot):
    bot.add_cog(Help(bot))
